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
| 2026-10-01 21:10 | 20261001-192400 | cattiva_chillet+blazehowl | -2 Pump-Action Shotgun / +2 Victor's Strategy | heuristic2 | -0.2 ± 1.3 | -0.17 | 2421 | — | **not better (futility)** |
| 2026-10-01 21:37 | 20261001-192400 | cattiva_chillet+blazehowl | -2 Pump-Action Shotgun / +2 Mau Cryst – Harbinger of Riches | heuristic2 | +0.7 ± 1.0 | 0.69 | 4035 | — | **not better (inconclusive)** |
| 2026-10-01 21:57 | 20261001-192400 | cattiva_chillet+blazehowl | -2 Pump-Action Shotgun / +2 Elphidran – Gentle Radiance | heuristic2 | +1.4 ± 1.0 | 1.35 | 4035 | — | **not better (inconclusive)** |
| 2026-10-01 22:17 | 20261001-192400 | cattiva_chillet+blazehowl | -2 Pump-Action Shotgun / +2 Celaray – Loop De Loop | heuristic2 | +1.2 ± 1.0 | 1.15 | 4035 | — | **not better (inconclusive)** |
| 2026-10-01 22:36 | 20261001-192400 | cattiva_chillet+blazehowl | -2 Pump-Action Shotgun / +2 Ribbuny – Little Princess | heuristic2 | +0.7 ± 1.0 | 0.72 | 4035 | — | **not better (inconclusive)** |
| 2026-10-01 22:48 | 20261001-192400 | cattiva_chillet+blazehowl | -2 Suzaku – Hellfire Wings / +2 Wumpo – Frostpeak Sentinel | heuristic2 | -0.1 ± 1.3 | -0.05 | 2421 | — | **not better (futility)** |

**J5 review (wide search from `cattiva_chillet+blazehowl`, Mew, Optiplex):**
- Screening covered all 230 sensible 2-copy swaps (the 4 weakest cards × every implemented red/blue/colorless card), 400 games each with `heuristic`. The top 6 went on to the sequential test with `heuristic2`, and **none passed**. The best was +1.4 ± 1.0, inconclusive.
- The run stopped after round 1, so the list is unchanged. J5 gauntlet: 68.2% (67.6–68.9) against the field.
- Pattern: almost every top-screened swap removes 2 Pump-Action Shotguns, but no replacement measurably beats them. That agrees with J4: in the sim the 3rd and 4th Shotguns are worth about the same as a generic card, and the sim underrates Shotgun against real engine decks. **Keep 4.**
- Conclusion: within 2-copy swaps, the current list is at the best the sim can find. Further gains would need bot improvements (engine decks), 1-copy fine-tuning, or a meta shift.

**Real-world research leads (palworldtcg.gg Cattiva · Azurobe page, 30 days, 7,198 games, read 2026-10-02).** Card usage shows "win rate when drawn minus never drawn". Almost every card is negative, because long games favor drawing more, so compare cards against each other:
- **Chillet** (Tech) is the best on the page at **+5.4**, which supports the Chillet swap.
- **Pal Sphere** is **−6.6**, the worst of the regular cards, which supports cutting it.
- **Hangyu Cryst** is **−6.3**, and fewer than half of lists play it. Our optimizer never tested removing it.
- Blazehowl is −5.6, but it's a Tech card with an unknown (likely small) sample, and the page doesn't say which Blazehowl.
- Elphidran (61.3% of lists that include it) and Relaxaurus (61.2%) appear in winning Cattiva lists. Both are Dragons that Chillet can deploy.

These lead to job J6: four variants, each compared head-to-head with the current list.

**J6 review (head-to-head vs `cattiva_chillet+blazehowl`, 6,000 games per list, both bots, Mew, Optiplex, `d3bcd84`):**
- **A: −2 Azurobe / +2 Chillet (4 Chillet, 0 Azurobe):** heuristic2 **+2.2 (z 2.7)**, heuristic **+1.8 (z 2.3)**. Gains in 9 of 10 matchups under heuristic2, including Chillet-BP (+2.2 / +2.7), the biggest slice of the field. This is the second time "more Chillet, less Azurobe" won (first: +3.8 / +4.1), and the real-world data agrees (Chillet +5.4, the best card on the deck page). **Adopted:** new list `results/runs/cattiva_chillet4+blazehowl.txt`.
- **B: −2 Hangyu / +2 Elphidran:** +0.1 / +0.3. No difference.
- **C: −2 Hangyu / +2 Relaxaurus:** −0.8 / −0.0. No difference (slightly worse).
- **D: −4 Hangyu / +2 Elphidran +2 Relaxaurus:** −0.3 / +0.6. No difference.
- **E: −2 Hangyu / +2 Aurora Guide:** **−2.4 (z −2.9) / −1.6 (z −2.0)**. Worse under both bots. (Ran with the old bot; J7-E2 re-tests it with Dragon stacking.)
- Takeaway: Hangyu Cryst's slot is replaceable by Dragons at no cost, but no Dragon there is a gain. Keep Hangyu unless J7 finds something.
