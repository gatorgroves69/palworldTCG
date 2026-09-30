#!/usr/bin/env python3
"""Previous calendar-month real-game report; no network and no LLM."""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from data_ops import ROOT, config, report


def render(data):
    def metric(s):
        if not s['games']:
            return 'no games'
        return f"{s['win_rate']:.1%} ({s['wins']}W/{s['losses']}L/{s['draws']}D; n={s['games']})"
    lines = [f"Palworld real games — {data['month']}", 'Overall: ' + metric(data['overall'])]
    if not data['overall']['games']:
        return '\n'.join(lines)
    lines.append('By opponent:')
    lines.extend(f"• {opp}: {metric(s)}" for opp, s in data['by_opponent'].items())
    lines.extend(f"{turn.title()}: {metric(s)}" for turn, s in data['by_turn'].items())
    lines.append('Win rate = wins / games; draws count in denominator. Small samples are descriptive, not predictive.')
    return '\n'.join(lines)


if __name__ == '__main__':
    today = datetime.now(ZoneInfo(config(ROOT)['timezone'])).date()
    month = (today.replace(day=1) - timedelta(days=1)).strftime('%Y-%m')
    print(render(report(ROOT, month)))
