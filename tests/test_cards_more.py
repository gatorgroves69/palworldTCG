"""Tests for the remaining BP01/TD01/TD02/PR red, blue and colorless cards."""
from dataclasses import replace

import pytest

from cards import REGISTRY
from engine import Activate, Attack, EndMain, PlayCard, UseInterrupt, Zone
from tests.test_cards_m2 import G, act, box, end_turn, play, put  # noqa: F401


@pytest.mark.parametrize("code", ["BP01-013", "BP01-037", "BP01-099", "TD01-002", "TD01-003",
                                  "TD01-013", "TD01-014"])
def test_vanilla_cards_registered(code):
    assert code in REGISTRY and REGISTRY(code).text == ""


# ---------------------------------------------------------------- red
def test_gobfin_ignis_other_red_pals(box):
    g, _ = G(box)
    gob = put(g, 0, "BP01-003")
    red, blue = put(g, 0, "BP01-008"), put(g, 0, "BP01-028")
    assert g.power(red) == 700 and g.power(blue) == 600 and g.power(gob) == 400


def test_bushi_returns_after_attacking(box):
    g, bots = G(box)
    b = put(g, 0, "BP01-004")
    bots[0].answers.append([True])
    g.perform(Attack(b.uid, None))
    assert b.zone is Zone.HAND


def test_bushi_is_an_interrupt(box):
    g, bots = G(box)
    att = put(g, 0, "BP01-028")
    b = put(g, 1, "BP01-004", Zone.HAND)
    bots[1].actions.append(UseInterrupt(b.uid, None))
    g.perform(Attack(att.uid, None))
    assert g.players[1].life == 10


def test_univolt_and_rooby_keywords(box):
    g, bots = G(box)
    u = put(g, 0, "BP01-009")
    g.perform(Attack(u.uid, None))
    assert g.power(u) == 900
    pit, rooby, other = put(g, 0, "TD01-008"), put(g, 0, "BP01-011"), put(g, 0, "BP01-028")
    act(g, bots, pit, 0, [[other.uid]], assign=rooby)
    assert g.power(other) == 1000


def test_ragnahawk_pumps_red_pals(box):
    g, _ = G(box)
    r, red, blue = put(g, 0, "BP01-010"), put(g, 0, "BP01-008"), put(g, 0, "BP01-028")
    g.perform(Attack(r.uid, None))
    assert g.power(red) == 900 and g.strike(red) == 2 and g.power(blue) == 600


def test_flame_cauldron(box):
    g, bots = G(box)
    put(g, 0, "BP01-017")
    red = play(g, bots, 0, "BP01-008")
    assert g.power(red) == 600 and g.players[0].resources["material"] == 1
    play(g, bots, 0, "BP01-028")  # blue: no Material
    assert g.players[0].resources["material"] == 1


def test_alarm_bell_stands_assigned_and_forces_attacks(box):
    g, bots = G(box)
    pit, bell = put(g, 0, "TD01-008"), put(g, 0, "BP01-018")
    a, b = put(g, 0, "BP01-028"), put(g, 0, "BP01-032")
    act(g, bots, pit, 0, assign=a)
    assert a.rested
    act(g, bots, bell, 0, assign=b)
    assert not a.rested and not b.rested
    acts = g.legal_actions(0)
    assert not any(isinstance(x, EndMain) for x in acts)  # must attack while able
    assert not any(isinstance(x, Activate) and x.assign_uid is not None for x in acts)
    g.perform(Attack(a.uid, None))
    g.perform(Attack(b.uid, None))
    assert any(isinstance(x, EndMain) for x in g.legal_actions(0))


def test_makeshift_handgun_and_stone_pickaxe(box):
    g, bots = G(box)
    t = put(g, 1, "BP01-032")
    play(g, bots, 0, "BP01-021", [[t.uid]])
    assert t.zone is Zone.GRAVEYARD
    pick, p = put(g, 0, "BP01-022"), put(g, 0, "BP01-028")
    act(g, bots, pick, 0, [[p.uid]])
    assert g.power(p) == 800 and g.players[0].resources["material"] == 1


def test_treasure_chest(box):
    g, bots = G(box)
    gear = put(g, 0, "BP01-020", Zone.DECK)
    play(g, bots, 0, "BP01-024", [[gear.uid]])
    assert gear.zone is Zone.HAND and g.players[0].resources["material"] == 0
    play(g, bots, 0, "BP01-024", [[]])
    assert g.players[0].resources["material"] == 3


# ---------------------------------------------------------------- blue
def test_reptyro_cryst(box):
    g, bots = G(box)
    rc = play(g, bots, 0, "BP01-030")
    assert len(g.players[0].hand) == 1
    s1, s2 = put(g, 0, "TD01-008", Zone.DECK), put(g, 0, "BP01-016", Zone.DECK)
    act(g, bots, rc, 0, [[g.players[0].hand[0].uid], [s1.uid, s2.uid]])
    assert s1.zone is Zone.BASE and s2.zone is Zone.BASE


