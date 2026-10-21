"""Fixed metadata/citation audit; no pricing, quantum or hardware execution."""
import time
START = time.monotonic()
import argparse
import copy
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OUT = ROOT / 'results/independent_110_20261004/C15/run001'
CORPUS = [
    'docs/independent_110_20261004/inventory_run001/WORK_LIST.txt',
    'docs/limitation_audit_20261001/implementation_plan/roadmap.json',
    'manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md',
    'docs/limitation_audit_20261001/ESTIMATION_AND_CERTIFICATION.md',
    'docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md',
    'docs/research_investigation/2026-09-23/ERRATA.md',
    'docs/research_investigation/2026-09-23/SCREENING_TABLE.md',
    'docs/independent_110_20261004/F18/NESTED_ASSUMPTIONS.txt',
    'results/independent_110_20261004/F18/run001/protocol.json',
    'research/independent_110_20261004/F18/nested_theorem_map_v1.py',
    'research/independent_110_20261004/F18/primary_sources/Sun_Wang_Blanchet_2602_08120v1.html',
    'results/limitation_program_20261001/H17_demand_run002/protocol.json',
    'results/limitation_program_20261001/H17_demand_run002/summary.json',
    'results/limitation_program_20261001/H17_demand_run002/hardware_provenance.json',
    'results/limitation_program_20261001/H17_demand_run002/manifest.json',
    'results/limitation_program_20261001/H17_demand_run002/B4x12/hardware_demand.json',
    'results/limitation_program_20261001/H17_demand_run002/B8x52/hardware_demand.json',
    Path(__file__).resolve().relative_to(ROOT).as_posix(),
]
PRIMARY = {
    'sun_v1.html': 'https://arxiv.org/html/2602.08120v1',
    'sun_pmlr.html': 'https://proceedings.mlr.press/v306/sun26ap.html',
    'fowler_v3.pdf': 'https://arxiv.org/pdf/1210.4626v3',
    'litinski_v1.pdf': 'https://arxiv.org/pdf/2211.15465v1',
    'cultivation_v1.html': 'https://arxiv.org/html/2409.17595v1',
    'fast_curious_v1.pdf': 'https://arxiv.org/pdf/2510.26078v1',
}

def require(value, message):
    if not value:
        raise ValueError(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def write(path, value):
    raw = (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()
    with path.open('xb') as f:
        f.write(raw)

def pins():
    return {key: sha((ROOT/key).read_bytes()) for key in CORPUS}

def prepare():
    require(not OUT.exists(), 'Fresh C15 namespace')
    bound = pins()
    require(sum((ROOT/key).stat().st_size for key in CORPUS) <= 16*2**20, '16MiB local metadata cap')
    OUT.mkdir(parents=True)
    write(OUT/'protocol.json', {
        'schema': 'c15-fixed-next-reference-audit-v1', 'corpus_sha256': bound,
        'primary_urls': PRIMARY, 'priority_next_work': ['F18 existing compound theorem map', 'H03 native multiply-add reaction interface using H17 original72/F40 rows'],
        'assumptions': ['Current reference versions are metadata, not historical source adoption.',
            'Conference metadata and frozen arXiv theorem text are separate evidence.',
            'Primary reading can support a conditional theorem/interface, never a free physical or pricing cost.',
            'Historical hardware, compiled-timing and screen rows remain unrefreshed unless their exact evidence is checked.'],
        'acceptance': ['Store title, exact version/date or explicit unresolved version, claim, primary/local locator, assumptions and transfer conditions.',
            'Classify every original section3 hardware anchor and compiled-circuit timing, and every archived screening-table decision row.',
            'Check selected H17 count metadata and all unresolved physical fields without reexecuting hardware or arithmetic.',
            'Six fixed negative controls reject absent version, absent locator, cost from an unverified row, conference-to-theorem substitution, full-hardware claim and exhaustive-screen claim.',
            'All frozen local bytes rechecked; selected primary snapshot results, failures and exact owned hashes retained.'],
        'budgets': {'local_CPU_seconds': 30, 'local_script_wall_seconds': 90, 'primary_URL_count': 6,
            'URL_attempts_each': 1, 'network_timeout_seconds_each': 30,
            'primary_fetch_script_wall_seconds': 90, 'individual_primary_bytes': 8*2**20,
            'total_primary_bytes': 32*2**20, 'new_owned_bytes': 40*2**20},
        'stop': 'One selected-source pass and one finite inventory check. No source-search expansion, theorem proof experiment, timing benchmark, backend, target or contract change. Missing primary evidence excludes its number from accepted costs. Preserve failures.',
        'new_fixture_credit': 0, 'source_adoption': False, 'quantum_advantage': False,
    })
    print(json.dumps({'prepared':True,'protocol_sha256':sha((OUT/'protocol.json').read_bytes()),'local_files':len(bound)}))

def collect(expected):
    raw=(OUT/'protocol.json').read_bytes()
    require(sha(raw)==expected, 'Frozen protocol')
    require(not (OUT/'primary_sources').exists(), 'One fixed fetch pass')
    require(pins()==json.loads(raw)['corpus_sha256'], 'Fresh frozen local bytes')
    directory=OUT/'primary_sources'; directory.mkdir()
    def fetch(item):
        name,url=item
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'local-primary-citation-audit/1.0'}),timeout=30) as f:
                data=f.read(8*2**20+1)
                require(len(data)<=8*2**20,'Fixed8MiB response cap')
                return name, data, {'url':url,'resolved_url':f.url,'http_status':f.status,'bytes':len(data),'sha256':sha(data),'retrieved':True}
        except Exception as error:
            return name,None,{'url':url,'retrieved':False,'error_type':type(error).__name__,'error':str(error),'accepted_pricing_cost':None}
    with ThreadPoolExecutor(max_workers=3) as pool:
        rows=list(pool.map(fetch,PRIMARY.items()))
    require(time.monotonic()-START <90,'Primary-fetch script90wall cap')
    require(sum(len(raw or b'') for _,raw,_ in rows)<=32*2**20,'Total primary snapshot cap')
    records={}
    for name,raw,record in rows:
        if raw is not None:
            with (directory/name).open('xb') as f:f.write(raw)
        records[name]=record
    write(OUT/'primary_retrieval.json',records)
    print(json.dumps({'fixed_attempts':len(rows),'retrieved':sum(r['retrieved'] for r in records.values()),'failed':sum(not r['retrieved'] for r in records.values())}))

