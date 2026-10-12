
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

## J21.2: DONE
HEAD: 20097204499ae6656995a8546597c28387d76090
Start UTC: 2026-10-12T09:57:03.758661+00:00
End UTC: 2026-10-12T10:01:22.467116+00:00
Command: `python3 -m sim compare --a results/runs/cattiva_dragons.txt --b results/runs/cattiva_dragons_v2.txt --games 20000 --seed 212 --bot heuristic --sequential --out results/runs/J21-compare/v2.md`
Exit: 0; artifact gate: PASS
Evidence: /home/gator/palworld-run-artifacts/J20-J22-reordered
**heuristic**, 2000 games per list, seed 212: A 65.6% -> B 69.7% (diff +4.2 ± 1.4, z 2.9) [sequential: stopped early, clear after 2000 games]

Stdout tail:
```text
**heuristic**, 2000 games per list, seed 212: A 65.6% -> B 69.7% (diff +4.2 ± 1.4, z 2.9) [sequential: stopped early, clear after 2000 games]

| Opponent | Weight | A | B | Diff | Games |
|---|---|---|---|---|---|
| chillet-relaxaurus-bp | 38.5% | 63.1 | 68.2 | +5.1 | 770 |
| chillet-relaxaurus-br | 13.0% | 42.9 | 49.4 | +6.6 | 259 |
| lamball-stone-pit-pr | 12.2% | 79.5 | 82.8 | +3.3 | 244 |
| tombat-medicine-gp | 6.8% | 82.4 | 80.9 | -1.5 | 136 |
| foxparks-harness-br | 6.2% | 60.2 | 69.9 | +9.8 | 123 |
| machine-gun-furnace-br | 6.0% | 74.4 | 81.8 | +7.4 | 121 |
| shadowbeak-menasting-bp | 5.9% | 83.1 | 86.4 | +3.4 | 118 |
| cattiva-azurobe-br | 5.1% | 62.1 | 56.3 | -5.8 | 103 |
| lamball-cattiva-bg | 4.7% | 66.3 | 64.2 | -2.1 | 95 |
| chillet-relaxaurus-bg | 1.5% | 64.5 | 77.4 | +12.9 | 31 |

```

## J21.3: DONE
HEAD: da6038414fed383ab051e343d98cba3e138704ea
Start UTC: 2026-10-12T10:01:25.565748+00:00
End UTC: 2026-10-12T10:22:36.662108+00:00
Command: `python3 -m sim compare --a results/runs/cattiva_dragons.txt --b results/runs/J21-A_rifle_for_suzaku.txt --games 12000 --seed 213 --bot heuristic2 --sequential --out results/runs/J21-compare/A_rifle_for_suzaku.md`
Exit: 0; artifact gate: PASS
Evidence: /home/gator/palworld-run-artifacts/J20-J22-reordered
**heuristic2**, 2000 games per list, seed 213: A 64.5% -> B 58.8% (diff -5.6 ± 1.5, z -3.8) [sequential: stopped early, clear after 2000 games]

Stdout tail:
```text
**heuristic2**, 2000 games per list, seed 213: A 64.5% -> B 58.8% (diff -5.6 ± 1.5, z -3.8) [sequential: stopped early, clear after 2000 games]

| Opponent | Weight | A | B | Diff | Games |
|---|---|---|---|---|---|
| chillet-relaxaurus-bp | 38.5% | 56.5 | 52.1 | -4.4 | 770 |
| chillet-relaxaurus-br | 13.0% | 48.3 | 47.1 | -1.2 | 259 |
| lamball-stone-pit-pr | 12.2% | 88.5 | 82.0 | -6.6 | 244 |
| tombat-medicine-gp | 6.8% | 86.8 | 75.7 | -11.0 | 136 |
| foxparks-harness-br | 6.2% | 59.3 | 56.9 | -2.4 | 123 |
| machine-gun-furnace-br | 6.0% | 81.0 | 73.6 | -7.4 | 121 |
| shadowbeak-menasting-bp | 5.9% | 77.1 | 66.9 | -10.2 | 118 |
| cattiva-azurobe-br | 5.1% | 64.1 | 60.2 | -3.9 | 103 |
| lamball-cattiva-bg | 4.7% | 53.7 | 42.1 | -11.6 | 95 |
| chillet-relaxaurus-bg | 1.5% | 54.8 | 35.5 | -19.4 | 31 |

```

