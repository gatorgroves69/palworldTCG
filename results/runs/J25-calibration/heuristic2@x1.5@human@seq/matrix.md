# Matchup matrix (500 games per pair, bot `heuristic2@x1.5@human@seq`, structures `any`)

Row deck's win rate against the column deck.

| | cattiva-azurobe-br | chillet-relaxaurus-bg | chillet-relaxaurus-bp | chillet-relaxaurus-br | foxparks-harness-br | lamball-cattiva-bg | lamball-stone-pit-pr | machine-gun-furnace-br | shadowbeak-menasting-bp | tombat-medicine-gp |
|---|---|---|---|---|---|---|---|---|---|---|
| **cattiva-azurobe-br** | — | 63 | 61 | 47 | 58 | 49 | 86 | 75 | 78 | 82 |
| **chillet-relaxaurus-bg** | 37 | — | 48 | 42 | 57 | 51 | 53 | 51 | 65 | 66 |
| **chillet-relaxaurus-bp** | 39 | 52 | — | 43 | 53 | 47 | 54 | 55 | 67 | 67 |
| **chillet-relaxaurus-br** | 53 | 58 | 57 | — | 59 | 50 | 67 | 68 | 75 | 69 |
| **foxparks-harness-br** | 42 | 43 | 47 | 41 | — | 35 | 61 | 64 | 64 | 53 |
| **lamball-cattiva-bg** | 51 | 49 | 53 | 50 | 65 | — | 86 | 73 | 72 | 76 |
| **lamball-stone-pit-pr** | 14 | 47 | 46 | 33 | 39 | 14 | — | 49 | 59 | 51 |
| **machine-gun-furnace-br** | 25 | 49 | 45 | 32 | 36 | 27 | 51 | — | 56 | 43 |
| **shadowbeak-menasting-bp** | 22 | 35 | 33 | 25 | 36 | 28 | 41 | 44 | — | 47 |
| **tombat-medicine-gp** | 18 | 34 | 33 | 31 | 47 | 24 | 49 | 57 | 53 | — |

## Calibration vs matchups_2026-10-12.json

13/36 pairs within ±5 points; mean absolute difference 9.0 points.
14/36 pairs consistent with the real data allowing for both sample sizes (|z| ≤ 2).

