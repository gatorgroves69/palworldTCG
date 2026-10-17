# J36 — Relaxaurus Lux versus Q-quivern4

Bobby explicitly approved the one handoff line. OpenAI cloud Linux; frozen source `bf3a7482b4ebb9c3f50edf5a91af145c26536a52`. Main pulled before execution. No other job run.

```sh
python3 -m sim compare --a results/runs/Q-quivern4.txt --b results/runs/J34-lux_for_quivern.txt --games 12000 --seed 405 --bot human --sequential --out results/runs/J36-compare/lux_for_quivern.md
```

Started 2026-10-17T06:16:25Z; completed 2026-10-17T06:28:04Z, exit 0; wall time 11m39s. Exact stdout/start/end/exit are the dot-run files alongside this note.

Result: Q-quivern4 70.7% versus Lux variant 65.3%, difference −5.4 ±1.4 percentage points, z −3.8. Sequential clear-difference stop at nominal 2,000 games/list, 2,001 actual games/list from opponent allocation rounding. All ten matchup rows present; same human bot and seed 405. This simulation does not support replacing the two Quivern with Relaxaurus Lux. No deck adoption.

Validation: all 1,262 protected/code/input SHA-256 values unchanged; manifest retained locally. The command generated the report but no raw game records or experiment row. results/experiments.md remains unchanged. Publish report, evidence and this note; append-only main, pull before push. STOPPED at the one-line boundary. Claude to review.
