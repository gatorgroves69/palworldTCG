# J5-optimize
Status: RUNNING
HEAD: 83596ebe49bd335df41702d21a7e15f80856b783
Start UTC: 2026-10-01T19:24:00.616228+00:00
Command: `python3 -m sim optimize --deck results/runs/cattiva_chillet+blazehowl.txt --rounds 3 --max-tries 6 --seed 51 --screen-games 400 --screen-outs 4`
End UTC: 2026-10-01T22:48:37.363611+00:00
Exit: 0

## Stdout tail
```text
optimizing cattiva_chillet+blazehowl; field weights: chillet-relaxaurus-bp 37.5%, chillet-relaxaurus-br 13.9%, lamball-stone-pit-pr 10.5%, tombat-medicine-gp 7.3%, machine-gun-furnace-br 7.0%, shadowbeak-menasting-bp 6.9%, foxparks-harness-br 5.6%, cattiva-azurobe-br 5.3%, lamball-cattiva-bg 4.5%, chillet-relaxaurus-bg 1.6%
round 1: incumbent 67.9% ± 0.8 (682s)
  screening 230 swaps x 400 games
  -2 Pump-Action Shotgun / +2 Victor's Strategy: -0.2 ± 1.3 (2421 games) -> not better (futility)
  -2 Pump-Action Shotgun / +2 Mau Cryst – Harbinger of Riches: +0.7 ± 1.0 (4035 games) -> not better (inconclusive)
  -2 Pump-Action Shotgun / +2 Elphidran – Gentle Radiance: +1.4 ± 1.0 (4035 games) -> not better (inconclusive)
  -2 Pump-Action Shotgun / +2 Celaray – Loop De Loop: +1.2 ± 1.0 (4035 games) -> not better (inconclusive)
  -2 Pump-Action Shotgun / +2 Ribbuny – Little Princess: +0.7 ± 1.0 (4035 games) -> not better (inconclusive)
  -2 Suzaku – Hellfire Wings / +2 Wumpo – Frostpeak Sentinel: -0.1 ± 1.3 (2421 games) -> not better (futility)
round 1: no swap passed; stopping
best list: /home/gator/palworldTCG/results/opt/20261001-192400/best.txt
```

Status: DONE; validated best list (RESULT: OK, no WARNING). Screening reports: 1. Source: results/opt/20261001-192400.

```text
=== best.txt
# main (50)
  4 BP01-002   Suzaku – Hellfire Wings  (pal, red, cost 7, 1200/S3, LUCKY)
  4 BP01-007   Kitsun – Wyrmbane Fangs  (pal, red, cost 5, 400/S2)
  4 BP01-008   Sparkit – Hazardous Contact  (pal, red, cost 3, 400/S1)
  2 BP01-014   Blazehowl – Hellflame Defender  (pal, red, cost 7, 1200/S3)
  4 BP01-020   Pump-Action Shotgun  (gear, red, cost 7)
  2 BP01-025   Chillet – Dragon Whisperer  (pal, blue, cost 5, 900/S2, LUCKY)
  4 BP01-028   Pengullet – Yearning for the Sky  (pal, blue, cost 4, 600/S2)
  2 BP01-029   Azurobe – Water Dragon Waltz  (pal, blue, cost 6, 1200/S2, LUCKY)
  4 BP01-032   Fuack – Manic Wave Ripper  (pal, blue, cost 2, 200/S1)
  4 TD01-004   Foxparks – A Toasty Hug  (pal, red, cost 4, 400/S2)
  4 TD01-015   Hangyu Cryst – Frigid Wanderer  (pal, blue, cost 4, 600/S2)
  4 TD01-016   Reindrix – Icy Gaze  (pal, blue, cost 5, 600/S2)
  4 TD01-023   Lamball – My First Pal  (pal, colorless, cost 2, 200/S1)
  4 TD02-023   Cattiva – My First Pal  (pal, colorless, cost 2, 200/S1)
# soul (10)
  10 SOUL-001   Soul  (soul, colorless, cost 0)
colours: {'red': 22, 'blue': 20, 'colorless': 8}   lucky: 8   names at max copies: 11
RESULT: OK
```
