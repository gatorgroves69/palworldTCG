"""M3: propose card swaps, test them against the weighted gauntlet, keep winners.

    python -m sim optimize --deck data/decks/cattiva-azurobe-br.txt --rounds 3

Each round:
1. Play the current deck ("incumbent") against the field and collect per-card
   statistics: draw impact and how often a card is still in hand at the end.
2. Propose swaps: remove 2 copies of a weak card, add 2 copies of an
   implemented card in the deck's colours. Every variant must be a legal deck.
3. Test each swap with a group-sequential paired test: batches of games on the
   same seeds as the incumbent, stopping early when the gain is clearly real
   (O'Brien-Fleming-style boundaries) or clearly absent (futility).
4. A swap that passes under the primary bot must also show a gain under the
   confirmation bot (a different bot, so the gain isn't one bot's quirk).
5. The first swap that passes becomes the new incumbent; the next round starts.

Every tried swap is logged to results/experiments.md (and .jsonl). Variant
decklists go to results/opt/<run>/. data/ is never written.
"""
from __future__ import annotations

import json
import math
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .gauntlet import GauntletResult, field_weights, play_gauntlet

RESULTS = Path(__file__).resolve().parent.parent / "results"


@dataclass
class TestConfig:
    batch: int = 800          # games per batch, per deck version
    max_batches: int = 5
    boundary: float = 2.4     # final z; look k uses boundary * sqrt(K / k)
    confirm_games: int = 3000
    confirm_z: float = 1.0    # the confirmation bot must also see a gain this clear
    copies: int = 2           # copies moved per swap
    screen_games: int = 0     # >0: screen every sensible swap with this many games first
    screen_bot: str = "heuristic"
    screen_outs: int = 4      # weakest cards considered for removal when screening


# ---------------------------------------------------------------- decklists
def read_list(path: Path) -> tuple[Counter, Counter]:
    from cards.decklist import parse_decklist
    main, soul = Counter(), Counter()
    for e in parse_decklist(path.read_text(encoding="utf-8"), str(path)):
        (main if e.section == "main" else soul)[e.code] += e.count
    return main, soul


def write_list(path: Path, main: Counter, soul: Counter, db) -> None:
    lines = ["# main"] + [f"{n} {c} {db[c].name}" for c, n in sorted(main.items()) if n > 0]
    lines += ["# soul"] + [f"{n} {c} {db[c].name}" for c, n in sorted(soul.items()) if n > 0]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def is_legal(main: Counter, soul: Counter, db) -> bool:
    from engine.deck import Deck, deck_problems
    d = Deck("variant", [db[c] for c, n in main.items() for _ in range(n)],
             [db[c] for c, n in soul.items() for _ in range(n)])
    return not deck_problems(d)


# ---------------------------------------------------------------- statistics
def card_stats(res: GauntletResult) -> dict[str, dict]:
    """Per card in our deck: win rate when drawn vs not, and how often it's stuck in hand."""
    drawn_w, drawn_n, not_w, not_n = Counter(), Counter(), Counter(), Counter()
    stuck, drawn_copies = Counter(), Counter()
    codes = set()
    for r in res.per_opp.values():
        for g in r.records:
            codes.update(g["drawn"][0])
    for r in res.per_opp.values():
        for g in r.records:
            won = 1.0 if g["winner"] == "deck" else 0.5 if g["winner"] == "draw" else 0.0
            seen = set(g["drawn"][0])
            for c in codes:
                if c in seen:
                    drawn_w[c] += won
                    drawn_n[c] += 1
                else:
                    not_w[c] += won
                    not_n[c] += 1
            drawn_copies.update(g["drawn"][0])
            stuck.update(g.get("hand_end", [[], []])[0])
    out = {}
    for c in codes:
        wr_d = drawn_w[c] / drawn_n[c] if drawn_n[c] else 0.0
        wr_n = not_w[c] / not_n[c] if not_n[c] else wr_d
        out[c] = {"impact": wr_d - wr_n, "stuck": stuck[c] / max(drawn_copies[c], 1),
                  "drawn": drawn_n[c]}
    return out


