"""The game engine: setup, turn structure, battle, damage checks, rule actions.

Pure logic: no file or network I/O. Rule references (CR x.y) are to the
Comprehensive Rules v1.00; see docs/rules.md.

Decisions are delegated to one agent per player (see bots/base.py). The
acting player's main-phase choices come back as `Action`s from
`legal_actions`; everything else (blocks, the Quick step, targets) goes
through `ask`. A search bot can `clone()` the game at any main-phase
decision point and play the rest out with its own rollout agents.
"""
from __future__ import annotations

import copy
import random
from collections import Counter
from dataclasses import dataclass, field
from typing import Callable, Protocol, Sequence

from .abilities import CardImpl, Event, Trigger
from .config import RulesConfig
from .actions import (Action, Activate, Attack, Decision, EndMain, Pass, PlayCard,
                      SoulDraw, UseInterrupt)
from .deck import Deck
from .model import CardType
from .state import Battle, CardInstance, Mod, PlayerState, Zone

PAL_LIMIT = 5                # CR 4.4.5.2
STARTING_LIFE = 10           # CR 6.2.1.8
OPENING_HAND = 5             # CR 6.2.1.6
SOULS_PER_TURN = 2           # CR 7.4.2.1
SOUL_DRAW_COST = 3           # CR 8.5.1
DEFAULT_TURN_CAP = 60        # safety net, see docs/assumptions.md S2
MAX_ACTIONS_PER_TURN = 200   # guards against a bot that never ends its turn


class GameOver(Exception):
    pass


class UnimplementedCardError(LookupError):
    """A deck contains a card with no implementation. Never play it as vanilla."""


class Agent(Protocol):
    def choose_redraw(self, game: "Game", player: int) -> bool: ...
    def choose_action(self, game: "Game", player: int, actions: list[Action]) -> Action: ...
    def choose(self, game: "Game", decision: Decision) -> list: ...


ImplResolver = Callable[[str], CardImpl]


@dataclass
class PlayerStats:
    drawn: list[str] = field(default_factory=list)       # codes, including the opening hand
    opening_hand: list[str] = field(default_factory=list)
    played: list[tuple[int, str]] = field(default_factory=list)  # (turn, code)
    life_lost_to: Counter = field(default_factory=Counter)       # attacker/source code -> life lost
    lucky_saves: int = 0
    redrew: bool = False
    attacks: int = 0


@dataclass
class GameResult:
    seed: int
    winner: int | None      # 0, 1, or None for a draw
    reason: str             # "life", "deckout", "draw", "turn_cap"
    turns: int
    first_player: int
    life: list[int]
    stats: list[PlayerStats]
    history: list[dict]


