"""At least one test per card added in M2 (plus the night / resource machinery).

Both players get a "toolbox" deck with 2 copies of every implemented card, so any
board can be arranged. Lucky cards are moved to the bottom so damage checks are
predictable.
"""
import pytest

from cards import REGISTRY
from cards.db import DEFAULT_PATH, load_card_db
from engine import (Activate, Attack, CardType, Deck, Decision, Game, PlayCard, RulesConfig,
                    UseInterrupt, Zone)
from tests.fixtures import ScriptedBot

pytestmark = pytest.mark.skipif(not DEFAULT_PATH.exists(), reason="data/cards.json missing")


@pytest.fixture(scope="module")
def box():
    db = load_card_db()
    main = [db[c] for c in REGISTRY.codes() if db[c].type is not CardType.SOUL for _ in range(4)]
    return Deck("toolbox", main, [db["SOUL-001"]] * 10)


def G(box, rules=None):
    bots = [ScriptedBot(), ScriptedBot()]
    g = Game([box, box], REGISTRY, bots, seed=3, log=True, rules=rules)
    g.setup()
    for ps in g.players:
        for c in list(ps.hand):
            g.move(c, Zone.DECK)
        ps.deck.sort(key=lambda c: c.defn.lucky)
        ps.souls, ps.soul_deck, ps.souls_rested = 10, 0, 0
    g.active, g.turn, g.phase = 0, 3, "main"
    return g, bots


def put(g, p, code, zone=Zone.BASE, rested=False):
    c = next(c for c in g.players[p].deck if c.code == code)
    if zone is Zone.BASE:
        g.deploy(c)
        g.pending.clear()
        c.rested = rested
    elif zone is Zone.DECK:  # to the top
        g.players[p].deck.remove(c)
        g.players[p].deck.insert(0, c)
    else:
        g.move(c, zone)
    return c


def play(g, bots, p, code, answers=(), mode=None):
    c = put(g, p, code, Zone.HAND)
    bots[p].answers.extend(answers)
    g.perform(PlayCard(c.uid, mode))
    return c


def act(g, bots, c, index=0, answers=(), assign=None, x=None):
    bots[c.owner].answers.extend(answers)
    a = Activate(c.uid, index, assign.uid if assign else None, x)
    assert a in g.legal_actions(c.owner), (a, g.legal_actions(c.owner))
    g.perform(a)


def end_turn(g):
    """Run the current turn's end phase; the turn passes to the other player."""
    g.end_phase()


# ---------------------------------------------------------------- red
def test_jormuntide_ignis_stand_shared_limit(box):
    g, bots = G(box)
    ig = put(g, 0, "BP01-001", rested=True)
    acts = [a for a in g.legal_actions(0) if isinstance(a, Activate) and a.uid == ig.uid]
    assert {a.index for a in acts} == {0}  # no hand: only the ③ version
    for code in ("BP01-047", "BP01-048"):
        put(g, 0, code, Zone.HAND)
    act(g, bots, ig, 1, [[g.players[0].hand[0].uid, g.players[0].hand[1].uid]])
    assert not ig.rested and len(g.players[0].hand) == 0
    ig.rested = True
    assert not any(isinstance(a, Activate) and a.uid == ig.uid for a in g.legal_actions(0))


def test_reptyro_material_and_gear_dig(box):
    g, bots = G(box)
    victim = put(g, 1, "BP01-025")  # 900
    play(g, bots, 0, "BP01-005")
    rep = next(c for c in g.players[0].pals if c.code == "BP01-005")
    assert g.players[0].resources["material"] == 3
    gun = put(g, 0, "BP01-020", Zone.DECK)
    act(g, bots, rep, 0, [[gun.uid]])
    assert gun.zone is Zone.BASE and victim.zone is Zone.GRAVEYARD  # Shotgun OnDeploy fired
    assert g.players[0].resources["material"] == 0


def test_foxparks_light_of_courage_brave(box):
    g, _ = G(box)
    f = put(g, 0, "BP01-006")
    g.perform(Attack(f.uid, None))
    assert g.power(f) == 500


@pytest.mark.parametrize("code", ["BP01-014", "TD02-004"])
def test_new_interrupts(box, code):
    g, bots = G(box)
    att = put(g, 0, "BP01-028")
    i = put(g, 1, code, Zone.HAND)
    bots[1].actions.append(UseInterrupt(i.uid, None))
    g.perform(Attack(att.uid, None))
    assert g.players[1].life == 10 and i.zone is Zone.GRAVEYARD


