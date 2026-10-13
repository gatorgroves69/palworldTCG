# J22 recovery — original attempt preserved, frozen retry authorized

Status: original attempt completed computation but is NOT certified as a consistent-input run. Bobby asked to ensure all approved work finishes and then said "try again". Retry J22 at the original batch HEAD in an isolated worktree, then run only the remaining J20.11 matrix. No engine edits or extra experiments.

Original command: `python3 -m sim optimize --deck results/runs/cattiva_dragons.txt --rounds 1 --max-tries 6 --seed 231 --screen-games 400 --screen-outs 14`

Original execution HEAD: `034a132b08d16023f6fe63a5a2b7ce0be06b5866`
Start UTC: 2026-10-12T13:52:54.748771+00:00
End UTC: 2026-10-13T02:24:58.135229+00:00
Child exit: 0. Controller failed on post-run input-diff assertion.

Original attempt screened 955 swaps and tested six finalists; none passed. Best equals round0. Exact saved stdout/rows/deck counts/allocations/old field weights and original-card deck validation passed in `/home/gator/palworld-run-artifacts/J22-recovery/verify_j22.py`. All ten earlier J20 mirrors and twelve J21 lines were separately reverified, including remote ancestry.

However the October12 weekly refresh changed cards.json during execution. Worker DB is cached per MatchSpec, not globally; new candidates can reload changed CardDefs. Changed definitions occur in screening candidates, so final candidate selection cannot be certified from aggregate artifacts alone. No numerical contamination has been demonstrated, but no full noninterference proof exists either. Do not treat a clean child exit or structural gate as strict experiment completion.

Original attempt's best and screening report are preserved in `attempt1/`; six experiment rows remain in results/experiments.md. Full original run: `/home/gator/palworldTCG/results/opt/20261012-135254/`. Input audit: `/home/gator/palworld-run-artifacts/J22-recovery-audit/REPORT.md`. This preserves real output, not a fabricated or silently replaced result.

Frozen retry and final matrix worktree: `/home/gator/palworld-run-artifacts/J22-recovery/matrix-worktree`, detached at original HEAD above. New runner/state/artifacts: `/home/gator/palworld-run-artifacts/J22-recovery/`. Final verdict will be added only after actual retry, artifact verification, commit and verified push. Shared main and the weekly refresh stay intact.