def test_penking_pumps_pengullets(box):
    g, _ = G(box)
    put(g, 0, "BP01-031")
    p1, p2 = put(g, 0, "BP01-028"), put(g, 0, "TD01-014")
    assert g.power(p1) == 1300 and g.power(p2) == 1200


def test_wumpo_strike_aura(box):
    g, _ = G(box)
    w = put(g, 0, "BP01-033")
    t = put(g, 1, "BP01-028")
    assert g.strike(t) == 2
    w.rested = True
    assert g.strike(t) == 1


def test_mau_cryst_draws_on_farming_structure(box):
    g, bots = G(box)
    pit, mau = put(g, 0, "TD01-008"), put(g, 0, "BP01-035")
    act(g, bots, pit, 0, assign=mau)
    assert len(g.players[0].hand) == 1  # Stone Pit's own draw only (Collecting)
    pit2, mau2 = put(g, 0, "TD01-008"), put(g, 0, "BP01-035")
    pit2.defn = replace(pit2.defn, work=("farming",))
    act(g, bots, pit2, 0, assign=mau2)
    assert len(g.players[0].hand) == 3


def test_celaray_loots_on_attack(box):
    g, bots = G(box)
    c = put(g, 0, "BP01-036")
    keep = put(g, 0, "BP01-002", Zone.HAND)
    bots[0].answers.append([keep.uid])
    g.perform(Attack(c.uid, None))
    assert keep.zone is Zone.GRAVEYARD and len(g.players[0].hand) == 1


def test_antique_curtain_counts_antique_names(box):
    g, bots = G(box)
    put(g, 0, "BP01-042")
    put(g, 0, "BP01-042")  # same name twice counts once
    a, b, c = put(g, 1, "BP01-028"), put(g, 1, "BP01-032"), put(g, 1, "BP01-025")
    seen = []
    bots[0].choose = lambda game, d: seen.append(d.max) or [a.uid, b.uid]
    play(g, bots, 0, "BP01-039")
    assert seen == [2] and a.zone is Zone.HAND and b.zone is Zone.HAND and c.zone is Zone.BASE


def test_antique_dresser_declare_and_pump(box):
    g, bots = G(box)
    d, pen = put(g, 0, "BP01-040"), put(g, 0, "BP01-032")
    put(g, 0, "BP01-031")  # Penking
    for code in ("BP01-047", "BP01-048", "BP01-002"):
        put(g, 0, code, Zone.HAND)
    hand = g.players[0].hand
    act(g, bots, d, 0, [[hand[0].uid], ["Pengullet – Yearning for the Sky"]])
    assert "Pengullet" in g.main_names(pen) and g.power(pen) == 900  # Fuack 200 + Penking 700
    act(g, bots, d, 1, [[g.players[0].hand[0].uid], [pen.uid]], x=1)
    assert g.power(pen) == 1900 and g.strike(pen) == 2


def test_hot_spring(box):
    g, bots = G(box)
    hs, pal = put(g, 0, "BP01-041"), put(g, 0, "BP01-032")
    t1, t2 = put(g, 1, "BP01-028"), put(g, 1, "BP01-038")
    act(g, bots, hs, 0, [[t1.uid, t2.uid]], assign=pal)
    assert t1.rested and t2.rested and 1 in t1.skip_stand


def test_antique_mirror_and_sphere_workbench(box):
    g, bots = G(box)
    play(g, bots, 0, "BP01-042")
    assert len(g.players[0].hand) == 1
    sw, pal = put(g, 0, "BP01-043"), put(g, 0, "BP01-032")
    act(g, bots, sw, 0, [[g.players[0].hand[0].uid]], assign=pal)
    assert len(g.players[0].hand) == 2


# ---------------------------------------------------------------- colorless
def test_adventure_begins_first_card_draws(box):
    g, bots = G(box)
    play(g, bots, 0, "BP01-100")
    assert len(g.players[0].hand) == 2


def test_adventure_begins_my_first_pump(box):
    g, bots = G(box)
    g.stats[0].played.append((1, "X"))  # not the first card this game: no draw
    pals = [put(g, 0, c) for c in ("TD01-023", "TD02-023", "TD02-024")]
    play(g, bots, 0, "BP01-100")
    assert len(g.players[0].hand) == 0
    assert all(g.power(p) == 1200 and g.strike(p) == 6 for p in pals)


def test_lamball_promo_same_as_trial(box):
    g, _ = G(box)
    lam = put(g, 1, "PR-001", rested=True)
    att = put(g, 0, "BP01-028")
    assert lam.uid not in g.attack_targets(att)


