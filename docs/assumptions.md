# Assumptions and open questions

These are the places where the rules are ambiguous or silent and I had to choose. Each one lists the options, the choice I made, and how much it could move win rates.
**Status:** `OPEN` = waiting for the user to confirm. `CONFIRMED` = the user agreed. `RESOLVED` = a source settles it.

## Rules

### A1: Can the first player attack on turn 1? (`CONFIRMED`)
- Yes. Only the draw is skipped (CR 7.3.1), and Pals can attack the turn they're deployed (CR 9.2.2.3). The user ruled on this on 2026-09-29.

### A2: Can standing Structures be attacked? (`OPEN`, config flag)
- CR 9.2.3 is ambiguous: "the non-turn player, or 1 of the structures or Pals in the resting state".
- The user asked for this to be a flag rather than a guess, so it's `RulesConfig.structures_attackable`, set to `any` (the default) or `rested_only`.
- M1 calibration runs both settings and reports which one lands closer to the real-world 56%.

### A3: Gear (`CONFIRMED`)
- Gear is deployed to its controller's own base as a card in its own right (CR 4.4.1, 10.6.2.4.1).
- It is implemented from each card's own text, and attaches to a Pal only if the text says so.
- Gear can't be attacked or damaged (CR 4.4.4, 9.2.3), and it doesn't count toward the 5-Pal limit.

### A4: Do soul cards have any rules text? (`RESOLVED`)
- They're blank resources. Every soul entry in `data/cards.json` (SOUL-000 to SOUL-024) has only reminder text for the "rest 3 souls, draw 1" main-phase action (CR 8.5), and reminder text doesn't affect the game (CR 2.12.2). The engine handles that action already.

### A5: Order of simultaneous triggers controlled by one player (simplification, `CONFIRMED for now`)
- CR 10.5.3: the controller picks which of their waiting triggers to resolve first.
- **Chosen:** each player's triggers resolve in the order they triggered. The bot doesn't choose. The turn player's triggers still resolve before the non-turn player's, as the CR requires.
- **Impact:** low, unless a deck has order-sensitive trigger chains. I'll check again once the M1 cards are implemented.

### A6: Blocking when the target isn't the player (`RESOLVED`)
- Palify's guide says Pals "block an attack aimed at you". CR 9.4.2 allows blocking any attack.
- **Chosen:** CR, so a block can redirect an attack aimed at a rested Pal or a Structure too.

### A7: Rested Pal attacked, does it deal damage back? (`RESOLVED`)
- CR 9.6.3.1 and QM "Battle" both say it does. Implemented.

### A8: Damage check with Strike ≥ 2 (`RESOLVED`)
- CR 11.2.2 and QM both say the first lucky flip cancels **all** of the damage, not just 1 point. Implemented.

### A9: Deck color limit (`RESOLVED`, from QM)
- The CR doesn't mention it. The QM says "Up to 2 colors can be used in a deck. Colorless cards can be used freely in any deck." Enforced when a deck is validated.

## Data caveats

### D1: Calibration target has no sample size or first/second split (`OPEN`)
- `data/calibration/matchups_2026-09-29.json` gives Cattiva·Azurobe (br) vs Chillet·Relaxaurus (bp) as 0.56, with `games: null`. Hermes couldn't get game counts.
- Without a sample size, the real rate's own confidence interval is unknown, so the ±5-point pass band is the only tolerance I apply.
- There's no first/second breakdown in the file, so the "does better going first" check can only confirm the direction, not compare numbers.

## Simulation choices (not rules questions)

### S1: Who goes first
- CR 6.2.1.3: a random player chooses. The sim decides who goes first at random from the game seed, so batches measure the deck's average over going first and second. Results are also reported separately for going first and going second.

### S2: Turn cap
- Games that pass 60 turns are recorded as draws with tag `turn_cap`. This should almost never happen, because every damage check and draw uses up deck cards.

### S3: Hidden information
- Bots get the full `Game` object so a future search bot can clone it. The heuristic bot must only read public information and its own hand, and I review it for that. A search bot will have to *determinize* (sample the opponent's hidden cards) instead of peeking at them.

### S4: Overloaded Pals (CR 11.5)
- The player keeps the newest Pals as the rule requires. When they have to choose among older Pals, the bot sends the one with the lowest power to the graveyard.
