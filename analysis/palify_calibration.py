"""Real-play calibration targets from Mew's Palify top-50 replay snapshot (read only).

Usage: python3 -m analysis.palify_calibration [dataset dir]

Prints: first-player win rate (overall and by the first player's archetype), archetype
records and head-to-head pairs, and play-style rates (attacks, Interrupts by defender
life, blocks, soul draws) to compare with the bots. Skips very short and timeout games.
The sample is top-50 players' public games: a skill-selected convenience sample, so deck
records mix deck strength with pilot strength (see the dataset README).
"""
import collections
import gzip
import json
import math
import re
import sys
from pathlib import Path

DEFAULT = Path(__file__).resolve().parent.parent / "data" / "replays" / "palify_ranked_2026-10-13"
SKIP = {"very_short_game", "timeout_or_disconnect"}


def load(base: Path):
    rows = [json.loads(line) for line in open(base / "games.jsonl")]
    return [r for r in rows if r["winner"].get("side") in ("p1", "p2")
            and not set(r["quality_flags"]) & SKIP]


def arch(p):
    return p["deck"]["archetype"]["archetype"]


def feed(base: Path, r):
    d = json.loads(gzip.open(base / r["replay_source"]["cache_body"]).read())
    seen, out = set(), []
    for f in d["frames"]:
        for e in f["view"].get("feed") or []:
            if e["id"] not in seen:
                seen.add(e["id"])
                out.append(e)
    return out


def pct(w, n):
    return f"{w}/{n} = {100 * w / n:.1f}%" if n else "n/a"


def main(base: Path = DEFAULT):
    games = load(base)
    print(f"{len(games)} games (top-50 public ranked, short/timeout games skipped)\n")

    fp = [r for r in games if (r.get("first_player") or {}).get("side") in ("p1", "p2")]
    w = sum(r["first_player"]["side"] == r["winner"]["side"] for r in fp)
    print(f"First player wins {pct(w, len(fp))} (95% ±{196 * math.sqrt(.25 / len(fp)):.1f})")
    by = collections.defaultdict(lambda: [0, 0])
    for r in fp:
        a = arch(r["players"][r["first_player"]["side"]])
        by[a][0] += r["first_player"]["side"] == r["winner"]["side"]
        by[a][1] += 1
    for a, (w, n) in sorted(by.items(), key=lambda x: -x[1][1]):
        if n >= 8:
            print(f"  going first with {a}: {pct(w, n)}")

    rec = collections.defaultdict(lambda: [0, 0])
    pair = collections.defaultdict(lambda: [0, 0])
    for r in games:
        for s, o in (("p1", "p2"), ("p2", "p1")):
            a, b = arch(r["players"][s]), arch(r["players"][o])
            won = r["winner"]["side"] == s
            rec[a][0] += won
            rec[a][1] += 1
            if a != b:
                pair[(a, b)][0] += won
                pair[(a, b)][1] += 1
    print("\nArchetype records (deck-games):")
    for a, (w, n) in sorted(rec.items(), key=lambda x: -x[1][1]):
        if n >= 8:
            print(f"  {a:28s} {pct(w, n)}")
    print("\nHead-to-head, n >= 8:")
    for (a, b), (w, n) in sorted(pair.items(), key=lambda x: -x[1][1]):
        if n >= 8 and a < b:
            print(f"  {a} vs {b}: {pct(w, n)}")

    st = collections.Counter()
    face = collections.defaultdict(lambda: [0, 0])
    pal = [0, 0]
    for r in games:
        f = feed(base, r)
        life = {}
        for i, e in enumerate(f):
            t, k = e["text"], e.get("kind")
            nxt = f[i + 1]["kind"] if i + 1 < len(f) else ""
            if k == "attack":
                m = re.match(r"(.+) attacks (.+) for (\d+)\.", t)
                if m:
                    st["face attacks"] += 1
                    L = life.get(m.group(2), 10)
                    b = "1-3" if L <= 3 else "4-6" if L <= 6 else "7-10"
                    face[b][1] += 1
                    face[b][0] += nxt == "interrupt"
                elif "attacks" in t:
                    st["Pal/structure attacks"] += 1
                    pal[1] += 1
                    pal[0] += nxt == "interrupt"
            mm = re.match(r"(.+) takes \d+: (\d+) life left", t)
            if mm:
                life[mm.group(1)] = int(mm.group(2))
            if "rests 3 souls to draw" in t:
                st["soul draws"] += 1
            if "blocks with" in t:
                st["blocks"] += 1
    n = len(games)
    print("\nPlay style, per game (both players):")
    for k, v in st.most_common():
        print(f"  {k:24s} {v / n:.2f}")
    print("Face attacks Interrupted, by defender life:")
    for b in ("7-10", "4-6", "1-3"):
        print(f"  {b}: {pct(*face[b])}")
    print(f"Attacks on Pals Interrupted: {pct(*pal)}")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT)
