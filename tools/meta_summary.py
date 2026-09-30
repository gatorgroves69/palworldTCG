#!/usr/bin/env python3
"""Three-line meta movement report, measured by play rate, from saved snapshots."""
import json
from pathlib import Path
from data_ops import ROOT


def summarize(current, previous=None):
    now = {r['deck']: r for r in current}
    if not now:
        raise ValueError('Empty current tiers')
    top = sorted(now, key=lambda d: (-now[d]['play_rate'], d))[:5]
    if previous is None:
        return 'Rose: baseline only; no previous snapshot.\nFell: baseline only; no previous snapshot.\nNew in top 5: baseline — ' + ', '.join(top)
    old = {r['deck']: r for r in previous}
    changes = sorted(((now[d]['play_rate'] - old[d]['play_rate'], d) for d in now.keys() & old.keys()), reverse=True)
    up = [x for x in changes if x[0] > 1e-9][:3]
    down = sorted(x for x in changes if x[0] < -1e-9)[:3]
    def describe(items):
        return ', '.join(f'{d} {change * 100:+.1f}pp play rate' for change, d in items) or 'none among comparable decks'
    old_top = set(sorted(old, key=lambda d: (-old[d]['play_rate'], d))[:5])
    entered = [d for d in top if d not in old_top]
    return 'Rose: ' + describe(up) + '\nFell: ' + describe(down) + '\nNew in top 5: ' + (', '.join(entered) or 'none')


if __name__ == '__main__':
    paths = sorted((ROOT / 'data/calibration').glob('tiers_????-??-??.json'))
    if not paths:
        raise SystemExit('No tier snapshots; cannot report trends')
    current = json.loads(paths[-1].read_text())
    previous = json.loads(paths[-2].read_text()) if len(paths) > 1 else None
    print(summarize(current, previous))
