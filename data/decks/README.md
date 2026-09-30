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

The two previously missing decks were added from real palworldtcg.gg Copy list exports on 2026-09-30 and passed validation without warnings:

- `tombat-medicine-gp.txt`
- `machine-gun-furnace-br.txt`

All ten lists are now available. Raw exports are preserved in `data/sources/2026-09-30/`; source URLs and normalization details are in `data/sources/progress.md`. Main-deck quantities are unchanged from the exports. The exports omit Souls, so each normalized list includes the repository-standard `10 SOUL-001 Soul` section required by the validator. Initial automated source collection encountered HTTP 403; these exports were retrieved through the public site's Copy list buttons.

For each new real export, run:

```sh
python3 -m cards.validate data/decks/<file>.txt
```

Require `RESULT: OK` with no `WARNING` lines. Validate `# main` = 50, `# soul` = 10, and every card code exists in `data/cards.json`.

The full requested top-eight-by-play-rate queue is recorded in `data/sources/2026-09-29/provenance.json` (`requested_top8`).
