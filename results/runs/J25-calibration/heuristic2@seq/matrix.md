# Matchup matrix (500 games per pair, bot `heuristic2@seq`, structures `any`)

Row deck's win rate against the column deck.

| | cattiva-azurobe-br | chillet-relaxaurus-bg | chillet-relaxaurus-bp | chillet-relaxaurus-br | foxparks-harness-br | lamball-cattiva-bg | lamball-stone-pit-pr | machine-gun-furnace-br | shadowbeak-menasting-bp | tombat-medicine-gp |
|---|---|---|---|---|---|---|---|---|---|---|
| **cattiva-azurobe-br** | — | 61 | 51 | 38 | 57 | 46 | 86 | 73 | 79 | 77 |
| **chillet-relaxaurus-bg** | 39 | — | 48 | 43 | 55 | 51 | 58 | 52 | 68 | 71 |
| **chillet-relaxaurus-bp** | 49 | 52 | — | 40 | 60 | 54 | 60 | 61 | 73 | 73 |
| **chillet-relaxaurus-br** | 62 | 57 | 60 | — | 61 | 55 | 72 | 70 | 80 | 78 |
| **foxparks-harness-br** | 43 | 45 | 40 | 39 | — | 35 | 60 | 56 | 62 | 53 |
| **lamball-cattiva-bg** | 54 | 49 | 46 | 45 | 65 | — | 80 | 70 | 74 | 73 |
| **lamball-stone-pit-pr** | 14 | 42 | 40 | 28 | 40 | 20 | — | 51 | 58 | 50 |
| **machine-gun-furnace-br** | 27 | 48 | 39 | 30 | 44 | 30 | 49 | — | 58 | 48 |
| **shadowbeak-menasting-bp** | 21 | 32 | 27 | 20 | 38 | 26 | 42 | 42 | — | 47 |
| **tombat-medicine-gp** | 23 | 29 | 27 | 22 | 47 | 27 | 50 | 52 | 53 | — |

## Calibration vs matchups_2026-10-12.json

7/36 pairs within ±5 points; mean absolute difference 10.1 points.
11/36 pairs consistent with the real data allowing for both sample sizes (|z| ≤ 2).

