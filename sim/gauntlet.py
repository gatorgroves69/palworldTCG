"""Weighted gauntlet: how does a deck do against the field?

Weights are real-world play rates from the latest
data/calibration/tiers_*.json, restricted to the decks we have lists for
and normalised to sum to 1. The deck's own archetype stays in the field
(it's a mirror match). Games are split across opponents in proportion to
their weight, and the headline number is the weighted win rate.

Game seeds depend only on (seed, opponent, game index), so two versions of a
deck played on the same seed range face the same opponent shuffles: a paired
comparison.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from multiprocessing import Pool
from pathlib import Path

from .runner import MatchSpec, play_one

ROOT = Path(__file__).resolve().parent.parent
DECK_DIR = ROOT / "data" / "decks"
CAL_DIR = ROOT / "data" / "calibration"


def field_weights(exclude_missing: bool = True) -> dict[str, float]:
    """Deck slug -> normalised play-rate weight."""
    files = sorted(CAL_DIR.glob("tiers_*.json"))
    if not files:
        raise FileNotFoundError("no data/calibration/tiers_*.json")
    rows = json.loads(files[-1].read_text(encoding="utf-8"))
    w = {r["deck"]: float(r["play_rate"]) for r in rows if r.get("play_rate")}
    if exclude_missing:
        w = {d: v for d, v in w.items() if (DECK_DIR / f"{d}.txt").exists()}
    total = sum(w.values())
    return {d: v / total for d, v in sorted(w.items(), key=lambda kv: -kv[1])}


def allocate(weights: dict[str, float], games: int, minimum: int = 20) -> dict[str, int]:
    """Games per opponent, proportional to weight, at least `minimum` each."""
    return {d: max(minimum, round(games * w)) for d, w in weights.items()}


def gauntlet_seed(seed: int, opp_index: int, i: int) -> int:
    return seed * 10_000_000 + opp_index * 100_000 + i


@dataclass
class OppResult:
    games: int = 0
    wins: float = 0.0
    records: list = field(default_factory=list)

    @property
    def rate(self) -> float:
        return self.wins / self.games if self.games else 0.0


@dataclass
class GauntletResult:
    weights: dict[str, float]
    per_opp: dict[str, OppResult]

    @property
    def win_rate(self) -> float:
        return sum(w * self.per_opp[d].rate for d, w in self.weights.items())

    @property
    def se(self) -> float:
        v = 0.0
        for d, w in self.weights.items():
            r = self.per_opp[d]
            p = min(max(r.rate, 1e-3), 1 - 1e-3)
            v += w * w * p * (1 - p) / max(r.games, 1)
        return math.sqrt(v)

    def merge(self, other: "GauntletResult") -> None:
        for d, r in other.per_opp.items():
            mine = self.per_opp.setdefault(d, OppResult())
            mine.games += r.games
            mine.wins += r.wins
            mine.records += r.records


_POOLS: dict = {}


def get_pool(workers: int | None = None):
    """One reusable worker pool per process: starting workers costs seconds on macOS,
    and the optimizer plays hundreds of small batches."""
    if workers not in _POOLS:
        import atexit
        pool = Pool(workers)
        _POOLS[workers] = pool
        atexit.register(pool.terminate)
    return _POOLS[workers]


def _job(args):
    spec, seed = args
    return spec.opp, play_one((spec, seed, False))


def play_gauntlet(deck_path: str, weights: dict[str, float], games: int, seed: int,
                  bot: str = "heuristic2", start: int = 0, workers: int | None = None,
                  keep_records: bool = False, mulligan: str = "default") -> GauntletResult:
    """Play `games` games spread over the field; game indices start at `start`
    (so batch k of a sequential test uses fresh, but reproducible, seeds)."""
    alloc = allocate(weights, games)
    jobs = []
    for oi, opp in enumerate(weights):
        spec = MatchSpec(deck_path, str(DECK_DIR / f"{opp}.txt"), bot, mulligan=mulligan)
        n = alloc[opp]
        first = round(start * alloc[opp] / max(games, 1))
        jobs += [(spec, gauntlet_seed(seed, oi, first + i)) for i in range(n)]
    res = GauntletResult(weights, {d: OppResult() for d in weights})
    pool = get_pool(workers)
    for opp_path, rec in pool.imap_unordered(_job, jobs, chunksize=8):
        opp = Path(opp_path).stem
        r = res.per_opp[opp]
        r.games += 1
        r.wins += 1.0 if rec["winner"] == "deck" else 0.5 if rec["winner"] == "draw" else 0.0
        if keep_records:
            r.records.append(rec)
    return res
