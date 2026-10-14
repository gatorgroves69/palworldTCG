# Matchup matrix (500 games per pair, bot `heuristic2`, structures `any`)

Row deck's win rate against the column deck.

| | cattiva-azurobe-br | chillet-relaxaurus-bg | chillet-relaxaurus-bp | chillet-relaxaurus-br | foxparks-harness-br | lamball-cattiva-bg | lamball-stone-pit-pr | machine-gun-furnace-br | shadowbeak-menasting-bp | tombat-medicine-gp |
|---|---|---|---|---|---|---|---|---|---|---|
| **cattiva-azurobe-br** | — | 61 | 51 | 38 | 57 | 46 | 83 | 72 | 79 | 76 |
| **chillet-relaxaurus-bg** | 39 | — | 48 | 43 | 55 | 51 | 54 | 49 | 69 | 71 |
| **chillet-relaxaurus-bp** | 49 | 52 | — | 40 | 60 | 54 | 62 | 61 | 73 | 72 |
| **chillet-relaxaurus-br** | 62 | 57 | 60 | — | 61 | 55 | 71 | 66 | 81 | 78 |
| **foxparks-harness-br** | 43 | 45 | 40 | 39 | — | 35 | 57 | 54 | 62 | 53 |
| **lamball-cattiva-bg** | 54 | 49 | 46 | 45 | 65 | — | 80 | 70 | 75 | 73 |
| **lamball-stone-pit-pr** | 17 | 46 | 38 | 29 | 43 | 20 | — | 45 | 62 | 48 |
| **machine-gun-furnace-br** | 28 | 51 | 39 | 34 | 46 | 30 | 55 | — | 59 | 47 |
| **shadowbeak-menasting-bp** | 21 | 31 | 27 | 19 | 38 | 25 | 38 | 41 | — | 47 |
| **tombat-medicine-gp** | 24 | 29 | 28 | 22 | 47 | 27 | 52 | 53 | 53 | — |

## Calibration vs matchups_2026-10-12.json

7/36 pairs within ±5 points; mean absolute difference 10.1 points.
10/36 pairs consistent with the real data allowing for both sample sizes (|z| ≤ 2).