| Matchup | Sim | 95% CI | Real (games) | Diff | z | |
|---|---|---|---|---|---|---|
| cattiva-azurobe-br vs lamball-stone-pit-pr | 85.6 | 82.2–88.4 | 55.0 (944) | +30.6 | +13.6 | ❌ |
| chillet-relaxaurus-br vs lamball-stone-pit-pr | 72.4 | 68.3–76.1 | 47.0 (1748) | +25.4 | +10.9 | ❌ |
| chillet-relaxaurus-br vs tombat-medicine-gp | 78.4 | 74.6–81.8 | 54.0 (893) | +24.4 | +9.8 | ❌ |
| cattiva-azurobe-br vs tombat-medicine-gp | 76.6 | 72.7–80.1 | 54.0 (343) | +22.6 | +6.9 | ❌ |
| lamball-cattiva-bg vs lamball-stone-pit-pr | 79.6 | 75.8–82.9 | 58.0 (1006) | +21.6 | +9.1 | ❌ |
| chillet-relaxaurus-br vs shadowbeak-menasting-bp | 80.4 | 76.7–83.6 | 65.0 (679) | +15.4 | +6.0 | ❌ |
| chillet-relaxaurus-br vs machine-gun-furnace-br | 70.2 | 66.0–74.0 | 55.0 (619) | +15.2 | +5.3 | ❌ |
| lamball-stone-pit-pr vs machine-gun-furnace-br | 51.4 | 47.0–55.8 | 66.0 (680) | -14.6 | -5.1 | ❌ |
| cattiva-azurobe-br vs chillet-relaxaurus-br | 38.2 | 34.1–42.5 | 52.0 (700) | -13.8 | -4.8 | ❌ |
| chillet-relaxaurus-bp vs chillet-relaxaurus-br | 39.6 | 35.4–44.0 | 53.0 (5264) | -13.4 | -5.8 | ❌ |
| lamball-stone-pit-pr vs shadowbeak-menasting-bp | 57.6 | 53.2–61.9 | 69.0 (665) | -11.4 | -4.0 | ❌ |
| chillet-relaxaurus-br vs foxparks-harness-br | 61.0 | 56.7–65.2 | 50.0 (989) | +11.0 | +4.1 | ❌ |
| chillet-relaxaurus-bp vs tombat-medicine-gp | 72.8 | 68.7–76.5 | 62.0 (2723) | +10.8 | +4.9 | ❌ |
| lamball-cattiva-bg vs tombat-medicine-gp | 73.0 | 68.9–76.7 | 63.0 (328) | +10.0 | +3.0 | ❌ |
| machine-gun-furnace-br vs tombat-medicine-gp | 48.0 | 43.6–52.4 | 58.0 (363) | -10.0 | -2.9 | ❌ |
| cattiva-azurobe-br vs machine-gun-furnace-br | 73.0 | 68.9–76.7 | 64.0 (258) | +9.0 | +2.5 | ❌ |
| lamball-stone-pit-pr vs tombat-medicine-gp | 50.0 | 45.6–54.4 | 59.0 (916) | -9.0 | -3.3 | ❌ |
| chillet-relaxaurus-bp vs lamball-stone-pit-pr | 60.4 | 56.0–64.6 | 52.0 (6608) | +8.4 | +3.7 | ❌ |
| cattiva-azurobe-br vs shadowbeak-menasting-bp | 78.6 | 74.8–82.0 | 71.0 (272) | +7.6 | +2.3 | ❌ |
| shadowbeak-menasting-bp vs tombat-medicine-gp | 46.6 | 42.3–51.0 | 39.0 (366) | +7.6 | +2.2 | ❌ |
| chillet-relaxaurus-bp vs lamball-cattiva-bg | 53.8 | 49.4–58.1 | 47.0 (2640) | +6.8 | +2.8 | ❌ |
| chillet-relaxaurus-br vs lamball-cattiva-bg | 54.8 | 50.4–59.1 | 48.0 (755) | +6.8 | +2.4 | ❌ |
| chillet-relaxaurus-bp vs shadowbeak-menasting-bp | 72.6 | 68.5–76.3 | 66.0 (1955) | +6.6 | +2.9 | ❌ |
| foxparks-harness-br vs lamball-cattiva-bg | 35.4 | 31.3–39.7 | 42.0 (478) | -6.6 | -2.1 | ❌ |
| foxparks-harness-br vs machine-gun-furnace-br | 56.0 | 51.6–60.3 | 62.0 (357) | -6.0 | -1.8 | ❌ |
| chillet-relaxaurus-bp vs foxparks-harness-br | 59.6 | 55.2–63.8 | 54.0 (3514) | +5.6 | +2.4 | ❌ |
| lamball-cattiva-bg vs machine-gun-furnace-br | 69.6 | 65.4–73.5 | 64.0 (296) | +5.6 | +1.6 | ❌ |
| foxparks-harness-br vs tombat-medicine-gp | 52.8 | 48.4–57.1 | 58.0 (494) | -5.2 | -1.6 | ❌ |
| lamball-cattiva-bg vs shadowbeak-menasting-bp | 74.2 | 70.2–77.8 | 69.0 (258) | +5.2 | +1.5 | ❌ |
| foxparks-harness-br vs lamball-stone-pit-pr | 59.6 | 55.2–63.8 | 55.0 (1220) | +4.6 | +1.8 | ✅ |
| cattiva-azurobe-br vs foxparks-harness-br | 57.2 | 52.8–61.5 | 54.0 (445) | +3.2 | +1.0 | ✅ |
| cattiva-azurobe-br vs chillet-relaxaurus-bp | 51.0 | 46.6–55.4 | 54.0 (2581) | -3.0 | -1.2 | ✅ |
| chillet-relaxaurus-bp vs machine-gun-furnace-br | 61.4 | 57.1–65.6 | 59.0 (1865) | +2.4 | +1.0 | ✅ |
| foxparks-harness-br vs shadowbeak-menasting-bp | 61.8 | 57.5–66.0 | 64.0 (360) | -2.2 | -0.7 | ✅ |
| machine-gun-furnace-br vs shadowbeak-menasting-bp | 58.2 | 53.8–62.4 | 57.0 (356) | +1.2 | +0.3 | ✅ |
| cattiva-azurobe-br vs lamball-cattiva-bg | 46.4 | 42.1–50.8 | 46.0 (406) | +0.4 | +0.1 | ✅ |

No real-world data for: cattiva-azurobe-br vs chillet-relaxaurus-bg, chillet-relaxaurus-bg vs chillet-relaxaurus-bp, chillet-relaxaurus-bg vs chillet-relaxaurus-br, chillet-relaxaurus-bg vs foxparks-harness-br, chillet-relaxaurus-bg vs lamball-cattiva-bg, chillet-relaxaurus-bg vs lamball-stone-pit-pr, chillet-relaxaurus-bg vs machine-gun-furnace-br, chillet-relaxaurus-bg vs shadowbeak-menasting-bp, chillet-relaxaurus-bg vs tombat-medicine-gp
