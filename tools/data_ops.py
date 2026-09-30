#!/usr/bin/env python3
"""Data-lane helpers only. Standard library; never imports or edits the engine."""
import argparse
import csv
import fcntl
import io
import json
import os
from pathlib import Path
import re
import tempfile
import urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ['date', 'event', 'my_deck', 'opp_deck', 'first_or_second', 'result', 'notes']


def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == content:
        return False
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as f:
        f.write(content)
        tmp = f.name
    os.replace(tmp, path)
    return True


def config(root):
    return json.loads((root / 'config/operator.json').read_text())


def check_cards(raw):
    data = json.loads(raw)
    cards = data['cards']
    if not cards or len(cards) != data['count']:
        raise ValueError('Invalid card count')
    # Palify includes SOUL-001 twice, one for each starter set. Preserve raw
    # JSON unchanged; code membership validation only needs one representative.
    return {c['code']: c for c in cards}


def fetch_cards(root, cached=None):
    # Exactly one network request, no redirects, retries or pagination.
    if cached:
        raw = Path(cached).read_bytes()
    else:
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *args, **kwargs):
                return None
        opener = urllib.request.build_opener(NoRedirect)
        request = urllib.request.Request('https://palify.org/api/cards', headers={'User-Agent': 'palworldTCG-data/1.0 (read-only weekly collection)'})
        with opener.open(request, timeout=30) as response:
            raw = response.read()
    cards = check_cards(raw)
    changed = atomic_write(root / 'data/cards.json', raw)
    return {'entries': json.loads(raw)['count'], 'unique_codes': len(cards), 'changed': changed}


def validate_deck(path, cards):
    totals = {'main': 0, 'soul': 0}
    seen = set()
    section = None
    errors = []
    for number, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        if line in ('# main', '# soul'):
            section = line[2:]
            if section in seen:
                errors.append(f'line {number}: duplicate section')
            seen.add(section)
            continue
        match = re.fullmatch(r'([1-9]\d*) ([A-Z0-9]+-\d+) (.+)', line)
        if section is None or not match:
            errors.append(f'line {number}: invalid format')
            continue
        quantity, code, name = match.groups()
        totals[section] += int(quantity)
        if code not in cards:
            errors.append(f'line {number}: unknown code {code}')
    if totals != {'main': 50, 'soul': 10}:
        errors.append(f'expected main=50 soul=10; got {totals}')
    return {'deck': path.stem, **totals, 'errors': errors}


def parse_game(text, cfg, date=None, my_deck=None):
    # log W chillet-bp 1st weekly — optional notes
    match = re.fullmatch(r'log\s+([WLD])\s+([a-z0-9-]+)\s+(1st|2nd|first|second)\s+(weekly|palify|casual)(?:\s+[—–-]\s*(.*))?', text.strip(), re.I)
    if not match:
        raise ValueError('Use: log W|L|D opponent 1st|2nd weekly|palify|casual — notes. For another own deck use --my-deck.')
    result, opponent, order, event, notes = match.groups()
    aliases = cfg.get('aliases', {})
    own = my_deck or cfg['default_deck']
    own = aliases.get(own, own)
    if not re.fullmatch(r'[a-z0-9-]+', own):
        raise ValueError('Invalid my-deck slug')
    day = date or datetime.now(ZoneInfo(cfg['timezone'])).date().isoformat()
    datetime.strptime(day, '%Y-%m-%d')
    return dict(zip(FIELDS, [day, event.lower(), own, aliases.get(opponent.lower(), opponent.lower()), 'first' if order.lower() in ('1st', 'first') else 'second', result.upper(), notes or '']))


def log_game(root, text, date=None, my_deck=None):
    row = parse_game(text, config(root), date, my_deck)
    path = root / 'data/games/real_games.csv'
    path.parent.mkdir(parents=True, exist_ok=True)
    # Lock on stable separate file so atomic CSV replacement remains safe.
    with (path.parent / '.logger.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        old = path.read_text() if path.exists() else ''
        if old and next(csv.reader(io.StringIO(old))) != FIELDS:
            raise ValueError('CSV header mismatch; refusing append')
        out = io.StringIO(newline='')
        writer = csv.DictWriter(out, fieldnames=FIELDS, lineterminator='\n')
        if not old:
            writer.writeheader()
        writer.writerow(row)
        atomic_write(path, (old + out.getvalue()).encode())
    return row


def stats(rows):
    n = len(rows)
    wins = sum(r['result'] == 'W' for r in rows)
    return {'games': n, 'wins': wins, 'losses': sum(r['result'] == 'L' for r in rows), 'draws': sum(r['result'] == 'D' for r in rows), 'win_rate': wins/n if n else None}


def report(root, month=None):
    path = root / 'data/games/real_games.csv'
    with path.open(newline='') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != FIELDS:
            raise ValueError('CSV header mismatch')
        rows = list(reader)
    if month:
        datetime.strptime(month, '%Y-%m')
        rows = [r for r in rows if r['date'].startswith(month + '-')]
    if any(r['result'] not in ('W', 'L', 'D') or r['first_or_second'] not in ('first', 'second') for r in rows):
        raise ValueError('Invalid result/order in CSV')
    return {'month': month or 'all-time', 'definition': 'wins / all games (draws included in denominator)', 'overall': stats(rows), 'by_opponent': {opp: stats([r for r in rows if r['opp_deck'] == opp]) for opp in sorted({r['opp_deck'] for r in rows})}, 'by_turn': {turn: stats([r for r in rows if r['first_or_second'] == turn]) for turn in ('first', 'second')}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    subs = parser.add_subparsers(dest='action', required=True)
    fetch = subs.add_parser('cards')
    fetch.add_argument('--cached', help='Use already fetched raw response, without networking')
    subs.add_parser('validate')
    log = subs.add_parser('log')
    log.add_argument('text')
    log.add_argument('--date')
    log.add_argument('--my-deck')
    rep = subs.add_parser('report')
    rep.add_argument('--month')
    rep.add_argument('--previous-month', action='store_true')
    args = parser.parse_args()
    if args.action == 'cards':
        out = fetch_cards(args.root, args.cached)
    elif args.action == 'validate':
        cards = check_cards((args.root / 'data/cards.json').read_bytes())
        paths = sorted((args.root / 'data/decks').glob('*.txt'))
        out = [validate_deck(p, cards) for p in paths]
        print(json.dumps(out, indent=2))
        raise SystemExit(0 if paths and not any(r['errors'] for r in out) else 1)
    elif args.action == 'log':
        out = log_game(args.root, args.text, args.date, args.my_deck)
    else:
        month = args.month
        if args.previous_month:
            today = datetime.now(ZoneInfo(config(args.root)['timezone'])).date()
            month = (today.replace(day=1) - timedelta(days=1)).strftime('%Y-%m')
        out = report(args.root, month)
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
