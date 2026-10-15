# J26 execution notes

Started 2026-10-15T15:15:28Z on frozen source cb14dde81b161ac0752012bcf5b5c59e6114cb48. Bobby explicitly authorized J26 as written in the latest handoff. Only J26 is running.

Command:
```
python3 -m sim optimize --deck results/runs/cattiva_dragons_v3.txt --rounds 2 --max-tries 6 --seed 261 --screen-games 400 --screen-outs 14 --sets BP01,TD01,TD02 --bot human --confirm-bot human1 --run-dir results/runs/J26-optimize/run
```

## Initial checkpoint — 2026-10-15 15:17 UTC

Status: running; no completed screened swap or final result yet. Initial round0 list, exact start timestamp and current stdout are included. The run checkout stays frozen; stable artifacts are copied to a separate publication checkout. JSONL snapshots retain complete valid lines only. Publish append-only main checkpoints every 15 minutes and completed results as available, pulling before every push, with no rebase or force-push. No engine, bot, sim, card, data or test edits.
