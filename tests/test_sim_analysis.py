"""sim runner + analysis (small batches, single process)."""
import json

import pytest

from analysis.report import draw_impact, write_report
from analysis.tags import loss_tags, rnd
from cards.db import DEFAULT_PATH, load_card_db
from sim.runner import MatchSpec, game_seed, make_game, rate, run, wilson

pytestmark = pytest.mark.skipif(not DEFAULT_PATH.exists(), reason="data/cards.json missing")
SPEC = MatchSpec("data/decks/cattiva-azurobe-br.txt", "data/decks/chillet-relaxaurus-bp.txt")


def test_wilson():
    lo, hi = wilson(56, 100)
    assert 0.46 < lo < 0.47 and 0.65 < hi < 0.66
    assert wilson(0, 0) == (0.0, 0.0)


def test_rate_counts_draws_as_half():
    gs = [{"winner": "deck"}, {"winner": "draw"}, {"winner": "opp"}, {"winner": "opp"}]
    r = rate(gs)
    assert r["win_rate"] == 0.375 and r["draws"] == 1


def test_run_writes_outputs_and_replays(tmp_path):
    s = run(SPEC, games=6, seed=7, out=tmp_path, workers=1, logs=1, progress=False)
    assert s["games"] == 6 and s["going_first"]["games"] + s["going_second"]["games"] == 6
    recs = [json.loads(x) for x in (tmp_path / "games.jsonl").read_text().splitlines()]
    assert len(recs) == 6 and recs[0]["seed"] == game_seed(7, 0)
    for key in ("seed", "winner", "turns", "drawn", "first"):
        assert key in recs[0]
    g = make_game(SPEC, recs[0]["seed"], log=True)
    g.play()
    assert "\n".join(g.lines) == (tmp_path / "logs" / f"game_{recs[0]['seed']}.log").read_text()
    report = write_report(tmp_path).read_text()
    assert "Why cattiva-azurobe-br loses" in report and "Calibration" in report


def test_same_seed_same_results(tmp_path):
    a = run(SPEC, 4, 3, tmp_path / "a", workers=1, logs=0, progress=False)
    b = run(SPEC, 4, 3, tmp_path / "b", workers=2, logs=0, progress=False)
    assert (tmp_path / "a" / "games.jsonl").read_text() == (tmp_path / "b" / "games.jsonl").read_text()
    assert a["win_rate"] == b["win_rate"]


def test_loss_tags_synthetic():
    db = load_card_db()
    g = {"winner": "opp", "first": "opp", "turns": 10, "reason": "life",
         "opening": [["BP01-002"] * 5, []],  # all ◇7: weak opening
         "played": [[[6, "BP01-002"]], []],
         "history": [[t, (t + 1) % 2, [10, 10], [5, 5], [40, 40], [0, 2], [0, 1500]]
                     for t in range(1, 11)],
         "life_lost_to": [{"BP01-027": 9, "BP01-025": 1}, {}],
         "lucky_saves": [0, 0]}
    tags = loss_tags(g, db)
    assert "weak_opening_hand" in tags and "no_early_play" in tags
    assert "behind_on_board_by_round_1-3" in tags and "lost_to:BP01-027" in tags
    assert "too_slow_on_the_draw" in tags
    assert rnd(1) == 1 and rnd(4) == 2


def test_draw_impact_math():
    gs = ([{"drawn": [["X"], []], "winner": "deck"}] * 40
          + [{"drawn": [[], []], "winner": "opp"}] * 40)
    (row,) = draw_impact(gs, 0)
    assert row["delta"] == 1.0 and row["significant"]


def test_matrix_small(tmp_path):
    from sim.matrix import run_matrix, win_rate
    decks = ["data/decks/cattiva-azurobe-br.txt", "data/decks/chillet-relaxaurus-bp.txt"]
    r = run_matrix(decks, games=4, seed=2, out=tmp_path, workers=1)
    (p,) = r["pairs"]
    assert p["real"] == 0.56 and r["calibrated_pairs"] == 1
    assert win_rate(r, "chillet-relaxaurus-bp", "cattiva-azurobe-br") == 1 - p["sim"]
    assert "Calibration" in (tmp_path / "matrix.md").read_text()


def test_field_weights_normalised():
    from sim.gauntlet import allocate, field_weights
    w = field_weights()
    assert abs(sum(w.values()) - 1) < 1e-9 and "cattiva-azurobe-br" in w
    assert max(w, key=w.get) == "chillet-relaxaurus-bp"
    a = allocate(w, 1000)
    assert a["chillet-relaxaurus-bp"] > a["chillet-relaxaurus-bg"] >= 20


def test_optimizer_smoke(tmp_path):
    import sim.optimize as opt
    cfg = opt.TestConfig(batch=24, max_batches=2, confirm_games=24)
    best = opt.optimize("data/decks/cattiva-azurobe-br.txt", rounds=1, bot="rules",
                        confirm_bot="rules", max_tries=2, cfg=cfg, baseline_games=40,
                        matrix_dir=str(tmp_path / "none"), results=tmp_path)
    assert best.exists()
    assert (tmp_path / "experiments.md").read_text().count("| rules |") >= 1


