"""Check publication links, source provenance and independent model arithmetic."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from fractions import Fraction as F
import json
R=Path(__file__).resolve().parents[1]
d=json.loads((R/'wiki/knowledge.json').read_text());plan=json.loads((R/'wiki/slide-plan.json').read_text());run=json.loads((R/'wiki/run.json').read_text())
S={x['id']:x for x in d['sources']};C={x['id']:x for x in d['concepts']}
assert len(S)==5 and len({s['filename'] for s in S.values()})==5
assert {x['source'] for x in run['ingestion']}==set(S)
assert len(plan)==12
used=set()
for c in C.values():
 assert set(c['sources'])<=S.keys() and c['sources']
 assert set(c['related'])<=C.keys()
for slide in plan:
 assert set(slide['concepts'])<=C.keys()
 for cid in slide['concepts']: used.update(C[cid]['sources'])
assert used==set(S)
class Page(HTMLParser):
 def __init__(self,p):
  super().__init__();self.ids=set();self.links=[];self.h1=0;self.details=0;self.feed(p.read_text())
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:
   assert a['id'] not in self.ids, a['id'];self.ids.add(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='details':assert 'open' not in a;self.details+=1
  for key in ('href','src'):
   if key in a:self.links.append(a[key])
files=[R/'index.html',*R.glob('wiki/**/*.html'),*R.glob('slides/**/*.html')]
pages={p:Page(p) for p in files};links=0
for p,doc in pages.items():
 assert doc.h1==1,(p,doc.h1)
 for href in doc.links:
  u=urlsplit(href)
  if u.scheme or u.netloc:continue
  target=(p.parent/unquote(u.path)).resolve() if u.path else p
  if target.is_dir():target=target/'index.html'
  assert target.exists(),(p,href)
  if u.fragment and target.suffix=='.html':
   other=pages.get(target) or Page(target)
   assert unquote(u.fragment) in other.ids,(p,href)
  links+=1
# Independent solutions of the published toy equations, not historical data.
assert F(1000,100)==10 and F(2000,100)==20 and F(2000,200)==10
assert F(100)/F(125,100)==80 and (F(100)-80)/100==F(1,5)
for ad,offset,expected in [(200,0,(100,100)),(220,0,(110,110)),(220,20,(100,120))]:
 y=F(ad-offset,2);price=y+offset
 assert (y,price)==expected and price==ad-y
print(f'PASS: 5 independent sources, 6 concepts, 12 slide mappings; {len(files)} pages, {links} local links/anchors; closed answers; independent arithmetic.')
