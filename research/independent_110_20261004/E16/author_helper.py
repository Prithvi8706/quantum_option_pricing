"""Metadata-only literal AST extraction; no imported or evaluated scientific code."""
import ast
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
p=ROOT/'research/independent_110_20261004/F23/screen_covariance_compression.py'
text=p.read_text(); lines=text.splitlines(keepends=True)
names={'down','up','I','atan_inverse','pi_interval','exp_positive'}
selected=[n for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names]
assert {n.name for n in selected}==names
out=ROOT/'research/independent_110_20261004/E16/interval_helper.py'
prefix='import math\nfrom fractions import Fraction as Q\nSCALE=1<<120\n\n'
with out.open('x',encoding='utf-8',newline='\n') as f:
    f.write(prefix+'\n\n'.join(''.join(lines[n.lineno-1:n.end_lineno]) for n in selected))
print('Created helper by literal AST extraction only; no mathematical functions executed')
