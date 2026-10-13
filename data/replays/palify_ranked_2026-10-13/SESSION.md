# Public ranked replay collection — Mew data lane

Bobby approved a one-time collection of public Palify ranked replays from the current top50 ladder players, at most a few hundred games, cached and polite, into data/. Claude owns calibration analysis.

Baseline: 05cb20f. Scope owned: this new data/replays/palify_ranked_2026-10-13/ directory only; final concise Mew handoff under AGENT_HANDOFF.md if safe. No modifications to cards.json, data/decks/, data/calibration/, engine, bots, simulation code, active simulation worktrees, cron or model settings. J23 is not authorized by this request.

Bound: maximum300 unique replay IDs, up to six most recent eligible history entries per player. Snapshot top50 first; no backfill/crawling unlimited history. All access is public no-auth GET, sequential minimum3-second request interval, gzip cache by full URL and response hashes, no repeat successful fetches. Stop on401/403/429; no retries or access-control bypass. Public profile HTML supplies discovered match IDs; only those IDs can be fetched. Public match-specific deck snapshots are fetched to avoid inferring full lists from revealed cards.

Access evidence: robots disallows /api/ for crawling, while /developers expressly offers free read-only no-key JSON API and /terms expressly allows reasonable cached noncommercial public API use. Collection follows that explicit API-use permission, not generalized crawling. Original terms/developer/robots responses cached. Palify attribution retained.

Important discovery: profile history wentFirst is not reliably the chosen first player. Pilot 8b089df8-e4f7-4d85-9f72-ca4dc953ff0f marks atto wentFirst=true but replay setup, explicit log and turn1 active player agree the opponent went first. Record replay evidence and profile disagreement separately; do not silently calibrate on profile wentFirst. Replay winner/identity mappings must also be validated, not inferred from which side owns the profile.

Status: collection initiated. No calibration results or simulation changes produced.

## Completion
2026-10-13T03:35:16.312821+00:00: 238 unique public ranked games, 9 private top50 histories skipped. Full offline regression suite and dataset validation PASS; first player known 237/238; winner known 238/238. No cards/decks/calibration/simulation input changes. Main commit/push plus remote ancestry gate follows. Claude calibration handoff: README.md, games.jsonl/csv and validation.json.
