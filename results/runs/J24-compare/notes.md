# J24 full-field comparisons

## Line 5: A_rifle4

**heuristic2**, 12000 games per list, seed 252: A 67.3% -> B 68.0% (diff +0.7 ± 0.6, z 1.2) [sequential: ran to the cap of 12000 games]

Command: `python3 -m sim compare --a results/runs/cattiva_dragons_v2.txt --b results/runs/J24-A_rifle4.txt --games 12000 --seed 252 --bot heuristic2 --sequential --out results/runs/J24-compare/A_rifle4.md`. Frozen execution code: 2c7ba53. Started 2026-10-14T06:14:50Z, ended 2026-10-14T08:18:06Z, exit 0. Report body matches stdout exactly after trimming terminal whitespace; deck paths, seed, bot and ten opponent rows checked.

The headline reports the nominal 12000-game cap per list. The opponent rows total 12006 games per list because the existing allocation independently rounds each opponent's share of every 2000-game batch (2001 actual games per batch, six batches). Counts match that allocation exactly. The compare command does not retain per-game JSONL; no raw game records are claimed for this line. Protected code and input paths remain unchanged from execution HEAD.

## Line 6: B_handgun

**heuristic2**, 10000 games per list, seed 253: A 68.2% -> B 66.5% (diff -1.7 ± 0.6, z -2.7) [sequential: stopped early, clear after 10000 games]

Command: `python3 -m sim compare --a results/runs/cattiva_dragons_v2.txt --b results/runs/J24-B_handgun.txt --games 12000 --seed 253 --bot heuristic2 --sequential --out results/runs/J24-compare/B_handgun.md`. Frozen execution code: 2c7ba53. Started 2026-10-14T08:25:42Z, ended 2026-10-14T10:08:12Z, exit 0. Report body matches stdout exactly after trimming terminal whitespace; deck paths, seed, bot and ten opponent rows checked.

The existing sequential stop threshold was reached at the nominal 10000 games per list, before the requested 12000 cap. Opponent rows total 10005 games per list, exactly matching five batches of the existing independently rounded allocation (2001 actual games per batch). The compare command does not retain per-game JSONL. Protected code and input paths remain unchanged from execution HEAD.

## Line 7: C_crystal

**heuristic2**, 12000 games per list, seed 254: A 68.3% -> B 67.1% (diff -1.2 ± 0.6, z -2.0) [sequential: ran to the cap of 12000 games]

Command: `python3 -m sim compare --a results/runs/cattiva_dragons_v2.txt --b results/runs/J24-C_crystal.txt --games 12000 --seed 254 --bot heuristic2 --sequential --out results/runs/J24-compare/C_crystal.md`. Frozen execution code: 2c7ba53. Completed retry started 2026-10-14T13:47:03Z, ended 2026-10-14T14:59:43Z, exit 0; successful evidence is in `logs/C_crystal.retry1.*`. Report body matches stdout exactly after trimming terminal whitespace; deck paths, seed, bot and ten opponent rows checked.

The original attempt started 2026-10-14T10:10:20Z and was interrupted without a completed report or exit marker. Its empty stdout and start marker are preserved in `logs/C_crystal.txt` and `.start`; no completion or exit status is claimed for that attempt. Only the completed retry contributes this result.

The headline reports the nominal 12000-game cap per list. Opponent rows total 12006 per list, matching six batches of the existing independently rounded allocation (2001 actual games per batch). The compare command does not retain per-game JSONL. Protected code and input paths remain unchanged from execution HEAD.

## Completed seven-line J24 summary

All seven authorized lines completed and were checkpointed individually. Stone Pit results use heuristic2@human@seq, seed 251, 2000 games per list; full-field comparisons use heuristic2 with the requested sequential stopping, paired seeds within each comparison.

- Line 1 baseline: 1747/2000, 87.35% (c85f167).
- Line 2 A_rifle4: 1716/2000, 85.80% (8f3082a).
- Line 3 B_handgun: 1751/2000, 87.55% (583b6c9).
- Line 4 C_crystal: 1703/2000, 85.15% (90f27dd).
- Line 5 A_rifle4 field: 67.3% to 68.0%, +0.7 ± 0.6 points, z 1.2; cap 12000/list, seed 252 (a18ccca).
- Line 6 B_handgun field: 68.2% to 66.5%, -1.7 ± 0.6 points, z -2.7; early stop at 10000/list, seed 253 (85c5bdb).
- Line 7 C_crystal field: 68.3% to 67.1%, -1.2 ± 0.6 points, z -2.0; cap 12000/list, seed 254 (this checkpoint).

No list change or automatic adoption was made. The Stone Pit simulation remains poorly calibrated against real play, so these rates are not real-event forecasts. J24 is complete; the user-authorized J25 calibration loop is next, with remote result checkpoints every 15 minutes.
