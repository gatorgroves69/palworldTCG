# J24 full-field comparisons

## Line 5: A_rifle4

**heuristic2**, 12000 games per list, seed 252: A 67.3% -> B 68.0% (diff +0.7 ± 0.6, z 1.2) [sequential: ran to the cap of 12000 games]

Command: `python3 -m sim compare --a results/runs/cattiva_dragons_v2.txt --b results/runs/J24-A_rifle4.txt --games 12000 --seed 252 --bot heuristic2 --sequential --out results/runs/J24-compare/A_rifle4.md`. Frozen execution code: 2c7ba53. Started 2026-10-14T06:14:50Z, ended 2026-10-14T08:18:06Z, exit 0. Report body matches stdout exactly after trimming terminal whitespace; deck paths, seed, bot and ten opponent rows checked.

The headline reports the nominal 12000-game cap per list. The opponent rows total 12006 games per list because the existing allocation independently rounds each opponent's share of every 2000-game batch (2001 actual games per batch, six batches). Counts match that allocation exactly. The compare command does not retain per-game JSONL; no raw game records are claimed for this line. Protected code and input paths remain unchanged from execution HEAD.
