"""Matchup matrix: every pair of decks, compared with real-world data.

    python -m sim matrix --decks data/decks/a.txt data/decks/b.txt ... --games 2000 --seed 1

Each unordered pair is one `run` (deck i as "deck", j as "opp", i < j) in its
own subdirectory. The reverse direction is 1 - p. Mirror matches are skipped.
Writes matrix.json and matrix.md, including calibration against the latest
data/calibration/matchups_*.json.
"""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

from .runner import MatchSpec, run

PASS_BAND = 0.05


def _calibration() -> tuple[dict, str | None]:
    from analysis.report import CALIBRATION_DIR
    files = sorted(CALIBRATION_DIR.glob("matchups_*.json"))
    if not files:
        return {}, None
    rows = json.loads(files[-1].read_text(encoding="utf-8"))
    return {(r["deck_a"], r["deck_b"]): r for r in rows}, files[-1].name


def run_matrix(decks: list[str], games: int, seed: int, out: Path, bot: str = "heuristic",
               structures: str = "any", workers: int | None = None) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    names = [Path(d).stem for d in decks]
    real, cal_file = _calibration()
    pairs = []
    for k, (i, j) in enumerate(combinations(range(len(decks)), 2)):
        spec = MatchSpec(decks[i], decks[j], bot, structures)
        print(f"[{k + 1}/{len(decks) * (len(decks) - 1) // 2}] {names[i]} vs {names[j]}",
              flush=True)
        s = run(spec, games, seed + k, out / f"{names[i]}__vs__{names[j]}", workers,
                logs=1, progress=False)
        r = real.get((names[i], names[j]))
        pairs.append({
            "deck": names[i], "opp": names[j], "sim": s["win_rate"], "ci95": s["ci95"],
            "games": s["games"], "first": s["going_first"]["win_rate"],
            "second": s["going_second"]["win_rate"],
            "real": r["win_rate_a"] if r else None, "real_games": r.get("games") if r else None,
        })
    for p in pairs:
        p["diff"] = None if p["real"] is None else round(p["sim"] - p["real"], 4)
        p["pass"] = None if p["real"] is None else abs(p["diff"]) <= PASS_BAND
        p["z"] = noise_z(p)
        p["consistent"] = None if p["z"] is None else abs(p["z"]) <= 2.0
    checked = [p for p in pairs if p["real"] is not None]
    zs = [p for p in checked if p["z"] is not None]
    result = {
        "consistent_pairs": sum(p["consistent"] for p in zs), "z_checked_pairs": len(zs),
        "decks": names, "games_per_pair": games, "seed": seed, "bot": bot,
        "rules": {"structures_attackable": structures}, "calibration_file": cal_file,
        "pairs": pairs,
        "calibrated_pairs": len(checked),
        "passing_pairs": sum(p["pass"] for p in checked),
        "mean_abs_diff": round(sum(abs(p["diff"]) for p in checked) / len(checked), 4)
        if checked else None,
    }
    (out / "matrix.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    (out / "matrix.md").write_text(render(result), encoding="utf-8")
    return result


def noise_z(p: dict) -> float | None:
    """Sim minus real, in units of the combined sampling error of both win rates.
    Needs the real game count; |z| <= 2 means the miss could be noise."""
    import math
    if p["real"] is None or not p.get("real_games"):
        return None
    r, s = p["real"], p["sim"]
    se = math.sqrt(r * (1 - r) / p["real_games"] + s * (1 - s) / max(p["games"], 1))
    return round((s - r) / se, 2) if se else None


def win_rate(result: dict, a: str, b: str) -> float | None:
    for p in result["pairs"]:
        if (p["deck"], p["opp"]) == (a, b):
            return p["sim"]
        if (p["deck"], p["opp"]) == (b, a):
            return 1 - p["sim"]
    return None


def render(result: dict) -> str:
    names = result["decks"]
    L = [f"# Matchup matrix ({result['games_per_pair']} games per pair, bot "
         f"`{result['bot']}`, structures `{result['rules']['structures_attackable']}`)", ""]
    L.append("Row deck's win rate against the column deck.")
    L.append("")
    L.append("| | " + " | ".join(names) + " |")
    L.append("|---|" + "---|" * len(names))
    for a in names:
        cells = []
        for b in names:
            w = win_rate(result, a, b)
            cells.append("—" if w is None else f"{100 * w:.0f}")
        L.append(f"| **{a}** | " + " | ".join(cells) + " |")
    L.append("")
    if result["calibrated_pairs"]:
        L.append(f"## Calibration vs {result['calibration_file']}")
        L.append("")
        L.append(f"{result['passing_pairs']}/{result['calibrated_pairs']} pairs within ±5 points; "
                 f"mean absolute difference {100 * result['mean_abs_diff']:.1f} points.")
        if result.get("z_checked_pairs"):
            L.append(f"{result['consistent_pairs']}/{result['z_checked_pairs']} pairs consistent "
                     "with the real data allowing for both sample sizes (|z| ≤ 2).")
        L.append("")
        L.append("| Matchup | Sim | 95% CI | Real (games) | Diff | z | |")
        L.append("|---|---|---|---|---|---|---|")
        for p in sorted(result["pairs"], key=lambda p: -abs(p["diff"] or 0)):
            if p["real"] is None:
                continue
            z = "—" if p.get("z") is None else f"{p['z']:+.1f}"
            L.append(f"| {p['deck']} vs {p['opp']} | {100 * p['sim']:.1f} | "
                     f"{100 * p['ci95'][0]:.1f}–{100 * p['ci95'][1]:.1f} | {100 * p['real']:.1f} "
                     f"({p.get('real_games') or '?'}) | {100 * p['diff']:+.1f} | {z} | "
                     f"{'✅' if p['pass'] else '❌'} |")
    missing = [p for p in result["pairs"] if p["real"] is None]
    if missing:
        L.append("")
        L.append("No real-world data for: " + ", ".join(f"{p['deck']} vs {p['opp']}"
                                                    for p in missing))
    return "\n".join(L) + "\n"
