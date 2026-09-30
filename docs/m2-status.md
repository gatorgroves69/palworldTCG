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
