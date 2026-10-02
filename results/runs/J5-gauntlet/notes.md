# J5-gauntlet
Status: RUNNING
HEAD: 179bbe6b292a04e8beec1f75f5d4926edc94052d
Start UTC: 2026-10-01T22:48:40.247522+00:00
Command: `python3 -m sim gauntlet --deck results/runs/J5-optimize/best.txt --games 20000 --seed 52 --out results/runs/J5-gauntlet`
End UTC: 2026-10-02T00:03:48.684502+00:00
Exit: 0

## Stdout tail
```text
best: 68.2% vs field (67.6-68.9, 20001 games, bot heuristic2)
Worst: lamball-cattiva-bg 52% (4% of field); chillet-relaxaurus-br 55% (14% of field); cattiva-azurobe-br 57% (5% of field)
Losses: behind on board by round 4-6 38%; ran out of cards 38%; opponent lucky saves 3+ 33%
seed 52, commit 179bbe6, 75 min

wrote results/runs/J5-gauntlet/summary.json, telegram.txt, games.jsonl
```

Status: DONE. Verified seed 52, bot, provenance, per-opponent counts, 20001 game rows, summary and telegram length. Optimizer pushed at 179bbe6b292a04e8beec1f75f5d4926edc94052d. Raw games: /home/gator/palworld-run-artifacts/J5/J5-gauntlet-games.jsonl.
