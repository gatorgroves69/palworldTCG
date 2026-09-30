"""Per-run markdown report: `python -m analysis results/<run>/`

Reads summary.json + games.jsonl, adds loss tags, per-card draw impact, and
a comparison with the latest real-world matchup data in data/calibration/.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from .tags import tag_counts

CALIBRATION_DIR = Path(__file__).resolve().parent.parent / "data" / "calibration"
PASS_BAND = 0.05
MIN_N = 30


def load_run(run_dir: Path) -> tuple[dict, list[dict]]:
    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    with open(run_dir / "games.jsonl", encoding="utf-8") as f:
        games = [json.loads(line) for line in f if line.strip()]
    return summary, games


def draw_impact(games: list[dict], side: int) -> list[dict]:
    """Per card: deck win rate when drawn at least once minus when never drawn."""
    codes = sorted({c for g in games for c in g["drawn"][side]})
    rows = []
    for code in codes:
        yes = [g for g in games if code in g["drawn"][side]]
        no = [g for g in games if code not in g["drawn"][side]]
        if len(yes) < MIN_N or len(no) < MIN_N:
            continue

        def wr(gs):
            won = "deck" if side == 0 else "opp"
            return sum((g["winner"] == won) + 0.5 * (g["winner"] == "draw") for g in gs) / len(gs)
        p1, p0 = wr(yes), wr(no)
        se = math.sqrt(p1 * (1 - p1) / len(yes) + p0 * (1 - p0) / len(no))
        rows.append({"code": code, "drawn_wr": p1, "not_drawn_wr": p0, "delta": p1 - p0,
                     "n_drawn": len(yes), "n_not": len(no),
                     "significant": abs(p1 - p0) > 1.96 * se})
    return sorted(rows, key=lambda r: -r["delta"])


def calibration_target(deck: str, opp: str) -> dict | None:
    files = sorted(CALIBRATION_DIR.glob("matchups_*.json"))
    if not files:
        return None
    for row in json.loads(files[-1].read_text(encoding="utf-8")):
        if row.get("deck_a") == deck and row.get("deck_b") == opp:
            return {**row, "file": files[-1].name}
    return None


def _pct(x) -> str:
    return "n/a" if x is None else f"{100 * x:.1f}%"


def write_report(run_dir: Path) -> Path:
    from cards.db import load_card_db
    db = load_card_db()
    s, games = load_run(run_dir)
    name = lambda code: db[code].name if code in db else code  # noqa: E731
    L = []
    L.append(f"# {s['deck']} vs {s['opp']}")
    L.append("")
    L.append(f"{s['games']} games, bot `{s['bot']}`, seed {s['seed']}, commit `{s['commit']}`, "
             f"structures attackable: `{s['rules']['structures_attackable']}`.")
    L.append("")
    L.append("| | Win rate | 95% CI | Games |")
    L.append("|---|---|---|---|")
    for label, r in (("Overall", s), ("Going first", s["going_first"]),
                     ("Going second", s["going_second"])):
        L.append(f"| {label} | **{_pct(r['win_rate'])}** | {_pct(r['ci95'][0])} – "
                 f"{_pct(r['ci95'][1])} | {r['games']} |")
    L.append("")
    L.append(f"Average game length: {s['avg_turns']} turns. Game ends: "
             + ", ".join(f"{k} {v}" for k, v in s["end_reasons"].items()) + ".")
    cal = calibration_target(s["deck"], s["opp"])
    if cal:
        diff = s["win_rate"] - cal["win_rate_a"]
        ok = abs(diff) <= PASS_BAND
        L.append("")
        L.append(f"**Calibration** ({cal['file']}, {cal.get('source')}): real {_pct(cal['win_rate_a'])}"
                 f" (games: {cal.get('games')}), sim {_pct(s['win_rate'])}, "
                 f"difference {100 * diff:+.1f} points: "
                 + ("**PASS** (within ±5)" if ok else "**FAIL** (outside ±5)"))

    for loser, label in (("deck", s["deck"]), ("opp", s["opp"])):
        counts, n = tag_counts(games, db, loser)
        L.append("")
        L.append(f"## Why {label} loses ({n} losses)")
        L.append("")
        L.append("| Tag | Losses | Share |")
        L.append("|---|---|---|")
        for tag, k in counts.most_common(12):
            shown = tag
            if tag.startswith("lost_to:"):
                shown = f"lost to {name(tag.split(':', 1)[1])}"
            L.append(f"| {shown} | {k} | {_pct(k / n if n else None)} |")

    for side, label in ((0, s["deck"]), (1, s["opp"])):
        rows = draw_impact(games, side)
        L.append("")
        L.append(f"## Draw impact: {label}")
        L.append("")
        L.append("Win rate when the card was drawn at least once minus when it never was. "
                 "Correlation, not causation: cards drawn late only show up in long games. "
                 "✱ = difference larger than its 95% noise band.")
        L.append("")
        L.append("| Card | Δ win rate | Drawn | Not drawn |")
        L.append("|---|---|---|---|")
        for r in rows:
            L.append(f"| {name(r['code'])} ({r['code']}) | {100 * r['delta']:+.1f}"
                     f"{' ✱' if r['significant'] else ''} | {_pct(r['drawn_wr'])} "
                     f"(n={r['n_drawn']}) | {_pct(r['not_drawn_wr'])} (n={r['n_not']}) |")
    logs = sorted((run_dir / "logs").glob("*.log")) if (run_dir / "logs").exists() else []
    if logs:
        L.append("")
        L.append("## Game logs")
        L.append("")
        for p in logs:
            L.append(f"- `{p.relative_to(run_dir)}`")
    L.append("")
    L.append(f"Replay any game: `{s['replay']}`")
    out = run_dir / "report.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    return out
