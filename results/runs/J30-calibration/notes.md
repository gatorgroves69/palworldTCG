# J30 calibration round 2

Bobby authorized J30 as written in the handoff on 2026-10-16. Frozen execution source: 0795d7a29719f48dde11e08d940e0c2886aaa77d. OpenAI cloud Linux, 9 cores, Python 3.12.14. Ten deck inputs, 45 unordered pairs per bot, 500 games per pair, four variants, 90,000 games total. No protected code or inputs changed.

Exact authorized command:
```
for b in heuristic2@human@struct3 heuristic2@human@kill2 heuristic2@human@allin heuristic2@human@struct3@kill2; do python3 -m sim matrix --decks data/decks/*.txt --games 500 --seed 255 --bot $b --out results/runs/J30-calibration/$b; done
```

Status: preparing launch. Completed pairs resume from summary.json. Separate publisher checkpoints completed pair evidence every 15 minutes, and each final matrix as it completes; append-only main, pull before push, no rebase/force. Historical J25 comparator: heuristic2@human, 14/36 within ±5 points, MAE 8.5 points. New source provenance differs from J25; no automatic adoption.

## Calibration results
Pending.
