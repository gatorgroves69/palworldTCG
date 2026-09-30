"""Bot behaviour checks with the real M1 cards."""
import pytest

from bots import HeuristicBot, RuleBot
from bots.heuristic import determinize
import random

import cards
from engine import Attack, Decision, EndMain, Game, SoulDraw, Zone
from tests.test_cards_m1 import DEFAULT_PATH, decks, put, real_game  # noqa: F401

pytestmark = pytest.mark.skipif(not DEFAULT_PATH.exists(), reason="data/cards.json missing")


def test_clone_replays_identically(decks):
    """A clone continued with the same bots ends exactly like the original."""
    g = Game(decks, cards.REGISTRY, [RuleBot(1), RuleBot(2)], seed=5)
    g.setup()
    for _ in range(4):
        g.take_turn()
    c = g.clone([RuleBot(1), RuleBot(2)])
    r1, r2 = g.play_on(), c.play_on()
    assert (r1.winner, r1.turns, r1.life) == (r2.winner, r2.turns, r2.life)


def test_determinize_keeps_counts_and_hides_order(decks):
    g, _ = real_game(decks)
    put(g, 1, "BP01-047", Zone.HAND)
    c = g.clone([RuleBot(), RuleBot()])
    determinize(c, 0, random.Random(3))
    assert len(c.players[1].hand) == 1 and len(c.players[1].deck) == len(g.players[1].deck)
    assert sorted(x.uid for x in c.players[1].hand + c.players[1].deck) == \
        sorted(x.uid for x in g.players[1].hand + g.players[1].deck)


def test_heuristic_deploys_before_soul_draw(decks):
    g, _ = real_game(decks)
    g.players[0].souls = 3
    put(g, 0, "TD01-023", Zone.HAND)  # Lamball ◇2
    bot = HeuristicBot(0)
    a = bot.choose_action(g, 0, g.legal_actions(0))
    assert not isinstance(a, (SoulDraw, EndMain))


def test_rulebot_interrupts_lethal(decks):
    g, _ = real_game(decks)
    g.players[1].life = 2
    att = put(g, 0, "BP01-029")  # S2
    i = put(g, 1, "TD02-017", Zone.HAND)
    g.agents[1] = RuleBot()
    g.perform(Attack(att.uid, None))
    assert i.zone is Zone.GRAVEYARD and g.players[1].life == 2


def test_rulebot_blocks_with_a_survivor(decks):
    g, _ = real_game(decks)
    att = put(g, 0, "BP01-032")  # Fuack 200
    big = put(g, 1, "BP01-026")  # Relaxaurus 1200
    d = Decision("block", 1, "", [big.uid], min=0, max=1,
                 context={"attacker": att.uid, "target": None})
    assert RuleBot().choose(g, d) == [big.uid]


def test_rulebot_harm_targets_opponent(decks):
    g, _ = real_game(decks)
    mine = put(g, 0, "BP01-029")
    theirs = put(g, 1, "BP01-025")
    d = Decision("target", 0, "", [mine.uid, theirs.uid], min=0, max=1,
                 context={"intent": "harm", "amount": 900})
    assert RuleBot().choose(g, d) == [theirs.uid]


def test_rulebot_puts_lucky_on_top(decks):
    g, _ = real_game(decks)
    a = put(g, 1, "BP01-047", Zone.HAND)
    lucky = put(g, 1, "BP01-027", Zone.HAND)
    d = Decision("target", 1, "", [a.uid, lucky.uid], min=0, max=1, context={"intent": "top"})
    assert RuleBot().choose(g, d) == [lucky.uid]
