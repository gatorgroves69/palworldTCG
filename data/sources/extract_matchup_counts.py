"""Extract explicit tooltip counts from a saved public matchup HTML response."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import sys
from bs4 import BeautifulSoup

html_path = Path(sys.argv[1])
root = Path(__file__).resolve().parents[2]
old = json.loads((root / 'data/calibration/matchups_2026-09-29.json').read_text())
slugs = list(dict.fromkeys(r['deck_a'] for r in old))
assert len(slugs) == 12 and len(old) == 144
html = html_path.read_bytes()
soup = BeautifulSoup(html, 'html.parser')
table = soup.select('table')[0]
trs = table.select('tr')
headers = [re.sub(r'^\d+\s+', '', e.get_text(' ', strip=True)) for e in trs[0].select('th')[1:]]
assert len(headers) == len(slugs) and len(trs) == 13
active = [e.get_text(' ', strip=True) for e in soup.select('[aria-current="page"]')]
assert all(x in active for x in ('30 days', 'All', 'Top 12'))
rows, evidence = [], []
for i, tr in enumerate(trs[1:]):
    label = re.sub(r'^\d+\s+', '', tr.select_one('th').get_text(' ', strip=True))
    assert label == headers[i]
    cells = tr.select('td')
    assert len(cells) == 12
    for j, cell in enumerate(cells):
        tooltip = cell.select_one('[title]')['title']
        assert tooltip.startswith(headers[i] + ' · ' + headers[j] + ' · ')
        match = re.search(r' · ([\d,]+) games$', tooltip)
        assert match, tooltip
        row = dict(old[i * 12 + j])
        assert row['deck_a'] == slugs[i] and row['deck_b'] == slugs[j]
        # Preserve the baseline's whole-percent displayed win rate; verify unchanged.
        rate = float(cell.get_text(strip=True).rstrip('%')) / 100
        assert rate == row['win_rate_a']
        row['games'] = int(match[1].replace(',', ''))
        assert row['games'] > 0
        rows.append(row)
        evidence.append({'deck_a': row['deck_a'], 'deck_b': row['deck_b'], 'tooltip': tooltip})
for i in range(12):
    for j in range(12):
        assert rows[i*12+j]['games'] == rows[j*12+i]['games']
now = datetime.datetime.now(datetime.timezone.utc)
date = now.date().isoformat()
out = root / f'data/calibration/matchups_{date}.json'
assert not out.exists(), f'Refusing overwrite: {out}'
source = root / f'data/sources/{date}/matchup-counts.json'
source.parent.mkdir(parents=True, exist_ok=True)
source.write_text(json.dumps({'url': 'https://palworldtcg.gg/meta/matchups', 'http_status': 200, 'captured_at_utc': now.isoformat(), 'source_updated_date': soup.select_one('time').get_text(strip=True), 'html_sha256': hashlib.sha256(html).hexdigest(), 'filters': {'time_window': '30 days', 'game_type': 'All', 'matrix_size': 'Top 12'}, 'mapping': dict(zip(slugs, headers)), 'note': 'Explicit per-cell title counts, including source mirror counts as displayed. No estimates from shading or global totals. Win rates retain verified whole-percent baseline precision.', 'cells': evidence}, indent=2, ensure_ascii=False) + '\n')
out.write_text(json.dumps(rows, indent=2) + '\n')
print(f'{out.relative_to(root)}: {len(rows)} rows, all explicit positive games counts')
print('PASS: labels, filters, baseline rates, complete matrix, reciprocal counts')
print(f'Evidence: {source.relative_to(root)}')
