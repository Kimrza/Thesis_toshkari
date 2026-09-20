"""Revision-3 notebook checks, run locally (no Kaggle, no iricore):
  A. inner script failure path (iricore absent) -> ok:false, failed_stage import_iricore, exit 1
  B. inner script end to end against a stub iricore carrying the REAL 1.8.0 wheel index
     files -> metadata/support fields populated, smoke-date cross-check passes, ok:true
  C. outer cells 1 + 5 (helpers + preflight) exec'd with the bundle dir redirected:
     run() classifies synthetic failures; preflight stop path writes the bundle and raises
  D. reconciliation cell (16) asserts pass on B's output and fail on a doctored one
"""
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path('C:/Users/LOTUS/Desktop/Thesis_toshkari')
nb = json.loads((REPO / 'kaggle/kaggle_iri2016_verification.ipynb').read_text(encoding='utf-8'))
cells = nb['cells']
inner = (HERE / 'rev3_inner.py').read_text(encoding='utf-8')
res = {}

# ---- A: failure path ------------------------------------------------------------------
env = dict(os.environ, PYTHONPATH=str(HERE / 'empty'))
(HERE / 'empty').mkdir(exist_ok=True)
pa = subprocess.run([sys.executable, str(HERE / 'rev3_inner.py')], capture_output=True, text=True, env=env, cwd=HERE / 'empty')
outA = json.loads(pa.stdout.strip().splitlines()[-1])
assert pa.returncode == 1 and outA['ok'] is False and outA['failed_stage'] == 'import_iricore', (pa.returncode, outA)
res['A_failure_path'] = outA['failed_stage']

# ---- B: stub iricore with the real wheel index files ----------------------------------
stub = HERE / 'stub_site' / 'iricore'
(stub / 'data' / 'index').mkdir(parents=True, exist_ok=True)
(stub / '__init__.py').write_text(
    "def vtec(dt, lat, lon, hbot=90.0, htop=2000.0, hstep=0.5, version=20, **kw):\n"
    "    assert version == 16 and htop == 2000.0\n"
    "    return [37.373754526924806]  # length-1 sequence, as iricore returns for scalar lat/lon\n", encoding='utf-8')
(stub / 'config.py').write_text("IRI_VERSIONS = [16, 20]\nDEFAULT_IRI_VERSION = 20\n", encoding='utf-8')
for f in ('apf107.dat', 'ig_rz.dat'):
    (stub / 'data' / 'index' / f).write_bytes((HERE / 'wheel' / f).read_bytes())
# fake dist metadata so importlib.metadata.version('iricore') answers
di = HERE / 'stub_site' / 'iricore-1.8.0.dist-info'; di.mkdir(exist_ok=True)
(di / 'METADATA').write_text("Metadata-Version: 2.1\nName: iricore\nVersion: 1.8.0\n", encoding='utf-8')
env = dict(os.environ, PYTHONPATH=str(HERE / 'stub_site'))
pb = subprocess.run([sys.executable, str(HERE / 'rev3_inner.py')], capture_output=True, text=True, env=env, cwd=HERE)
assert pb.returncode == 0, pb.stderr[-2000:]
outB = json.loads(pb.stdout.strip().splitlines()[-1])
assert outB['ok'] is True and outB['_stage'] == 'done', outB
ix = outB['index_files']
assert ix['sha256_before']['apf107.dat'] == 'cdf4d5dffe6d05eaae9ed90532cddea4c3cf2fdad255d837e660018cae60e674'
assert ix['sha256_before']['ig_rz.dat'] == 'fbbed3049483ac445070cc63841b7d14aa2929894eb725bdf946889840a41486'
assert ix['apf107']['summary']['last_date'] == '2024-03-06' and ix['apf107']['summary']['rows'] == 24172
assert ix['apf107']['summary']['contiguous_daily'] is True
assert ix['apf107']['support_2022']['ok'] is True and ix['apf107']['support_2022']['centered_means_recomputed_rows'] == 365
assert ix['ig_rz']['summary']['update_date_month_day_year'] == '2024-03-07'
assert ix['ig_rz']['summary']['range_last_month'] == '2024-10' and ix['ig_rz']['summary']['value_count_each'] == 804
assert ix['ig_rz']['support_2022']['ok'] is True and ix['ig_rz']['support_2022']['months_missing'] == []
assert ix['last_covered_date_in_apf107'] == '2024-03-06' and outB['smoke_test_timestamp_utc'] == '2024-01-06T12:00:00'
assert outB['smoke_test']['repeatable_bit_identical'] and ix['unchanged_after_smoke_test']
res['B_stub_end_to_end'] = {'stage': outB['_stage'], 'apf107_last': ix['apf107']['summary']['last_date'],
                            'ig_rz_update': ix['ig_rz']['summary']['update_date_month_day_year']}

