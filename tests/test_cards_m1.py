"""One or more tests per M1 card, using the real decklists and cards.json.

P1 (index 0) = Cattiva·Azurobe BR, P2 (index 1) = Chillet·Relaxaurus BP.
"""
import pytest

from bots import RandomBot
from cards import REGISTRY
from cards.db import DEFAULT_PATH, load_card_db
from cards.decklist import load_deck
from engine import Activate, Attack, Game, PlayCard, UseInterrupt, Zone
from tests.fixtures import ScriptedBot, stack_top

DECKS = ["data/decks/cattiva-azurobe-br.txt", "data/decks/chillet-relaxaurus-bp.txt"]
pytestmark = pytest.mark.skipif(not DEFAULT_PATH.exists(), reason="data/cards.json missing")


@pytest.fixture(scope="module")
def decks():
    db = load_card_db()
    return [load_deck(p, db) for p in DECKS]


def real_game(decks, seed=1):
    bots = [ScriptedBot(), ScriptedBot()]
    g = Game(decks, REGISTRY, bots, seed=seed, log=True)
    g.setup()
    for ps in g.players:
        for c in list(ps.hand):
            g.move(c, Zone.DECK)
        ps.deck.sort(key=lambda c: c.defn.lucky)  # lucky to the bottom: predictable checks
        ps.souls, ps.soul_deck, ps.souls_rested = 10, 0, 0
    g.active, g.turn, g.phase = 0, 3, "main"
    return g, bots


def put(g, p, code, zone=Zone.BASE, rested=False):
    c = next(c for c in g.players[p].deck if c.code == code)
    if zone is Zone.BASE:
        g.deploy(c)
        g.pending.clear()  # arranging the board: don't fire OnDeploy
        c.rested = rested
    else:
        g.move(c, zone)
    return c


def play(g, bots, p, code, answers=(), mode=None):
    """Play a card from p's hand (fetched from deck), answering its choices in order."""
    c = put(g, p, code, Zone.HAND)
    bots[p].answers.extend(answers)
    g.perform(PlayCard(c.uid, mode))
    return c


# ---------------------------------------------------------------- registry
def test_every_decklist_card_is_implemented(decks):
    for d in decks:
        assert REGISTRY.missing(c.code for c in d.main + d.soul) == []


def test_impl_text_matches_cards_json():
    db = load_card_db()
    for code in REGISTRY.codes():
        assert REGISTRY(code).text == db[code].text, code


# ---------------------------------------------------------------- BP01-002 Suzaku
def test_suzaku_on_deploy_700_plus_own_200(decks):
    g, bots = real_game(decks)
    t = put(g, 1, "BP01-025")  # Chillet 900
    play(g, bots, 0, "BP01-002", [[t.uid]])
    assert t.zone is Zone.GRAVEYARD  # 700 + 200 (strengthens its own ability) = 900


def test_suzaku_boosts_other_red_effect_damage_and_stacks(decks):
    g, bots = real_game(decks)
    put(g, 0, "BP01-002")
    put(g, 0, "BP01-002")
    t = put(g, 1, "BP01-026")  # Relaxaurus 1200
    play(g, bots, 0, "BP01-008", [[t.uid]])  # Sparkit 500 +200 +200
    assert t.damage == 900


def test_suzaku_ignores_battle_and_nonred_damage(decks):
    g, bots = real_game(decks)
    put(g, 0, "BP01-002")
    blue = put(g, 0, "BP01-028")  # Pengullet (blue)
    t = put(g, 1, "BP01-026", rested=True)
    g.deal_card_damage(t, 300, blue)
    assert t.damage == 300
    k = put(g, 0, "BP01-007")  # Kitsun 400, red
    g.perform(Attack(k.uid, t.uid))
    assert t.damage == 700  # 300 + battle 400, no bonus


# ---------------------------------------------------------------- BP01-007 Kitsun
def test_kitsun_only_targets_cost_7_plus(decks):
    g, bots = real_game(decks)
    big = put(g, 1, "BP01-026")  # Relaxaurus ◇7
    small = put(g, 1, "BP01-028")  # Pengullet ◇4
    seen = []
    bots[0].choose = lambda game, d: seen.append(d.options) or [big.uid]
    play(g, bots, 0, "BP01-007")
    assert seen[0] == [big.uid] and small.uid not in seen[0]
    assert big.zone is Zone.GRAVEYARD