def test_mounted_machine_gun_x(box):
    g, bots = G(box)
    mmg, pal = put(g, 0, "BP01-015"), put(g, 0, "BP01-032")
    t = put(g, 1, "BP01-026")  # 1200
    g.players[0].resources["material"] = 3
    xs = sorted(a.x for a in g.legal_actions(0) if isinstance(a, Activate) and a.uid == mmg.uid)
    assert xs == [1, 2, 3]
    act(g, bots, mmg, 0, [[t.uid], [t.uid]], assign=pal, x=2)
    assert t.damage == 1000 and pal.rested and g.players[0].resources["material"] == 1


def test_primitive_furnace_material_draw_and_discount(box):
    g, bots = G(box)
    fur, pal = put(g, 0, "BP01-016"), put(g, 0, "BP01-032")
    act(g, bots, fur, 0, assign=pal)
    assert g.players[0].resources["material"] == 3 and len(g.players[0].hand) == 1
    gun = put(g, 0, "BP01-020", Zone.HAND)
    act(g, bots, fur, 1, x=2)
    assert g.cost(gun) == 5
    g.perform(PlayCard(gun.uid))
    assert g.players[0].gear_discount == 0  # only the next gear


def test_furnace_discount_floor_is_one(box):
    g, _ = G(box)
    harness = put(g, 0, "BP01-019", Zone.HAND)  # ◇3
    g.players[0].gear_discount = 5
    assert g.cost(harness) == 1


def test_foxparks_harness_grants_on_attack(box):
    g, bots = G(box)
    h, fox = put(g, 0, "BP01-019"), put(g, 0, "TD01-004")
    t = put(g, 1, "BP01-028")  # 600
    act(g, bots, h, 0, [[fox.uid]])
    assert g.power(fox) == 600 and fox.granted_auto
    bots[0].answers.append([t.uid])
    g.perform(Attack(fox.uid, None))
    assert t.zone is Zone.GRAVEYARD  # 700 from the granted OnAttack


def test_harness_on_non_foxparks_only_200(box):
    g, bots = G(box)
    h, p = put(g, 0, "BP01-019"), put(g, 0, "BP01-028")
    act(g, bots, h, 0, [[p.uid]])
    assert g.power(p) == 800 and not p.granted_auto


def test_axels_strategy_modes(box):
    g, bots = G(box)
    t = put(g, 1, "BP01-026")
    play(g, bots, 0, "BP01-023", [[t.uid]], mode=0)
    assert t.zone is Zone.GRAVEYARD
    g.players[0].souls_rested = 0  # three 4-cost events in one test
    put(g, 0, "BP01-020")  # 1 gear
    mine = put(g, 0, "BP01-028", rested=True)
    play(g, bots, 0, "BP01-023", [[mine.uid]], mode=1)
    assert not mine.rested
    big, small = put(g, 1, "BP01-025"), put(g, 1, "BP01-032")
    g.players[0].souls_rested = 0
    play(g, bots, 0, "BP01-023", mode=2)
    assert not g.can_block(big) and g.can_block(small)


# ---------------------------------------------------------------- blue / green
def test_teafant_serious(box):
    g, bots = G(box)
    pit, tea = put(g, 0, "TD01-008"), put(g, 0, "BP01-034")
    other = put(g, 0, "BP01-028")
    act(g, bots, pit, 0, [[other.uid]], assign=tea)
    assert g.power(other) == 1000


def test_grappling_gun_vigilance(box):
    g, bots = G(box)
    gun, p = put(g, 0, "BP01-045"), put(g, 0, "BP01-028")
    act(g, bots, gun, 0, [[p.uid]])
    g.perform(Attack(p.uid, None))
    assert p.rested
    end_turn(g)
    assert not p.rested


def test_victors_strategy_modes(box):
    g, bots = G(box)
    want = put(g, 0, "BP01-002", Zone.DECK)
    play(g, bots, 0, "BP01-046", [[want.uid]], mode=0)
    assert want.zone is Zone.HAND
    t = put(g, 1, "BP01-026")
    play(g, bots, 0, "BP01-046", [[t.uid]], mode=1)
    assert t.zone is Zone.HAND
    put(g, 0, "TD01-008"), put(g, 0, "BP01-016")
    n = len(g.players[0].hand)
    play(g, bots, 0, "BP01-046", mode=2)
    assert len(g.players[0].hand) == n + 2


def test_lyleen_ingredient_and_dig(box):
    g, bots = G(box)
    play(g, bots, 0, "BP01-049")
    ly = next(c for c in g.players[0].pals if c.code == "BP01-049")
    assert g.players[0].resources["ingredient"] == 3
    target = put(g, 0, "BP01-038", Zone.DECK)  # Cryolinx ◇6
    act(g, bots, ly, 0, [[target.uid]])
    assert target.zone is Zone.BASE and g.players[0].resources["ingredient"] == 0


