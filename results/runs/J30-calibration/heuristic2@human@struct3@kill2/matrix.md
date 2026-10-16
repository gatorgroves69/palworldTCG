# Matchup matrix (500 games per pair, bot `heuristic2@human@struct3@kill2`, structures `any`)

Row deck's win rate against the column deck.

| | cattiva-azurobe-br | chillet-relaxaurus-bg | chillet-relaxaurus-bp | chillet-relaxaurus-br | foxparks-harness-br | lamball-cattiva-bg | lamball-stone-pit-pr | machine-gun-furnace-br | shadowbeak-menasting-bp | tombat-medicine-gp |
|---|---|---|---|---|---|---|---|---|---|---|
| **cattiva-azurobe-br** | — | 59 | 51 | 45 | 60 | 47 | 86 | 74 | 79 | 77 |
| **chillet-relaxaurus-bg** | 41 | — | 45 | 53 | 64 | 49 | 64 | 58 | 78 | 81 |
| **chillet-relaxaurus-bp** | 49 | 55 | — | 52 | 73 | 52 | 68 | 66 | 84 | 82 |
| **chillet-relaxaurus-br** | 55 | 47 | 48 | — | 68 | 46 | 71 | 67 | 84 | 78 |
| **foxparks-harness-br** | 40 | 36 | 27 | 32 | — | 33 | 61 | 60 | 71 | 61 |
| **lamball-cattiva-bg** | 53 | 51 | 48 | 54 | 67 | — | 86 | 78 | 78 | 82 |
| **lamball-stone-pit-pr** | 14 | 36 | 32 | 29 | 39 | 14 | — | 49 | 64 | 44 |
| **machine-gun-furnace-br** | 26 | 42 | 34 | 33 | 40 | 22 | 51 | — | 60 | 46 |
| **shadowbeak-menasting-bp** | 21 | 22 | 16 | 16 | 29 | 22 | 36 | 40 | — | 45 |
| **tombat-medicine-gp** | 23 | 19 | 18 | 22 | 39 | 18 | 56 | 54 | 55 | — |

## Calibration vs matchups_2026-10-12.json

9/36 pairs within ±5 points; mean absolute difference 12.0 points.
11/36 pairs consistent with the real data allowing for both sample sizes (|z| ≤ 2).

