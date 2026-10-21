"""Read-only primary HTML conversion; no experimental calculations."""
from html.parser import HTMLParser
from pathlib import Path
class Text(HTMLParser):
 def __init__(self): super().__init__(); self.parts=[];self.skip=0;self.math=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
  if t=='math':
   if self.math==0:self.parts.append(' '+dict(a).get('alttext','')+' ')
   self.math+=1
  if t in ('p','div','section','h1','h2','h3','h4','h5','h6','li','tr'):self.parts.append('\n')
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
  if t=='math':self.math=max(0,self.math-1)
 def handle_data(self,s):
  if not self.skip and not self.math:self.parts.append(s)
ROOT=Path(__file__).resolve().parents[3]
base=ROOT/'docs/independent_110_20261004/E25/primary_sources'
p=Text();p.feed((base/'Ramoa_Santos_2412_04394v5.html').read_text(encoding='utf-8'))
lines=[' '.join(x.split()) for x in ''.join(p.parts).splitlines()]
with (base/'Ramoa_Santos_2412_04394v5.txt').open('x',encoding='utf-8',newline='\n') as f:f.write('\n'.join(x for x in lines if x)+'\n')
print('Primary text extracted only; no scientific checks executed')
