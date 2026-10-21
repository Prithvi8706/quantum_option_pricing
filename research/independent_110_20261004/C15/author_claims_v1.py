"""Author the fixed citation table after reading the prospectively selected primary texts."""
import hashlib
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
OUT=ROOT/'results/independent_110_20261004/C15/run002'
retrieval=json.loads((OUT/'primary_retrieval.json').read_bytes())

def row(id,title,version,claim,locator,assumptions,transfer,status,**extra):
    return {'id':id,'title':title,'version_or_date':version,'claim':claim,'locator':locator,'assumptions':assumptions,
        'transfer_conditions':transfer,'status':status,'accepted_pricing_cost':None,'theorem_from_conference_metadata':False,
        'complete_hardware_certificate':False,'exhaustive_screen':False,**extra}

def primary(id,name,title,version,claim,locator,assumptions,transfer,status):
    return row(id,title,version,claim,locator,assumptions,transfer,status,category='next_reference',
        primary_url=retrieval[name]['url'],primary_snapshot='results/independent_110_20261004/C15/run002/primary_sources/'+name,
        primary_snapshot_sha256=retrieval[name]['sha256'],read_date='2026-10-04')

rows=[
    primary('NEXT01','sun_v1.html','Optimal Quantum Speedups for Repeatedly Nested Expectation Estimation',
        'arXiv2602.08120v1, 8February2026',
        'Definition1.1 has unit-cost trajectory steps, zero-cost function evaluation, last-argument Lipschitz constants and terminal L2 integrability at fixed depth. Theorem1.4 uses Lp with p=2-delta/2^d and exponent2(1+delta/2^(d-1)); Theorem1.6 gives RMSE with O(epsilon^-1 log^(3(D-d)+1)(epsilon^-1)).',
        'Section1.2 equation1.1/Definition1.1; Theorems1.4/1.6; Section3.3; https://arxiv.org/html/2602.08120v1',
        'Scalar-coordinate notation, almost-everywhere histories and fixed problem parameters. Complexity constants are not finite circuit costs.',
        'F18 blockD=1 requires an implementable scalar/block access justification. Charge coherent preparation/function/inverse/level/reflection/readout and bias/confidence conversion before pricing transfer.',
        'PRIMARY_VERSION_AND_THEOREM_TEXT_CHECKED; PRACTICAL_TRANSFER_UNRESOLVED'),
    primary('NEXT02','sun_pmlr.html','Optimal Quantum Speedups for Repeatedly Nested Expectation Estimation',
        'ICML2026, PMLR306:117260-117275, meeting6-11July2026; page compiled29September2026',
        'The official proceedings page confirms conference metadata and the authors Sun, Wang and Blanchet. The old audit did not verify this attribution; this new record does.',
        'Official page BibTeX/APA records: https://proceedings.mlr.press/v306/sun26ap.html',
        'Bibliographic metadata and conference abstract only; conference full proof was not inspected.',
        'Keep the frozen arXivv1 theorem evidence separate. No theorem version equivalence or new cost follows from conference metadata.',
        'OFFICIAL_CONFERENCE_METADATA_CHECKED; THEOREM_EQUIVALENCE_UNVERIFIED'),
    primary('NEXT03','fowler_v3.pdf','Time-optimal quantum computation',
        'arXiv1210.4626v3; margin2February2013; internal displayed date27November2024; discrepancy retained',
        'Theoretical selective teleportation can process independent T layers subject to physical measurement and fast classical processing/communication. Figure3 explicitly shows byproduct-induced dependence that can invalidate an apparent same-layer arrangement.',
        'PDFpp1-3, Figures1/2/3 and physical measurement assumptions; https://arxiv.org/pdf/1210.4626v3',
        'Compatible universal QEC code, transversal logical X/Z measurement, prepared resource states, classical signalling and space-time resources.',
        'H03 must retain actual correction dependencies and native72/F40 demand. A code cycle is not automatically a T-layer clock; no architecture latency/error calibration is supplied.',
        'EXACT_V3_INTERFACE_TEXT_CHECKED; DATE_HEADER_DISCREPANCY_RETAINED; PHYSICAL_TRANSFER_UNRESOLVED'),
    primary('NEXT04','litinski_v1.pdf','Active-volume architecture (archived H17 title; full front matter unread)',
        'Exact arXiv2211.15465v1 snapshot; posting day/full internal date not freshly verified; retrieved4October2026',
        'H17 references this construction for memory, active-volume and reaction interfaces. The snapshot was retained, but the browser full-text reopening timed out; no numerical claim is refreshed.',
        'H17 hardware_provenance.json reviewed_primary_options[2]; fixed PDF https://arxiv.org/pdf/2211.15465v1',
        'Archived architecture-interface description only; primary text locator/conditions remain unverified in this pass.',
        'Exclude all quantitative clocks, volumes and pricing transfers until the relevant exact text and a compatible source lowering are checked.',
        'SNAPSHOT_RETAINED; PRIMARY_TEXT_READING_UNVERIFIED'),
    primary('NEXT05','cultivation_v1.html','Magic state cultivation: growing T states as cheap as CNOT gates',
        'arXiv2409.17595v1, header26September2024; displayed internal date24August2026; discrepancy retained',
        'This is simulation-based magic-state preparation. Its conventions include escape and postselection; Assumption3.1 estimates T-state error using twice the S-state error. Section3.3 does not include consuming the state in gate teleportation.',
        'Sections2.4/3.1/3.2 Assumption3.1/3.3; AppendixA; https://arxiv.org/html/2409.17595v1',
        'Specified depolarizing noise and decoder/postselection models; the conversion is checked at faultdistance3 and assumed at5.',
        'Match H17 error-per-state requirement, rejected attempts, escape, transport, memory and consumption before transfer. No published factory reliability is admitted here.',
        'PRIMARY_INTERFACE_AND_ASSUMPTION_TEXT_CHECKED; DATE_HEADER_DISCREPANCY_RETAINED; TARGET_TRANSFER_UNRESOLVED'),
    primary('NEXT06','fast_curious_v1.pdf','The Fast for the Curious: How to accelerate fault-tolerant quantum applications (archived title)',
        'Exact arXiv2510.26078v1 snapshot; exact posting day/internal date not freshly verified; retrieved4October2026',
        'The archived hardware memo cites architecture-dependent arithmetic acceleration. Primary browser full-text reopening timed out; the historical33-bit addition times and external circuit timing are not refreshed.',
        'HARDWARE_AND_COST_MODEL.md H17; original WHY_NO_ADVANTAGE.md section3; https://arxiv.org/pdf/2510.26078v1',
        'Selected primary snapshot and archived attribution only; full numerical/architecture conditions remain unverified in this pass.',
        'Do not borrow projected addition/circuit times as physical cost of the current pricing source or convert T-depth directly to runtime.',
        'SNAPSHOT_RETAINED; PRIMARY_NUMERICAL_READING_UNVERIFIED'),
]
hardware_conditions=[
    'Memory-cycle experiment only; no universal logical gate or current source timing.',
    'Keep decoding endpoints and excluded feedback separate; match code distance/reliability before transfer.',
    'Reaction-time projection is an assumption, not a current-device measurement or universal clock.',
    'Projected CCZ/lattice-surgery period is operation/code-distance specific; it is not every logical T layer.',
    'Projected33-bit arithmetic has its own circuit, architecture and cost boundary; no72/F40 source transfer.',
    'Reaction-limited carry-lookahead requires the stated classical reaction assumption and large space cost.',
    'Trapped-ion layer endpoint, gate set and error protection must match; no universal FT pricing rate.',
    'Neutral-atom layer interval cannot transfer without exact experiment, protected operation and reliability.',
    'Commodity primitive CPU addition is not a measured complete classical pricing sample.',
    'Peak GPU throughput is not measured pricing latency or achieved arithmetic throughput.',
]
path=ROOT/'manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md';lines=path.read_text(encoding='utf-8').splitlines();active=False;count=0
for number,line in enumerate(lines,1):
    if line.startswith('| Anchor |'):active=True;continue
    if active:
        if not line.startswith('|'):break
        if line.startswith('|---'):continue
        count+=1;cells=[x.strip() for x in line.split('|')[1:-1]]
        rows.append(row(f'HW{count:02d}',cells[0], 'Historical manuscript anchor; exact primary version/experiment locator unresolved in this pass',
            'Archived value '+cells[1]+'; archived status '+cells[2]+' (classification not freshly revalidated)',
            path.relative_to(ROOT).as_posix()+f':{number}', 'Original anchor and original boundary retained; primary numerical evidence not refreshed.',
            hardware_conditions[count-1]+' Exclude this number from accepted costs in F18/H03.', 'UNREFRESHED_PRIMARY_NUMBER; EXCLUDED_FROM_ACCEPTED_COSTS',
            category='hardware_anchor',archived_row_sha256=hashlib.sha256(line.encode()).hexdigest()))