def prior_impacts(matrix_dir: Path) -> dict[str, float]:
    """Average draw impact of each card across the M2 matrix games (for 'in' candidates)."""
    tot, cnt = defaultdict(float), Counter()
    for gfile in matrix_dir.glob("*__vs__*/games.jsonl"):
        games = [json.loads(line) for line in gfile.open(encoding="utf-8")]
        for side, won_tag in ((0, "deck"), (1, "opp")):
            codes = {c for g in games for c in g["drawn"][side]}
            for c in codes:
                yes = [g["winner"] == won_tag for g in games if c in g["drawn"][side]]
                no = [g["winner"] == won_tag for g in games if c not in g["drawn"][side]]
                if len(yes) >= 30 and len(no) >= 30:
                    tot[c] += sum(yes) / len(yes) - sum(no) / len(no)
                    cnt[c] += 1
    return {c: tot[c] / cnt[c] for c in cnt}


# ---------------------------------------------------------------- proposals
def propose(main: Counter, soul: Counter, stats: dict, prior: dict, db, registry,
            copies: int, n_out: int = 3, n_in: int = 4) -> list[tuple[str, str]]:
    from engine.model import Color
    colors = {db[c].color for c in main} - {Color.COLORLESS}
    names = Counter()
    for c, n in main.items():
        names[db[c].name] += n
    outs = sorted((c for c in main if main[c] >= copies and c in stats),
                  key=lambda c: stats[c]["impact"] - 0.05 * stats[c]["stuck"])[:n_out]
    ins = []
    for c in registry.codes():
        d = db.get(c)
        if d is None or d.type.value == "soul" or c in main:
            continue
        if d.color is not Color.COLORLESS and d.color not in colors:
            continue
        if names[d.name] + copies > 4:
            continue
        ins.append(c)
    ins.sort(key=lambda c: -prior.get(c, -1.0))
    ins = ins[:n_in]
    swaps = []
    for o in outs:
        for i in ins:
            m = Counter(main)
            m[o] -= copies
            m[i] += copies
            if is_legal(+m, soul, db):
                swaps.append((o, i))
    swaps.sort(key=lambda s: -(prior.get(s[1], 0.0) - stats[s[0]]["impact"]))
    return swaps


def all_swaps(main: Counter, soul: Counter, stats: dict, db, registry, copies: int,
              n_out: int) -> list[tuple[str, str]]:
    """Every legal swap of `copies` copies: one of the `n_out` weakest cards out, any
    implemented card in the deck's colours in (including more copies of a card already
    in the list), for the screening pass."""
    from engine.model import Color
    colors = {db[c].color for c in main} - {Color.COLORLESS}
    names = Counter()
    for c, n in main.items():
        names[db[c].name] += n
    outs = sorted((c for c in main if main[c] >= copies and c in stats),
                  key=lambda c: stats[c]["impact"] - 0.05 * stats[c]["stuck"])[:n_out]
    swaps = []
    for i in registry.codes():
        d = db.get(i)
        if d is None or d.type.value == "soul":
            continue
        if d.color is not Color.COLORLESS and d.color not in colors:
            continue
        for o in outs:
            if o == i or db[o].name == d.name:
                continue
            m = Counter(main)
            m[o] -= copies
            m[i] += copies
            if is_legal(+m, soul, db):
                swaps.append((o, i))
    return swaps