def validate(rows):
    require(rows and len({r['id'] for r in rows})==len(rows),'Unique claim inventory')
    for row in rows:
        require(all(row.get(k) for k in ('title','version_or_date','claim','locator','assumptions','transfer_conditions','status')), 'Required exact-or-unresolved evidence fields')
        require(row.get('accepted_pricing_cost') is None, 'No physical/pricing cost admitted in this interface audit')
        require(row.get('theorem_from_conference_metadata') is False,'No conference metadata theorem substitution')
        require(row.get('complete_hardware_certificate') is False,'No full hardware transfer')
        require(row.get('exhaustive_screen') is False,'Selected screen is not exhaustive')

def historical_rows():
    records=[]
    path=ROOT/'manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md'
    lines=path.read_text(encoding='utf-8').splitlines(); active=False; count=0
    for number,line in enumerate(lines,1):
        if line.startswith('| Anchor |'):active=True;continue
        if active:
            if not line.startswith('|'):break
            if line.startswith('|---'):continue
            count+=1;records.append({'id':f'HW{count:02d}','category':'hardware_anchor','line':number,'text':line,
                'locator':path.relative_to(ROOT).as_posix()+f':{number}'})
    timing=next((i for i,line in enumerate(lines,1) if '3.7 days per single circuit' in line),None)
    require(timing is not None,'Original compiled-circuit timing locator')
    records.append({'id':'COMPILED01','category':'compiled_timing','line':timing,'text':lines[timing-1],
        'locator':path.relative_to(ROOT).as_posix()+f':{timing}'})
    path=ROOT/'docs/research_investigation/2026-09-23/SCREENING_TABLE.md'; count=0
    for number,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
        if not line.startswith('|') or line.startswith('|---') or line.startswith('| Lane |'):continue
        count+=1;records.append({'id':f'SCREEN{count:03d}','category':'source_screen','line':number,'text':line,
            'locator':path.relative_to(ROOT).as_posix()+f':{number}'})
    require(count>0,'Archived source-screen corpus')
    return records

