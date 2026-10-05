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

## Card interpretations (M1)

### C1: Fuack: does *blocking* count as "this card is attacked"? (`CONFIRMED` 2026-09-30)
- CR 9.3.2: a card has "been attacked" when it's chosen as the target at the attack declaration. Blocking (CR 9.4.2.1) changes the target later and isn't described as being attacked.
- **Chosen:** Fuack gets +300 only when it's declared as the target, not when it blocks.
- **Impact:** medium. A blocking Fuack is 200 instead of 500.

### C2: Lamball / Cattiva "cannot be attacked by": can they still *block* those Pals? (`CONFIRMED` 2026-09-30)
- The restriction applies to choosing attack targets (CR 9.2.4.1). CR 9.4.2 only stops Pals "restricted from blocking", and blocking isn't declaring an attack.
- **Chosen:** they can still block any attacker. For example, Lamball can block a ◇4+ Pal.
- **Impact:** low to medium. They're 200-power bodies, so blocking with them is mostly chump-blocking.

### C3: Suzaku: two copies stack (`CONFIRMED` 2026-09-30)
- Each Suzaku is its own replacement effect, and CR 10.11.2.3 only limits the *same* effect to once per situation.
- **Chosen:** two Suzakus give +400. "Your red card" includes red Gear (Pump-Action Shotgun: 1200 → 1400 per Pal) and Suzaku itself (700 → 900). It applies only to non-battle damage dealt to **Pals**.

### C4: "Dragon Pal" = Pal with the Dragon element (`CONFIRMED` 2026-09-30)
- Chillet and Elphidran check for a "Dragon Pal". I read that as a Pal with the Dragon element icon (CR 2.4).
- Elements come from Palify's `game.element` field in `cards.json` (e.g. "Water / Dragon"), which is the only element data available. I checked every M1 Pal's element and they look right.
- Dragon Pals in M1: Azurobe, Chillet, Relaxaurus, Jormuntide, Elphidran, Elphidran Aqua, Astegon.

### C5: Pengullet draws only when it goes from the **base** to the graveyard (`RESOLVED` by CR 10.3.5)
- A Pal's abilities only work in the base. Discarding Pengullet from hand (for example as Interrupt's extra discard) or flipping it in a damage check doesn't draw a card. Being butchered (Zoe's Strategy) or destroyed does.

### C6: Pengullet Rocket Launcher: X = the Pengullet's power when the granted ability resolves (`OPEN`, low)
- After the +500 that's normally 1100. The ability rests the **Pengullet** (not the Gear), deals X to each opposing Pal, then puts the Pengullet in the graveyard, which draws a card via C5.

### C7: Zoe's Strategy, mode 1: the player takes as many resources as possible
- "Up to 5" is a choice, but taking fewer is never better, so the bot always takes the maximum. It's irrelevant in M1, because neither deck produces Material or Ingredient.

### C8: Kitsun / Hangyu Cryst / Relaxaurus / Jormuntide cost conditions use the **printed** cost
- A card in the base has no cost modifiers in M1, so printed cost equals current cost.

### C9: Chillet's revealed card counts as "drawn" for draw-impact statistics
- It reaches the hand or the base either way. This affects analysis only, not play.

## Card interpretations (M2)

### C10: Shadowbeak: "your Pal's AUTO activates twice" (`OPEN`, **high impact**)
- **Chosen:** at night, every AUTO ability of your Pals goes into standby twice (CR 5.21). That includes keyword AUTOs (Brave, Serious, Retaliate, Vigilance, Breakthrough), OnDeploy / OnAttack, "when put into the graveyard" triggers (Pengullet, Menasting, Leezpunk), and Shadowbeak's own end-of-turn butcher.
- It doesn't apply to Structure or Gear abilities. Two Shadowbeaks still means twice, not four times (CR 5.21.2).
- Shadowbeak has to be in your base when the ability triggers. A Pal that has just left the base still counts as "your Pal" (last-known information, CR 10.8.4.1.2).

### C11: Lily's Strategy "increase your soul by 1 card in the rest state" (`OPEN`)
- **Chosen:** move 1 soul card from your soul deck to the soul area, rested. If the soul deck is empty (usually from about turn 9 on), nothing happens. The soul deck has only 10 physical cards (CR 6.1.2).

### C12: Nocturnal instances stack (`OPEN`)
- **Chosen:** Depresso has Nocturnal printed twice, so it gets +600 at night. Lamp gives each of your Pals one more instance, so a Daedream under Lamp gets +600. Only Taunt has an explicit "regardless of instances" rule (CR 12.10.2.1).