class Game:
    def __init__(
        self,
        decks: Sequence[Deck],
        impls: ImplResolver,
        agents: Sequence[Agent],
        seed: int,
        log: bool = False,
        turn_cap: int = DEFAULT_TURN_CAP,
        rules: RulesConfig | None = None,
    ) -> None:
        assert len(decks) == 2 and len(agents) == 2
        self.seed = seed
        self.rng = random.Random(seed)
        self.deck_names = [d.name for d in decks]
        self.agents: list[Agent] | None = list(agents)
        self.logging = log
        self.lines: list[str] = []
        self.turn_cap = turn_cap
        self.rules = rules or RulesConfig()

        self.players = [PlayerState(0), PlayerState(1)]
        self.cards: dict[int, CardInstance] = {}
        missing: list[str] = []
        uid = 0
        for p, deck in enumerate(decks):
            for d in deck.soul:
                self._resolve(impls, d.code, missing)  # soul cards must be registered too
            self.players[p].soul_deck = len(deck.soul)
            for d in deck.main:
                impl = self._resolve(impls, d.code, missing)
                if impl is None:
                    continue
                card = CardInstance(uid, d, impl, p)
                self.cards[uid] = card
                self.players[p].deck.append(card)
                uid += 1
        if missing:
            raise UnimplementedCardError(
                "no implementation for: " + ", ".join(sorted(set(missing))))

        self.turn = 0
        self.active = 0
        self.first_player = 0
        self.phase = "setup"
        self.battle: Battle | None = None
        self.pending: list[Trigger] = []
        self.night = False
        self.winner: int | None = None
        self.reason = ""
        self.stats = [PlayerStats(), PlayerStats()]
        self.history: list[dict] = []
        self._deploy_seq = 0
        self._deploy_order: dict[int, int] = {}

    @staticmethod
    def _resolve(impls: ImplResolver, code: str, missing: list[str]) -> CardImpl | None:
        try:
            return impls(code)
        except (KeyError, LookupError):
            missing.append(code)
            return None

    # ================================================================ logging
    def log(self, msg: str) -> None:
        if self.logging:
            self.lines.append(msg)

    def pname(self, p: int) -> str:
        return f"P{p + 1}"

    def _status_line(self) -> str:
        parts = []
        for ps in self.players:
            parts.append(
                f"{self.pname(ps.idx)}: life {ps.life}, hand {len(ps.hand)}, deck {len(ps.deck)}, "
                f"souls {ps.souls_standing}/{ps.souls}, grave {len(ps.graveyard)}")
        return " | ".join(parts)

    def _board_line(self, p: int) -> str:
        ps = self.players[p]
        if not ps.base:
            return f"  {self.pname(p)} base: (empty)"
        cards = []
        for c in ps.base:
            s = f"{c.name} {self.power(c)}"
            if c.is_pal:
                s += f"/S{self.strike(c)}"
            if c.rested:
                s += " (rested)"
            if c.damage:
                s += f" dmg {c.damage}"
            cards.append(s)
        return f"  {self.pname(p)} base: " + ", ".join(cards)

    # ================================================================ queries
    def card(self, uid: int) -> CardInstance:
        return self.cards[uid]

    def opponent(self, p: int) -> int:
        return 1 - p

    def power(self, c: CardInstance) -> int:
        v = c.defn.power + sum(m.amount for m in c.mods if m.stat == "power")
        v += c.impl.power_mod(self, c)
        if c.kw("nocturnal") and self.night:  # CR 12.13
            v += 300
        return v

    def strike(self, c: CardInstance) -> int:
        v = c.defn.strike + sum(m.amount for m in c.mods if m.stat == "strike")
        return v + c.impl.strike_mod(self, c)

    def cost(self, c: CardInstance) -> int:
        return max(0, c.defn.cost + c.impl.cost_mod(self, c))

    def on_base(self, c: CardInstance, incarnation: int | None = None) -> bool:
        return c.zone is Zone.BASE and (incarnation is None or c.incarnation == incarnation)

    def attack_targets(self, attacker: CardInstance) -> list[int | None]:
        """Legal attack targets (CR 9.2.3, Taunt 12.10, Assault 12.15). None = player."""
        opp = self.players[self.opponent(attacker.owner)]
        targets: list[int | None] = [None]
        for c in opp.base:
            if c.is_pal and (c.rested or attacker.kw("assault")):
                targets.append(c.uid)
            elif c.is_structure and (c.rested or self.rules.structures_attackable == "any"):
                targets.append(c.uid)  # A2: configurable. Gear is never a target (CR 9.2.3)
        taunters = [t for t in targets if t is not None and self.card(t).kw("taunt")]
        return taunters or targets

    def can_attack(self, c: CardInstance) -> bool:
        return (c.is_pal and c.zone is Zone.BASE and not c.rested
                and c.owner == self.active and c.impl.can_attack(self, c))

    def _can_activate(self, p: int, c: CardInstance, i: int, quick_only: bool) -> bool:
        a = c.impl.acts[i]
        if quick_only and not a.quick:
            return False
        if a.once_per_turn and c.act_uses.get(i, 0) >= 1:
            return False
        if self.players[p].souls_standing < a.souls:
            return False
        if a.assign and not any(not x.rested for x in self.players[p].pals):
            return False
        if a.can_pay_extra and not a.can_pay_extra(self, c):
            return False
        if a.condition and not a.condition(self, c):
            return False
        return True

    def legal_actions(self, p: int) -> list[Action]:
        """Main-phase actions for the turn player (CR 8)."""
        ps = self.players[p]
        acts: list[Action] = []
        seen: set[str] = set()
        for c in ps.hand:
            if c.code in seen or c.type is CardType.SOUL:
                continue
            seen.add(c.code)
            if ps.souls_standing >= self.cost(c) and c.impl.can_play(self, c):
                acts.append(PlayCard(c.uid))
        for c in ps.base:
            for i, a in enumerate(c.impl.acts):
                if not self._can_activate(p, c, i, quick_only=False):
                    continue
                if a.assign:
                    for pal in ps.pals:
                        if not pal.rested:
                            acts.append(Activate(c.uid, i, pal.uid))
                else:
                    acts.append(Activate(c.uid, i))
        for c in ps.pals:
            if self.can_attack(c):
                for t in self.attack_targets(c):
                    acts.append(Attack(c.uid, t))
        if not ps.soul_draw_used and ps.souls_standing >= SOUL_DRAW_COST:
            acts.append(SoulDraw())
        acts.append(EndMain())
        return acts

    def quick_actions(self, p: int) -> list[Action]:
        """What the non-turn player may do in the Quick step (CR 9.5)."""
        ps = self.players[p]
        acts: list[Action] = [Pass()]
        seen: set[str] = set()
        for c in ps.hand:
            if c.code in seen:
                continue
            seen.add(c.code)
            if c.kw("interrupt"):
                if ps.souls_standing >= 1:
                    acts.append(UseInterrupt(c.uid, None))
                other_codes: set[str] = set()
                for o in ps.hand:
                    if o is not c and o.code not in other_codes:
                        other_codes.add(o.code)
                        acts.append(UseInterrupt(c.uid, o.uid))
            if (c.type is CardType.EVENT and c.impl.quick
                    and ps.souls_standing >= self.cost(c) and c.impl.can_play(self, c)):
                acts.append(PlayCard(c.uid))
        for c in ps.base:
            for i, a in enumerate(c.impl.acts):
                if self._can_activate(p, c, i, quick_only=True):
                    if a.assign:
                        acts += [Activate(c.uid, i, x.uid) for x in ps.pals if not x.rested]
                    else:
                        acts.append(Activate(c.uid, i))
        return acts

    # ================================================================ decisions
    def ask(self, decision: Decision) -> list:
        assert self.agents is not None
        if not decision.options or decision.max == 0:
            return []
        choice = list(self.agents[decision.player].choose(self, decision))
        if not (decision.min <= len(choice) <= decision.max) or any(
                x not in decision.options for x in choice):
            raise ValueError(f"illegal choice {choice} for {decision}")
        return choice

    def choose_cards(self, player: int, prompt: str, candidates: list[CardInstance],
                     n: int = 1, up_to: bool = False) -> list[CardInstance]:
        """CR 10.6.3: choose as many as possible up to n (or 0..n for 'up to')."""
        if not candidates:
            return []
        k = min(n, len(candidates))
        uids = self.ask(Decision("target", player, prompt, [c.uid for c in candidates],
                                 min=0 if up_to else k, max=k))
        return [self.card(u) for u in uids]

    def may(self, player: int, prompt: str) -> bool:
        return self.ask(Decision("may", player, prompt, [True, False]))[0]

    # ================================================================ zones
    def _zone_list(self, c: CardInstance) -> list[CardInstance] | None:
        ps = self.players[c.owner]
        return {Zone.DECK: ps.deck, Zone.HAND: ps.hand, Zone.BASE: ps.base,
                Zone.GRAVEYARD: ps.graveyard, Zone.EXILE: ps.exile}.get(c.zone)

    def move(self, c: CardInstance, zone: Zone, top: bool = True) -> None:
        """Move a card between zones. Leaving the base makes it a new card (CR 4.1.4)."""
        src = self._zone_list(c)
        if src is not None and c in src:
            src.remove(c)
        left_base = c.zone is Zone.BASE and zone is not Zone.BASE
        from_zone = c.zone
        if left_base:
            self._on_leave_base(c, zone)
            c.reset_for_new_zone()
        c.zone = zone
        dst = self._zone_list(c)
        assert dst is not None
        if zone is Zone.DECK and top:
            dst.insert(0, c)
        else:
            dst.append(c)
        if left_base:
            self.emit(Event("left_base", c.owner, c.uid, {"to": zone, "from": from_zone}),
                      extra=[c])

    def draw(self, p: int, n: int = 1) -> list[CardInstance]:
        ps = self.players[p]
        drawn = []
        for _ in range(n):
            if not ps.deck:  # CR 1.3.2: nothing happens; deck-out is checked at check timing
                break
            c = ps.deck[0]
            self.move(c, Zone.HAND)
            drawn.append(c)
            self.stats[p].drawn.append(c.code)
        if drawn:
            self.log(f"  {self.pname(p)} draws {', '.join(c.name for c in drawn)}")
        return drawn

    def discard(self, c: CardInstance) -> None:
        self.move(c, Zone.GRAVEYARD)

    def send_to_graveyard(self, c: CardInstance, why: str = "") -> None:
        if c.zone is Zone.BASE:
            self.log(f"  {c.label()} ({self.pname(c.owner)}) goes to the graveyard"
                     + (f" ({why})" if why else ""))
        self.move(c, Zone.GRAVEYARD)

    def return_to_hand(self, c: CardInstance) -> None:
        self.log(f"  {c.label()} returns to {self.pname(c.owner)}'s hand")
        self.move(c, Zone.HAND)

    def _on_leave_base(self, c: CardInstance, to: Zone) -> None:
        """Retaliate (CR 12.12) and Breakthrough (CR 12.14) look at the battle."""
        b = self.battle
        if b is None or to is not Zone.GRAVEYARD:
            return
        opp = b.opponent_of(c)
        if opp is None:
            return
        if c.kw("retaliate") and self.on_base(opp):
            inc = opp.incarnation

            def retaliate(g: Game, opp=opp, inc=inc, src=c) -> None:
                if g.on_base(opp, inc):
                    g.send_to_graveyard(opp, f"Retaliate from {src.name}")
            self.pending.append(Trigger(c.owner, f"Retaliate ({c.name})", retaliate, c.uid))
        if c is b.target and b.attacker.kw("breakthrough"):
            dmg = self.strike(b.attacker)  # last known information if it has left too
            att = b.attacker

            def breakthrough(g: Game, victim=c.owner, dmg=dmg, att=att) -> None:
                g.deal_player_damage(victim, dmg, att)
            self.pending.append(Trigger(b.attacker_player, f"Breakthrough ({att.name})",
                                        breakthrough, att.uid))

    # ================================================================ effects API
    def pay_souls(self, p: int, n: int) -> None:
        ps = self.players[p]
        if ps.souls_standing < n:
            raise ValueError(f"{self.pname(p)} cannot pay {n} souls")
        ps.souls_rested += n

    def add_mod(self, c: CardInstance, stat: str, amount: int, until: str | None = "turn",
                source: str = "") -> None:
        c.mods.append(Mod(stat, amount, until, source))
        self.log(f"  {c.name} {stat} {amount:+d}" + (f" until end of {until}" if until else ""))

    def deal_card_damage(self, c: CardInstance, n: int, source: CardInstance | None = None) -> None:
        # Only Pals and structures have damage (CR 4.4.4); gear can't be damaged.
        if n > 0 and c.zone is Zone.BASE and (c.is_pal or c.is_structure):
            c.damage += n
            self.log(f"  {c.name} takes {n} damage (total {c.damage}/{self.power(c)})")

    def gain_life(self, p: int, n: int) -> None:
        self.players[p].life += n
        self.log(f"  {self.pname(p)} gains {n} life ({self.players[p].life})")

    def rest(self, c: CardInstance) -> None:
        c.rested = True

    def stand(self, c: CardInstance) -> None:
        c.rested = False

    def nullify_attack(self) -> None:
        if self.battle is not None:
            self.battle.nullified = True
            self.log("  the attack is nullified")

    def deal_player_damage(self, p: int, n: int, source: CardInstance | None = None) -> None:
        """Deal n damage to a player and run the damage check (CR 11.2).

        Player damage resolution is an interrupt-type rule action, so it happens
        right here. Flip cards one at a time into the graveyard; a lucky card
        cancels all of it; otherwise lose n life."""
        if n <= 0:
            return
        ps = self.players[p]
        ps.damage_taken += n
        src = source.name if source else "an effect"
        self.log(f"  {self.pname(p)} takes {n} damage from {src}: damage check")
        flipped = 0
        while True:
            if ps.deck:
                c = ps.deck[0]
                self.move(c, Zone.GRAVEYARD)
                flipped += 1
                if c.defn.lucky:
                    self.log(f"    flip {flipped}: {c.name} (LUCKY): damage cancelled")
                    self.stats[p].lucky_saves += 1
                    break
                self.log(f"    flip {flipped}: {c.name}")
            if flipped >= ps.damage_taken or not ps.deck:
                lost = ps.damage_taken
                ps.life -= lost
                if source is not None:
                    self.stats[p].life_lost_to[source.code] += lost
                self.log(f"    {self.pname(p)} loses {lost} life -> {ps.life}")
                self.emit(Event("life_lost", p, None, {"amount": lost}))
                break
        ps.damage_taken = 0

    # ================================================================ triggers & check timing
    def emit(self, event: Event, extra: Sequence[CardInstance] = ()) -> None:
        """Broadcast an event to cards in both bases (turn player first) plus `extra`."""
        seen: set[int] = set()
        for p in (self.active, self.opponent(self.active)):
            for c in list(self.players[p].base) + [x for x in extra if x.owner == p]:
                if c.uid in seen:
                    continue
                seen.add(c.uid)
                self.pending.extend(c.impl.triggers(self, c, event))

    def queue(self, master: int, name: str, fn: Callable[["Game"], None],
              source: CardInstance | None = None) -> None:
        self.pending.append(Trigger(master, name, fn, source.uid if source else None))

    def check_timing(self) -> None:
        """CR 10.5.3: rule actions until none remain, then one trigger at a time
        (turn player's first, in the order they triggered: A5)."""
        while True:
            if self._rule_actions():
                continue
            nxt = next((t for t in self.pending if t.master == self.active), None)
            if nxt is None:
                nxt = next(iter(self.pending), None)
            if nxt is None:
                return
            self.pending.remove(nxt)
            self.log(f"  [trigger] {nxt.name}")
            nxt.fn(self)

    def _rule_actions(self) -> bool:
        # Losing verdict (CR 11.3)
        lost = [ps.idx for ps in self.players if ps.life <= 0 or not ps.deck]
        if lost:
            if len(lost) == 2:
                self.winner, self.reason = None, "draw"
            else:
                loser = self.players[lost[0]]
                self.winner = self.opponent(lost[0])
                self.reason = "life" if loser.life <= 0 else "deckout"
            self.log(f"GAME OVER: {self._result_text()}")
            raise GameOver()
        # Lethal damage (CR 11.4)
        dead = [c for ps in self.players for c in ps.base
                if (c.is_pal or c.is_structure) and c.damage > 0 and c.damage >= self.power(c)]
        for c in dead:
            self.send_to_graveyard(c, "defeated")
        if dead:
            return True
        # Overloaded Pals (CR 11.5)
        for ps in self.players:
            pals = ps.pals
            if len(pals) > PAL_LIMIT:
                excess = len(pals) - PAL_LIMIT
                newest = max(self._deploy_order.get(c.uid, 0) for c in pals)
                older = [c for c in pals if self._deploy_order.get(c.uid, 0) != newest]
                gone = self.choose_cards(ps.idx, f"Too many Pals: choose {excess} to send to the "
                                         "graveyard", older, n=excess)
                for c in gone:
                    self.send_to_graveyard(c, "Pal limit")
                return True
        return False

    def _result_text(self) -> str:
        if self.winner is None:
            return "draw"
        return f"{self.pname(self.winner)} ({self.deck_names[self.winner]}) wins by {self.reason}"

    # ================================================================ actions
    def perform(self, action: Action) -> None:
        if isinstance(action, PlayCard):
            self.play_card(self.card(action.uid).owner, self.card(action.uid))
        elif isinstance(action, Activate):
            c = self.card(action.uid)
            self.activate(c.owner, c, action.index, action.assign_uid)
        elif isinstance(action, Attack):
            self.attack(self.card(action.attacker_uid), action.target_uid)
        elif isinstance(action, SoulDraw):
            ps = self.players[self.active]
            self.pay_souls(self.active, SOUL_DRAW_COST)
            ps.soul_draw_used = True
            self.log(f"{self.pname(self.active)} rests {SOUL_DRAW_COST} souls to draw 1")
            self.draw(self.active)
        elif isinstance(action, UseInterrupt):
            self.use_interrupt(action)
        elif isinstance(action, (EndMain, Pass)):
            return
        else:
            raise TypeError(action)
        self.check_timing()

    def play_card(self, p: int, c: CardInstance) -> None:
        cost = self.cost(c)
        self.pay_souls(p, cost)
        self.stats[p].played.append((self.turn, c.code))
        self.log(f"{self.pname(p)} plays {c.label()} (cost {cost})")
        if c.type is CardType.EVENT:
            self.players[p].hand.remove(c)
            c.zone = Zone.RESOLUTION  # CR 10.6.2.4.2
            c.impl.resolve_event(self, c)
            if c.zone is Zone.RESOLUTION:
                self.move(c, Zone.GRAVEYARD)
        else:
            self.deploy(c)

    def deploy(self, c: CardInstance) -> None:
        """CR 5.15: put a Pal/structure/gear onto its master's base."""
        self.move(c, Zone.BASE)
        c.rested = False
        c.deployed_turn = self.turn
        self._deploy_seq += 1
        self._deploy_order[c.uid] = self._deploy_seq
        if c.impl.overrides("on_deploy"):
            self.queue(c.owner, f"On Deploy: {c.name}", lambda g, c=c: c.impl.on_deploy(g, c), c)
        self.emit(Event("deployed", c.owner, c.uid))

    def activate(self, p: int, c: CardInstance, index: int, assign_uid: int | None = None) -> None:
        a = c.impl.acts[index]
        self.pay_souls(p, a.souls)
        ctx: dict = {}
        if a.assign:
            pal = self.card(assign_uid) if assign_uid is not None else None
            if pal is None or pal.rested or pal.owner != p or not pal.is_pal:
                raise ValueError("assign cost needs a standing Pal you control")
            self.assign(pal, c)
            ctx["assigned"] = pal
        if a.pay_extra:
            a.pay_extra(self, c)
        c.act_uses[index] = c.act_uses.get(index, 0) + 1
        self.log(f"{self.pname(p)} activates {c.name}: {a.name}")
        a.effect(self, c, ctx)

    def assign(self, pal: CardInstance, structure: CardInstance) -> None:
        """CR 5.17: rest a standing Pal; it is now assigned to the structure."""
        pal.rested = True
        pal.assigned_to = structure.uid
        self.log(f"  {pal.name} is assigned to {structure.name}")
        if pal.impl.overrides("on_assign"):
            self.queue(pal.owner, f"On Assign: {pal.name}",
                       lambda g, c=pal: c.impl.on_assign(g, c), pal)
        n = pal.kw("serious")
        if n:
            def serious(g: Game, pal=pal, n=int(n)) -> None:  # CR 12.7
                pals = [x for ps in g.players for x in ps.pals]
                for t in g.choose_cards(pal.owner, f"Serious {n}: choose a Pal", pals):
                    g.add_mod(t, "power", n, "turn", f"Serious ({pal.name})")
            self.queue(pal.owner, f"Serious {n}: {pal.name}", serious, pal)
        self.emit(Event("assigned", pal.owner, pal.uid, {"structure": structure.uid}))

    def use_interrupt(self, a: UseInterrupt) -> None:
        c = self.card(a.uid)
        p = c.owner
        if a.discard_uid is None:
            self.pay_souls(p, 1)
            how = "resting 1 soul"
        else:
            other = self.card(a.discard_uid)
            self.discard(other)
            how = f"discarding {other.name}"
        self.discard(c)
        self.log(f"{self.pname(p)} uses Interrupt: {c.name} ({how})")
        self.nullify_attack()

    # ================================================================ battle
    def attack(self, att: CardInstance, target_uid: int | None) -> None:
        p = att.owner
        opp = self.opponent(p)
        if not self.can_attack(att) or target_uid not in self.attack_targets(att):
            raise ValueError(f"illegal attack {att.label()} -> {target_uid}")
        tgt = self.card(target_uid) if target_uid is not None else None
        self.log(f"{self.pname(p)}: {att.name} ({self.power(att)}/S{self.strike(att)}) attacks "
                 + (f"{tgt.name}" if tgt else self.pname(opp)))
        att.rested = True  # CR 9.3.2
        self.stats[p].attacks += 1
        self.battle = b = Battle(att, p, tgt, opp)
        att_inc = att.incarnation
        brave = att.kw("brave")
        if brave:
            self.queue(p, f"Brave {brave}: {att.name}",
                       lambda g, c=att, n=int(brave): g.add_mod(c, "power", n, "turn", "Brave"), att)
        if att.impl.overrides("on_attack"):
            self.queue(p, f"On Attack: {att.name}", lambda g, c=att: c.impl.on_attack(g, c), att)
        self.emit(Event("attack", p, att.uid, {"target": target_uid}))
        self.check_timing()

        # Block declaration step (CR 9.4)
        if not b.nullified and att.impl.can_be_blocked(self, att) and not att.kw("stealth"):
            blockers = [c for c in self.players[opp].pals if not c.rested and c is not b.target]
            if blockers:
                chosen = self.ask(Decision("block", opp, f"Block {att.name}?",
                                           [c.uid for c in blockers], min=0, max=1,
                                           context={"attacker": att.uid, "target": target_uid}))
                if chosen:
                    blk = self.card(chosen[0])
                    blk.rested = True
                    b.target = blk
                    b.blocked_by = blk
                    self.log(f"  {self.pname(opp)} blocks with {blk.name} ({self.power(blk)})")
                    self.emit(Event("block", opp, blk.uid, {"attacker": att.uid}))
        self.check_timing()

        # Quick step (CR 9.5)
        assert self.agents is not None
        while not b.nullified:
            options = self.quick_actions(opp)
            if len(options) == 1:
                break
            choice = self.agents[opp].choose_action(self, opp, options)
            if isinstance(choice, Pass):
                break
            if choice not in options:
                raise ValueError(f"illegal quick action {choice}")
            if isinstance(choice, UseInterrupt):
                self.use_interrupt(choice)
            elif isinstance(choice, PlayCard):
                self.play_card(opp, self.card(choice.uid))
            elif isinstance(choice, Activate):
                self.activate(opp, self.card(choice.uid), choice.index, choice.assign_uid)
            self.check_timing()

        # Damage step (CR 9.6)
        if not b.nullified:
            tgt = b.target
            if self.on_base(att, att_inc) and (tgt is None or self.on_base(tgt)):
                if tgt is None:
                    self.deal_player_damage(opp, self.strike(att), att)
                elif tgt.is_pal:
                    pa, pt = self.power(att), self.power(tgt)
                    if pa > 0:
                        tgt.damage += pa
                    if pt > 0:
                        att.damage += pt
                    self.log(f"  battle: {att.name} deals {max(pa, 0)} to {tgt.name}, "
                             f"{tgt.name} deals {max(pt, 0)} back")
                else:
                    self.deal_card_damage(tgt, self.power(att), att)
            self.check_timing()

        # End of battle step (CR 9.7)
        self.emit(Event("battle_end", p, att.uid))
        self.check_timing()
        for ps in self.players:
            for c in ps.base:
                c.mods = [m for m in c.mods if m.until != "battle"]
        self.battle = None

    # ================================================================ turn structure
    def setup(self) -> None:
        """CR 6.2."""
        assert self.agents is not None
        self.first_player = self.active = self.rng.randrange(2)
        for ps in self.players:
            self.rng.shuffle(ps.deck)
        second = self.players[self.opponent(self.first_player)]
        second.soul_deck -= 1
        second.souls += 1
        self.log(f"Seed {self.seed}. P1 = {self.deck_names[0]}, P2 = {self.deck_names[1]}")
        self.log(f"{self.pname(self.first_player)} goes first; "
                 f"{self.pname(second.idx)} starts with 1 soul")
        for p in (self.first_player, second.idx):
            self.draw(p, OPENING_HAND)
        for p in (self.first_player, second.idx):
            ps = self.players[p]
            if self.agents[p].choose_redraw(self, p):
                self.log(f"{self.pname(p)} redraws")
                for c in list(ps.hand):
                    self.move(c, Zone.DECK)
                self.rng.shuffle(ps.deck)
                ps.redrew = self.stats[p].redrew = True
                self.draw(p, OPENING_HAND)
            else:
                self.log(f"{self.pname(p)} keeps")
        for p in (0, 1):
            self.stats[p].opening_hand = [c.code for c in self.players[p].hand]
            self.players[p].life = STARTING_LIFE

    def play(self) -> GameResult:
        try:
            self.setup()
            while self.turn < self.turn_cap:
                self.take_turn()
            self.winner, self.reason = None, "turn_cap"
            self.log(f"GAME OVER: turn cap ({self.turn_cap}) reached, draw")
        except GameOver:
            pass
        return GameResult(self.seed, self.winner, self.reason, self.turn, self.first_player,
                          [ps.life for ps in self.players], self.stats, self.history)

    def take_turn(self) -> None:
        assert self.agents is not None
        self.turn += 1
        p = self.active
        ps = self.players[p]
        self.log("")
        self.log(f"=== Turn {self.turn}: {self.pname(p)} ({self.deck_names[p]}) ===")

        self.phase = "stand"  # CR 7.2
        for c in ps.base:
            c.rested = False
        ps.souls_rested = 0
        self.emit(Event("turn_start", p))
        self.check_timing()

        self.phase = "draw"  # CR 7.3
        if self.turn == 1:
            self.log(f"  {self.pname(p)} skips the draw (first turn)")
        else:
            self.emit(Event("draw_phase", p))
            self.check_timing()
            self.draw(p)
            self.check_timing()

        self.phase = "soul"  # CR 7.4
        n = min(SOULS_PER_TURN, ps.soul_deck)
        ps.soul_deck -= n
        ps.souls += n
        self.log(f"  {self.pname(p)} gains {n} soul(s): {ps.souls} total")
        self.check_timing()

        self.phase = "main"  # CR 7.5
        self.log("  " + self._status_line())
        for _ in range(MAX_ACTIONS_PER_TURN):
            self.check_timing()
            actions = self.legal_actions(p)
            action = self.agents[p].choose_action(self, p, actions)
            if action not in actions:
                raise ValueError(f"illegal action {action}")
            if isinstance(action, EndMain):
                break
            self.perform(action)
        else:
            self.log(f"  {self.pname(p)} hit the action limit; main phase ends")

        self.phase = "end"  # CR 7.6
        for c in ps.base:
            if c.kw("vigilance"):
                self.queue(p, f"Vigilance: {c.name}", lambda g, c=c: g.stand(c), c)
        self.emit(Event("turn_end", p))
        self.check_timing()
        for q in self.players:
            for c in q.base:
                c.damage = 0
                c.mods = [m for m in c.mods if m.until not in ("turn", "battle")]
                c.act_uses.clear()
                c.assigned_to = None
        ps.soul_draw_used = False
        self.log(self._board_line(0))
        self.log(self._board_line(1))
        self.history.append({
            "turn": self.turn, "active": p,
            "life": [q.life for q in self.players],
            "hand": [len(q.hand) for q in self.players],
            "deck": [len(q.deck) for q in self.players],
            "pals": [len(q.pals) for q in self.players],
            "board_power": [sum(self.power(c) for c in q.pals) for q in self.players],
        })
        self.active = self.opponent(p)

    # ================================================================ search seam
    def clone(self, agents: Sequence[Agent]) -> "Game":
        """Deep copy for lookahead. Only valid at a decision point with no
        pending triggers (e.g. choosing a main-phase action)."""
        if self.pending:
            raise RuntimeError("cannot clone with pending triggers")
        saved, self.agents = self.agents, None
        try:
            g = copy.deepcopy(self)
        finally:
            self.agents = saved
        g.agents = list(agents)
        g.logging = False
        g.lines = []
        return g
