# J32 cloud runner

Bobby explicitly approved J32 as written. Frozen execution source: d26379e3b7aa0935866d3c3ee735814cfc16788f. OpenAI cloud Linux, 9 cores, Python 3.12.14. No protected-code/input edits or other jobs. Six exact commands, sequential human comparisons, cap 12000. Publish after every line before starting the next. Nonresumable: only restart an unfinished line after verifying its process stopped.

## Commands
```sh
python3 -m sim compare --a results/runs/cattiva_dragons_v3.txt --b results/runs/Q-frostallion_for_jorm.txt --games 12000 --seed 381 --bot human --sequential --out results/runs/J32-compare/frostallion_for_jorm.md
python3 -m sim compare --a results/runs/cattiva_dragons_v3.txt --b results/runs/Q-axgambit_for_jorm.txt --games 12000 --seed 382 --bot human --sequential --out results/runs/J32-compare/axgambit_for_jorm.md
python3 -m sim compare --a results/runs/cattiva_dragons_v3.txt --b results/runs/Q-vicgambit_for_jorm.txt --games 12000 --seed 383 --bot human --sequential --out results/runs/J32-compare/vicgambit_for_jorm.md
python3 -m sim compare --a results/runs/cattiva_dragons_v2.txt --b results/runs/Q-frostallion_for_suzaku.txt --games 12000 --seed 384 --bot human --sequential --out results/runs/J32-compare/frostallion_for_suzaku.md
python3 -m sim compare --a results/runs/cattiva_dragons_v2.txt --b results/runs/Q-axgambit_for_suzaku.txt --games 12000 --seed 385 --bot human --sequential --out results/runs/J32-compare/axgambit_for_suzaku.md
python3 -m sim compare --a results/runs/cattiva_dragons_v2.txt --b results/runs/Q-jetragon_for_suzaku.txt --games 12000 --seed 386 --bot human --sequential --out results/runs/J32-compare/jetragon_for_suzaku.md
```

## Status
Line 1 starting; lines 2–6 pending. No result yet.

## Line 1 complete
Exit 0 at 2026-10-16T20:29:35Z. Report matches stdout. All 1268 protected/input hashes unchanged. Actual opponent counts sum to 6003 games/list (allocation rounding).

**human**, 6000 games per list, seed 381: A 69.3% -> B 68.6% (diff -0.7 ± 0.8, z -0.9) [sequential: stopped early, no difference after 6000 games]

Waiting for verified publication before line 2.

## Line 2 complete
Exit 0 at 2026-10-16T20:45:15Z. Report matches stdout. All 1268 protected/input hashes unchanged. Actual opponent counts sum to 2001 games/list.

**human**, 2000 games per list, seed 382: A 68.3% -> B 63.0% (diff -5.3 ± 1.5, z -3.6) [sequential: stopped early, clear after 2000 games]

Waiting for verified publication before line 3.

## Line 3 complete
Exit 0 at 2026-10-16T21:00:41Z. Report matches stdout. All 1268 protected/input hashes unchanged. Actual opponent counts sum to 2001 games/list.

**human**, 2000 games per list, seed 383: A 69.2% -> B 64.6% (diff -4.6 ± 1.4, z -3.2) [sequential: stopped early, clear after 2000 games]

Waiting for verified publication before line 4.

## Line 4 complete
Exit 0 at 2026-10-16T21:42:59Z. Report matches stdout. All 1268 protected/input hashes unchanged. Actual opponent counts sum to 6003 games/list.

**human**, 6000 games per list, seed 384: A 68.4% -> B 68.0% (diff -0.4 ± 0.8, z -0.5) [sequential: stopped early, no difference after 6000 games]

Waiting for verified publication before line 5.
