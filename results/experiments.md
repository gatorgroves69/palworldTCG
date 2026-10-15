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

**J7 review (head-to-head vs `cattiva_chillet+blazehowl`, 6,000 games per list, both bots, new defensive Quick logic, Mew, Optiplex, `3786c9b`):**
- **F: −2 Hangyu / +2 Crystal Breath:** −1.6 (z −1.9) / −0.9. Not better.
- **G: −2 Hangyu / +2 Ignis Breath:** −0.8 / −0.1. Neutral.
- **H: −2 Hangyu / +2 Elphidran Aqua:** **+1.2 (z 1.5) / +0.9 (z 1.2)**. Positive under both bots, about z 1.9 pooled. Not significant yet, so it's re-tested on the 4-Chillet list in J8.
- **I: −4 Hangyu / +2 Penking +2 Pengullet Rocket Launcher:** **−5.7 (z −6.8) / −5.4 (z −6.7)**. Clearly worse: the deck is too slow to set it up.
- **E2: −2 Hangyu / +2 Aurora Guide (Dragon stacking):** −1.0 / −1.7 (z −2.2). Still worse; Aurora is rejected.
- **Z: 4 Foxparks – Light of Courage instead of 4 A Toasty Hug:** −0.4 / −2.3 (z −2.8). Playing the wrong Foxparks cost roughly 1–2 points.

**Bot fix before J8:** the bot forgot cards it had put on top of its own deck when it planned (see docs/assumptions.md S5), which undersold Aurora Guide and Elphidran Aqua. J8 re-tests both on the 4-Chillet list with the fix, 12,000 games per list per bot.

**J8 review (head-to-head vs `cattiva_chillet4+blazehowl`, 12,000 games per list, both bots, fixed top-card memory, Mew, Optiplex, `3f0e713`):**
- **H: −2 Hangyu / +2 Elphidran Aqua:** heuristic2 **+1.1 (z 1.9)**, heuristic **+0.9 (z 1.6)**. On its own, J8 narrowly misses the "both significant" bar. But this is the 4th independent run, all positive and about the same size: J7 gave +1.2 / +0.9 on the 2-Chillet list. Pooled across all four runs (inverse-variance), it's **+1.0 ± 0.3, z ≈ 3.1**. **Adopted as a small edge:** new list `results/runs/cattiva_chillet4+aqua.txt`. The worst case looks like "no difference".
- **E3: −2 Hangyu / +2 Aurora Guide:** **−2.0 (z −3.3) / −1.3 (z −2.4)**. Worse again, even with the fixed bot. That's 3 losing tests (E, E2, E3): **Aurora Guide is rejected for this deck.**
| 2026-10-04 10:54 | 20261004-091514 | cattiva_chillet4+aqua | -2 Suzaku – Hellfire Wings / +2 Blazamut – Molten Sovereign | heuristic2 | -0.6 ± 1.6 | -0.36 | 1614 | — | **not better (futility)** |
| 2026-10-04 11:02 | 20261004-091514 | cattiva_chillet4+aqua | -2 Blazehowl – Hellflame Defender / +2 Reptyro – Ore Gorger | heuristic2 | -4.0 ± 1.6 | -2.52 | 1614 | — | **not better (futility)** |
| 2026-10-04 11:33 | 20261004-091514 | cattiva_chillet4+aqua | -2 Pump-Action Shotgun / +2 Surfent – Swift Swimmer | heuristic2 | +0.8 ± 1.0 | 0.81 | 4035 | — | **not better (inconclusive)** |
| 2026-10-04 11:41 | 20261004-091514 | cattiva_chillet4+aqua | -2 Blazehowl – Hellflame Defender / +2 Cryolinx – Arctic Ordeal | heuristic2 | -1.6 ± 1.6 | -1.04 | 1614 | — | **not better (futility)** |
| 2026-10-04 11:48 | 20261004-091514 | cattiva_chillet4+aqua | -2 Sparkit – Hazardous Contact / +2 Kelpsea Ignis – Balmy Magma | heuristic2 | -1.1 ± 1.6 | -0.69 | 1614 | — | **not better (futility)** |
| 2026-10-04 11:56 | 20261004-091514 | cattiva_chillet4+aqua | -2 Sparkit – Hazardous Contact / +2 Direhowl – Proud Fang | heuristic2 | -1.1 ± 1.6 | -0.69 | 1614 | — | **not better (futility)** |

