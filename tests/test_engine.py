"""Rule tests for the engine, using the test-only cards in fixtures.py."""
import pytest

from bots import RandomBot
from cards.decklist import DecklistError, build_deck, parse_decklist
from engine import (Activate, RulesConfig, Attack, CardType, Deck, DeckError, Game, GameOver, PlayCard,
                    SoulDraw, UnimplementedCardError, UseInterrupt, Zone, validate_deck)
from tests.fixtures import CARDS, deck, legal_deck, make_game, make_registry, put, stack_top, staged


# ---------------------------------------------------------------- deck construction
def test_legal_deck_passes():
    validate_deck(legal_deck())


@pytest.mark.parametrize("mk, msg", [
    (lambda: Deck("x", [CARDS["T-100"]] * 49, [CARDS["T-SOUL"]] * 10), "exactly 50"),
    (lambda: deck(soul=9), "soul deck has 9"),
    (lambda: deck(extra=["T-LUCKY"] * 9), "lucky"),
])
def test_illegal_decks(mk, msg):
    with pytest.raises(DeckError, match=msg):
        validate_deck(mk())


def test_copy_limit_is_by_name():
    d = deck(fill="T-100")  # 50 copies of one name
    with pytest.raises(DeckError, match="copies"):
        validate_deck(d)


def test_three_colours_illegal_colorless_free():
    blue = CARDS["T-INT"]
    d = deck(extra=["T-GREEN", "T-INT"])  # red + green + blue
    assert blue.color.value == "blue"
    with pytest.raises(DeckError, match="colours"):
        validate_deck(d)


def test_unimplemented_card_fails_loudly():
    with pytest.raises(UnimplementedCardError, match="T-UNIMPL"):
        make_game(deck(extra=["T-UNIMPL"]))


def test_registry_lookup_unknown_raises():
    with pytest.raises(UnimplementedCardError):
        make_registry()("NOPE-001")


# ---------------------------------------------------------------- decklist parsing
def test_parse_decklist():
    text = "# main\n4 T-100 Pal\n46 T-200 Pal Two\n\n# soul\n10 T-SOUL Soul\n"
    entries = parse_decklist(text)
    d = build_deck(entries, CARDS, "x")
    assert len(d.main) == 50 and len(d.soul) == 10


def test_decklist_unknown_code():
    with pytest.raises(DecklistError, match="ZZZ"):
        build_deck(parse_decklist("# main\n1 ZZZ x\n"), CARDS, "x")


def test_decklist_needs_header():
    with pytest.raises(DecklistError, match="header"):
        parse_decklist("4 T-100 Pal\n")


# ---------------------------------------------------------------- setup & turn structure
def test_setup():
    g, _ = make_game()
    g.setup()
    second = 1 - g.first_player
    for ps in g.players:
        assert len(ps.hand) == 5 and len(ps.deck) == 45 and ps.life == 10
    assert g.players[second].souls == 1 and g.players[g.first_player].souls == 0


def test_redraw_once():
    g, bots = make_game()
    bots[0].redraw = True
    g.setup()
    assert g.players[0].redrew and len(g.players[0].hand) == 5
    assert len(g.players[0].deck) == 45


def test_first_player_skips_first_draw_and_souls():
    g, _ = make_game()
    g.setup()
    f, s = g.first_player, 1 - g.first_player
    g.take_turn()
    assert len(g.players[f].hand) == 5          # no draw on turn 1
    assert g.players[f].souls == 2
    g.take_turn()
    assert len(g.players[s].hand) == 6          # second player draws
    assert g.players[s].souls == 3              # 1 at setup + 2


def test_souls_cap_at_soul_deck():
    g, _ = make_game()
    g.setup()
    for _ in range(14):
        g.take_turn()
    assert all(ps.souls == 10 and ps.soul_deck == 0 for ps in g.players)


def test_souls_stand_each_turn():
    g, bots = staged()
    put(g, 0, "T-100", Zone.HAND)
    g.perform(PlayCard(g.players[0].hand[0].uid))
    assert g.players[0].souls_rested == 1
    g.active = 1
    g.take_turn()
    g.take_turn()  # player 0's turn: stand phase
    assert g.players[0].souls_rested == 0