def seal(expected,release):
    require(not (OUT/'RUN_STARTED.json').exists(),'One metadata invocation')
    require(sha((OUT/'protocol.json').read_bytes())==expected,'Frozen protocol')
    require(sha((HERE/'claims_v1.json').read_bytes())==release,'Frozen author claim table')
    write(OUT/'RUN_STARTED.json',{'protocol_sha256':expected,'claims_sha256':release,'new_scientific_checks':0})
    write(OUT/'FAILED_UNSEALED.json',{'passed':False,'provisional':True})
    try:
        require(pins()==json.loads((OUT/'protocol.json').read_bytes())['corpus_sha256'],'Fresh initial frozen corpus')
        rows=json.loads((HERE/'claims_v1.json').read_bytes()); validate(rows)
        original=historical_rows();byid={r['id']:r for r in rows}
        require({r['id'] for r in rows if r['category']!='next_reference'}=={r['id'] for r in original},'Every exact archived hardware/timing/screen row accounted')
        require(len([r for r in rows if r['category']=='next_reference'])==6,'Exactly six fixed primary references')
        for r in original:
            attached=byid[r['id']]
            require(attached['locator']==r['locator'] and attached['archived_row_sha256']==sha(r['text'].encode()),'Exact historical row binding')
        mutations=[('missing_version',lambda r:r.update(version_or_date=None)),('missing_locator',lambda r:r.update(locator=None)),
            ('unverified_cost',lambda r:r.update(accepted_pricing_cost=0)),('conference_theorem_substitution',lambda r:r.update(theorem_from_conference_metadata=True)),
            ('complete_hardware_claim',lambda r:r.update(complete_hardware_certificate=True)),('exhaustive_screen_claim',lambda r:r.update(exhaustive_screen=True))]
        controls=[]
        for name,change in mutations:
            candidate=copy.deepcopy(rows);change(candidate[0])
            try:validate(candidate)
            except ValueError as error:controls.append({'name':name,'rejected':True,'reason':str(error)})
            else:raise ValueError('Escaped control '+name)
        summary=json.loads((ROOT/'results/limitation_program_20261001/H17_demand_run002/summary.json').read_bytes())
        provenance=json.loads((ROOT/'results/limitation_program_20261001/H17_demand_run002/hardware_provenance.json').read_bytes())
        require(summary['architecture_rows']==0 and summary['tau_grid'] is None and summary['measurement_reaction_depth'] is None
            and summary['full_physical_fidelity_certificate'] is False and summary['full_physical_latency_certificate'] is False
            and provenance['architecture_calibrations_admitted']==0, 'H17 unresolved physical interface retained')
        h17=[]
        for record in summary['case_rows']:
            report=json.loads((ROOT/('results/limitation_program_20261001/H17_demand_run002/'+record['case']+'/hardware_demand.json')).read_bytes())
            h17.append({'case':record['case'],'logical_qubits':record['logical_qubits'],'native_CCX_positions':record['native_CCX_positions'],
                'native_demand_metadata_only':True,'reaction_depth':None,'complete_physical_time':None})
            require(report['case']==record['case'],'Exact report case binding')
            require(report['logical_qubits']==record['logical_qubits'] and report['consumed_T_states']==record['consumed_T_states']
                and report['primitive_elementary_gate_count']==record['primitive_elementary_gate_count']
                and report['native_CCX_positions_before_exact_seven_T_expansion']==record['native_CCX_positions'], 'Selected H17 report/summary exact counts')
        write(OUT/'claim_table.json',rows);write(OUT/'negative_controls.json',controls);write(OUT/'H17_metadata_scope.json',h17)
        require(pins()==json.loads((OUT/'protocol.json').read_bytes())['corpus_sha256'],'Fresh final frozen corpus')
        summary={'passed':True,'claim_rows':len(rows),'negative_controls':len(controls),'frozen_local_files':len(CORPUS),
            'all_original_hardware_and_compiled_timing_rows_explicit':True,'all_original_screen_rows_explicit':True,
            'new_fixture_credit':0,'new_scientific_checks':0,'accepted_external_pricing_costs':0,'quantum_advantage':False,
            'CPU_seconds_checkpoint':time.process_time(),'script_wall_seconds_checkpoint':time.monotonic()-START,
            'scope':'Selected next-reference recovery and explicit historical claim classifications; no broad bibliographic closure or theorem/physical transfer.'}
        require(time.process_time()<30 and time.monotonic()-START<90,'Metadata30CPU90wall cap')
        write(OUT/'summary.json',summary)
        owned={str(p.relative_to(OUT)).replace('\\','/'):sha(p.read_bytes()) for p in OUT.rglob('*') if p.is_file() and p.name!='FAILED_UNSEALED.json'}
        require(sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file())<39*2**20,'Reserved full owned40MiB cap')
        write(OUT/'manifest.json',{'files':owned,'corpus_sha256':pins(),'claim_release_sha256':release,'passed':True,'self_hash_excluded':True})
        (OUT/'FAILED_UNSEALED.json').unlink()
        print(json.dumps({'passed':True,'claim_rows':len(rows),'manifest_sha256':sha((OUT/'manifest.json').read_bytes())}))
    except BaseException as error:
        (OUT/'FAILED_UNSEALED.json').write_text(json.dumps({'passed':False,'error':str(error),'type':type(error).__name__})+'\n')
        raise

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['prepare','collect','seal']);parser.add_argument('--protocol-sha256');parser.add_argument('--claims-sha256');a=parser.parse_args()
    if a.mode=='prepare':prepare()
    elif a.mode=='collect':collect(a.protocol_sha256)
    else:seal(a.protocol_sha256,a.claims_sha256)
