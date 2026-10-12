"""Offline normalization of October 12 loaded DOM only; no network."""
import json,re,sys
from pathlib import Path
from urllib.parse import urlparse,parse_qs
from decimal import Decimal
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from tools.data_ops import check_cards,validate_deck
HERE=Path(__file__).resolve().parent
load=lambda p:json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def frac(s):return float(Decimal(s)/100)
mapping=load(ROOT/'data/sources/2026-09-29/slug-mapping.json')
byurl={r['source_url']:r['normalized_slug'] for r in mapping}
byold={r['source_old_slug']:r['normalized_slug'] for r in mapping}
meta=load(HERE/'meta-dom.json');mat=load(HERE/'matchups-dom.json')
for d in [meta,mat]:
    assert {'30 DAYS','ALL'}<={r['text'] for r in d['filters'] if r['current']=='page'}
    assert BeautifulSoup(d['html'],'html.parser').select_one('time').text=='2026-10-11'
assert 'TOP 12' in {r['text'] for r in mat['filters'] if r['current']=='page'}
tiers=[]
for r in meta['links']:
    if not isinstance(r.get('href'),str) or r['href'] not in byurl or 'raw ' not in r.get('text',''):continue
    rates=re.findall(r'([\d.]+)%',r['text']);assert len(rates)==4
    tiers.append(dict(deck=byurl[r['href']],win_rate=frac(rates[0]),play_rate=frac(rates[3])))
assert len(tiers)==len({r['deck'] for r in tiers})==13
tiers.sort(key=lambda r:-r['play_rate'])
soup=BeautifulSoup(mat['html'],'html.parser');table=soup.select_one('table')
headers=[e['title'] for e in table.select('thead th[title]')]
trs=table.select('tbody tr')
slugs=[byold[parse_qs(urlparse(tr.select_one('th a')['href']).query)['pin'][0]] for tr in trs]
assert len(slugs)==12 and set(slugs)=={r['deck'] for r in tiers[:12]}
# Display rounds both ranks 10/11 to 3.3%; retain source matrix tie order.
rates_by_slug={r['deck']:r['play_rate'] for r in tiers}
assert [rates_by_slug[s] for s in slugs]==sorted([rates_by_slug[s] for s in slugs],reverse=True)
tiers.sort(key=lambda r:(-r['play_rate'],slugs.index(r['deck']) if r['deck'] in slugs else 99))
rows=[]
for i,tr in enumerate(trs):
    assert tr.select_one('th a').text==headers[i]
    cells=tr.select('td');assert len(cells)==12
    for j,c in enumerate(cells):
        title=c.select_one('[title]')['title'];assert title.startswith(headers[i]+' · '+headers[j]+' · ')
        count=re.search(r' · ([\d,]+) games$',title)
        rows.append(dict(deck_a=slugs[i],deck_b=slugs[j],win_rate_a=frac(c.get_text(strip=True).rstrip('%')),games=int(count[1].replace(',','')) if count else None,source='palworldtcg.gg'))
assert len(rows)==len({(r['deck_a'],r['deck_b']) for r in rows})==144
for i in range(12):
    for j in range(12):
        a,b=rows[i*12+j],rows[j*12+i]
        assert a['games']==b['games'] and abs(a['win_rate_a']+b['win_rate_a']-1)<0.011
assert all(isinstance(r['games'],int) and r['games']>0 and 0<=r['win_rate_a']<=1 for r in rows)
save(ROOT/'data/calibration/tiers_2026-10-12.json',tiers)
save(ROOT/'data/calibration/matchups_2026-10-12.json',rows)
cards=check_cards((ROOT/'data/cards.json').read_bytes());report=[]
(HERE/'quarantine').mkdir(exist_ok=True)
for slug in slugs[:8]:
    d=load(HERE/f'{slug}-dom.json');assert byurl[d['url']]==slug
    s=BeautifulSoup(d['html'],'html.parser');assert s.select_one('time').text=='2026-10-11'
    assert {'30 DAYS','ALL'}<={e.text.upper() for e in s.select('nav [aria-current="page"]')}
    raw=d['copy'];assert raw
    (HERE/f'{slug}-export.txt').write_text(raw+'\n')
    normalized=['# main'];resolutions=[]
    for line in raw.splitlines():
        q,name=line.split(' ',1)
        candidates={code for code,c in cards.items() if c['name']==name}
        if len(candidates)>1:
            linked={m[1].upper() for a in s.select('a[href]') if (m:=re.search(r'/card/([a-z0-9]+-\d+)-',a['href']))}
            candidates &= linked
        assert len(candidates)==1,(slug,name,candidates)
        code=candidates.pop();normalized.append(f'{q} {code} {name}')
        resolutions.append(dict(quantity=int(q),code=code,name=name))
    normalized.append('# soul');p=HERE/'quarantine'/f'{slug}.txt';p.write_text('\n'.join(normalized)+'\n')
    v=validate_deck(p,cards);assert v['main']==50 and v['soul']==0
    v.update(reason='Copy list omits Souls; no quantities invented; engine file retained.',source=d['url'],resolutions=resolutions);report.append(v)
save(HERE/'quarantine-validation.json',report)
old=load(ROOT/'data/calibration/tiers_2026-10-05.json');assert {r['deck'] for r in old}=={r['deck'] for r in tiers}
oldrates={r['deck']:r['play_rate'] for r in old}
deltas=sorted([dict(deck=r['deck'],play_rate=r['play_rate'],delta_pp=round((r['play_rate']-oldrates[r['deck']])*100,3)) for r in tiers],key=lambda r:-r['delta_pp'])
oldtop={r['deck'] for r in sorted(old,key=lambda r:-r['play_rate'])[:5]}
comparison=dict(previous='2026-10-05',current='2026-10-12',source_updated='2026-10-11',coverage='Same 13 mapped archetypes; complete top12 play-rate matrix, not full 35-deck field',deltas=deltas,new_top5=[r for r in tiers[:5] if r['deck'] not in oldtop])
save(HERE/'comparison.json',comparison)
print(json.dumps(dict(tiers=len(tiers),matchups=len(rows),quarantined=len(report),top8=slugs[:8],comparison=comparison),indent=2))
