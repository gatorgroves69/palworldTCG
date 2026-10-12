
## J21.1: DONE
HEAD: eb23999dcebe804263508ccf39dfd73f43311aee
Start UTC: 2026-10-12T09:18:38.831877+00:00
End UTC: 2026-10-12T09:57:00.842790+00:00
Command: `python3 -m sim compare --a results/runs/cattiva_dragons.txt --b results/runs/cattiva_dragons_v2.txt --games 20000 --seed 211 --bot heuristic2 --sequential --out results/runs/J21-compare/v2.md`
Exit: 0; artifact gate: PASS
Evidence: /home/gator/palworld-run-artifacts/J20-J22-reordered
**heuristic2**, 4000 games per list, seed 211: A 65.8% -> B 68.4% (diff +2.6 ± 1.0, z 2.5) [sequential: stopped early, clear after 4000 games]

Stdout tail:
```text
**heuristic2**, 4000 games per list, seed 211: A 65.8% -> B 68.4% (diff +2.6 ± 1.0, z 2.5) [sequential: stopped early, clear after 4000 games]

| Opponent | Weight | A | B | Diff | Games |
|---|---|---|---|---|---|
| chillet-relaxaurus-bp | 38.5% | 58.4 | 61.4 | +3.0 | 1540 |
| chillet-relaxaurus-br | 13.0% | 52.3 | 56.9 | +4.6 | 518 |
| lamball-stone-pit-pr | 12.2% | 84.4 | 85.7 | +1.2 | 488 |
| tombat-medicine-gp | 6.8% | 79.0 | 85.3 | +6.2 | 272 |
| foxparks-harness-br | 6.2% | 69.1 | 72.8 | +3.7 | 246 |
| machine-gun-furnace-br | 6.0% | 76.0 | 78.1 | +2.1 | 242 |
| shadowbeak-menasting-bp | 5.9% | 78.0 | 80.5 | +2.5 | 236 |
| cattiva-azurobe-br | 5.1% | 73.3 | 69.9 | -3.4 | 206 |
| lamball-cattiva-bg | 4.7% | 55.3 | 55.3 | +0.0 | 190 |
| chillet-relaxaurus-bg | 1.5% | 67.7 | 64.5 | -3.2 | 62 |

```
