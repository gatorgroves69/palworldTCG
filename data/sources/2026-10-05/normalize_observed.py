"""Offline normalization of this run's loaded DOM evidence. No network."""
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
def save(p,x): p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def frac(s):return float(Decimal(s)/100)
mapping=load(ROOT/'data/sources/2026-09-29/slug-mapping.json')
byurl={r['source_url']:r['normalized_slug'] for r in mapping}
byold={r['source_old_slug']:r['normalized_slug'] for r in mapping}
meta=load(HERE/'meta-dom.json')['result']
assert {'30 days','All'} <= {r['text'] for r in meta['filters'] if r['value']=='page'}
tiers=[]
for r in meta['rows']:
    if not isinstance(r['url'],str) or r['url'] not in byurl or 'raw ' not in r.get('text',''):continue
    lines=r['text'].splitlines()
    rates=re.findall(r'([\d.]+)%',r['text'])
    assert len(rates)==4,(r['url'],rates)
    tiers.append(dict(deck=byurl[r['url']],win_rate=frac(rates[0]),play_rate=frac(rates[3])))
assert len(tiers)==13 and len({r['deck'] for r in tiers})==13
tiers.sort(key=lambda r:-r['play_rate'])
mat=load(HERE/'matchups-dom.json')
assert {'30 days','All','Top 12'}<=set(mat['filters'])
assert mat['date']==meta['date']=='2026-10-04'
soup=BeautifulSoup(mat['html'],'html.parser')
headers=[e['title'] for e in soup.select('thead th[title]')]
trs=soup.select('tbody tr')
slugs=[byold[parse_qs(urlparse(tr.select_one('th a')['href']).query)['pin'][0]] for tr in trs]
assert slugs==[r['deck'] for r in tiers[:12]]
rows=[]
for i,tr in enumerate(trs):
    assert tr.select_one('th a').text==headers[i]
    cells=tr.select('td'); assert len(cells)==12
    for j,c in enumerate(cells):
        title=c.select_one('[title]')['title']
        assert title.startswith(headers[i]+' · '+headers[j]+' · ')
        count=re.search(r' · ([\d,]+) games$',title)
        rows.append(dict(deck_a=slugs[i],deck_b=slugs[j],win_rate_a=frac(c.get_text(strip=True).rstrip('%')),games=int(count[1].replace(',','')) if count else None,source='palworldtcg.gg'))
assert len(rows)==144 and len({(r['deck_a'],r['deck_b']) for r in rows})==144
for i in range(12):
    for j in range(12):
        a,b=rows[i*12+j],rows[j*12+i]
        assert a['games']==b['games'] and abs(a['win_rate_a']+b['win_rate_a']-1)<0.011
save(ROOT/'data/calibration/tiers_2026-10-05.json',tiers)
save(ROOT/'data/calibration/matchups_2026-10-05.json',rows)
cards=check_cards((ROOT/'data/cards.json').read_bytes())
report=[]
(HERE/'quarantine').mkdir(exist_ok=True)
for slug in slugs[:8]:
    d=load(HERE/f'{slug}-dom.json')['result']; assert byurl[d['url']]==slug
    s=BeautifulSoup(d['html'],'html.parser')
    assert s.select_one('time').text==meta['date']
    assert {'30 days','All'}<={e.text for e in s.select('[aria-current="page"]')}
    raw=d['copy']; assert raw
    (HERE/f'{slug}-export.txt').write_text(raw+'\n')
    normalized=['# main']; resolutions=[]
    for line in raw.splitlines():
        q,name=line.split(' ',1)
        candidates={code for code,c in cards.items() if c['name']==name}
        if len(candidates)>1:
            linked={m[1].upper() for a in s.select('a[href]') if (m:=re.search(r'/card/([a-z0-9]+-\d+)-',a['href']))}
            candidates &= linked
        assert len(candidates)==1,(slug,name,candidates)
        code=candidates.pop();normalized.append(f'{q} {code} {name}')
        resolutions.append(dict(quantity=int(q),code=code,name=name))
    normalized.append('# soul')
    p=HERE/'quarantine'/f'{slug}.txt';p.write_text('\n'.join(normalized)+'\n')
    v=validate_deck(p,cards)
    assert v['main']==50 and v['soul']==0
    v.update(reason='Copy list omits Souls. No missing quantities invented; last-valid engine file retained.',source=d['url'],resolutions=resolutions)
    report.append(v)
save(HERE/'quarantine-validation.json',report)
old=load(ROOT/'data/calibration/tiers_2026-09-29.json')
assert {r['deck'] for r in old}=={r['deck'] for r in tiers}
oldrates={r['deck']:r['play_rate'] for r in old}
deltas=sorted([dict(deck=r['deck'],play_rate=r['play_rate'],delta_pp=round((r['play_rate']-oldrates[r['deck']])*100,3)) for r in tiers],key=lambda r:-r['delta_pp'])
oldtop={r['deck'] for r in sorted(old,key=lambda r:-r['play_rate'])[:5]}
comparison=dict(previous='2026-09-29',current='2026-10-05',source_updated='2026-10-04',coverage='Same 13 slugs, full top12 play-rate matrix; not complete 40-deck field',deltas=deltas,new_top5=[r for r in tiers[:5] if r['deck'] not in oldtop])
save(HERE/'comparison.json',comparison)
print(json.dumps(dict(tiers=len(tiers),matchups=len(rows),quarantined=len(report),top8=slugs[:8],comparison=comparison),indent=2))
