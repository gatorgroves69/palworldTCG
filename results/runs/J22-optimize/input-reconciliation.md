# J22 read-only recovery audit

## Recommendation

Preserve the completed optimizer artifacts, but **do not certify the entire run as a consistent original-card-input execution on the proposed lru_cache rationale: that cache does not exist.** A detached original-head checkout can validate artifact structure and original field weights; it cannot retroactively prove which card bytes each worker read. Do not launch an optimizer rerun merely to repair wrapper bookkeeping. Parent should either explicitly label this completed run's input-refresh provenance limitation, or, if strict original-input certification is required, decide whether a frozen-input rerun is authorized. This audit launches neither simulations nor matrix jobs and makes no Git changes.

There is no evidence here that the six final conclusions numerically changed. Conversely, zero exit and valid summaries do not prove the entire 955-candidate search used original CardDefs. Behavioral equivalence of the changed fields has NOT been established; their presence alone does not prove numerical contamination.

## Hard findings

- Exact original source is retrieved from `034a132b08d16023f6fe63a5a2b7ce0be06b5866`, not inferred from current files. The five audited source files equal both refresh commit `585a291b1a304a69d85075fb17654835a7fa8acc` and the live checkout at audit time. The commit-to-commit diff for sim/cards/engine/bots, data/decks and the baseline deck is empty.
- `failure.json` records the exact approved argv (primary seed 231), launch 2026-10-12 13:52:54.748771 UTC, child exit **0**, end 2026-10-13 02:24:58.135229 UTC. The failure is the controller's post-run input-diff assertion, not the optimizer's exit status.
- Stdout has 955 screened swaps, six sequential tests, no accepted swap. Last candidate passed primary but failed confirmation. Six matching-run JSONL rows exist; `best.txt` is byte-identical to `round0.txt`. These are observed completion facts, not a claim the parent's full artifact validator passed.

## Exact caching and reload behavior

Source line references below refer to saved `*.numbered.txt` extracts.

1. `sim/optimize.py:277-284`: parent loads card DB once, computes field weights once, reads baseline counts once and writes round0. Parent retains `db`, `weights`, `main`, `soul` for the complete run. Candidate legality, candidate choices, names printed in all generated decks and experiment rows use that original parent DB. Thus old names in generated decks do **not** prove workers used old CardDefs.
2. `sim/gauntlet.py:28-38`: field weights come from lexicographically latest tiers JSON at that one call. Newly added October 12 calibration does not change the already retained dict. Stdout matches original October 5 normalized weights exactly at printed precision. Original 800-game allocation actually sums to 807; observed 1614 and 4035 counts match two/five looks. Matchups JSON is not read on this path.
3. `sim/gauntlet.py:87-98,106-128`: one reusable multiprocessing pool per `workers` key; optimizer calls use default `None`. Pool reuse is **not** database caching. No maxtasksperchild is passed; process replacement is still not logged.
4. `sim/runner.py:38-56`: each worker has `_CACHE`, keyed by full frozen `MatchSpec` (deck path, opponent path, bot, rules/cards/mulligan/deck_bot). A cache hit reuses both built decks, registry and bot class. A cache miss calls `load_card_db`, then loads BOTH deck files against that new DB, validates them and caches the tuple.
5. `cards/db.py:50-65`: `load_card_db` is an ordinary undecorated function; every call reads and JSON-decodes the file. **No lru_cache.** New candidate paths and changing primary/screen/confirm bots mean new MatchSpecs and new DB reads in each worker receiving those jobs. Reused worker processes do not preserve one global original DB. Even under fork, the parent's local db is not used by `_setup`.
6. `cards/decklist.py:58-73`: deck counts/codes read on each MatchSpec miss; CardDefs come from the newly loaded database, not the decklist's human-readable card-name suffix. Opponent lists are reread on those misses too, but tracked engine decklists did not change in the refresh commit.
7. `sim/optimize.py:215-222`: separate parent cache stores incumbent gauntlet batch results by incumbent path/bot/seed/look; it avoids recomputing those aggregates across candidates. It does not freeze the workers' DB on misses. Confirmation uses seed+7 and a different bot. Screen uses seed+501 for round 1; baseline uses seed+1001. Saved screen header confirms 732; primary 231 provenance is argv, because JSONL omits it.
8. Prior matrix draw impacts are loaded once at `optimize.py:285`, but screening branch uses `all_swaps`, not `propose`/prior ranking. No live calibration reload occurs in worker calls.

