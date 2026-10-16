# Matchup matrix (500 games per pair, bot `heuristic2@human@kill2`, structures `any`)

Row deck's win rate against the column deck.

| | cattiva-azurobe-br | chillet-relaxaurus-bg | chillet-relaxaurus-bp | chillet-relaxaurus-br | foxparks-harness-br | lamball-cattiva-bg | lamball-stone-pit-pr | machine-gun-furnace-br | shadowbeak-menasting-bp | tombat-medicine-gp |
|---|---|---|---|---|---|---|---|---|---|---|
| **cattiva-azurobe-br** | — | 59 | 51 | 45 | 60 | 47 | 87 | 73 | 78 | 71 |
| **chillet-relaxaurus-bg** | 41 | — | 45 | 53 | 64 | 49 | 62 | 53 | 75 | 76 |
| **chillet-relaxaurus-bp** | 49 | 55 | — | 52 | 73 | 52 | 63 | 64 | 82 | 78 |
| **chillet-relaxaurus-br** | 55 | 47 | 48 | — | 68 | 46 | 69 | 67 | 79 | 71 |
| **foxparks-harness-br** | 40 | 36 | 27 | 32 | — | 33 | 61 | 60 | 68 | 53 |
| **lamball-cattiva-bg** | 53 | 51 | 48 | 54 | 67 | — | 85 | 74 | 74 | 75 |
| **lamball-stone-pit-pr** | 13 | 38 | 37 | 31 | 39 | 15 | — | 45 | 54 | 42 |
| **machine-gun-furnace-br** | 27 | 47 | 36 | 33 | 40 | 26 | 55 | — | 62 | 44 |
| **shadowbeak-menasting-bp** | 22 | 25 | 18 | 21 | 32 | 26 | 46 | 38 | — | 42 |
| **tombat-medicine-gp** | 29 | 24 | 22 | 29 | 47 | 25 | 58 | 56 | 58 | — |

## Calibration vs matchups_2026-10-12.json

10/36 pairs within ±5 points; mean absolute difference 11.0 points.
13/36 pairs consistent with the real data allowing for both sample sizes (|z| ≤ 2).