def test_proposals_are_legal():
    import cards
    from pathlib import Path
    from cards.db import load_card_db
    from sim.optimize import is_legal, propose, read_list
    db = load_card_db()
    main, soul = read_list(Path("data/decks/cattiva-azurobe-br.txt"))
    stats = {c: {"impact": 0.0, "stuck": 0.0, "drawn": 10} for c in main}
    swaps = propose(main, soul, stats, {}, db, cards.REGISTRY, 2)
    assert swaps
    for o, i in swaps:
        m = main.copy()
        m[o] -= 2
        m[i] += 2
        assert is_legal(+m, soul, db) and db[i].color.value in ("red", "blue", "colorless")


def test_gauntlet_command(tmp_path):
    import json
    from sim.__main__ import main
    assert main(["gauntlet", "--deck", "data/decks/cattiva-azurobe-br.txt", "--games", "60",
                 "--bot", "rules", "--seed", "3", "--out", str(tmp_path), "--workers", "2"]) == 0
    s = json.loads((tmp_path / "summary.json").read_text())
    assert s["games"] >= 60 and set(s["field"]) >= {"chillet-relaxaurus-bp"}
    msg = (tmp_path / "telegram.txt").read_text()
    assert msg.startswith("cattiva-azurobe-br:") and len(msg) <= 900 and "Worst:" in msg


def test_noise_z():
    from sim.matrix import noise_z
    p = {"real": 0.56, "real_games": 2389, "sim": 0.567, "games": 4000}
    assert abs(noise_z(p)) < 1
    p = {"real": 0.56, "real_games": 705, "sim": 0.847, "games": 1000}
    assert noise_z(p) > 10
    assert noise_z({"real": 0.5, "real_games": None, "sim": 0.6, "games": 10}) is None


def test_compare_command(tmp_path):
    from sim.__main__ import main
    out = tmp_path / "cmp.md"
    assert main(["compare", "--a", "data/decks/cattiva-azurobe-br.txt",
                 "--b", "results/runs/cattiva-azurobe-br_after-chillet-swap.txt",
                 "--games", "40", "--bot", "rules", "--workers", "2", "--out", str(out)]) == 0
    text = out.read_text()
    assert "chillet-relaxaurus-bp" in text and "diff" in text


def test_all_swaps_covers_new_cards_and_is_legal():
    import cards
    from pathlib import Path
    from cards.db import load_card_db
    from sim.optimize import all_swaps, is_legal, read_list
    db = load_card_db()
    main, soul = read_list(Path("results/runs/cattiva_chillet+blazehowl.txt"))
    stats = {c: {"impact": 0.0, "stuck": 0.0, "drawn": 10} for c in main}
    swaps = all_swaps(main, soul, stats, db, cards.REGISTRY, 2, 4)
    ins = {i for _, i in swaps}
    assert {"BP01-003", "BP01-031", "TD01-007"} <= ins  # Gobfin, Penking, Blazamut
    assert len({o for o, _ in swaps}) <= 4
    for o, i in swaps[:50]:
        m = main.copy()
        m[o] -= 2
        m[i] += 2
        assert is_legal(+m, soul, db)


def test_optimizer_with_screening(tmp_path, monkeypatch):
    import sim.optimize as opt
    real = opt.all_swaps
    monkeypatch.setattr(opt, "all_swaps", lambda *a, **k: real(*a, **k)[:2])
    cfg = opt.TestConfig(batch=20, max_batches=2, confirm_games=20, screen_games=20,
                         screen_outs=1)
    best = opt.optimize("results/runs/cattiva_chillet+blazehowl.txt", rounds=1, bot="rules",
                        confirm_bot="rules", max_tries=1, cfg=cfg, baseline_games=30,
                        matrix_dir=str(tmp_path / "none"), results=tmp_path)
    assert best.exists() and list((tmp_path / "opt").glob("*/screen_round1.md"))


def test_real_vs_sim_report(tmp_path):
    from analysis.real_vs_sim import binom_p, load_games, report
    csv_path = tmp_path / "g.csv"
    rows = ["date,event,my_deck,opp_deck,first_or_second,result,notes"]
    rows += ["2026-10-02,weekly,cattiva-br,chillet-bp,first,W,"] * 10
    rows += ["2026-10-02,weekly,cattiva-br,mystery-deck,second,D,"]
    csv_path.write_text("\n".join(rows) + "\n")
    games = load_games(csv_path, {"cattiva-br": "cattiva-azurobe-br",
                                  "chillet-bp": "chillet-relaxaurus-bp"})
    text = report("cattiva-azurobe-br", games,
                  {"field": {"chillet-relaxaurus-bp": {"win_rate": 0.66}}})
    assert "| chillet-relaxaurus-bp | 10 | 10-0 | 100% | 56% (n=2389) | 66% | above online |" in text
    assert "mystery-deck | 1 | 0-0-1" in text
    assert report("cattiva-azurobe-br", []).startswith("No games logged yet")
    assert abs(binom_p(5, 10, 0.5) - 1.0) < 1e-9 and binom_p(10, 10, 0.5) < 0.01
