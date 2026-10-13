"""Offline replay/deck normalization with explicit provenance and disagreement flags."""
import pathlib as P,json,gzip,hashlib,collections,csv,datetime as D
from archetypes import classify,VERSION
ROOT=P.Path(__file__).resolve().parent

def cached(ref):
    raw=gzip.decompress((ROOT/ref['cache_body']).read_bytes());meta=json.loads((ROOT/ref['cache_meta']).read_text())
    assert meta['status']==200 and meta['url']==ref['url'] and meta['sha256']==hashlib.sha256(raw).hexdigest()
    return json.loads(raw)
def side_name(name,names):
    matches=[s for s in ('p1','p2') if names.get(s)==name and isinstance(name,str)]
    return matches[0] if len(matches)==1 else None

def perspective(raw,frame,names):
    if raw in ('p1','p2','draw'):return raw
    view=frame.get('view') or {};hands=frame.get('hands') or {}
    if raw in ('me','opp'):return side_name((view.get(raw) or {}).get('name'),names)
    if raw in ('you','bot'):return side_name((hands.get(raw) or {}).get('name'),names)
    return None

def result_evidence(replay,discoveries):
    names=replay['names'];frames=replay['frames'];first=[];flags=[];first_active_seen=False
    for f in frames:
        view=f.get('view') or {};seq=f.get('seq');setup=view.get('setup') or {}
        if type(setup.get('firstIsMe')) is bool:
            raw='me' if setup['firstIsMe'] else 'opp';side=perspective(raw,f,names)
            if side:first.append({'side':side,'seq':seq,'field':'view.setup.firstIsMe','value':setup['firstIsMe']})
        if not first_active_seen and view.get('activeIs'):
            first_active_seen=True
            if view.get('turn')==1:
                side=perspective(view['activeIs'],f,names)
                if side:first.append({'side':side,'seq':seq,'field':'view.activeIs at first active turn1 frame','value':view['activeIs']})
        for entry in view.get('log') or []:
            text=entry.get('text','')
            for side,name in names.items():
                if side in ('p1','p2') and side_name(name,names) and text==name+' takes the first turn.':
                    evidence={'side':side,'seq':seq,'field':'view.log explicit first turn','value':text}
                    if not any(x['field']==evidence['field'] and x['value']==text for x in first):first.append(evidence)
    sides={x['side'] for x in first};chosen=next(iter(sides)) if len(sides)==1 else None
    if len(sides)>1:flags.append('replay_first_player_conflict')
    elif not sides:flags.append('first_player_unknown')
    final=frames[-1];view=final['view'];winner=perspective(view.get('winner'),final,names)
    if view.get('status')!='finished':winner=None;flags.append('replay_not_finished')
    if winner is None:flags.append('winner_unknown')
    hist=[]
    for d in discoveries:
        g=d['history'];owner='p1' if g.get('iAmP1') is True else ('p2' if g.get('iAmP1') is False else None)
        other={'p1':'p2','p2':'p1'}.get(owner)
        hf=(owner if g['wentFirst'] else other) if type(g.get('wentFirst')) is bool and owner else None
        hw={'win':owner,'loss':other,'draw':'draw'}.get(g.get('result'))
        hist.append({'handle':d['handle'],'owner_side':owner,'wentFirst_raw':g.get('wentFirst'),'profile_first_side':hf,'profile_winner_side':hw,'profile_result':g.get('result')})
        if hf and chosen and hf!=chosen:flags.append('profile_first_player_disagrees_with_replay')
        if hw and winner and hw!=winner:flags.append('profile_winner_disagrees_with_replay')
    seqs=[f.get('seq') for f in frames]
    if any(not isinstance(s,int) for s in seqs) or seqs!=sorted(set(seqs)):flags.append('frame_sequence_invalid')
    elif seqs and seqs[0]!=0:flags.append('replay_missing_initial_frame')
    if view.get('turn') is not None and view['turn']<=2:flags.append('very_short_game')
    if view.get('endReason') in ('timeout','disconnect','inactive'):flags.append('timeout_or_disconnect')
    return {'first_player':{'side':chosen,'name':names.get(chosen),'source':'replay_evidence_consensus' if chosen else 'unknown','confidence':'high' if chosen else 'unknown','evidence':first},'winner':{'side':winner,'name':names.get(winner),'source':'replay_terminal_view','evidence':{'seq':final.get('seq'),'raw':view.get('winner'),'status':view.get('status'),'hands_names':{k:v.get('name') for k,v in (final.get('hands') or {}).items()},'view_names':{k:(view.get(k) or {}).get('name') for k in ('me','opp')}}},'history_comparison':hist,'quality_flags':sorted(set(flags)),'end_reason':view.get('endReason'),'final_turn':view.get('turn'),'frame_count':len(frames),'frame_seq_first':seqs[0],'frame_seq_last':seqs[-1]}

