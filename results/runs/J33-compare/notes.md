# J33 cloud runner evidence

Bobby explicitly authorized J33 in chat. Frozen source: 5f0282063d05bfe48f9d79b029e8b409791612a0. OpenAI cloud Linux only. Five exact commands, sequential; publish and verify after each. No protected edits or other jobs. Initial status: preflight complete, not yet launched.

1. `python3 -m sim compare --a results/runs/cattiva_dragons_v3.txt --b results/runs/J33-A_myfirst_axels.txt --games 12000 --seed 391 --bot human --sequential --out results/runs/J33-compare/A_myfirst_axels.md`
2. `python3 -m sim compare --a results/runs/cattiva_dragons_v3.txt --b results/runs/J33-B_myfirst_heavy.txt --games 12000 --seed 392 --bot human --sequential --out results/runs/J33-compare/B_myfirst_heavy.md`
3. `python3 -m sim compare --a results/runs/cattiva_dragons_v3.txt --b results/runs/J33-C_orserk_flambelle.txt --games 12000 --seed 393 --bot human --sequential --out results/runs/J33-compare/C_orserk_flambelle.md`
4. `python3 -m sim gauntlet --deck results/runs/swee_br.txt --games 4000 --seed 394 --bot human --out results/runs/J33-gauntlet/swee_br`
5. `python3 -m sim gauntlet --deck results/runs/cattiva_dragons_v3.txt --games 4000 --seed 394 --bot human --out results/runs/J33-gauntlet/v3`

All reports are simulation evidence, not real-event predictions or automatic adoption. BP02 preview texts remain provisional.
