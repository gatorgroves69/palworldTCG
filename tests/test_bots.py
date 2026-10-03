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


def test_determinize_keeps_zone_labels(decks):
    g, _ = real_game(decks)
    for code in ("BP01-047", "BP01-047", "BP01-048"):
        put(g, 1, code, Zone.HAND)
    c = g.clone([RuleBot(), RuleBot()])
    determinize(c, 0, random.Random(1))
    ps = c.players[1]
    assert all(x.zone is Zone.HAND for x in ps.hand)
    assert all(x.zone is Zone.DECK for x in ps.deck)
    c.draw(1, 2)  # would duplicate cards if labels were stale
    assert len(ps.hand) == 5 and len({x.uid for x in ps.hand + ps.deck}) == len(ps.hand + ps.deck)


@pytest.mark.parametrize("name", ["fast", "search", "plan", "heuristic-learned"])
def test_new_bots_finish_games(decks, name):
    from bots import BOTS
    g = Game(decks, cards.REGISTRY, [BOTS[name](1), BOTS[name](2)], seed=11)
    r = g.play()
    assert r.reason in ("life", "deckout", "draw", "turn_cap")


def test_features_match_names(decks):
    from bots.features import FEATURES, features
    g, _ = real_game(decks)
    assert len(features(g, 0, True)) == len(FEATURES)


def test_learned_eval_prefers_more_life(decks):
    from bots.evaluate import evaluate_learned
    g, _ = real_game(decks)
    a = evaluate_learned(g, 0)
    g.players[1].life = 3
    assert evaluate_learned(g, 0) > a


# ---------------------------------------------------------------- quick-step tricks (J7)
def _box_game():
    from tests.test_cards_m2 import G
    from cards import REGISTRY
    from cards.db import load_card_db
    from engine import CardType, Deck
    db = load_card_db()
    main = [db[c] for c in REGISTRY.codes() if db[c].type is not CardType.SOUL for _ in range(4)]
    return G(Deck("toolbox", main, [db["SOUL-001"]] * 10))


def test_rulebot_crystal_breath_on_big_hit():
    from tests.test_cards_m2 import put
    g, _ = _box_game()
    g.agents[1] = RuleBot()
    att = put(g, 0, "BP01-026")  # Relaxaurus S3
    cb = put(g, 1, "TD01-022", Zone.HAND)
    g.perform(Attack(att.uid, None))
    assert cb.zone is Zone.GRAVEYARD and g.players[1].life == 10
    assert 0 in att.skip_stand  # doesn't stand in the attacker's (P1's) next stand phase


def test_rulebot_ignis_breath_finishes_blocked_attacker():
    from tests.test_cards_m2 import put
    g, _ = _box_game()
    g.agents[1] = RuleBot()
    att = put(g, 0, "BP01-025")  # Chillet 900
    put(g, 1, "TD01-016")        # Reindrix 600, will block
    ib = put(g, 1, "TD01-011", Zone.HAND)
    g.perform(Attack(att.uid, None))
    assert ib.zone is Zone.GRAVEYARD and att.zone is Zone.GRAVEYARD


def test_rulebot_top_prefers_dragon_with_chillet_in_hand():
    from tests.test_cards_m2 import put
    g, _ = _box_game()
    put(g, 0, "BP01-025", Zone.HAND)
    az = put(g, 0, "BP01-029", Zone.HAND)   # Azurobe: Dragon, lucky
    su = put(g, 0, "BP01-002", Zone.HAND)   # Suzaku: lucky, not a Dragon
    opts = [c.uid for c in g.players[0].hand]
    d = Decision("target", 0, "", opts, min=0, max=1, context={"intent": "top"})
    assert RuleBot().choose(g, d) == [az.uid]
    assert su.uid in opts
