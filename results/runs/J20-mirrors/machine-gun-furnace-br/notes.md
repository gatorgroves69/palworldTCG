
## J20.8: DONE
HEAD: cf9271f09c9087b0be22321c56e3af91f5279388
Start UTC: 2026-10-12T08:30:40.964898+00:00
End UTC: 2026-10-12T08:57:58.149225+00:00
Command: `python3 -m sim run --deck data/decks/machine-gun-furnace-br.txt --opp data/decks/machine-gun-furnace-br.txt --games 1000 --seed 201 --bot heuristic2 --deck-bot heuristic3 --no-report --logs 0 --out results/runs/J20-mirrors/machine-gun-furnace-br`
Exit: 0; artifact gate: PASS
Evidence: /home/gator/palworld-run-artifacts/J20-J22-reordered
machine-gun-furnace-br: heuristic3 mirror win rate 52.5%

Stdout tail:
```text
  700/1000 games
  800/1000 games
  900/1000 games
  1000/1000 games
{
  "win_rate": 0.525,
  "ci95": [
    0.494,
    0.5558
  ],
  "going_first": {
    "games": 500,
    "wins": 239,
    "losses": 261,
    "draws": 0,
    "win_rate": 0.478,
    "ci95": [
      0.4346,
      0.5218
    ]
  },
  "going_second": {
    "games": 500,
    "wins": 286,
    "losses": 214,
    "draws": 0,
    "win_rate": 0.572,
    "ci95": [
      0.5282,
      0.6147
    ]
  },
  "avg_turns": 19.26
}
wrote results/runs/J20-mirrors/machine-gun-furnace-br/summary.json, games.jsonl
```