# ---------------------------------------------------------------- TD01 / TD02
def test_grizzbolt_assault(box):
    g, _ = G(box)
    gz = put(g, 0, "TD01-001")
    t = put(g, 1, "BP01-028")
    assert t.uid in g.attack_targets(gz)


def test_arsox_and_mossanda(box):
    g, bots = G(box)
    play(g, bots, 0, "TD01-005")
    m = put(g, 0, "TD01-006")
    act(g, bots, m, 0)
    assert g.power(m) == 1600 and g.players[0].resources["material"] == 0


def test_blazamut(box):
    g, bots = G(box)
    t = put(g, 1, "BP01-025")
    play(g, bots, 0, "TD01-007", [[t.uid]])
    assert t.zone is Zone.GRAVEYARD


def test_weapon_workbench(box):
    g, bots = G(box)
    wb, pal, other = put(g, 0, "TD01-009"), put(g, 0, "BP01-032"), put(g, 0, "BP01-028")
    g.players[0].resources["material"] = 1
    t = put(g, 1, "BP01-028")
    act(g, bots, wb, 0, [[t.uid]], assign=pal)
    assert t.zone is Zone.GRAVEYARD and g.strike(other) == 3


def test_ignis_breath_is_quick(box):
    g, bots = G(box)
    ib = put(g, 1, "TD01-011", Zone.HAND)
    att = put(g, 0, "BP01-032")
    bots[1].actions.append(PlayCard(ib.uid))
    bots[1].answers.append([att.uid])
    g.perform(Attack(att.uid, None))
    assert att.zone is Zone.GRAVEYARD


def test_suzaku_aqua_vigilance(box):
    g, _ = G(box)
    s = put(g, 0, "TD01-017")
    g.perform(Attack(s.uid, None))
    end_turn(g)
    assert not s.rested


def test_mammorest_cryst(box):
    g, bots = G(box)
    m = put(g, 0, "TD01-018")
    put(g, 0, "TD01-008")
    assert g.power(m) == 1900
    put(g, 0, "BP01-016", Zone.HAND)
    act(g, bots, m, 0, [[g.players[0].hand[0].uid]])
    assert g.strike(m) == 4


def test_antique_wooden_chair(box):
    g, bots = G(box)
    p = put(g, 0, "BP01-028")
    play(g, bots, 0, "TD01-019", [[p.uid]])
    assert g.power(p) == 1600


def test_primitive_workbench(box):
    g, bots = G(box)
    pw, pal = put(g, 0, "TD01-020"), put(g, 0, "BP01-032")
    gear = put(g, 0, "BP01-021", Zone.DECK)
    act(g, bots, pw, 0, [[True]], assign=pal)
    assert gear.zone is Zone.BASE


def test_sphere_launcher(box):
    g, bots = G(box)
    sl = play(g, bots, 0, "TD01-021")
    assert len(g.players[0].hand) == 1
    p = put(g, 0, "BP01-028")
    act(g, bots, sl, 0, [[p.uid]])
    assert g.power(p) == 800


def test_crystal_breath(box):
    g, bots = G(box)
    t = put(g, 1, "BP01-025")
    play(g, bots, 0, "TD01-022", [[t.uid]])
    assert g.strike(t) == -1 and 1 in t.skip_stand


def test_ribbuny_and_chikipi(box):
    g, _ = G(box)
    r, c = put(g, 0, "TD01-024"), put(g, 0, "TD02-024")
    g.send_to_graveyard(r)
    g.send_to_graveyard(c)
    g.check_timing()
    res = g.players[0].resources
    assert res["material"] == 1 and res["ingredient"] == 1


# ---------------------------------------------------------------- green (gf deck)
def test_warsect_taunt_and_wumpo_interrupt(box):
    g, bots = G(box)
    att = put(g, 0, "BP01-028")
    w = put(g, 1, "BP01-054", rested=True)   # Warsect, rested so it's attackable
    other = put(g, 1, "BP01-028", rested=True)
    assert g.attack_targets(att) == [w.uid]  # Taunt: only Warsect
    wb = put(g, 1, "BP01-062", Zone.HAND)
    bots[1].actions.append(UseInterrupt(wb.uid, None))
    g.perform(Attack(att.uid, w.uid))
    assert w.damage == 0 and wb.zone is Zone.GRAVEYARD


def test_stone_blast_quick_saves_blocker(box):
    from bots import RuleBot
    g, bots = G(box)
    g.agents[1] = RuleBot()
    att = put(g, 0, "BP01-025")                 # Chillet 900
    v = put(g, 1, "BP01-028", rested=True)      # Pengullet 600, attacked; no blocker available
    sb = put(g, 1, "TD02-011", Zone.HAND)
    g.perform(Attack(att.uid, v.uid))
    # Pengullet 600 vs 900: Stone Blast (+500 -> 1100) saves it and kills Chillet
    assert sb.zone is Zone.GRAVEYARD and v.zone is Zone.BASE and att.zone is Zone.GRAVEYARD
