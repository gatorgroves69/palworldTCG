# J25 calibration grid

## heuristic2 — complete, 2026-10-14 19:25 UTC

7/36 pairs within ±5 points; mean absolute difference 10.1 points.
10/36 pairs consistent with the real data allowing for both sample sizes (|z| ≤ 2).

All 45 unordered pairs completed, 500 games each (22,500 total), matrix seed 255, on frozen execution source 815792c. Calibration source: matchups_2026-10-12.json; nine pairs have no real-world comparison. All pair summaries were validated against their exact 500-record local games.jsonl files, including seeds, pair identities, bot, outcome counts, first/second splits, confidence intervals, average turns and end reasons. Matrix JSON agrees with all 45 summaries and calibration data; matrix Markdown matches the renderer output exactly.

This checkpoint preserves the 45 summary.json files and exact matrix.json/matrix.md on main. Raw games.jsonl publication remains pending; do not infer that these raw files are backed up remotely. Earlier lost pair evidence was not reconstructed.

The authorized loop has advanced to heuristic2@human. The other five variants are not complete; no cross-variant conclusion is available yet. Continue small validated checkpoints every 15 minutes and preserve each completed matrix. No new jobs, protected-code edits or deck adoption.

## heuristic2@human — complete, 2026-10-14 21:38 UTC

14/36 pairs within ±5 points; mean absolute difference 8.5 points.
16/36 pairs consistent with the real data allowing for both sample sizes (|z| ≤ 2).

All 45 pairs completed, 500 games each (22,500 total), matrix seed 255, frozen source 815792c. All summaries passed the same exact raw-record validation above. Matrix JSON agrees with all summaries and matchups_2026-10-12.json; exact Markdown matches renderer output. The human variant has lower mean absolute calibration error than baseline (8.5 vs 10.1 points) in this grid; the remaining four variants are unfinished.

This checkpoint saves all 90 pair summaries for the first two completed variants, both matrix artifacts for heuristic2@human, and the first completed heuristic2@seq pair summary (91 summaries total). Raw JSONL publication remains pending. The loop is now running heuristic2@seq. Prior progress statements above describe their dated checkpoints; this section is the current status. No code changes or automatic adoption.
