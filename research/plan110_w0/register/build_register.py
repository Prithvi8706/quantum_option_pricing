"""Build the 110-item closure register from PLAN_110 v1 Appendix A + triage rows (R0, stdlib)."""
import hashlib, json, re, sys
from pathlib import Path
ROOT = Path.cwd()
PLAN = ROOT / 'docs/program_plan_20261010/supporting/PLAN_110_v1_draft.md'
ROWS = ROOT / 'docs/program_plan_20261010/supporting/triage_rows'
STATUS = ROOT / 'docs/limitation_program_20261001/STATUS.md'
OUT = ROOT / 'results/plan110_w0/register'
# Re-tiering adopted from the critiques and W0 results (PLAN_110_EFFICIENT.md section 2)
OVERRIDES = {
    'E02': ('T4', 'N1 headline scope input'), 'H03': ('T4', 'N1 headline scope input (cite H03 leaf ratio by SHA)'),
    'H04': ('T5', 'register only (zero-cost line held in triage row)'), 'H07': ('T5', 'register only'),
    'H14': ('T5', 'register only'), 'C08': ('T5', 'register only; no eps-extrapolated crossover planned'),
    'H16': ('T4', 'DONE in W0: 1-16 worker grid run001'), 'C02': ('T4', 'DONE in W0: bias desk + depth convention closed'),
}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
text = PLAN.read_text(encoding='utf-8')
app = text.split('## Appendix A', 1)[1]
table = {}
for line in app.splitlines():
    m = re.match(r'\|\s*([ACEFH]\d\d)\s*\|\s*(T\d)\s*\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|', line)
    if m:
        i, tier, wave, dep, cost, kill = (x.strip() for x in m.groups())
        table[i] = dict(tier=tier, wave_or_trigger=wave, key_dependency=dep, cost=cost, kill_or_defer=kill)
triage = {}
for f in sorted(ROWS.glob('rows_*.jsonl')):
    for l in f.read_text(encoding='utf-8').splitlines():
        r = json.loads(l); triage[r['id']] = r
status = {}
for l in STATUS.read_text(encoding='utf-8').splitlines():
    m = re.match(r'\|\s*([ACEFH]\d\d)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|', l)
    if m: status[m.group(1)] = (m.group(2), m.group(3))
assert set(table) == set(triage) == set(status) and len(table) == 110, (len(table), len(triage), len(status))
DISP = {'T1': 'decision-critical (W0 done)', 'T2': 'credited screen value / branch-A lever', 'T3': 'deferred certification debt',
        'T4': 'closed or folded into N1', 'T5': 'dormant until trigger', 'T6': 'parked: different task (TRIG-G0)'}
reg = []
for i in sorted(table):
    t = dict(table[i]); tr = triage[i]
    if i in OVERRIDES: t['tier'], t['wave_or_trigger'] = OVERRIDES[i]
    reg.append(dict(id=i, title=status[i][0], live_status=status[i][1], tier=t['tier'], disposition=DISP[t['tier']],
                    wave_or_trigger=t['wave_or_trigger'], key_dependency=t['key_dependency'], cost=t['cost'],
                    kill_or_defer=t['kill_or_defer'], inequality_lever=tr.get('inequality_lever'),
                    optimistic_max_factor=tr.get('optimistic_max_factor'), evidence='docs/limitation_program_20261001/STATUS.md row ' + i,
                    reopen_rule=t['kill_or_defer'], rigour_tier='R0 register record'))
assert len(reg) == 110 and len({r['id'] for r in reg}) == 110
OUT.mkdir(parents=True, exist_ok=True)
run = OUT / (sys.argv[1] if len(sys.argv) > 1 else 'run001'); run.mkdir(exist_ok=False)
meta = dict(inputs_sha256={str(p.relative_to(ROOT)): sha(p) for p in [PLAN, STATUS] + sorted(ROWS.glob('rows_*.jsonl'))},
            count=len(reg), tiers={k: sum(r['tier'] == k for r in reg) for k in DISP}, overrides=sorted(OVERRIDES))
with (run / 'register.json').open('x', encoding='utf-8') as f: json.dump(dict(meta=meta, items=reg), f, indent=1)
md = ['# 110-item closure register (plan110 W0, R0)', '', f"Count: {meta['count']}/110. Tiers: {meta['tiers']}.", '',
      '| ID | Title | Live status | Tier | Disposition | Wave / trigger | Reopen / kill rule |', '|---|---|---|---|---|---|---|']
for r in reg:
    md.append(f"| {r['id']} | {r['title']} | {r['live_status']} | {r['tier']} | {r['disposition']} | {r['wave_or_trigger']} | {r['reopen_rule']} |")
with (run / 'REGISTER.md').open('x', encoding='utf-8') as f: f.write('\n'.join(md) + '\n')
print(json.dumps(meta, indent=1))
