# M2 status: calibration fails, and the cause is the bot

**Result:** 3/21 calibrated matchups within ±5 points (mean absolute error 16.4 points). The M2 bar isn't met.

## What's done
- 8-deck gauntlet: cattiva-azurobe-br, chillet-relaxaurus-{bp,br,bg}, lamball-stone-pit-pr, lamball-cattiva-bg, shadowbeak-menasting-bp, foxparks-harness-br. There are no lists for tombat-medicine-gp or machine-gun-furnace-br.
- All 57 non-soul cards are implemented and tested (26 from M1, 31 new), and 231 tests pass.
- 2,000 games per pair for all 28 pairs, under both Structures settings: [matrix-any](m2/matrix-any.md), [matrix-rested_only](m2/matrix-rested_only.md).

## Findings
1. **The Structures ruling (A2) barely matters in this meta.** `any` and `rested_only` differ by 3 points or less per deck, and 3/21 pairs pass either way. Structures do get attacked (about 0.7 attacks and 0.6 Structures destroyed per game for the Stone Pit deck), so the setting was genuinely tested. Neither setting fits the real data better.
2. **Results depend on the bot as much as on the decks.** The same pairs under two bots:

   | Matchup | RuleBot | HeuristicBot | Real |
   |---|---|---|---|
   | Chillet-BP vs Chillet-BR | 56.5% | 18.4% | 52% |
   | Chillet-BP vs Lamball·Cattiva | 31.4% | 74.6% | 49% |
   | Cattiva vs Lamball·Stone Pit | 78.1% | 89.4% | 56% |
   | Cattiva vs Chillet-BP (M1) | 72.1% | 57.2% | 56% |

   With swings of up to 43 points, the matrix measures bot policy more than deck strength. **This also weakens the M1 pass:** it held for HeuristicBot, but it depends on the bot.
3. **Mechanism: board stalls.** HeuristicBot looks one action ahead, and its scoring penalizes leaving an attacker rested next to a bigger enemy Pal. The mid-game then stalls, with both sides holding big Pals back as blockers (see [the annotated log](m2/game_5000010_bp-vs-br_stall.log) from turn 9 on). Stalls are decided by repeatable non-attack damage: Single-Shot Rifle, Pump-Action Shotgun, Reptyro digging for Gear. So:
   - **Chillet-BR, which has lots of that damage, is inflated:** 74.5% against the gauntlet vs 52.8% real.
   - **Setup decks are deflated.** Lamball·Stone Pit is at 29.1% vs 53.9% real, and Shadowbeak·Menasting at 25.2% vs 39.5%. Their plans take several turns (Material, then Mounted Machine Gun; night, then Nocturnal Pals, then Helzephyr), and the bot doesn't sequence them. Lamp, Workbench and Rocket Launcher usually stay in hand.
4. **No rules or card errors found.** I read logs for Stone Pit, Shadowbeak, and Chillet BP vs BR line by line, and every step follows the card text. Two bot bugs were found and fixed along the way: the bot was peeking at the opponent's hand, and its choices were noisy.

## Proposed fix (needs sign-off: it's the "stronger bot" seam planned since M1)
1. **Turn-level search bot.** For each candidate plan for the whole turn, roll out the opponent's reply turn on reshuffled copies, then score. That means determinized Monte Carlo tree search, or a cheaper version of it: a beam search over the turn's actions plus a one-turn rollout of the reply. The search is what fixes the stalls: attacking only looks bad when you can't see the opponent's reply.
2. **Check that results don't depend on the bot before calibrating.** Only trust a matrix entry when two competent bots, for example the search bot at two different search budgets, agree within about 5 points. Otherwise the calibration can be "passed" by luck, as M1 partly was.
3. **Don't fit the scoring weights to the real data.** They stay hand-set. If a stronger bot still misses on specific pairs, those misses become the next diagnosis targets.

Cost: roughly 10–50× slower per game, depending on search budget. That's fine for Hermes's overnight runs, and heavy but workable on the Mac.

## Update: search bots and learned evaluation (sign-off given for "stronger bot")

| Bot | Mirror score vs HeuristicBot | Calibration | Speed |
|---|---|---|---|
| SearchBot (flat Monte Carlo + simulated opponent reply, FastBot rollouts) | 31–42%, weaker | not run | ~1 s/game |
| PlanBot (per-turn attack style picked from rollouts) | 44–52%, no better | not run | ~1.5 s/game |
| HeuristicBot + evaluation learned from self-play (v1) | 53–62% in 4/5 decks, modestly stronger | **3/21, mean abs error 17.3** ([matrix](m2/matrix-learned.md)) | ~0.2 s/game |
| Learned evaluation, second self-play round | 0–6%, broken (learned "never attack") | discarded | — |

**Bot agreement check** (HeuristicBot vs learned HeuristicBot, all 28 pairs): only **6/28 within 5 points**, mean difference 18.5 points, maximum 46.8. The absolute matchup numbers still depend mostly on which bot plays.

Per deck (average against the gauntlet):

