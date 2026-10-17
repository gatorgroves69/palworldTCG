# J33 gauntlets: authorized rerun

Bobby requested on 2026-10-17 05:52 UTC: pull main and rerun only lines 4 and 5, using identical handoff commands, pushing each when finished. Frozen source: fcda92fa670d50c31944d1eb63611cb0627650c1. Prior source was 5f028206; all 1265 protected/input hashes match it exactly, so execution code and inputs are unchanged. Old Swee evidence remains separate in the previous checkout; this directory is the new attempt. No lines 1–3 rerun.

python3 -m sim gauntlet --deck results/runs/swee_br.txt --games 4000 --seed 394 --bot human --out results/runs/J33-gauntlet/swee_br
python3 -m sim gauntlet --deck results/runs/cattiva_dragons_v3.txt --games 4000 --seed 394 --bot human --out results/runs/J33-gauntlet/v3

## Line 4 complete

Exit 0 at 2026-10-17T06:11:06.636781+00:00. Requested 4000 games, 3999 actual from allocation rounding. Validated all 3999 raw records, unique opponent/seed keys and per-opponent counts/winrates against summary. All 1265 protected/input hashes unchanged.

swee_br: 40.3% vs field (38.9-41.8, 3999 games, bot human)
Worst: chillet-relaxaurus-br 27% (12% of field); lamball-cattiva-bg 32% (6% of field); chillet-relaxaurus-bp 33% (39% of field)
Losses: ran out of cards 42%; behind on board by round 4-6 39%; behind on board by round 7+ 20%
seed 394, commit fcda92f, 17 min

Next: publish and remotely verify line 4 including lossless raw evidence, then run exact line 5.

## Line 5 complete / execution finished

Exit 0 at 2026-10-17T06:40:31.064971+00:00. Requested 4000 games, 3999 actual from allocation rounding. Validated all 3999 raw records, unique opponent/seed keys and per-opponent counts/winrates against summary. All 1265 protected/input hashes unchanged.

cattiva_dragons_v3: 70.4% vs field (69.0-71.7, 3999 games, bot human)
Worst: lamball-cattiva-bg 54% (6% of field); chillet-relaxaurus-bp 62% (39% of field); chillet-relaxaurus-bg 63% (2% of field)
Losses: ran out of cards 36%; behind on board by round 4-6 31%; opponent lucky saves 3+ 21%
seed 394, commit fcda92f, 12 min

Both gauntlets completed. No simulation remains running; no further job started. Final publication/remote verification pending. These are simulation results using provisional BP02 texts, not real-event predictions or an adoption decision.

Publication format: both exact raw record files are stored losslessly as `swee_br/games.jsonl.xz` and `v3/games.jsonl.xz`; decompress each with `xz -dk games.jsonl.xz` and verify against its `games.jsonl.sha256`. Uncompressed files remain in the execution checkout. Remote compressed bytes and decompressed SHA-256 are verified before completion is reported.
