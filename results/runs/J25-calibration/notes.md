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

## heuristic2@seq — complete, verified 2026-10-15 00:55 UTC

7/36 pairs within ±5 points; mean absolute difference 10.1 points.
11/36 pairs consistent with the real data allowing for both sample sizes (|z| ≤ 2).

All 45 pairs completed, 500 games each (22,500 total), matrix seed 255, frozen source 815792c. All summaries passed exact raw-record validation. Matrix JSON agrees with all summaries and matchups_2026-10-12.json; exact Markdown matches renderer output. The unrounded mean absolute differences are 0.1009 for seq and 0.1005 for baseline; both display as 10.1 points. The human-only variant remains the lowest-error completed variant at 8.5 points; three variants remain unfinished and no default-bot decision is made.

This checkpoint preserves all 135 summaries and matrices for the first three variants plus three completed heuristic2@human@seq summaries (138 total). Raw JSONL publication remains outstanding. The fourth variant is incomplete. Existing historical sections remain unchanged; this is the latest verified checkpoint. No protected-code changes or additional jobs.


## heuristic2@human@seq — complete, verified 2026-10-15 04:29 UTC

14/36 pairs within ±5 points; mean absolute difference 9.0 points.
15/36 pairs consistent with the real data allowing for both sample sizes (|z| ≤ 2).

All 45 pairs completed, 500 games each (22,500 total), matrix seed 255, frozen source 815792c. All summaries passed exact raw-record validation. Matrix JSON agrees with all summaries and matchups_2026-10-12.json; exact Markdown matches renderer output. Human-only remains the lowest-error completed variant at 8.5 points. Two variants remain unfinished; no default-bot adoption decision is made.

This checkpoint preserves 216 validated pair summaries and the fourth variant's exact matrix.json/matrix.md. Raw JSONL publication remains outstanding. Publication resumed after user approval following the cancelled checkpoint call. Existing historical sections remain unchanged. No protected-code changes or additional jobs.


## heuristic2@human@seq@bold — complete, verified 2026-10-15 05:22 UTC

13/36 pairs within ±5 points; mean absolute difference 9.4 points.
13/36 pairs consistent with the real data allowing for both sample sizes (|z| ≤ 2).

All 45 pairs completed, 500 games each (22,500 total), matrix seed 255, frozen source 815792c. All summaries passed exact raw-record validation. Matrix JSON agrees with all summaries and matchups_2026-10-12.json; exact Markdown matches renderer output. Human-only remains the lowest-error completed variant at 8.5 points. The sixth variant remains unfinished; no default-bot adoption decision is made.

This checkpoint preserves 229 validated pair summaries and the fifth variant's exact matrix.json/matrix.md. Raw JSONL publication remains outstanding. Existing historical sections remain unchanged. No protected-code changes or additional jobs.


## Frozen execution provenance — verified 2026-10-15 05:45 UTC

J25 continues on source commit 815792ca3fa13ef2d384ae803b0f8033b3cbbb0d. All 1,247 tracked engine/bots/sim/cards/data file blob hashes were verified against that commit, with no protected-path working-tree changes. Remote main has since advanced to 05aa425edc0a0e550412f2cb99771efa2afd57d0, including changed @seq behavior; those changes are preserved by publication but were not pulled into the running source. These J25 results characterize the original frozen implementation, not the later @seq implementation on main.


## J25 six-variant grid complete — verified 2026-10-15 07:46 UTC

All six variants completed 45 pairs each, 500 games per pair: 270 pair summaries / 135,000 games. All summaries passed exact 500-record raw validation; the sixth matrix agrees with all 45 summaries and calibration data, and its Markdown matches the renderer exactly.

Calibration headlines (36 calibrated pairs; passing means within ±5 percentage points; noise-consistent means |z| ≤ 2):

- heuristic2: 7/36 passing, MAE 10.05 points, 10/36 noise-consistent.
- heuristic2@human: 14/36 passing, MAE 8.54 points, 16/36 noise-consistent.
- heuristic2@seq: 7/36 passing, MAE 10.09 points, 11/36 noise-consistent.
- heuristic2@human@seq: 14/36 passing, MAE 9.01 points, 15/36 noise-consistent.
- heuristic2@human@seq@bold: 13/36 passing, MAE 9.36 points, 13/36 noise-consistent.
- heuristic2@x1.5@human@seq: 13/36 passing, MAE 8.98 points, 14/36 noise-consistent.

Human-only has the lowest observed mean absolute calibration error in this grid. This is a descriptive comparison, not a statistical superiority claim or automatic bot adoption decision. All results use frozen source 815792c and matchups_2026-10-12.json, matrix seed 255, structures_attackable=any. They do not evaluate the later @seq implementation on main.

Publication handoff: all 270 summaries and six exact matrix JSON/Markdown pairs are preserved on main. Raw games.jsonl publication remains outstanding; raw evidence was validated locally but must not be described as remotely backed up. No extra jobs or protected-code edits were made. Earlier dated checkpoint statuses above are historical.