**J9 review (vs `cattiva_chillet4+aqua`, 12,000 games per list, both bots, Mew, Optiplex, `3a3055f`):**
- **A: −2 Hangyu / +2 Elphidran Aqua (4 Aqua, 0 Hangyu):** heuristic2 **+0.9 (z 1.6)**, heuristic **+0.9 (z 1.8)**. Pooled: **+0.9 ± 0.4, z ≈ 2.4**. It's the same pattern as the first 2 Aqua: small, consistent and positive under both bots. **Adopted:** new list `results/runs/cattiva_chillet4+aqua4.txt`.
- **B: −2 Hangyu / +2 Elphidran – Gentle Radiance:** +0.5 (z 0.8) / +0.5 (z 1.0). Not distinguishable from zero, and smaller than A. Not adopted.
- **Optimizer (line 5) from `cattiva_chillet4+aqua`:** incumbent 70.3% ± 0.8. Screened 233 swaps × 400 games, and the top 6 went to the sequential test. **None passed.** The best was −2 Shotgun / +2 Surfent at +0.8 ± 1.0, inconclusive; the rest stopped for futility. The run completed (exit 0). Mew's notes say "FAILED" only because its own output-verification check didn't match the printed `best list:` path; the optimizer itself didn't fail.
| 2026-10-05 09:13 | 20261005-061909 | cattiva_chillet4+aqua4 | -2 Foxparks – A Toasty Hug / +2 Kelpsea Ignis – Balmy Magma | heuristic2 | -0.3 ± 1.5 | -0.21 | 1614 | — | **not better (futility)** |
| 2026-10-05 09:21 | 20261005-061909 | cattiva_chillet4+aqua4 | -2 Foxparks – A Toasty Hug / +2 Direhowl – Proud Fang | heuristic2 | -0.3 ± 1.5 | -0.21 | 1614 | — | **not better (futility)** |
| 2026-10-05 09:53 | 20261005-061909 | cattiva_chillet4+aqua4 | -2 Sparkit – Hazardous Contact / +2 Relaxaurus – Hungry Gunner | heuristic2 | +0.4 ± 1.0 | 0.40 | 4035 | — | **not better (inconclusive)** |
| 2026-10-05 10:14 | 20261005-061909 | cattiva_chillet4+aqua4 | -2 Fuack – Manic Wave Ripper / +2 Ribbuny – Little Princess | heuristic2 | +0.8 ± 1.0 | 0.82 | 4035 | — | **not better (inconclusive)** |
| 2026-10-05 10:37 | 20261005-061909 | cattiva_chillet4+aqua4 | -2 Pump-Action Shotgun / +2 Flambelle – Scorching Tears | heuristic2 | +0.6 ± 1.0 | 0.65 | 4035 | — | **not better (inconclusive)** |
| 2026-10-05 11:04 | 20261005-061909 | cattiva_chillet4+aqua4 | -2 Suzaku – Hellfire Wings / +2 Jormuntide – Surging Sea Serpent | heuristic2 | +2.4 ± 1.0 | 2.53 | 4035 | heuristic +1.9 (z 1.8) | **KEPT** |

**J10 review (vs `cattiva_chillet4+aqua4`, 12,000 games per list, both bots, bot stacks for Chillet only when one can follow, Mew, Optiplex, `350a3b0`):**
- **A: −2 Suzaku / +2 Jormuntide – Surging Sea Serpent:** heuristic2 **+1.1 (z 1.9)**, heuristic **+1.4 (z 2.6)**. The J10 optimizer found and **KEPT the same swap independently** (+2.4 ± 1.0, sequential test), from 449 screened swaps. Three runs agree. **Adopted:** new list `results/runs/cattiva_dragons.txt` (= `J10-A_jormuntide.txt`).
- **B: −2 Blazehowl / +2 Relaxaurus:** −1.4 (z −2.4) / −0.9. Worse.
- **Optimizer:** 8 removal candidates. The other top-6 swaps were inconclusive or futile: Foxparks → Kelpsea Ignis or Direhowl, Sparkit → Relaxaurus, Fuack → Ribbuny, Shotgun → Flambelle.
- Note: Mew refreshed the tiers on 2026-10-05 (`1196995`), so field weights moved slightly (Chillet-BP 37.5 → 38.5%, Stone Pit 10.5 → 12.2%). J11 and later runs use the new weights.

**J11 review (SS01 cards and the Aurora re-test, vs `cattiva_dragons` = `J10-A_jormuntide`, 12,000 games per list, both bots, Mew, Optiplex, `011f728`):**
- **Q: −2 Suzaku / +2 Quivern:** heuristic2 **+1.3 (z 2.4)**, heuristic +0.3 (z 0.6). The bots disagree. Pooled it's +0.7 ± 0.4 (z ≈ 1.9), so **not proven**. The gain comes from the small-Pal decks (Cattiva mirror +6.7 / +4.7, Lamball·Cattiva, Machine Gun, Shadowbeak). Against Chillet-BP, 38.5% of the field, it's flat (+0.2 / −0.1). Confirmation run proposed as J12.
- **G: −2 Blazehowl / +2 Grizzbolt:** **−1.4 (z −2.4) / −2.2 (z −4.1)**. Worse.
- **I: −2 Blazehowl / +2 Chillet – Finishing Ice Blade:** **−1.5 (z −2.7) / −1.8 (z −3.4)**. Worse. Blazehowl's Interrupt mode keeps proving its worth.
- **C: −2 Sparkit / +2 Cattiva – Brimming with Confidence:** −0.1 / −0.0. No difference.
- **A: −2 Sparkit / +2 Aurora Guide (Jormuntide as a stack target):** −0.6 / **−1.3 (z −2.5)**. Fourth loss. **Aurora Guide is closed for this deck.**

**J12 review (Quivern confirmation, fresh seeds, 20,000 games per list, `326a7d7`):**
- **−2 Suzaku / +2 Quivern:** heuristic2 **+1.6 (z 3.7)**, heuristic +0.5 (z 1.3). All 4 Quivern runs (J11 + J12) are positive. Pooled (inverse-variance) it's **+0.9 ± 0.23, z ≈ 4**. The default bot `heuristic2`, which plans an attack and its trigger together, sees it as clearly better. The one-step bot sees a smaller gain. The gain is broad (Chillet-BP +1.2 / +0.3) and largest in the small-Pal matchups (Cattiva mirror +7.0 / +4.5). **Adopted:** new list `results/runs/cattiva_dragons_quivern.txt`. All 8 lucky cards are now Dragons (4 Chillet, 2 Jormuntide, 2 Quivern), and there's no Suzaku.

