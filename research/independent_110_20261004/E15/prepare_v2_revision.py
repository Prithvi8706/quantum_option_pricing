"""Keep v1 frozen; clarify the proven oracle domain before the sole toy run."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[3]
old=Path(__file__).with_name('coherent_inner_toy_v1.py')
new=old.with_name('coherent_inner_toy_v2.py')
assert not new.exists()
s=old.read_text()
for a,b in [
 ('E15/run001','E15/run002'),
 ('intended_full_unitary_operator_error_exact','intended_clean_scratch_isometry_error_exact'),
 ("'toy_unitary_error_exact'","'toy_clean_scratch_isometry_error_exact'"),
 ("'toy_fixed_fallback_retained':True", "'toy_fixed_fallback_retained':True,'full_space_unitarity_proved_as_phase_free_permutation':True,'arbitrary_dirty_scratch_financial_oracle_semantics_claimed':False"),
]:
    assert s.count(a)==1
    s=s.replace(a,b)
compile(s,str(new),'exec');new.write_text(s)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
hold=ROOT/'results/independent_110_20261004/E15/v1_preflight_hold.json'
assert not hold.exists()
hold.write_text(json.dumps({'decision':'STATIC_REJECTED_BEFORE_SCIENTIFIC_RUN',
 'original_source_sha256':sha(old),'original_protocol_sha256':sha(ROOT/'results/independent_110_20261004/E15/run001/protocol.json'),
 'replacement_source_sha256':sha(new),'scientific_runs':0,
 'reason':'Returned-oracle truth-table semantics are proved on clean scratch. Do not label that bound as error against an unspecified ideal extension on arbitrary dirty ancillas. Whole space unitarity is separately exact phase-free permutation.',
 'algorithm_and_budgets_unchanged':True},indent=2)+'\n')
print('E15 V1 scope-label hold retained; V2 compiled before any toy run.')
