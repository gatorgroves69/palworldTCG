
## J20.10: DONE
HEAD: 2f0f52cad866d188e7ad58d1967f76d21ef00ecd
Start UTC: 2026-10-12T09:09:51.618239+00:00
End UTC: 2026-10-12T09:18:27.578707+00:00
Command: `python3 -m sim run --deck data/decks/tombat-medicine-gp.txt --opp data/decks/tombat-medicine-gp.txt --games 1000 --seed 201 --bot heuristic2 --deck-bot heuristic3 --no-report --logs 0 --out results/runs/J20-mirrors/tombat-medicine-gp`
Exit: 0; artifact gate: PASS
Evidence: /home/gator/palworld-run-artifacts/J20-J22-reordered
tombat-medicine-gp: heuristic3 mirror win rate 53.8%

Stdout tail:
```text
  700/1000 games
  800/1000 games
  900/1000 games
  1000/1000 games
{
  "win_rate": 0.538,
  "ci95": [
    0.507,
    0.5687
  ],
  "going_first": {
    "games": 500,
    "wins": 217,
    "losses": 283,
    "draws": 0,
    "win_rate": 0.434,
    "ci95": [
      0.3912,
      0.4778
    ]
  },
  "going_second": {
    "games": 500,
    "wins": 321,
    "losses": 179,
    "draws": 0,
    "win_rate": 0.642,
    "ci95": [
      0.599,
      0.6828
    ]
  },
  "avg_turns": 15.37
}
wrote results/runs/J20-mirrors/tombat-medicine-gp/summary.json, games.jsonl
```