def test_rushoar_vs_structure(box):
    g, _ = G(box)
    r = put(g, 0, "BP01-052")
    pit = put(g, 1, "TD01-008")  # durability 600
    g.perform(Attack(r.uid, pit.uid))
    assert pit.zone is Zone.GRAVEYARD and g.power(r) == 1000 and r.damage == 0


def test_lilys_strategy_modes(box):
    g, bots = G(box)
    a, b = put(g, 0, "BP01-028"), put(g, 0, "BP01-032")
    play(g, bots, 0, "BP01-070", mode=0)
    assert g.power(a) == 1600 and g.power(b) == 1200
    gear = put(g, 1, "BP01-020")
    play(g, bots, 0, "BP01-070", [[gear.uid]], mode=1)
    assert gear.zone is Zone.GRAVEYARD
    g.players[0].soul_deck = 1
    play(g, bots, 0, "BP01-070", mode=2)
    ps = g.players[0]
    assert ps.souls == 11 and ps.soul_deck == 0 and ps.souls_rested >= 1


def test_found_an_egg(box):
    g, bots = G(box)
    pal = put(g, 0, "BP01-028", Zone.DECK)
    play(g, bots, 0, "BP01-071", [[pal.uid]])
    assert pal.zone is Zone.HAND and g.players[0].resources["ingredient"] == 0
    play(g, bots, 0, "BP01-071", [[]])
    assert g.players[0].resources["ingredient"] == 3


# ---------------------------------------------------------------- purple / night
def test_night_timing_until_end_of_opponents_next_turn(box):
    g, _ = G(box)
    g.make_night(0)  # turn 3, P1's own turn
    end_turn(g)  # end of turn 3: still night
    assert g.is_night() and g.active == 1
    g.begin_turn()  # turn 4: the opponent's next turn
    assert g.is_night()
    end_turn(g)
    assert not g.is_night()


def test_daedream_and_depresso_nocturnal(box):
    g, _ = G(box)
    d, dp = put(g, 0, "BP01-080"), put(g, 0, "BP01-079")
    g.night = True
    assert g.power(d) == 500 and g.power(dp) == 700


def test_lamp_night_and_granted_nocturnal(box):
    g, bots = G(box)
    lamp, dd, p = put(g, 0, "BP01-088"), put(g, 0, "BP01-082"), put(g, 0, "BP01-028")
    act(g, bots, lamp, 0)
    assert g.is_night() and len(g.players[0].graveyard) == 3
    assert g.power(p) == 900 and g.power(dd) == 1000  # Daedream: two instances
    theirs = put(g, 1, "BP01-028")
    assert g.power(theirs) == 600


def test_shoddy_bed_draws_with_rested_nocturnal(box):
    g, bots = G(box)
    bed = put(g, 0, "BP01-089")
    put(g, 0, "BP01-080", rested=True)
    act(g, bots, bed, 0)
    assert g.is_night()
    n = len(g.players[0].hand)
    end_turn(g)
    assert len(g.players[0].hand) >= n + 1


def test_maraith_night_and_aura(box):
    g, _ = G(box)
    m = put(g, 0, "BP01-085")
    t = put(g, 1, "BP01-028")
    assert not g.is_night() and g.power(t) == 600
    m.rested = True
    assert g.is_night() and g.power(t) == 400 and g.power(m) == 900


def test_helzephyr_kills_on_nocturnal_deploy_at_night(box):
    g, bots = G(box)
    hz = put(g, 0, "BP01-073")
    victim = put(g, 1, "BP01-032")  # ◇2
    big = put(g, 1, "BP01-026")  # ◇7: too expensive for a ◇2 Daedream
    g.night = True
    seen = []
    bots[0].choose = lambda game, d: seen.append(d.options) or [victim.uid]
    play(g, bots, 0, "BP01-080")
    assert victim.zone is Zone.GRAVEYARD and big.uid not in seen[0]
    end_turn(g)
    assert hz.rested


def test_helzephyr_needs_night(box):
    g, bots = G(box)
    put(g, 0, "BP01-073")
    victim = put(g, 1, "BP01-032")
    play(g, bots, 0, "BP01-080", [[victim.uid]])
    assert victim.zone is Zone.BASE


def test_shadowbeak_night_and_double_auto(box):
    g, bots = G(box)
    sb = put(g, 0, "BP01-074")
    pen = put(g, 0, "BP01-028")
    assert not g.is_night()
    sb.rested = True
    assert g.is_night()
    g.send_to_graveyard(pen)
    g.check_timing()
    assert len(g.players[0].hand) == 2  # Pengullet's draw activates twice


