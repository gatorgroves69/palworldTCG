# Matchup matrix (1000 games per pair, bot `heuristic-learned`, structures `any`)

Row deck's win rate against the column deck.

| | cattiva-azurobe-br | chillet-relaxaurus-bg | chillet-relaxaurus-bp | chillet-relaxaurus-br | foxparks-harness-br | lamball-cattiva-bg | lamball-stone-pit-pr | shadowbeak-menasting-bp |
|---|---|---|---|---|---|---|---|---|
| **cattiva-azurobe-br** | — | 56 | 55 | 62 | 78 | 38 | 86 | 91 |
| **chillet-relaxaurus-bg** | 44 | — | 57 | 62 | 79 | 37 | 74 | 86 |
| **chillet-relaxaurus-bp** | 45 | 43 | — | 56 | 76 | 33 | 79 | 87 |
| **chillet-relaxaurus-br** | 38 | 38 | 44 | — | 67 | 26 | 73 | 82 |
| **foxparks-harness-br** | 22 | 21 | 24 | 33 | — | 15 | 63 | 70 |
| **lamball-cattiva-bg** | 62 | 63 | 67 | 74 | 85 | — | 90 | 94 |
| **lamball-stone-pit-pr** | 14 | 26 | 21 | 27 | 37 | 10 | — | 68 |
| **shadowbeak-menasting-bp** | 9 | 14 | 13 | 18 | 30 | 6 | 32 | — |

## Calibration vs matchups_2026-09-29.json

3/21 pairs within ±5 points; mean absolute difference 17.3 points.

| Matchup | Sim | 95% CI | Real | Diff | |
|---|---|---|---|---|---|
| lamball-cattiva-bg vs lamball-stone-pit-pr | 90.2 | 88.2–91.9 | 59.0 | +31.2 | ❌ |
| cattiva-azurobe-br vs lamball-stone-pit-pr | 86.3 | 84.0–88.3 | 56.0 | +30.3 | ❌ |
| chillet-relaxaurus-br vs lamball-stone-pit-pr | 73.2 | 70.4–75.8 | 47.0 | +26.2 | ❌ |
| foxparks-harness-br vs lamball-cattiva-bg | 14.9 | 12.8–17.2 | 41.0 | -26.1 | ❌ |
| chillet-relaxaurus-bp vs lamball-stone-pit-pr | 78.6 | 75.9–81.0 | 53.0 | +25.6 | ❌ |
| chillet-relaxaurus-bp vs shadowbeak-menasting-bp | 87.2 | 85.0–89.1 | 64.0 | +23.2 | ❌ |
| cattiva-azurobe-br vs foxparks-harness-br | 78.2 | 75.5–80.7 | 56.0 | +22.2 | ❌ |
| lamball-cattiva-bg vs shadowbeak-menasting-bp | 93.5 | 91.8–94.9 | 72.0 | +21.5 | ❌ |
| chillet-relaxaurus-bp vs foxparks-harness-br | 76.4 | 73.7–78.9 | 55.0 | +21.4 | ❌ |
| cattiva-azurobe-br vs shadowbeak-menasting-bp | 91.1 | 89.2–92.7 | 70.0 | +21.1 | ❌ |
| chillet-relaxaurus-br vs shadowbeak-menasting-bp | 82.1 | 79.6–84.4 | 63.0 | +19.1 | ❌ |
| chillet-relaxaurus-br vs lamball-cattiva-bg | 26.3 | 23.7–29.1 | 45.0 | -18.7 | ❌ |
| chillet-relaxaurus-br vs foxparks-harness-br | 67.1 | 64.1–69.9 | 50.0 | +17.1 | ❌ |
| chillet-relaxaurus-bp vs lamball-cattiva-bg | 33.3 | 30.4–36.3 | 49.0 | -15.7 | ❌ |
| cattiva-azurobe-br vs lamball-cattiva-bg | 38.0 | 35.0–41.0 | 51.0 | -13.0 | ❌ |
| foxparks-harness-br vs lamball-stone-pit-pr | 62.9 | 59.9–65.8 | 50.0 | +12.9 | ❌ |
| foxparks-harness-br vs shadowbeak-menasting-bp | 69.9 | 67.0–72.7 | 62.0 | +7.9 | ❌ |
| cattiva-azurobe-br vs chillet-relaxaurus-br | 61.5 | 58.5–64.5 | 56.0 | +5.5 | ❌ |
| chillet-relaxaurus-bp vs chillet-relaxaurus-br | 56.5 | 53.4–59.5 | 52.0 | +4.5 | ✅ |
| cattiva-azurobe-br vs chillet-relaxaurus-bp | 55.3 | 52.2–58.4 | 56.0 | -0.7 | ✅ |
| lamball-stone-pit-pr vs shadowbeak-menasting-bp | 68.1 | 65.1–70.9 | 68.0 | +0.1 | ✅ |

No real-world data for: cattiva-azurobe-br vs chillet-relaxaurus-bg, chillet-relaxaurus-bg vs chillet-relaxaurus-bp, chillet-relaxaurus-bg vs chillet-relaxaurus-br, chillet-relaxaurus-bg vs foxparks-harness-br, chillet-relaxaurus-bg vs lamball-cattiva-bg, chillet-relaxaurus-bg vs lamball-stone-pit-pr, chillet-relaxaurus-bg vs shadowbeak-menasting-bp
