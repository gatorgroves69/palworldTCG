# J1 DONE
HEAD: c1a5dba0f766ab2d9bde62c2a99ef1d810a7ee44
Start UTC: 2026-09-30T19:38:12.057446+00:00
End UTC: 2026-09-30T23:35:56.401402+00:00
Command: `python3 -m sim matrix --decks data/decks/cattiva-azurobe-br.txt data/decks/chillet-relaxaurus-bg.txt data/decks/chillet-relaxaurus-bp.txt data/decks/chillet-relaxaurus-br.txt data/decks/foxparks-harness-br.txt data/decks/lamball-cattiva-bg.txt data/decks/lamball-stone-pit-pr.txt data/decks/machine-gun-furnace-br.txt data/decks/shadowbeak-menasting-bp.txt data/decks/tombat-medicine-gp.txt --games 1000 --seed 21 --bot heuristic2 --out results/runs/J1-matrix`
Seed: 21
Exit: 0

```text
[1/45] cattiva-azurobe-br vs chillet-relaxaurus-bg
[2/45] cattiva-azurobe-br vs chillet-relaxaurus-bp
[3/45] cattiva-azurobe-br vs chillet-relaxaurus-br
[4/45] cattiva-azurobe-br vs foxparks-harness-br
[5/45] cattiva-azurobe-br vs lamball-cattiva-bg
[6/45] cattiva-azurobe-br vs lamball-stone-pit-pr
[7/45] cattiva-azurobe-br vs machine-gun-furnace-br
[8/45] cattiva-azurobe-br vs shadowbeak-menasting-bp
[9/45] cattiva-azurobe-br vs tombat-medicine-gp
[10/45] chillet-relaxaurus-bg vs chillet-relaxaurus-bp
[11/45] chillet-relaxaurus-bg vs chillet-relaxaurus-br
[12/45] chillet-relaxaurus-bg vs foxparks-harness-br
[13/45] chillet-relaxaurus-bg vs lamball-cattiva-bg
[14/45] chillet-relaxaurus-bg vs lamball-stone-pit-pr
[15/45] chillet-relaxaurus-bg vs machine-gun-furnace-br
[16/45] chillet-relaxaurus-bg vs shadowbeak-menasting-bp
[17/45] chillet-relaxaurus-bg vs tombat-medicine-gp
[18/45] chillet-relaxaurus-bp vs chillet-relaxaurus-br
[19/45] chillet-relaxaurus-bp vs foxparks-harness-br
[20/45] chillet-relaxaurus-bp vs lamball-cattiva-bg
[21/45] chillet-relaxaurus-bp vs lamball-stone-pit-pr
[22/45] chillet-relaxaurus-bp vs machine-gun-furnace-br
[23/45] chillet-relaxaurus-bp vs shadowbeak-menasting-bp
[24/45] chillet-relaxaurus-bp vs tombat-medicine-gp
[25/45] chillet-relaxaurus-br vs foxparks-harness-br
[26/45] chillet-relaxaurus-br vs lamball-cattiva-bg
[27/45] chillet-relaxaurus-br vs lamball-stone-pit-pr
[28/45] chillet-relaxaurus-br vs machine-gun-furnace-br
[29/45] chillet-relaxaurus-br vs shadowbeak-menasting-bp
[30/45] chillet-relaxaurus-br vs tombat-medicine-gp
[31/45] foxparks-harness-br vs lamball-cattiva-bg
[32/45] foxparks-harness-br vs lamball-stone-pit-pr
[33/45] foxparks-harness-br vs machine-gun-furnace-br
[34/45] foxparks-harness-br vs shadowbeak-menasting-bp
[35/45] foxparks-harness-br vs tombat-medicine-gp
[36/45] lamball-cattiva-bg vs lamball-stone-pit-pr
[37/45] lamball-cattiva-bg vs machine-gun-furnace-br
[38/45] lamball-cattiva-bg vs shadowbeak-menasting-bp
[39/45] lamball-cattiva-bg vs tombat-medicine-gp
[40/45] lamball-stone-pit-pr vs machine-gun-furnace-br
[41/45] lamball-stone-pit-pr vs shadowbeak-menasting-bp
[42/45] lamball-stone-pit-pr vs tombat-medicine-gp
[43/45] machine-gun-furnace-br vs shadowbeak-menasting-bp
[44/45] machine-gun-furnace-br vs tombat-medicine-gp
[45/45] shadowbeak-menasting-bp vs tombat-medicine-gp
# Matchup matrix (1000 games per pair, bot `heuristic2`, structures `any`)

Row deck's win rate against the column deck.

| | cattiva-azurobe-br | chillet-relaxaurus-bg | chillet-relaxaurus-bp | chillet-relaxaurus-br | foxparks-harness-br | lamball-cattiva-bg | lamball-stone-pit-pr | machine-gun-furnace-br | shadowbeak-menasting-bp | tombat-medicine-gp |
|---|---|---|---|---|---|---|---|---|---|---|
| **cattiva-azurobe-br** | — | 56 | 58 | 53 | 62 | 43 | 85 | 76 | 82 | 81 |
| **chillet-relaxaurus-bg** | 44 | — | 53 | 48 | 63 | 39 | 69 | 60 | 74 | 70 |
| **chillet-relaxaurus-bp** | 42 | 47 | — | 43 | 67 | 37 | 67 | 64 | 72 | 66 |
| **chillet-relaxaurus-br** | 47 | 52 | 57 | — | 63 | 40 | 69 | 67 | 73 | 70 |
| **foxparks-harness-br** | 38 | 37 | 33 | 37 | — | 30 | 60 | 60 | 60 | 48 |
| **lamball-cattiva-bg** | 57 | 61 | 63 | 60 | 70 | — | 84 | 76 | 80 | 82 |
| **lamball-stone-pit-pr** | 15 | 31 | 33 | 31 | 40 | 16 | — | 45 | 56 | 48 |
| **machine-gun-furnace-br** | 24 | 40 | 36 | 33 | 40 | 24 | 55 | — | 56 | 46 |
| **shadowbeak-menasting-bp** | 18 | 26 | 28 | 27 | 40 | 20 | 44 | 44 | — | 45 |
| **tombat-medicine-gp** | 19 | 30 | 34 | 30 | 52 | 18 | 52 | 54 | 55 | — |

## Calibration vs matchups_2026-09-30.json

6/36 pairs within ±5 points; mean absolute difference 11.3 points.

| Matchup | Sim | 95% CI | Real | Diff | |
|---|---|---|---|---|---|
| cattiva-azurobe-br vs lamball-stone-pit-pr | 84.7 | 82.3–86.8 | 56.0 | +28.7 | ❌ |
| lamball-cattiva-bg vs lamball-stone-pit-pr | 84.3 | 81.9–86.4 | 59.0 | +25.3 | ❌ |
| cattiva-azurobe-br vs tombat-medicine-gp | 81.0 | 78.5–83.3 | 58.0 | +23.0 | ❌ |
| chillet-relaxaurus-br vs lamball-stone-pit-pr | 69.2 | 66.3–72.0 | 47.0 | +22.2 | ❌ |
| lamball-stone-pit-pr vs machine-gun-furnace-br | 44.6 | 41.5–47.7 | 65.0 | -20.4 | ❌ |
| lamball-cattiva-bg vs machine-gun-furnace-br | 76.1 | 73.4–78.6 | 57.0 | +19.1 | ❌ |
| lamball-cattiva-bg vs tombat-medicine-gp | 82.1 | 79.6–84.4 | 64.0 | +18.1 | ❌ |
| cattiva-azurobe-br vs machine-gun-furnace-br | 76.1 | 73.4–78.6 | 60.0 | +16.1 | ❌ |
| chillet-relaxaurus-br vs tombat-medicine-gp | 70.0 | 67.1–72.8 | 56.0 | +14.0 | ❌ |
| chillet-relaxaurus-bp vs lamball-stone-pit-pr | 66.6 | 63.6–69.5 | 53.0 | +13.6 | ❌ |
| chillet-relaxaurus-br vs foxparks-harness-br | 63.4 | 60.4–66.3 | 50.0 | +13.4 | ❌ |
| chillet-relaxaurus-br vs machine-gun-furnace-br | 66.8 | 63.8–69.7 | 54.0 | +12.8 | ❌ |
| lamball-stone-pit-pr vs shadowbeak-menasting-bp | 55.5 | 52.4–58.6 | 68.0 | -12.5 | ❌ |
| lamball-stone-pit-pr vs tombat-medicine-gp | 48.5 | 45.4–51.6 | 61.0 | -12.5 | ❌ |
| chillet-relaxaurus-bp vs foxparks-harness-br | 67.4 | 64.4–70.2 | 55.0 | +12.4 | ❌ |
| chillet-relaxaurus-bp vs lamball-cattiva-bg | 37.1 | 34.2–40.1 | 49.0 | -11.9 | ❌ |
| cattiva-azurobe-br vs shadowbeak-menasting-bp | 81.8 | 79.3–84.1 | 70.0 | +11.8 | ❌ |
| foxparks-harness-br vs lamball-cattiva-bg | 30.1 | 27.3–33.0 | 41.0 | -10.9 | ❌ |
| foxparks-harness-br vs lamball-stone-pit-pr | 60.4 | 57.3–63.4 | 50.0 | +10.4 | ❌ |
| chillet-relaxaurus-br vs shadowbeak-menasting-bp | 72.7 | 69.9–75.4 | 63.0 | +9.7 | ❌ |
| machine-gun-furnace-br vs tombat-medicine-gp | 45.9 | 42.8–49.0 | 55.0 | -9.1 | ❌ |
| chillet-relaxaurus-bp vs chillet-relaxaurus-br | 43.4 | 40.4–46.5 | 52.0 | -8.6 | ❌ |
| cattiva-azurobe-br vs lamball-cattiva-bg | 42.7 | 39.7–45.8 | 51.0 | -8.3 | ❌ |
| lamball-cattiva-bg vs shadowbeak-menasting-bp | 80.3 | 77.7–82.7 | 72.0 | +8.3 | ❌ |
| chillet-relaxaurus-bp vs shadowbeak-menasting-bp | 71.9 | 69.0–74.6 | 64.0 | +7.9 | ❌ |
| chillet-relaxaurus-bp vs machine-gun-furnace-br | 63.5 | 60.5–66.4 | 56.0 | +7.5 | ❌ |
| foxparks-harness-br vs tombat-medicine-gp | 47.7 | 44.6–50.8 | 55.0 | -7.3 | ❌ |
| cattiva-azurobe-br vs foxparks-harness-br | 62.5 | 59.5–65.5 | 56.0 | +6.5 | ❌ |
| chillet-relaxaurus-bp vs tombat-medicine-gp | 66.5 | 63.5–69.4 | 60.0 | +6.5 | ❌ |
| chillet-relaxaurus-br vs lamball-cattiva-bg | 39.9 | 36.9–43.0 | 45.0 | -5.1 | ❌ |
| cattiva-azurobe-br vs chillet-relaxaurus-br | 52.7 | 49.6–55.8 | 56.0 | -3.3 | ✅ |
| cattiva-azurobe-br vs chillet-relaxaurus-bp | 58.3 | 55.2–61.3 | 56.0 | +2.3 | ✅ |
| shadowbeak-menasting-bp vs tombat-medicine-gp | 45.1 | 42.0–48.2 | 43.0 | +2.1 | ✅ |
| foxparks-harness-br vs shadowbeak-menasting-bp | 60.0 | 56.9–63.0 | 62.0 | -2.0 | ✅ |
| foxparks-harness-br vs machine-gun-furnace-br | 59.9 | 56.8–62.9 | 58.0 | +1.9 | ✅ |
| machine-gun-furnace-br vs shadowbeak-menasting-bp | 55.5 | 52.4–58.6 | 56.0 | -0.5 | ✅ |

No real-world data for: cattiva-azurobe-br vs chillet-relaxaurus-bg, chillet-relaxaurus-bg vs chillet-relaxaurus-bp, chillet-relaxaurus-bg vs chillet-relaxaurus-br, chillet-relaxaurus-bg vs foxparks-harness-br, chillet-relaxaurus-bg vs lamball-cattiva-bg, chillet-relaxaurus-bg vs lamball-stone-pit-pr, chillet-relaxaurus-bg vs machine-gun-furnace-br, chillet-relaxaurus-bg vs shadowbeak-menasting-bp, chillet-relaxaurus-bg vs tombat-medicine-gp

wrote results/runs/J1-matrix/matrix.json, matrix.md (6/36 calibrated pairs within ±5)

```
