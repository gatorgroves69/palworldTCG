# palworldTCG

A simulation lab for the **Palworld Official Card Game** (Bushiroad). It plays decks against each other thousands of times to measure matchups and find card swaps that improve a deck.

Status: the rules engine skeleton is done. Card implementations are waiting on `data/`. See [docs/rules.md](docs/rules.md) for the rules as implemented and [docs/assumptions.md](docs/assumptions.md) for the interpretations that still need confirming.

## Layout

| Path | What |
|---|---|
| `engine/` | Game state, turns, battle, damage checks, rule actions, deck legality. Pure logic, no I/O |
| `cards/` | One implementation per card code in `REGISTRY`, plus the decklist parser. A deck with an unimplemented card fails loudly |
| `bots/` | AI players behind `bots.base.Bot`. `RandomBot` is only for fuzzing the engine; the heuristic bot comes next |
| `data/` | Card data, decklists and calibration data. **Owned by Hermes**; don't edit it by hand |
| `docs/` | Rules and assumptions |
| `tests/` | pytest. `tests/fixtures.py` defines test-only `T-*` cards |

## Running tests

Requires Python 3.11+. The engine has no runtime dependencies.

```bash
python -m pip install pytest
python -m pytest -q
```

Or, with [uv](https://docs.astral.sh/uv/):

```bash
uv run --with pytest python -m pytest -q
```

## Credits

- Card data comes from **[Palify](https://palify.org)**'s free card API (`https://palify.org/api/cards`). It's cached in `data/cards.json` so the API isn't hit on every run. Thanks to Palify for the API, the rules transcription and the browser simulator.
- Rules follow Bushiroad's Comprehensive Rules v1.00 and Quick Manual (<https://en.palworld-official-cardgame.com/rule/>).
- Palworld and the Palworld OCG are the property of Pocketpair and Bushiroad. This is an unaffiliated fan project.
