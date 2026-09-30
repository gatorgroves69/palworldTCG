# Palworld OCG rules, as implemented

Sources, in order of precedence:

1. **Card text.** Card text overrides the rules (CR 1.3.1).
2. **Comprehensive Rules v1.00** (Bushiroad, 30 July 2026), 575 numbered rules.
   Official PDF: <https://en.palworld-official-cardgame.com/rule/>.
   Palify's searchable transcription: <https://palify.org/rules/comprehensive>. I spot-checked it against the PDF and they match.
   Rule numbers below (`CR x.y`) refer to this document.
3. **Official Quick Manual / Play Guide** (Bushiroad, "rules accurate as of June 27, 2026").
   Used only where the CR is silent or ambiguous. Cited below as `QM`.
4. **Palify's illustrated guide** (<https://palify.org/rules>). Background only; it never overrides 1–3.

Every place where I had to choose an interpretation is tagged **⚠ INTERPRETATION** and listed in
[`assumptions.md`](assumptions.md) for the user to confirm.

---

## 1. Deck construction (CR 6.1, QM)

- Main deck: exactly **50** cards (CR 6.1.1.1).
- No more than **4** copies of any one card name (CR 6.1.1.2). Copies are counted by *name*, not by code, so alt-arts share the limit.
- No more than **8** cards with the lucky icon (CR 6.1.1.3).
- **At most 2 colors** per deck. Colorless cards don't count toward that (QM, "Deck Construction Rules"). The CR doesn't mention this; the QM does, and I enforce it.
- Soul deck: **10** soul cards (CR 6.1.2.1).
- Colors: red, blue, green, purple, or colorless (CR 2.6).

## 2. Zones (CR 4)

| Zone | Visibility | Order matters | Notes |
|---|---|---|---|
| Deck | hidden | yes | Shuffled at setup |
| Hand | hidden (you can see your own) | no | **No hand size limit** in the CR |
| Base | public | no | Pals (max **5**, CR 4.4.5.2), Structures and Gear (no limit, QM Q&A). Cards here are standing or rested |
| Graveyard | public | no | |
| Soul deck | public | no | Remaining soul cards |
| Soul area | public | no | Souls, each standing or rested |
| Exile | public | no | |
| Resolution | public, shared | yes | Temporary; the engine does not model it as a zone |

A card that leaves the base becomes a new object. Effects that applied to it on the base stop applying (CR 4.1.4).
Pals and Structures in the base have a **damage taken** counter (CR 4.4.4).

## 3. Setup (CR 6.2)

1. Each player shuffles their main deck.
2. A random player chooses who goes first. **The sim always picks the first player at random from the game seed**, so first/second is split roughly 50/50 over a batch.
3. The **second** player puts 1 soul from their soul deck into the soul area, standing (CR 6.2.1.5).
4. Each player draws 5 cards.
5. **Redraw (mulligan):** the first player decides first, then the second player. A player who redraws puts their whole hand back, shuffles, and draws 5 new cards. Each player can do this once per game (CR 6.2.1.7).
6. Life is set to **10**, damage taken to 0, and resources (Material, Ingredient) to 0.

## 4. Turn structure (CR 7)

1. **Stand phase:** stand every card in your base and soul area. "At the beginning of turn" and "at the beginning of stand phase" abilities trigger, and on turn 1 so do "at the beginning of the game" abilities.
2. **Draw phase:** draw 1 card. **The first player skips the draw phase on the first turn of the game** (CR 7.3.1, QM "Skipped for the first turn of player going first").
3. **Soul phase:** move **2** souls from the soul deck to the soul area, standing. If fewer than 2 remain, move all of them (CR 7.4.2). Because the soul deck holds 10 cards, you can never have more than 10 souls.
4. **Main phase:** take any of the following actions, any number of times, in any order (CR 8):
   - Play a card from hand by resting standing souls equal to its cost (CR 10.4.3).
   - Use an ACT ability of a card in your base.
   - Start a battle (§5).
   - Rest 3 souls to draw 1 card, **once per turn** (CR 8.5).
   - When you're done, go to the end phase.
5. **End phase:** "At the end of turn" abilities trigger, then a check timing. Then the damage on **every** Pal and Structure in **both** bases goes to 0, and "until end of turn" effects end (CR 7.6). Then the turn passes to the other player.

## 5. Battle (CR 9)

**Who can attack (CR 9.2.2):** a standing Pal you control that isn't prevented by an effect.
**Pals can attack on the turn they're deployed** (CR 9.2.2.3). No rule stops the first player from attacking on turn 1. ⚠ INTERPRETATION A1.

**What can be attacked (CR 9.2.3):**
- the opponent (the player),
- a **rested** opposing Pal (a standing Pal only if the attacker has *Assault*),
- an opposing **Structure**, standing or rested. ⚠ INTERPRETATION A2.

Steps:

1. **Attack declaration:** choose the attacker and the target, then rest the attacker. "On Attack" and *Brave* trigger.
2. **Block declaration:** the non-turn player may block with 1 of their standing Pals that isn't already the target. That Pal is rested and becomes the new target. Blocking is allowed whatever the original target was (player, Pal or Structure). A Pal with *Stealth* can't be blocked.
3. **Quick step:** the non-turn player may play Quick events, Quick ACT abilities and *Interrupt* as many times as they like. The turn player can't act here.
4. **Damage step:** if the attacker or the target has left play, skip to the end of battle.
   - **Pal vs Pal:** each deals damage equal to its power to the other. This includes a **rested** Pal that was attacked: it still deals damage back (CR 9.6.3.1, and QM "both deal damage equal to their power to each other").
   - **Pal vs Structure:** the Pal deals its power in damage to the Structure. The Structure deals no damage back.
   - **Pal vs player:** the Pal deals damage to the player equal to its **Strike**, and the player then does a **damage check** (§6).