**J13 review (answers to big late-game Pals, vs `cattiva_dragons_quivern`, 12,000 games per list, both bots, `f68f098`):**
- **X: −2 Sparkit / +2 Axel's Strategy:** −0.2 / +0.2. No difference overall. It's slightly positive against Chillet-BR and negative against Lamball·Cattiva.
- **R: −2 Sparkit / +2 Single-Shot Rifle:** −0.3 / **−1.5 (z −2.7)**. Worse.
- Reading: in the sim, the late game against big Pals isn't what decides most games, and Sparkit's cheap body plus 500 to a standing Pal is worth as much as a 1500 single-target removal. Caveat: Bobby's real losses came from an engine deck (GP Shadowbeak), which the sim plays too weakly (docs/m2-status.md), so these tests can't price a card's value against real engine decks. Axel's Strategy stays a reasonable personal tech choice if a local meta is full of engine decks.

**J16 review (Cup list `cattiva_dragons`, no SS01; 12,000 games per list, both bots, `2e5a682`):**
- **A: −2 Suzaku / +2 Jormuntide Ignis:** **−2.3 (z −4.0) / −2.3 (z −4.2)**. Worse. Third rejection of Ignis, now on the 12-Dragon list.
- **B: −2 Jormuntide Surging / +2 Jormuntide Ignis:** **−2.9 (z −5.1) / −2.7 (z −5.0)**. Worse. Surging (draw + lock) beats Ignis (re-stand) in this deck.
- **C: −2 Reindrix / +2 Crystal Breath:** **−1.9 (z −3.4) / −2.2 (z −4.1)**. Worse. The Interrupt is better than the Quick lock.
- **D: −2 Sparkit / +2 Crystal Breath:** −0.5 / −0.7. Not better.
- Caveat: these ran before the defensive expected-damage fix (the bot values a Strike-S hit as S×(1−p) rather than S×(1−p)^S, and uses a fixed p). Both lists in each comparison use the same bot, so the direction is reliable; the size of C and D could shift a little once Crystal Breath is cast with correct odds.

**J17 review (Cup list `cattiva_dragons`, `831a439`):**
- **Part 1, defence policy for the deck under test** (12,000 games each, seed 171, paired; opponents = legacy default heuristic2):

  | Deck bot | Win vs field | vs legacy |
  |---|---|---|
  | legacy (current default) | 71.9% | — |
  | **exact odds, x1.0** | **73.6%** | **+1.7 (z ≈ 2.8)** |
  | exact odds, x1.5 (stingier) | 72.7% | +0.8 |
  | legacy, x1.5 (stingier) | 73.0% | +1.1 |
  | exact odds, x0.65 (trigger-happy) | 71.1% | −0.8 |

  Reading: for this deck, valuing hits by the real odds and Interrupting only when the expected loss is worth about one card wins the most. Defending more eagerly than that loses. Both "stingier" settings also beat the legacy default. Caveat: the opponents are the uncalibrated legacy bots (see S5, J17), so this measures the best policy against bot-like opponents; real players defend more and may punish a passive defender differently. Not adopted as the default (M1 calibration, S5); recorded as the evidence behind the pocket guide's rule 1.
- **Part 2** (12,000 games per list, both bots, legacy default):
  - K1: −2 Kitsun / +2 Crystal Breath: **−2.3 (z −4.0) / −1.7 (z −3.2)**. Worse.
  - K2: −2 Kitsun / +2 Axel's Strategy: **−1.9 (z −3.4) / −1.3 (z −2.4)**. Worse. Kitsun stays at 4.
  - S1: −2 Sparkit / +2 Crystal Breath: −0.4 / −0.4. Not better; third and final Crystal Breath test. **Closed.**