# ---------------------------------------------------------------- BP01-008 Sparkit
def test_sparkit_only_standing_pals(decks):
    g, bots = real_game(decks)
    up = put(g, 1, "BP01-028")
    down = put(g, 1, "BP01-038", rested=True)
    seen = []
    bots[0].choose = lambda game, d: seen.append(d.options) or [up.uid]
    play(g, bots, 0, "BP01-008")
    assert down.uid not in seen[0] and up.damage == 500


# ---------------------------------------------------------------- BP01-020 Pump-Action Shotgun
def test_shotgun_hits_all_opposing_pals(decks):
    g, bots = real_game(decks)
    a, b = put(g, 1, "BP01-025"), put(g, 1, "BP01-026")  # 900, 1200
    mine = put(g, 0, "BP01-032")
    gun = play(g, bots, 0, "BP01-020")
    assert gun.zone is Zone.BASE and not gun.is_pal
    assert a.zone is Zone.GRAVEYARD and b.zone is Zone.GRAVEYARD and mine.damage == 0


def test_shotgun_act_rests_itself(decks):
    g, bots = real_game(decks)
    gun = put(g, 0, "BP01-020")
    f = put(g, 0, "BP01-032")
    bots[0].answers.append([f.uid])
    g.perform(Activate(gun.uid, 0))
    assert gun.rested and g.power(f) == 400
    assert Activate(gun.uid, 0) not in g.legal_actions(0)


# ---------------------------------------------------------------- BP01-028 Pengullet
def test_pengullet_draws_when_defeated_not_when_discarded(decks):
    g, bots = real_game(decks)
    p = put(g, 1, "BP01-028")
    g.send_to_graveyard(p)
    g.check_timing()
    assert len(g.players[1].hand) == 1
    h = put(g, 1, "BP01-028", Zone.HAND)
    g.discard(h)
    g.check_timing()
    assert len(g.players[1].hand) == 1


# ---------------------------------------------------------------- BP01-029 Azurobe
def test_azurobe_draws_and_rests(decks):
    g, bots = real_game(decks)
    t = put(g, 1, "BP01-026")
    play(g, bots, 0, "BP01-029", [[t.uid]])
    assert t.rested and len(g.players[0].hand) == 1


# ---------------------------------------------------------------- BP01-032 Fuack
def test_fuack_gets_300_when_attacked(decks):
    g, bots = real_game(decks)
    f = put(g, 0, "BP01-032", rested=True)
    g.add_mod(f, "power", 200, "turn")  # 400: dies to a 600 attacker unless boosted
    a = put(g, 1, "BP01-028")  # Pengullet 600
    g.active = 1
    g.perform(Attack(a.uid, f.uid))
    assert f.zone is Zone.BASE and f.damage == 600 and g.power(f) == 700
    assert a.zone is Zone.GRAVEYARD  # took 700 >= its 600


def test_fuack_blocking_is_not_being_attacked(decks):
    g, bots = real_game(decks)
    f = put(g, 0, "BP01-032")
    a = put(g, 1, "BP01-028")  # Pengullet 600
    g.active = 1
    bots[0].answers.append([f.uid])  # block
    g.perform(Attack(a.uid, None))
    assert f.zone is Zone.GRAVEYARD and a.damage == 200


# ---------------------------------------------------------------- BP01-038 / TD01-004 / TD01-016 /
# BP01-077 / TD02-017 interrupts
@pytest.mark.parametrize("p, code", [(1, "BP01-038"), (0, "TD01-004"), (0, "TD01-016"),
                                     (1, "BP01-077"), (1, "TD02-017")])
def test_interrupt_cards(decks, p, code):
    g, bots = real_game(decks)
    g.active = 1 - p
    att_code = "BP01-028"
    att = put(g, 1 - p, att_code)
    i = put(g, p, code, Zone.HAND)
    bots[p].actions.append(UseInterrupt(i.uid, None))
    g.perform(Attack(att.uid, None))
    assert g.players[p].life == 10 and i.zone is Zone.GRAVEYARD


