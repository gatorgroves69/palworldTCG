# Palify public ranked replays — top-50 snapshot

Source and attribution: [Palify](https://palify.org), public ranked online games, read-only GET endpoints. Collected for Bobby's noncommercial study; Claude owns calibration analysis. This dataset is **not** an estimate of population win rates or real-world tournament performance.

## Scope and selection
- Current global top50 ranks frozen once from `/api/pvp/ladder`; see `top50.json` and response metadata for exact capture time.
- One public `/u/<handle>` page per selected ladder player; no private-history probing, pagination or unlimited backfill.
- Up to six most recent visible completed entries with `format=standard`, `mode=standard` per player. Private histories explicitly skipped. Deduplicated by match UUID and fetched round-robin; cap300 unique replay IDs.
- Candidate selection is frozen in `selection.json`. The replay's explicit `view.ranked` flags, not rating changes alone, determine final ranked eligibility.
- `/api/pvp/match/<id>/replay` supplies actual timeline/result; publicly exposed match-specific `/decks` supplies both full **main** deck snapshots. No soul counts invented. These are historical match decks, not the player's current saved deck.
- Requests serialized at least3 seconds apart, cached by URL, no credentials/cookies/auth, POSTs, retries or simulations. Stop on401/403/429. `requests.jsonl` and `cache/*.meta.json` contain HTTP provenance and SHA256 of decompressed response bytes; raw bytes retained as deterministic gzip.
- `robots.txt` disallows API indexing/crawling, while Palify's `/developers` and `/terms` explicitly permit reasonable cached noncommercial public API use. These responses are cached. This bounded API collection follows that published permission.

## Claude: start here
- `games.jsonl`: one unique ranked game per row, complete source/evidence/quality metadata, both main-deck count maps, player identities, inferred archetypes and candidate overlaps.
- `games.csv`: flattened convenience view, same unique match rows.
- `summary.json`, `validation.json`: actual completion counts and quality coverage. A summary written during collection can be partial; **validation status PASS plus a completed handoff** is the completion gate.
- `selection.json`: every top50 player accounted for, explicit private status, selected history entries, all discovery routes for duplicate matches.
- `acquired.jsonl`: one terminal acquisition status for every selected ID, including unavailable/excluded responses rather than silent drops.
- `cache/`: raw replay/deck/profile/ladder responses and request metadata. `cached()` in normalize.py reads and verifies hashes without network.

## First player and winner: important pitfalls
The profile history `wentFirst` field **disagrees with actual replay first-turn choices in observed games**. It is retained only in `history_comparison`, never silently used as ground truth. Primary first-player evidence is consensus of explicit setup `firstIsMe`, the named “takes the first turn” log, and the **earliest active frame at turn1**. Later frames can retain turn1 while the other player acts, so taking every turn1 frame would falsely create conflicts.

Map every `me/opp` or `you/bot` through that frame's view/hands names into replay `names.p1/p2`. Replay anchoring is not guaranteed to be p1: one observed replay has p2 as `me/you`. Never equate `you` with p1 or assume the profile owner wins. Winner comes from the terminal finished replay view. Disagreements, unknowns, ambiguous names, truncated starts, nonfinished records, short games and selected timeout reasons are flagged. No unknown first player/winner is guessed. Historical profile rank/rating and current snapshot rank are distinct.

## Archetypes
`archetypes.py` is deterministic offline inference, **not a Palify-authoritative label**. `source=inferred`, `site_authoritative=false`, classifier version, rule evidence and ranked canonical overlaps are retained. Ten frozen local reference lists plus broader engine signatures support conservative labels; exact50-card identity is strongest, overlap alone never forces a match. `unknown` and `mixed` are deliberate abstentions. Confidence is an authored heuristic, not a calibrated probability. Canonical lists are non-exhaustive and alternate-printing equivalence is not guessed. Full main counts are retained so Claude can revise labels without more requests.

## Bias and limitations
This is a current-top50 **convenience sample**, not a random sample of all ranked games. It is conditioned on leaderboard success, public histories, the limited visible history window and successful replay availability. Games may predate capture substantially; inspect source millisecond timestamps and validation's date range. Players/repeated opponents and deck variants are clustered; a match discovered from both players is still only one observation. Private-history users can appear as opponents in independently public matches. Friendly/custom games excluded. Online manual play, concessions, errors and short games are not physical-event adjudication. Calibration, first/second performance estimates and model tuning are explicitly deferred to Claude.

## Reproduce offline
From this directory:
```sh
python3 -B -m unittest discover -p 'test_*.py' -v
python3 normalize.py
python3 validate.py
```
`collect.py` is the optional bounded resumable acquisition entry point; it uses cached successful URLs, refuses a recorded access block and never broadens beyond the frozen selection. Do not start another network collection merely to analyze this dataset. `SESSION.md` records scope and collection history.
