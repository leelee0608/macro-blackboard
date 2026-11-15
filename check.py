from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from fractions import Fraction as F
R=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,s):
  super().__init__();self.links=[];self.ids=[];self.h1=0;self.details=0;self.opened=0;self.math=0;self.feed(s)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  for k in ['href','src']:
   if k in a:self.links.append(a[k])
  if tag=='h1':self.h1+=1
  if tag=='details' and a.get('class')!='mobile-nav':
   self.details+=1;self.opened+='open' in a
  if tag=='math':self.math+=1
files=[R/'index.html',*sorted((R/'notes').rglob('*.html'))]
pages={f:Page(f.read_text()) for f in files};issues=[]
for f,q in pages.items():
 if q.h1!=1:issues.append(f'{f}: h1 count')
 if len(set(q.ids))!=len(q.ids):issues.append(f'{f}: duplicate ids')
 if '{{' in f.read_text():issues.append(f'{f}: unresolved placeholder')
 if f.parent!=R and (q.details<2 or q.opened):issues.append(f'{f}: answer disclosure')
 for link in q.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  if u.path.startswith('/'):issues.append(f'{f}: root-relative URL {link}')
  target=(f.parent/unquote(u.path)).resolve() if u.path else f
  if not target.exists():issues.append(f'{f}: missing {link}')
  if u.fragment and target in pages and u.fragment not in pages[target].ids:issues.append(f'{f}: broken anchor {link}')
# Independent exact-arithmetic checks of the numerical teaching examples.
assert F(1,2)*1000-100*F(5,100)==495
assert 2*(F(1,2)*1000-100*F(10,100))==980
assert F(108,100)/F(103,100)-1==F(5,103)
assert F(105,100)*F(98,100)-1==F(29,1000)
for money,Y,r in [(360,800,F(4,100)),(395,850,F(3,100)),(300,F(5000,7),F(2,35))]:
 assert Y==1000-5000*r
 assert money==F(1,2)*Y-1000*r
assert 100+F(8,10)*(900-100)+(100-1000*F(4,100))+100==900
for infl,Y in [(F(2,100),900),(F(3,100),875)]:assert 1000-5000*(F(1,100)+F(1,2)*infl)==Y
if issues:raise SystemExit('\n'.join(issues))
print(f'PASS: {len(files)} pages, internal assets/links/anchors, unique headings/IDs, 16 initially closed answers, exact example calculations.')
