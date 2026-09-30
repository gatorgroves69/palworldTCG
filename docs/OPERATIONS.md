# Data operations handoff

## Ownership
Mew: public data acquisition, validation, Telegram game logging, scheduled reports, and future approved batch execution. Another agent: simulation engine. No engine code has been added or modified in this data setup.

Canonical repo: https://github.com/gatorgroves69/palworldTCG
Local checkout: `/home/gator/palworldTCG`
Default own deck: `cattiva-azurobe-br` (Bobby may change it).

## Current collection status — 2026-09-29 Phoenix
- Palify cards: HTTP 200, raw JSON retained; 184 entries, 183 unique card codes (two SOUL-001 set entries). Exactly one API request during initial collection.
- 144 directed matchup cells including mirrors, top 12 by play rate, 30-day / All games selected in browser. Rates have whole-percent display precision; per-cell game counts were not shown and are null.
- Tier snapshot: 13 rows covering the top 12 most-played plus the top-12 ranked tier union. Not a complete 40-deck tier list. `win_rate` is the displayed field-adjusted rate, not raw win rate. Play rates are fractions of the entire field and are NOT renormalized to this subset.
- Decklists: **0/8 obtained**, including neither priority list. Browser index pages loaded, but subsequent direct archival requests to both domains returned HTTP 403. All further network collection stopped; there was no workaround. Matrix and tier data already observed were preserved with evidence.
- Unblock: Bobby can paste the two Copy-list exports, or provide permitted access/exports. Never fabricate card quantities. Fresh routine weekly attempt is allowed; after a new block stop that source for that run.
- Card, game-logger and report tools exercised. Sample games used only in temporary test directories. Real CSV contains its header only.
- Local `agent-task init` rejected this checkout as outside its allowlisted roots. No allowlist/security settings were changed and initialization was not retried around the denial. Coordination is documented here; `.agent/` initialization remains pending an approved root choice.

## Schedules
Hermes host scheduler uses Eastern time (observed -04:00 in September).
- Weekly data/meta: Monday 11:00 Eastern; job `29a20f78509d`. Next first run 2026-10-05 11:00 -04:00 (08:00 Phoenix). Runtime prompt includes one cards request, bounded browser collection, validation, scoped commit/push, and exactly three meta lines. No immediate second card request was made to test cron.
- Monthly real games: first of month 11:00 Eastern; job `f4cdb5d391a7`. Next first run 2026-10-01 11:00 -04:00 (08:00 Phoenix). Pure Python, no LLM. Reports previous Phoenix calendar month. Entry point at `~/.hermes/scripts/palworld_monthly_report.py` only loads the repo's `tools/monthly_report.py` (Hermes requires scheduler scripts under its scripts directory).
- Eastern daylight-saving changes shift these to 09:00 Phoenix in winter; no fixed Phoenix clock-time promise.
- No overnight batch schedule exists. `config/operator.json` has milestone approval false and no command/games configured.

## Telegram game ingestion
For Bobby messages such as `log W chillet-bp 1st weekly — notes`:
1. Check repo status and pull --ff-only only when clean. Never overwrite another agent's work.
2. Run `python3 tools/data_ops.py log '<exact game text>'`; translate an explicit own-deck selection into `--my-deck <slug>`. `chillet-bp` maps to `chillet-relaxaurus-bp`. Unrecognized/ambiguous own-deck changes require clarification, not guesses.
3. Verify the actual saved CSV row and briefly acknowledge it. Do not double-log a Telegram retry. A repeated textual result may be a distinct game; ask when uncertain.
4. Commit only `data/games/real_games.csv`; push without force and verify. If publishing fails, retain the row and report local-only status.

All logger writes use a lock and atomic CSV replacement; CSV handles notes containing commas/quotes. Monthly reports include sample sizes. An empty sample is not 0%.

## Weekly collection checks
- Obtain main=50 and soul=10, with every code in the current raw catalog, before placing a deck export at an engine path. Invalid evidence can be stored separately, with errors.
- Top8 means play rate, not win-rate/tier order. Required canonical slugs never follow source rename drift; mappings are under `data/sources/2026-09-29/slug-mapping.json`.
- Verify selected window 30 days and game type All rather than assume defaults. Save the relevant DOM snapshot/filter values directly; don't refetch pages just for archival.
- Weekly summary ranks movement and top-five entries by play rate. First run is baseline. Incomplete coverage and stale data must be labeled, not hidden.
- `tools/meta_capture_observed.py` only reconstructs the specific initial observed date; it must NEVER be treated as a live refresh. It depends on the initial cached evidence and is retained solely for audit.
- Card writes are byte-compared; no unchanged card commits. Commit explicit data paths only. On dirty trees, conflict, or non-fast-forward push stop and report; no reset/stash/force.

## Batch approval gate
Before batch deployment, Bobby must approve milestone 1. The engine owner must provide an executable command, game count/budget, seed semantics and summary path/schema. No guessed `python -m sim` command is installed as an active job. Once approved, record git commit, command, seed, start/end, exit code and output; morning report uses actual confidence interval, worst matchup and loss reasons. On crashes return actual stderr and seed (or mark seed unavailable).
