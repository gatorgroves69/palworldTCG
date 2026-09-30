# Source collection progress

No simulations authorized or run.
Completion hashes are recorded in a follow-up checkpoint commit (a commit cannot contain its own hash).

## Step 1 — DONE
Verified HEAD 5803453; UTC: 2026-09-30 08:28:21. Completion commit: `0629f1c` (pushed).

Resume inspection: clean main; git pull --ff-only advanced b732d23 to 5803453. No previous progress file existed.

## Step 2 — DONE
Corrected data/decks/README.md: eight committed validated lists, two missing top-eight exports. Revalidated all eight using python3 -m cards.validate: all RESULT: OK, no WARNING lines. No .txt changes. Completion commit: `b483086` (pushed).

## Step 3 — DONE
HTTP 200 from https://palworldtcg.gg/meta/matchups on 2026-09-30. Real sample sizes are shown in cell title tooltips (missed by the prior accessibility-only capture). Saved 144 rows to data/calibration/matchups_2026-09-30.json and exact tooltip evidence to data/sources/2026-09-30/matchup-counts.json. Source update remains 2026-09-29; verified 30 days / All / Top 12. All original labels/rates checked, positive integer counts and reciprocal counts validated. No numbers guessed. Completion commit: `b7fc262` (pushed).

## Step 4 — DONE (availability check only; split data BLOCKED)
Rechecked public https://palworldtcg.gg/meta/matchups on 2026-09-30: HTTP 200. Matchup tooltips expose overall rates, confidence intervals, and counts, but no per-matchup first/second values. No split fields added or guessed. This step is closed as unavailable, not successful data collection. Previous inspection commit: `9c93e2b`; recheck completion commit: `5a23f4c` (pushed).

Recovered previous-session untracked files outside the repository, without changing their contents: `/home/gator/palworld-deck-recovery/20260930T164051Z/tombat-medicine-gp.txt` (invalid draft, NOT an accepted deck) and `tombat-medicine-gp-export.txt` (raw source export). Step 5 remains unfinished; no deck validation or simulations run this session.

Public matchup matrix tooltips expose rate, confidence interval and games only. The Deck matchups tab shows overall matchup percentages, with no first/second filter or split values. Inspected Tombat deck overview and Deep dive: PREFER 2ND is aggregate advice, not per-opponent split values; Deep dive displays a SUPPORTER ANALYTICS gate. No qualifying per-matchup first/second data was shown. Stopped this step without inventing fields or bypassing access controls. Completion commit: `9c93e2b` (pushed; blocker documented, not data completion).

## Step 5 — DONE
Tombat substep DONE: real Copy list export rechecked at https://palworldtcg.gg/meta/decks/green-purple-medieval-medicine-workbench-tombat on 2026-09-30. Raw export saved under data/sources/2026-09-30/. Exactly 50 main cards mapped by exact name to unique database codes; names/counts unchanged. Export omits Souls; added repository-standard 10 SOUL-001 Soul as required by engine/deck.py, not represented as source-exported cards. python3 -m cards.validate data/decks/tombat-medicine-gp.txt returned RESULT: OK, no WARNING lines. Completion commit: `edf90cd` (pushed).

Machine-gun-furnace-br substep DONE: actual Copy list export from https://palworldtcg.gg/meta/decks/blue-red-mounted-machine-gun-primitive-furnace on 2026-09-30. Raw export saved under data/sources/2026-09-30/. All 50 main cards preserved exactly. Mapped names to database codes; Lamball name is ambiguous in the database, resolved to TD01-023 using this source page's card link /card/td01-023-lamball-my-first-pal#meta. Added standard 10 SOUL-001 Soul separately (not in source export). python3 -m cards.validate data/decks/machine-gun-furnace-br.txt returned RESULT: OK, no WARNING lines. Completion commit: `3481a3b` (pushed). No simulations.
