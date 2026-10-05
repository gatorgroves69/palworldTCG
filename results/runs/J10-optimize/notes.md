
## J10 line 5: DONE
HEAD: 055b0592df4a1122af8caa215c5631a1270abcde
Start UTC: 2026-10-05T06:19:09.703418+00:00
End UTC: 2026-10-05T11:04:50.199627+00:00
Command: `python3 -m sim optimize --deck results/runs/cattiva_chillet4+aqua4.txt --rounds 1 --max-tries 6 --seed 105 --screen-games 400 --screen-outs 8`
Exit: 0
Artifact verified: True

```text
optimizing cattiva_chillet4+aqua4; field weights: chillet-relaxaurus-bp 37.5%, chillet-relaxaurus-br 13.9%, lamball-stone-pit-pr 10.5%, tombat-medicine-gp 7.3%, machine-gun-furnace-br 7.0%, shadowbeak-menasting-bp 6.9%, foxparks-harness-br 5.6%, cattiva-azurobe-br 5.3%, lamball-cattiva-bg 4.5%, chillet-relaxaurus-bg 1.6%
round 1: incumbent 70.5% ± 0.8 (634s)
  screening 449 swaps x 400 games
  -2 Foxparks – A Toasty Hug / +2 Kelpsea Ignis – Balmy Magma: -0.3 ± 1.5 (1614 games) -> not better (futility)
  -2 Foxparks – A Toasty Hug / +2 Direhowl – Proud Fang: -0.3 ± 1.5 (1614 games) -> not better (futility)
  -2 Sparkit – Hazardous Contact / +2 Relaxaurus – Hungry Gunner: +0.4 ± 1.0 (4035 games) -> not better (inconclusive)
  -2 Fuack – Manic Wave Ripper / +2 Ribbuny – Little Princess: +0.8 ± 1.0 (4035 games) -> not better (inconclusive)
  -2 Pump-Action Shotgun / +2 Flambelle – Scorching Tears: +0.6 ± 1.0 (4035 games) -> not better (inconclusive)
  -2 Suzaku – Hellfire Wings / +2 Jormuntide – Surging Sea Serpent: +2.4 ± 1.0 (4035 games) -> KEPT
best list: /home/gator/palworldTCG/results/opt/20261005-061909/best.txt


Best-list validation:

=== best.txt
# main (50)
  2 BP01-002   Suzaku – Hellfire Wings  (pal, red, cost 7, 1200/S3, LUCKY)
  4 BP01-007   Kitsun – Wyrmbane Fangs  (pal, red, cost 5, 400/S2)
  4 BP01-008   Sparkit – Hazardous Contact  (pal, red, cost 3, 400/S1)
  2 BP01-014   Blazehowl – Hellflame Defender  (pal, red, cost 7, 1200/S3)
  4 BP01-020   Pump-Action Shotgun  (gear, red, cost 7)
  4 BP01-025   Chillet – Dragon Whisperer  (pal, blue, cost 5, 900/S2, LUCKY)
  2 BP01-027   Jormuntide – Surging Sea Serpent  (pal, blue, cost 8, 1600/S3, LUCKY)
  4 BP01-028   Pengullet – Yearning for the Sky  (pal, blue, cost 4, 600/S2)
  4 BP01-032   Fuack – Manic Wave Ripper  (pal, blue, cost 2, 200/S1)
  4 TD01-004   Foxparks – A Toasty Hug  (pal, red, cost 4, 400/S2)
  4 TD01-012   Elphidran Aqua – Gentle Ripples  (pal, blue, cost 6, 900/S2)
  4 TD01-016   Reindrix – Icy Gaze  (pal, blue, cost 5, 600/S2)
  4 TD01-023   Lamball – My First Pal  (pal, colorless, cost 2, 200/S1)
  4 TD02-023   Cattiva – My First Pal  (pal, colorless, cost 2, 200/S1)
# soul (10)
  10 SOUL-001   Soul  (soul, colorless, cost 0)
colours: {'red': 20, 'blue': 22, 'colorless': 8}   lucky: 8   names at max copies: 11
RESULT: OK

Optimizer verdict: KEPT -2 Suzaku – Hellfire Wings / +2 Jormuntide – Surging Sea Serpent

```
