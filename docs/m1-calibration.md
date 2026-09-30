# M1 calibration: Cattiva · Azurobe (BR) vs Chillet · Relaxaurus (BP)

**Verdict: PASS.** The sim gives Cattiva · Azurobe **56.7%** (95% CI 55.2–58.2%, 4,000 games) against a real-world **56%**. That's +0.7 points, well inside the ±5 band. It also reproduces the first/second pattern.

| | Sim | Real |
|---|---|---|
| Overall (this matchup) | **56.7%** (55.2–58.2) | 56% (palworldtcg.gg, game count not available) |
| Going first | **60.6%** (58.5–62.7), n=1,994 | 60%, whole deck across all matchups, 7,468 games |
| Going second | **52.8%** (50.6–55.0), n=2,006 | 52%, whole deck across all matchups |
| First − second gap | 7.8 points | 8 points |

The first/second numbers aren't a like-for-like comparison: the real split covers the deck against every opponent, not just this one. So it's only a check that the direction and rough size match (docs/assumptions.md D1), and they do.

- Run: `python -m sim run --deck data/decks/cattiva-azurobe-br.txt --opp data/decks/chillet-relaxaurus-bp.txt --games 4000 --seed 1`, commit `5e58122`, bot `heuristic` on both sides.
- Average game length is 15.0 turns (about 7.5 each). 3,987 games ended on life and 13 by deck-out.
- Runtime is about 50 s on this Mac for 4,000 games.
- The full report is [m1/report.md](m1/report.md), and the raw summary is [m1/summary.json](m1/summary.json).

## `structures_attackable`: any vs rested_only

**This matchup can't answer the question.** Neither deck has a Structure, and no card here puts one into play. With the same seed, both settings produce byte-identical `games.jsonl` (56.7% both ways). The flag stays at `any` and stays `OPEN` (A2) until M2 brings in decks with Structures.

## Why Cattiva · Azurobe loses (1,731 losses; a game can have several tags)

| Tag | Share of losses |
|---|---|
| Behind on board by round 4–6 | 42.6% |
| Ran out of cards (empty hand near the end) | 26.8% |
| Opponent got 3+ lucky saves | 24.8% |
| Lost to Jormuntide (≥40% of the life lost came from it) | 24.5% |
| Lost to Chillet | 17.6% |
| Behind on board by round 7+ | 15.8% |
| Too slow on the draw (went second, game ≤12 turns) | 12.8% |
| Behind on board by round 1–3 | 11.7% |

In short, Cattiva · Azurobe loses the mid-game board to Chillet's big Dragons (a free Jormuntide off Chillet is the swing turn), and runs out of gas against a deck that draws more cards.

For comparison, Chillet · Relaxaurus loses mainly on board by round 4–6 (20.9%), weak opening hands (19.6%, meaning no Pal of cost 4 or less), and being too slow on the draw (14.6%). It also often **loses to Lamball** (14.5%): nothing in the Chillet deck costs 3 or less, so it can never attack Lamball.

## Draw impact (win rate when drawn at least once − never drawn)

This measures correlation, not causation. ✱ = the difference is larger than its 95% noise band.

**Cattiva · Azurobe, top:** Pump-Action Shotgun **+7.0 ✱**, Suzaku **+5.4 ✱**, Kitsun **+4.0 ✱**. All three kill Chillet's big Pals outright: Shotgun hits every opposing Pal for 1200, Suzaku adds 200 to effect damage, and Kitsun deals 1200 to any Pal costing 7 or more.
**Cattiva · Azurobe, bottom:** Foxparks −3.4, Azurobe −1.6, Reindrix −1.2. None of these is significant.

**Chillet · Relaxaurus, top:** Chillet **+20.5 ✱**, Jormuntide **+20.1 ✱**, Astegon **+17.9 ✱**, Elphidran Aqua +7.0 ✱.
**Chillet · Relaxaurus, bottom:** Pyrin Noct **−7.7 ✱**, Aurora Guide **−7.0 ✱**, Cryolinx **−5.6 ✱**, Blazehowl Noct −4.7 ✱.

The negative Chillet cards are the Interrupt Pals and Aurora Guide. That's partly a real effect (drawing them instead of Dragons) and partly the bot (see below).

## Why a pass isn't proof

The number matches, but errors can cancel out. Here's what I checked and what I know is imperfect.

**Checked:**
- I read three full games line by line: rules, soul counts, damage checks, card effects, locks, Interrupt costs. No rules errors.
- Every card has a unit test, and the implementation text matches `cards.json` word for word (194 tests in total).
- I audited card usage over 300 games. That found one bot bug (Gear was undervalued, so Pengullet Rocket Launcher never got played). I fixed it before the reported run; the fix moved the result by less than 0.1 point.

**Known bot weaknesses** (same bot on both sides, but they may not hurt both decks equally):
1. **No combo planning.** The bot looks one action ahead, so it rarely sets up Rocket Launcher → Pengullet (+500) → barrage. It still deploys the Launcher only when it has spare souls, and the Launcher's draw impact is −3.1. This probably **understates Chillet · Relaxaurus** a little.
2. **Interrupts are used freely.** Chillet's bot uses about 3.6 Interrupts a game and often deploys its Interrupt Pals as bodies. Both habits are plausible, but I can't check them against real games.
3. **Too cautious attacking into Interrupts.** In game 1000000, P1's Suzaku didn't attack a P2 at 1 life, because the bot expected to be Interrupted and didn't want to leave Suzaku exposed. A human would keep forcing Interrupts. This probably **understates Cattiva · Azurobe** a little.

The bot's weights are hand-set by card economics (a card in hand = 3.5, a life point = 4). I didn't adjust them toward the 56% target.

## Game logs for hand-checking against Palify's simulator

- [m1/game_1000000_cattiva-first.log](m1/game_1000000_cattiva-first.log): Cattiva · Azurobe goes first and loses on turn 16. It covers:
  - a free Jormuntide off Chillet
  - Jormuntide's skipped stand phase
  - Pump-Action Shotgun wiping two Chillets
  - Suzaku boosting Kitsun to 1400 to kill Relaxaurus
  - Relaxaurus's lock
  - seven Interrupts
- [m1/game_1000005_chillet-first.log](m1/game_1000005_chillet-first.log): Chillet · Relaxaurus goes first and loses on turn 12. It covers:
  - Fuack's +300 when attacked
  - Relaxaurus locking an already-rested Reindrix, and the lock lifting when Relaxaurus dies
  - Kitsun killing Relaxaurus with exactly 1200 damage
  - a lucky-heavy race with small Pals

Replay any game: `python -m sim replay --deck data/decks/cattiva-azurobe-br.txt --opp data/decks/chillet-relaxaurus-bp.txt --game-seed <seed>`. The same seed always gives the same log.