5. **End of battle:** "At the end of the battle" abilities trigger, and "until end of the battle" effects end.

**Nullify the attack** (for example, *Interrupt*): go straight to end of battle (CR 5.18). The attacker stays rested, and any On Attack effects that already resolved stay resolved.

## 6. Player damage and the damage check (CR 11.2)

This happens immediately (it's an interrupt-type rule action) whenever a player's damage taken is 1 or more:

1. Put the top card of the player's deck into their graveyard.
2. If that card has the **lucky icon**, all of this damage is **cancelled**. The player loses no life. Go to step 4.
3. If the number of cards flipped so far is at least the damage taken, **or** the deck is now empty, the player loses life equal to the damage taken. Otherwise go back to step 1.
4. Set damage taken back to 0.

In short, **Strike N flips up to N cards, and a single lucky card among them cancels all of the damage**.
The QM agrees: "stop flipping and cancel the damage". The flipped cards go to the **graveyard**, which is why taking hits brings you closer to decking out.

## 7. Winning and losing (CR 1.2, 11.3)

These are checked at every check timing:

- A player at **0 or less life** loses.
- A player with **0 cards in their deck** loses. This applies as soon as the deck is empty, even if they never try to draw from it. QM Q&A: "You'll lose the game when your deck has 0 cards remaining."
- If both players lose at the same time, the game is a draw.
- Any Pal or Structure whose damage is **greater than 0 and at least** its power (durability for Structures) goes to the graveyard (CR 11.4).
- If a player has more than 5 Pals, they send the extras to the graveyard. They must keep the Pals placed most recently and choose among the rest (CR 11.5).

## 8. Abilities and timing (CR 10)

- **ACT** (activated): the player uses it by paying the cost in `[ ]`. A circled number such as `[②]` means rest that many souls. "1/Turn" limits how often it can be used.
- **AUTO** (automatic): triggers when its condition is met and resolves at the next check timing. If both players have triggers waiting, the turn player's resolve first, one at a time, and rule actions are re-checked after each one (CR 10.5.3). A trigger **must** be played unless it has an optional cost (CR 10.8.3.1).
- **CONT** (continuous): always on while the card is in the base.
- Abilities on Pals, Structures and Gear only work while the card is in the base, unless the ability says otherwise (CR 10.3.5).
- Continuous effects apply in layers: printed value, then abilities granted or removed, then non-numeric effects, then numeric changes, then order of creation (CR 10.10).
- **Choose** (CR 10.6.3): the player must choose as many targets as possible, up to the number given. "Up to X" allows choosing 0.
- An **X** whose value the card doesn't define is 1 (CR 10.6.2.2.2).
- An instruction to do something impossible does nothing. A partly possible instruction is carried out as far as possible (CR 1.3.2).

## 9. Keywords (CR 12)

| Keyword | Type | Meaning |
|---|---|---|
| Quick | — | Can be used in the Quick step (defender's window) |
| On Deploy | AUTO | Triggers when the card is deployed |
| On Attack | AUTO | Triggers when the card attacks |
| On Assign | AUTO | Triggers when the card is assigned to a Structure |
| Brave N | AUTO | On Attack: +N power until end of turn |
| Serious N | AUTO | On Assign: choose 1 Pal, which gets +N power until end of turn |
| Interrupt | ACT, Quick | Pay [① + discard this card] **or** [discard this card + 1 other card from hand] to nullify the opponent's attack |
| Vigilance | AUTO | At the end of your turn, stand this card |
| Taunt | CONT | The opponent must target this card if it can legally be targeted |
| Stealth | CONT | This card can't be blocked |
| Retaliate | AUTO | When this card goes to the graveyard during a battle it fought in, the opposing Pal in that battle also goes to the graveyard |
| Nocturnal | CONT | +300 power while it is Night |
| Breakthrough | AUTO | If this card is attacking and the opposing Pal goes to the graveyard, deal damage equal to this card's Strike to that Pal's controller. This damage causes a damage check |
| Assault | CONT | Can attack **standing** Pals |

Other terms:
- **Assign:** rest one of your standing Pals as the cost of a Structure's ability. The Pal is now "assigned" (CR 5.17).
- **Butcher:** put a Pal you control into your graveyard (CR 5.16).
- **Material / Ingredient:** resources you gain with "Get" and spend with "Consume". You can't consume more than you have (CR 3.3, 5.13).
- **Night:** a game-wide state that cards can switch on (CR 5.3).
- **Deploy:** move a Pal, Structure or Gear onto a base from anywhere else (CR 5.15).
- **〈 〉:** an ability that one card grants to another, usually until end of turn.

## 10. Loops

An unbreakable infinite loop is a draw (CR 13.1). The sim also has a **hard turn cap** (default 60 turns), after which the game is recorded as a draw with loss tag `turn_cap`. It's a safety net and should never trigger in a real game.