| Matchup | Sim | 95% CI | Real (games) | Diff | z | |
|---|---|---|---|---|---|---|
| cattiva-azurobe-br vs lamball-stone-pit-pr | 86.8 | 83.5–89.5 | 55.0 (944) | +31.8 | +14.3 | ❌ |
| lamball-cattiva-bg vs lamball-stone-pit-pr | 85.0 | 81.6–87.9 | 58.0 (1006) | +27.0 | +12.1 | ❌ |
| chillet-relaxaurus-br vs lamball-stone-pit-pr | 68.8 | 64.6–72.7 | 47.0 (1748) | +21.8 | +9.1 | ❌ |
| lamball-stone-pit-pr vs machine-gun-furnace-br | 45.0 | 40.7–49.4 | 66.0 (680) | -21.0 | -7.3 | ❌ |
| chillet-relaxaurus-bp vs foxparks-harness-br | 73.2 | 69.2–76.9 | 54.0 (3514) | +19.2 | +8.9 | ❌ |
| chillet-relaxaurus-br vs foxparks-harness-br | 68.0 | 63.8–71.9 | 50.0 (989) | +18.0 | +6.9 | ❌ |
| cattiva-azurobe-br vs tombat-medicine-gp | 71.0 | 66.9–74.8 | 54.0 (343) | +17.0 | +5.0 | ❌ |
| chillet-relaxaurus-br vs tombat-medicine-gp | 71.0 | 66.9–74.8 | 54.0 (893) | +17.0 | +6.5 | ❌ |
| lamball-stone-pit-pr vs tombat-medicine-gp | 42.2 | 38.0–46.6 | 59.0 (916) | -16.8 | -6.1 | ❌ |
| chillet-relaxaurus-bp vs shadowbeak-menasting-bp | 82.4 | 78.8–85.5 | 66.0 (1955) | +16.4 | +8.2 | ❌ |
| chillet-relaxaurus-bp vs tombat-medicine-gp | 78.0 | 74.2–81.4 | 62.0 (2723) | +16.0 | +7.7 | ❌ |
| lamball-stone-pit-pr vs shadowbeak-menasting-bp | 53.6 | 49.2–57.9 | 69.0 (665) | -15.4 | -5.4 | ❌ |
| chillet-relaxaurus-br vs shadowbeak-menasting-bp | 79.4 | 75.6–82.7 | 65.0 (679) | +14.4 | +5.6 | ❌ |
| machine-gun-furnace-br vs tombat-medicine-gp | 44.4 | 40.1–48.8 | 58.0 (363) | -13.6 | -4.0 | ❌ |
| lamball-cattiva-bg vs tombat-medicine-gp | 75.2 | 71.2–78.8 | 63.0 (328) | +12.2 | +3.7 | ❌ |
| chillet-relaxaurus-br vs machine-gun-furnace-br | 66.8 | 62.6–70.8 | 55.0 (619) | +11.8 | +4.1 | ❌ |
| chillet-relaxaurus-bp vs lamball-stone-pit-pr | 62.8 | 58.5–66.9 | 52.0 (6608) | +10.8 | +4.8 | ❌ |
| lamball-cattiva-bg vs machine-gun-furnace-br | 73.8 | 69.8–77.5 | 64.0 (296) | +9.8 | +2.9 | ❌ |
| foxparks-harness-br vs lamball-cattiva-bg | 32.8 | 28.8–37.0 | 42.0 (478) | -9.2 | -3.0 | ❌ |
| cattiva-azurobe-br vs machine-gun-furnace-br | 72.8 | 68.7–76.5 | 64.0 (258) | +8.8 | +2.5 | ❌ |
| cattiva-azurobe-br vs chillet-relaxaurus-br | 44.8 | 40.5–49.2 | 52.0 (700) | -7.2 | -2.5 | ❌ |
| cattiva-azurobe-br vs shadowbeak-menasting-bp | 77.6 | 73.7–81.0 | 71.0 (272) | +6.6 | +2.0 | ❌ |
| cattiva-azurobe-br vs foxparks-harness-br | 60.4 | 56.0–64.6 | 54.0 (445) | +6.4 | +2.0 | ❌ |
| foxparks-harness-br vs lamball-stone-pit-pr | 60.8 | 56.5–65.0 | 55.0 (1220) | +5.8 | +2.2 | ❌ |
| chillet-relaxaurus-bp vs machine-gun-furnace-br | 64.2 | 59.9–68.3 | 59.0 (1865) | +5.2 | +2.1 | ❌ |
| lamball-cattiva-bg vs shadowbeak-menasting-bp | 74.2 | 70.2–77.8 | 69.0 (258) | +5.2 | +1.5 | ❌ |
| machine-gun-furnace-br vs shadowbeak-menasting-bp | 62.0 | 57.7–66.1 | 57.0 (356) | +5.0 | +1.5 | ✅ |
| chillet-relaxaurus-bp vs lamball-cattiva-bg | 51.6 | 47.2–56.0 | 47.0 (2640) | +4.6 | +1.9 | ✅ |
| foxparks-harness-br vs tombat-medicine-gp | 53.4 | 49.0–57.7 | 58.0 (494) | -4.6 | -1.5 | ✅ |
| foxparks-harness-br vs shadowbeak-menasting-bp | 67.8 | 63.6–71.8 | 64.0 (360) | +3.8 | +1.2 | ✅ |
| cattiva-azurobe-br vs chillet-relaxaurus-bp | 51.0 | 46.6–55.4 | 54.0 (2581) | -3.0 | -1.2 | ✅ |
| shadowbeak-menasting-bp vs tombat-medicine-gp | 42.0 | 37.8–46.4 | 39.0 (366) | +3.0 | +0.9 | ✅ |
| foxparks-harness-br vs machine-gun-furnace-br | 59.6 | 55.2–63.8 | 62.0 (357) | -2.4 | -0.7 | ✅ |
| chillet-relaxaurus-br vs lamball-cattiva-bg | 46.0 | 41.7–50.4 | 48.0 (755) | -2.0 | -0.7 | ✅ |
| chillet-relaxaurus-bp vs chillet-relaxaurus-br | 51.6 | 47.2–56.0 | 53.0 (5264) | -1.4 | -0.6 | ✅ |
| cattiva-azurobe-br vs lamball-cattiva-bg | 47.2 | 42.9–51.6 | 46.0 (406) | +1.2 | +0.4 | ✅ |

No real-world data for: cattiva-azurobe-br vs chillet-relaxaurus-bg, chillet-relaxaurus-bg vs chillet-relaxaurus-bp, chillet-relaxaurus-bg vs chillet-relaxaurus-br, chillet-relaxaurus-bg vs foxparks-harness-br, chillet-relaxaurus-bg vs lamball-cattiva-bg, chillet-relaxaurus-bg vs lamball-stone-pit-pr, chillet-relaxaurus-bg vs machine-gun-furnace-br, chillet-relaxaurus-bg vs shadowbeak-menasting-bp, chillet-relaxaurus-bg vs tombat-medicine-gp
