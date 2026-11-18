#!/usr/bin/env python3
"""Build the academic website from Markdown and YAML; run from any directory."""
from pathlib import Path
from datetime import datetime
from urllib.parse import quote
import argparse, html, json, re, shutil, sys
import yaml
import markdown
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

ROOT=Path(__file__).resolve().parents[1]
STATUSES=['Published & accepted','Under revision','Working papers']
NAV=[('research','research/','Research'),('publications','publications/','Publications'),('teaching','teaching/','Teaching'),('talks','talks/','Talks'),('service','service/','Service')]
SEARCH='<svg aria-hidden="true" viewBox="0 0 20 20" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="8" cy="8" r="5.5"/><path d="m12 12 5 5"/></svg>'

def load(path):
    with (ROOT/path).open(encoding='utf-8') as stream:return yaml.safe_load(stream)

def md(text):
    return markdown.markdown(text,extensions=['extra','sane_lists'],output_format='html')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='dist');args=parser.parse_args()
    if args.output not in {'dist','_site'}:raise ValueError('Output must be dist or _site; source folders are protected.')
    out=ROOT/args.output
    site=load('site.yml')
    if not re.fullmatch(r'#[0-9a-fA-F]{6}',site.get('accent_color','')):raise ValueError('site.yml: accent_color must be a six-digit hex color.')
    for field in ['name','email','portrait','cv','description','updated']:
        if not site.get(field):raise ValueError(f'site.yml: {field} is required.')
    for field in ['portrait','cv']:
        if not (ROOT/site[field]).is_file():raise ValueError(f'site.yml: missing {field} file: {site[field]}')
    areas=load('data/research.yml')
    if not isinstance(areas,list) or len(areas)!=3:raise ValueError('data/research.yml must define three research areas.')
    slugs={area['slug'] for area in areas}
    if len(slugs)!=3:raise ValueError('Research area slugs must be unique.')
    for area in areas:
        if not re.fullmatch('[a-z]+(?:-[a-z]+)*',area['slug']):raise ValueError('Use lowercase letters and hyphens in research slugs.')
        area['html']=md((ROOT/'content'/area['content']).read_text(encoding='utf-8'))
    papers=load('data/publications.yml');ids=set()
    if not isinstance(papers,list):raise ValueError('data/publications.yml must contain a list.')
    for paper in papers:
        if not isinstance(paper.get('id'),int) or paper['id'] in ids:raise ValueError('Each paper needs a unique integer id.')
        ids.add(paper['id'])
        for field in ['title','authors','year','status','topic']:
            if not paper.get(field):raise ValueError(f'Paper {paper["id"]}: {field} is required.')
        if paper['status'] not in STATUSES:raise ValueError(f'Paper {paper["id"]}: unknown status.')
        if not isinstance(paper['year'],int):raise ValueError(f'Paper {paper["id"]}: year must be an integer.')
        if not isinstance(paper.get('selected',False),bool):raise ValueError(f'Paper {paper["id"]}: selected must be true or false.')
        for field in ['url','code']:
            if paper.get(field) and not paper[field].startswith(('https://','http://')):raise ValueError(f'Paper {paper["id"]}: invalid {field}.')
        paper['pdf']=paper.get('pdf') or ''
        if paper['pdf'] and not paper['pdf'].startswith(('http://','https://')):
            pdf=(ROOT/paper['pdf']).resolve()
            if not pdf.is_relative_to(ROOT/'assets') or not pdf.is_file():raise ValueError(f'Paper {paper["id"]}: PDF must exist under assets/.')
        fallback={'Transfer learning':'transfer','Federated learning':'federated'}.get(paper['topic'],'inference')
        paper['areas']=paper.get('areas',[fallback])
        if not isinstance(paper['areas'],list) or not paper['areas'] or not set(paper['areas']).issubset(slugs):raise ValueError(f'Paper {paper["id"]}: areas must use valid research slugs.')
        for field in ['venue','detail']:paper[field]=paper.get(field) or ''
        paper['selected']=paper.get('selected',False)
        paper['authors_html']=html.escape(paper['authors']).replace(html.escape(site['name']),'<strong>'+html.escape(site['name'])+'</strong>')
        paper['scholar_url']='https://scholar.google.com/scholar?q='+quote(paper['title'])
    papers.sort(key=lambda paper:(STATUSES.index(paper['status']),-paper['year']))
    for area in areas:area['papers']=[paper for paper in papers if area['slug'] in paper['areas']]
    news=load('data/news.yml') or []
    for item in news:item['html']=md(item['text'])
    if out.exists():shutil.rmtree(out)
    out.mkdir(parents=True)
    shutil.copytree(ROOT/'assets',out/'assets')
    for name in ['LICENSE','THIRD_PARTY_NOTICES.md']:shutil.copy2(ROOT/name,out/name)
    clean=[{key:value for key,value in paper.items() if key not in ['authors_html','scholar_url']} for paper in papers]
    (out/'assets/publications.json').write_text(json.dumps(clean,ensure_ascii=False,indent=2),encoding='utf-8')
    env=Environment(loader=FileSystemLoader(ROOT/'templates'),autoescape=select_autoescape(['html']),undefined=StrictUndefined)
    common=dict(site=site,year=datetime.now().year,navigation=NAV,search_icon=SEARCH,papers=papers,selected_count=sum(p['selected'] for p in papers),statuses=STATUSES,status_counts={status:sum(p['status']==status for p in papers) for status in STATUSES},topics=list(dict.fromkeys(p['topic'] for p in papers)),news=news,research=areas,software=load('data/software.yml') or [])
    def render(path,section,title,template,content=None,**extra):
        depth=len(Path(path).parts) if path else 0
        prefix='../'*depth
        def url(target):
            target=str(target)
            if target.startswith(('https://','http://','mailto:')):return target
            return prefix+target.lstrip('/') if target else prefix or './'
        folder=out/path;folder.mkdir(parents=True,exist_ok=True)
        values=dict(common,section=section,nav_section='research' if section=='research-area' else section,page_title=title,url=url,content_html=md((ROOT/'content'/content).read_text(encoding='utf-8')) if content else '',has_papers=section in ['publications','research-area'])
        values.update(extra)
        (folder/'index.html').write_text(env.get_template(template).render(**values),encoding='utf-8')
    render('','home',site['name'],'home.html','about.md')
    render('research','research','Research','research.html','research.md')
    render('publications','publications','Publications','publications.html')
    for section,title,file in [('teaching','Teaching','teaching.md'),('talks','Talks','talks.md'),('service','Professional Service','service.md')]:render(section,section,title,'page.html',file)
    for area in areas:render('research/'+area['slug'],'research-area',area['title'],'research-area.html',area=area,page_papers=area['papers'])
    for section in ['research','publications','teaching','talks','service']:
        (out/f'{section}.html').write_text(f'<!doctype html><html><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url={section}/"><title>Redirecting</title></head><body><a href="{section}/">Continue</a><script>location.replace("{section}/"+location.hash)</script></body></html>',encoding='utf-8')
    (out/'.nojekyll').touch()
    (out/'404.html').write_text('<!doctype html><meta charset="utf-8"><title>Page not found</title><h1>Page not found</h1><p>Please return to the website home page.</p>',encoding='utf-8')
    print(f'Built 9 content pages, 3 research areas, and {len(papers)} publications → {out}')

if __name__=='__main__':
    try:main()
    except Exception as error:
        print(f'Build failed: {error}',file=sys.stderr);sys.exit(1)
