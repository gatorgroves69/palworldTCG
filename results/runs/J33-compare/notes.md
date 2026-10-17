# J33 cloud runner evidence

Bobby explicitly authorized J33 in chat. Frozen source: 5f0282063d05bfe48f9d79b029e8b409791612a0. OpenAI cloud Linux only. Five exact commands, sequential; publish and verify after each. No protected edits or other jobs. Initial status: preflight complete, not yet launched.

1. `python3 -m sim compare --a results/runs/cattiva_dragons_v3.txt --b results/runs/J33-A_myfirst_axels.txt --games 12000 --seed 391 --bot human --sequential --out results/runs/J33-compare/A_myfirst_axels.md`
2. `python3 -m sim compare --a results/runs/cattiva_dragons_v3.txt --b results/runs/J33-B_myfirst_heavy.txt --games 12000 --seed 392 --bot human --sequential --out results/runs/J33-compare/B_myfirst_heavy.md`
3. `python3 -m sim compare --a results/runs/cattiva_dragons_v3.txt --b results/runs/J33-C_orserk_flambelle.txt --games 12000 --seed 393 --bot human --sequential --out results/runs/J33-compare/C_orserk_flambelle.md`
4. `python3 -m sim gauntlet --deck results/runs/swee_br.txt --games 4000 --seed 394 --bot human --out results/runs/J33-gauntlet/swee_br`
5. `python3 -m sim gauntlet --deck results/runs/cattiva_dragons_v3.txt --games 4000 --seed 394 --bot human --out results/runs/J33-gauntlet/v3`

All reports are simulation evidence, not real-event predictions or automatic adoption. BP02 preview texts remain provisional.

## Line 1 complete

Exit 0 at 2026-10-16T23:55:19.644490+00:00. Report/stdout agree; 2001 actual games per list from allocation rounding. **human**, 2000 games per list, seed 391: A 71.1% -> B 64.4% (diff -6.7 ± 1.4, z -4.6) [sequential: stopped early, clear after 2000 games]

All 1265 protected/input hashes unchanged. Next: line 2 after verified main publication.

## Line 2 complete

Exit 0 at 2026-10-17T00:10:08.313271+00:00. Report/stdout agree; 2001 actual games per list from allocation rounding. **human**, 2000 games per list, seed 392: A 68.4% -> B 62.5% (diff -5.9 ± 1.5, z -4.1) [sequential: stopped early, clear after 2000 games]

All 1265 protected/input hashes unchanged. Next: line 3 after verified main publication.

## Line 3 interruption

The original 2026-10-17 00:11 UTC supervised session became unavailable after cloud restart. At 00:37 UTC the session was unknown, no result/exit existed and no simulation process was found. Empty log and start/PID preserved as line-3-interrupted-001118.*. All 1265 protected/input hashes unchanged. Restarting only unfinished line 3 with the identical command; completed lines 1 and 2 are not rerun.

## Line 3 complete

Retry exit 0 at 2026-10-17T00:49:46.059578+00:00. Report/stdout agree; 2001 actual games per list from allocation rounding. **human**, 2000 games per list, seed 393: A 71.9% -> B 66.9% (diff -5.0 ± 1.4, z -3.5) [sequential: stopped early, clear after 2000 games]

All 1265 protected/input hashes unchanged. Next: line 4 after verified main publication.
