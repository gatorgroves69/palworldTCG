# cattiva-azurobe-br vs chillet-relaxaurus-bp

4000 games, bot `heuristic`, seed 1, commit `5e58122`, structures attackable: `any`.

| | Win rate | 95% CI | Games |
|---|---|---|---|
| Overall | **56.7%** | 55.2% – 58.2% | 4000 |
| Going first | **60.6%** | 58.5% – 62.7% | 1994 |
| Going second | **52.8%** | 50.6% – 55.0% | 2006 |

Average game length: 14.96 turns. Game ends: deckout 13, life 3987.

**Calibration** (matchups_2026-09-29.json, palworldtcg.gg): real 56.0% (games: None), sim 56.7%, difference +0.7 points: **PASS** (within ±5)

## Why cattiva-azurobe-br loses (1731 losses)

| Tag | Losses | Share |
|---|---|---|
| behind_on_board_by_round_4-6 | 738 | 42.6% |
| ran_out_of_cards | 464 | 26.8% |
| opponent_lucky_saves_3+ | 430 | 24.8% |
| lost to Jormuntide – Surging Sea Serpent | 424 | 24.5% |
| lost to Chillet – Dragon Whisperer | 304 | 17.6% |
| behind_on_board_by_round_7+ | 273 | 15.8% |
| too_slow_on_the_draw | 221 | 12.8% |
| behind_on_board_by_round_1-3 | 203 | 11.7% |
| lost to Elphidran Aqua – Gentle Ripples | 144 | 8.3% |
| untagged | 105 | 6.1% |
| lost to Elphidran – Gentle Radiance | 80 | 4.6% |
| lost to Pyrin Noct – Steed of Azure Flames | 73 | 4.2% |

## Why chillet-relaxaurus-bp loses (2269 losses)

| Tag | Losses | Share |
|---|---|---|
| behind_on_board_by_round_4-6 | 474 | 20.9% |
| weak_opening_hand | 444 | 19.6% |
| too_slow_on_the_draw | 332 | 14.6% |
| lost to Lamball – My First Pal | 329 | 14.5% |
| opponent_lucky_saves_3+ | 304 | 13.4% |
| untagged | 268 | 11.8% |
| lost to Pengullet – Yearning for the Sky | 219 | 9.7% |
| behind_on_board_by_round_7+ | 214 | 9.4% |
| behind_on_board_by_round_1-3 | 176 | 7.8% |
| lost to Fuack – Manic Wave Ripper | 171 | 7.5% |
| lost to Hangyu Cryst – Frigid Wanderer | 154 | 6.8% |
| lost to Azurobe – Water Dragon Waltz | 151 | 6.7% |

## Draw impact: cattiva-azurobe-br

Win rate when the card was drawn at least once minus when it never was. Correlation, not causation: cards drawn late only show up in long games. ✱ = difference larger than its 95% noise band.

| Card | Δ win rate | Drawn | Not drawn |
|---|---|---|---|
| Pump-Action Shotgun (BP01-020) | +7.0 ✱ | 58.3% (n=3096) | 51.3% (n=904) |
| Suzaku – Hellfire Wings (BP01-002) | +5.4 ✱ | 57.8% (n=3167) | 52.5% (n=833) |
| Kitsun – Wyrmbane Fangs (BP01-007) | +4.0 ✱ | 57.6% (n=3169) | 53.5% (n=831) |
| Pengullet – Yearning for the Sky (BP01-028) | +3.3 | 57.4% (n=3139) | 54.1% (n=861) |
| Lamball – My First Pal (TD01-023) | +1.8 | 57.1% (n=3218) | 55.2% (n=782) |
| Hangyu Cryst – Frigid Wanderer (TD01-015) | +1.2 | 57.0% (n=3186) | 55.8% (n=814) |
| Cattiva – My First Pal (TD02-023) | +0.2 | 56.8% (n=3227) | 56.5% (n=773) |
| Pal Sphere (BP01-047) | -0.3 | 56.6% (n=1998) | 56.9% (n=2002) |
| Sparkit – Hazardous Contact (BP01-008) | -0.6 | 56.6% (n=3180) | 57.2% (n=820) |
| Fuack – Manic Wave Ripper (BP01-032) | -0.6 | 56.6% (n=3210) | 57.2% (n=790) |
| Reindrix – Icy Gaze (TD01-016) | -1.2 | 56.5% (n=3143) | 57.6% (n=857) |
| Azurobe – Water Dragon Waltz (BP01-029) | -1.6 | 56.4% (n=3110) | 58.0% (n=890) |
| Foxparks – A Toasty Hug (TD01-004) | -3.4 | 56.0% (n=3191) | 59.5% (n=809) |

## Draw impact: chillet-relaxaurus-bp

Win rate when the card was drawn at least once minus when it never was. Correlation, not causation: cards drawn late only show up in long games. ✱ = difference larger than its 95% noise band.

| Card | Δ win rate | Drawn | Not drawn |
|---|---|---|---|
| Chillet – Dragon Whisperer (BP01-025) | +20.5 ✱ | 46.7% (n=3339) | 26.2% (n=661) |
| Jormuntide – Surging Sea Serpent (BP01-027) | +20.1 ✱ | 48.6% (n=2941) | 28.5% (n=1059) |
| Astegon – Aegis Wyvern of Death (TD02-012) | +17.9 ✱ | 54.6% (n=1479) | 36.7% (n=2521) |
| Elphidran Aqua – Gentle Ripples (TD01-012) | +7.0 ✱ | 45.2% (n=2908) | 38.2% (n=1092) |
| Pengullet – Yearning for the Sky (BP01-028) | +6.7 ✱ | 44.1% (n=3503) | 37.4% (n=497) |
| Strike from the Darkness (TD02-021) | +4.6 ✱ | 45.0% (n=2509) | 40.4% (n=1491) |
| Relaxaurus – Hungry Gunner (BP01-026) | +4.6 ✱ | 45.0% (n=2483) | 40.4% (n=1517) |
| Elphidran – Gentle Radiance (BP01-098) | +4.1 | 43.7% (n=3541) | 39.7% (n=459) |
| Pal Sphere (BP01-047) | -2.4 | 42.2% (n=2256) | 44.6% (n=1744) |
| Reindrix – Icy Gaze (TD01-016) | -2.6 | 42.9% (n=3446) | 45.5% (n=554) |
| Pengullet Rocket Launcher (BP01-044) | -3.1 | 42.5% (n=3022) | 45.6% (n=978) |
| Zoe's Strategy (BP01-095) | -3.3 | 42.8% (n=3423) | 46.1% (n=577) |
| Blazehowl Noct – Darkflame Defender (TD02-017) | -4.7 ✱ | 41.6% (n=2585) | 46.3% (n=1415) |
| Cryolinx – Arctic Ordeal (BP01-038) | -5.6 ✱ | 42.5% (n=3481) | 48.2% (n=519) |
| Aurora Guide (BP01-048) | -7.0 ✱ | 42.2% (n=3380) | 49.2% (n=620) |
| Pyrin Noct – Steed of Azure Flames (BP01-077) | -7.7 ✱ | 42.2% (n=3433) | 49.9% (n=567) |

## Game logs

- `logs/game_1000000.log`
- `logs/game_1000001.log`
- `logs/game_1000002.log`
- `logs/game_1000003.log`
- `logs/game_1000004.log`
- `logs/game_1000005.log`

Replay any game: `python -m sim replay --deck data/decks/cattiva-azurobe-br.txt --opp data/decks/chillet-relaxaurus-bp.txt --bot heuristic --structures any --game-seed <seed>`