## J21.4: DONE
HEAD: cea85ce933932c88b01a76b3456525d3e376995c
Start UTC: 2026-10-12T10:22:39.713245+00:00
End UTC: 2026-10-12T10:27:06.244640+00:00
Command: `python3 -m sim compare --a results/runs/cattiva_dragons.txt --b results/runs/J21-A_rifle_for_suzaku.txt --games 12000 --seed 214 --bot heuristic --sequential --out results/runs/J21-compare/A_rifle_for_suzaku.md`
Exit: 0; artifact gate: PASS
Evidence: /home/gator/palworld-run-artifacts/J20-J22-reordered
**heuristic**, 2000 games per list, seed 214: A 67.6% -> B 60.4% (diff -7.2 ± 1.5, z -4.9) [sequential: stopped early, clear after 2000 games]

Stdout tail:
```text
**heuristic**, 2000 games per list, seed 214: A 67.6% -> B 60.4% (diff -7.2 ± 1.5, z -4.9) [sequential: stopped early, clear after 2000 games]

| Opponent | Weight | A | B | Diff | Games |
|---|---|---|---|---|---|
| chillet-relaxaurus-bp | 38.5% | 67.3 | 57.8 | -9.5 | 770 |
| chillet-relaxaurus-br | 13.0% | 47.1 | 43.2 | -3.9 | 259 |
| lamball-stone-pit-pr | 12.2% | 78.3 | 74.6 | -3.7 | 244 |
| tombat-medicine-gp | 6.8% | 82.4 | 66.9 | -15.4 | 136 |
| foxparks-harness-br | 6.2% | 60.2 | 61.0 | +0.8 | 123 |
| machine-gun-furnace-br | 6.0% | 71.9 | 64.5 | -7.4 | 121 |
| shadowbeak-menasting-bp | 5.9% | 83.1 | 83.1 | +0.0 | 118 |
| cattiva-azurobe-br | 5.1% | 66.0 | 64.1 | -1.9 | 103 |
| lamball-cattiva-bg | 4.7% | 67.4 | 50.5 | -16.8 | 95 |
| chillet-relaxaurus-bg | 1.5% | 61.3 | 45.2 | -16.1 | 31 |

```

## J21.5: DONE
HEAD: 4369969cb8e7ee90df9d4af25453965876dcb6e0
Start UTC: 2026-10-12T10:27:09.206968+00:00
End UTC: 2026-10-12T11:08:56.008875+00:00
Command: `python3 -m sim compare --a results/runs/cattiva_dragons.txt --b results/runs/J21-B_package_keep_sparkit.txt --games 12000 --seed 215 --bot heuristic2 --sequential --out results/runs/J21-compare/B_package_keep_sparkit.md`
Exit: 0; artifact gate: PASS
Evidence: /home/gator/palworld-run-artifacts/J20-J22-reordered
**heuristic2**, 4000 games per list, seed 215: A 65.9% -> B 60.8% (diff -5.0 ± 1.0, z -4.8) [sequential: stopped early, clear after 4000 games]

Stdout tail:
```text
**heuristic2**, 4000 games per list, seed 215: A 65.9% -> B 60.8% (diff -5.0 ± 1.0, z -4.8) [sequential: stopped early, clear after 4000 games]

| Opponent | Weight | A | B | Diff | Games |
|---|---|---|---|---|---|
| chillet-relaxaurus-bp | 38.5% | 60.5 | 54.8 | -5.7 | 1540 |
| chillet-relaxaurus-br | 13.0% | 53.5 | 50.0 | -3.5 | 518 |
| lamball-stone-pit-pr | 12.2% | 86.1 | 80.9 | -5.1 | 488 |
| tombat-medicine-gp | 6.8% | 76.8 | 71.7 | -5.1 | 272 |
| foxparks-harness-br | 6.2% | 60.6 | 61.0 | +0.4 | 246 |
| machine-gun-furnace-br | 6.0% | 75.2 | 74.4 | -0.8 | 242 |
| shadowbeak-menasting-bp | 5.9% | 79.7 | 80.9 | +1.3 | 236 |
| cattiva-azurobe-br | 5.1% | 68.0 | 59.7 | -8.3 | 206 |
| lamball-cattiva-bg | 4.7% | 54.2 | 34.2 | -20.0 | 190 |
| chillet-relaxaurus-bg | 1.5% | 56.5 | 51.6 | -4.8 | 62 |

```
