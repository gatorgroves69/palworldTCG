# Matchup matrix (2000 games per pair, bot `heuristic`, structures `any`)

Row deck's win rate against the column deck.

| | cattiva-azurobe-br | chillet-relaxaurus-bg | chillet-relaxaurus-bp | chillet-relaxaurus-br | foxparks-harness-br | lamball-cattiva-bg | lamball-stone-pit-pr | shadowbeak-menasting-bp |
|---|---|---|---|---|---|---|---|---|
| **cattiva-azurobe-br** | — | 65 | 57 | 38 | 54 | 49 | 89 | 86 |
| **chillet-relaxaurus-bg** | 35 | — | 22 | 17 | 32 | 62 | 64 | 69 |
| **chillet-relaxaurus-bp** | 43 | 78 | — | 18 | 40 | 75 | 64 | 79 |
| **chillet-relaxaurus-br** | 62 | 83 | 82 | — | 62 | 69 | 79 | 85 |
| **foxparks-harness-br** | 46 | 68 | 60 | 38 | — | 47 | 68 | 69 |
| **lamball-cattiva-bg** | 51 | 38 | 25 | 31 | 53 | — | 85 | 82 |
| **lamball-stone-pit-pr** | 11 | 36 | 36 | 21 | 32 | 15 | — | 55 |
| **shadowbeak-menasting-bp** | 14 | 31 | 21 | 15 | 31 | 18 | 45 | — |

## Calibration vs matchups_2026-09-29.json

3/21 pairs within ±5 points; mean absolute difference 16.4 points.

| Matchup | Sim | 95% CI | Real | Diff | |
|---|---|---|---|---|---|
| chillet-relaxaurus-bp vs chillet-relaxaurus-br | 18.4 | 16.8–20.2 | 52.0 | -33.6 | ❌ |
| cattiva-azurobe-br vs lamball-stone-pit-pr | 89.4 | 88.0–90.7 | 56.0 | +33.4 | ❌ |
| chillet-relaxaurus-br vs lamball-stone-pit-pr | 79.4 | 77.6–81.1 | 47.0 | +32.4 | ❌ |
| lamball-cattiva-bg vs lamball-stone-pit-pr | 85.4 | 83.8–86.9 | 59.0 | +26.4 | ❌ |
| chillet-relaxaurus-bp vs lamball-cattiva-bg | 74.6 | 72.6–76.4 | 49.0 | +25.6 | ❌ |
| chillet-relaxaurus-br vs lamball-cattiva-bg | 68.9 | 66.8–70.9 | 45.0 | +23.9 | ❌ |
| chillet-relaxaurus-br vs shadowbeak-menasting-bp | 84.8 | 83.2–86.3 | 63.0 | +21.8 | ❌ |
| foxparks-harness-br vs lamball-stone-pit-pr | 68.2 | 66.2–70.2 | 50.0 | +18.2 | ❌ |
| cattiva-azurobe-br vs chillet-relaxaurus-br | 38.4 | 36.3–40.6 | 56.0 | -17.6 | ❌ |
| cattiva-azurobe-br vs shadowbeak-menasting-bp | 85.8 | 84.2–87.2 | 70.0 | +15.8 | ❌ |
| chillet-relaxaurus-bp vs foxparks-harness-br | 39.8 | 37.6–41.9 | 55.0 | -15.2 | ❌ |
| chillet-relaxaurus-bp vs shadowbeak-menasting-bp | 79.0 | 77.1–80.7 | 64.0 | +14.9 | ❌ |
| lamball-stone-pit-pr vs shadowbeak-menasting-bp | 54.7 | 52.5–56.9 | 68.0 | -13.3 | ❌ |
| chillet-relaxaurus-br vs foxparks-harness-br | 62.3 | 60.2–64.4 | 50.0 | +12.3 | ❌ |
| chillet-relaxaurus-bp vs lamball-stone-pit-pr | 64.3 | 62.2–66.4 | 53.0 | +11.3 | ❌ |
| lamball-cattiva-bg vs shadowbeak-menasting-bp | 81.7 | 79.9–83.3 | 72.0 | +9.7 | ❌ |
| foxparks-harness-br vs shadowbeak-menasting-bp | 68.8 | 66.8–70.8 | 62.0 | +6.9 | ❌ |
| foxparks-harness-br vs lamball-cattiva-bg | 47.0 | 44.9–49.2 | 41.0 | +6.0 | ❌ |
| cattiva-azurobe-br vs foxparks-harness-br | 53.9 | 51.7–56.1 | 56.0 | -2.1 | ✅ |
| cattiva-azurobe-br vs lamball-cattiva-bg | 49.1 | 47.0–51.3 | 51.0 | -1.8 | ✅ |
| cattiva-azurobe-br vs chillet-relaxaurus-bp | 57.2 | 55.0–59.4 | 56.0 | +1.2 | ✅ |

No real-world data for: cattiva-azurobe-br vs chillet-relaxaurus-bg, chillet-relaxaurus-bg vs chillet-relaxaurus-bp, chillet-relaxaurus-bg vs chillet-relaxaurus-br, chillet-relaxaurus-bg vs foxparks-harness-br, chillet-relaxaurus-bg vs lamball-cattiva-bg, chillet-relaxaurus-bg vs lamball-stone-pit-pr, chillet-relaxaurus-bg vs shadowbeak-menasting-bp
