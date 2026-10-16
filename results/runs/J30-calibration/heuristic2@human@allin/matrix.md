# Matchup matrix (500 games per pair, bot `heuristic2@human@allin`, structures `any`)

Row deck's win rate against the column deck.

| | cattiva-azurobe-br | chillet-relaxaurus-bg | chillet-relaxaurus-bp | chillet-relaxaurus-br | foxparks-harness-br | lamball-cattiva-bg | lamball-stone-pit-pr | machine-gun-furnace-br | shadowbeak-menasting-bp | tombat-medicine-gp |
|---|---|---|---|---|---|---|---|---|---|---|
| **cattiva-azurobe-br** | — | 58 | 61 | 47 | 63 | 46 | 84 | 75 | 83 | 78 |
| **chillet-relaxaurus-bg** | 42 | — | 59 | 51 | 61 | 43 | 67 | 60 | 74 | 76 |
| **chillet-relaxaurus-bp** | 39 | 41 | — | 47 | 64 | 38 | 63 | 59 | 70 | 71 |
| **chillet-relaxaurus-br** | 53 | 49 | 53 | — | 59 | 40 | 67 | 66 | 74 | 70 |
| **foxparks-harness-br** | 37 | 39 | 36 | 41 | — | 31 | 57 | 59 | 62 | 62 |
| **lamball-cattiva-bg** | 54 | 57 | 62 | 60 | 69 | — | 84 | 75 | 79 | 83 |
| **lamball-stone-pit-pr** | 16 | 33 | 37 | 33 | 43 | 16 | — | 41 | 58 | 53 |
| **machine-gun-furnace-br** | 25 | 40 | 41 | 34 | 41 | 25 | 59 | — | 61 | 53 |
| **shadowbeak-menasting-bp** | 17 | 26 | 30 | 26 | 38 | 21 | 42 | 39 | — | 49 |
| **tombat-medicine-gp** | 22 | 24 | 29 | 30 | 38 | 17 | 47 | 47 | 51 | — |

## Calibration vs matchups_2026-10-12.json

10/36 pairs within ±5 points; mean absolute difference 10.2 points.
10/36 pairs consistent with the real data allowing for both sample sizes (|z| ≤ 2).

