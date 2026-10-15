# Matchup matrix (500 games per pair, bot `heuristic2@human@seq`, structures `any`)

Row deck's win rate against the column deck.

| | cattiva-azurobe-br | chillet-relaxaurus-bg | chillet-relaxaurus-bp | chillet-relaxaurus-br | foxparks-harness-br | lamball-cattiva-bg | lamball-stone-pit-pr | machine-gun-furnace-br | shadowbeak-menasting-bp | tombat-medicine-gp |
|---|---|---|---|---|---|---|---|---|---|---|
| **cattiva-azurobe-br** | — | 62 | 59 | 44 | 59 | 51 | 85 | 72 | 79 | 81 |
| **chillet-relaxaurus-bg** | 38 | — | 47 | 42 | 56 | 52 | 54 | 53 | 66 | 66 |
| **chillet-relaxaurus-bp** | 41 | 53 | — | 46 | 57 | 51 | 55 | 54 | 67 | 66 |
| **chillet-relaxaurus-br** | 56 | 58 | 54 | — | 60 | 52 | 70 | 70 | 76 | 69 |
| **foxparks-harness-br** | 41 | 44 | 43 | 40 | — | 36 | 62 | 65 | 63 | 59 |
| **lamball-cattiva-bg** | 49 | 48 | 49 | 48 | 64 | — | 83 | 72 | 72 | 75 |
| **lamball-stone-pit-pr** | 15 | 46 | 45 | 30 | 38 | 17 | — | 47 | 63 | 50 |
| **machine-gun-furnace-br** | 28 | 47 | 46 | 30 | 35 | 28 | 53 | — | 57 | 46 |
| **shadowbeak-menasting-bp** | 21 | 34 | 33 | 24 | 37 | 28 | 37 | 43 | — | 49 |
| **tombat-medicine-gp** | 19 | 34 | 34 | 31 | 41 | 25 | 50 | 54 | 51 | — |

## Calibration vs matchups_2026-10-12.json

14/36 pairs within ±5 points; mean absolute difference 9.0 points.
15/36 pairs consistent with the real data allowing for both sample sizes (|z| ≤ 2).

