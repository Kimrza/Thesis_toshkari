"""iri_net_preflight.py -- bounded network preflight and failure classification for the
Kaggle IRI-2016 verification notebook.

Purpose: before anything is installed, establish whether the package index and the
wheel host are reachable, stage by stage (DNS -> TCP -> TLS -> HTTPS), each stage under
its own timeout, and name the first stage that fails. Also classifies the stderr of a
failed install command into a small closed set so a report reader can tell a DNS
failure from a TLS failure from a hash mismatch without reading raw logs.

Inputs: host names and paths; a captured command's stdout/stderr/exit code.
Re-run behaviour: pure network probes and pure string classification; nothing is
written; the caller records the returned dicts.
"""
import socket
import ssl
import time
import urllib.error
import urllib.request

NETWORK_FAILURE_CLASSES = (
    "dns_failure", "tcp_timeout", "tcp_connect_failure", "tls_failure", "tls_timeout",
    "http_error", "http_timeout", "unknown",
)

# Possible causes are stated as possibilities. The preflight cannot see the Kaggle
# settings panel, so it never asserts that the Internet toggle is off.
POSSIBLE_CAUSES = {
    "dns_failure": "name resolution failed: possible causes include the Kaggle notebook's "
                   "Internet setting being OFF (Settings sidebar -> Internet), a DNS outage, "
                   "or a restricted network; this probe cannot tell these apart -- check the "
                   "Internet setting first, then re-run",
    "tcp_timeout": "the name resolved but no TCP connection completed within the timeout: "
                   "possible causes include a firewall, a proxy requirement, or an outage",
    "tcp_connect_failure": "the name resolved but the TCP connection was refused or reset: "
                           "possible causes include a firewall, a proxy requirement, or an outage",
    "tls_failure": "TCP connected but the TLS handshake or certificate validation failed: "
                   "possible causes include a TLS-intercepting proxy, a stale CA bundle, or a "
                   "clock error on the machine",
    "tls_timeout": "TCP connected but the TLS handshake did not complete within the timeout",
    "http_error": "TLS succeeded but the HTTPS request returned an error status: possible "
                  "causes include a blocked path, a proxy error page, or a service incident",
    "http_timeout": "TLS succeeded but the HTTPS response did not arrive within the timeout",
    "unknown": "an unclassified network error; see the recorded exception text",
}


def _elapsed(t0):
    return round(time.monotonic() - t0, 3)


