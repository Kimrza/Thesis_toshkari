"""Focused checks for iri_net_preflight and iri_index_checks (synthetic failures + real files)."""
import json
import socket
import ssl
import sys
import threading
import time

import iri_index_checks as X
import iri_net_preflight as N

results = {}

# ---- network preflight: real path (Internet ON here) ---------------------------------
ok = N.network_preflight(timeout=10.0)
results["real_preflight_ok"] = ok["ok"]
results["real_preflight_stages"] = {t["host"]: list(t["stages"]) for t in ok["targets"]}
assert ok["ok"], ok

# ---- synthetic: DNS failure ---------------------------------------------------------
r = N.probe_host("nonexistent-host.invalid", path="/", timeout=5)
assert not r["ok"] and r["failure_class"] == "dns_failure", r
results["synthetic_dns"] = r["failure_class"]
s = N.network_preflight([{"host": "nonexistent-host.invalid", "path": "/", "expect_status": None}], timeout=5)
assert s["failure_class"] == "dns_failure" and s["failed_stage"] == "dns" and "possible causes" in s["possible_causes"]
assert "Internet setting being OFF" in s["possible_causes"] and "cannot tell these apart" in s["possible_causes"]

# ---- synthetic: TCP refused (a local port nobody listens on) --------------------------
probe = socket.socket(); probe.bind(("127.0.0.1", 0)); free_port = probe.getsockname()[1]; probe.close()
r = N.probe_host("127.0.0.1", port=free_port, path="/", timeout=5)
assert not r["ok"] and r["failure_class"] == "tcp_connect_failure", r
results["synthetic_tcp_refused"] = r["failure_class"]

# ---- synthetic: TCP accepted but no TLS (plain server that says nothing / or garbage) --
srv = socket.socket(); srv.bind(("127.0.0.1", 0)); srv.listen(1); port = srv.getsockname()[1]

def _serve_garbage():
    c, _ = srv.accept()
    try:
        c.recv(1024)
        c.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n")  # plain HTTP answer to a TLS ClientHello
    finally:
        c.close()

t = threading.Thread(target=_serve_garbage, daemon=True); t.start()
r = N.probe_host("127.0.0.1", port=port, path="/", timeout=5)
assert not r["ok"] and r["failure_class"] == "tls_failure", r
assert r["stages"]["tcp"]["ok"] is True
results["synthetic_tls_failure"] = r["failure_class"]
srv.close()

# ---- synthetic: HTTP status mismatch ---------------------------------------------------
r = N.probe_host("pypi.org", path="/simple/this-package-does-not-exist-xyz123/", timeout=10, expect_status=200)
assert not r["ok"] and r["failure_class"] == "http_error" and r["stages"]["tls"]["ok"], r
results["synthetic_http_error"] = r["stages"]["https"].get("status")

# ---- command failure classifier -----------------------------------------------------
kaggle_run3_stderr = ("...after connection broken by 'NewConnectionError(...: Failed to establish a new connection: "
                      "[Errno -3] Temporary failure in name resolution')': /simple/virtualenv/\n"
                      "ERROR: Could not find a version that satisfies the requirement virtualenv (from versions: none)\n"
                      "ERROR: No matching distribution found for virtualenv")
cases = [
    (dict(stderr=kaggle_run3_stderr, returncode=1), "dns_failure"),
    (dict(stderr="", returncode=None, timed_out=True), "timeout"),
    (dict(stderr="", returncode=0), "none"),
    (dict(stderr="ERROR: THESE PACKAGES DO NOT MATCH THE HASHES FROM THE REQUIREMENTS FILE.", returncode=1), "hash_mismatch"),
    (dict(stderr="ERROR: iricore-1.8.0-cp310-cp310-manylinux_2_35_x86_64.whl is not a supported wheel on this platform.", returncode=1), "platform_tag_mismatch"),
    (dict(stderr="WARNING: Retrying ... SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed'))", returncode=1), "tls_failure"),
    (dict(stderr="ERROR: No matching distribution found for iricore==1.8.0", returncode=1), "resolution_failure"),
    (dict(stderr="/usr/bin/python3: No module named virtualenv", returncode=1), "missing_module"),
    (dict(stderr="ProxyError('Cannot connect to proxy.')", returncode=1), "connection_failure"),
    (dict(stderr="something else entirely", returncode=2), "unknown"),
]
for kw, want in cases:
    got = N.classify_command_failure(**kw)
    assert got == want, (kw, got, want)
