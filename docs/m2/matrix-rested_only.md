# Matchup matrix (2000 games per pair, bot `heuristic`, structures `rested_only`)

Row deck's win rate against the column deck.

| | cattiva-azurobe-br | chillet-relaxaurus-bg | chillet-relaxaurus-bp | chillet-relaxaurus-br | foxparks-harness-br | lamball-cattiva-bg | lamball-stone-pit-pr | shadowbeak-menasting-bp |
|---|---|---|---|---|---|---|---|---|
| **cattiva-azurobe-br** | — | 65 | 57 | 38 | 54 | 49 | 90 | 86 |
| **chillet-relaxaurus-bg** | 35 | — | 22 | 17 | 32 | 62 | 65 | 68 |
| **chillet-relaxaurus-bp** | 43 | 78 | — | 18 | 40 | 75 | 63 | 78 |
| **chillet-relaxaurus-br** | 62 | 83 | 82 | — | 62 | 69 | 80 | 84 |
| **foxparks-harness-br** | 46 | 68 | 60 | 38 | — | 47 | 71 | 69 |
| **lamball-cattiva-bg** | 51 | 38 | 25 | 31 | 53 | — | 87 | 80 |
| **lamball-stone-pit-pr** | 9 | 35 | 37 | 20 | 29 | 13 | — | 54 |
| **shadowbeak-menasting-bp** | 14 | 32 | 22 | 16 | 31 | 20 | 46 | — |

## Calibration vs matchups_2026-09-29.json

3/21 pairs within ±5 points; mean absolute difference 16.5 points.

| Matchup | Sim | 95% CI | Real | Diff | |
|---|---|---|---|---|---|
| cattiva-azurobe-br vs lamball-stone-pit-pr | 90.5 | 89.1–91.7 | 56.0 | +34.5 | ❌ |
| chillet-relaxaurus-bp vs chillet-relaxaurus-br | 18.4 | 16.8–20.2 | 52.0 | -33.6 | ❌ |
| chillet-relaxaurus-br vs lamball-stone-pit-pr | 80.3 | 78.5–82.0 | 47.0 | +33.4 | ❌ |
| lamball-cattiva-bg vs lamball-stone-pit-pr | 87.0 | 85.5–88.4 | 59.0 | +28.0 | ❌ |
| chillet-relaxaurus-bp vs lamball-cattiva-bg | 74.6 | 72.6–76.4 | 49.0 | +25.6 | ❌ |
| chillet-relaxaurus-br vs lamball-cattiva-bg | 68.9 | 66.8–70.9 | 45.0 | +23.9 | ❌ |
| foxparks-harness-br vs lamball-stone-pit-pr | 70.9 | 68.9–72.9 | 50.0 | +20.9 | ❌ |
| chillet-relaxaurus-br vs shadowbeak-menasting-bp | 83.9 | 82.2–85.4 | 63.0 | +20.8 | ❌ |
| cattiva-azurobe-br vs chillet-relaxaurus-br | 38.4 | 36.3–40.6 | 56.0 | -17.6 | ❌ |
| cattiva-azurobe-br vs shadowbeak-menasting-bp | 85.7 | 84.0–87.1 | 70.0 | +15.7 | ❌ |
| chillet-relaxaurus-bp vs foxparks-harness-br | 39.8 | 37.6–41.9 | 55.0 | -15.2 | ❌ |
| chillet-relaxaurus-bp vs shadowbeak-menasting-bp | 78.2 | 76.3–80.0 | 64.0 | +14.2 | ❌ |
| lamball-stone-pit-pr vs shadowbeak-menasting-bp | 53.8 | 51.7–56.0 | 68.0 | -14.1 | ❌ |
| chillet-relaxaurus-br vs foxparks-harness-br | 62.3 | 60.2–64.4 | 50.0 | +12.3 | ❌ |
| chillet-relaxaurus-bp vs lamball-stone-pit-pr | 62.9 | 60.8–65.0 | 53.0 | +9.9 | ❌ |
| lamball-cattiva-bg vs shadowbeak-menasting-bp | 80.0 | 78.1–81.7 | 72.0 | +8.0 | ❌ |
| foxparks-harness-br vs shadowbeak-menasting-bp | 69.4 | 67.3–71.4 | 62.0 | +7.4 | ❌ |
| foxparks-harness-br vs lamball-cattiva-bg | 47.0 | 44.9–49.2 | 41.0 | +6.0 | ❌ |
| cattiva-azurobe-br vs foxparks-harness-br | 53.9 | 51.7–56.1 | 56.0 | -2.1 | ✅ |
| cattiva-azurobe-br vs lamball-cattiva-bg | 49.1 | 47.0–51.3 | 51.0 | -1.8 | ✅ |
| cattiva-azurobe-br vs chillet-relaxaurus-bp | 57.2 | 55.0–59.4 | 56.0 | +1.2 | ✅ |

No real-world data for: cattiva-azurobe-br vs chillet-relaxaurus-bg, chillet-relaxaurus-bg vs chillet-relaxaurus-bp, chillet-relaxaurus-bg vs chillet-relaxaurus-br, chillet-relaxaurus-bg vs foxparks-harness-br, chillet-relaxaurus-bg vs lamball-cattiva-bg, chillet-relaxaurus-bg vs lamball-stone-pit-pr, chillet-relaxaurus-bg vs shadowbeak-menasting-bp