**J18 review (Mew's own Cup-only micro-swaps, Bobby-approved by Telegram; vs `cattiva_dragons`, 12,000 games per list, both bots, `e111745`):**
- **V: −1 Sparkit / +1 Victor's Strategy:** −0.1 / −0.0. No difference. A 1-card change is below what 12,000 games can resolve (±0.6), so "flat" is the expected reading either way; the bounce mode didn't show up as a gain.
- **H: −2 Sparkit / +2 Makeshift Handgun:** −0.8 / **−1.2 (z −2.3)**. Not better. 500 for 2 souls loses to Sparkit's body + 500 on a standing Pal.
- Process: clean. Mew wrote its own spec, kept to its owned paths, used the Cup list as the baseline and ran the exact lines. Nothing adopted.

**gf deck candidates (Mac, 2,000 games each, bot `heuristic`, vs the Cup list `cattiva_dragons`, 2026-10-09):**
- Meta Tombat·Medicine (GP Shadowbeak): Bobby wins **87.6%** (real data says 58%; the sim misplays engine decks).
- Meta Shadowbeak·Menasting (BP): Bobby wins 90.1% (real 70%).
- **Green/Purple Nocturnal** (a list Bobby was shown: Stone Blast, Dinossom, Elphidran Radiance, Lamp, Medicine Workbench, Tombat, Blazehowl Noct, Maraith, Quivern, Lyleen, Pyrin Noct ×4 each; Wumpo Botan ×2; Warsect ×4): Bobby wins **59.5%** (GP 44.4% going first, 36.6% second). The sim handles this deck better than the Shadowbeak lists: its plan is 14 Interrupts, Taunt walls and night pumps, not a multi-turn engine. New cards for it: Warsect, Wumpo Botan, Stone Blast (`cards/bp01_green.py`, `cards/td02.py`); the bot casts Stone Blast in the Quick step when it saves a Pal or kills the attacker.
- Same list with **4 Astegon for 4 Quivern** (no SS01): Bobby wins 65.8%. Quivern is worth about 6 points to it.

**J19 review (Cup list, Mew, `ceea7c7`, pre-race-term bot):** −2 Sparkit / +2 Axel's Strategy: −0.2 / −0.7 (z −0.4 / −1.4). Flat, as in J13. Gauntlet re-baseline on that code: Cup list 72.6%, Axel's list 72.7%.

**J19b review (Cup list, Mew, `9d208a2`+, race-term bot):** **−4 Sparkit / +2 Axel's Strategy +2 Single-Shot Rifle: +2.3 (z 4.0) / +2.3 (z 3.9).** Significant under both bots. Gains where the field is: Chillet-BP +3.6 / +4.2 (38.5% of the field), Chillet-BR +5.7 / +7.3, Foxparks·Harness +2.8 / +6.4, Shadowbeak +2.0 / +4.5. Losses against small-Pal decks: Lamball·Cattiva −5.4 / −9.8, mirror −2.1 / −5.8, Tombat −2 / −3. Reading: with defenders that now hold blockers (race term), uninterruptible 1500 single-target removal (Rifle, Axel's) is worth more than Sparkit's 500-to-a-standing-Pal body, and both answer a 1300 Shadowbeak and big blockers. Note the race term lowered the Cup list's field number from 72.6% to 66.1%: opponents defend now. **Recommended, pending a fresh-seed confirmation (J21).** Candidate list: `results/runs/cattiva_dragons_v2.txt` (= J19-P).

**J20 mirrors review (10 mirrors, 1,000 games each, `heuristic3` vs `heuristic2`, seed 201):** heuristic3 wins 53.2 / 53.1 / 50.9 / 53.9 / 54.8 / 53.8 / 55.4 / 52.5 / 47.9 / 53.8 (Cattiva·Azurobe, Chillet-BP, -BR, -BG, Foxparks·Harness, Lamball·Cattiva, Stone Pit, Machine Gun, Shadowbeak, Tombat). Mean **52.9%**, pooled z ≈ 5.8; the Shadowbeak mirror (47.9) is within one 1,000-game noise band of 50. Reading: depth-3 beam search is a real but small edge (about 3 points) over the default, and it doesn't fix the engine-deck gap (Shadowbeak is the one mirror it doesn't win). Not adopted as the default: J16–J21 were all run on heuristic2, and the gain is below the deck-swap effects we're measuring. Kept as an opt-in third opinion (`--bot heuristic3`).

**J21 review (Cup list `cattiva_dragons`, Mew, sequential compares, race-term bot, seeds 211–222):**
- **v2 confirmed: −4 Sparkit / +2 Axel's Strategy +2 Single-Shot Rifle: +2.6 (z 2.5, 4,000 games) / +4.2 (z 2.9, 2,000 games).** Fresh seeds, both bots, same direction as J19b (+2.3 / +2.3, z 4). Pooled over J19b+J21: about +2.7 under heuristic2 and +2.9 under heuristic. Gains again where the field is: Chillet-BP +3.0 / +5.1, Chillet-BR +4.6 / +6.6, Foxparks·Harness +3.7 / +9.8, Shadowbeak +2.5 / +3.4, Machine Gun +2.1 / +7.4. Losses only against the mirror (−3.4 / −5.8) and nothing clear elsewhere. **Adopted. Bobby's list is now `results/runs/cattiva_dragons_v2.txt`** (plain copy `cattiva_dragons_v2.export.txt`). `cattiva_dragons.txt` stays as the J22 baseline and the 8-Sparkit fallback.
- **Suzaku slot: every replacement loses, under both bots.** A: −2 Suzaku +2 Rifle (6 lucky): **−5.6 (z −3.8) / −7.2 (z −4.9)**. B: −2 Suzaku −2 Sparkit +2 Rifle +2 Axel's (6 lucky): **−5.0 (z −4.8) / −4.0 (z −3.8)**. D: −2 Suzaku +2 Blazehowl (4 Blazehowl, 6 lucky): **−5.7 (z −3.8) / −5.4 (z −3.7)**. G: −2 Suzaku +2 Wumpo: **−2.2 (z −3.0) / −2.2 (z −2.6)**. F: −2 Suzaku +2 Bushi: **−5.0 (z −3.4) / −6.3 (z −4.3)**.
- Reading: the three 6-lucky builds lose 4–7 points each, so the 7th and 8th lucky cards are worth about 2–3 points apiece in this deck; the "opponents assume 8" mind-game can't be worth that. Suzaku is weak as a card (draw impact −1.3) but it's the right 8th lucky: both 8-lucky replacements (Wumpo, Bushi) also lose, Wumpo least. The Suzaku slot is **closed** for BP01; the only thing that has beaten it is Quivern (SS01, not Cup-legal).
- Sequential stopping worked: 10 of 12 lines stopped at 2,000–4,000 games, the Wumpo lines ran to 6,000–8,000 because the effect was small. J21 took 4.5 hours instead of about 12.

