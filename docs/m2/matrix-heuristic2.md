# Matchup matrix (1000 games per pair, bot `heuristic2`, structures `any`)

Row deck's win rate against the column deck.

| | cattiva-azurobe-br | chillet-relaxaurus-bg | chillet-relaxaurus-bp | chillet-relaxaurus-br | foxparks-harness-br | lamball-cattiva-bg | lamball-stone-pit-pr | shadowbeak-menasting-bp |
|---|---|---|---|---|---|---|---|---|
| **cattiva-azurobe-br** | — | 58 | 58 | 51 | 66 | 42 | 85 | 82 |
| **chillet-relaxaurus-bg** | 42 | — | 54 | 47 | 64 | 43 | 67 | 72 |
| **chillet-relaxaurus-bp** | 42 | 46 | — | 42 | 66 | 37 | 66 | 72 |
| **chillet-relaxaurus-br** | 49 | 53 | 58 | — | 62 | 38 | 70 | 74 |
| **foxparks-harness-br** | 34 | 36 | 34 | 38 | — | 30 | 62 | 59 |
| **lamball-cattiva-bg** | 58 | 57 | 63 | 62 | 70 | — | 85 | 85 |
| **lamball-stone-pit-pr** | 15 | 33 | 34 | 30 | 38 | 15 | — | 56 |
| **shadowbeak-menasting-bp** | 18 | 28 | 28 | 26 | 41 | 15 | 44 | — |

## Calibration vs matchups_2026-09-29.json

3/21 pairs within ±5 points; mean absolute difference 12.0 points.

| Matchup | Sim | 95% CI | Real | Diff | |
|---|---|---|---|---|---|
| cattiva-azurobe-br vs lamball-stone-pit-pr | 84.9 | 82.5–87.0 | 56.0 | +28.9 | ❌ |
| lamball-cattiva-bg vs lamball-stone-pit-pr | 85.4 | 83.1–87.5 | 59.0 | +26.4 | ❌ |
| chillet-relaxaurus-br vs lamball-stone-pit-pr | 70.5 | 67.6–73.2 | 47.0 | +23.5 | ❌ |
| lamball-cattiva-bg vs shadowbeak-menasting-bp | 85.2 | 82.9–87.3 | 72.0 | +13.2 | ❌ |
| chillet-relaxaurus-bp vs lamball-stone-pit-pr | 66.1 | 63.1–69.0 | 53.0 | +13.1 | ❌ |
| chillet-relaxaurus-bp vs lamball-cattiva-bg | 36.6 | 33.7–39.6 | 49.0 | -12.4 | ❌ |
| chillet-relaxaurus-br vs foxparks-harness-br | 62.3 | 59.2–65.2 | 50.0 | +12.3 | ❌ |
| cattiva-azurobe-br vs shadowbeak-menasting-bp | 82.1 | 79.6–84.4 | 70.0 | +12.1 | ❌ |
| foxparks-harness-br vs lamball-stone-pit-pr | 61.9 | 58.9–64.9 | 50.0 | +11.9 | ❌ |
| lamball-stone-pit-pr vs shadowbeak-menasting-bp | 56.2 | 53.1–59.2 | 68.0 | -11.8 | ❌ |
| foxparks-harness-br vs lamball-cattiva-bg | 29.5 | 26.8–32.4 | 41.0 | -11.5 | ❌ |
| chillet-relaxaurus-br vs shadowbeak-menasting-bp | 74.4 | 71.6–77.0 | 63.0 | +11.4 | ❌ |
| chillet-relaxaurus-bp vs foxparks-harness-br | 65.5 | 62.5–68.4 | 55.0 | +10.5 | ❌ |
| cattiva-azurobe-br vs foxparks-harness-br | 66.0 | 63.0–68.9 | 56.0 | +10.0 | ❌ |
| chillet-relaxaurus-bp vs chillet-relaxaurus-br | 42.1 | 39.1–45.2 | 52.0 | -9.9 | ❌ |
| cattiva-azurobe-br vs lamball-cattiva-bg | 42.0 | 39.0–45.1 | 51.0 | -9.0 | ❌ |
| chillet-relaxaurus-bp vs shadowbeak-menasting-bp | 71.7 | 68.8–74.4 | 64.0 | +7.7 | ❌ |
| chillet-relaxaurus-br vs lamball-cattiva-bg | 37.6 | 34.6–40.6 | 45.0 | -7.4 | ❌ |
| cattiva-azurobe-br vs chillet-relaxaurus-br | 51.1 | 48.0–54.2 | 56.0 | -4.9 | ✅ |
| foxparks-harness-br vs shadowbeak-menasting-bp | 59.1 | 56.0–62.1 | 62.0 | -2.9 | ✅ |
| cattiva-azurobe-br vs chillet-relaxaurus-bp | 58.3 | 55.2–61.3 | 56.0 | +2.3 | ✅ |

No real-world data for: cattiva-azurobe-br vs chillet-relaxaurus-bg, chillet-relaxaurus-bg vs chillet-relaxaurus-bp, chillet-relaxaurus-bg vs chillet-relaxaurus-br, chillet-relaxaurus-bg vs foxparks-harness-br, chillet-relaxaurus-bg vs lamball-cattiva-bg, chillet-relaxaurus-bg vs lamball-stone-pit-pr, chillet-relaxaurus-bg vs shadowbeak-menasting-bp