number=next(i for i,line in enumerate(lines,1) if '3.7 days per single circuit' in line)
rows.append(row('COMPILED01','External compiled options-circuit timing','Historical manuscript section3; exact primary timing/version boundary unrefreshed',
    'Archived3.7days per circuit repetition under1microsecond-cycle assumptions; approximately10^4logical qubits/10^10T gates and nominal1second classical target are not current pricing delivery costs.',
    path.relative_to(ROOT).as_posix()+f':{number}', 'Historical external circuit and architecture model; no fresh confidence/workload/clock match.',
    'Exclude runtime from this batch. Recover exact source, definition of repetition, protected resources, confidence and comparator before using it.',
    'UNREFRESHED_EXTERNAL_COMPILED_TIMING; EXCLUDED_FROM_ACCEPTED_COSTS',category='compiled_timing',
    archived_row_sha256=hashlib.sha256(lines[number-1].encode()).hexdigest()))
path=ROOT/'docs/research_investigation/2026-09-23/SCREENING_TABLE.md';count=0
for number,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
    if not line.startswith('|') or line.startswith('|---') or line.startswith('| Lane |'):continue
    count+=1;cells=[x.strip() for x in line.split('|')[1:-1]]
    match=re.search(r'\[([^\]]+)\]\(([^)]+)\)',cells[1]);title=match.group(1) if match else cells[1]
    rows.append(row(f'SCREEN{count:03d}', title or 'Archived selected-screen row',
        'Archived '+cells[2]+'; exact reused primary version not freshly verified',
        'Archived screen conclusion: '+cells[-1], path.relative_to(ROOT).as_posix()+f':{number}',
        'Archived reading tier '+cells[3]+'; this pass classifies the selected row without refreshing its theorem or experiment.',
        'Only an archived selected screen; no exhaustive exclusion, universal lower bound or accepted cost. Require exact primary version/locator and workload/access/confidence match before reuse.',
        'HISTORICAL_SELECTED_SCREEN_UNREFRESHED; NOT_EXHAUSTIVE; EXCLUDED_FROM_ACCEPTED_COSTS',
        category='source_screen',archived_row_sha256=hashlib.sha256(line.encode()).hexdigest(),archived_url=match.group(2) if match else None))
encoded=(json.dumps(rows,sort_keys=True,indent=2)+'\n').encode()
with (HERE/'claims_v1.json').open('xb') as f:f.write(encoded)
freeze={'schema':'c15-author-claim-release-v1','claims_sha256':hashlib.sha256(encoded).hexdigest(),
    'source_sha256':hashlib.sha256((HERE/'citation_audit_v2.py').read_bytes()).hexdigest(),
    'protocol_sha256':hashlib.sha256((OUT/'protocol.json').read_bytes()).hexdigest(),
    'primary_retrieval_sha256':hashlib.sha256((OUT/'primary_retrieval.json').read_bytes()).hexdigest(),
    'claims':len(rows),'screen_rows':count,'negative_inventory_controls':6,'claim_table_checks_executed':False,
    'scope':'Human primary reading/classification authoring; metadata audit not yet invoked; physical costs null.'}
with (HERE/'AUTHOR_FREEZE.json').open('x') as f:json.dump(freeze,f,indent=2);f.write('\n')
print(json.dumps(freeze))