| Matchup | Sim | 95% CI | Real (games) | Diff | z | |
|---|---|---|---|---|---|---|
| cattiva-azurobe-br vs lamball-stone-pit-pr | 82.8 | 79.2–85.9 | 55.0 (944) | +27.8 | +11.9 | ❌ |
| chillet-relaxaurus-br vs lamball-stone-pit-pr | 71.4 | 67.3–75.2 | 47.0 (1748) | +24.4 | +10.4 | ❌ |
| chillet-relaxaurus-br vs tombat-medicine-gp | 77.8 | 74.0–81.2 | 54.0 (893) | +23.8 | +9.5 | ❌ |
| cattiva-azurobe-br vs tombat-medicine-gp | 76.4 | 72.5–79.9 | 54.0 (343) | +22.4 | +6.8 | ❌ |
| lamball-cattiva-bg vs lamball-stone-pit-pr | 80.0 | 76.3–83.3 | 58.0 (1006) | +22.0 | +9.3 | ❌ |
| lamball-stone-pit-pr vs machine-gun-furnace-br | 44.8 | 40.5–49.2 | 66.0 (680) | -21.2 | -7.4 | ❌ |
| chillet-relaxaurus-br vs shadowbeak-menasting-bp | 80.8 | 77.1–84.0 | 65.0 (679) | +15.8 | +6.2 | ❌ |
| cattiva-azurobe-br vs chillet-relaxaurus-br | 38.2 | 34.1–42.5 | 52.0 (700) | -13.8 | -4.8 | ❌ |
| chillet-relaxaurus-bp vs chillet-relaxaurus-br | 39.6 | 35.4–44.0 | 53.0 (5264) | -13.4 | -5.8 | ❌ |
| chillet-relaxaurus-br vs machine-gun-furnace-br | 66.4 | 62.2–70.4 | 55.0 (619) | +11.4 | +3.9 | ❌ |
| chillet-relaxaurus-br vs foxparks-harness-br | 61.0 | 56.7–65.2 | 50.0 (989) | +11.0 | +4.1 | ❌ |
| lamball-stone-pit-pr vs tombat-medicine-gp | 48.0 | 43.6–52.4 | 59.0 (916) | -11.0 | -4.0 | ❌ |
| machine-gun-furnace-br vs tombat-medicine-gp | 47.2 | 42.9–51.6 | 58.0 (363) | -10.8 | -3.2 | ❌ |
| chillet-relaxaurus-bp vs tombat-medicine-gp | 72.2 | 68.1–75.9 | 62.0 (2723) | +10.2 | +4.6 | ❌ |
| chillet-relaxaurus-bp vs lamball-stone-pit-pr | 62.0 | 57.7–66.1 | 52.0 (6608) | +10.0 | +4.4 | ❌ |
| lamball-cattiva-bg vs tombat-medicine-gp | 72.8 | 68.7–76.5 | 63.0 (328) | +9.8 | +3.0 | ❌ |
| shadowbeak-menasting-bp vs tombat-medicine-gp | 47.4 | 43.1–51.8 | 39.0 (366) | +8.4 | +2.5 | ❌ |
| cattiva-azurobe-br vs machine-gun-furnace-br | 72.2 | 68.1–75.9 | 64.0 (258) | +8.2 | +2.3 | ❌ |
| foxparks-harness-br vs machine-gun-furnace-br | 54.2 | 49.8–58.5 | 62.0 (357) | -7.8 | -2.3 | ❌ |
| cattiva-azurobe-br vs shadowbeak-menasting-bp | 78.6 | 74.8–82.0 | 71.0 (272) | +7.6 | +2.3 | ❌ |
| lamball-stone-pit-pr vs shadowbeak-menasting-bp | 61.8 | 57.5–66.0 | 69.0 (665) | -7.2 | -2.6 | ❌ |
| chillet-relaxaurus-bp vs shadowbeak-menasting-bp | 73.0 | 68.9–76.7 | 66.0 (1955) | +7.0 | +3.1 | ❌ |
| chillet-relaxaurus-bp vs lamball-cattiva-bg | 53.8 | 49.4–58.1 | 47.0 (2640) | +6.8 | +2.8 | ❌ |
| chillet-relaxaurus-br vs lamball-cattiva-bg | 54.8 | 50.4–59.1 | 48.0 (755) | +6.8 | +2.4 | ❌ |
| foxparks-harness-br vs lamball-cattiva-bg | 35.4 | 31.3–39.7 | 42.0 (478) | -6.6 | -2.1 | ❌ |
| lamball-cattiva-bg vs machine-gun-furnace-br | 69.8 | 65.6–73.7 | 64.0 (296) | +5.8 | +1.7 | ❌ |
| lamball-cattiva-bg vs shadowbeak-menasting-bp | 74.8 | 70.8–78.4 | 69.0 (258) | +5.8 | +1.7 | ❌ |
| chillet-relaxaurus-bp vs foxparks-harness-br | 59.6 | 55.2–63.8 | 54.0 (3514) | +5.6 | +2.4 | ❌ |
| foxparks-harness-br vs tombat-medicine-gp | 52.8 | 48.4–57.1 | 58.0 (494) | -5.2 | -1.6 | ❌ |
| cattiva-azurobe-br vs foxparks-harness-br | 57.2 | 52.8–61.5 | 54.0 (445) | +3.2 | +1.0 | ✅ |
| cattiva-azurobe-br vs chillet-relaxaurus-bp | 51.0 | 46.6–55.4 | 54.0 (2581) | -3.0 | -1.2 | ✅ |
| chillet-relaxaurus-bp vs machine-gun-furnace-br | 61.2 | 56.9–65.4 | 59.0 (1865) | +2.2 | +0.9 | ✅ |
| foxparks-harness-br vs shadowbeak-menasting-bp | 62.0 | 57.7–66.1 | 64.0 (360) | -2.0 | -0.6 | ✅ |
| foxparks-harness-br vs lamball-stone-pit-pr | 56.8 | 52.4–61.1 | 55.0 (1220) | +1.8 | +0.7 | ✅ |
| machine-gun-furnace-br vs shadowbeak-menasting-bp | 58.6 | 54.2–62.8 | 57.0 (356) | +1.6 | +0.5 | ✅ |
| cattiva-azurobe-br vs lamball-cattiva-bg | 46.4 | 42.1–50.8 | 46.0 (406) | +0.4 | +0.1 | ✅ |

No real-world data for: cattiva-azurobe-br vs chillet-relaxaurus-bg, chillet-relaxaurus-bg vs chillet-relaxaurus-bp, chillet-relaxaurus-bg vs chillet-relaxaurus-br, chillet-relaxaurus-bg vs foxparks-harness-br, chillet-relaxaurus-bg vs lamball-cattiva-bg, chillet-relaxaurus-bg vs lamball-stone-pit-pr, chillet-relaxaurus-bg vs machine-gun-furnace-br, chillet-relaxaurus-bg vs shadowbeak-menasting-bp, chillet-relaxaurus-bg vs tombat-medicine-gp
