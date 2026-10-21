"""Final prepared-packet static review; no imports of experiment or NumPy."""
from pathlib import Path
import ast,copy,hashlib,json
root=Path(__file__).resolve().parents[3];out=root/'results/independent_110_20261004/F30/run002'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=json.loads((out/'protocol.json').read_text())
for row in p['corpus']:assert sha(root/row['path'])==row['sha256'],row['path']
assert not (out/'ATTEMPT.json').exists()
assert p['numpy']=='2.0.2' and p['python']=='3.12.4' and p['ranks']==[2,4,8] and p['training_payoffs_already_evaluated']==0
def functions(v):
 t=ast.parse((root/f'research/independent_110_20261004/F30/rank_screen_v{v}.py').read_text())
 return {n.name:n for n in t.body if isinstance(n,ast.FunctionDef)}
old,new=functions(1),functions(2)
for name in ['bind_contract','existing_PCA_map']:assert ast.dump(old[name])==ast.dump(new[name]),name
adapted=copy.deepcopy(new['run'])
assert isinstance(adapted.body[0],ast.Expr) and adapted.body[0].value.func.id=='check_environment'
adapted.body.pop(0)
attempt=next(n for n in adapted.body if isinstance(n,ast.Try))
assert isinstance(attempt.body[0],ast.If) and 'python' in ast.dump(attempt.body[0])
attempt.body.pop(0)
assert ast.dump(adapted)==ast.dump(old['run']),'Scientific run AST changed beyond reviewed environment guard'
prior=root/'docs/independent_110_20261004/F30/STATIC_REVIEW_REJECTION_run001.json'
receipt={'item':'F30','disposition':'STATIC_REVIEW_PASS_FOR_ONE_FROZEN_RUN002_DIAGNOSTIC',
 'protocol_sha256':sha(out/'protocol.json'),'input_sha256':{r['path']:r['sha256'] for r in p['corpus']},
 'prior_rejection_sha256':sha(prior),'selected_launcher_sha256':sha(Path(p['executable'])),
 'fresh_six_input_pins_match':True,'scientific_core_AST_unchanged_beyond_environment_guards':True,
 'no_payoff_or_fit_invocation_marker':True,'audited_source_imports':0,'scientific_invocations_by_reviewer':0,
 'findings':['Original D1 plain unconditioned PCA Asian integrand/contract retained; no F03 transform or new workload.',
  'Training33x33 Gaussian-weighted cube is unnormalized truncated contribution; separate512 fixed validation points follow the conditioned cube law.',
  'One weighted matrix SVD and prescribed ranks2/4/8 share1089 training and512 validation targets; negative fits remain, no validation-based rank selection.',
  'Finite weighted-grid SVD residual and Cauchy checks are floating diagnostics, with tail/interpolation/continuum price certificates unresolved.',
  'Contraction operation counts include two core sums and rank dot product; training/setup obligations are explicit. No coherent loader, finite normalization or20percent gain follows.',
  'Version2 binds exact launcher/Python3.12.4/NumPy2.0.2 and rechecks inputs after science. Timer scope excludes import and data preparation; complete runtime dependency closure is not certified.',
  'Original prepared-v1 environment mismatch remains rejected with zero science; fresh environment preparation is not a scientific retry.'],
 'budgets':p['budgets'],'quantum_advantage':False,'new_fixture_credit':0,'full_F30_acceptance':False,
 'unresolved':['Continuum/tail/interpolation and finite-law error','Numerical enclosures','Quantum core loading/sign/normalization/rotation/inverse','Estimator/readout and complete physical costs','Matched full training-inclusive performance']}
dest=Path(__file__).with_name('STATIC_REVIEW_run002.json');assert not dest.exists();dest.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({'receipt':dest.relative_to(root).as_posix(),'sha256':sha(dest),'disposition':receipt['disposition']}))
