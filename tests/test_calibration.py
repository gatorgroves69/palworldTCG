"""Offline evidence/schema checks for the initial observed snapshot; not deck readiness."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data/sources/2026-09-29'
CAL = ROOT / 'data/calibration'


class CalibrationTests(unittest.TestCase):
    def test_matrix_schema_and_browser_evidence(self):
        rows = json.loads((CAL / 'matchups_2026-09-29.json').read_text())
        observed = json.loads((SOURCE / 'observed-matrix.json').read_text())
        snapshot = (SOURCE / 'matchups-browser-snapshot.txt').read_text()
        cells = [int(n) for n in re.findall(r'- cell "(\d+)%"', snapshot)]
        self.assertEqual(cells, [n for row in observed['displayed_percentages'] for n in row])
        self.assertEqual(len(rows), 144)
        pairs = {(r['deck_a'], r['deck_b']): r['win_rate_a'] for r in rows}
        self.assertEqual(len(pairs), 144)
        for i, a in enumerate(observed['order']):
            for j, b in enumerate(observed['order']):
                self.assertEqual(pairs[a, b], observed['displayed_percentages'][i][j] / 100)
                self.assertAlmostEqual(pairs[a, b] + pairs[b, a], 1)
        for row in rows:
            self.assertEqual(set(row), {'deck_a', 'deck_b', 'win_rate_a', 'games', 'source'})
            self.assertIsNone(row['games'])
            self.assertEqual(row['source'], 'palworldtcg.gg')
            self.assertTrue(0 <= row['win_rate_a'] <= 1)

    def test_tiers_match_browser_evidence(self):
        rows = {r['deck']: r for r in json.loads((CAL / 'tiers_2026-09-29.json').read_text())}
        source = json.loads((SOURCE / 'meta-browser-observation.json').read_text())
        links = {r['href']: r['text'] for r in source['links']}
        mapping = json.loads((SOURCE / 'slug-mapping.json').read_text())
        for entry in mapping:
            text = links['/meta/decks/' + entry['source_deck_slug']]
            rates = re.search(r': ([\d.]+)%, ([\d.]+)%', text)
            self.assertIsNotNone(rates)
            assert rates
            row = rows[entry['normalized_slug']]
            self.assertAlmostEqual(row['win_rate'], float(rates[1])/100)
            self.assertAlmostEqual(row['play_rate'], float(rates[2])/100)
        active = [r['text'] for r in source['filters'] if r['current'] == 'page']
        self.assertEqual(active, ['30 days', 'All'])

    def test_top8_selected_by_play_rate(self):
        rows = json.loads((CAL / 'tiers_2026-09-29.json').read_text())
        expected = [r['deck'] for r in sorted(rows, key=lambda r:r['play_rate'], reverse=True)[:8]]
        provenance = json.loads((SOURCE / 'provenance.json').read_text())
        self.assertEqual(provenance['requested_top8'], expected)
        self.assertIn('cattiva-azurobe-br', expected)
        self.assertIn('chillet-relaxaurus-bp', expected)


if __name__ == '__main__':
    unittest.main()