# ---------------------------------------------------------------- BP01-044 Rocket Launcher
def test_launcher_plus_200_on_non_pengullet(decks):
    g, bots = real_game(decks)
    g.active = 1
    rl = put(g, 1, "BP01-044")
    c = put(g, 1, "BP01-025")
    bots[1].answers.append([c.uid])
    g.perform(Activate(rl.uid, 0))
    assert g.power(c) == 1100 and rl.rested and not c.granted


def test_launcher_pengullet_barrage(decks):
    g, bots = real_game(decks)
    g.active = 1
    rl = put(g, 1, "BP01-044")
    pen = put(g, 1, "BP01-028")
    victims = [put(g, 0, "BP01-029"), put(g, 0, "BP01-032")]  # 1200, 200
    bots[1].answers.append([pen.uid])
    g.perform(Activate(rl.uid, 0))
    assert g.power(pen) == 1100
    barrage = Activate(pen.uid, 0)  # granted ability is the Pengullet's first ACT
    assert barrage in g.legal_actions(1)
    g.perform(barrage)
    assert victims[1].zone is Zone.GRAVEYARD and victims[0].damage == 1100
    assert pen.zone is Zone.GRAVEYARD and len(g.players[1].hand) == 1  # Pengullet draw


def test_launcher_grant_expires(decks):
    g, bots = real_game(decks)
    g.active = 1
    rl, pen = put(g, 1, "BP01-044"), put(g, 1, "BP01-028")
    bots[1].answers.append([pen.uid])
    g.perform(Activate(rl.uid, 0))
    g.take_turn()  # finishes player 1's turn (turn counter moves on)
    assert pen.granted == []


# ---------------------------------------------------------------- BP01-047 Pal Sphere
def test_pal_sphere_draws_3(decks):
    g, bots = real_game(decks)
    play(g, bots, 0, "BP01-047")
    assert len(g.players[0].hand) == 3


# ---------------------------------------------------------------- BP01-048 Aurora Guide
def test_aurora_guide_quick_and_top_of_deck(decks):
    g, bots = real_game(decks)
    ag = put(g, 1, "BP01-048", Zone.HAND)
    lucky = put(g, 1, "BP01-027", Zone.HAND)  # Jormuntide, lucky
    att = put(g, 0, "BP01-029")  # Azurobe S2
    bots[1].actions.append(PlayCard(ag.uid))
    bots[1].answers.append([lucky.uid])
    g.perform(Attack(att.uid, None))
    assert g.players[1].life == 10  # lucky put on top cancels the damage check
    assert lucky.zone is Zone.GRAVEYARD


# ---------------------------------------------------------------- BP01-077 Pyrin Noct
def test_pyrin_noct_nocturnal(decks):
    g, bots = real_game(decks)
    p = put(g, 1, "BP01-077")
    assert g.power(p) == 1100
    g.night = True
    assert g.power(p) == 1400


# ---------------------------------------------------------------- BP01-095 Zoe's Strategy
def test_zoe_offers_three_modes(decks):
    g, bots = real_game(decks)
    g.active = 1
    z = put(g, 1, "BP01-095", Zone.HAND)
    plays = [a for a in g.legal_actions(1) if isinstance(a, PlayCard) and a.uid == z.uid]
    assert [a.mode for a in plays] == [0, 1, 2]


def test_zoe_mode_resources(decks):
    g, bots = real_game(decks)
    g.active = 1
    g.players[0].resources.update(material=4, ingredient=3)
    play(g, bots, 1, "BP01-095", mode=0)
    assert g.players[0].resources == {"material": 0, "ingredient": 2}


def test_zoe_mode_return_and_discard(decks):
    g, bots = real_game(decks)
    g.active = 1
    dead = put(g, 1, "BP01-026", Zone.GRAVEYARD)
    victim = put(g, 0, "BP01-047", Zone.HAND)
    bots[0].answers.append([victim.uid])  # the opponent picks their own discard
    play(g, bots, 1, "BP01-095", [[dead.uid]], mode=1)
    assert dead.zone is Zone.HAND and victim.zone is Zone.GRAVEYARD


