"""M4: one command for an overnight run, with a short summary for Telegram.

    python -m sim gauntlet --deck data/decks/cattiva-azurobe-br.txt --games 20000 --seed 1

Plays the deck against the play-rate-weighted field (sim/gauntlet.py) and
writes to --out (default results/gauntlet/<timestamp>_<deck>/):
- summary.json  the full numbers (per opponent, loss reasons, provenance)
- telegram.txt  a message under ~900 characters Hermes can forward as is
- games.jsonl   one line per game, same format as `sim run`
"""
from __future__ import annotations

import json
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from .gauntlet import field_weights, play_gauntlet
from .runner import git_commit, wilson

MAX_TELEGRAM = 900


def run_gauntlet(deck: str, games: int, seed: int, bot: str, out: Path | None = None,
                 workers: int | None = None, deck_bot: str | None = None) -> dict:
    from analysis.tags import loss_tags
    from cards.db import load_card_db
    db = load_card_db()
    name = Path(deck).stem
    out = out or Path("results") / "gauntlet" / (
        datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + f"_{name}")
    out.mkdir(parents=True, exist_ok=True)
    weights = field_weights()
    t0 = time.time()
    res = play_gauntlet(deck, weights, games, seed, bot, workers=workers, keep_records=True,
                        deck_bot=deck_bot)
    elapsed = time.time() - t0

    per_opp = {}
    tags: Counter = Counter()
    losses = 0
    with open(out / "games.jsonl", "w", encoding="utf-8") as f:
        for opp, r in res.per_opp.items():
            lo, hi = wilson(round(r.wins), r.games)
            first = [g for g in r.records if g["first"] == "deck"]
            per_opp[opp] = {"weight": round(weights[opp], 4), "games": r.games,
                            "win_rate": round(r.rate, 4), "ci95": [round(lo, 4), round(hi, 4)],
                            "going_first": round(sum(g["winner"] == "deck" for g in first)
                                                 / max(len(first), 1), 4)}
            for g in r.records:
                g["opp_deck"] = opp
                f.write(json.dumps(g, separators=(",", ":")) + "\n")
                if g["winner"] == "opp":
                    losses += 1
                    tags.update(set(loss_tags(g, db)))
    wr, se = res.win_rate, res.se
    summary = {
        "deck": name, "games": sum(r.games for r in res.per_opp.values()), "bot": bot,
        "deck_bot": deck_bot,
        "seed": seed, "commit": git_commit(), "seconds": round(elapsed),
        "weighted_win_rate": round(wr, 4), "ci95": [round(wr - 1.96 * se, 4),
                                                    round(wr + 1.96 * se, 4)],
        "field": per_opp,
        "loss_reasons": {t: round(k / max(losses, 1), 3) for t, k in tags.most_common(8)},
        "replay": (f"python -m sim replay --deck {deck} --opp data/decks/<opp>.txt "
                   f"--bot {bot} --game-seed <seed from games.jsonl>"),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (out / "telegram.txt").write_text(telegram(summary, db), encoding="utf-8")
    return {"out": str(out), **summary}


def _tag_text(tag: str, db) -> str:
    if tag.startswith("lost_to:"):
        code = tag.split(":", 1)[1]
        return f"lost to {db[code].name.split(' –')[0]}" if code in db else tag
    return tag.replace("_", " ")


def telegram(s: dict, db) -> str:
    """Short plain-text report: headline, weakest matchups, top loss reasons."""
    lo, hi = s["ci95"]
    lines = [f"{s['deck']}: {100 * s['weighted_win_rate']:.1f}% vs field "
             f"({100 * lo:.1f}-{100 * hi:.1f}, {s['games']} games, bot {s['bot']}"
             + (f", deck bot {s['deck_bot']}" if s.get("deck_bot") else "") + ")"]
    worst = sorted(s["field"].items(), key=lambda kv: kv[1]["win_rate"])[:3]
    lines.append("Worst: " + "; ".join(
        f"{opp} {100 * r['win_rate']:.0f}% ({100 * r['weight']:.0f}% of field)"
        for opp, r in worst))
    reasons = list(s["loss_reasons"].items())[:3]
    lines.append("Losses: " + "; ".join(f"{_tag_text(t, db)} {100 * v:.0f}%" for t, v in reasons))
    lines.append(f"seed {s['seed']}, commit {s['commit']}, {s['seconds'] // 60} min")
    text = "\n".join(lines)
    return text[:MAX_TELEGRAM]


def compare_lists(a: str, b: str, games: int, seed: int, bot: str,
                  workers: int | None = None) -> str:
    """Two versions of a deck against the same weighted field on the same seeds;
    returns a per-opponent table (markdown)."""
    weights = field_weights()
    ra = play_gauntlet(a, weights, games, seed, bot, workers=workers)
    rb = play_gauntlet(b, weights, games, seed, bot, workers=workers)
    se = (ra.se ** 2 + rb.se ** 2) ** 0.5
    diff = rb.win_rate - ra.win_rate
    lines = [f"**{bot}**, {games} games per list, seed {seed}: A {100 * ra.win_rate:.1f}% -> "
             f"B {100 * rb.win_rate:.1f}% (diff {100 * diff:+.1f} ± {100 * se:.1f}, "
             f"z {diff / se if se else 0:.1f})", "",
             "| Opponent | Weight | A | B | Diff | Games |", "|---|---|---|---|---|---|"]
    for d, w in weights.items():
        x, y = ra.per_opp[d], rb.per_opp[d]
        lines.append(f"| {d} | {100 * w:.1f}% | {100 * x.rate:.1f} | {100 * y.rate:.1f} | "
                     f"{100 * (y.rate - x.rate):+.1f} | {x.games} |")
    return "\n".join(lines) + "\n"
