# Matchup matrix (1000 games per pair, bot `heuristic2`, structures `any`)

Row deck's win rate against the column deck.

| | cattiva-azurobe-br | chillet-relaxaurus-bg | chillet-relaxaurus-bp | chillet-relaxaurus-br | foxparks-harness-br | lamball-cattiva-bg | lamball-stone-pit-pr | machine-gun-furnace-br | shadowbeak-menasting-bp | tombat-medicine-gp |
|---|---|---|---|---|---|---|---|---|---|---|
| **cattiva-azurobe-br** | — | 57 | 53 | 42 | 56 | 45 | 80 | 69 | 76 | 76 |
| **chillet-relaxaurus-bg** | 43 | — | 48 | 40 | 57 | 51 | 54 | 48 | 70 | 70 |
| **chillet-relaxaurus-bp** | 47 | 52 | — | 45 | 62 | 52 | 59 | 57 | 76 | 72 |
| **chillet-relaxaurus-br** | 58 | 60 | 55 | — | 62 | 47 | 69 | 68 | 80 | 73 |
| **foxparks-harness-br** | 44 | 43 | 38 | 38 | — | 36 | 60 | 54 | 63 | 52 |
| **lamball-cattiva-bg** | 55 | 49 | 48 | 53 | 64 | — | 79 | 70 | 74 | 77 |
| **lamball-stone-pit-pr** | 19 | 46 | 41 | 31 | 40 | 21 | — | 47 | 61 | 47 |
| **machine-gun-furnace-br** | 31 | 52 | 43 | 32 | 46 | 30 | 53 | — | 64 | 51 |
| **shadowbeak-menasting-bp** | 24 | 31 | 24 | 20 | 37 | 26 | 39 | 36 | — | 43 |
| **tombat-medicine-gp** | 24 | 30 | 28 | 27 | 48 | 23 | 53 | 49 | 57 | — |

## Calibration vs matchups_2026-10-05.json

12/36 pairs within ±5 points; mean absolute difference 9.0 points.
13/36 pairs consistent with the real data allowing for both sample sizes (|z| ≤ 2).

