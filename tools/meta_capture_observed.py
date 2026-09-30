"""Materialize browser-observed 2026-09-29 public meta data. No network calls."""
import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import shutil

ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'data/sources/2026-09-29'
C=ROOT/'data/calibration'
S.mkdir(parents=True,exist_ok=True); C.mkdir(parents=True,exist_ok=True)
def save(path,value):
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
# Columns and rows in the source's most-played top-12 matrix order.
observed=[
('chillet-relaxaurus-bp','blue-purple-chillet-relaxaurus','blue-purple-chillet-dragon-whisperer-elphidran-aqua-gentle-ripples',58.2,28.3),
('chillet-relaxaurus-br','blue-red-chillet-relaxaurus','blue-red-chillet-dragon-whisperer-relaxaurus-hungry-gunner',52.8,10.5),
('lamball-stone-pit-pr','purple-red-lamball-stone-pit','purple-red-menasting-darkness-dwelling-scorpion-blazehowl-noct-darkflame-defender',53.9,7.9),
('tombat-medicine-gp','green-purple-medieval-medicine-workbench-tombat','green-purple-tombat-out-of-nowhere-katress-abyssal-sorcerer',44.4,5.5),
('machine-gun-furnace-br','blue-red-mounted-machine-gun-primitive-furnace','blue-red-suzaku-hellfire-wings-primitive-furnace-2',47.1,5.3),
('shadowbeak-menasting-bp','blue-purple-shadowbeak-menasting','blue-purple-shadowbeak-seed-of-despair-menasting-darkness-dwelling-scorpion',39.5,5.2),
('foxparks-harness-br','blue-red-foxparks-foxparks-harness','blue-red-foxparks-light-of-courage-foxparks-harness',51.7,4.2),
('cattiva-azurobe-br','blue-red-cattiva-azurobe','blue-red-cattiva-my-first-pal-fuack-manic-wave-ripper',59.2,4.0),
('pengullet-launcher-bg','blue-green-pengullet-rocket-launcher-pengullet','blue-green-pengullet-rocket-launcher-pengullet-yearning-for-the-sky',45.8,3.9),
('foxparks-harness-pr','purple-red-foxparks-foxparks-harness','purple-red-foxparks-light-of-courage-foxparks-harness',48.0,3.6),
('lamball-cattiva-bg','blue-green-lamball-cattiva','blue-green-chillet-dragon-whisperer-lamball-my-first-pal',58.6,3.4),
('furnace-machine-gun-gr','green-red-primitive-furnace-mounted-machine-gun','green-red-mounted-machine-gun-primitive-furnace',43.3,2.3),
('chillet-relaxaurus-bg','blue-green-chillet-relaxaurus','blue-green-chillet-dragon-whisperer-elphidran-gentle-radiance',47.5,1.2),
]
rows=[
[50,52,53,60,56,64,55,44,60,62,49,63],
[48,50,47,56,54,63,50,44,52,51,45,60],
[47,53,50,61,65,68,50,44,58,45,41,57],
[40,44,39,50,45,57,45,42,45,43,36,49],
[44,46,35,55,50,56,42,40,51,42,43,50],
[36,37,32,43,44,50,38,30,44,44,28,46],
[45,50,50,55,58,62,50,44,60,57,41,61],
[56,56,56,58,60,70,56,50,67,61,51,61],
[40,48,42,55,49,56,40,33,50,49,35,52],
[38,49,55,57,58,56,43,39,51,50,39,58],
[51,55,59,64,57,72,59,49,65,61,50,61],
[37,40,43,51,50,54,39,39,48,42,39,50],
]
rank_order=[7,10,0,2,1,6,9,12,4,8,3,11,5]
matchups=[dict(deck_a=observed[i][0],deck_b=observed[j][0],win_rate_a=n/100,games=None,source='palworldtcg.gg') for i,row in enumerate(rows) for j,n in enumerate(row)]
tiers=[dict(deck=observed[i][0],win_rate=observed[i][3]/100,play_rate=observed[i][4]/100) for i in rank_order]
save(C/'matchups_2026-09-29.json',matchups)
save(C/'tiers_2026-09-29.json',tiers)
save(S/'slug-mapping.json',[dict(normalized_slug=d[0],source_deck_slug=d[1],source_old_slug=d[2],source_url='https://palworldtcg.gg/meta/decks/'+d[1]) for d in observed])
save(S/'observed-matrix.json',dict(source='https://palworldtcg.gg/meta/matchups',order=[d[0] for d in observed[:12]],displayed_percentages=rows))
save(S/'observed-tiers.json',[dict(slug=d[0],displayed_win_rate_percent=d[3],displayed_play_rate_percent=d[4]) for d in observed])
snapshot=Path('/home/gator/.hermes/cache/web/browser-snapshot-005ddbc560.txt')
if snapshot.exists(): shutil.copyfile(snapshot,S/'matchups-browser-snapshot.txt')
raw=Path('/tmp/palify-cards-response').read_bytes()
cards=json.loads(raw)
assert len(matchups)==144 and len(tiers)==13
assert all(len(r)==12 for r in rows)
assert all(rows[i][j]+rows[j][i]==100 for i in range(12) for j in range(12))
assert all(rows[i][i]==50 for i in range(12))
assert len({(r['deck_a'],r['deck_b']) for r in matchups})==144
save(S/'provenance.json',dict(
 captured_at_phoenix=datetime.now(ZoneInfo('America/Phoenix')).isoformat(),source_updated_date='2026-09-29',
 source_urls=['https://palworldtcg.gg/meta','https://palworldtcg.gg/meta/matchups','https://palify.org/meta'],
 status='partial_blocked',
 browser_verification={'meta':{'time_window':'30 days','game_type':'All','aria_current':'page'},'matchups':{'time_window':'30 days','game_type':'All','matrix_size':'Top 12','aria_current':'page'}},
 filters_note='Verified aria-current=page on 30 days and All links on both loaded browser pages; Top 12 on matchups. No filter defaults guessed.',
 matrix_note='12 most played, not 12 highest win-rate. Both directed cells and 12 mirrors retained. Whole-percent display precision; games not shown, hence null.',
 tiers_note='13-deck union of 12 highest-ranked tier rows and 12 most-played matrix decks. win_rate is the prominent displayed field-adjusted percentage, NOT the smaller raw or vs-meta percentage. Sorted by displayed tier-list rank.',
 decklist_status='No representative lists retrieved or invented. HTTP 403 stopped further network collection. main50/soul10/code validation not performed because lists unavailable.',
 requested_top8=[d[0] for d in sorted(observed,key=lambda d:d[4],reverse=True)[:8]],
 blocks=[{'url':url,'client':'Python urllib.request.urlopen (25s timeout)','exact_error':'HTTP Error 403: Forbidden'} for url in ['https://palworldtcg.gg/meta','https://palworldtcg.gg/meta/matchups','https://palify.org/meta']],
 block_handling='Browser meta and matchup navigations succeeded before direct archival fetches returned 403. No subsequent network requests, alternate identities, challenge bypass or retries. Only already-loaded matchup DOM inspected afterward.',
 card_catalog={'path':'/tmp/palify-cards-response','sha256':hashlib.sha256(raw).hexdigest(),'cards':len(cards['cards']),'fetched_again':False},
 verification={'matrix_records':144,'matrix_decks':12,'tier_records':13,'slug_mappings':13,'mirror_cells':12,'reciprocity_checks':'passed','decks_retrieved':0,'decks_validated_main50_soul10':0}
))
print(json.dumps({'matchups':len(matchups),'tiers':len(tiers),'slug_mappings':len(observed),'matrix_reciprocity':'passed','decklists':0,'status':'partial_blocked'}))