def test_shadowbeak_end_of_turn_edict(box):
    g, bots = G(box)
    put(g, 0, "BP01-074")  # standing: not night, so the AUTO activates once
    mine = put(g, 0, "BP01-032")
    theirs = put(g, 1, "BP01-026")
    bots[0].answers.append([mine.uid])
    bots[1].answers.append([theirs.uid])
    end_turn(g)
    assert mine.zone is Zone.GRAVEYARD and theirs.zone is Zone.GRAVEYARD


def test_lyleen_noct_revives_rested(box):
    g, bots = G(box)
    ln = put(g, 0, "BP01-078")
    dead = put(g, 0, "BP01-038", Zone.GRAVEYARD)  # ◇6
    put(g, 0, "BP01-047", Zone.HAND)
    act(g, bots, ln, 0, [[g.players[0].hand[0].uid], [dead.uid]])
    assert dead.zone is Zone.BASE and dead.rested and ln.rested


def test_menasting_retaliate_and_return(box):
    g, bots = G(box)
    m = put(g, 1, "BP01-084", rested=True)
    normal = put(g, 1, "BP01-028", Zone.GRAVEYARD)
    att = put(g, 0, "BP01-026")  # 1200 beats 700
    bots[1].answers.append([normal.uid])
    g.perform(Attack(att.uid, m.uid))
    assert m.zone is Zone.GRAVEYARD and att.zone is Zone.GRAVEYARD
    assert normal.zone is Zone.HAND


def test_workbench_revives_up_to_cost_plus_2(box):
    g, bots = G(box)
    wb, pal = put(g, 0, "BP01-090"), put(g, 0, "BP01-028")  # assigned ◇4 -> up to ◇6
    ok = put(g, 0, "BP01-038", Zone.GRAVEYARD)  # ◇6
    no = put(g, 0, "BP01-026", Zone.GRAVEYARD)  # ◇7
    seen = []
    bots[0].choose = lambda game, d: seen.append(d.options) or [ok.uid]
    act(g, bots, wb, 0, assign=pal)
    assert ok.zone is Zone.BASE and ok.rested and no.uid not in seen[0]
    assert g.players[0].souls_rested == 3


def test_necklace_deploys_daedream_and_makes_night(box):
    g, bots = G(box)
    dd = put(g, 0, "BP01-082", Zone.HAND)
    neck = play(g, bots, 0, "BP01-094", [[dd.uid]])
    assert dd.zone is Zone.BASE
    act(g, bots, neck, 0, [[dd.uid]])
    assert g.is_night() and g.power(dd) == 900


# ---------------------------------------------------------------- TD01 / TD02
def test_stone_pit(box):
    g, bots = G(box)
    pit, pal = put(g, 0, "TD01-008"), put(g, 0, "BP01-032")
    act(g, bots, pit, 0, assign=pal)
    assert g.players[0].resources["material"] == 3 and len(g.players[0].hand) == 1
    assert pal.rested and not any(isinstance(a, Activate) and a.uid == pit.uid
                                  for a in g.legal_actions(0))


def test_single_shot_rifle(box):
    g, bots = G(box)
    t = put(g, 1, "BP01-026")
    rifle = play(g, bots, 0, "TD01-010", [[t.uid]])
    assert t.zone is Zone.GRAVEYARD
    p = put(g, 0, "BP01-028")
    act(g, bots, rifle, 0, [[p.uid]])
    assert g.power(p) == 800


def test_leezpunk_death_discard(box):
    g, bots = G(box)
    lz = put(g, 0, "TD02-014")
    card = put(g, 1, "BP01-047", Zone.HAND)
    g.send_to_graveyard(lz)
    g.check_timing()
    assert card.zone is Zone.GRAVEYARD


def test_structures_rested_only_flag_with_real_structure(box):
    g, _ = G(box, RulesConfig(structures_attackable="rested_only"))
    att = put(g, 0, "BP01-028")
    pit = put(g, 1, "TD01-008")
    assert pit.uid not in g.attack_targets(att)


def test_rulebot_edict_only_when_worth_it(box):
    from bots import RuleBot
    g, _ = G(box)
    small = put(g, 0, "BP01-032")
    put(g, 1, "BP01-026")
    d = Decision("target", 0, "", [small.uid], min=0, max=1, context={"intent": "edict"})
    assert RuleBot().choose(g, d) == [small.uid]
    g2, _ = G(box)
    big = put(g2, 0, "BP01-026")
    put(g2, 1, "BP01-032")
    d2 = Decision("target", 0, "", [big.uid], min=0, max=1, context={"intent": "edict"})
    assert RuleBot().choose(g2, d2) == []