| Matchup | Sim | 95% CI | Real (games) | Diff | z | |
|---|---|---|---|---|---|---|
| cattiva-azurobe-br vs lamball-stone-pit-pr | 84.2 | 80.7–87.1 | 55.0 (944) | +29.2 | +12.7 | ❌ |
| lamball-cattiva-bg vs lamball-stone-pit-pr | 84.2 | 80.7–87.1 | 58.0 (1006) | +26.2 | +11.6 | ❌ |
| lamball-stone-pit-pr vs machine-gun-furnace-br | 41.4 | 37.2–45.8 | 66.0 (680) | -24.6 | -8.6 | ❌ |
| cattiva-azurobe-br vs tombat-medicine-gp | 78.2 | 74.4–81.6 | 54.0 (343) | +24.2 | +7.4 | ❌ |
| chillet-relaxaurus-br vs lamball-stone-pit-pr | 66.8 | 62.6–70.8 | 47.0 (1748) | +19.8 | +8.2 | ❌ |
| lamball-cattiva-bg vs tombat-medicine-gp | 82.6 | 79.0–85.7 | 63.0 (328) | +19.6 | +6.2 | ❌ |
| chillet-relaxaurus-br vs tombat-medicine-gp | 70.0 | 65.8–73.9 | 54.0 (893) | +16.0 | +6.1 | ❌ |
| cattiva-azurobe-br vs shadowbeak-menasting-bp | 83.2 | 79.7–86.2 | 71.0 (272) | +12.2 | +3.8 | ❌ |
| lamball-stone-pit-pr vs shadowbeak-menasting-bp | 57.6 | 53.2–61.9 | 69.0 (665) | -11.4 | -4.0 | ❌ |
| lamball-cattiva-bg vs machine-gun-furnace-br | 75.2 | 71.2–78.8 | 64.0 (296) | +11.2 | +3.3 | ❌ |
| chillet-relaxaurus-bp vs lamball-stone-pit-pr | 63.0 | 58.7–67.1 | 52.0 (6608) | +11.0 | +4.9 | ❌ |
| chillet-relaxaurus-br vs machine-gun-furnace-br | 65.8 | 61.5–69.8 | 55.0 (619) | +10.8 | +3.7 | ❌ |
| cattiva-azurobe-br vs machine-gun-furnace-br | 74.6 | 70.6–78.2 | 64.0 (258) | +10.6 | +3.0 | ❌ |
| foxparks-harness-br vs lamball-cattiva-bg | 31.4 | 27.5–35.6 | 42.0 (478) | -10.6 | -3.5 | ❌ |
| chillet-relaxaurus-bp vs foxparks-harness-br | 64.4 | 60.1–68.5 | 54.0 (3514) | +10.4 | +4.5 | ❌ |
| shadowbeak-menasting-bp vs tombat-medicine-gp | 49.2 | 44.8–53.6 | 39.0 (366) | +10.2 | +3.0 | ❌ |
| lamball-cattiva-bg vs shadowbeak-menasting-bp | 79.0 | 75.2–82.3 | 69.0 (258) | +10.0 | +2.9 | ❌ |
| chillet-relaxaurus-br vs shadowbeak-menasting-bp | 74.4 | 70.4–78.0 | 65.0 (679) | +9.4 | +3.5 | ❌ |
| cattiva-azurobe-br vs foxparks-harness-br | 63.2 | 58.9–67.3 | 54.0 (445) | +9.2 | +2.9 | ❌ |
| chillet-relaxaurus-br vs foxparks-harness-br | 59.2 | 54.8–63.4 | 50.0 (989) | +9.2 | +3.4 | ❌ |
| chillet-relaxaurus-bp vs lamball-cattiva-bg | 38.4 | 34.2–42.7 | 47.0 (2640) | -8.6 | -3.6 | ❌ |
| chillet-relaxaurus-bp vs tombat-medicine-gp | 70.6 | 66.5–74.4 | 62.0 (2723) | +8.6 | +3.8 | ❌ |
| chillet-relaxaurus-br vs lamball-cattiva-bg | 40.4 | 36.2–44.8 | 48.0 (755) | -7.6 | -2.7 | ❌ |
| cattiva-azurobe-br vs chillet-relaxaurus-bp | 60.6 | 56.2–64.8 | 54.0 (2581) | +6.6 | +2.8 | ❌ |
| lamball-stone-pit-pr vs tombat-medicine-gp | 53.2 | 48.8–57.5 | 59.0 (916) | -5.8 | -2.1 | ❌ |
| chillet-relaxaurus-bp vs chillet-relaxaurus-br | 47.4 | 43.1–51.8 | 53.0 (5264) | -5.6 | -2.4 | ❌ |
| cattiva-azurobe-br vs chillet-relaxaurus-br | 47.2 | 42.9–51.6 | 52.0 (700) | -4.8 | -1.6 | ✅ |
| machine-gun-furnace-br vs tombat-medicine-gp | 53.2 | 48.8–57.5 | 58.0 (363) | -4.8 | -1.4 | ✅ |
| chillet-relaxaurus-bp vs shadowbeak-menasting-bp | 70.4 | 66.3–74.2 | 66.0 (1955) | +4.4 | +1.9 | ✅ |
| machine-gun-furnace-br vs shadowbeak-menasting-bp | 60.8 | 56.5–65.0 | 57.0 (356) | +3.8 | +1.1 | ✅ |
| foxparks-harness-br vs tombat-medicine-gp | 61.6 | 57.3–65.8 | 58.0 (494) | +3.6 | +1.2 | ✅ |
| foxparks-harness-br vs machine-gun-furnace-br | 59.0 | 54.6–63.2 | 62.0 (357) | -3.0 | -0.9 | ✅ |
| foxparks-harness-br vs lamball-stone-pit-pr | 57.4 | 53.0–61.7 | 55.0 (1220) | +2.4 | +0.9 | ✅ |
| foxparks-harness-br vs shadowbeak-menasting-bp | 61.8 | 57.5–66.0 | 64.0 (360) | -2.2 | -0.7 | ✅ |
| chillet-relaxaurus-bp vs machine-gun-furnace-br | 59.4 | 55.0–63.6 | 59.0 (1865) | +0.4 | +0.2 | ✅ |
| cattiva-azurobe-br vs lamball-cattiva-bg | 46.2 | 41.9–50.6 | 46.0 (406) | +0.2 | +0.1 | ✅ |

No real-world data for: cattiva-azurobe-br vs chillet-relaxaurus-bg, chillet-relaxaurus-bg vs chillet-relaxaurus-bp, chillet-relaxaurus-bg vs chillet-relaxaurus-br, chillet-relaxaurus-bg vs foxparks-harness-br, chillet-relaxaurus-bg vs lamball-cattiva-bg, chillet-relaxaurus-bg vs lamball-stone-pit-pr, chillet-relaxaurus-bg vs machine-gun-furnace-br, chillet-relaxaurus-bg vs shadowbeak-menasting-bp, chillet-relaxaurus-bg vs tombat-medicine-gp
