"""Metadata authoring only: extract numerical routines without executing them."""
import ast
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
old=ROOT/'research/independent_110_20261004/F23/screen_covariance_compression.py'
new=ROOT/'research/independent_110_20261004/E09/readout_interval.py'
names={'down','up','I','atan_inverse','pi_interval','sin_ratio'}
text=old.read_text(encoding='utf-8')
lines=text.splitlines(keepends=True)
tree=ast.parse(text)
parts=[]
for node in tree.body:
    if isinstance(node,(ast.FunctionDef,ast.ClassDef)) and node.name in names:
        first=min([node.lineno]+[d.lineno for d in getattr(node,'decorator_list',[])])-1
        parts.append(''.join(lines[first:node.end_lineno]))
assert len(parts)==len(names)
prefix='''"""Owned numerical extraction of frozen F23 dyadic120 routines; no finance code."""
import math
import functools
from fractions import Fraction as Q
SCALE=1<<120
guard=lambda: None
PI=None

'''
with new.open('x',encoding='utf-8') as handle:
    handle.write(prefix+'\n\n'.join(parts)+'\n')
print('Owned helper authored by AST extraction only; no mathematical function executed.')
