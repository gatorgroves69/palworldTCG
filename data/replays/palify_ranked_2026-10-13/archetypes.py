"""Conservative, offline main-deck inference; NOT an authoritative Palify label.

API: classify(public_deck: dict) -> JSON-serializable dict. No I/O or dependencies.
Frozen reference snapshot: repository data/decks/*.txt (ten 50-card main lists,
excluding synthetic Souls), data/sources/2026-09-29/slug-mapping.json and card
colors from data/cards.json, captured for the 2026-10-13 collection. The README
attributes the last two exports to 2026-09-30. These are canonical local examples,
not exhaustive coverage, ranked-population evidence, or a calibration dataset.

Identity compares every code AND multiplicity. Otherwise classification requires
engine signatures, not nearest-neighbor overlap. Rules deliberately privilege
Stone Pit over incidental furnace/gun, medicine/Tombat over generic purple
finishers, and first-Pal swarms over incidental dragons. Independent conflicting
engines abstain as mixed. Rocket Launcher is only a primary engine without a
Chillet/Relaxaurus engine (the frozen BP Chillet list contains three launchers).
Thresholds are conservative authored heuristics, not calibrated probabilities.
Confidence 1.0 means exact local list identity, NOT site-authoritative archetype.
Unknown is a valid deck outside our evidence, never evidence of an absent deck.

Names and group types do not establish identity. Codes are case-normalized, but
alternate printings are NOT guessed equivalent. Known card colors are frozen;
unknown codes may contribute supplied standard color metadata. Two colors need
at least four copies each; a third such color or >10 unknown-color copies
prevents a color-specific label. No runtime reads of mutable repository data.
"""
from collections import Counter