# ---- C: outer helpers + preflight cell, bundle dir redirected -------------------------
work = HERE / 'rev3_work'
if work.exists():
    import shutil; shutil.rmtree(work)
work.mkdir()
c1 = ''.join(cells[1]['source']).replace("Path('/kaggle/working/iri_verification_bundle')", f"Path({str(work / 'bundle')!r})") \
                                 .replace("Path('/kaggle/working/iri_venv')", f"Path({str(work / 'venv')!r})") \
                                 .replace("Path('/kaggle/working/iri_verification_bundle.zip')", f"Path({str(work / 'bundle.zip')!r})")
assert '/kaggle/working' not in c1
g = {}
exec(c1, g)
c5 = ''.join(cells[5]['source'])
pre, post = c5.split("report['network_preflight'] = network_preflight(timeout=10.0)")
exec(pre, g)  # module part only: defines network_preflight + classify_command_failure
assert 'classify_command_failure' in g and 'network_preflight' in g
# run(): synthetic dns failure, timeout, success
e1 = g['run']([sys.executable, '-c', "import sys; sys.stderr.write('Temporary failure in name resolution'); sys.exit(1)"])
assert e1['failure_class'] == 'dns_failure' and e1['returncode'] == 1, e1
e2 = g['run']([sys.executable, '-c', "import time; time.sleep(5)"], timeout=1)
assert e2['timed_out'] is True and e2['returncode'] is None and e2['failure_class'] == 'timeout', e2
e3 = g['run']([sys.executable, '-c', "print('ok')"])
assert e3['returncode'] == 0 and 'failure_class' not in e3
# preflight stop branch with an unreachable target: bundle written, RuntimeError raised
g['report']['network_preflight'] = g['network_preflight']([{'host': 'nonexistent-host.invalid', 'path': '/', 'expect_status': None}], timeout=5)
try:
    exec(post.replace("report['network_preflight']['ok']", "report['network_preflight']['ok']"), g)
    raise AssertionError('expected RuntimeError from save_and_stop')
except RuntimeError as exc:
    msg = str(exc)
assert msg.startswith('STOPPED: network preflight failed before any install') and "class 'dns_failure'" in msg and 'possible causes' in msg, msg
rep = json.loads((work / 'bundle' / 'verification_report.json').read_text(encoding='utf-8'))
assert rep['ok'] is False and rep['stopped_reason'].startswith('network preflight failed') and rep['notebook_revision'] == 3
assert rep['network_preflight']['failure_class'] == 'dns_failure' and rep['network_preflight']['failed_stage'] == 'dns'
assert zipfile.ZipFile(work / 'bundle.zip').namelist() == ['verification_report.json']
# real preflight passes here (Internet ON on this machine)
g['report']['network_preflight'] = g['network_preflight'](timeout=10.0)
assert g['report']['network_preflight']['ok'] is True
res['C_outer'] = {'dns_class': e1['failure_class'], 'timeout_class': e2['failure_class'], 'stop_msg_head': msg[:60]}

# ---- D: reconciliation cell on B's output, then on a doctored one ---------------------
c16 = ''.join(cells[16]['source'])
g2 = {'verification': outB, 'report': {}, 'json': json}
exec(c16, g2)
assert g2['report']['reconciliation_passed'] is True
bad = json.loads(json.dumps(outB)); bad['index_files']['ig_rz']['support_2022']['ok'] = False
try:
    exec(c16, {'verification': bad, 'report': {}, 'json': json}); raise AssertionError('expected AssertionError')
except AssertionError as exc:
    assert 'ig_rz.dat does not cover' in str(exc), str(exc)
res['D_reconciliation'] = 'pass-on-good, fail-on-doctored'

print(json.dumps(res, indent=1))
print('ALL REVISION-3 CHECKS PASSED')