results["classifier_cases"] = len(cases)

# ---- index checks on the real installed (wheel) and historical files ------------------
inst = X.parse_apf107(open("wheel/apf107.dat", encoding="ascii").read())
hist = X.parse_apf107(open("wheel/apf107_hist.dat", encoding="ascii").read())
gi = X.parse_ig_rz(open("wheel/ig_rz.dat", encoding="ascii").read())
gh = X.parse_ig_rz(open("wheel/ig_rz_hist.dat", encoding="ascii").read())
assert X.apf107_summary(inst)["last_date"] == "2024-03-06" and X.apf107_summary(hist)["last_date"] == "2024-06-17"
assert gi["update_date_month_day_year"] == "2024-03-07" and gh["update_date_month_day_year"] == "2024-06-18"
sa = X.apf107_support_check(inst); assert sa["ok"], sa
sg = X.ig_rz_support_check(gi); assert sg["ok"], sg
ca = X.compare_apf107(inst, hist); assert ca["support_window_dates_with_any_value_difference"] == [] and ca["common_dates_with_any_value_difference"] == 176
cg = X.compare_ig_rz(gi, gh); assert cg["required_months_with_any_value_difference"] == [] and len(cg["common_months_with_any_value_difference"]) == 15
# tcon index arithmetic: value 1 is 1957-12, value 804 is 2024-11
assert gi["months"][0] == (1957, 12) and gi["months"][-1] == (2024, 11) and len(gi["months"]) == 804
# the smoke-date regex of revision 2 and the parser agree on the last date
import re
last_line = [l for l in open("wheel/apf107.dat", encoding="ascii").read().splitlines() if l.strip()][-1]
m = re.match(r"\s*(\d{2})\s*(\d{1,2})\s*(\d{1,2})", last_line); yy, mm, dd = (int(x) for x in m.groups())
assert (2000 + yy, mm, dd) == (2024, 3, 6)
results["index_checks"] = "ok"

# ---- synthetic index failures ---------------------------------------------------------
# apf107 truncated so the 365-day window and the direct rows are missing -> ok False
short = [r for r in inst if r["date"].year <= 2022 and not (r["date"].year == 2022 and r["date"].month == 12)]
s2 = X.apf107_support_check(short)
assert not s2["ok"] and s2["direct_read_rows_missing"][0] == X.dt.date(2022, 12, 1).isoformat() and not s2["centered_365d_window_inside_file"]
assert s2["direct_read_rows_required"]["count"] == 367 and s2["direct_read_rows_required"]["end_exclusive"] == "2023-01-01"
# a negative sentinel inside the direct window -> flagged
bad = [dict(r) for r in inst]; bad[[i for i, r in enumerate(bad) if r["date"].isoformat() == "2022-05-05"][0]]["f107d"] = -11.0
s3 = X.apf107_support_check(bad); assert s3["direct_read_rows_with_negative_sentinel"] == ["2022-05-05"] and not s3["ok"]
# ig_rz with an update date too early for the last required month's window -> ok False
early = dict(gi); early["update_date_month_day_year"] = "2023-05-01"
s4 = X.ig_rz_support_check(early); assert not s4["ok"] and not s4["update_date_at_or_after_that_window"]
# ig_rz truncated before 2023-01 -> months_missing
trunc = dict(gi); n = gi["months"].index((2022, 12)) + 1
trunc.update(months=gi["months"][:n], ig12=gi["ig12"][:n], rz12=gi["rz12"][:n])
s5 = X.ig_rz_support_check(trunc); assert s5["months_missing"] == ["2023-01"] and not s5["ok"]
assert sg["months_required"] == {"first": "2021-12", "last": "2023-01", "count": 14}
# malformed apf107 line -> ValueError
try:
    X.parse_apf107(" 22  1  1 12 3\n"); raise AssertionError("expected ValueError")
except ValueError:
    pass
results["synthetic_index_failures"] = 5

print(json.dumps(results, indent=1))
print("ALL MODULE CHECKS PASSED")