VERSION = "palify-offline-archetypes-v1"
REFERENCE_PROVENANCE = {
    "snapshot": "2026-10-13",
    "deck_sources": "data/decks/*.txt (main only; ten local examples)",
    "slug_source": "data/sources/2026-09-29/slug-mapping.json",
    "color_source": "data/cards.json",
    "coverage": "non-exhaustive; three mapped archetypes have no frozen list",
}
_FROZEN_LISTS = {
    'cattiva-azurobe-br': 'BP01-002:4 BP01-007:4 BP01-008:4 BP01-020:4 BP01-028:4 BP01-029:4 BP01-032:4 BP01-047:2 TD01-004:4 TD01-015:4 TD01-016:4 TD01-023:4 TD02-023:4',
    'chillet-relaxaurus-bg': 'BP01-025:4 BP01-026:4 BP01-027:2 BP01-034:3 BP01-038:4 BP01-046:4 BP01-047:4 BP01-048:4 BP01-049:2 BP01-071:3 BP01-098:4 TD01-012:4 TD01-016:4 TD02-004:4',
    'chillet-relaxaurus-bp': 'BP01-025:4 BP01-026:2 BP01-027:3 BP01-028:4 BP01-038:4 BP01-044:3 BP01-047:2 BP01-048:4 BP01-077:4 BP01-095:4 BP01-098:4 TD01-012:3 TD01-016:4 TD02-012:1 TD02-017:2 TD02-021:2',
    'chillet-relaxaurus-br': 'BP01-001:2 BP01-005:4 BP01-020:4 BP01-025:4 BP01-026:4 BP01-027:2 BP01-028:2 BP01-038:3 BP01-045:2 BP01-047:1 BP01-048:4 BP01-098:2 BP01-014:3 TD01-004:3 TD01-010:3 TD01-012:4 TD01-016:3',
    'foxparks-harness-br': 'BP01-001:4 BP01-005:4 BP01-006:4 BP01-014:4 BP01-019:4 BP01-020:4 BP01-023:3 BP01-025:4 BP01-038:4 BP01-047:4 BP01-048:4 TD01-004:4 TD01-010:3',
    'lamball-cattiva-bg': 'BP01-025:4 BP01-026:2 BP01-028:4 BP01-029:2 BP01-032:4 BP01-046:2 BP01-049:2 BP01-052:4 BP01-070:2 BP01-098:4 TD01-012:4 TD01-015:2 TD01-016:2 TD01-023:4 TD02-004:4 TD02-023:4',
    'lamball-stone-pit-pr': 'BP01-002:3 BP01-015:2 BP01-016:4 BP01-020:4 BP01-074:2 BP01-078:2 BP01-084:3 BP01-090:1 BP01-095:4 TD01-004:4 TD01-008:3 TD01-010:4 TD01-023:4 TD02-014:2 TD02-017:4 TD02-023:4',
    'machine-gun-furnace-br': 'BP01-001:4 BP01-002:4 BP01-005:2 BP01-007:2 BP01-012:4 BP01-015:4 BP01-016:4 BP01-020:4 BP01-038:4 BP01-045:2 BP01-047:1 TD01-004:4 TD01-010:4 TD01-016:4 TD01-023:3',
    'shadowbeak-menasting-bp': 'BP01-038:2 BP01-047:2 BP01-073:3 BP01-074:2 BP01-077:4 BP01-078:1 BP01-079:2 BP01-080:4 BP01-082:4 BP01-084:3 BP01-085:1 BP01-088:1 BP01-089:3 BP01-090:2 BP01-094:4 BP01-095:3 TD02-014:3 TD02-017:4 TD02-021:2',
    'tombat-medicine-gp': 'BP01-049:3 BP01-051:4 BP01-052:4 BP01-070:2 BP01-074:3 BP01-076:3 BP01-077:4 BP01-078:3 BP01-084:2 BP01-085:3 BP01-090:4 BP01-095:3 TD02-014:4 TD02-017:4 TD02-021:4',
}
REFERENCES = {
    slug: dict((code, int(n)) for code, n in (part.split(':') for part in text.split()))
    for slug, text in _FROZEN_LISTS.items()
}
_COLOR_CODES = {
    'Blue': 'BP01-025 BP01-026 BP01-027 BP01-028 BP01-029 BP01-032 BP01-034 BP01-038 BP01-044 BP01-045 BP01-046 BP01-047 BP01-048 TD01-012 TD01-014 TD01-015 TD01-016',
    'Purple': 'BP01-073 BP01-074 BP01-076 BP01-077 BP01-078 BP01-079 BP01-080 BP01-082 BP01-084 BP01-085 BP01-088 BP01-089 BP01-090 BP01-094 BP01-095 TD02-012 TD02-014 TD02-017 TD02-021',
    'Red': 'BP01-001 BP01-002 BP01-005 BP01-006 BP01-007 BP01-008 BP01-012 BP01-014 BP01-015 BP01-016 BP01-019 BP01-020 BP01-023 TD01-004 TD01-008 TD01-010',
    'Green': 'BP01-049 BP01-051 BP01-052 BP01-070 BP01-071 TD02-004',
    'Colorless': 'BP01-098 TD01-023 TD02-023',
}
COLORS = {code: color for color, codes in _COLOR_CODES.items() for code in codes.split()}
PALETTES = {'bg': ['Blue', 'Green'], 'bp': ['Blue', 'Purple'],
            'br': ['Blue', 'Red'], 'gp': ['Green', 'Purple'],
            'gr': ['Green', 'Red'], 'pr': ['Purple', 'Red']}
# Slug mapping is broader than the frozen ten-list overlap panel.
MAPPED_SLUGS = tuple(sorted((*REFERENCES, 'pengullet-launcher-bg',
                            'foxparks-harness-pr', 'furnace-machine-gun-gr')))
SIGNATURES = {
    'chillet-relaxaurus': {'BP01-025': 3, 'BP01-026': 2},
    'cattiva-azurobe': {'TD02-023': 3, 'BP01-029': 2, 'BP01-032': 2},
    'lamball-cattiva': {'TD01-023': 3, 'TD02-023': 3, 'BP01-032': 2},
    'lamball-stone-pit': {'TD01-023': 3, 'TD01-008': 2},
    'machine-gun-furnace': {'BP01-015': 2, 'BP01-016': 3},
    'tombat-medicine': {'BP01-076': 2, 'BP01-090': 3},
    'shadowbeak-menasting': {'BP01-074': 2, 'BP01-084': 2},
    'foxparks-harness': {'BP01-006': 2, 'BP01-019': 3},
    'pengullet-launcher': {'BP01-028': 3, 'BP01-044': 3},
}


