# Matchup matrix (500 games per pair, bot `heuristic2@human`, structures `any`)

Row deck's win rate against the column deck.

| | cattiva-azurobe-br | chillet-relaxaurus-bg | chillet-relaxaurus-bp | chillet-relaxaurus-br | foxparks-harness-br | lamball-cattiva-bg | lamball-stone-pit-pr | machine-gun-furnace-br | shadowbeak-menasting-bp | tombat-medicine-gp |
|---|---|---|---|---|---|---|---|---|---|---|
| **cattiva-azurobe-br** | — | 62 | 59 | 44 | 59 | 51 | 82 | 71 | 79 | 80 |
| **chillet-relaxaurus-bg** | 38 | — | 47 | 42 | 56 | 52 | 53 | 50 | 65 | 66 |
| **chillet-relaxaurus-bp** | 41 | 53 | — | 46 | 57 | 51 | 53 | 54 | 68 | 67 |
| **chillet-relaxaurus-br** | 56 | 58 | 54 | — | 60 | 52 | 67 | 71 | 76 | 69 |
| **foxparks-harness-br** | 41 | 44 | 43 | 40 | — | 36 | 54 | 60 | 63 | 58 |
| **lamball-cattiva-bg** | 49 | 48 | 49 | 48 | 64 | — | 82 | 72 | 71 | 75 |
| **lamball-stone-pit-pr** | 18 | 47 | 47 | 33 | 46 | 18 | — | 44 | 63 | 49 |
| **machine-gun-furnace-br** | 29 | 50 | 46 | 29 | 40 | 28 | 56 | — | 57 | 46 |
| **shadowbeak-menasting-bp** | 21 | 35 | 32 | 24 | 37 | 29 | 37 | 43 | — | 48 |
| **tombat-medicine-gp** | 20 | 34 | 33 | 31 | 42 | 25 | 51 | 54 | 52 | — |

## Calibration vs matchups_2026-10-12.json

14/36 pairs within ±5 points; mean absolute difference 8.5 points.
16/36 pairs consistent with the real data allowing for both sample sizes (|z| ≤ 2).