### C13: Helzephyr triggers on its own deployment (`OPEN`)
- **Chosen:** it's a Nocturnal Pal, so deploying it at night triggers its own ability (CR 10.8.4.2). The destroyed Pal's cost limit is the cost of the Nocturnal Pal that was deployed. "If it is night" is checked when the ability triggers and again when it resolves.

### C14: Mounted Machine Gun (`OPEN`, low)
- X is at least 1 and at most your Material. The sim caps it at 8 to limit branching; 8 × 500 kills anything in BP01.
- Each of the X shots chooses a Pal again, and it can be the same Pal. Lethal damage is only checked after the whole ability (CR 11.4.2).
- Each 500 is a separate damage event, so with Suzaku each shot deals 700.

### C15: Primitive Furnace discount (`OPEN`, low)
- It applies to the next Gear played from hand this turn, then it's used up. Unused discount expires at end of turn.
- It never takes a Gear below ◇1. X is only offered up to (cost of the priciest Gear in hand − 1).

### C16: Jormuntide Ignis "[③] OR [Discard 2]" is one ability with one 1/Turn (`RESOLVED` by the text)
- The sim offers it only while Ignis is rested, since standing a standing card does nothing.

### C17: "Choose 1 Pal" / "Choose 1 structure or gear" with no side given can target either player's cards (`RESOLVED`, CR 4.4.3)
- This covers Victor's Strategy (return a Pal to hand), Lily's Strategy (destroy a structure or gear), and Strike from the Darkness.

### C18: Cards deployed by effects trigger their OnDeploy
- This covers Reptyro, Lyleen, Chillet, Daedream's Necklace, Lyleen Noct and Medicine Workbench. Deploying is deploying (CR 5.15, 12.3), and nothing is paid.

### C19: Axel's Strategy "cannot block" affects only the opponent's ◇5+ Pals in the base when it resolves

### C20: "It becomes night until the end of the opponent's next turn" (`OPEN`, low)
- Played on your own turn T, it's night through turn T+1. Several effects extend to the latest end.
- Separately, Shadowbeak and Maraith make it night while they're rested.

### C21: Maraith's −200 applies whenever it's night, from any source

### C22: Foxparks' Harness's granted OnAttack damage comes from the Foxparks
- The Foxparks is a red card, so Suzaku's +200 applies (700 → 900).

### C23: Shoddy Bed checks for a rested Nocturnal Pal at the end of your turn
- Lamp-granted Nocturnal counts.

## Card interpretations (rest of BP01/TD, red/blue/colorless)

### C24: Alarm Bell "must attack as much as possible" (`OPEN`)
- **Chosen:** CR 7.5.2.1. While any of your Pals can legally attack, you can't end the main phase. "Cannot be assigned" blocks every assign cost for the rest of the turn. Both also apply to Pals deployed afterwards, as the card says.
- "Stand all Pals assigned this turn" includes the Pal assigned to Alarm Bell's own cost.

### C25: Antique Dresser "Declare 1 card name. Choose all of your cards" (`OPEN`)
- **Chosen:** your cards **in the base** get the declared name until end of turn (CR 4.4.3: "cards" with no zone named means the base). You may declare the name of any card that exists in the game (CR 5.19).
- Added names count for Penking (main name Pengullet), Antique Curtain (names containing "Antique") and The Adventure Begins ("My First").

### C26: Mau Cryst "「Farming」 structure" uses the structure's work suitability from cards.json
- Only Breeding Farm and Ranch (both green) are Farming. Stone Pit is Collecting.

### C27: The Adventure Begins "not played any other cards during this game"
- **Chosen:** counts cards played from hand. Cards deployed by effects (Chillet, Reptyro, Necklace and so on) don't count. "3 or more Pals with 《My First》 in their different card names" counts *distinct* names among your Pals in the base.

### C28: Bushi "At the end of the battle this card attacked, you may return this card to hand"
- **Chosen:** this also applies when the attack was nullified. It only applies if Bushi is still in the base.

### C29: Format of BP02 / SS01 cards (`RESOLVED for now`, 2026-10-01)
- Bobby: BP02 isn't released yet, so it's not implemented. SS01 is the "Sleeve & Card Set Vol.1" (5 cards); Bobby is unsure whether it's legal, and no meta deck uses it, so it's skipped for now. It's a quick add later.
- 13 red/blue/colorless BP02 and SS01 cards are **not implemented**. None of the 10 meta decks uses them, and the stated format is BP01 + TD01/TD02. I'll implement them if they're legal at Bobby's weeklies.
- Update 2026-10-05: Bobby says the SS01 cards have just been released. The 4 red/blue/colorless SS01 cards are now implemented (`cards/ss01.py`): Grizzbolt, Chillet – Finishing Ice Blade, Cattiva – Brimming with Confidence and Quivern. Depresso is purple and isn't needed. BP02 "Legends Awaken" is still unreleased and not implemented.

