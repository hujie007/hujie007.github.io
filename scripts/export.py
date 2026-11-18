#!/usr/bin/env python3
"""Create a portable source-only starter without hosting identity or credentials."""
from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/'exports/Jie_Hu_Academic_Website.zip'
INCLUDE=['.github','.gitignore','assets','content','data','templates','scripts','site.yml','requirements.txt','README.md','GITHUB_PAGES_WORKFLOW.yml','LICENSE','THIRD_PARTY_NOTICES.md']
TARGET.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(TARGET,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name in INCLUDE:
        path=ROOT/name
        files=path.rglob('*') if path.is_dir() else [path]
        for f in files:
            if f.is_file() and '__pycache__' not in f.parts and f.suffix!='.pyc':
                z.write(f,'Jie_Hu_Academic_Website/'+f.relative_to(ROOT).as_posix())
print(TARGET)