| Matchup | Sim | 95% CI | Real (games) | Diff | z | |
|---|---|---|---|---|---|---|
| cattiva-azurobe-br vs lamball-stone-pit-pr | 81.6 | 78.0–84.8 | 55.0 (944) | +26.6 | +11.2 | ❌ |
| cattiva-azurobe-br vs tombat-medicine-gp | 80.2 | 76.5–83.5 | 54.0 (343) | +26.2 | +8.1 | ❌ |
| lamball-cattiva-bg vs lamball-stone-pit-pr | 81.8 | 78.2–84.9 | 58.0 (1006) | +23.8 | +10.2 | ❌ |
| lamball-stone-pit-pr vs machine-gun-furnace-br | 44.2 | 39.9–48.6 | 66.0 (680) | -21.8 | -7.6 | ❌ |
| chillet-relaxaurus-br vs lamball-stone-pit-pr | 67.2 | 63.0–71.2 | 47.0 (1748) | +20.2 | +8.4 | ❌ |
| chillet-relaxaurus-br vs machine-gun-furnace-br | 70.6 | 66.5–74.4 | 55.0 (619) | +15.6 | +5.5 | ❌ |
| chillet-relaxaurus-br vs tombat-medicine-gp | 69.2 | 65.0–73.1 | 54.0 (893) | +15.2 | +5.7 | ❌ |
| lamball-cattiva-bg vs tombat-medicine-gp | 75.0 | 71.0–78.6 | 63.0 (328) | +12.0 | +3.6 | ❌ |
| machine-gun-furnace-br vs tombat-medicine-gp | 46.4 | 42.1–50.8 | 58.0 (363) | -11.6 | -3.4 | ❌ |
| chillet-relaxaurus-br vs shadowbeak-menasting-bp | 75.8 | 71.9–79.3 | 65.0 (679) | +10.8 | +4.1 | ❌ |
| chillet-relaxaurus-br vs foxparks-harness-br | 60.2 | 55.9–64.4 | 50.0 (989) | +10.2 | +3.8 | ❌ |
| lamball-stone-pit-pr vs tombat-medicine-gp | 49.4 | 45.0–53.8 | 59.0 (916) | -9.6 | -3.5 | ❌ |
| shadowbeak-menasting-bp vs tombat-medicine-gp | 48.0 | 43.6–52.4 | 39.0 (366) | +9.0 | +2.6 | ❌ |
| cattiva-azurobe-br vs shadowbeak-menasting-bp | 79.2 | 75.4–82.5 | 71.0 (272) | +8.2 | +2.5 | ❌ |
| cattiva-azurobe-br vs chillet-relaxaurus-br | 44.2 | 39.9–48.6 | 52.0 (700) | -7.8 | -2.7 | ❌ |
| lamball-cattiva-bg vs machine-gun-furnace-br | 71.6 | 67.5–75.4 | 64.0 (296) | +7.6 | +2.2 | ❌ |
| cattiva-azurobe-br vs machine-gun-furnace-br | 71.0 | 66.9–74.8 | 64.0 (258) | +7.0 | +1.9 | ❌ |
| chillet-relaxaurus-bp vs chillet-relaxaurus-br | 46.0 | 41.7–50.4 | 53.0 (5264) | -7.0 | -3.0 | ❌ |
| foxparks-harness-br vs lamball-cattiva-bg | 35.6 | 31.5–39.9 | 42.0 (478) | -6.4 | -2.1 | ❌ |
| lamball-stone-pit-pr vs shadowbeak-menasting-bp | 63.4 | 59.1–67.5 | 69.0 (665) | -5.6 | -2.0 | ❌ |
| cattiva-azurobe-br vs lamball-cattiva-bg | 51.2 | 46.8–55.6 | 46.0 (406) | +5.2 | +1.6 | ❌ |
| chillet-relaxaurus-bp vs machine-gun-furnace-br | 53.8 | 49.4–58.1 | 59.0 (1865) | -5.2 | -2.1 | ❌ |
| chillet-relaxaurus-bp vs tombat-medicine-gp | 66.8 | 62.6–70.8 | 62.0 (2723) | +4.8 | +2.1 | ✅ |
| cattiva-azurobe-br vs chillet-relaxaurus-bp | 58.6 | 54.2–62.8 | 54.0 (2581) | +4.6 | +1.9 | ✅ |
| cattiva-azurobe-br vs foxparks-harness-br | 58.6 | 54.2–62.8 | 54.0 (445) | +4.6 | +1.4 | ✅ |
| chillet-relaxaurus-br vs lamball-cattiva-bg | 52.2 | 47.8–56.5 | 48.0 (755) | +4.2 | +1.5 | ✅ |
| chillet-relaxaurus-bp vs lamball-cattiva-bg | 50.8 | 46.4–55.2 | 47.0 (2640) | +3.8 | +1.6 | ✅ |
| chillet-relaxaurus-bp vs foxparks-harness-br | 56.8 | 52.4–61.1 | 54.0 (3514) | +2.8 | +1.2 | ✅ |
| foxparks-harness-br vs machine-gun-furnace-br | 59.6 | 55.2–63.8 | 62.0 (357) | -2.4 | -0.7 | ✅ |
| lamball-cattiva-bg vs shadowbeak-menasting-bp | 71.4 | 67.3–75.2 | 69.0 (258) | +2.4 | +0.7 | ✅ |
| chillet-relaxaurus-bp vs shadowbeak-menasting-bp | 67.6 | 63.4–71.5 | 66.0 (1955) | +1.6 | +0.7 | ✅ |
| chillet-relaxaurus-bp vs lamball-stone-pit-pr | 53.2 | 48.8–57.5 | 52.0 (6608) | +1.2 | +0.5 | ✅ |
| foxparks-harness-br vs lamball-stone-pit-pr | 53.8 | 49.4–58.1 | 55.0 (1220) | -1.2 | -0.5 | ✅ |
| foxparks-harness-br vs shadowbeak-menasting-bp | 63.2 | 58.9–67.3 | 64.0 (360) | -0.8 | -0.2 | ✅ |
| foxparks-harness-br vs tombat-medicine-gp | 58.4 | 54.0–62.6 | 58.0 (494) | +0.4 | +0.1 | ✅ |
| machine-gun-furnace-br vs shadowbeak-menasting-bp | 57.0 | 52.6–61.3 | 57.0 (356) | +0.0 | +0.0 | ✅ |

No real-world data for: cattiva-azurobe-br vs chillet-relaxaurus-bg, chillet-relaxaurus-bg vs chillet-relaxaurus-bp, chillet-relaxaurus-bg vs chillet-relaxaurus-br, chillet-relaxaurus-bg vs foxparks-harness-br, chillet-relaxaurus-bg vs lamball-cattiva-bg, chillet-relaxaurus-bg vs lamball-stone-pit-pr, chillet-relaxaurus-bg vs machine-gun-furnace-br, chillet-relaxaurus-bg vs shadowbeak-menasting-bp, chillet-relaxaurus-bg vs tombat-medicine-gp
