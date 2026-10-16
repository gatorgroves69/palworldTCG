# J28 BP02 preview screen

Status: RUNNING. Started UTC: 2026-10-16T08:03:53.795857+00:00. Latest checkpoint UTC: 2026-10-16T11:19:52.986186+00:00.

Frozen execution HEAD: `7fd05267958bf766d5d29c7b1d2ac0ce27d3c72a`; verified descendant of 0795d7a.

Bobby directly approved this exact single command:
```
python3 -m sim optimize --deck results/runs/cattiva_dragons_v3.txt --rounds 1 --max-tries 6 --seed 281 --screen-games 400 --screen-outs 14 --sets BP02 --bot human --confirm-bot human1 --run-dir results/runs/J28-bp02/run
```

Completed screening records: 166; sequential verdicts: 3.
Original command/run-dir preserved; screening checkpoints support resume. No engine, bot, card, data, deck-adoption or other-job changes. BP02 preview texts remain provisional; this is not a completed >=10 BP02 tournament deck.

Publication uses a separate checkout so remote changes cannot affect live simulation inputs. Checkpoint every 15 minutes and at completion. Exact stdout: command.log; execution/input hashes: execution.json; new experiment rows: sequential-results.jsonl.

- -2 Axel's Strategy / +2 Eikthyrdeer – Warden of the Woods: +0.1 ± 1.0 (4045 games) -> not better (inconclusive)
- -2 Fuack – Manic Wave Ripper / +2 Foxcicle – Aurora Hymn: -1.1 ± 1.6 (1618 games) -> not better (futility)
- -2 Fuack – Manic Wave Ripper / +2 Foxparks – Breathing Practice: -1.0 ± 1.6 (1618 games) -> not better (futility)
