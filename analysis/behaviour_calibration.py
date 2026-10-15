"""Behaviour profile of one archetype: real top-50 replays vs a logged sim run, per turn.

Usage: python3 -m analysis.behaviour_calibration <archetype-slug> <sim run dir with logs/> [P1|P2]

The sim run is a `sim run --logs N` output; by default the archetype is the P1 (--deck) side.
Rates are per turn of that player, so game length doesn't confound them. The real side is
every top-50 game where a player's inferred archetype matches the slug (dataset README).
"""
import collections
import glob
import gzip
import json
import re
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "replays" / "palify_ranked_2026-10-13"
STRUCTS = ("Stone Pit", "Primitive Furnace", "Mounted Machine Gun", "Medieval Medicine Workbench",
           "Ranch", "Feed Box", "Cola Vending Machine", "Lamp", "Shoddy Bed", "Berry Plantation",
           "Hot Spring", "Antique Dresser", "Wooden Wall")
KEYS = ["turns/game", "face attacks", "Pal attacks", "structure attacks", "Pals deployed",
        "structures built", "gear played", "events cast", "soul draws", "Interrupts",
        "engine activations", "damage dealt", "damage taken"]


def real_profile(slug: str) -> dict:
    rows = [json.loads(l) for l in open(DATA / "games.jsonl")]
    tot = collections.Counter()
    games = 0
    for r in rows:
        if r["winner"].get("side") not in ("p1", "p2"):
            continue
        for s, o in (("p1", "p2"), ("p2", "p1")):
            if r["players"][s]["deck"]["archetype"]["archetype"] != slug:
                continue
            me, opp = r["players"][s]["name"], r["players"][o]["name"]
            games += 1
            d = json.loads(gzip.open(DATA / r["replay_source"]["cache_body"]).read())
            seen = set()
            for fr in d["frames"]:
                for e in fr["view"].get("feed") or []:
                    if e["id"] in seen:
                        continue
                    seen.add(e["id"])
                    t, k = e["text"], e.get("kind")
                    if k == "turn" and f"{me}'s turn" in t:
                        tot["turns/game"] += 1
                    if not t.startswith(me) and k not in ("attack", "damage"):
                        continue
                    if k == "attack" and not t.startswith(opp):
                        if re.search(rf"attacks {re.escape(opp)} for \d+", t):
                            tot["face attacks"] += 1
                        elif any(t.endswith(f"attacks {x}.") for x in STRUCTS):
                            tot["structure attacks"] += 1
                        elif " attacks " in t:
                            tot["Pal attacks"] += 1
                    if t.startswith(me + " deployed"):
                        tot["Pals deployed"] += 1
                    if t.startswith(me + " built"):
                        tot["structures built"] += 1
                    if t.startswith(me + " equipped"):
                        tot["gear played"] += 1
                    if t.startswith(me + " casts"):
                        tot["events cast"] += 1
                    if t.startswith(me + " rests 3 souls"):
                        tot["soul draws"] += 1
                    if t.startswith(me) and "pay for the Interrupt" in t:
                        tot["Interrupts"] += 1
                    if t.startswith(me + " activates") and any(x in t for x in STRUCTS):
                        tot["engine activations"] += 1
                    m = re.match(rf"{re.escape(opp)} takes (\d+)", t)
                    if m:
                        tot["damage dealt"] += int(m.group(1))
                    m = re.match(rf"{re.escape(me)} takes (\d+)", t)
                    if m:
                        tot["damage taken"] += int(m.group(1))
    return tot, games


def sim_profile(run_dir: Path, side: str = "P1") -> dict:
    other = "P2" if side == "P1" else "P1"
    tot = collections.Counter()
    files = glob.glob(str(run_dir / "logs" / "*.log"))
    for f in files:
        txt = open(f, encoding="utf-8").read()
        tot["turns/game"] += len(re.findall(rf"=== Turn \d+: {side}\b", txt))
        for line in txt.splitlines():
            m = re.match(rf"{side}: .* attacks (.+)$", line)
            if m:
                tgt = m.group(1)
                if tgt == other:
                    tot["face attacks"] += 1
                elif any(tgt.startswith(x) for x in STRUCTS):
                    tot["structure attacks"] += 1
                else:
                    tot["Pal attacks"] += 1
            m = re.match(rf"{side} plays (.+?) \[([A-Z0-9]+-\d+)\]", line)
            if m:
                name = m.group(1)
                if any(name.startswith(x) for x in STRUCTS):
                    tot["structures built"] += 1
                elif any(w in name for w in ("Shotgun", "Rifle", "Handgun", "Launcher", "Gun",
                                              "Harness", "Pickaxe", "Saddle")):
                    tot["gear played"] += 1
                elif "Strategy" in name or "Breath" in name or "Guide" in name or "Sphere" in name:
                    tot["events cast"] += 1
                else:
                    tot["Pals deployed"] += 1
            if line.startswith(f"{side} rests 3 souls"):
                tot["soul draws"] += 1
            if line.startswith(f"{side} uses Interrupt"):
                tot["Interrupts"] += 1
            if line.startswith(f"{side} activates") and any(x in line for x in STRUCTS):
                tot["engine activations"] += 1
        lives = re.findall(rf"{other}: life (\d+)", txt) if other == "P2" else None
        l1 = re.findall(r"P1: life (\d+)", txt)
        l2 = re.findall(r"P2: life (\d+)", txt)
        mine, theirs = (l1, l2) if side == "P1" else (l2, l1)
        if theirs:
            tot["damage dealt"] += 10 - int(theirs[-1])
        if mine:
            tot["damage taken"] += 10 - int(mine[-1])
    return tot, len(files)


def main(slug: str, run_dir: str, side: str = "P1"):
    real, rg = real_profile(slug)
    sim, sg = sim_profile(Path(run_dir), side)
    rt, stt = max(real["turns/game"], 1), max(sim["turns/game"], 1)
    print(f"{slug}: real {rg} games ({real['turns/game'] / max(rg, 1):.1f} turns), "
          f"sim {sg} games ({sim['turns/game'] / max(sg, 1):.1f} turns). Per turn of that player:")
    print(f"  {'metric':22s} {'real':>7s} {'sim':>7s} {'sim/real':>9s}")
    for k in KEYS[1:]:
        a, b = real[k] / rt, sim[k] / stt
        ratio = f"{b / a:.2f}" if a else "n/a"
        print(f"  {k:22s} {a:7.2f} {b:7.2f} {ratio:>9s}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "P1")
