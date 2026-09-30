# Assumptions and open questions

These are the places where the rules are ambiguous or silent and I had to choose. Each one lists the options, the choice I made, and how much it could move win rates.
**Status:** `OPEN` = waiting for the user to confirm. `CONFIRMED` = the user agreed. `RESOLVED` = a source settles it.

## Rules

### A1: Can the first player attack on turn 1? (`OPEN`)
- The CR has no rule against it. CR 9.2.2.3 says Pals can attack the turn they're deployed.
- The first player's only turn-1 handicap is skipping the draw (CR 7.3.1).
- **Chosen:** yes, the first player can deploy and attack on turn 1.
- **Impact:** high for aggressive decks and for the first/second-player split.

### A2: Can standing Structures be attacked? (`OPEN`)
- CR 9.2.3: "the non-turn player, or 1 of the structures or Pals in the resting state". It's unclear whether "in the resting state" applies to structures too.
- The QM lists "opposing Pal, structure, or player" as attack targets. The QM Q&A requires Pals to be rested, but says nothing about structures being rested.
- Normal play never rests a structure (assigning rests the *Pal*). If structures had to be rested, durability would almost never matter.
- **Chosen:** any opposing Structure can be attacked, standing or rested.
- **Impact:** medium. It only matters for decks that play Structures.

### A3: How does Gear attach to Pals? (`OPEN`, waiting on card data)
- The CR says Gear is "fielded to assist your Pals" and is deployed to the base. It has no general rules for equipping.
- **Chosen:** the engine deploys Gear to the base. Anything about equipping or attaching is handled by that card's own implementation, following its text. I'll read the Gear cards in `cards.json` before writing any of this, and I'll ask if the text is unclear.

### A4: Do soul cards have any rules text? (`OPEN`, waiting on card data)
- The QM shows soul cards with a small text box, but no rules mention soul card abilities.
- **Chosen:** soul cards are blank resources. If any soul card in `cards.json` has real text, I'll stop and ask.

### A5: Order of simultaneous triggers controlled by one player (simplification, `OPEN`)
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

## Simulation choices (not rules questions)

### S1: Who goes first
- CR 6.2.1.3: a random player chooses. The sim decides who goes first at random from the game seed, so batches measure the deck's average over going first and second. Results are also reported separately for going first and going second.

### S2: Turn cap
- Games that pass 60 turns are recorded as draws with tag `turn_cap`. This should almost never happen, because every damage check and draw uses up deck cards.

### S3: Hidden information
- Bots get the full `Game` object so a future search bot can clone it. The heuristic bot must only read public information and its own hand, and I review it for that. A search bot will have to *determinize* (sample the opponent's hidden cards) instead of peeking at them.

### S4: Overloaded Pals (CR 11.5)
- The player keeps the newest Pals as the rule requires. When they have to choose among older Pals, the bot sends the one with the lowest power to the graveyard.
