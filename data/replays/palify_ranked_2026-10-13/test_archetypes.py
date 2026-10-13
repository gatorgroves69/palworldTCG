"""Bounded offline fixtures. Run: python -B -m unittest discover -s <this-dir> -v.
Synthetic mutations test inference boundaries; they are not ranked match data.
"""
import copy
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

_spec = importlib.util.spec_from_file_location('offline_archetypes', Path(__file__).with_name('archetypes.py'))
assert _spec is not None and _spec.loader is not None
a = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(a)


def deck(counts, color_overrides=None):
    overrides = color_overrides or {}
    return {'total': sum(counts.values()), 'groups': [
        {'type': 'Pal', 'count': sum(counts.values()), 'items': [
            {'code': code, 'n': n, 'name': 'fixture',
             'color': overrides.get(code, a.COLORS.get(code, 'Colorless'))}
            for code, n in counts.items()]}]}


def variant(slug, remove, add):
    counts = dict(a.REFERENCES[slug])
    for code, n in remove.items():
        counts[code] -= n
        if not counts[code]:
            del counts[code]
    for code, n in add.items():
        counts[code] = counts.get(code, 0) + n
    return deck(counts)


def padded(core, colors=None):
    counts = dict(core)
    left = 50 - sum(counts.values())
    i = 0
    while left:
        n = min(4, left)
        counts['UNSEEN-%03d' % i] = n
        left -= n
        i += 1
    return deck(counts, colors)