def screen(inc_path: Path, swaps, main, soul, db, weights, seed: int, cfg: TestConfig,
           out: Path, rnd: int) -> list[tuple[float, str, str]]:
    """Quick paired estimate of every swap; returns (diff, out, in) sorted best first."""
    base = play_gauntlet(str(inc_path), weights, cfg.screen_games, seed, cfg.screen_bot)
    scored = []
    for o, i in swaps:
        m = Counter(main)
        m[o] -= cfg.copies
        m[i] += cfg.copies
        path = out / "screen" / f"round{rnd}_{o}_to_{i}.txt"
        write_list(path, +m, soul, db)
        r = play_gauntlet(str(path), weights, cfg.screen_games, seed, cfg.screen_bot)
        scored.append((r.win_rate - base.win_rate, o, i))
    scored.sort(reverse=True)
    lines = [f"# Round {rnd} screening: {len(scored)} swaps, {cfg.screen_games} games each, "
             f"bot {cfg.screen_bot}, seed {seed}", "",
             f"Incumbent {100 * base.win_rate:.1f}%. Diff is noisy (about ±4 points); only the "
             "top candidates go on to the full sequential test.", "",
             "| Rank | Swap | Diff |", "|---|---|---|"]
    for k, (d, o, i) in enumerate(scored, 1):
        lines.append(f"| {k} | -{cfg.copies} {db[o].name} / +{cfg.copies} {db[i].name} | "
                     f"{100 * d:+.1f} |")
    (out / f"screen_round{rnd}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return scored


# ---------------------------------------------------------------- sequential test
def sequential_test(inc_path: Path, var_path: Path, weights, seed: int, bot: str,
                    cfg: TestConfig, cache: dict) -> dict:
    """Group-sequential paired comparison. `cache` holds the incumbent's batches."""
    inc_total = GauntletResult(weights, {})
    var_total = GauntletResult(weights, {})
    K = cfg.max_batches
    for k in range(1, K + 1):
        key = (str(inc_path), bot, seed, k)
        if key not in cache:
            cache[key] = play_gauntlet(str(inc_path), weights, cfg.batch, seed, bot,
                                       start=(k - 1) * cfg.batch)
        inc_total.merge(cache[key])
        var_total.merge(play_gauntlet(str(var_path), weights, cfg.batch, seed, bot,
                                      start=(k - 1) * cfg.batch))
        diff = var_total.win_rate - inc_total.win_rate
        se = math.sqrt(var_total.se ** 2 + inc_total.se ** 2)
        z = diff / se if se else 0.0
        bound = cfg.boundary * math.sqrt(K / k)
        games = sum(r.games for r in var_total.per_opp.values())
        if z >= bound:
            return {"decision": "better", "diff": diff, "se": se, "z": z, "games": games,
                    "looks": k}
        if k >= 2 and z < 0:
            return {"decision": "not better (futility)", "diff": diff, "se": se, "z": z,
                    "games": games, "looks": k}
    return {"decision": "not better (inconclusive)", "diff": diff, "se": se, "z": z,
            "games": games, "looks": K}


def confirm(inc_path: Path, var_path: Path, weights, seed: int, bot: str,
            cfg: TestConfig) -> dict:
    inc = play_gauntlet(str(inc_path), weights, cfg.confirm_games, seed + 7, bot)
    var = play_gauntlet(str(var_path), weights, cfg.confirm_games, seed + 7, bot)
    diff = var.win_rate - inc.win_rate
    se = math.sqrt(var.se ** 2 + inc.se ** 2)
    z = diff / se if se else 0.0
    return {"bot": bot, "diff": diff, "se": se, "z": z, "passed": z >= cfg.confirm_z}


# ---------------------------------------------------------------- logging
def log_experiment(row: dict, results: Path = RESULTS) -> None:
    md, jsonl = results / "experiments.md", results / "experiments.jsonl"
    results.mkdir(parents=True, exist_ok=True)
    if not md.exists():
        md.write_text(
            "# Deck experiments\n\nEvery swap the optimizer tried, newest last. Δ = weighted "
            "gauntlet win rate (variant − incumbent), paired on the same seeds.\n\n"
            "| When (UTC) | Run | Deck | Swap | Primary bot | Δ ± SE | z | Games | "
            "Confirm bot | Result |\n|---|---|---|---|---|---|---|---|---|---|\n",
            encoding="utf-8")
    c = row.get("confirm")
    conf = (f"{row['confirm_bot']} {100 * c['diff']:+.1f} (z {c['z']:.1f})" if c else "—")
    with md.open("a", encoding="utf-8") as f:
        f.write(f"| {row['when']} | {row['run']} | {row['deck']} | {row['swap']} | "
                f"{row['bot']} | {100 * row['diff']:+.1f} ± {100 * row['se']:.1f} | "
                f"{row['z']:.2f} | {row['games']} | {conf} | **{row['result']}** |\n")
    with jsonl.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")


# ---------------------------------------------------------------- main loop
def optimize(deck: str, rounds: int = 1, seed: int = 1, bot: str = "heuristic2",
             confirm_bot: str = "heuristic", max_tries: int = 6,
             cfg: TestConfig | None = None, baseline_games: int = 3000,
             matrix_dir: str | None = None, results: Path = RESULTS) -> Path:
    import cards
    from cards.db import load_card_db
    cfg = cfg or TestConfig()
    db = load_card_db()
    weights = field_weights()
    run = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out = results / "opt" / run
    out.mkdir(parents=True, exist_ok=True)
    main, soul = read_list(Path(deck))
    inc_path = out / "round0.txt"
    write_list(inc_path, main, soul, db)
    prior = prior_impacts(Path(matrix_dir) if matrix_dir else results / "m2-matrix-heuristic2")
    cache: dict = {}
    name = Path(deck).stem
    print(f"optimizing {name}; field weights: "
          + ", ".join(f"{d} {100 * w:.1f}%" for d, w in weights.items()))
    for rnd in range(1, rounds + 1):
        t0 = time.time()
        base = play_gauntlet(str(inc_path), weights, baseline_games, seed + 1000 + rnd, bot,
                             keep_records=True)
        stats = card_stats(base)
        print(f"round {rnd}: incumbent {100 * base.win_rate:.1f}% ± {100 * base.se:.1f} "
              f"({time.time() - t0:.0f}s)")
        if cfg.screen_games > 0:
            cands = all_swaps(main, soul, stats, db, cards.REGISTRY, cfg.copies, cfg.screen_outs)
            print(f"  screening {len(cands)} swaps x {cfg.screen_games} games", flush=True)
            ranked = screen(inc_path, cands, main, soul, db, weights, seed + 500 + rnd, cfg,
                            out, rnd)
            swaps = [(o, i) for d, o, i in ranked if d > 0][:max_tries]
        else:
            swaps = propose(main, soul, stats, prior, db, cards.REGISTRY, cfg.copies)[:max_tries]
        accepted = None
        for o, i in swaps:
            m = Counter(main)
            m[o] -= cfg.copies
            m[i] += cfg.copies
            var_path = out / f"round{rnd}_{o}_to_{i}.txt"
            write_list(var_path, +m, soul, db)
            swap = f"-{cfg.copies} {db[o].name} / +{cfg.copies} {db[i].name}"
            t = sequential_test(inc_path, var_path, weights, seed, bot, cfg, cache)
            c = None
            result = t["decision"]
            if t["decision"] == "better":
                c = confirm(inc_path, var_path, weights, seed, confirm_bot, cfg)
                result = "KEPT" if c["passed"] else "rejected (confirmation bot disagrees)"
            print(f"  {swap}: {100 * t['diff']:+.1f} ± {100 * t['se']:.1f} "
                  f"({t['games']} games) -> {result}")
            log_experiment({
                "when": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"), "run": run,
                "deck": name, "round": rnd, "swap": swap, "out": o, "in": i, "bot": bot,
                "diff": t["diff"], "se": t["se"], "z": t["z"], "games": t["games"],
                "looks": t["looks"], "confirm_bot": confirm_bot, "confirm": c,
                "result": result, "incumbent_wr": base.win_rate,
            }, results)
            if result == "KEPT":
                accepted = (m, var_path)
                break
        if accepted is None:
            print(f"round {rnd}: no swap passed; stopping")
            break
        main, inc_path = +accepted[0], accepted[1]
    best = out / "best.txt"
    write_list(best, main, soul, db)
    print(f"best list: {best}")
    return best
