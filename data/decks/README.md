# Deck collection status

The engine agent committed eight validated decklists at the user's request:

- `cattiva-azurobe-br.txt`
- `chillet-relaxaurus-bp.txt`
- `chillet-relaxaurus-br.txt`
- `chillet-relaxaurus-bg.txt`
- `lamball-stone-pit-pr.txt`
- `lamball-cattiva-bg.txt`
- `shadowbeak-menasting-bp.txt`
- `foxparks-harness-br.txt`

The two missing decks from the requested top-eight queue are:

- `tombat-medicine-gp.txt`
- `machine-gun-furnace-br.txt`

Collection is not globally blocked: the eight lists above are available. The two missing lists still require real source exports; do not invent quantities. Initial automated source collection encountered HTTP 403.

For each new real export, run:

```sh
python3 -m cards.validate data/decks/<file>.txt
```

Require `RESULT: OK` with no `WARNING` lines. Validate `# main` = 50, `# soul` = 10, and every card code exists in `data/cards.json`.

The full requested top-eight-by-play-rate queue is recorded in `data/sources/2026-09-29/provenance.json` (`requested_top8`).