def probe_host(host, port=443, path="/", timeout=10.0, expect_status=None):
    """DNS -> TCP -> TLS -> HTTPS GET, stopping at the first failing stage.

    Returns {"host", "port", "path", "ok", "stages": {...}, "failure_class"?, "error"?}.
    Every stage records its wall time; a failing stage records repr(exception).
    """
    out = {"host": host, "port": port, "path": path, "stages": {}, "ok": False}

    t0 = time.monotonic()
    try:
        infos = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
        addrs = sorted({i[4][0] for i in infos})
        out["stages"]["dns"] = {"ok": True, "addresses": addrs[:8], "seconds": _elapsed(t0)}
    except socket.gaierror as exc:
        out["stages"]["dns"] = {"ok": False, "error": repr(exc), "seconds": _elapsed(t0)}
        out["failure_class"] = "dns_failure"
        out["error"] = repr(exc)
        return out

    t0 = time.monotonic()
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
        out["stages"]["tcp"] = {"ok": True, "peer": list(sock.getpeername()[:2]), "seconds": _elapsed(t0)}
    except socket.timeout as exc:
        out["stages"]["tcp"] = {"ok": False, "error": repr(exc), "seconds": _elapsed(t0)}
        out["failure_class"] = "tcp_timeout"
        out["error"] = repr(exc)
        return out
    except OSError as exc:
        out["stages"]["tcp"] = {"ok": False, "error": repr(exc), "seconds": _elapsed(t0)}
        out["failure_class"] = "tcp_connect_failure"
        out["error"] = repr(exc)
        return out

    t0 = time.monotonic()
    try:
        ctx = ssl.create_default_context()
        sock.settimeout(timeout)
        tls = ctx.wrap_socket(sock, server_hostname=host)
        cert = tls.getpeercert() or {}
        subject = dict(x[0] for x in cert.get("subject", ())) if cert.get("subject") else {}
        out["stages"]["tls"] = {
            "ok": True, "version": tls.version(), "cipher": (tls.cipher() or ("",))[0],
            "peer_common_name": subject.get("commonName"), "not_after": cert.get("notAfter"),
            "seconds": _elapsed(t0),
        }
        tls.close()
    except socket.timeout as exc:
        out["stages"]["tls"] = {"ok": False, "error": repr(exc), "seconds": _elapsed(t0)}
        out["failure_class"] = "tls_timeout"
        out["error"] = repr(exc)
        sock.close()
        return out
    except (ssl.SSLError, ssl.CertificateError, OSError) as exc:
        out["stages"]["tls"] = {"ok": False, "error": repr(exc), "seconds": _elapsed(t0)}
        out["failure_class"] = "tls_failure"
        out["error"] = repr(exc)
        sock.close()
        return out

    t0 = time.monotonic()
    url = f"https://{host}{path}"
    req = urllib.request.Request(url, headers={"User-Agent": "iri-verification-preflight/3"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.status
            resp.read(4096)
        st = {"ok": True, "status": status, "seconds": _elapsed(t0)}
        if expect_status is not None and status != expect_status:
            st.update({"ok": False, "expected_status": expect_status})
            out["stages"]["https"] = st
            out["failure_class"] = "http_error"
            out["error"] = f"HTTP {status} from {url}, expected {expect_status}"
            return out
        out["stages"]["https"] = st
    except urllib.error.HTTPError as exc:
        st = {"ok": False, "status": exc.code, "error": repr(exc), "seconds": _elapsed(t0)}
        if expect_status is None:  # any HTTP answer proves the path end to end
            st["ok"] = True
            out["stages"]["https"] = st
        else:
            out["stages"]["https"] = st
            out["failure_class"] = "http_error"
            out["error"] = repr(exc)
            return out
    except urllib.error.URLError as exc:
        out["stages"]["https"] = {"ok": False, "error": repr(exc), "seconds": _elapsed(t0)}
        reason = exc.reason
        if isinstance(reason, socket.gaierror):
            out["failure_class"] = "dns_failure"
        elif isinstance(reason, (ssl.SSLError, ssl.CertificateError)):
            out["failure_class"] = "tls_failure"
        elif isinstance(reason, socket.timeout) or "timed out" in str(reason):
            out["failure_class"] = "http_timeout"
        else:
            out["failure_class"] = "unknown"
        out["error"] = repr(exc)
        return out
    except socket.timeout as exc:
        out["stages"]["https"] = {"ok": False, "error": repr(exc), "seconds": _elapsed(t0)}
        out["failure_class"] = "http_timeout"
        out["error"] = repr(exc)
        return out

    out["ok"] = True
    return out


def network_preflight(targets=None, timeout=10.0):
    """Probe each target in order; overall ok only if every target is ok.

    Default targets: the PyPI simple index page for iricore (must answer 200) and the
    wheel host (any HTTP answer accepted). Bounded: at most 4 stages x timeout per
    target.
    """
    if targets is None:
        targets = [
            {"host": "pypi.org", "path": "/simple/iricore/", "expect_status": 200},
            {"host": "files.pythonhosted.org", "path": "/", "expect_status": None},
        ]
    results = [probe_host(t["host"], path=t["path"], timeout=timeout, expect_status=t.get("expect_status"))
               for t in targets]
    failed = [r for r in results if not r["ok"]]
    summary = {"ok": not failed, "timeout_seconds_per_stage": timeout, "targets": results}
    if failed:
        first = failed[0]
        summary["failure_class"] = first.get("failure_class", "unknown")
        summary["failed_host"] = first["host"]
        summary["failed_stage"] = next((k for k, v in first["stages"].items() if not v.get("ok")), None)
        summary["error"] = first.get("error")
        summary["possible_causes"] = POSSIBLE_CAUSES.get(summary["failure_class"], POSSIBLE_CAUSES["unknown"])
    return summary


# ---- classifying a failed install command -------------------------------------------

COMMAND_FAILURE_CLASSES = (
    "none", "timeout", "dns_failure", "tls_failure", "connection_failure", "hash_mismatch",
    "platform_tag_mismatch", "resolution_failure", "missing_module", "unknown",
)

_DNS = ("Temporary failure in name resolution", "Name or service not known",
        "nodename nor servname provided", "getaddrinfo failed", "Name resolution failure")
_TLS = ("CERTIFICATE_VERIFY_FAILED", "certificate verify failed", "SSLError", "SSL: ",
        "TLSV1_ALERT", "WRONG_VERSION_NUMBER")
_HASH = ("THESE PACKAGES DO NOT MATCH THE HASHES", "Hashes are required in --require-hashes mode",
         "do not match the hashes")
_PLATFORM = ("is not a supported wheel on this platform", "not supported on this platform")
_CONN = ("Connection refused", "Connection reset", "NewConnectionError", "Max retries exceeded",
         "ProxyError", "Network is unreachable", "ReadTimeoutError", "ConnectTimeoutError")
_RESOLUTION = ("No matching distribution found", "Could not find a version that satisfies")


def classify_command_failure(stderr, stdout="", returncode=None, timed_out=False):
    """Map a failed command's output to one closed-set class. Order matters: a DNS
    failure also prints 'No matching distribution found', so network signatures are
    tested before resolution ones."""
    if timed_out:
        return "timeout"
    if returncode == 0:
        return "none"
    text = (stderr or "") + "\n" + (stdout or "")
    if any(s in text for s in _DNS):
        return "dns_failure"
    if any(s in text for s in _TLS):
        return "tls_failure"
    if any(s in text for s in _HASH):
        return "hash_mismatch"
    if any(s in text for s in _PLATFORM):
        return "platform_tag_mismatch"
    if any(s in text for s in _CONN):
        return "connection_failure"
    if any(s in text for s in _RESOLUTION):
        return "resolution_failure"
    if "No module named" in text:
        return "missing_module"
    return "unknown"
