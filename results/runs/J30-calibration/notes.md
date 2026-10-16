# J30 calibration round 2

Bobby authorized J30 as written in the handoff on 2026-10-16. Frozen execution source: 0795d7a29719f48dde11e08d940e0c2886aaa77d. OpenAI cloud Linux, 9 cores, Python 3.12.14. Ten deck inputs, 45 unordered pairs per bot, 500 games per pair, four variants, 90,000 games total. No protected code or inputs changed.

Exact authorized command:
```
for b in heuristic2@human@struct3 heuristic2@human@kill2 heuristic2@human@allin heuristic2@human@struct3@kill2; do python3 -m sim matrix --decks data/decks/*.txt --games 500 --seed 255 --bot $b --out results/runs/J30-calibration/$b; done
```

Status: COMPLETE. Started 2026-10-16T07:49:26Z; resumed after interruption 11:37:30Z; exact loop exited 0 at 2026-10-16T14:40:31Z. All four matrices complete. Completed pairs resume from summary.json. Separate publisher checkpoints completed pair evidence every 15 minutes, and each final matrix as it completes; append-only main, pull before push, no rebase/force. Historical J25 comparator: heuristic2@human, 14/36 within ±5 points, MAE 8.5 points. New source provenance differs from J25; no automatic adoption.

## Calibration results
- heuristic2@human@struct3: 14/36 pairs within ±5 points; mean absolute difference 8.6 points (unrounded 8.55). 14/36 pairs consistent with real data allowing for both sample sizes (|z| ≤ 2). All 45 pair summaries validated against 22,500 raw game records, including win/loss and first/second counts, source, bot and seed. No demonstrated improvement over J25 baseline.
- heuristic2@human@kill2: 10/36 pairs within ±5 points; mean absolute difference 11.0 points. 13/36 pairs consistent with real data allowing for both sample sizes (|z| ≤ 2). All 45 pair summaries validated against 22,500 raw game records with the same checks above.
- heuristic2@human@allin: 10/36 pairs within ±5 points; mean absolute difference 10.2 points. 10/36 pairs consistent with real data allowing for both sample sizes (|z| ≤ 2). All 45 pair summaries validated against 22,500 raw game records with the same checks above.
- heuristic2@human@struct3@kill2: 9/36 pairs within ±5 points; mean absolute difference 12.0 points (11.98 unrounded). 11/36 pairs consistent with real data allowing for both sample sizes (|z| ≤ 2). All 45 pair summaries validated against 22,500 raw game records with the same checks above.

## Interrupted attempt and resume
Original supervised session disappeared after 97 finished pairs; no exit status was produced. Verified unknown process ID and unchanged protected inputs before rerunning the exact authorized loop at 2026-10-16T11:37:30Z. All 97 completed pair summaries were already verified on main at 588c0bf8d2ac4166467f4931a1d019ca7e04f8be. Earlier attempt evidence remains separately preserved; current attempt is dot-resume-20261016-1137.*.

## Final validation and boundary
All 180 pair summaries match 90,000 locally retained raw game records, including win/loss and first/second counts, bot, source and deterministic seed progression. Four matrix.json/matrix.md pairs are complete. All 1,268 protected-file SHA-256 hashes remain unchanged, and tracked source diff is empty. Exact final attempt exit/end evidence is preserved. Raw JSONL remote publication is not established; completed summaries and matrices are the resumable result checkpoints.

No new variant reduces observed calibration MAE versus the historical J25 human baseline; struct3 is closest, essentially flat at 8.55 versus 8.54 points. This is descriptive, not a statistical superiority test. Historical source differs, so comparison is qualified. No bot/deck adoption or source edit made. STOPPED at J30 boundary; next owner Claude to review.
