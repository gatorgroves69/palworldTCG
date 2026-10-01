# Deck experiments

Every swap the optimizer tried, newest last. Δ = weighted gauntlet win rate (variant − incumbent), paired on the same seeds.

| When (UTC) | Run | Deck | Swap | Primary bot | Δ ± SE | z | Games | Confirm bot | Result |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-30 08:17 | 20260930-080346 | cattiva-azurobe-br | -2 Azurobe – Water Dragon Waltz / +2 Chillet – Dragon Whisperer | heuristic2 | +2.7 ± 1.0 | 2.56 | 4025 | heuristic +2.9 (z 2.5) | **KEPT** |
| 2026-09-30 08:32 | 20260930-080346 | cattiva-azurobe-br | -2 Pal Sphere / +2 Foxparks – Light of Courage | heuristic2 | +2.1 ± 1.0 | 2.02 | 4025 | — | **not better (inconclusive)** |
| 2026-09-30 08:34 | 20260930-080346 | cattiva-azurobe-br | -2 Suzaku – Hellfire Wings / +2 Foxparks – Light of Courage | heuristic2 | -6.5 ± 1.7 | -3.91 | 1610 | — | **not better (futility)** |
| 2026-09-30 08:35 | 20260930-080346 | cattiva-azurobe-br | -2 Hangyu Cryst – Frigid Wanderer / +2 Foxparks – Light of Courage | heuristic2 | -0.3 ± 1.6 | -0.20 | 1610 | — | **not better (futility)** |
| 2026-09-30 08:37 | 20260930-080346 | cattiva-azurobe-br | -2 Suzaku – Hellfire Wings / +2 Jormuntide Ignis – Savage Lava Dragon | heuristic2 | -2.5 ± 1.7 | -1.53 | 1610 | — | **not better (futility)** |
| 2026-09-30 08:38 | 20260930-080346 | cattiva-azurobe-br | -2 Pal Sphere / +2 Mounted Machine Gun | heuristic2 | -1.8 ± 1.7 | -1.07 | 1610 | — | **not better (futility)** |
| 2026-09-30 08:41 | 20260930-080346 | cattiva-azurobe-br | -2 Pal Sphere / +2 Blazehowl – Hellflame Defender | heuristic2 | -0.1 ± 1.3 | -0.08 | 2415 | — | **not better (futility)** |

**Verification of run 20260930-080346's kept swap (−2 Azurobe / +2 Chillet), 3,000 fresh games per version, seed 99:**
- **heuristic2:** 60.5% → 64.3% (+3.8). The gain comes from Chillet-BP (+5.8, 43.7% of the field) and Chillet-BR (+7.8, 16.2%), not from the unreliable Stone Pit matchup (+1.6).
- **heuristic:** 63.5% → 67.6% (+4.1). It rises against every opponent.
- **Verdict:** a robust gain under both bots. Recommended.
| 2026-10-01 00:01 | 20260930-233713 | cattiva-azurobe-br_after-chillet-swap | -2 Pump-Action Shotgun / +2 Reptyro – Ore Gorger | heuristic2 | -1.6 ± 1.6 | -1.01 | 1614 | — | **not better (futility)** |
| 2026-10-01 00:31 | 20260930-233713 | cattiva-azurobe-br_after-chillet-swap | -2 Pump-Action Shotgun / +2 Foxparks – Light of Courage | heuristic2 | +2.9 ± 1.0 | 2.90 | 4035 | heuristic +1.9 (z 1.7) | **KEPT** |
| 2026-10-01 00:57 | 20260930-233713 | cattiva-azurobe-br_after-chillet-swap | -2 Pal Sphere / +2 Reptyro – Ore Gorger | heuristic2 | -0.9 ± 1.6 | -0.55 | 1614 | — | **not better (futility)** |
| 2026-10-01 01:24 | 20260930-233713 | cattiva-azurobe-br_after-chillet-swap | -2 Pal Sphere / +2 Flambelle – Scorching Tears | heuristic2 | +1.6 ± 1.0 | 1.62 | 4035 | — | **not better (inconclusive)** |
| 2026-10-01 01:45 | 20260930-233713 | cattiva-azurobe-br_after-chillet-swap | -2 Pal Sphere / +2 Blazehowl – Hellflame Defender | heuristic2 | +2.5 ± 1.0 | 2.55 | 4035 | heuristic +3.2 (z 2.9) | **KEPT** |
| 2026-10-01 02:10 | 20260930-233713 | cattiva-azurobe-br_after-chillet-swap | -2 Pump-Action Shotgun / +2 Reptyro – Ore Gorger | heuristic2 | -3.0 ± 1.6 | -1.92 | 1614 | — | **not better (futility)** |
| 2026-10-01 02:17 | 20260930-233713 | cattiva-azurobe-br_after-chillet-swap | -2 Pump-Action Shotgun / +2 Flambelle – Scorching Tears | heuristic2 | -0.3 ± 1.6 | -0.17 | 1614 | — | **not better (futility)** |
| 2026-10-01 02:23 | 20260930-233713 | cattiva-azurobe-br_after-chillet-swap | -2 Pump-Action Shotgun / +2 Mounted Machine Gun | heuristic2 | -3.9 ± 1.6 | -2.47 | 1614 | — | **not better (futility)** |
| 2026-10-01 02:29 | 20260930-233713 | cattiva-azurobe-br_after-chillet-swap | -2 Azurobe – Water Dragon Waltz / +2 Jormuntide Ignis – Savage Lava Dragon | heuristic2 | -1.3 ± 1.6 | -0.83 | 1614 | — | **not better (futility)** |
| 2026-10-01 02:35 | 20260930-233713 | cattiva-azurobe-br_after-chillet-swap | -2 Azurobe – Water Dragon Waltz / +2 Reptyro – Ore Gorger | heuristic2 | -8.4 ± 1.6 | -5.24 | 1614 | — | **not better (futility)** |
| 2026-10-01 02:41 | 20260930-233713 | cattiva-azurobe-br_after-chillet-swap | -2 Azurobe – Water Dragon Waltz / +2 Flambelle – Scorching Tears | heuristic2 | -4.7 ± 1.6 | -2.98 | 1614 | — | **not better (futility)** |
| 2026-10-01 02:47 | 20260930-233713 | cattiva-azurobe-br_after-chillet-swap | -2 Azurobe – Water Dragon Waltz / +2 Mounted Machine Gun | heuristic2 | -8.5 ± 1.6 | -5.29 | 1614 | — | **not better (futility)** |
| 2026-10-01 02:53 | 20260930-233713 | cattiva-azurobe-br_after-chillet-swap | -2 Sparkit – Hazardous Contact / +2 Reptyro – Ore Gorger | heuristic2 | -1.6 ± 1.6 | -1.05 | 1614 | — | **not better (futility)** |

**J4: per-opponent recheck of the J2 swaps, applied one at a time to the Chillet list, 6,000 games per list (Mew, Optiplex):**
- **−2 Pal Sphere / +2 Blazehowl – Hellflame Defender:** heuristic2 +1.6 (z 2.0), heuristic +2.5 (z 3.1). The largest weighted gain is against Chillet-BP (+2.7 / +2.2). **Recommended.**
- **−2 Pump-Action Shotgun / +2 Foxparks – Light of Courage:** heuristic2 +1.6 (z 2.0), heuristic +2.4 (z 3.0). The gain comes from Chillet-BR (+4.1 / +4.7) and Stone Pit (+2.7 / +4.1), both matchups the sim misjudges; against Chillet-BP it's +0.3 / +1.6. **Not recommended for now:** Shotgun is the main tool against the engine decks the sim underrates.
