"""Offline final completeness/integrity checks; no collection or calibration analysis."""
import pathlib as P,json,gzip,hashlib,collections,csv,datetime as D
ROOT=P.Path(__file__).resolve().parent
from normalize import cached

def main():
    state=json.loads((ROOT/'state.json').read_text());assert state['phase']=='ACQUISITION_COMPLETE'
    selection=json.loads((ROOT/'selection.json').read_text());top=json.loads((ROOT/'top50.json').read_text());summary=json.loads((ROOT/'summary.json').read_text())
    games=[json.loads(x) for x in (ROOT/'games.jsonl').read_text().splitlines()];acquired=[json.loads(x) for x in (ROOT/'acquired.jsonl').read_text().splitlines()]
    assert len(top['players'])==50 and len(selection['profiles'])==50
    assert [p['rank'] for p in top['players']]==list(range(1,51))
    selected={g['match_id']:g for g in selection['matches']};assert len(selected)==len(selection['matches'])<=300
    assert len(acquired)==len(selected)==state['processed']
    assert {g['match_id'] for g in acquired}==set(selected)
    good={g['match_id']:g for g in acquired if g['status']=='acquired'}
    assert len(games)==len(good)==summary['games'] and len({g['match_id'] for g in games})==len(games)
    assert all(p['ranked_candidates_selected']<=6 for p in selection['profiles'])
    private={p['player']['handle'] for p in selection['profiles'] if p['history_access']!='public'}
    assert not (private & {d['handle'] for g in selection['matches'] for d in g['discovered_from']})
    assert len(list(csv.DictReader((ROOT/'games.csv').open())))==len(games)
    for g in games:
        raw=cached(g['replay_source']);deck=cached(g['deck_source']);assert raw['id']==g['match_id'] and g['ranked'] is True
        flags={f['view'].get('ranked') for f in raw['frames'] if type(f['view'].get('ranked')) is bool};assert flags=={True}
        side=g['first_player']['side']
        if side:
            assert {e['side'] for e in g['first_player']['evidence']}=={side}
            assert g['first_player']['name']==raw['names'][side]
        for s in ('p1','p2'):
            info=g['players'][s]['deck'];counts=collections.Counter()
            if isinstance(deck.get(s),dict):
                for group in deck[s].get('groups',[]):
                    for item in group['items']:counts[item['code']]+=item['n']
                assert dict(counts)==info['main_counts'] and sum(counts.values())==info['main_total']
                assert info['archetype']['source']=='inferred' and info['archetype']['site_authoritative'] is False
            assert info.get('soul_counts') is None
    requests=[json.loads(x) for x in (ROOT/'requests.jsonl').read_text().splitlines()]
    assert len({r['url'] for r in requests})==len(requests),'Repeated network URL'
    assert all(r['method']=='GET' and r['url'].startswith('https://palify.org/') for r in requests)
    replay_requests=[r for r in requests if r['url'].endswith('/replay')];assert len(replay_requests)<=300
    for meta in (ROOT/'cache').glob('*.meta.json'):
        rec=json.loads(meta.read_text());body=meta.with_name(meta.name.replace('.meta.json','.body.gz'));raw=gzip.decompress(body.read_bytes())
        assert len(raw)==rec['bytes'] and hashlib.sha256(raw).hexdigest()==rec['sha256']
    dates=[g['ended_at_ms'] for g in games if isinstance(g['ended_at_ms'],(int,float))]
    report={'status':'PASS','unique_ranked_games':len(games),'selected_ids':len(selected),'all_top50_profiles_accounted_for':True,'private_profiles_skipped':len(private),'network_requests':len(requests),'replay_endpoint_requests':len(replay_requests),'cache_hits_not_refetched':True,'GET_only':True,'raw_cache_hashes_verified':True,'first_player_known':summary['first_player_known'],'winner_known':summary['winner_known'],'oldest_game_utc':D.datetime.fromtimestamp(min(dates)/1000,D.timezone.utc).isoformat() if dates else None,'newest_game_utc':D.datetime.fromtimestamp(max(dates)/1000,D.timezone.utc).isoformat() if dates else None,'quality_flag_counts':summary['quality_flag_counts'],'no_calibration_analysis_performed':True}
    (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