| Deck | HeuristicBot | Learned | Real |
|---|---|---|---|
| cattiva-azurobe-br | 62.7 | 66.7 | 59.2 |
| chillet-relaxaurus-bg | 42.9 | 62.6 | 47.5 |
| chillet-relaxaurus-bp | 56.8 | 59.9 | 58.2 |
| chillet-relaxaurus-br | 74.5 | 52.7 | 52.8 |
| foxparks-harness-br | 56.5 | 35.3 | 51.7 |
| lamball-cattiva-bg | 52.2 | 76.3 | 58.6 |
| **lamball-stone-pit-pr** | **29.1** | **29.1** | 53.9 |
| **shadowbeak-menasting-bp** | **25.2** | **17.5** | 39.5 |

**The two misses that don't depend on the bot:** Lamball·Stone Pit and Shadowbeak·Menasting are 15–25 points too weak under *every* bot. A miss that survives a change of bot is the strongest sign of a card or rules problem (or of a strategy none of these bots can play), so these two are the next diagnosis targets.

Also fixed along the way: determinize() left stale zone labels on reshuffled cards (duplicated or looping cards in simulated copies; affected HeuristicBot too).

## Update: two-step bot (heuristic2)

The Stone Pit and Shadowbeak logs showed **no card or rules errors**. They showed the bot never taking *setup* actions whose payoff comes one action later:
- the Primitive Furnace discount before a Pump-Action Shotgun (the Stone Pit deck sat on 9 Material)
- Lamp or Necklace night before a Nocturnal deploy (the Helzephyr kill)
- Rocket Launcher before the Pengullet barrage, and Axel's "cannot block" before an attack

`heuristic2` scores each action together with its best follow-up action in the same turn.

- **It's stronger in every mirror tested:** 55–62% against `heuristic` across 6 decks. Furnace discounts go from 0.00 to 0.17 per game, Mounted Machine Gun fire rises about 2.6×, and Helzephyr kills about 3×.
- **Speed:** ~0.3 s/game.
- **Calibration** ([matrix](m2/matrix-heuristic2.md)): 3/21 pairs within ±5, but the **mean absolute error drops from 16.4 to 12.0**.
- **Agreement with `heuristic`:** 10/28 pairs within 5 points.

| Deck | 1-step | 2-step | Real |
|---|---|---|---|
| cattiva-azurobe-br | 62.7 | 63.2 | 59.2 |
| chillet-relaxaurus-bg | 42.9 | 55.7 | 47.5 |
| chillet-relaxaurus-bp | 56.8 | 52.8 | 58.2 |
| chillet-relaxaurus-br | 74.5 | 57.8 | 52.8 |
| foxparks-harness-br | 56.5 | 41.9 | 51.7 |
| lamball-cattiva-bg | 52.2 | 68.8 | 58.6 |
| lamball-stone-pit-pr | 29.1 | 31.5 | 53.9 |
| shadowbeak-menasting-bp | 25.2 | 28.4 | 39.5 |

Lamball·Stone Pit is still about 22 points too weak under every bot. It accounts for the 3 largest misses. Its engine (Material → Furnace discount → cheap Pump-Action Shotgun each turn, Mounted Machine Gun with stored Material) takes several turns, which even a two-step bot barely plans. The learned-evaluation bot never plays Structures or Gear at all (the self-play fit learned "Structures lose"), so it isn't used further.

## Update: full-turn-cycle lookahead (LookaheadBot), tried and rejected

J1 (10 decks, `heuristic2`, 1,000 games/pair, run by Mew on the Optiplex) showed the same pattern for the whole field: every engine deck comes out too weak (Stone Pit 35 vs 54, Machine Gun·Furnace 39 vs 47, Tombat·Medicine 38 vs 44, Shadowbeak 33 vs 40), and decks with a straightforward plan come out too strong. In the logs, the Stone Pit bot keeps Mounted Machine Gun in hand all game. Engine pieces pay off on the *next* turn, which the two-step score can't see.

`LookaheadBot` takes the two-step bot's top 3 actions and re-ranks them with 2 simulations each of: the rest of this turn, the opponent's turn, and our next turn (one-step bots inside). Result: it's **weaker in every mirror (39–45% vs heuristic2)** and 14× slower (~3.9 s/game). Its rollouts are played by a weaker bot and there are only 2 of them, so they are noisier and worse informed than the two-step ranking they override.

Tally of the stronger-bot attempts so far:

| Bot | vs predecessor in mirrors |
|---|---|
| SearchBot (flat Monte Carlo, FastBot rollouts) | weaker (31–42%) |
| PlanBot (per-turn attack style from rollouts) | equal (44–52%) |
| Learned evaluation v1 | slightly stronger (53–62%), but never plays Structures/Gear |
| Learned evaluation v2 | broken (0–6%) |
| **TwoStepHeuristicBot (one-action follow-up)** | **stronger in 6/6 (55–62%); current default** |
| LookaheadBot (turn-cycle rollouts) | weaker (39–45%) |

**Conclusion:** cheap search on top of hand-set scoring has stopped paying off. A real gain likely needs a much stronger rollout policy *and* far more rollouts, which this hardware can't run at matrix scale, or human-written plans for each engine deck. Until then: **absolute win rates for engine decks are unreliable** (too low), and so are the absolute numbers for decks that beat them up (too high). **Relative swap tests** (same field, same bot, confirmed under a second bot) remain the recommended use.