def _family(slug):
    family = slug.rsplit('-', 1)[0]
    return 'machine-gun-furnace' if family == 'furnace-machine-gun' else family


def _parse(deck):
    counts, colors, errors = Counter(), Counter(), []
    if not isinstance(deck, dict) or not isinstance(deck.get('groups'), list):
        return counts, colors, ['deck.groups must be a list']
    total = deck.get('total', deck.get('total50'))
    if type(total) is not int or total != 50:
        errors.append('declared total must be integer 50 (total or total50)')
    for i, group in enumerate(deck['groups']):
        if not isinstance(group, dict) or not isinstance(group.get('items'), list):
            errors.append('invalid group at index %s' % i)
            continue
        if group.get('type') not in ('Pal', 'Event', 'Gear', 'Structure'):
            errors.append('unsupported main-deck group type at index %s' % i)
        subtotal = 0
        for item in group['items']:
            if not isinstance(item, dict):
                errors.append('item must be an object')
                continue
            code, n = item.get('code'), item.get('n')
            if not isinstance(code, str) or not code.strip() or type(n) is not int or n <= 0:
                errors.append('item requires nonempty code and positive integer n')
                continue
            code = code.strip().upper()
            if code.startswith('SOUL-'):
                errors.append('Souls are not main-deck cards')
            counts[code] += n
            subtotal += n
            supplied = item.get('color')
            color = COLORS.get(code)
            if color is None:
                color = supplied.strip().title() if isinstance(supplied, str) else 'Unknown'
                if color not in _COLOR_CODES:
                    color = 'Unknown'
            colors[color] += n
        if type(group.get('count')) is not int or group['count'] != subtotal:
            errors.append('group count mismatch at index %s' % i)
    if sum(counts.values()) != 50:
        errors.append('observed main count is not 50')
    return counts, colors, errors


