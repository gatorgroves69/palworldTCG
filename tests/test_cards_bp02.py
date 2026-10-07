"""BP02 Legends Awaken preview cards (unreleased; texts may change)."""
from engine import Attack, PlayCard, Zone
from tests.test_cards_m2 import G, act, box, play, put  # noqa: F401


def test_orserk_three_modes_each_once(box):
    g, bots = G(box)
    o = put(g, 0, "BP02-001")
    g.players[0].resources["material"] = 6
    mine = put(g, 0, "TD01-023")           # Lamball 200/S1, cost 2
    theirs = put(g, 1, "BP01-028")         # Pengullet 600
    act(g, bots, o, 0, answers=[[mine.uid]])
    assert g.power(mine) == 700 and g.strike(mine) == 2
    act(g, bots, o, 1, answers=[[theirs.uid]])
    assert theirs.zone is Zone.GRAVEYARD
    mine.rested = True
    act(g, bots, o, 2, answers=[[mine.uid]])
    assert not mine.rested and g.players[0].resources["material"] == 0
    from engine import Activate
    assert Activate(o.uid, 0, None, None) not in g.legal_actions(0)  # used this turn / no Material


def test_chillet_ignis_discards_dragon_for_700(box):
    g, bots = G(box)
    tgt = put(g, 1, "BP01-028")  # Pengullet 600
    dragon = put(g, 0, "BP01-025", Zone.HAND)
    play(g, bots, 0, "BP02-004", answers=[[dragon.uid], [tgt.uid]])
    assert dragon.zone is Zone.GRAVEYARD and tgt.zone is Zone.GRAVEYARD


def test_chillet_ignis_may_decline(box):
    g, bots = G(box)
    tgt = put(g, 1, "BP01-028")
    put(g, 0, "BP01-025", Zone.HAND)
    play(g, bots, 0, "BP02-004", answers=[[]])
    assert tgt.damage == 0


def test_relaxaurus_lux_assault_and_restand(box):
    g, bots = G(box)
    lux = put(g, 0, "BP02-010")             # 1100, Assault
    v = put(g, 1, "BP01-028")               # standing Pengullet 600
    assert v.uid in g.attack_targets(lux)
    g.perform(Attack(lux.uid, v.uid))
    assert v.zone is Zone.GRAVEYARD and not lux.rested


def test_frostallion_discount_and_draw_to_4(box):
    g, bots = G(box)
    f = put(g, 0, "BP02-025")
    c = put(g, 0, "BP01-032", Zone.HAND)    # Fuack ◇2 -> stays ◇1 (not 0)
    k = put(g, 0, "BP01-007", Zone.HAND)    # Kitsun ◇5 -> ◇3
    assert g.cost(c) == 1 and g.cost(k) == 3
    g.end_phase()
    assert len(g.players[0].hand) == 4
    # Legendary: a second copy can't be played while one is in the base
    f2 = put(g, 0, "BP02-025", Zone.HAND)
    assert PlayCard(f2.uid) not in g.legal_actions(0)
    assert f.zone is Zone.BASE


def test_foxcicle_discounts_legendary_only(box):
    g, bots = G(box)
    put(g, 0, "BP02-026")
    leg = put(g, 0, "BP02-097", Zone.HAND)
    pal = put(g, 0, "BP01-007", Zone.HAND)
    assert g.cost(leg) == 7 and g.cost(pal) == 5


def test_jolthog_rests_without_legendary(box):
    g, bots = G(box)
    j = play(g, bots, 0, "BP02-029")
    assert j.rested
    put(g, 0, "BP02-097", Zone.HAND)
    j2 = play(g, bots, 0, "BP02-029")
    assert not j2.rested


def test_overloaded_with_love(box):
    g, bots = G(box)
    deck = g.players[0].deck
    top = deck[:3]
    pal = next((c for c in top if c.is_pal), None)
    n = len(g.players[0].hand)
    answers = [[pal.uid]] if pal else [[]]
    answers.append([])
    play(g, bots, 0, "BP02-047", answers=answers)
    assert len(g.players[0].hand) == n + (1 if pal else 0)
    for c in top:
        assert c.zone is Zone.HAND or c is deck[-1] or c is deck[-2] or c is deck[-3]


def test_jetragon_exiles_and_gains_vigilance(box):
    g, bots = G(box)
    j = put(g, 0, "BP02-097")
    a, b = put(g, 0, "BP01-002", Zone.GRAVEYARD), put(g, 0, "BP01-020", Zone.GRAVEYARD)
    big = put(g, 0, "BP01-027", Zone.GRAVEYARD)  # Jormuntide ◇8
    act(g, bots, j, 0, answers=[[a.uid, big.uid]])
    assert a.zone is Zone.EXILE and big.zone is Zone.EXILE and b.zone is Zone.GRAVEYARD
    assert g.has_kw(j, "vigilance")


def test_faleris_power_per_gear_and_flambelle_material(box):
    g, bots = G(box)
    f = put(g, 0, "BP02-003")
    assert g.power(f) == 1100
    put(g, 0, "BP01-020"); put(g, 0, "BP01-044")
    assert g.power(f) == 1500
    fl = put(g, 0, "BP02-007")
    act(g, bots, fl, 0)
    assert g.players[0].resources["material"] == 2 and fl.rested