class ArchetypesTests(unittest.TestCase):
    def test_frozen_reference_integrity_and_exact_identity(self):
        self.assertEqual(len(a.REFERENCES), 10)
        for slug, counts in a.REFERENCES.items():
            with self.subTest(slug=slug):
                self.assertEqual(sum(counts.values()), 50)
                self.assertTrue(all(0 < n <= 4 for n in counts.values()))
                result = a.classify(deck(counts))
                self.assertEqual(result['archetype'], slug)
                self.assertEqual(result['confidence'], 1.0)
                self.assertTrue(result['candidates'][0]['exact_count_identity'])
                self.assertEqual(result['candidates'][0]['overlap_copies'], 50)
                self.assertEqual(sum(result['evidence_counts'].values()), 50)
                self.assertFalse(result['site_authoritative'])
                self.assertEqual(result['source'], 'inferred')

    def test_chillet_blue_purple_and_blue_red_variants(self):
        for suffix in ('bp', 'br'):
            slug = 'chillet-relaxaurus-' + suffix
            result = a.classify(variant(slug, {'BP01-047': 1}, {'UNSEEN-001': 1}))
            self.assertEqual(result['archetype'], slug)
            self.assertEqual(result['confidence'], .8)
            self.assertFalse(result['candidates'][0]['exact_count_identity'])
            self.assertIn('BP01-025', result['evidence_codes'])
            self.assertIn('BP01-026', result['evidence_codes'])

    def test_cattiva_dragons_not_chillet(self):
        result = a.classify(variant('lamball-cattiva-bg', {'BP01-046': 1}, {'UNSEEN-001': 1}))
        self.assertEqual(result['archetype'], 'lamball-cattiva-bg')
        self.assertIn('chillet-relaxaurus', result['ambiguity']['suppressed_signatures'])

    def test_uncovered_cattiva_dragons_abstain(self):
        result = a.classify(variant('chillet-relaxaurus-br', {'BP01-005': 4}, {'TD02-023': 4}))
        self.assertEqual(result['status'], 'unknown')
        self.assertNotIn('chillet-relaxaurus', result['archetype'])

    def test_cattiva_azurobe_variant(self):
        result = a.classify(variant('cattiva-azurobe-br', {'BP01-047': 1}, {'UNSEEN-001': 1}))
        self.assertEqual(result['archetype'], 'cattiva-azurobe-br')

    def test_structure_engine_disambiguation(self):
        for slug, removal in [('lamball-stone-pit-pr', 'BP01-020'),
                              ('machine-gun-furnace-br', 'BP01-047'),
                              ('tombat-medicine-gp', 'BP01-095')]:
            with self.subTest(slug=slug):
                result = a.classify(variant(slug, {removal: 1}, {'UNSEEN-001': 1}))
                self.assertEqual(result['archetype'], slug)
                self.assertEqual(result['status'], 'inferred')

    def test_structure_signature_removal_not_nearest_neighbor(self):
        result = a.classify(variant('machine-gun-furnace-br', {'BP01-016': 4}, {'UNSEEN-001': 4}))
        self.assertEqual(result['status'], 'unknown')
        self.assertEqual(result['candidates'][0]['canonical_slug'], 'machine-gun-furnace-br')
        self.assertEqual(result['candidates'][0]['overlap_copies'], 46)
        self.assertIn('BP01-016', result['candidates'][0]['missing_signature_codes'])

    def test_multiple_independent_engines_are_mixed(self):
        result = a.classify(variant('chillet-relaxaurus-br',
                                   {'BP01-005': 4, 'BP01-014': 3},
                                   {'BP01-015': 3, 'BP01-016': 4}))
        self.assertEqual(result['status'], 'mixed')
        self.assertEqual(result['archetype'], 'mixed')
        self.assertIsNone(result['canonical_slug'])
        self.assertIn('BP01-016', result['evidence_codes'])

    def test_no_reference_does_not_mean_no_deck(self):
        d = padded({'BP01-028': 4, 'BP01-044': 4, 'BP01-049': 4})
        result = a.classify(d)
        self.assertEqual(result['archetype'], 'pengullet-launcher-bg')
        self.assertEqual(result['observed_total'], 50)
        self.assertNotIn(result['canonical_slug'], a.REFERENCES)
        self.assertLess(result['candidates'][0]['overlap_fraction'], .5)
        self.assertEqual(result['reference_coverage'], 'non_exhaustive')

    def test_other_mapped_families_without_lists(self):
        for core, expected in [
            ({'BP01-006': 4, 'BP01-019': 4, 'BP01-077': 4}, 'foxparks-harness-pr'),
            ({'BP01-015': 4, 'BP01-016': 4, 'BP01-049': 4}, 'furnace-machine-gun-gr'),
        ]:
            self.assertEqual(a.classify(padded(core))['archetype'], expected)

    def test_generic_purple_finishers_are_not_control_engine(self):
        result = a.classify(padded({'BP01-074': 3, 'BP01-084': 3, 'BP01-038': 4}))
        self.assertEqual(result['status'], 'unknown')
        control = a.classify(variant('shadowbeak-menasting-bp', {'BP01-095': 1}, {'UNSEEN-001': 1}))
        self.assertEqual(control['archetype'], 'shadowbeak-menasting-bp')
        self.assertIn('BP01-089', control['evidence_codes'])

    def test_chillet_signature_removed_abstains_despite_46_overlap(self):
        result = a.classify(variant('chillet-relaxaurus-br', {'BP01-025': 4}, {'UNSEEN-001': 4}))
        self.assertEqual(result['status'], 'unknown')
        self.assertEqual(result['candidates'][0]['overlap_copies'], 46)

    def test_unknown_full_deck_is_valid_and_has_candidate_ties(self):
        result = a.classify(padded({}))
        self.assertEqual(result['status'], 'unknown')
        self.assertEqual(result['validation_errors'], [])
        self.assertEqual(result['observed_total'], 50)
        self.assertEqual(len(result['ambiguity']['overlap_near_ties']), 10)
        self.assertEqual(result['ambiguity']['overlap_margin_copies'], 0)
        self.assertEqual(result['confidence'], 0)

    def test_exact_requires_multiplicity_not_just_card_set(self):
        result = a.classify(variant('chillet-relaxaurus-bp', {'BP01-025': 1}, {'BP01-026': 1}))
        self.assertFalse(any(c['exact_count_identity'] for c in result['candidates']))
        self.assertLess(result['confidence'], 1)
        self.assertEqual(result['candidates'][0]['overlap_copies'], 49)

    def test_order_duplicates_and_case_normalization(self):
        d = deck(a.REFERENCES['chillet-relaxaurus-br'])
        first = d['groups'][0]['items'][0]
        first['n'] -= 1
        d['groups'][0]['items'].append(dict(first, n=1, code=first['code'].lower()))
        d['groups'][0]['items'].reverse()
        self.assertEqual(a.classify(d)['confidence'], 1)

    def test_malformed_counts_never_exact(self):
        original = deck(a.REFERENCES['chillet-relaxaurus-br'])
        mutations = []
        for total in (49, True, '50', None):
            d = copy.deepcopy(original)
            d['total'] = total
            mutations.append(d)
        for n in (True, 0, -1, 1.5, '2'):
            d = copy.deepcopy(original)
            d['groups'][0]['items'][0]['n'] = n
            mutations.append(d)
        d = copy.deepcopy(original)
        d['groups'][0]['count'] = 49
        mutations.append(d)
        mutations.extend([None, {}, {'total': 50, 'groups': [None]}, {'total': 50, 'groups': []}])
        for d in mutations:
            with self.subTest(deck=d):
                result = a.classify(d)
                self.assertEqual(result['status'], 'invalid_input')
                self.assertEqual(result['confidence'], 0)
                self.assertFalse(any(c['exact_count_identity'] for c in result['candidates']))

    def test_souls_not_accepted_as_main(self):
        result = a.classify(padded({'SOUL-001': 4}))
        self.assertEqual(result['status'], 'invalid_input')

    def test_total50_alias(self):
        d = deck(a.REFERENCES['chillet-relaxaurus-br'])
        d['total50'] = d.pop('total')
        self.assertEqual(a.classify(d)['confidence'], 1)

    def test_names_and_incorrect_known_colors_do_not_override_codes(self):
        d = deck(a.REFERENCES['cattiva-azurobe-br'])
        for item in d['groups'][0]['items']:
            item.update(name='Chillet Relaxaurus', color='Purple')
        self.assertEqual(a.classify(d)['archetype'], 'cattiva-azurobe-br')

    def test_alternate_printing_not_guessed(self):
        result = a.classify(variant('chillet-relaxaurus-br', {'BP01-025': 4}, {'BP01-025SSP': 4}))
        self.assertFalse(any(c['exact_count_identity'] for c in result['candidates']))
        self.assertEqual(result['status'], 'unknown')

    def test_three_colors_not_forced_to_nearest_palette(self):
        result = a.classify(variant('chillet-relaxaurus-br', {'BP01-005': 4}, {'BP01-077': 4}))
        self.assertIsNone(result['palette'])
        self.assertEqual(result['archetype'], 'chillet-relaxaurus')
        self.assertIsNone(result['canonical_slug'])
        self.assertTrue(result['ambiguity']['color_ambiguous'])

    def test_pair_without_dragon_support_is_unknown(self):
        result = a.classify(padded({'BP01-025': 4, 'BP01-026': 4, 'BP01-077': 4}))
        self.assertEqual(result['status'], 'unknown')
        self.assertIn('chillet-relaxaurus', result['ambiguity']['suppressed_signatures'])

    def test_incidental_finishers_do_not_make_dragons_mixed(self):
        result = a.classify(variant('chillet-relaxaurus-bp',
                                   {'BP01-077': 4}, {'BP01-074': 2, 'BP01-084': 2}))
        self.assertEqual(result['archetype'], 'chillet-relaxaurus-bp')

    def test_unknown_color_mass_prevents_palette_guess(self):
        d = padded({'BP01-025': 4, 'BP01-026': 4, 'TD01-012': 4, 'BP01-077': 4})
        for item in d['groups'][0]['items']:
            if item['code'].startswith('UNSEEN'):
                item.pop('color')
        result = a.classify(d)
        self.assertIsNone(result['palette'])
        self.assertEqual(result['archetype'], 'chillet-relaxaurus')
        self.assertIsNone(result['canonical_slug'])

    def test_no_mutation_deterministic_json_serializable_no_io(self):
        d = deck(a.REFERENCES['chillet-relaxaurus-br'])
        before = copy.deepcopy(d)
        with patch('builtins.open', side_effect=AssertionError('no runtime IO')):
            first = a.classify(d)
            second = a.classify(d)
        self.assertEqual(d, before)
        self.assertEqual(first, second)
        json.dumps(first, allow_nan=False)
        overlaps = [c['overlap_copies'] for c in first['candidates']]
        self.assertEqual(overlaps, sorted(overlaps, reverse=True))


if __name__ == '__main__':
    unittest.main()