The executable proof AST-extracts the exact original loader and `_setup`, substituting read-counting value-only stubs rather than importing project modules. Two loader calls produce two reads/distinct DB objects. Three `_setup` calls (same spec twice, then new variant) produce two DB reads and four deck loads. This verifies code semantics, not historical per-worker execution.

## Compact card-data reconciliation

Original versus refreshed raw data: **21 added codes, zero removed; 22 existing cards have raw changes; seven existing CardDefs change.** Raw changed-field counts: printings 22, image 7, name 6, flavor 5, workSuitability 1, effect 1, color 1. See JSON for exact values rather than a huge git diff.

- BP02-004 Chillet Ignis: subtitle Spark-Clad → Ember-Clad; effect wording changes; work `(kindling, farming)` → `(kindling, harvesting)`.
- BP02-099: green → colorless.
- SS01-001 through SS01-005: subtitles change.

Changed-code occurrence scan of saved candidate/best/round0 lists plus ten current retained opponent lists: BP02-004 and SS01-001/002/004 occur in 14 screen variants each; SS01-005 in three; BP02-099 and SS01-003 in none. These occurrences are confined to screening candidates, not the final six tested variants, round0/best or retained opponents. Added codes were not available to the parent's original candidate generator. This substantially narrows the exposure, but the screening stage selects the final six, so final-deck equivalence alone does not certify original-input selection.

The engine does consume names and some work fields; current static search finds `cards/bp01_blue_green.py:268` reading farming on an assigned structure. BP02-004 is a Pal, so that particular structure-only use is NOT proof its changed work field affects games. No complete noninterference proof was attempted. Do not overstate cosmetic changes as demonstrated numerical effects, or claim no effects without proving all relevant code paths.

## Timing and evidentiary limits

- Refresh commit recorded 2026-10-12 **15:09:10 UTC**. This is a commit time, not a timestamp for first overwrite of cards.json.
- Screen candidate file mtimes span **14:09:32.881344–23:23:01.799891 UTC**; 110 before refresh commit and 845 at/after it. Candidate files are written immediately before their gauntlet calls in the source. All 14 BP02-004 candidates have mtimes around 19:33–19:41 UTC, well after the commit.
- This establishes a credible mid-search new-MatchSpec reload exposure, not exact per-worker read timing. Mtimes and commit metadata are not immutable process telemetry. No worker input hashes, DB snapshots, worker PID/read logs or cached object dumps were persisted.
- Screening, sequential and confirmation aggregate results cannot be recalculated from saved raw games: those calls do not persist raw game records. No ability to authenticate every number independently is asserted.
- Original-head artifact validation remains useful and should be performed by parent, but is a consistency gate rather than historical input attestation. Existing validator also requires stdout's absolute run path under its REPO root; merely overriding REPO to a detached worktree without a documented path strategy may fail that gate. Preserve raw stdout unchanged; do not disguise rebased paths as original evidence.
- Live shared checkout and experiments.md were already mutable. Audit files hash observed artifacts; later parent changes can make repeat-run manifests differ. The script uses immutable Git blobs for the two input revisions but live files for artifact inspection.

## Outputs and execution

Run `/home/gator/palworld-run-artifacts/J22-recovery-audit/reconcile.py` directly. It is executable, uses standard library only, no simulation/project imports, only read-only Git commands, and writes exclusively to this audit directory.

- `reconciliation.json`: revision/source comparisons, argv/exit record, old/new weights, timing, six experiment rows and limitations.
- `cards-semantic-diff.json`: compact per-code raw deltas and exact AST-converted CardDef deltas.
- `cache-proof.json`: instrumented exact-source cache/read results.
- `changed-card-deck-occurrences.json`: relevant saved list paths and mtimes.
- `artifact-manifest.json`: SHA256/size/mtime of saved run files and execution evidence.
- `cards_db.py.numbered.txt`, `cards_decklist.py.numbered.txt`, `sim_runner.py.numbered.txt`, `sim_gauntlet.py.numbered.txt`, `sim_optimize.py.numbered.txt`: original revision evidence.

Initial script execution exposed JSON enum serialization in reporting; fixed inside the audit script and rerun successfully. No repo source, data, results, Git state, other profile or external messages were written by this audit.
