# J24 Stone Pit comparisons

Baseline: 1747/2000 wins (87.35%;95% CI85.82–88.74%),seed251,heuristic2@human@seq. Going first882/991 (89.00%),second865/1009 (85.73%). Execution code2c7ba53,verified2000JSONL records and summary consistency.

A_rifle4: 1716/2000 wins (85.80%; 95% CI 84.20–87.26%), seed 251, heuristic2@human@seq. Going first 858/991 (86.58%), second 858/1009 (85.03%). Average 16.93 turns. Execution code 2c7ba53; verified all 2000 unique JSONL records, seeds, outcome counts, first/second splits, end reasons and average turns against summary.json.

Line 2 command: `python3 -m sim run --deck results/runs/J24-A_rifle4.txt --opp results/runs/palify_consensus/lamball-stone-pit-pr.txt --games 2000 --seed 251 --bot heuristic2@human@seq --no-report --logs 0 --out results/runs/J24-stonepit/A_rifle4`. Completed retry started 2026-10-14T04:15:53Z, ended 2026-10-14T04:42:26Z, exit 0; raw stdout and timing/exit markers are in `logs/A_rifle4.retry1.*`. The earlier attempt started 2026-10-14T03:51:55Z and was interrupted after its last logged 600/2000 progress; `logs/A_rifle4.txt` and `.start` preserve that incomplete attempt. No completion or exit status is claimed for the earlier attempt. Only the completed retry contributes results.

B_handgun: 1751/2000 wins (87.55%; 95% CI 86.03–88.93%), seed 251, heuristic2@human@seq. Going first 868/991 (87.59%), second 883/1009 (87.51%). Average 16.83 turns. Execution code 2c7ba53; verified all 2000 unique JSONL records, seeds, outcome counts, first/second splits, end reasons and average turns against summary.json.

Line 3 command: `python3 -m sim run --deck results/runs/J24-B_handgun.txt --opp results/runs/palify_consensus/lamball-stone-pit-pr.txt --games 2000 --seed 251 --bot heuristic2@human@seq --no-report --logs 0 --out results/runs/J24-stonepit/B_handgun`. Started 2026-10-14T05:05:52Z, ended 2026-10-14T05:34:53Z, exit 0; raw stdout and timing/exit markers are in `logs/B_handgun.*`.