def classify(deck: dict) -> dict:
    """Return inference, evidence, validation, and ten diagnostic overlap candidates.

    status: inferred | unknown | mixed | invalid_input. source is always inferred.
    canonical_slug is set only when the inferred family/palette is in the frozen
    mapping. candidates are ranked by copy overlap (ties slug-lexical), not votes;
    near ties report overlap ambiguity even when signatures resolve the family.
    No candidate score alone can produce a classification. Exact matches include
    all 50 copies as evidence. Incomplete/invalid inputs never earn an identity.
    """
    counts, colors, errors = _parse(deck)
    prominent = sorted(c for c, n in colors.items() if c not in ('Colorless', 'Unknown') and n >= 4)
    palette = next((p for p, cs in PALETTES.items() if cs == prominent), None)
    if colors['Unknown'] > 10:
        palette = None
    raw = {family for family, requirements in SIGNATURES.items()
           if all(counts[code] >= n for code, n in requirements.items())}
    active = set(raw)
    suppressed = {}

    def suppress(family, reason):
        if family in active:
            active.remove(family)
            suppressed[family] = reason

    if counts['BP01-027'] + counts['BP01-098'] + counts['TD01-012'] < 4:
        suppress('chillet-relaxaurus', 'dragon pair lacks corroborating dragon support')
    if not (counts['BP01-089'] >= 2 and counts['BP01-080'] + counts['BP01-082'] >= 4):
        suppress('shadowbeak-menasting', 'purple finishers lack discriminating bed / Daedream support')
    if 'lamball-stone-pit' in active:
        suppress('machine-gun-furnace', 'Stone Pit / Lamball is the more specific structure engine')
        suppress('shadowbeak-menasting', 'purple finishers occur in the Stone Pit reference')
    if 'tombat-medicine' in active:
        suppress('shadowbeak-menasting', 'Tombat / medicine is the more specific engine')
    if 'lamball-cattiva' in active and palette == 'bg':
        suppress('cattiva-azurobe', 'BG first-Pal swarm has incidental Azurobe')
        suppress('chillet-relaxaurus', 'BG first-Pal swarm has incidental dragons')
    else:
        # This prevents Cattiva dragons being promoted to the Chillet family even
        # when they lack Azurobe and therefore have no covered swarm signature.
        if counts['TD02-023'] >= 3:
            suppress('chillet-relaxaurus', 'Cattiva core makes the dragon engine ambiguous')
        suppress('lamball-cattiva', 'first-Pal BG family requires Blue/Green palette')
    if 'chillet-relaxaurus' in raw:
        suppress('pengullet-launcher', 'launcher may be support in Chillet/Relaxaurus')

    candidates = []
    for slug, reference in REFERENCES.items():
        shared = {code: min(n, counts[code]) for code, n in reference.items() if counts[code]}
        overlap = sum(shared.values())
        family = _family(slug)
        candidates.append({
            'canonical_slug': slug,
            'overlap_copies': overlap,
            'overlap_fraction': round(overlap / 50, 4),
            'overlap_codes': sorted(shared),
            'shared_counts': dict(sorted(shared.items())),
            'exact_count_identity': not errors and dict(counts) == reference,
            'signature_match': family in active,
            'palette_match': palette == slug.rsplit('-', 1)[1],
            'missing_signature_codes': sorted(c for c, n in SIGNATURES[family].items() if counts[c] < n),
        })
    candidates.sort(key=lambda c: (-c['exact_count_identity'], -c['overlap_copies'], c['canonical_slug']))
    best = candidates[0]
    margin = best['overlap_copies'] - candidates[1]['overlap_copies']
    result = {
        'classifier_version': VERSION, 'source': 'inferred', 'site_authoritative': False,
        'status': 'unknown', 'archetype': 'unknown', 'canonical_slug': None,
        'confidence': 0.0, 'confidence_kind': 'heuristic_not_probability',
        'evidence_codes': [], 'evidence_counts': {}, 'reason': '',
        'observed_total': sum(counts.values()), 'colors': dict(sorted(colors.items())),
        'palette': palette, 'validation_errors': errors,
        'reference_coverage': 'non_exhaustive', 'candidates': candidates,
        'ambiguity': {
            'overlap_margin_copies': margin,
            'overlap_near_ties': [c['canonical_slug'] for c in candidates
                                  if best['overlap_copies'] - c['overlap_copies'] <= 2],
            'competing_signatures': sorted(active),
            'suppressed_signatures': dict(sorted(suppressed.items())),
            'color_ambiguous': palette is None,
        },
    }
    if errors:
        result.update(status='invalid_input', reason='invalid or incomplete main-deck counts; no inference')
        return result
    if best['exact_count_identity']:
        slug = best['canonical_slug']
        result.update(status='inferred', archetype=slug, canonical_slug=slug,
                      confidence=1.0, reason='full exact 50-card code/count identity with frozen local reference',
                      evidence_codes=sorted(counts), evidence_counts=dict(sorted(counts.items())))
        return result
    evidence = sorted({c for f in raw for c in SIGNATURES[f]})
    result.update(evidence_codes=evidence, evidence_counts={c: counts[c] for c in evidence})
    if len(active) > 1:
        result.update(status='mixed', archetype='mixed', confidence=0.3,
                      reason='multiple independent engine signatures; abstaining')
    elif len(active) == 1:
        family = next(iter(active))
        slug = family + '-' + palette if palette else family
        if slug == 'machine-gun-furnace-gr':
            slug = 'furnace-machine-gun-gr'
        canonical = slug if slug in MAPPED_SLUGS else None
        confidence = 0.8 if canonical else 0.65
        result.update(status='inferred', archetype=slug, canonical_slug=canonical,
                      confidence=confidence, reason='engine signature; overlap is diagnostic only')
        codes = set(SIGNATURES[family])
        if family == 'chillet-relaxaurus':
            codes.update(c for c in ('BP01-027', 'BP01-098', 'TD01-012') if counts[c])
        if family == 'shadowbeak-menasting':
            codes.update(c for c in ('BP01-089', 'BP01-080', 'BP01-082') if counts[c])
        result.update(evidence_codes=sorted(codes), evidence_counts={c: counts[c] for c in sorted(codes)})
    else:
        result['reason'] = 'no unambiguous supported engine; valid deck may be outside reference coverage'
    return result
