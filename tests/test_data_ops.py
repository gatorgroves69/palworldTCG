import csv
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('data_ops', Path(__file__).resolve().parents[1] / 'tools/data_ops.py')
assert spec is not None and spec.loader is not None
ops = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ops)


class DataOpsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / 'config').mkdir()
        (self.root / 'config/operator.json').write_text(json.dumps({'default_deck': 'cattiva-azurobe-br', 'timezone': 'America/Phoenix', 'aliases': {'chillet-bp': 'chillet-relaxaurus-bp'}}))

    def tearDown(self):
        self.tmp.cleanup()

    def test_game_and_csv_quotes(self):
        row = ops.log_game(self.root, 'log W chillet-bp 1st weekly — drew stone pit early, opp bricked', '2026-09-29')
        self.assertEqual(row['my_deck'], 'cattiva-azurobe-br')
        self.assertEqual(row['opp_deck'], 'chillet-relaxaurus-bp')
        with (self.root / 'data/games/real_games.csv').open() as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(rows, [row])

    def test_summary_and_own_override(self):
        ops.log_game(self.root, 'log W chillet-bp 1st weekly', '2026-09-29')
        ops.log_game(self.root, 'log L chillet-bp 2nd casual', '2026-09-29', 'chillet-bp')
        ops.log_game(self.root, 'log D other 2nd palify', '2026-08-29')
        out = ops.report(self.root, '2026-09')
        self.assertEqual(out['overall']['win_rate'], 0.5)
        self.assertEqual(out['by_turn']['first']['win_rate'], 1)
        self.assertEqual(out['by_turn']['second']['win_rate'], 0)
        self.assertEqual(out['overall']['games'], 2)
        self.assertEqual(ops.report(self.root)['overall']['draws'], 1)

    def test_reject_malformed(self):
        cfg = ops.config(self.root)
        for text in ('log W chillet weekly', 'log X chillet 1st casual', 'log W chillet 1st unknown'):
            with self.assertRaises(ValueError):
                ops.parse_game(text, cfg)

    def test_deck_counts_and_unknowns(self):
        deck = self.root / 'test.txt'
        deck.write_text('# main\n50 TD02-023 Cattiva – My First Pal\n# soul\n10 S01-001 Soul\n')
        cards = {'TD02-023': {}, 'S01-001': {}}
        self.assertEqual(ops.validate_deck(deck, cards)['errors'], [])
        self.assertTrue(ops.validate_deck(deck, {})['errors'])
        deck.write_text('# main\n49 TD02-023 Cattiva\n# soul\n10 S01-001 Soul\n')
        self.assertTrue(ops.validate_deck(deck, cards)['errors'])

    def test_cached_cards_raw_and_no_change(self):
        source = self.root / 'response.json'
        raw = b'{"count":1,"cards":[{"code":"TD02-023","name":"Cattiva"}]}\n'
        source.write_bytes(raw)
        self.assertTrue(ops.fetch_cards(self.root, source)['changed'])
        target = self.root / 'data/cards.json'
        before = target.stat().st_mtime_ns
        self.assertFalse(ops.fetch_cards(self.root, source)['changed'])
        self.assertEqual(target.read_bytes(), raw)
        self.assertEqual(target.stat().st_mtime_ns, before)

    def test_duplicate_soul_entries_are_preserved(self):
        source = self.root / 'souls.json'
        source.write_text(json.dumps({'count': 2, 'cards': [{'code': 'SOUL-001', 'set': 'TD01'}, {'code': 'SOUL-001', 'set': 'TD02'}]}))
        result = ops.fetch_cards(self.root, source)
        self.assertEqual(result['entries'], 2)
        self.assertEqual(result['unique_codes'], 1)
        self.assertEqual((self.root / 'data/cards.json').read_bytes(), source.read_bytes())

    def test_empty_report_is_not_zero_percent(self):
        target = self.root / 'data/games/real_games.csv'
        target.parent.mkdir(parents=True)
        target.write_text(','.join(ops.FIELDS) + '\n')
        self.assertIsNone(ops.report(self.root)['overall']['win_rate'])

    def test_bad_card_response_does_not_overwrite(self):
        path = self.root / 'invalid.json'
        path.write_text('{"count":2,"cards":[]}')
        with self.assertRaises(ValueError):
            ops.fetch_cards(self.root, path)
        self.assertFalse((self.root / 'data/cards.json').exists())


if __name__ == '__main__':
    unittest.main()
