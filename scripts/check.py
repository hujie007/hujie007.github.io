#!/usr/bin/env python3
"""Check rendered pages, local assets, and fragment links before publication."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
ROOT=Path(__file__).resolve().parents[1]/'dist'
class Page(HTMLParser):
    def __init__(self):super().__init__();self.refs=[];self.ids=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        for k in ('href','src'):
            if k in a:self.refs.append(a[k])
pages={}
for file in ROOT.rglob('*.html'):
    p=Page();p.feed(file.read_text(encoding='utf-8'));pages[file.resolve()]=p
errors=[]
for file,page in pages.items():
    if len(page.ids)!=len(set(page.ids)):errors.append(f'{file.name}: duplicate ids')
    for ref in page.refs:
        u=urlsplit(ref)
        if u.scheme or u.netloc:continue
        target=(ROOT/u.path.lstrip('/')).resolve() if u.path.startswith('/') else (file.parent/unquote(u.path)).resolve() if u.path else file
        if target.is_dir():target=target/'index.html'
        if not target.is_file():errors.append(f'{file.relative_to(ROOT)}: missing {ref}')
        elif u.fragment and target in pages and u.fragment not in pages[target].ids:errors.append(f'{file.relative_to(ROOT)}: missing anchor {ref}')
if errors:raise SystemExit('\n'.join(errors))
print(f'Checked {len(pages)} HTML pages: local files and fragment links passed.')
