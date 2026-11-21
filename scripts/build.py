from pathlib import Path
import shutil
r=Path(__file__).resolve().parents[1]
out=r/'dist'
if out.exists(): shutil.rmtree(out)
out.mkdir()
for name in ['index.html','assets','notes','wiki','slides','.nojekyll']:
 p=r/name
 if p.is_dir(): shutil.copytree(p,out/name)
 else: shutil.copy2(p,out/name)
print('Built static site in dist/')