| Matchup | Sim | 95% CI | Real (games) | Diff | z | |
|---|---|---|---|---|---|---|
| cattiva-azurobe-br vs lamball-stone-pit-pr | 86.2 | 82.9–88.9 | 55.0 (944) | +31.2 | +13.9 | ❌ |
| lamball-cattiva-bg vs lamball-stone-pit-pr | 86.4 | 83.1–89.1 | 58.0 (1006) | +28.4 | +13.0 | ❌ |
| cattiva-azurobe-br vs tombat-medicine-gp | 82.0 | 78.4–85.1 | 54.0 (343) | +28.0 | +8.8 | ❌ |
| chillet-relaxaurus-br vs lamball-stone-pit-pr | 67.2 | 63.0–71.2 | 47.0 (1748) | +20.2 | +8.4 | ❌ |
| lamball-stone-pit-pr vs machine-gun-furnace-br | 48.6 | 44.2–53.0 | 66.0 (680) | -17.4 | -6.0 | ❌ |
| chillet-relaxaurus-br vs tombat-medicine-gp | 69.2 | 65.0–73.1 | 54.0 (893) | +15.2 | +5.7 | ❌ |
| machine-gun-furnace-br vs tombat-medicine-gp | 43.4 | 39.1–47.8 | 58.0 (363) | -14.6 | -4.3 | ❌ |
| lamball-cattiva-bg vs tombat-medicine-gp | 76.4 | 72.5–79.9 | 63.0 (328) | +13.4 | +4.1 | ❌ |
| chillet-relaxaurus-br vs machine-gun-furnace-br | 68.2 | 64.0–72.1 | 55.0 (619) | +13.2 | +4.6 | ❌ |
| cattiva-azurobe-br vs machine-gun-furnace-br | 75.2 | 71.2–78.8 | 64.0 (258) | +11.2 | +3.1 | ❌ |
| chillet-relaxaurus-bp vs chillet-relaxaurus-br | 42.8 | 38.5–47.2 | 53.0 (5264) | -10.2 | -4.4 | ❌ |
| chillet-relaxaurus-br vs shadowbeak-menasting-bp | 75.2 | 71.2–78.8 | 65.0 (679) | +10.2 | +3.8 | ❌ |
| lamball-stone-pit-pr vs shadowbeak-menasting-bp | 59.0 | 54.6–63.2 | 69.0 (665) | -10.0 | -3.5 | ❌ |
| chillet-relaxaurus-br vs foxparks-harness-br | 59.2 | 54.8–63.4 | 50.0 (989) | +9.2 | +3.4 | ❌ |
| lamball-cattiva-bg vs machine-gun-furnace-br | 72.6 | 68.5–76.3 | 64.0 (296) | +8.6 | +2.5 | ❌ |
| lamball-stone-pit-pr vs tombat-medicine-gp | 51.2 | 46.8–55.6 | 59.0 (916) | -7.8 | -2.8 | ❌ |
| shadowbeak-menasting-bp vs tombat-medicine-gp | 46.8 | 42.5–51.2 | 39.0 (366) | +7.8 | +2.3 | ❌ |
| cattiva-azurobe-br vs shadowbeak-menasting-bp | 78.4 | 74.6–81.8 | 71.0 (272) | +7.4 | +2.2 | ❌ |
| cattiva-azurobe-br vs chillet-relaxaurus-bp | 60.6 | 56.2–64.8 | 54.0 (2581) | +6.6 | +2.8 | ❌ |
| foxparks-harness-br vs lamball-cattiva-bg | 35.4 | 31.3–39.7 | 42.0 (478) | -6.6 | -2.1 | ❌ |
| foxparks-harness-br vs lamball-stone-pit-pr | 61.2 | 56.9–65.4 | 55.0 (1220) | +6.2 | +2.4 | ❌ |
| chillet-relaxaurus-bp vs tombat-medicine-gp | 67.4 | 63.2–71.4 | 62.0 (2723) | +5.4 | +2.4 | ❌ |
| foxparks-harness-br vs tombat-medicine-gp | 52.6 | 48.2–56.9 | 58.0 (494) | -5.4 | -1.7 | ❌ |
| cattiva-azurobe-br vs chillet-relaxaurus-br | 47.0 | 42.7–51.4 | 52.0 (700) | -5.0 | -1.7 | ✅ |
| chillet-relaxaurus-bp vs machine-gun-furnace-br | 54.6 | 50.2–58.9 | 59.0 (1865) | -4.4 | -1.8 | ✅ |
| cattiva-azurobe-br vs foxparks-harness-br | 58.0 | 53.6–62.3 | 54.0 (445) | +4.0 | +1.2 | ✅ |
| lamball-cattiva-bg vs shadowbeak-menasting-bp | 72.0 | 67.9–75.8 | 69.0 (258) | +3.0 | +0.8 | ✅ |
| cattiva-azurobe-br vs lamball-cattiva-bg | 48.8 | 44.4–53.2 | 46.0 (406) | +2.8 | +0.8 | ✅ |
| chillet-relaxaurus-br vs lamball-cattiva-bg | 50.4 | 46.0–54.8 | 48.0 (755) | +2.4 | +0.8 | ✅ |
| chillet-relaxaurus-bp vs lamball-stone-pit-pr | 54.0 | 49.6–58.3 | 52.0 (6608) | +2.0 | +0.9 | ✅ |
| foxparks-harness-br vs machine-gun-furnace-br | 64.0 | 59.7–68.1 | 62.0 (357) | +2.0 | +0.6 | ✅ |
| chillet-relaxaurus-bp vs shadowbeak-menasting-bp | 67.4 | 63.2–71.4 | 66.0 (1955) | +1.4 | +0.6 | ✅ |
| chillet-relaxaurus-bp vs foxparks-harness-br | 52.8 | 48.4–57.1 | 54.0 (3514) | -1.2 | -0.5 | ✅ |
| machine-gun-furnace-br vs shadowbeak-menasting-bp | 56.4 | 52.0–60.7 | 57.0 (356) | -0.6 | -0.2 | ✅ |
| foxparks-harness-br vs shadowbeak-menasting-bp | 64.2 | 59.9–68.3 | 64.0 (360) | +0.2 | +0.1 | ✅ |
| chillet-relaxaurus-bp vs lamball-cattiva-bg | 47.0 | 42.7–51.4 | 47.0 (2640) | +0.0 | +0.0 | ✅ |

No real-world data for: cattiva-azurobe-br vs chillet-relaxaurus-bg, chillet-relaxaurus-bg vs chillet-relaxaurus-bp, chillet-relaxaurus-bg vs chillet-relaxaurus-br, chillet-relaxaurus-bg vs foxparks-harness-br, chillet-relaxaurus-bg vs lamball-cattiva-bg, chillet-relaxaurus-bg vs lamball-stone-pit-pr, chillet-relaxaurus-bg vs machine-gun-furnace-br, chillet-relaxaurus-bg vs shadowbeak-menasting-bp, chillet-relaxaurus-bg vs tombat-medicine-gp