# ---------------------------------------------------------------- damage check
def test_strike_damage_no_lucky():
    g, _ = staged()
    a = put(g, 0, "T-300")  # strike 2
    g.perform(Attack(a.uid, None))
    assert g.players[1].life == 8
    assert len(g.players[1].graveyard) == 2


def test_lucky_cancels_all_damage():
    g, _ = staged(d1=deck(extra=["T-LUCKY"]))
    stack_top(g, 1, ["T-LUCKY"])
    a = put(g, 0, "T-300")
    g.perform(Attack(a.uid, None))
    assert g.players[1].life == 10
    assert [c.code for c in g.players[1].graveyard] == ["T-LUCKY"]  # stopped after 1 flip


def test_lucky_on_second_flip_still_cancels():
    g, _ = staged(d1=deck(extra=["T-LUCKY"]))
    stack_top(g, 1, ["T-100", "T-LUCKY"])
    g.deal_player_damage(1, 2)
    assert g.players[1].life == 10 and len(g.players[1].graveyard) == 2


def test_damage_with_short_deck_still_hits():
    g, _ = staged()
    ps = g.players[1]
    for c in ps.deck[1:]:
        g.move(c, Zone.EXILE)
    g.deal_player_damage(1, 3)
    assert ps.life == 7 and not ps.deck
    with pytest.raises(GameOver):
        g.check_timing()
    assert g.winner == 0 and g.reason == "deckout"


def test_life_zero_loses():
    g, _ = staged()
    g.players[1].life = 1
    g.deal_player_damage(1, 1)
    with pytest.raises(GameOver):
        g.check_timing()
    assert g.winner == 0 and g.reason == "life"


# ---------------------------------------------------------------- battle
def test_cannot_attack_standing_pal():
    g, _ = staged()
    a = put(g, 0, "T-200")
    b = put(g, 1, "T-100")
    assert b.uid not in g.attack_targets(a)
    b.rested = True
    assert b.uid in g.attack_targets(a)


def test_new_pal_can_attack():
    g, _ = staged()
    put(g, 0, "T-100", Zone.HAND)
    c = g.players[0].hand[0]
    g.perform(PlayCard(c.uid))
    assert Attack(c.uid, None) in g.legal_actions(0)


def test_pal_battle_mutual_damage_and_rested_target_hits_back():
    g, _ = staged()
    a = put(g, 0, "T-300")
    b = put(g, 1, "T-200", rested=True)
    g.perform(Attack(a.uid, b.uid))
    assert b.zone is Zone.GRAVEYARD
    assert a.zone is Zone.BASE and a.damage == 200 and a.rested


def test_damage_accumulates_and_resets_at_end_of_turn():
    g, _ = staged()
    a1, a2 = put(g, 0, "T-100"), put(g, 0, "T-200")
    t = put(g, 1, "T-300", rested=True)
    g.perform(Attack(a1.uid, t.uid))
    assert t.damage == 100 and t.zone is Zone.BASE
    g.perform(Attack(a2.uid, t.uid))
    assert t.zone is Zone.GRAVEYARD  # 100 + 200 >= 300
    t2 = put(g, 1, "T-300", rested=True)
    t2.damage = 100
    g.take_turn()
    assert t2.damage == 0


def test_equal_power_trade():
    g, _ = staged()
    a, b = put(g, 0, "T-200"), put(g, 1, "T-STEALTH", rested=True)
    g.perform(Attack(a.uid, b.uid))
    assert a.zone is Zone.GRAVEYARD and b.zone is Zone.GRAVEYARD


def test_block_redirects_attack():
    g, bots = staged()
    a = put(g, 0, "T-100")
    blk = put(g, 1, "T-300")
    bots[1].answers.append([blk.uid])
    g.perform(Attack(a.uid, None))
    assert g.players[1].life == 10
    assert a.zone is Zone.GRAVEYARD and blk.rested and blk.damage == 100


def test_stealth_cannot_be_blocked():
    g, bots = staged()
    a = put(g, 0, "T-STEALTH")
    put(g, 1, "T-300")
    bots[1].answers.append(["should not be asked"])
    g.perform(Attack(a.uid, None))
    assert g.players[1].life == 9


def test_structure_attack_no_damage_back():
    g, _ = staged()
    a = put(g, 0, "T-300")
    w = put(g, 1, "T-WALL")
    assert w.uid in g.attack_targets(a)  # standing structure is a target (A2)
    g.perform(Attack(a.uid, w.uid))
    assert a.damage == 0 and w.damage == 300 and w.zone is Zone.BASE