def test_zoe_mode_butcher_and_destroy(decks):
    g, bots = real_game(decks)
    g.active = 1
    mine = put(g, 1, "BP01-028")
    theirs = put(g, 0, "BP01-029")
    play(g, bots, 1, "BP01-095", [[mine.uid], [theirs.uid]], mode=2)
    assert mine.zone is Zone.GRAVEYARD and theirs.zone is Zone.GRAVEYARD
    assert len(g.players[1].hand) == 1  # butchered Pengullet still draws


def test_zoe_butcher_needs_a_pal(decks):
    g, bots = real_game(decks)
    g.active = 1
    theirs = put(g, 0, "BP01-029")
    play(g, bots, 1, "BP01-095", mode=2)
    assert theirs.zone is Zone.BASE


# ---------------------------------------------------------------- BP01-098 Elphidran
def test_elphidran_reveals_dragon(decks):
    g, bots = real_game(decks)
    g.active = 1
    e = put(g, 1, "BP01-098")
    d = put(g, 1, "BP01-026", Zone.HAND)
    bots[1].answers.append([d.uid])
    g.perform(Attack(e.uid, None))
    assert g.power(e) == 1100 and d.zone is Zone.HAND


def test_elphidran_no_dragon_no_boost(decks):
    g, bots = real_game(decks)
    g.active = 1
    e = put(g, 1, "BP01-098")
    put(g, 1, "BP01-047", Zone.HAND)
    g.perform(Attack(e.uid, None))
    assert g.power(e) == 600


# ---------------------------------------------------------------- BP01-025 Chillet
def test_chillet_deploys_dragon(decks):
    g, bots = real_game(decks)
    g.active = 1
    stack_top(g, 1, ["BP01-026"])
    relax = g.players[1].deck[0]
    play(g, bots, 1, "BP01-025", [[True], []])  # deploy; Relaxaurus targets nothing
    assert relax.zone is Zone.BASE


def test_chillet_non_dragon_to_hand(decks):
    g, bots = real_game(decks)
    g.active = 1
    stack_top(g, 1, ["BP01-047"])
    top = g.players[1].deck[0]
    play(g, bots, 1, "BP01-025")
    assert top.zone is Zone.HAND


def test_chillet_may_decline(decks):
    g, bots = real_game(decks)
    g.active = 1
    stack_top(g, 1, ["BP01-098"])
    top = g.players[1].deck[0]
    play(g, bots, 1, "BP01-025", [[False]])
    assert top.zone is Zone.HAND


# ---------------------------------------------------------------- BP01-026 Relaxaurus
def test_relaxaurus_lock_while_on_base(decks):
    g, bots = real_game(decks)
    g.active = 1
    t = put(g, 0, "BP01-029")  # ◇6
    r = play(g, bots, 1, "BP01-026", [[t.uid]])
    assert t.rested
    g.take_turn()  # rest of P2's turn
    g.take_turn()  # P1's turn: Azurobe stays rested
    assert t.rested
    g.send_to_graveyard(r)
    g.take_turn()
    g.take_turn()
    assert not t.rested


def test_relaxaurus_cost_limit(decks):
    g, bots = real_game(decks)
    g.active = 1
    big = put(g, 0, "BP01-002")  # ◇7
    ok = put(g, 0, "BP01-029")  # ◇6
    seen = []
    bots[1].choose = lambda game, d: seen.append(d.options) or []
    play(g, bots, 1, "BP01-026")
    assert ok.uid in seen[0] and big.uid not in seen[0]


# ---------------------------------------------------------------- BP01-027 Jormuntide
def test_jormuntide_skips_one_stand(decks):
    g, bots = real_game(decks)
    g.active = 1
    t = put(g, 0, "BP01-002")  # ◇7
    play(g, bots, 1, "BP01-027", [[t.uid]])
    assert t.rested and len(g.players[1].hand) == 1
    g.take_turn()
    g.take_turn()  # P1's stand phase: skipped
    assert t.rested
    g.take_turn()
    g.take_turn()  # next one: stands
    assert not t.rested


