"""Bounded public top-50 collection. No analysis, auth, POSTs, or simulations."""
import pathlib as P,json,re,urllib.parse,hashlib,datetime as D,traceback,fcntl
from fetch import get,ROOT,now
from typing import Any
MAX_GAMES=300;PER_PLAYER=6

import html as html_lib
class PrivateHistory(Exception):
    pass

def history(html):
    visible=re.sub(r'<(script|style)\b[^>]*>.*?</\1>',' ',html,flags=re.S|re.I)
    visible=' '.join(html_lib.unescape(re.sub(r'<[^>]+>',' ',visible)).split())
    if 'keeps their games private.' in visible:
        raise PrivateHistory('Public profile explicitly says history is private; no probing')
    decoder=json.JSONDecoder();pieces=[]
    for m in re.finditer(r'self\.__next_f\.push\(',html):
        try:value,end=decoder.raw_decode(html[m.end():])
        except json.JSONDecodeError:continue
        if isinstance(value,list) and len(value)==2 and value[0]==1 and isinstance(value[1],str):pieces.append(value[1])
    stream=''.join(pieces);candidates=[]
    for m in re.finditer(r'"games":',stream):
        try:value,end=decoder.raw_decode(stream[m.end():])
        except json.JSONDecodeError:continue
        if isinstance(value,list) and (not value or all(isinstance(g,dict) and 'id' in g and 'endedAt' in g for g in value)):candidates.append(value)
    if not candidates:raise ValueError('Profile has no parseable public games property; not assumed empty')
    unique={json.dumps(x,sort_keys=True):x for x in candidates}
    assert len(unique)==1,'Ambiguous profile history properties'
    return next(iter(unique.values()))
def cache_ref(url):
    key=hashlib.sha256(url.encode()).hexdigest();return {'url':url,'cache_body':'cache/'+key+'.body.gz','cache_meta':'cache/'+key+'.meta.json'}
def freeze_selection() -> dict[str,Any]:
    dest=ROOT/'selection.json'
    if dest.exists():return json.loads(dest.read_text())
    ladder_url='https://palify.org/api/pvp/ladder';ladder=json.loads(get(ladder_url))['board']
    top=sorted([p for p in ladder if isinstance(p.get('rank'),int) and p['rank']<=50],key=lambda x:x['rank'])
    assert len(top)==50 and [p['rank'] for p in top]==list(range(1,51))
    assert len({p['handle'] for p in top})==50
    (ROOT/'top50.json').write_text(json.dumps({'captured_utc':json.loads((ROOT/cache_ref(ladder_url)['cache_meta']).read_text())['captured_utc'],'source':cache_ref(ladder_url),'players':top},ensure_ascii=False,indent=2)+'\n')
    profiles=[];by_id={};ordered=[]
    for p in top:
        url='https://palify.org/u/'+urllib.parse.quote(p['handle'],safe='')
        try:
            games=history(get(url).decode());privacy='public'
        except PrivateHistory:
            games=[];privacy='private_history_skipped'
        eligible=[g for g in games if g.get('format')=='standard' and g.get('mode')=='standard' and g.get('endedAt')]
        eligible=sorted(eligible,key=lambda g:(-g['endedAt'],g['id']))[:PER_PLAYER]
        profiles.append({'player':p,'source':cache_ref(url),'history_access':privacy,'public_history_count':len(games) if privacy=='public' else None,'ranked_candidates_selected':len(eligible),'selected_games':eligible})
        print(f'PROFILE rank {p["rank"]}: public {len(games)}, selected {len(eligible)}',flush=True)
    # Round-robin order, at most six historical games per player; all 50 sampled before replay fetches.
    for slot in range(PER_PLAYER):
        for profile in profiles:
            games=profile['selected_games']
            if slot>=len(games):continue
            g=games[slot];mid=g['id'];assert re.fullmatch(r'[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}',mid)
            if mid not in by_id:by_id[mid]={'match_id':mid,'discovered_from':[]};ordered.append(mid)
            by_id[mid]['discovered_from'].append({'handle':profile['player']['handle'],'rank_now':profile['player']['rank'],'name_now':profile['player']['name'],'profile_source':profile['source'],'history':g})
    assert len(ordered)<=MAX_GAMES
    data=dict(created_utc=now(),max_games=MAX_GAMES,per_player=PER_PLAYER,policy='six most recent standard-format standard-mode completed profile entries per current top50; deduplicated; round-robin fetch order; replay ranked flag is final eligibility gate',profiles=profiles,matches=[by_id[k] for k in ordered])
    dest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');return data

def run():
    selection=freeze_selection();result=ROOT/'acquired.jsonl';done={}
    if result.exists():done={r['match_id']:r for r in map(json.loads,result.read_text().splitlines())}
    for selected in selection['matches']:
        mid=selected['match_id']
        if mid in done:continue
        url=f'https://palify.org/api/pvp/match/{mid}/replay';record={'match_id':mid,'replay_source':cache_ref(url),'captured_utc':now()}
        try:
            replay=json.loads(get(url));assert replay.get('id')==mid
            frames=replay.get('frames') or [];assert frames,'Empty replay'
            flags={f.get('view',{}).get('ranked') for f in frames if isinstance(f.get('view',{}).get('ranked'),bool)}
            if flags!={True}:record.update(status='excluded_not_unambiguously_ranked',ranked_flags=list(flags))
            else:
                deckurl=f'https://palify.org/api/pvp/match/{mid}/decks';decks=json.loads(get(deckurl));assert 'p1' in decks and 'p2' in decks
                record.update(status='acquired',deck_source=cache_ref(deckurl),frames=len(frames))
        except Exception as error:
            record.update(status='failed',error=str(error))
            if (ROOT/'BLOCKED.json').exists():
                with result.open('a') as f:f.write(json.dumps(record,ensure_ascii=False)+'\n')
                raise
        with result.open('a') as f:f.write(json.dumps(record,ensure_ascii=False)+'\n')
        done[mid]=record
        (ROOT/'state.json').write_text(json.dumps(dict(phase='COLLECTING',processed=len(done),target=len(selection['matches']),last_match=mid,updated_utc=now()),indent=2)+'\n')
        print(f'REPLAY {len(done)}/{len(selection["matches"])} {record["status"]} {mid}',flush=True)
    state=dict(phase='ACQUISITION_COMPLETE',processed=len(done),acquired=sum(r['status']=='acquired' for r in done.values()),failed=sum(r['status']=='failed' for r in done.values()),target=len(selection['matches']),updated_utc=now())
    (ROOT/'state.json').write_text(json.dumps(state,indent=2)+'\n');print(json.dumps(state),flush=True)
if __name__=='__main__':
    lock=(ROOT/'collector.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    try:run()
    except BaseException:(ROOT/'FAILED.txt').write_text(now()+'\n'+traceback.format_exc());raise