### C30: SS01 card readings (`OPEN`, 2026-10-05)
- **Copy limit:** the 4-copy limit counts the full card name, so "Chillet – Finishing Ice Blade" and "Chillet – Dragon Whisperer" are different names (as with every other card here, see rules.md). If Bobby's events count by main name (《Chillet》), 4 + 4 would be illegal.
- **Chillet – Finishing Ice Blade:** "its opposing combat Pal" is the Pal it battles (CR 9.4.3), whether it attacks or is attacked. It only draws if it's still in the base when that Pal goes to the graveyard. In a mutual kill, the order of the rule action decides, so it may not draw.
- **Quivern:** the 700 is chosen when the attack is declared at a Pal or structure (before blocks). It can hit any Pal or structure, including the attack target, and not when attacking the player.

## Data caveats

### D1: Calibration target has no sample size or first/second split (`OPEN`)
- `data/calibration/matchups_2026-09-29.json` gives Cattiva·Azurobe (br) vs Chillet·Relaxaurus (bp) as 0.56, with `games: null`. Hermes couldn't get game counts.
- Without a sample size, the real rate's own confidence interval is unknown, so the ±5-point pass band is the only tolerance I apply.
- There's no first/second breakdown in the file. On 2026-09-29 the user supplied a deck-level split instead: Cattiva·Azurobe wins **60% going first and 52% going second**, across all matchups, over 7,468 games (palworldtcg.gg, last 30 days). It covers the deck overall, not this matchup, so I use it only as a **directional check**: the sim should show Cattiva·Azurobe doing better going first, with a gap of roughly the same size (about 8 points). It isn't a tight target.

## Simulation choices (not rules questions)

### S1: Who goes first
- CR 6.2.1.3: a random player chooses. The sim decides who goes first at random from the game seed, so batches measure the deck's average over going first and second. Results are also reported separately for going first and going second.

### S2: Turn cap
- Games that pass 60 turns are recorded as draws with tag `turn_cap`. This should almost never happen, because every damage check and draw uses up deck cards.

### S3: Hidden information
- Bots get the full `Game` object so a future search bot can clone it. The heuristic bot must only read public information and its own hand, and I review it for that. A search bot will have to *determinize* (sample the opponent's hidden cards) instead of peeking at them.

### S5: Bot (`bots/heuristic.py`)
- Both sides always use the same bot. It looks one action ahead: for each main-phase action it copies the game, reshuffles the hidden information (so there's no peeking at the opponent's hand or the next damage-check flip), plays the action, and scores the position.
- The scoring weights are hand-set by card economics (a card in hand = 3.5, a life point = 4, a Pal on the board = 3 + power/150 + 1.5 × strike). **They must not be tuned toward a calibration target.** A change is allowed only when a log or card-usage audit shows a specific misplay, and it has to be recorded here.
- Change log: after the first M1 run, Gear on the base is valued at its card value + 0.4 × cost. Before that, Pengullet Rocket Launcher was never deployed. The fix moved M1 by less than 0.1 point.
- Known weaknesses: no combo planning (Launcher → Pengullet barrage), and too cautious about attacking into likely Interrupts. See docs/m1-calibration.md.
- Change log (M2): the scoring function valued Interrupt cards in the **opponent's** hand, which peeked at hidden information in the real position and added noise in the reshuffled copies. Now only the opponent's hand size counts. Actions within one decision are also scored on the same reshuffled samples (common random numbers). Both are bug fixes found by reading logs (a Stone Pit game where Suzaku didn't attack an empty board), not tuning.
- Change log (J8): when it reshuffled its own deck to plan, the bot also forgot cards it had put on top itself (Aurora Guide, Elphidran Aqua), so it couldn't plan Aurora → Chillet. Cards a player puts on top from hand now stay in place in that player's own reshuffles; a shuffle or the card leaving the deck clears this. Also, Aurora's top card is now always lucky while an attack at us is pending (before, holding Chillet could make it stack a non-lucky Dragon). Both are bug fixes found by reading the card logic, not tuning.
- Change log (J10): a card put on top of the deck is drawn in our next draw phase, so stacking a Dragon for Chillet only pays off if a Chillet is played from hand the same turn. The bot now stacks a Dragon only when it's our main phase and a Chillet in hand is still affordable. Otherwise it stacks a lucky card, which protects against the opponent's attacks before we draw it. This matters with 4 Elphidran Aqua: before, holding any Chillet made it stack a non-lucky Aqua. It's a bug fix from reading the turn structure, not tuning.

### S4: Overloaded Pals (CR 11.5)
- The player keeps the newest Pals as the rule requires. When they have to choose among older Pals, the bot sends the one with the lowest power to the graveyard.