def test_structures_rested_only_config():
    g, _ = staged(rules=RulesConfig(structures_attackable="rested_only"))
    a = put(g, 0, "T-300")
    w = put(g, 1, "T-WALL")
    assert w.uid not in g.attack_targets(a)
    w.rested = True
    assert w.uid in g.attack_targets(a)


def test_bad_rules_config():
    with pytest.raises(ValueError):
        RulesConfig(structures_attackable="sometimes")


def test_gear_deploys_to_own_base_and_is_untouchable():
    g, _ = staged()
    gear = put(g, 0, "T-GEAR", Zone.HAND)
    g.perform(PlayCard(gear.uid))
    assert gear in g.players[0].base and gear.zone is Zone.BASE
    a = put(g, 1, "T-300")
    gear.rested = True
    assert gear.uid not in g.attack_targets(a)
    g.deal_card_damage(gear, 500)
    g.check_timing()
    assert gear.damage == 0 and gear.zone is Zone.BASE
    assert len(g.players[0].pals) == 0  # gear doesn't count toward the Pal limit


def test_first_player_can_attack_turn_one():
    g, bots = make_game()
    g.setup()
    f = g.first_player
    pal = g.players[f].hand[0]  # default deck is all T-100
    bots[f].actions.extend([PlayCard(pal.uid), Attack(pal.uid, None)])
    g.take_turn()
    assert g.turn == 1 and g.stats[f].attacks == 1


def test_taunt_forces_target():
    g, _ = staged()
    a = put(g, 0, "T-ASSAULT")
    t = put(g, 1, "T-TAUNT")
    put(g, 1, "T-100", rested=True)
    assert g.attack_targets(a) == [t.uid]  # assault lets it hit the standing taunter


def test_taunt_standing_not_targetable_without_assault():
    g, _ = staged()
    a = put(g, 0, "T-100")
    put(g, 1, "T-TAUNT")
    assert g.attack_targets(a) == [None]


def test_interrupt_nullifies():
    g, bots = staged()
    a = put(g, 0, "T-300")
    i = put(g, 1, "T-INT", Zone.HAND)
    bots[1].actions.append(UseInterrupt(i.uid, None))
    g.perform(Attack(a.uid, None))
    assert g.players[1].life == 10 and i.zone is Zone.GRAVEYARD
    assert g.players[1].souls_rested == 1 and a.rested


def test_interrupt_discard_cost():
    g, bots = staged()
    a = put(g, 0, "T-300")
    i = put(g, 1, "T-INT", Zone.HAND)
    o = put(g, 1, "T-100", Zone.HAND)
    bots[1].actions.append(UseInterrupt(i.uid, o.uid))
    g.perform(Attack(a.uid, None))
    assert o.zone is Zone.GRAVEYARD and g.players[1].souls_rested == 0


def test_brave():
    g, _ = staged()
    a = put(g, 0, "T-BRAVE")  # 200 + Brave 200
    t = put(g, 1, "T-300", rested=True)
    g.perform(Attack(a.uid, t.uid))
    assert t.zone is Zone.GRAVEYARD and a.zone is Zone.BASE


def test_retaliate():
    g, _ = staged()
    a = put(g, 0, "T-300")
    r = put(g, 1, "T-RETAL", rested=True)
    g.perform(Attack(a.uid, r.uid))
    assert r.zone is Zone.GRAVEYARD and a.zone is Zone.GRAVEYARD


def test_breakthrough():
    g, _ = staged()
    a = put(g, 0, "T-BREAK")
    t = put(g, 1, "T-100", rested=True)
    g.perform(Attack(a.uid, t.uid))
    assert t.zone is Zone.GRAVEYARD and g.players[1].life == 9


def test_vigilance():
    g, _ = staged()
    v = put(g, 0, "T-VIG")
    g.perform(Attack(v.uid, None))
    assert v.rested
    g.take_turn()
    assert not v.rested


def test_pal_limit_overload():
    g, _ = staged()
    olds = [put(g, 0, c) for c in ("T-100", "T-100", "T-100", "T-VIG", "T-VIG")]
    new = put(g, 0, "T-200", Zone.HAND)
    g.perform(PlayCard(new.uid))
    assert new.zone is Zone.BASE and len(g.players[0].pals) == 5
    assert sum(c.zone is Zone.GRAVEYARD for c in olds) == 1


