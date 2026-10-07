# palworldTCG

Palworld deck-simulation project. The engine is built by a separate agent; this data lane only collects public data, validates decklists, logs Bobby's games, and runs approved batches.

## Data and credit

- **Card data: [Palify](https://palify.org)** — free read-only [API](https://palify.org/api/cards). `data/cards.json` retains the original response bytes. One request per scheduled run; no retries, scraping loops, or access-block workarounds. Update/commit only when changed.
- Meta/decklist/calibration sources: [palworldtcg.gg](https://palworldtcg.gg/meta) and [Palify meta](https://palify.org/meta). Source evidence and any coverage/filter limitations are recorded under `data/sources/`.
- Cards and art belong to their respective rights holders; this is an unaffiliated project.

### Engine-facing contracts

- `data/cards.json`: raw Palify API object, not a rewritten array. Initial API response has 184 entries / 183 unique codes: `SOUL-001` appears in both starter sets. Consumers must not assume code uniqueness across raw entries.
- `data/decks/<slug>.txt`: `# main`, quantity/code/name rows, `# soul`, quantity/code/name rows. Exactly 50 main + 10 soul; each code must be present in card data.
- Priority files: `cattiva-azurobe-br.txt`, `chillet-relaxaurus-bp.txt`.
- `data/calibration/matchups_<Phoenix YYYY-MM-DD>.json`: array of `{deck_a, deck_b, win_rate_a, games, source}`. Rates are fractions; unavailable game counts are JSON null. Requested population is last 30 days, all games. Do not present unverified populations as calibrated data.
- `data/calibration/tiers_<date>.json`: array of `{deck, win_rate, play_rate}` (fractions), optionally extra provenance fields. Stable deck slugs match matchup/deck files.
- `data/games/real_games.csv`: exact header `date,event,my_deck,opp_deck,first_or_second,result,notes`. Phoenix dates; turns `first`/`second`; results `W`/`L`/`D`; events `weekly`/`palify`/`casual`.

## Operator commands (Python standard library)

```sh
python3 tools/data_ops.py cards
python3 tools/data_ops.py validate
python3 tools/data_ops.py log 'log W chillet-bp 1st weekly — drew stone pit early, opp bricked'
python3 tools/data_ops.py log 'log L cattiva-br 2nd casual — poor opening' --my-deck chillet-relaxaurus-bp
python3 tools/data_ops.py report --month 2026-09
python3 tools/monthly_report.py
python3 -m unittest discover -s tests -v
```

The log commands above are usage examples, **not recorded games**. Own-deck default is `cattiva-azurobe-br` in `config/operator.json`. An explicit own-deck override is supported. Unknown opponent slugs are retained rather than guessed; ambiguous Telegram messages require clarification. Identical game text can represent separate games: the operator must not append the same Telegram message twice on retry.

Telegram logging is agent-operated: send `log W chillet-bp 1st weekly — notes` to Mew. Mew executes the logger, reads back the saved row, and commits only the changed game file. No gateway interception/plugin has been installed.

## Automation and boundaries

Weekly: refresh cards, top-eight decks by play rate, top-twelve 30-day all-game calibration; validate before publishing; compare snapshots for a three-line rose/fell/new-top-five report. First snapshot is a baseline, not a trend. Top-five means play-rate rank for this report. Scheduler details live in `docs/OPERATIONS.md`.

Monthly: previous Phoenix calendar-month win rate overall, by opponent, and first versus second. Rates are wins/all games (draws included in denominator); report sample sizes.

**Overnight simulations are disabled** until Bobby approves milestone 1 and the engine agent supplies the exact command, seed option, game budget and summary output contract. Then use a clean working tree, `git pull --ff-only`, execute the provided command without engine edits, record command/commit/seed/stdout/stderr, and report win rate with confidence range, worst matchup, and top loss reasons. If it crashes, report the actual error and seed (or explicitly say the engine did not expose it). Never fabricate simulation output.

Stop on source access blocks, dirty/conflicting Git state, or schema drift. No force-push, no resets, and no modification of the simulation engine.

## Engine overview

A simulation lab for the **Palworld Official Card Game** (Bushiroad): it plays decks against each other thousands of times, measures matchups, and tests card swaps.

**Status (2026-10-01)**
- **M1 calibration passed.** Cattiva · Azurobe vs Chillet · Relaxaurus BP: sim 56.7%, real 56% (n = 2,389). See [docs/m1-calibration.md](docs/m1-calibration.md).
- **M2: the 10-deck gauntlet is implemented but not calibrated.** Mean absolute error is about 11 points. Decks that build an engine over several turns come out too weak in the sim, because the bots don't plan far enough ahead. See [docs/m2-status.md](docs/m2-status.md).
- **M3: the swap optimizer works.** It uses a screening pass, a sequential test, and confirmation under a second bot. Every attempt is logged in [results/experiments.md](results/experiments.md).
- **M4: the overnight command works.** `sim gauntlet` writes a Telegram-ready summary. Long runs go on the Optiplex (Mew); see [AGENT_HANDOFF.md](AGENT_HANDOFF.md).
- **Cards:** every red/blue/colorless card from BP01, TD01, TD02 and PR is implemented, plus everything the 10 meta decks use. BP02 and SS01 aren't implemented (see docs/assumptions.md C29).

Rules as implemented: [docs/rules.md](docs/rules.md). Interpretations and open questions: [docs/assumptions.md](docs/assumptions.md).

**Commands**

```bash
# one matchup, with report.md (loss tags, draw impact, calibration check)
python -m sim run --deck data/decks/cattiva-azurobe-br.txt --opp data/decks/chillet-relaxaurus-bp.txt --games 2000 --seed 1
# replay any game exactly, with a full log
python -m sim replay --deck data/decks/cattiva-azurobe-br.txt --opp data/decks/chillet-relaxaurus-bp.txt --game-seed 1000000
# every pair of decks vs real matchup data
python -m sim matrix --decks data/decks/*.txt --games 1000 --bot heuristic2
# one list vs the play-rate-weighted field; writes telegram.txt
python -m sim gauntlet --deck results/runs/cattiva_chillet+blazehowl.txt --games 20000
# two lists, per opponent, on identical seeds
python -m sim compare --a <list A> --b <list B> --games 6000 --bot heuristic2
# keep-or-redraw rules for a list, plus going first vs second
python -m sim mulligan --deck <list> --games 8000 --bot heuristic2
# search for swaps (screen every sensible swap, then test the best)
python -m sim optimize --deck <list> --rounds 3 --screen-games 400
# your logged games vs online and sim expectations
python -m analysis.real_vs_sim --summary results/runs/J3-gauntlet/summary.json
python -m cards.validate data/decks/*.txt
```

Heavy runs (matrix, optimize, long gauntlets) take hours and use every core. They belong on the always-on Optiplex, not a laptop.

## Layout

| Path | What |
|---|---|
| `engine/` | Game state, turns, battle, damage checks, rule actions, deck legality. Pure logic, no I/O |
| `cards/` | One implementation per card code in `REGISTRY`; decklist parser and validator. A deck with an unimplemented card fails loudly |
| `bots/` | AI players. `heuristic2` is the default; `heuristic` is the second opinion; the rest are documented experiments (see `bots/__init__.py`) |
| `sim/` | Runner, matrix, weighted gauntlet, A/B compare, optimizer |
| `analysis/` | Loss tags, per-card draw impact, per-run reports, real-games vs sim |
| `results/runs/` | Committed summaries of overnight jobs and the current recommended lists |
| `data/` | Card data, decklists, calibration, real games. **Owned by Mew (Hermes)** |
| `docs/` | Rules, assumptions, milestone reports |
| `tests/` | pytest. `tests/fixtures.py` defines test-only `T-*` cards |

## Running tests

Requires Python 3.11+. The engine has no runtime dependencies.

```bash
uv run --with pytest python -m pytest -q
```

## Credits

- Card data comes from **[Palify](https://palify.org)**'s free card API (`https://palify.org/api/cards`). It's cached in `data/cards.json` so the API isn't hit on every run. Thanks to Palify for the API, the rules transcription and the browser simulator.
- Rules follow Bushiroad's Comprehensive Rules v1.00 and Quick Manual (<https://en.palworld-official-cardgame.com/rule/>).
- Palworld and the Palworld OCG are the property of Pocketpair and Bushiroad. This is an unaffiliated fan project.