def deck_record(deck):
    if not isinstance(deck,dict):return {'main_counts':None,'main_total':None,'archetype':{'archetype':'unknown','source':'unavailable','confidence':0},'quality_flags':['deck_unavailable']}
    counts=collections.Counter()
    for group in deck.get('groups') or []:
        for item in group.get('items') or []:
            assert type(item.get('n')) is int and item['n']>0
            counts[item['code']]+=item['n']
    countmap=dict(sorted(counts.items()));flags=[]
    if sum(counts.values())!=50 or deck.get('total')!=50:flags.append('main_deck_count_not_50')
    return {'main_counts':countmap,'main_total':sum(counts.values()),'source_reported_total':deck.get('total'),'deck_fingerprint':hashlib.sha256(json.dumps(countmap,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'archetype':classify(deck),'quality_flags':flags,'soul_counts':None,'soul_note':'Endpoint supplies main deck only; no Soul quantities invented.'}

def normalize(selected,record,top):
    replay=cached(record['replay_source']);decks=cached(record['deck_source']);assert replay['id']==selected['match_id']
    names=replay['names'];e=result_evidence(replay,selected['discovered_from'])
    ranks={p['handle']:p['rank'] for p in top['players']};player_data={s:{'name':names.get(s),'handle':None,'rank_now':None,'deck':deck_record(decks.get(s))} for s in ('p1','p2')}
    for d in selected['discovered_from']:
        g=d['history'];owner='p1' if g.get('iAmP1') is True else ('p2' if g.get('iAmP1') is False else None)
        if not owner:continue
        other='p2' if owner=='p1' else 'p1'
        for side,handle in [(owner,d['handle']),(other,(g.get('opponent') or {}).get('handle'))]:
            old=player_data[side]['handle']
            if old and handle and old!=handle:e['quality_flags'].append('profile_player_handle_conflict')
            elif handle:player_data[side].update(handle=handle,rank_now=ranks.get(handle))
    for side in player_data:
        e['quality_flags'] += [side+'_'+f for f in player_data[side]['deck']['quality_flags']]
    e['quality_flags']=sorted(set(e['quality_flags']))
    return {'schema_version':1,'match_id':replay['id'],'replay_url':'https://palify.org/play/replay/'+replay['id'],'format':replay.get('format'),'ranked':True,'started_at_ms':replay.get('startedAt'),'ended_at_ms':replay.get('endedAt'),'ladder_snapshot_utc':top['captured_utc'],'discovered_from':[{'handle':d['handle'],'rank_now':d['rank_now'],'profile_source':d['profile_source'],'rank_then':d['history'].get('myRank'),'rating_then':d['history'].get('myRatingThen'),'history_ended_at_ms':d['history'].get('endedAt')} for d in selected['discovered_from']],'players':player_data,**e,'replay_anchor_raw':replay.get('anchor'),'replay_source':record['replay_source'],'deck_source':record['deck_source'],'archetype_classifier':VERSION}

def run():
    selection=json.loads((ROOT/'selection.json').read_text());top=json.loads((ROOT/'top50.json').read_text());byid={r['match_id']:r for r in selection['matches']};records=[json.loads(x) for x in (ROOT/'acquired.jsonl').read_text().splitlines() if x.strip()]
    assert len(records)==len({r['match_id'] for r in records}) and len(records)<=300
    games=[normalize(byid[r['match_id']],r,top) for r in records if r['status']=='acquired']
    (ROOT/'games.jsonl').write_text(''.join(json.dumps(g,ensure_ascii=False)+'\n' for g in games))
    fields=['match_id','started_at_ms','ended_at_ms','p1_name','p2_name','p1_handle','p2_handle','p1_archetype','p2_archetype','p1_confidence','p2_confidence','first_player','winner','end_reason','final_turn','quality_flags']
    with (ROOT/'games.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');writer.writeheader()
        for g in games:
            row={k:g[k] for k in ('match_id','started_at_ms','ended_at_ms','end_reason','final_turn')}
            for s in ('p1','p2'):
                p=g['players'][s];row[s+'_name']=p['name'];row[s+'_handle']=p['handle'];row[s+'_archetype']=p['deck']['archetype']['archetype'];row[s+'_confidence']=p['deck']['archetype']['confidence']
            row.update(first_player=g['first_player']['side'],winner=g['winner']['side'],quality_flags=';'.join(g['quality_flags']));writer.writerow(row)
    summary={'games':len(games),'current_top50_players':len(top['players']),'private_profiles_skipped':[p['player']['rank'] for p in selection['profiles'] if p['history_access']!='public'],'selected_unique_ids':len(selection['matches']),'acquisition_status_counts':dict(collections.Counter(r['status'] for r in records)),'first_player_known':sum(g['first_player']['side'] in ('p1','p2') for g in games),'winner_known':sum(g['winner']['side'] in ('p1','p2','draw') for g in games),'quality_flag_counts':dict(collections.Counter(f for g in games for f in g['quality_flags'])),'archetype_counts':dict(collections.Counter(g['players'][s]['deck']['archetype']['archetype'] for g in games for s in ('p1','p2'))),'archetype_classifier':VERSION,'normalized_utc':D.datetime.now(D.timezone.utc).isoformat()}
    (ROOT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':run()