def test_soul_draw_once_per_turn():
    g, _ = staged()
    assert SoulDraw() in g.legal_actions(0)
    g.perform(SoulDraw())
    assert len(g.players[0].hand) == 1 and g.players[0].souls_rested == 3
    assert SoulDraw() not in g.legal_actions(0)


def test_event_resolves_to_graveyard():
    g, _ = staged(d0=deck(extra=["T-DRAW2"]))
    e = put(g, 0, "T-DRAW2", Zone.HAND)
    g.perform(PlayCard(e.uid))
    assert e.zone is Zone.GRAVEYARD and len(g.players[0].hand) == 2


def test_cannot_play_unaffordable():
    g, _ = staged()
    g.players[0].souls_rested = 8
    put(g, 0, "T-100", Zone.HAND)
    assert not any(isinstance(a, PlayCard) for a in g.legal_actions(0))


def test_left_base_becomes_new_card():
    g, _ = staged()
    c = put(g, 0, "T-200")
    g.add_mod(c, "power", 500, None)
    g.return_to_hand(c)
    g.deploy(c)
    assert g.power(c) == 200 and c.incarnation == 1


# ---------------------------------------------------------------- whole games
def _random_game(seed, log=False):
    decks = [deck("A", extra=["T-300"] * 4 + ["T-LUCKY"] * 4 + ["T-STEALTH"] * 4
                  + ["T-INT"] * 4 + ["T-WALL"] * 2 + ["T-DRAW2"] * 4 + ["T-BRAVE"] * 4),
             deck("B", extra=["T-TAUNT"] * 4 + ["T-RETAL"] * 4 + ["T-BREAK"] * 4
                  + ["T-LUCKY"] * 8 + ["T-VIG"] * 4 + ["T-ASSAULT"] * 4)]
    g = Game(decks, make_registry(), [RandomBot(seed * 2), RandomBot(seed * 2 + 1)],
             seed=seed, log=log)
    return g, g.play()


@pytest.mark.parametrize("seed", range(40))
def test_random_games_terminate(seed):
    _, r = _random_game(seed)
    assert r.reason in ("life", "deckout", "draw", "turn_cap")
    assert r.turns >= 1


def test_deterministic_replay():
    g1, r1 = _random_game(7, log=True)
    g2, r2 = _random_game(7, log=True)
    assert g1.lines == g2.lines and r1.winner == r2.winner and r1.turns == r2.turns
    g3, _ = _random_game(8, log=True)
    assert g3.lines != g1.lines


def test_clone_is_independent():
    g, bots = staged()
    a = put(g, 0, "T-300")
    c = g.clone([RandomBot(1), RandomBot(2)])
    c.perform(Attack(a.uid, None))
    assert g.players[1].life == 10 and c.players[1].life == 8
    assert c.card(a.uid) is not a


def test_first_player_split_roughly_even():
    firsts = [_random_game(s)[1].first_player for s in range(200)]
    assert 70 < sum(firsts) < 130


def test_activate_assign_cost():
    from engine import ActAbility, CardImpl
    reg = make_registry()

    @reg.register
    class Mill(CardImpl):
        code = "T-MILL"
        text = "[ACT] [Assign] Draw 1 card."
        acts = [ActAbility("draw", lambda g, c, ctx: g.draw(c.owner), assign=True)]

    from engine import CardDef, Color
    mill = CardDef("T-MILL", "Mill", CardType.STRUCTURE, Color.RED, 1, 300)
    d = deck()
    d.main[0] = mill
    from tests.fixtures import ScriptedBot
    g2 = Game([d, deck()], reg, [ScriptedBot(), ScriptedBot()], seed=1)
    g2.setup()
    for c in list(g2.players[0].hand):
        g2.move(c, Zone.DECK)
    g2.active, g2.turn = 0, 3
    g2.players[0].souls = 5
    s = put(g2, 0, "T-MILL")
    p = put(g2, 0, "T-100")
    act = Activate(s.uid, 0, p.uid)
    assert act in g2.legal_actions(0)
    g2.perform(act)
    assert p.rested and len(g2.players[0].hand) == 1
    assert not any(isinstance(a, Activate) for a in g2.legal_actions(0))
