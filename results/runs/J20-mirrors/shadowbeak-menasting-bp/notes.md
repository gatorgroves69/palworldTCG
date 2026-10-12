
## J20.9: DONE
HEAD: 33c98a05189967eada9e607f91316a5e1879f496
Start UTC: 2026-10-12T08:58:01.272984+00:00
End UTC: 2026-10-12T09:09:48.462128+00:00
Command: `python3 -m sim run --deck data/decks/shadowbeak-menasting-bp.txt --opp data/decks/shadowbeak-menasting-bp.txt --games 1000 --seed 201 --bot heuristic2 --deck-bot heuristic3 --no-report --logs 0 --out results/runs/J20-mirrors/shadowbeak-menasting-bp`
Exit: 0; artifact gate: PASS
Evidence: /home/gator/palworld-run-artifacts/J20-J22-reordered
shadowbeak-menasting-bp: heuristic3 mirror win rate 47.9%

Stdout tail:
```text
  700/1000 games
  800/1000 games
  900/1000 games
  1000/1000 games
{
  "win_rate": 0.479,
  "ci95": [
    0.4482,
    0.51
  ],
  "going_first": {
    "games": 500,
    "wins": 197,
    "losses": 303,
    "draws": 0,
    "win_rate": 0.394,
    "ci95": [
      0.3521,
      0.4375
    ]
  },
  "going_second": {
    "games": 500,
    "wins": 282,
    "losses": 218,
    "draws": 0,
    "win_rate": 0.564,
    "ci95": [
      0.5202,
      0.6068
    ]
  },
  "avg_turns": 15.95
}
wrote results/runs/J20-mirrors/shadowbeak-menasting-bp/summary.json, games.jsonl
```