**Real games with v2 (Bobby, online, 2026-10-12): 0–5.** Opponents: GP Shadowbeak, Chillet·Relaxaurus BR, GP Tombat·Medicine, red Ignis/Blazamut Machine Gun, Chillet·Relaxaurus BP. Axel's Strategy was never cast in the five logs: it was discarded or held until discarded, including one turn where Axel's + Suzaku (1700) would have killed the Jormuntide that then took 4 of Bobby's Pals. Single-Shot Rifle was cast and used well. Recurring play patterns, which aren't about the list: paying 3 souls to draw with an empty or one-Pal board, attacking with every Pal so the rested Pals get picked off, and unused blocks or Interrupts at low life. Reading: the sim's v2 gain assumes Axel's is played well; in Bobby's hands it has been a blank card so far. Recommended Bobby return to the Cup list (`cattiva_dragons.txt`) while the habits settle.

## J22 original attempt — input-refresh caveat; frozen retry pending
The following observed rows are preserved, not certified as a consistent-input search. See `runs/J22-optimize/input-reconciliation.md`.

| When | Run | Deck | Swap | Bot | Diff | z | Games | Confirmation | Result |
|---|---|---|---|---|---|---|---|---|---|
| 2026-10-12 23:55 | 20261012-135254 | cattiva_dragons | -2 Cattiva – My First Pal / +2 Reptyro Cryst – Glacial Devourer | heuristic2 | -0.5 ± 1.6 | -0.30 | 1614 | — | **not better (futility)** |
| 2026-10-13 00:12 | 20261012-135254 | cattiva_dragons | -2 Lamball – My First Pal / +2 Reptyro Cryst – Glacial Devourer | heuristic2 | -0.9 ± 1.6 | -0.54 | 1614 | — | **not better (futility)** |
| 2026-10-13 01:11 | 20261012-135254 | cattiva_dragons | -2 Blazehowl – Hellflame Defender / +2 Relaxaurus – Hungry Gunner | heuristic2 | +1.6 ± 1.0 | 1.60 | 4035 | — | **not better (inconclusive)** |
| 2026-10-13 01:26 | 20261012-135254 | cattiva_dragons | -2 Reindrix – Icy Gaze / +2 Flambelle – Feverish Tears | heuristic2 | -2.1 ± 1.6 | -1.27 | 1614 | — | **not better (futility)** |
| 2026-10-13 01:42 | 20261012-135254 | cattiva_dragons | -2 Elphidran Aqua – Gentle Ripples / +2 Jolthog – Shocking Yet Innocent | heuristic2 | -1.5 ± 1.6 | -0.93 | 1614 | — | **not better (futility)** |
| 2026-10-13 02:24 | 20261012-135254 | cattiva_dragons | -2 Sparkit – Hazardous Contact / +2 Axel's Strategy | heuristic2 | +2.9 ± 1.0 | 2.83 | 4035 | heuristic +1.1 (z 0.9) | **rejected (confirmation bot disagrees)** |

