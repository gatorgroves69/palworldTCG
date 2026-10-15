# J26 execution notes

Started 2026-10-15T15:15:28Z on frozen source cb14dde81b161ac0752012bcf5b5c59e6114cb48. Bobby explicitly authorized J26 as written in the latest handoff. Only J26 is running.

Command:
```
python3 -m sim optimize --deck results/runs/cattiva_dragons_v3.txt --rounds 2 --max-tries 6 --seed 261 --screen-games 400 --screen-outs 14 --sets BP01,TD01,TD02 --bot human --confirm-bot human1 --run-dir results/runs/J26-optimize/run
```

## Initial checkpoint — 2026-10-15 15:17 UTC

Status: running; no completed screened swap or final result yet. Initial round0 list, exact start timestamp and current stdout are included. The run checkout stays frozen; stable artifacts are copied to a separate publication checkout. JSONL snapshots retain complete valid lines only. Publish append-only main checkpoints every 15 minutes and completed results as available, pulling before every push, with no rebase or force-push. No engine, bot, sim, card, data or test edits.

## Screening provenance — 2026-10-15 15:45 UTC

The exact authorized command uses `human` for primary sequential testing and `human1` for confirmation. Its cheap screening pass uses the optimizer's existing `screen_bot = "heuristic"` default, as recorded in every screened-swap JSONL row; no screening-bot override or code change was made. Screening results remain preliminary, not accepted swaps or final deck recommendations. Completed scores are checkpointed in `run/screen/round1_scores.jsonl`; candidate lists alone do not imply a completed score.

## Interrupted attempt checkpoint — 2026-10-15 17:21 UTC

The original execution session was lost around 17:20 UTC. No final exit/end artifact exists, so this is not a completed optimizer run. Its original start/stdout evidence is preserved unchanged. All 294 retained round-1 screening rows are complete, valid and unique (400 requested games, heuristic, seed 762). Frozen protected-file SHA-256 values and the v3 input were verified against the execution baseline before resume. The exact authorized command can resume from these 294 scores; no final swap verdict exists yet.

## Resumed attempt — 2026-10-15 17:30 UTC

The exact command above resumed at 2026-10-15T17:22:30Z on the same frozen execution checkout. Separate evidence: `dot-resume-20261015-1722.start` and `.log`; original attempt evidence remains intact. At this checkpoint 294 complete screening rows remain saved, while the resumed attempt recomputes its baseline before skipping completed screening swaps. Running, with no final verdict or exit/end artifact yet.

## Second resumed attempt — 2026-10-15 18:00 UTC

The 17:22 execution session was lost by 17:51 UTC without a final exit/end artifact. All 323 completed screening rows were already published and survived locally. The exact authorized command resumed again at 2026-10-15T17:51:40Z on the frozen checkout. Separate evidence: `dot-resume-20261015-1751.start` and `.log`; all earlier attempt logs are retained. At this checkpoint the new attempt is recomputing its baseline with the 323 completed scores preserved. No final verdict is available.

## Third resumed attempt — 2026-10-15 19:30 UTC

The 17:51 execution session was lost by 19:20 UTC without a final exit/end artifact. All 532 completed screening rows survived locally and are included in this checkpoint. The exact authorized command resumed at 2026-10-15T19:21:00Z on the frozen checkout. Separate evidence: `dot-resume-20261015-1921.start` and `.log`; prior attempt logs remain intact. At this checkpoint baseline recomputation is in progress with 532 completed scores preserved; no final verdict exists.

## Round 1 screening complete — 2026-10-15 21:15 UTC

All 801 round-1 screening scores are complete, valid and unique; `run/screen_round1.md` contains all 801 ranks. Screening used heuristic, 400 requested games per candidate, seed 762. The first full sequential candidate list is present (`run/round1_TD01-023_to_TD01-013.txt`, Lamball to Jolthog Cryst), but no completed sequential result or new experiment row is available yet. Rankings are noisy screening leads, not confirmed improvements or adoption decisions. Primary/confirmation remain human/human1 under the exact authorized command.

## Complete — 2026-10-15 23:56 UTC

The final resumed attempt exited 0 at 2026-10-15T23:56:17Z. All 801 unique screening scores and ranks, six sequential verdicts, and final start/log/exit/end evidence are preserved. No swap passed the primary human sequential test; no human1 confirmation was triggered. The optimizer stopped after round 1 as designed. best.txt has exactly the original v3 card counts in each section, with canonical ordering (not byte-identical to the input). No deck adoption is implied.

| Swap | Difference ± SE (percentage points) | z | Games/list | Verdict |
|---|---:|---:|---:|---|
| -2 Lamball – My First Pal / +2 Jolthog Cryst – Stoic Yet Innocent | +0.2 ± 1.0 | 0.24 | 4045 | not better (inconclusive) |
| -2 Blazehowl – Hellflame Defender / +2 Reptyro – Ore Gorger | -0.0 ± 1.0 | -0.03 | 4045 | not better (futility) |
| -2 Cattiva – My First Pal / +2 Jolthog Cryst – Stoic Yet Innocent | +0.7 ± 1.0 | 0.73 | 4045 | not better (inconclusive) |
| -2 Fuack – Manic Wave Ripper / +2 Cryolinx – Arctic Ordeal | -0.2 ± 1.6 | -0.11 | 1618 | not better (futility) |
| -2 Pump-Action Shotgun / +2 Reptyro – Ore Gorger | -1.0 ± 1.6 | -0.62 | 1618 | not better (futility) |
| -2 Axel's Strategy / +2 Single-Shot Rifle | +0.5 ± 1.0 | 0.50 | 4045 | not better (inconclusive) |

Validated all 1260 protected-file SHA-256 hashes unchanged against the frozen execution baseline, and the original v3 input byte-for-byte against frozen HEAD. Screening used heuristic, 400 requested games per swap, seed 762; primary/confirmation configuration was human/human1. Earlier running/interruption checkpoints above are historical. J26 is complete and stopped; no further job started.
