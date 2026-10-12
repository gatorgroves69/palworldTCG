"""Turn a Palify replay (link, match id, or saved JSON) into a readable log with both hands.

Usage: python3 -m analysis.palify_log https://palify.org/play/replay/<id>  (prints to stdout)"""
import json, re, sys, urllib.request
from pathlib import Path
CARDS = Path(__file__).resolve().parent.parent / "data" / "cards.json"
def names():
    d = json.load(open(CARDS)); d = d.get("cards", d) if isinstance(d, dict) else d
    return {c["code"]: c["name"].split(" – ")[0] for c in d}
def load(arg):
    if arg.endswith(".json"): return json.load(open(arg))
    mid = re.search(r"[0-9a-f]{8}-[0-9a-f-]{27}", arg).group(0)
    url = f"https://palify.org/api/pvp/match/{mid}/replay"
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})))
def main(arg):
    d, nm = load(arg), names()
    seen, turn, out = set(), None, []
    out.append(f"{d['names']['p1']} vs {d['names']['p2']} · {d['format']}")
    for f in d["frames"]:
        v = f["view"]
        if v.get("turn") != turn:
            turn = v.get("turn")
            out.append(f"\n=== Turn {turn} · {v.get('activeIs','?')} active")
            for side, h in (f.get("hands") or {}).items():
                out.append(f"  {h['name']} hand: " + ", ".join(nm.get(c, c) for c in h["cards"]))
        for e in v.get("feed") or []:
            if e["id"] not in seen:
                seen.add(e["id"]); out.append(f"  [{e.get('kind','')}] {e['text']}")
    last = d["frames"][-1]["view"]
    hands = d["frames"][-1].get("hands") or {}
    side = {k: h["name"] for k, h in hands.items()}  # "you"/"bot" -> player name in this replay's view
    w = last.get("winner")
    w = side.get({"opp": "bot", "me": "you"}.get(w, w), w)
    out.append(f"\nResult: {w} wins ({last.get('endReason')})")
    print("\n".join(out))
if __name__ == "__main__": main(sys.argv[1])