**J22 attempt-1 review (Claude, provisional; Mew's frozen retry pending):** 955 swaps screened at 400 games (noise about ±4), top 6 sequentially tested, none accepted, so the Cup list held. The screen's top two (Reptyro Cryst for Cattiva or Lamball, +5.8 / +5.7) were noise: −0.5 and −0.9 on the full test. Closest: −2 Sparkit +2 Axel's +2.9 (z 2.8) under heuristic2, confirmation +1.1, which agrees with the v2 direction (J19b, J21). −2 Blazehowl +2 Relaxaurus +1.6, inconclusive. 4 Jormuntide (−2 Suzaku) screened +0.5: no signal at 400 games. Spec flaw (mine): the candidate pool included SS01 and BP02 preview cards, which aren't Cup-legal (113 screen rows; Flambelle – Feverish Tears made the final six and lost). Mew's input audit: the October 12 refresh changed only names/subtitles, BP02-099's colour and Chillet Ignis's wording, and touched only screening candidates with SS01/BP02 cards. The verdict "nothing beats the list" is very unlikely to change on a frozen rerun.

**Palify top-50 calibration, first pass (Claude, 2026-10-13; data: Mew's `data/replays/palify_ranked_2026-10-13`, 230 usable games; script `python3 -m analysis.palify_calibration`):**
- Real results: Lamball·Stone Pit wins 72.5% of its 69 deck-games (8/9 in top-vs-top games, 6+ different pilots) and goes ~even with Chillet BP head-to-head (13/27). The sim had Chillet BP over Stone Pit 61–67%. Going first: 42.6% overall, but aggro decks win going first (Stone Pit 71%, Cattiva·Azurobe 9/10); Chillet/control decks prefer second. Keep "go first" for Bobby.
- Top-50 lists differ from our reference lists (Stone Pit: ~4 Machine Gun, 4 Leezpunk, few Rifles; Chillet BP: 3 Relaxaurus, 3 Astegon, Lyleen Noct). Consensus lists: `results/runs/palify_consensus/`.
- Real defence vs bots: face hits Interrupted 17/26/39% at 7–10/4–6/1–3 life (bots ~20% flat); Pal attacks Interrupted 36% (bots 21%); blocks 0.47/game (bots 1.35); soul draws 3.9/game (bots 2.7). New opt-in `@human` profile (life-weighted Interrupts, Pal protection, fewer blocks): matches high/mid-life Interrupt rates; still short at low life and still blocks too much. Calibration effect: Cattiva vs Chillet BP 56.3% (real 55), Chillet BP vs Stone Pit 57.9% (default 60.7; real 48–53). Small, right direction.
- Main gap found: real Stone Pit pilots activate Stone Pit 3.7×/game (each copy ~3×); the bot ~0.8×, because it attacks with every Pal and has none left to assign. Opt-in `@engineK` (Material/Ingredient worth K×) raises it only to 1.05 (K=2) / 1.27 (K=3), and Bobby v2 vs consensus Stone Pit stays 84–85% (real ~56). Not fixed: the fix needs "assign before attacking" sequencing, not values. Real players also Interrupt 44% of attacks on their structures. Neither option is a default; nothing that Mew runs changes.
- Housekeeping: BP02-004 renamed Chillet Ignis – Ember-Clad Dragon in the 2026-10-12 refresh; implementation text synced (same effect). 317 tests pass.

**J23 review (on v2 `cattiva_dragons_v2`, Mew, sequential, seeds 241–246):**
- **A: −2 Suzaku +2 Jormuntide Surging (4 Jormuntide, 12 Dragons, 8 lucky): +1.3 (z 2.2, ran to the 12,000 cap) / +2.0 (z 2.8).** Both bots positive; pooled about +1.6, z ≈ 3.5. Gains mostly against Chillet BP (+1.3 / +1.2, 39% of the field) and Stone Pit (+0.4 / +1.7); small loss to Shadowbeak (−2.2 / −1.0). Unlike the five J21 Suzaku replacements, this keeps 8 lucky cards and adds Dragons for Chillet. **Recommended: `results/runs/cattiva_dragons_v3.txt`** (plain copy `cattiva_dragons_v3.export.txt`); v2 stays the fallback if Bobby doesn't have 4 Jormuntide. Real-play caveat: Suzaku's 900 deploy and its +200 to Rifle/Axel's/Kitsun/Shotgun are gone, and the deck now has four 8-cost Pals.
- B: −2 Blazehowl +2 Relaxaurus: +0.2 / +0.3, no difference. C: 4 Axel's, 0 Rifle: +0.5 / −0.1, no difference. Both closed.

**J20 matrix review (seed 202, heuristic2, pinned original inputs):** 12/36 pairs within ±5 of real, mean absolute difference 9.0 points (M2 was 12.0), so the race term helped calibration overall. The engine-deck pairs remain the big misses; see the Palify calibration notes for the Stone Pit diagnosis.

**Stone Pit sequencing and engine play (Claude, 2026-10-13; consensus top-50 Stone Pit list vs Bobby's v2, 300-game checks, Mac):**
- New opt-in bot options (defaults unchanged): `@seq` runs engine structures that assign a Pal (Stone Pit, Furnace, Ranch, Machine Gun, Medicine Workbench, …) before attacking or ending the turn, unless the attacks are lethal, and prunes duplicate assign/X activations (fixes 30-second Stone Pit games); `@human` now also values on-death payoffs (Leezpunk, Menasting, Pengullet), keeps a soul open for Interrupts by life, draws with souls more eagerly, and values a structure under attack by `structure_value`; `@bold` (exposure 0.85/0.95) is an experiment.
- Stone Pit behaviour per turn now matches the Palify top-50: Stone Pit activations 0.38/turn (real 0.39), Interrupts 0.43/turn (real 0.43), Furnace 3.9/game (real 3.9), Machine Gun 1.9 (real 2.1). Leezpunk still low (0.16/turn vs 0.27).
- **The matchup number doesn't move:** v2 vs consensus Stone Pit 85–86% under every variant (real ~56 for Cattiva-type decks); Chillet BP vs Stone Pit 70–71% (real 48–53); M1 stays 53–56% (real 55). `@bold` didn't raise Stone Pit's face attacks (3.1/game vs real 5.2).
- Reading: the sim's Stone Pit now plays its turns like real pilots; the games end two turns earlier (7.6 vs 9.5 Stone Pit turns) because the aggro side closes games perfectly. Bobby's own Palify losses to Stone Pit show the human version: the aggro side gets Stone Pit to 1–2 life and then misses the closing turn (attackers held back, removal held, overextension into Shotgun). So for this matchup the sim's 85% is close to "the deck played without mistakes", and the gap to reality is mostly the aggro pilot, not the Stone Pit bot. Deck-vs-deck *differences* in the sim remain usable; absolute rates against Stone Pit should be read as an upper bound.

**Palify gauntlet report (external sim, 2026-10-13; `results/runs/palify_reports/eClau-v6-gauntlet-2026-10-13.pdf`):** Bobby's v3 list ("eClau v6", 4 Jormuntide) played 10,080 games by Palify's "forge-2" bot against 20 ladder archetypes rebuilt from 54,892 real games. Headline 59.8% weighted / 63.2% unweighted. **Going first 80.0%, going second 46.4%** (our sim: ~+8 points for first). Worst: Cattiva+Pengullet 32%, Chillet+Aqua 41%, Pengullet+Chillet (the main Chillet BP cluster) 45.6%. Stone Pit/Furnace/Leezpunk clusters 65–83%, so Palify's bot agrees with ours that aggro beats Stone Pit, while the top-50 replays say otherwise: two bots, same blind spot, or pilot. Opening findings (all 18–20 of 20 matchups agree): **Shotgun down by turn 3: 30% vs 67%**; any Gear by turn 4: 48% vs 75% without; Rifle by turn 3 −15; Cattiva-then-Shotgun −21, Pengullet-then-Shotgun −18; Pengullet-then-Chillet within 2 turns +22 (80.7%); Aqua-then-Chillet +19; Chillet best on turn 3 (78%) not turn 1–2 (52%); Jormuntide down by turn 4 (via Chillet) +15; Reindrix deployed by turn 2 −15; Foxparks still in hand at turn 5 +9. Card drawn-lift: Reindrix/Foxparks +12, Jormuntide +13 (t7–9), Blazehowl +10, Chillet +11; Shotgun −13 (their bot casts it early in losses), Axel's −2 to −4, Kitsun −3. "Board first" pilot line +2.6 over the default. No mulligans in their sim. Nearest ladder archetype (64.8%, 68 players) runs Relaxaurus, Azurobe, Sparkit and Elphidran Radiance where we run Lamball, Jormuntide, Aqua and the Axel's/Rifle package.
- Mulligan check from the Palify report (Mac, v2, 2,000 games per rule, same seeds, heuristic2): default rule 68.8%; "keep with Pengullet or 2+ cheap Pals" 68.3% (−0.5); "also redraw 2+ Gear hands" 67.8% (−1.0); "need 2+ cheap Pals" 67.8% (−1.0). None better: the current keep rule stands (keep any hand with a Pal costing ◇4 or less, redraw only with none or with 3+ cards costing ◇7+). Stricter rules throw back 3× as many hands and lose more than they gain.

**J24 review (Stone Pit tech on v2; Dots, frozen code 2c7ba53):**
- Part 1, 2,000 games each vs the top-50 Stone Pit list, `heuristic2@human@seq`, same seed (noise about ±1.5): baseline **87.4%**; A 4 Rifle **85.8** (−1.6); B 2 Handgun **87.6** (+0.2); C 2 Crystal Breath **85.2** (−2.2). Nothing helps against Stone Pit in the sim; the two cards aimed at Menasting/Shadowbeak (Rifle, Crystal) are slightly worse than two Fuacks there.
- Part 2, full field, sequential, default bot: A +0.7 (z 1.2, ran to the cap: no difference); B **−1.7 (z −2.7)**; C **−1.2 (z −2.0)**. Handgun and Crystal Breath are closed again (third and fourth tests). 4 Rifle is flat.
- Reading: with the Stone Pit opponent now playing its engine like real pilots, the aggro side still wins ~87% by racing, and the removal-heavy variants trade a body for a trick the race doesn't need. Consistent with the Palify report (Rifle/Axel's drawn-lift slightly negative). **No change to the list.** The Stone Pit gap vs reality (~56%) is not a card problem the sim can see; see the sequencing notes above.
- Process: Dots ran all seven lines, verified every JSONL against its summary, labelled an interrupted attempt separately and only counted the completed retry. Clean.

**J25 interim (Dots, 500 games per pair, seed 255):** `heuristic2` 7/36 within ±5, MAE **10.1**; `heuristic2@human` 14/36, MAE **8.5**. Four variants to go. If `@human` holds up as best, it becomes the default; comparability note: J16–J24 were run on `heuristic2`.

**J27 pre-check (Mac, 2026-10-14, on v3 `cattiva_dragons_v3`, 2,000 games per list, heuristic2):** −2 Fuack +2 Antique Dresser **−8.3 (z −5.7)**; Chillet BP −10, Stone Pit −7.7; vs the top-50 Stone Pit list with `@human@seq` (300 games) 84.3 → 76.7. −2 Fuack +2 Hot Spring **−4.1 (z −2.8)**; worse against Stone Pit too (−3.3). Both withdrawn before the full job: a 4- or 6-soul structure that adds no body is the opening the Palify report flags as this deck's worst, and the Stone Pit lock/finisher ideas don't pay for it. Caveat: the bot fires the Dresser every turn it's out; a once-only lethal-turn use isn't modelled, but a drop this size isn't all misuse. J27 cancelled; the Stone Pit matchup remains a play problem plus the sim's under-hitting Stone Pit (next bot work).
- Quick checks on v3 (Mac, 2,000 games per list, heuristic2, seed 281), following the Palify report's card ranking: −2 Shotgun +2 Foxparks – Light of Courage +0.2 (flat; Stone Pit +2.2, Shadowbeak −3.0); −2 Rifle +2 Sparkit −0.0; −2 Axel's +2 Sparkit −0.7. All within noise (±1.4). The Shotgun count, Rifle slot and Axel's slot are each worth about the same as their alternatives in the sim; no lead.

**Real games vs Stone Pit, winners vs losers (Palify top-50 set, 17 winners / 48 losers, 2026-10-14):** winners destroyed 2.9 of its structures a game (Furnace 1.3, Machine Gun 0.8, Stone Pit 0.8) vs 1.5 for losers, and attacked structures 5.1 vs 2.9 times. Winners deployed fewer Pals by turn 3 (1.2 vs 1.8), did not have Stone Pit lower by turn 5 (7.9 vs 7.6 life), spent Interrupts at ≤4 life more (0.59 vs 0.25) and at 5+ life less, went first less often (59% vs 69%) and won longer games (11 vs 10 turns). 13 of the 17 winners were Chillet BP; among the 7 aggro-type opponents, both winners attacked structures (7 and 2 attacks), four of five losers attacked them 0–1 times. Reading: against Stone Pit, killing the engine beats racing it, which contradicts the sim (both ours and Palify's bot race and win ~85%). Pocket guide corrected. Sim implication: the bots don't attack structures enough as Stone Pit's opponent, and Stone Pit's bot doesn't punish a racer; both are calibration targets.
- **`@structK` (2026-10-14):** opponent and own structures worth K× in the evaluation. v3 vs the top-50 Stone Pit list, 60 logged games, `heuristic2@human@seq`: structure attacks 3.1/game, destroyed 1.8 (losers' profile); `@struct2` 4.7 / 2.5; **`@struct3` 4.9 / 2.7, the real winners' profile (5.1 / 2.9)**. Win rate vs the (still too weak) Stone Pit bot unchanged within noise (77–82%). Candidate default once the Stone Pit bot itself hits like real pilots; both go into the next calibration grid.
- **Behaviour profiles, real vs sim, per turn (`python3 -m analysis.behaviour_calibration <slug> <run> P1`, 2026-10-14; an earlier version double-counted real attacks, so the "bots attack Pals 7–8× less" reading was wrong and is withdrawn).** Corrected: Pal attacks per turn are similar (Stone Pit real 0.17 / sim 0.26; Chillet BP 0.37 / 0.26). The real gaps: **damage dealt per turn is ~60% of real for every deck** (Stone Pit 0.53 real / 0.35 sim; Chillet BP 0.83 / 0.54; Cattiva·Azurobe 1.60 / 0.72, n=13), aggro pilots attack face about twice as often per turn as the bot (1.89 vs 0.97) and deploy more (1.47 vs 1.21), and the simulated Stone Pit takes twice the damage per turn that real Stone Pit does from its opponents. New opt-in knobs tried: `@killK` (enemy Pals worth K×) and `@allin` (no exposure penalty, no race term): neither closes the damage gap on its own. Engine-first now yields to a chosen attack on a Pal or structure. Next: a calibration grid scored on both the matchup error and these per-turn profiles.

**J25 review (bot calibration grid; Dots, 6 × 45 pairs × 500 games, seed 255, frozen code 815792c):**

| Bot | within ±5 | consistent (|z|≤2) | MAE | engine pairs | other pairs |
|---|---|---|---|---|---|
| heuristic2 (old default) | 7/36 | 10/36 | 10.1 | 11.2 | 7.1 |
| **heuristic2@human** | **14/36** | **16/36** | **8.5** | **9.6** | **5.7** |
| heuristic2@seq | 7/36 | 11/36 | 10.1 | | |
| heuristic2@human@seq | 14/36 | 15/36 | 9.0 | | |
| heuristic2@human@seq@bold | 13/36 | 13/36 | 9.4 | | |
| heuristic2@x1.5@human@seq | 13/36 | 14/36 | 9.0 | | |

- **Adopted: `human` (= `heuristic2@human`) is the default bot for new jobs, with `human1` (= `heuristic@human`) as the second opinion.** `heuristic2` and `heuristic` stay unchanged so J16–J24 remain comparable; new jobs state the bot explicitly. M1 under `human`: 58.6 (real 55).
- Engine sequencing (`@seq`) doesn't improve calibration on its own and slightly hurts with `@human`; `@bold` hurts. The engine-deck pairs remain the misses (MAE 9.6): Cattiva/Lamball·Cattiva/Chillet-BR vs Stone Pit and Tombat still read 20–27 points too kind to the aggro side, and Stone Pit vs Machine Gun 22 too harsh. That is the damage-per-turn gap in the behaviour profiles, not the defence policy.
- Process: Dots completed all six matrices with per-pair resume and 15-minute checkpoints after losing its first checkout; every pair validated against its raw records. Clean.
- Aurora Guide, fifth test (Mac, 2026-10-15, on v3 with 12 Dragons and 4 Jormuntide, 2,000 games per list, `human` bot, seed 291): for 2 Reindrix −2.6 (z −1.8); for 2 Foxparks −2.3 (z −1.6); for 2 Fuack −1.9 (z −1.3). All negative, all slots. The Jormuntide-off-Chillet setup doesn't pay for a card that puts no body on the board, and it isn't better than an Interrupt. **Aurora Guide stays closed.**
| 2026-10-15 22:05 | run | cattiva_dragons_v3 | -2 Lamball – My First Pal / +2 Jolthog Cryst – Stoic Yet Innocent | human | +0.2 ± 1.0 | 0.24 | 4045 | — | **not better (inconclusive)** |
| 2026-10-15 22:33 | run | cattiva_dragons_v3 | -2 Blazehowl – Hellflame Defender / +2 Reptyro – Ore Gorger | human | -0.0 ± 1.0 | -0.03 | 4045 | — | **not better (futility)** |
| 2026-10-15 23:02 | run | cattiva_dragons_v3 | -2 Cattiva – My First Pal / +2 Jolthog Cryst – Stoic Yet Innocent | human | +0.7 ± 1.0 | 0.73 | 4045 | — | **not better (inconclusive)** |
| 2026-10-15 23:14 | run | cattiva_dragons_v3 | -2 Fuack – Manic Wave Ripper / +2 Cryolinx – Arctic Ordeal | human | -0.2 ± 1.6 | -0.11 | 1618 | — | **not better (futility)** |
| 2026-10-15 23:26 | run | cattiva_dragons_v3 | -2 Pump-Action Shotgun / +2 Reptyro – Ore Gorger | human | -1.0 ± 1.6 | -0.62 | 1618 | — | **not better (futility)** |
| 2026-10-15 23:56 | run | cattiva_dragons_v3 | -2 Axel's Strategy / +2 Single-Shot Rifle | human | +0.5 ± 1.0 | 0.50 | 4045 | — | **not better (inconclusive)** |
