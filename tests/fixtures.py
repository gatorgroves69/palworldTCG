"""Test-only cards and helpers. These are NOT real cards: codes start with 'T-'."""
from __future__ import annotations

from collections import deque

from bots.base import Bot
from cards.registry import Registry
from engine import (CardDef, CardImpl, CardType, Color, Deck, EndMain, Game, Pass, Zone)

R = CardType


def pal(code, power, strike=1, lucky=False, color=Color.RED, cost=1):
    return CardDef(code, f"Pal {code}", R.PAL, color, cost, power, strike, lucky)


CARDS = {
    "T-100": pal("T-100", 100),
    "T-200": pal("T-200", 200),
    "T-300": pal("T-300", 300, strike=2, cost=2),
    "T-LUCKY": pal("T-LUCKY", 100, lucky=True),
    "T-STEALTH": pal("T-STEALTH", 200),
    "T-TAUNT": pal("T-TAUNT", 400),
    "T-ASSAULT": pal("T-ASSAULT", 300),
    "T-RETAL": pal("T-RETAL", 100),
    "T-BREAK": pal("T-BREAK", 500),
    "T-BRAVE": pal("T-BRAVE", 200),
    "T-VIG": pal("T-VIG", 200),
    "T-INT": CardDef("T-INT", "Interrupt Pal", R.PAL, Color.BLUE, 2, 200, 1),
    "T-WALL": CardDef("T-WALL", "Wall", R.STRUCTURE, Color.RED, 2, 500, 0),
    "T-GEAR": CardDef("T-GEAR", "Gear", R.GEAR, Color.RED, 1, 0, 0),
    "T-DRAW2": CardDef("T-DRAW2", "Draw Two", R.EVENT, Color.BLUE, 1),
    "T-SOUL": CardDef("T-SOUL", "Soul", R.SOUL),
    "T-GREEN": pal("T-GREEN", 100, color=Color.GREEN),
    "T-UNIMPL": pal("T-UNIMPL", 100),
}


def make_registry() -> Registry:
    reg = Registry()
    for code in ("T-100", "T-200", "T-300", "T-LUCKY", "T-SOUL", "T-GREEN"):
        reg.vanilla(code)

    def kw(code, **k):
        reg.register(type(f"K_{code}", (CardImpl,), {"code": code, "keywords": k}))

    kw("T-STEALTH", stealth=True)
    kw("T-TAUNT", taunt=True)
    kw("T-ASSAULT", assault=True)
    kw("T-RETAL", retaliate=True)
    kw("T-BREAK", breakthrough=True)
    kw("T-BRAVE", brave=200)
    kw("T-VIG", vigilance=True)
    kw("T-INT", interrupt=True)
    reg.vanilla("T-WALL")
    reg.vanilla("T-GEAR")

    @reg.register
    class DrawTwo(CardImpl):
        code = "T-DRAW2"
        text = "Draw 2 cards."

        def resolve_event(self, game, card):
            game.draw(card.owner, 2)

    return reg


def deck(name="test", fill="T-100", extra=(), soul=10) -> Deck:
    main = [CARDS[c] for c in extra]
    main += [CARDS[fill]] * (50 - len(main))
    return Deck(name, main, [CARDS["T-SOUL"]] * soul)


RED_PALS = ["T-100", "T-200", "T-300", "T-LUCKY", "T-STEALTH", "T-TAUNT", "T-ASSAULT",
            "T-RETAL", "T-BREAK", "T-BRAVE", "T-VIG"]


def legal_deck(name="legal") -> Deck:
    """44 red Pals (11 names x4), 4 structures, 2 blue Interrupt Pals: 2 colours, 4 lucky."""
    return deck(name, extra=[c for c in RED_PALS for _ in range(4)] + ["T-WALL"] * 4
                + ["T-INT"] * 2)


def toolbox(name="toolbox") -> Deck:
    """Not construction-legal: 3 of every test card, for arranging board states."""
    codes = RED_PALS + ["T-INT", "T-WALL", "T-DRAW2", "T-GEAR"]
    return deck(name, extra=[c for c in codes for _ in range(3)])


class ScriptedBot(Bot):
    """Plays queued actions/answers; otherwise ends the turn, passes and never blocks."""

    def __init__(self):
        super().__init__(0)
        self.actions: deque = deque()
        self.answers: deque = deque()
        self.redraw = False

    def choose_redraw(self, game, player):
        return self.redraw

    def choose_action(self, game, player, actions):
        if self.actions:
            a = self.actions.popleft()
            assert a in actions, f"{a} not legal; legal={actions}"
            return a
        return next(a for a in actions if isinstance(a, (EndMain, Pass)))

    def choose(self, game, decision):
        if self.answers:
            return self.answers.popleft()
        return list(decision.options[: decision.min])


def make_game(d0=None, d1=None, seed=1, log=True, rules=None):
    bots = [ScriptedBot(), ScriptedBot()]
    g = Game([d0 or deck("A"), d1 or deck("B")], make_registry(), bots, seed=seed, log=log,
             rules=rules)
    return g, bots


def staged(d0=None, d1=None, active=0, rules=None):
    """A game past setup, at player `active`'s main phase, with empty hands,
    8 standing souls each and life 10. Use `put` to arrange cards."""
    g, bots = make_game(d0 or toolbox("A"), d1 or toolbox("B"), rules=rules)
    g.setup()
    for ps in g.players:
        for c in list(ps.hand):
            g.move(c, Zone.DECK)
        ps.souls, ps.soul_deck, ps.souls_rested = 8, 2, 0
        # Lucky cards to the bottom so damage checks are predictable; tests that
        # want a lucky flip use stack_top.
        ps.deck.sort(key=lambda c: c.defn.lucky)
    g.active = active
    g.turn = 3
    g.phase = "main"
    return g, bots


def put(g, p, code, zone=Zone.BASE, rested=False):
    """Move a card with `code` from player p's deck into `zone`."""
    c = next(c for c in g.players[p].deck if c.code == code)
    if zone is Zone.BASE:
        g.deploy(c)
        g.pending.clear()
        c.rested = rested
    else:
        g.move(c, zone)
    return c


def stack_top(g, p, codes):
    """Put cards with these codes on top of player p's deck, in order."""
    for code in reversed(codes):
        c = next(c for c in g.players[p].deck if c.code == code)
        g.players[p].deck.remove(c)
        g.players[p].deck.insert(0, c)