| Matchup | Sim | 95% CI | Real (games) | Diff | z | |
|---|---|---|---|---|---|---|
| cattiva-azurobe-br vs lamball-stone-pit-pr | 80.5 | 77.9–82.8 | 56.0 (832) | +24.5 | +11.5 | ❌ |
| lamball-cattiva-bg vs lamball-stone-pit-pr | 79.1 | 76.5–81.5 | 58.0 (751) | +21.1 | +9.5 | ❌ |
| chillet-relaxaurus-br vs lamball-stone-pit-pr | 68.6 | 65.7–71.4 | 48.0 (1655) | +20.6 | +10.8 | ❌ |
| cattiva-azurobe-br vs tombat-medicine-gp | 75.9 | 73.2–78.5 | 56.0 (345) | +19.9 | +6.6 | ❌ |
| lamball-stone-pit-pr vs machine-gun-furnace-br | 47.1 | 44.0–50.2 | 66.0 (701) | -18.9 | -7.9 | ❌ |
| chillet-relaxaurus-br vs tombat-medicine-gp | 72.6 | 69.8–75.3 | 54.0 (1054) | +18.6 | +8.9 | ❌ |
| chillet-relaxaurus-br vs shadowbeak-menasting-bp | 79.6 | 77.0–82.0 | 63.0 (912) | +16.6 | +8.1 | ❌ |
| chillet-relaxaurus-br vs foxparks-harness-br | 62.3 | 59.2–65.2 | 48.0 (891) | +14.3 | +6.3 | ❌ |
| chillet-relaxaurus-br vs machine-gun-furnace-br | 68.1 | 65.1–70.9 | 55.0 (826) | +13.1 | +5.8 | ❌ |
| lamball-stone-pit-pr vs tombat-medicine-gp | 47.2 | 44.1–50.3 | 60.0 (868) | -12.8 | -5.6 | ❌ |
| cattiva-azurobe-br vs chillet-relaxaurus-br | 41.8 | 38.8–44.9 | 53.0 (711) | -11.2 | -4.6 | ❌ |
| chillet-relaxaurus-bp vs tombat-medicine-gp | 72.1 | 69.2–74.8 | 61.0 (2937) | +11.1 | +6.6 | ❌ |
| lamball-cattiva-bg vs tombat-medicine-gp | 77.1 | 74.4–79.6 | 66.0 (302) | +11.1 | +3.7 | ❌ |
| chillet-relaxaurus-bp vs shadowbeak-menasting-bp | 75.9 | 73.2–78.5 | 65.0 (2164) | +10.9 | +6.4 | ❌ |
| machine-gun-furnace-br vs shadowbeak-menasting-bp | 63.5 | 60.5–66.4 | 55.0 (490) | +8.5 | +3.1 | ❌ |
| lamball-stone-pit-pr vs shadowbeak-menasting-bp | 60.6 | 57.5–63.6 | 69.0 (675) | -8.4 | -3.6 | ❌ |
| foxparks-harness-br vs lamball-stone-pit-pr | 59.9 | 56.8–62.9 | 52.0 (945) | +7.9 | +3.5 | ❌ |
| foxparks-harness-br vs lamball-cattiva-bg | 35.5 | 32.6–38.5 | 43.0 (344) | -7.5 | -2.4 | ❌ |
| lamball-cattiva-bg vs machine-gun-furnace-br | 70.1 | 67.2–72.9 | 63.0 (298) | +7.1 | +2.2 | ❌ |
| chillet-relaxaurus-bp vs lamball-stone-pit-pr | 59.0 | 55.9–62.0 | 52.0 (5847) | +7.0 | +4.2 | ❌ |
| chillet-relaxaurus-bp vs chillet-relaxaurus-br | 45.1 | 42.0–48.2 | 52.0 (5595) | -6.9 | -4.0 | ❌ |
| chillet-relaxaurus-bp vs foxparks-harness-br | 61.6 | 58.6–64.6 | 55.0 (2931) | +6.6 | +3.7 | ❌ |
| cattiva-azurobe-br vs machine-gun-furnace-br | 68.6 | 65.7–71.4 | 63.0 (299) | +5.6 | +1.8 | ❌ |
| cattiva-azurobe-br vs shadowbeak-menasting-bp | 76.5 | 73.8–79.0 | 71.0 (309) | +5.5 | +1.9 | ❌ |
| foxparks-harness-br vs tombat-medicine-gp | 52.5 | 49.4–55.6 | 57.0 (451) | -4.5 | -1.6 | ✅ |
| chillet-relaxaurus-bp vs lamball-cattiva-bg | 51.9 | 48.8–55.0 | 48.0 (2317) | +3.9 | +2.1 | ✅ |
| lamball-cattiva-bg vs shadowbeak-menasting-bp | 74.1 | 71.3–76.7 | 71.0 (255) | +3.1 | +1.0 | ✅ |
| machine-gun-furnace-br vs tombat-medicine-gp | 50.9 | 47.8–54.0 | 54.0 (470) | -3.1 | -1.1 | ✅ |
| foxparks-harness-br vs machine-gun-furnace-br | 54.1 | 51.0–57.2 | 57.0 (368) | -2.9 | -1.0 | ✅ |
| cattiva-azurobe-br vs foxparks-harness-br | 55.7 | 52.6–58.8 | 53.0 (366) | +2.7 | +0.9 | ✅ |
| cattiva-azurobe-br vs lamball-cattiva-bg | 45.4 | 42.3–48.5 | 48.0 (344) | -2.6 | -0.8 | ✅ |
| cattiva-azurobe-br vs chillet-relaxaurus-bp | 52.8 | 49.7–55.9 | 55.0 (2431) | -2.2 | -1.2 | ✅ |
| chillet-relaxaurus-bp vs machine-gun-furnace-br | 56.6 | 53.5–59.6 | 58.0 (2276) | -1.4 | -0.8 | ✅ |
| shadowbeak-menasting-bp vs tombat-medicine-gp | 43.3 | 40.3–46.4 | 42.0 (443) | +1.3 | +0.5 | ✅ |
| chillet-relaxaurus-br vs lamball-cattiva-bg | 47.0 | 43.9–50.1 | 46.0 (700) | +1.0 | +0.4 | ✅ |
| foxparks-harness-br vs shadowbeak-menasting-bp | 62.6 | 59.6–65.5 | 63.0 (366) | -0.4 | -0.1 | ✅ |

No real-world data for: cattiva-azurobe-br vs chillet-relaxaurus-bg, chillet-relaxaurus-bg vs chillet-relaxaurus-bp, chillet-relaxaurus-bg vs chillet-relaxaurus-br, chillet-relaxaurus-bg vs foxparks-harness-br, chillet-relaxaurus-bg vs lamball-cattiva-bg, chillet-relaxaurus-bg vs lamball-stone-pit-pr, chillet-relaxaurus-bg vs machine-gun-furnace-br, chillet-relaxaurus-bg vs shadowbeak-menasting-bp, chillet-relaxaurus-bg vs tombat-medicine-gp