| Matchup | Sim | 95% CI | Real (games) | Diff | z | |
|---|---|---|---|---|---|---|
| cattiva-azurobe-br vs lamball-stone-pit-pr | 85.6 | 82.2–88.4 | 55.0 (944) | +30.6 | +13.6 | ❌ |
| lamball-cattiva-bg vs lamball-stone-pit-pr | 85.8 | 82.5–88.6 | 58.0 (1006) | +27.8 | +12.6 | ❌ |
| chillet-relaxaurus-br vs lamball-stone-pit-pr | 71.2 | 67.1–75.0 | 47.0 (1748) | +24.2 | +10.3 | ❌ |
| chillet-relaxaurus-br vs tombat-medicine-gp | 77.6 | 73.7–81.0 | 54.0 (893) | +23.6 | +9.4 | ❌ |
| cattiva-azurobe-br vs tombat-medicine-gp | 77.4 | 73.5–80.8 | 54.0 (343) | +23.4 | +7.1 | ❌ |
| chillet-relaxaurus-bp vs tombat-medicine-gp | 82.4 | 78.8–85.5 | 62.0 (2723) | +20.4 | +10.5 | ❌ |
| chillet-relaxaurus-bp vs foxparks-harness-br | 73.2 | 69.2–76.9 | 54.0 (3514) | +19.2 | +8.9 | ❌ |
| chillet-relaxaurus-br vs shadowbeak-menasting-bp | 84.0 | 80.5–87.0 | 65.0 (679) | +19.0 | +7.7 | ❌ |
| lamball-cattiva-bg vs tombat-medicine-gp | 82.0 | 78.4–85.1 | 63.0 (328) | +19.0 | +6.0 | ❌ |
| chillet-relaxaurus-br vs foxparks-harness-br | 68.0 | 63.8–71.9 | 50.0 (989) | +18.0 | +6.9 | ❌ |
| chillet-relaxaurus-bp vs shadowbeak-menasting-bp | 83.8 | 80.3–86.8 | 66.0 (1955) | +17.8 | +9.1 | ❌ |
| lamball-stone-pit-pr vs machine-gun-furnace-br | 48.8 | 44.4–53.2 | 66.0 (680) | -17.2 | -6.0 | ❌ |
| chillet-relaxaurus-bp vs lamball-stone-pit-pr | 68.2 | 64.0–72.1 | 52.0 (6608) | +16.2 | +7.5 | ❌ |
| lamball-stone-pit-pr vs tombat-medicine-gp | 44.4 | 40.1–48.8 | 59.0 (916) | -14.6 | -5.3 | ❌ |
| lamball-cattiva-bg vs machine-gun-furnace-br | 77.8 | 74.0–81.2 | 64.0 (296) | +13.8 | +4.1 | ❌ |
| chillet-relaxaurus-br vs machine-gun-furnace-br | 67.2 | 63.0–71.2 | 55.0 (619) | +12.2 | +4.2 | ❌ |
| machine-gun-furnace-br vs tombat-medicine-gp | 46.2 | 41.9–50.6 | 58.0 (363) | -11.8 | -3.5 | ❌ |
| cattiva-azurobe-br vs machine-gun-furnace-br | 74.0 | 70.0–77.6 | 64.0 (258) | +10.0 | +2.8 | ❌ |
| foxparks-harness-br vs lamball-cattiva-bg | 32.8 | 28.8–37.0 | 42.0 (478) | -9.2 | -3.0 | ❌ |
| lamball-cattiva-bg vs shadowbeak-menasting-bp | 78.0 | 74.2–81.4 | 69.0 (258) | +9.0 | +2.6 | ❌ |
| cattiva-azurobe-br vs shadowbeak-menasting-bp | 79.4 | 75.6–82.7 | 71.0 (272) | +8.4 | +2.5 | ❌ |
| foxparks-harness-br vs shadowbeak-menasting-bp | 71.4 | 67.3–75.2 | 64.0 (360) | +7.4 | +2.3 | ❌ |
| cattiva-azurobe-br vs chillet-relaxaurus-br | 44.8 | 40.5–49.2 | 52.0 (700) | -7.2 | -2.5 | ❌ |
| chillet-relaxaurus-bp vs machine-gun-furnace-br | 66.2 | 61.9–70.2 | 59.0 (1865) | +7.2 | +3.0 | ❌ |
| cattiva-azurobe-br vs foxparks-harness-br | 60.4 | 56.0–64.6 | 54.0 (445) | +6.4 | +2.0 | ❌ |
| shadowbeak-menasting-bp vs tombat-medicine-gp | 45.4 | 41.1–49.8 | 39.0 (366) | +6.4 | +1.9 | ❌ |
| foxparks-harness-br vs lamball-stone-pit-pr | 61.0 | 56.7–65.2 | 55.0 (1220) | +6.0 | +2.3 | ❌ |
| lamball-stone-pit-pr vs shadowbeak-menasting-bp | 64.2 | 59.9–68.3 | 69.0 (665) | -4.8 | -1.7 | ✅ |
| chillet-relaxaurus-bp vs lamball-cattiva-bg | 51.6 | 47.2–56.0 | 47.0 (2640) | +4.6 | +1.9 | ✅ |
| foxparks-harness-br vs tombat-medicine-gp | 61.2 | 56.9–65.4 | 58.0 (494) | +3.2 | +1.0 | ✅ |
| cattiva-azurobe-br vs chillet-relaxaurus-bp | 51.0 | 46.6–55.4 | 54.0 (2581) | -3.0 | -1.2 | ✅ |
| machine-gun-furnace-br vs shadowbeak-menasting-bp | 60.0 | 55.6–64.2 | 57.0 (356) | +3.0 | +0.9 | ✅ |
| foxparks-harness-br vs machine-gun-furnace-br | 59.8 | 55.4–64.0 | 62.0 (357) | -2.2 | -0.7 | ✅ |
| chillet-relaxaurus-br vs lamball-cattiva-bg | 46.0 | 41.7–50.4 | 48.0 (755) | -2.0 | -0.7 | ✅ |
| chillet-relaxaurus-bp vs chillet-relaxaurus-br | 51.6 | 47.2–56.0 | 53.0 (5264) | -1.4 | -0.6 | ✅ |
| cattiva-azurobe-br vs lamball-cattiva-bg | 47.2 | 42.9–51.6 | 46.0 (406) | +1.2 | +0.4 | ✅ |

No real-world data for: cattiva-azurobe-br vs chillet-relaxaurus-bg, chillet-relaxaurus-bg vs chillet-relaxaurus-bp, chillet-relaxaurus-bg vs chillet-relaxaurus-br, chillet-relaxaurus-bg vs foxparks-harness-br, chillet-relaxaurus-bg vs lamball-cattiva-bg, chillet-relaxaurus-bg vs lamball-stone-pit-pr, chillet-relaxaurus-bg vs machine-gun-furnace-br, chillet-relaxaurus-bg vs shadowbeak-menasting-bp, chillet-relaxaurus-bg vs tombat-medicine-gp