# ---------------------------------------------------------------- TD01-012 Elphidran Aqua
def test_elphidran_aqua_draw2_top1(decks):
    g, bots = real_game(decks)
    g.active = 1
    aqua = put(g, 1, "TD01-012", Zone.HAND)
    first_two = g.players[1].deck[:2]
    top_before = g.players[1].deck[2]
    bots[1].answers.append([first_two[0].uid])
    g.perform(PlayCard(aqua.uid))
    assert len(g.players[1].hand) == 1 and g.players[1].deck[0] is first_two[0]
    assert g.players[1].deck[1] is top_before


# ---------------------------------------------------------------- TD01-015 Hangyu Cryst
def test_hangyu_only_cost_3_or_less(decks):
    g, bots = real_game(decks)
    cheap = put(g, 1, "BP01-098")  # ◇4: not allowed
    seen = []
    bots[0].choose = lambda game, d: seen.append(d.options) or []
    play(g, bots, 0, "TD01-015")
    assert seen == []  # no legal targets at all -> no question asked
    lam = put(g, 0, "TD01-023")  # own Lamball ◇2 is a legal (if silly) target
    play(g, bots, 0, "TD01-015")
    assert seen and seen[-1] == [lam.uid] and cheap.uid not in seen[-1]


# ---------------------------------------------------------------- TD01-023 Lamball / TD02-023 Cattiva
def test_lamball_immune_to_cost_4_plus(decks):
    g, bots = real_game(decks)
    g.active = 1
    lam = put(g, 0, "TD01-023", rested=True)
    big = put(g, 1, "BP01-028")  # ◇4
    assert lam.uid not in g.attack_targets(big)


def test_cattiva_immune_to_cost_3_or_less(decks):
    g, bots = real_game(decks)
    cat = put(g, 0, "TD02-023", rested=True)
    small = put(g, 0, "BP01-032")  # a ◇2 Pal (no ◇3- Pals in the Chillet deck)
    elph = put(g, 1, "BP01-098")  # ◇4
    g.active = 1
    assert cat.uid in g.attack_targets(elph)
    assert not cat.impl.can_be_attacked_by(g, cat, small)


def test_lamball_can_attack_normally(decks):
    g, bots = real_game(decks)
    lam = put(g, 0, "TD01-023")
    t = put(g, 1, "BP01-028", rested=True)
    assert t.uid in g.attack_targets(lam)


# ---------------------------------------------------------------- TD02-012 Astegon
def test_astegon_minus_1000_not_lethal(decks):
    g, bots = real_game(decks)
    g.active = 1
    t = put(g, 0, "BP01-029")  # 1200
    play(g, bots, 1, "TD02-012", [[t.uid]])
    assert g.power(t) == 200 and t.zone is Zone.BASE


def test_astegon_on_attack_wipes_small_pals_both_sides(decks):
    g, bots = real_game(decks)
    g.active = 1
    a = put(g, 1, "TD02-012")
    mine_small = put(g, 1, "BP01-098")  # 600: survives
    their_small = put(g, 0, "BP01-032")  # Fuack 200
    lam = put(g, 0, "TD01-023")  # 200
    big = put(g, 0, "BP01-029")  # 1200
    g.perform(Attack(a.uid, None))
    assert their_small.zone is Zone.GRAVEYARD and lam.zone is Zone.GRAVEYARD
    assert big.zone is Zone.BASE and mine_small.zone is Zone.BASE


# ---------------------------------------------------------------- TD02-021 Strike from the Darkness
def test_strike_from_the_darkness(decks):
    g, bots = real_game(decks)
    g.active = 1
    t = put(g, 0, "BP01-002")
    play(g, bots, 1, "TD02-021", [[t.uid]])
    assert t.zone is Zone.GRAVEYARD


# ---------------------------------------------------------------- whole games
@pytest.mark.parametrize("seed", range(30))
def test_random_bot_games_with_real_decks(decks, seed):
    g = Game(decks, REGISTRY, [RandomBot(2 * seed), RandomBot(2 * seed + 1)], seed=seed)
    r = g.play()
    assert r.reason in ("life", "deckout", "draw", "turn_cap")