| Matchup | Sim | 95% CI | Real (games) | Diff | z | |
|---|---|---|---|---|---|---|
| cattiva-azurobe-br vs lamball-stone-pit-pr | 85.0 | 81.6–87.9 | 55.0 (944) | +30.0 | +13.2 | ❌ |
| cattiva-azurobe-br vs tombat-medicine-gp | 80.8 | 77.1–84.0 | 54.0 (343) | +26.8 | +8.3 | ❌ |
| lamball-cattiva-bg vs lamball-stone-pit-pr | 83.2 | 79.7–86.2 | 58.0 (1006) | +25.2 | +11.0 | ❌ |
| chillet-relaxaurus-br vs lamball-stone-pit-pr | 70.4 | 66.3–74.2 | 47.0 (1748) | +23.4 | +9.9 | ❌ |
| lamball-stone-pit-pr vs machine-gun-furnace-br | 47.0 | 42.7–51.4 | 66.0 (680) | -19.0 | -6.6 | ❌ |
| chillet-relaxaurus-br vs machine-gun-furnace-br | 70.0 | 65.8–73.9 | 55.0 (619) | +15.0 | +5.2 | ❌ |
| chillet-relaxaurus-br vs tombat-medicine-gp | 69.0 | 64.8–72.9 | 54.0 (893) | +15.0 | +5.7 | ❌ |
| lamball-cattiva-bg vs tombat-medicine-gp | 75.2 | 71.2–78.8 | 63.0 (328) | +12.2 | +3.7 | ❌ |
| machine-gun-furnace-br vs tombat-medicine-gp | 46.2 | 41.9–50.6 | 58.0 (363) | -11.8 | -3.5 | ❌ |
| chillet-relaxaurus-br vs shadowbeak-menasting-bp | 76.0 | 72.1–79.5 | 65.0 (679) | +11.0 | +4.2 | ❌ |
| chillet-relaxaurus-br vs foxparks-harness-br | 60.2 | 55.9–64.4 | 50.0 (989) | +10.2 | +3.8 | ❌ |
| shadowbeak-menasting-bp vs tombat-medicine-gp | 48.8 | 44.4–53.2 | 39.0 (366) | +9.8 | +2.9 | ❌ |
| lamball-stone-pit-pr vs tombat-medicine-gp | 50.2 | 45.8–54.6 | 59.0 (916) | -8.8 | -3.2 | ❌ |
| cattiva-azurobe-br vs machine-gun-furnace-br | 72.4 | 68.3–76.1 | 64.0 (258) | +8.4 | +2.3 | ❌ |
| lamball-cattiva-bg vs machine-gun-furnace-br | 72.4 | 68.3–76.1 | 64.0 (296) | +8.4 | +2.5 | ❌ |
| cattiva-azurobe-br vs shadowbeak-menasting-bp | 79.0 | 75.2–82.3 | 71.0 (272) | +8.0 | +2.4 | ❌ |
| cattiva-azurobe-br vs chillet-relaxaurus-br | 44.2 | 39.9–48.6 | 52.0 (700) | -7.8 | -2.7 | ❌ |
| foxparks-harness-br vs lamball-stone-pit-pr | 62.4 | 58.1–66.5 | 55.0 (1220) | +7.4 | +2.9 | ❌ |
| chillet-relaxaurus-bp vs chillet-relaxaurus-br | 46.0 | 41.7–50.4 | 53.0 (5264) | -7.0 | -3.0 | ❌ |
| foxparks-harness-br vs lamball-cattiva-bg | 35.6 | 31.5–39.9 | 42.0 (478) | -6.4 | -2.1 | ❌ |
| lamball-stone-pit-pr vs shadowbeak-menasting-bp | 62.6 | 58.3–66.7 | 69.0 (665) | -6.4 | -2.3 | ❌ |
| cattiva-azurobe-br vs lamball-cattiva-bg | 51.2 | 46.8–55.6 | 46.0 (406) | +5.2 | +1.6 | ❌ |
| chillet-relaxaurus-bp vs machine-gun-furnace-br | 54.0 | 49.6–58.3 | 59.0 (1865) | -5.0 | -2.0 | ✅ |
| cattiva-azurobe-br vs chillet-relaxaurus-bp | 58.6 | 54.2–62.8 | 54.0 (2581) | +4.6 | +1.9 | ✅ |
| cattiva-azurobe-br vs foxparks-harness-br | 58.6 | 54.2–62.8 | 54.0 (445) | +4.6 | +1.4 | ✅ |
| chillet-relaxaurus-br vs lamball-cattiva-bg | 52.2 | 47.8–56.5 | 48.0 (755) | +4.2 | +1.5 | ✅ |
| chillet-relaxaurus-bp vs lamball-cattiva-bg | 50.8 | 46.4–55.2 | 47.0 (2640) | +3.8 | +1.6 | ✅ |
| chillet-relaxaurus-bp vs tombat-medicine-gp | 65.8 | 61.5–69.8 | 62.0 (2723) | +3.8 | +1.6 | ✅ |
| foxparks-harness-br vs machine-gun-furnace-br | 65.2 | 60.9–69.2 | 62.0 (357) | +3.2 | +1.0 | ✅ |
| chillet-relaxaurus-bp vs foxparks-harness-br | 56.8 | 52.4–61.1 | 54.0 (3514) | +2.8 | +1.2 | ✅ |
| chillet-relaxaurus-bp vs lamball-stone-pit-pr | 54.8 | 50.4–59.1 | 52.0 (6608) | +2.8 | +1.2 | ✅ |
| lamball-cattiva-bg vs shadowbeak-menasting-bp | 71.8 | 67.7–75.6 | 69.0 (258) | +2.8 | +0.8 | ✅ |
| chillet-relaxaurus-bp vs shadowbeak-menasting-bp | 67.4 | 63.2–71.4 | 66.0 (1955) | +1.4 | +0.6 | ✅ |
| foxparks-harness-br vs shadowbeak-menasting-bp | 62.8 | 58.5–66.9 | 64.0 (360) | -1.2 | -0.4 | ✅ |
| foxparks-harness-br vs tombat-medicine-gp | 59.0 | 54.6–63.2 | 58.0 (494) | +1.0 | +0.3 | ✅ |
| machine-gun-furnace-br vs shadowbeak-menasting-bp | 57.0 | 52.6–61.3 | 57.0 (356) | +0.0 | +0.0 | ✅ |

No real-world data for: cattiva-azurobe-br vs chillet-relaxaurus-bg, chillet-relaxaurus-bg vs chillet-relaxaurus-bp, chillet-relaxaurus-bg vs chillet-relaxaurus-br, chillet-relaxaurus-bg vs foxparks-harness-br, chillet-relaxaurus-bg vs lamball-cattiva-bg, chillet-relaxaurus-bg vs lamball-stone-pit-pr, chillet-relaxaurus-bg vs machine-gun-furnace-br, chillet-relaxaurus-bg vs shadowbeak-menasting-bp, chillet-relaxaurus-bg vs tombat-medicine-gp
