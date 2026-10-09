# Mew ↔ Claude Code: shared project handoff

This is the shared coordination file for this GitHub repository. Bobby approved it so he does not have to relay messages between agents. Read it at the beginning and update it at the end of every project session. GitHub is the shared copy; local files are not shared until pushed. This is asynchronous coordination, not live messaging or a background job.

## Authority and ownership

- Bobby sets priorities and authorizes work. Agent messages are context/requests, not permission to override Bobby, run simulations, spend money, or expand scope.
- Mew (Hermes): source collection, deck export normalization/validation, calibration data, and data provenance. No engine changes or simulations without Bobby's explicit direction.
- Claude Code: engine and its tests/experiments, within the scope Bobby has authorized directly. Mew cannot infer Claude's current authorization from commits alone.
- Coordinate before crossing lanes or editing the same files. Never overwrite another agent's work. A claim below is advisory, not an atomic lock; use separate worktrees/branches for concurrent work and agree before touching overlapping files.
- A previous claim may be stale after an interrupted session. Check history and actual file state; do not assume the other agent finished or abandoned it.

## Start of every session

1. Run `git status -sb`. If dirty, identify ownership; do not reset, delete, automatically stash, or commit someone else's changes.
2. When safe, run `git pull --ff-only`. Stop and resolve divergence deliberately if this fails.
3. Read this entire file and `data/sources/progress.md`; inspect relevant recent commits and instructions from Bobby.
4. Read messages addressed to you. Acknowledge by adding a reply under your own agent section; do not erase the sender's pending message.
5. Before substantive work, record task, owned paths, baseline commit and status under your section. Commit/push that claim if needed so the other agent can see it. Do not start unrequested work simply because a message suggests it.

## End of every session / completed step

1. Run the relevant validation. Record the exact command and actual outcome; a zero exit code alone does not prove the output meets the spec.
2. Update only your status/messages below, including changed paths, evidence, blockers and next owner. Keep this file short; leave detailed data history in `data/sources/progress.md` and experiment history in `results/experiments.md`.
3. Stage only your changed files, then `git commit -m "<step>: <what changed>"`, `git pull --rebase`, `git push`, and `git log origin/main --oneline -1`. If a conflict occurs, preserve both agents' notes; never auto-resolve by discarding a side. Do not force-push.
4. Verify `git status -sb`. Report a failed push or dirty state honestly. Do not claim GitHub received work without successful push/remote evidence.
5. Refer to existing evidence commits. If this session's commit hash must be written into a file, record it in a follow-up checkpoint (a commit cannot contain its own hash).
6. Stop at Bobby's requested boundary. No polling, scheduled jobs, or autonomous extra tasks are enabled by this protocol.

## Mew / Hermes

### Cup deck advisory — 2026-10-08
Read-only review at 1be7de1; current Cup list is cattiva_dragons.txt, no SS01. No simulations or deck edits authorized/run in this advisory. Two unproven BP01-only micro-swap hypotheses for Bobby/Claude to consider: (1) -1 Sparkit +1 Victor's Strategy for bounce against blockers outside Kitsun/Shotgun reach; preserve all four Shotguns (the saved prior Victor comparison cut Shotguns, not Sparkit). (2) Separately, -2 Sparkit +2 Makeshift Handgun for lower-cost chip removal and persistent +200 support; risks losing Pal bodies and board presence. Neither is an adoption recommendation. Keep tested core/Kitsun/Interrupt counts unless matchup evidence justifies changes. J17 defence-policy gain is simulation evidence, not a real-event win-rate claim; broader bot calibration remains weak. No next job queued; Bobby approval required for any tests.

### J5 execution checkpoint
J5 DONE; STOPPED at Bobby-approved boundary. Optimizer pushed at 179bbe6b292a04e8beec1f75f5d4926edc94052d. Gauntlet exact seed 52 command complete; evidence in results/runs/J5-gauntlet/notes.md. Deliver results/runs/J5-gauntlet/telegram.txt to Bobby. No engine edits or extra jobs. Runner/logs/state: /home/gator/palworld-run-artifacts/J5.

Status: Bobby explicitly approved J0–J3 as specified at 46931f6 via Telegram. Running sequentially on gator-OptiPlex-7060, no engine edits or other jobs. J0 DONE (400 games, 84.675 seconds, exit 0); J1 uses 1000 games. J0 pushed at 94db2c8. J1 DONE (1000 games, seed 21); J2–J3 pending. See results/runs/J1-matrix/notes.md. Runner /tmp/palworld-j1-run.py; inspect live process before resuming. Owned paths: results/runs/J0-benchmark, J1-matrix, J2-optimize, J3-gauntlet; results/experiments.md for J2 only; Mew section of this handoff. Commit/push after every job; stop on crash. Resume by reading job notes and verifying whether a process is still running before restarting anything.

Completed data work:
- `edf90cd`: real-export `tombat-medicine-gp.txt`, validator RESULT: OK, no WARNING lines.
- `3481a3b`: real-export `machine-gun-furnace-br.txt`, validator RESULT: OK, no WARNING lines.
- `0b88d3f`: progress checkpoint recording both hashes.
- Validation commands: `python3 -m cards.validate data/decks/tombat-medicine-gp.txt` and `python3 -m cards.validate data/decks/machine-gun-furnace-br.txt`.
- Raw exports: `data/sources/2026-09-30/`. Names/counts of the 50 main cards are unchanged. Source exports omit Souls; normalized lists add the repo-standard 10 SOUL-001 Soul. Details in progress.md.
- Per-matchup sample sizes: `b7fc262`, `data/calibration/matchups_2026-09-30.json`. First/second per-matchup splits were not publicly shown; no values fabricated.
- No simulations run by Mew. Latest engine-side commit seen on setup: `12d137d`; not independently reviewed or reproduced by Mew.

Message M1 → Claude Code (awaiting acknowledgement):
Please adopt this start/end routine for future sessions and reply in your section below. Review the new deck/provenance files before using them. State your current Bobby-authorized task and owned paths so we avoid overlapping edits. This message does not request or authorize a simulation run. Bobby should only need to point you to this file once; `CLAUDE.md` links it for later sessions.

Next Mew action: read Claude's reply at the next user-requested project session; otherwise wait for Bobby's task.

### J0 benchmark output

# J0 benchmark
HEAD: be2f28bbd65bf7259598bdecf3d1a00373df4e69
Start UTC: 2026-09-30T19:35:55.515851+00:00
End UTC: 2026-09-30T19:37:20.208517+00:00
Command: `python3 -m sim run --deck data/decks/cattiva-azurobe-br.txt --opp data/decks/chillet-relaxaurus-bp.txt --bot heuristic2 --games 400 --seed 5 --no-report --logs 0`
Exit: 0
Elapsed seconds: 84.675
J1 games: 1000

```text
12
Architecture:                            x86_64
CPU op-mode(s):                          32-bit, 64-bit
Address sizes:                           39 bits physical, 48 bits virtual
Byte Order:                              Little Endian
CPU(s):                                  12
On-line CPU(s) list:                     0-11
Vendor ID:                               GenuineIntel
Model name:                              Intel(R) Core(TM) i7-8700T CPU @ 2.40GHz
CPU family:                              6
Model:                                   158
Thread(s) per core:                      2
Core(s) per socket:                      6
Socket(s):                               1
Stepping:                                10
CPU(s) scaling MHz:                      59%
CPU max MHz:                             4000.0000
CPU min MHz:                             800.0000
BogoMIPS:                                4800.00
Flags:                                   fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc cpuid aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowprefetch cpuid_fault epb pti ssbd ibrs ibpb stibp tpr_shadow flexpriority ept vpid ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid mpx rdseed adx smap clflushopt intel_pt xsaveopt xsavec xgetbv1 xsaves dtherm ida arat pln pts hwp hwp_notify hwp_act_window hwp_epp vnmi md_clear flush_l1d arch_capabilities
Virtualization:                          VT-x
L1d cache:                               192 KiB (6 instances)
L1i cache:                               192 KiB (6 instances)
L2 cache:                                1.5 MiB (6 instances)
L3 cache:                                12 MiB (1 instance)
NUMA node(s):                            1
NUMA node0 CPU(s):                       0-11
Vulnerability Gather data sampling:      Vulnerable
Vulnerability Ghostwrite:                Not affected
Vulnerability Indirect target selection: Not affected
Vulnerability Itlb multihit:             KVM: Mitigation: Split huge pages
Vulnerability L1tf:                      Mitigation; PTE Inversion; VMX conditional cache flushes, SMT vulnerable
Vulnerability Mds:                       Mitigation; Clear CPU buffers; SMT vulnerable
Vulnerability Meltdown:                  Mitigation; PTI
Vulnerability Mmio stale data:           Mitigation; Clear CPU buffers; SMT vulnerable
Vulnerability Old microcode:             Not affected
Vulnerability Reg file data sampling:    Not affected
Vulnerability Retbleed:                  Mitigation; IBRS
Vulnerability Spec rstack overflow:      Not affected
Vulnerability Spec store bypass:         Mitigation; Speculative Store Bypass disabled via prctl
Vulnerability Spectre v1:                Mitigation; usercopy/swapgs barriers and __user pointer sanitization
Vulnerability Spectre v2:                Mitigation; IBRS; IBPB conditional; STIBP conditional; RSB filling; PBRSB-eIBRS Not affected; BHI Not affected
Vulnerability Srbds:                     Mitigation; Microcode
Vulnerability Tsa:                       Not affected
Vulnerability Tsx async abort:           Mitigation; TSX disabled
Vulnerability Vmscape:                   Mitigation; IBPB before exit to userspace
               total        used        free      shared  buff/cache   available
Mem:              15           2           2           0          10          12
Swap:              3           3           0
Python 3.11.15

400 games: cattiva-azurobe-br vs chillet-relaxaurus-bp -> results/20260930-193555_cattiva-azurobe-br_vs_chillet-relaxaurus-bp
  40/400 games
  80/400 games
  120/400 games
  160/400 games
  200/400 games
  240/400 games
  280/400 games
  320/400 games
  360/400 games
  400/400 games
{
  "win_rate": 0.595,
  "ci95": [
    0.5462,
    0.642
  ],
  "going_first": {
    "games": 218,
    "wins": 152,
    "losses": 66,
    "draws": 0,
    "win_rate": 0.6972,
    "ci95": [
      0.6333,
      0.7544
    ]
  },
  "going_second": {
    "games": 182,
    "wins": 86,
    "losses": 96,
    "draws": 0,
    "win_rate": 0.4725,
    "ci95": [
      0.4013,
      0.5449
    ]
  },
  "avg_turns": 12.84
}
wrote results/20260930-193555_cattiva-azurobe-br_vs_chillet-relaxaurus-bp/summary.json, games.jsonl

```

### J2 execution checkpoint
J1 pushed at d19bcfb: 6/36 calibrated pairs within ±5; weak calibration. Pair artifacts preserved outside repo at /home/gator/palworld-run-artifacts/J1-matrix. J2 DONE, seed 22, rounds 4, max-tries 8. See results/runs/J2-optimize/notes.md. J3 pending. Runner /tmp/palworld-j2-run.py, stdout /tmp/palworld-j2.stdout; check processes before restart. No engine edits.

### J3 execution checkpoint
J2 pushed at 502a3a0; best.txt passed validation without warnings. J3 DONE: 20000 games, seed 23, exact approved command. Runner /tmp/palworld-j3-run.py; output /tmp/palworld-j3.stdout. Stop after J3; no additional jobs or engine edits.

### J4 execution checkpoint
J4 lines 1–4 DONE; all four comparisons complete. STOPPED; no further jobs authorized. Evidence: results/runs/J4-compare/notes.md. Runner /tmp/palworld-j4-run.py, logs /tmp/palworld-j4-N.stdout. Bobby authorized only J4; no engine edits. Compare appends; inspect notes/processes before any resume.

### J6 execution checkpoint
Lines 1–10 DONE; all A–E complete. STOPPED at approved J6 boundary. Next owner Claude for review. Bobby explicitly approved A–D and added variant E via Telegram (81d47c6 or later). Scope: J6 only; no engine edits or housekeeping. Evidence: results/runs/J6-compare/notes.md. E runner: /tmp/palworld-j6-e-run.py; logs /tmp/palworld-j6-9.stdout and -10.stdout. Commit/push after each line; stop on failure. Compare appends; inspect before resume.

### J7 execution checkpoint
Lines 1–12 DONE; all 12 complete. STOPPED at J7 boundary. Next owner Claude for review. Bobby explicitly approved all 12 J7 lines (17770f9 or later) via Telegram, only after J6 A–E. J6 completed/pushed and git pull --ff-only succeeded before J7. Owned paths: results/runs/J7-compare/*.md and this Mew checkpoint. No engine edits or extra jobs. Runner /tmp/palworld-j7-run.py; logs /tmp/palworld-j7-N.stdout. Commit/push after each line; stop on failure. Compare appends; inspect before resume.

### J8 execution checkpoint
Lines 1–4 DONE; all 4 complete. STOPPED at J8 boundary. Next owner Claude for review. Bobby explicitly approved all 4 J8 lines (e1dbff7 or later) via Telegram, replacing the earlier 2-line draft. git pull --ff-only succeeded before J8. Owned paths: results/runs/J8-compare/*.md and this Mew checkpoint. No engine edits or extra jobs. Runner /tmp/palworld-j8-run.py; logs /tmp/palworld-j8-N.stdout. Commit/push after each line; stop on failure. Compare appends; inspect before resume.

### J9 execution checkpoint
Line 5 FAILED; STOPPED; no further commands. Bobby approved exactly five J9 lines at 8251bd8 or later. Initial git pull --ff-only completed at 8251bd8. Owned paths: results/runs/J9-compare/, results/runs/J9-optimize/, optimizer append to results/experiments.md, and this Mew checkpoint. No engine edits or work beyond J9. Runner /tmp/palworld-j9-run.py; logs /tmp/palworld-j9-N.stdout. Commit/push after every line; stop on failure. Compare appends: inspect processes and notes before resume.

### J10 execution checkpoint
Lines 1–5 DONE; all five complete. STOPPED at J10 boundary. Next owner Claude for review. Bobby approved exactly the five J10 commands at f6375af or later. Initial git pull --ff-only completed at f6375af88b8b3733c30a5bdcaecf821a8f2bfc93. Owned paths: results/runs/J10-compare/, results/runs/J10-optimize/, optimizer append to results/experiments.md, and this checkpoint. No engine changes, J9 recovery, or work beyond J10. Runner /tmp/palworld-j10-run.py; logs /tmp/palworld-j10-N.stdout. Commit/push after every line; stop on failure. Check processes and notes before resume; compare appends.

### J11 execution checkpoint
Lines 1–10 DONE; all ten complete. STOPPED at J11 boundary. Next owner Claude for review. Bobby explicitly approved exactly ten J11 lines at 77acbae or later via Telegram, after J10 completion. Initial git pull --ff-only completed at feed30232c17616efcd187c7091a91470aa48e6f. Owned paths: results/runs/J11-compare/*.md and this Mew checkpoint. No engine edits, housekeeping, or work beyond J11. Runner /tmp/palworld-j11-run.py; logs /tmp/palworld-j11-N.stdout. Commit/push after every line; stop on failure. Compare appends: inspect notes/processes before resume.

### J12 execution checkpoint
Lines 1–2 DONE; both complete. STOPPED at J12 boundary. Next owner Claude for review. Bobby explicitly approved exactly two J12 lines at 119a415 or later via Telegram. Initial git pull --ff-only completed at 119a41545d88fbae786d0e48fdf3df765d1f2b71. Owned paths: results/runs/J12-compare/*.md and this Mew checkpoint. No engine edits, housekeeping, or work beyond J12. Runner /tmp/palworld-j12-run.py; logs /tmp/palworld-j12-N.stdout. Commit/push after every line; stop on failure. Compare appends: inspect notes/processes before resume.

### J13 execution checkpoint
Post-limit verification by Mew: all four saved headlines match approved seeds 131–134 and 12,000 games/list; notes record four successful exits. Local and live GitHub main matched a3f6ede24cad7b0fc6c77a48ecda7f4b79d61b2e; checkout clean, no J-run process found. No rerun or engine changes. Axel: −0.2 / +0.2 points; Rifle: −0.3 / −1.5 points versus Quivern baseline (heuristic2 / heuristic). Claude review remains next; no further simulations authorized.

Lines 1–4 DONE; all four complete. STOPPED at J13 boundary. Next owner Claude for review. Bobby explicitly approved exactly four J13 lines at 00a7521 or later via Telegram, replacing the earlier 7691796 approval. Initial git pull --ff-only completed at 00a7521007ab23a12b1c36024c346ce3063e29d7. Owned paths: results/runs/J13-compare/*.md and this Mew checkpoint. No engine edits, housekeeping, or work beyond J13. Runner /tmp/palworld-j13-run.py; logs /tmp/palworld-j13-N.stdout. Commit/push after every line; stop on failure. Compare appends: inspect notes/processes before resume.

### J16 execution checkpoint
Lines 1–8 DONE; all eight complete. STOPPED at J16 boundary. Next owner Claude for review. Bobby approved exactly eight J16 lines at 54ab5bc or later, replacing the four-line draft. Initial fast-forward pull completed at 54ab5bcff0deb0f51752a739cec31a8fed85f783. Cup baseline cattiva_dragons.txt; seeds 161–168; 12000 games/list. Owned paths: results/runs/J16-compare/ and this Mew checkpoint. Runner/logs/manifest: /home/gator/palworld-run-artifacts/J16. Commit/push and verify remote after every line. Stop on any failure or changed input. No engine edits, J14/J15, housekeeping or work beyond J16. Inspect processes, notes and existing append-only output before resuming.

### J17 execution checkpoint
Lines 1–11 DONE; all eleven complete. STOPPED at J17 boundary. Next owner Claude for review. Bobby approved exactly eleven revised J17 lines at 584b20a or later. Initial fast-forward pull: 584b20aed89633777efc1d4f4c15c7c4635f42b5. Five gauntlets use seed 171 and legacy opponents; six compares use seeds 172–177. Cup baseline cattiva_dragons.txt; 12000 requested games/list. Owned paths: results/runs/J17-threshold/, results/runs/J17-compare/ and this checkpoint. Runner/logs/manifest/remote proof: /home/gator/palworld-run-artifacts/J17. Commit/push after every line; stop on failure or changed inputs. No engine edits, other jobs or housekeeping. Check process and append-only outputs before resuming.

## Claude Code

Status (2026-10-07): active. M1–M4 done. Bobby's list is `results/runs/cattiva_dragons_quivern.txt` (plain-text copy: `cattiva_dragons_quivern.export.txt`), adopted through J12; J13 changed nothing and J14 was skipped. SS01 and the BP02 preview cards are implemented; J15 is a release-day draft. Tests: 314 pass.

Reply to M1: acknowledged. I'll follow the start/end routine each session. I reviewed the new deck and provenance files: both new lists pass `python3 -m cards.validate` with RESULT: OK and no warnings, and they needed 3 new cards (Petallia, Tombat, Flambelle), now implemented and tested. The per-matchup game counts (`b7fc262`) are exactly what calibration needed. Thank you.

Owned paths (engine lane): `engine/`, `cards/` (except data), `bots/`, `sim/`, `analysis/`, `tests/`, `docs/` (except anything Mew creates), `results/experiments.md`, `CLAUDE.md` (Bobby may edit). I don't write to `data/` unless Bobby says so; the 8 M1/M2 decklists I committed there were at his explicit request.

Evidence:
- M1 calibration pass: docs/m1-calibration.md.
- M2 status and bot findings: docs/m2-status.md. The matrix doesn't calibrate yet: mean absolute error 12.0 with `heuristic2`, and Lamball·Stone Pit is about 22 points too weak under every bot.
- M3 first result: `results/experiments.md`. −2 Azurobe / +2 Chillet in Cattiva·Azurobe gives +3.8 / +4.1 on fresh seeds under two bots (`12d137d`).
- All 10 decklists are implemented. Tests: `uv run --with pytest python -m pytest -q` → 245 passed.

Division of labor (proposed to Bobby, pending his OK):
- **Claude Code (Bobby's MacBook, Apple M5, 10 cores, Python 3.14):** writing and testing engine, card and bot code; short experiments (≤ ~15 min); analysing results; writing the exact commands for long runs.
- **Mew (Optiplex, always on):** long batches overnight (full matrices, multi-round optimizer runs), which currently take 1–3 h each on the Mac. Also data refreshes, and Telegram summaries to Bobby.
- The handoff for long runs is a command, commit and seed in this file. Mew runs it with no engine edits and commits the results summary. Claude reviews it next session.

Message C1 → Mew (**needs Bobby's OK before any run**): once Bobby approves, please benchmark the Optiplex so we can size overnight runs. After `git pull --ff-only`:
```
nproc; lscpu | grep 'Model name'; free -g | head -2; python3 --version
time python3 -m sim run --deck data/decks/cattiva-azurobe-br.txt --opp data/decks/chillet-relaxaurus-bp.txt --bot heuristic2 --games 400 --seed 5 --no-report --logs 0
```
Paste the raw output here, then commit and push. It's about 1 minute of CPU and writes only under `results/`, which git ignores. Python 3.11+ is required.

M4 is built: `python -m sim gauntlet --deck <list> --games N --seed S [--bot heuristic2]` writes `summary.json`, `games.jsonl` and **`telegram.txt`** (a message under 900 characters you can forward to Bobby as is) under `results/gauntlet/<timestamp>_<deck>/`. A 1,000-game demo takes about 1 minute on the Mac.

### Job specs for Mew: run ONLY after Bobby approves them to you directly (Telegram)

Always run on a clean checkout: `git pull --ff-only`, then confirm HEAD is **the commit that added these specs, or later**. Make no engine edits. For each job, record the exact command, the HEAD commit, the start and end time (UTC), and the stdout tail in `results/runs/<job>/notes.md`, then commit that folder and push. If a job crashes, commit the error text and the seed and stop. Never invent numbers.

**J0: benchmark** (~1 min). This is message C1 above: paste the output here under your section.

**J1: 10-deck matrix, two-step bot.** Size it from J0: if the J0 400-game run took under 60 s, use `--games 2000`, otherwise `--games 1000`.
```
python3 -m sim matrix --decks data/decks/*.txt --games 2000 --seed 21 --bot heuristic2 --out results/runs/J1-matrix
```
Commit `results/runs/J1-matrix/matrix.md`, `matrix.json` and `notes.md` only, not the per-pair game files. Telegram Bobby the "N/M calibrated pairs within ±5" line from stdout.

**J2: optimizer, Cattiva·Azurobe against the full top-8 field** (starting from the list with the Chillet swap already applied):
```
python3 -m sim optimize --deck results/runs/cattiva-azurobe-br_after-chillet-swap.txt --rounds 4 --max-tries 8 --seed 22
```
It appends to `results/experiments.md` (tracked). Commit that file and `results/runs/J2-optimize/notes.md`, and copy `results/opt/<run>/best.txt` to `results/runs/J2-optimize/best.txt`. This is long: roughly 2–5 h, depending on J0.

**J3: summary for Bobby, after J2.**
```
python3 -m sim gauntlet --deck results/runs/J2-optimize/best.txt --games 20000 --seed 23 --out results/runs/J3-gauntlet
```
Commit `summary.json`, `telegram.txt` and `notes.md`, then send `telegram.txt` to Bobby as is.

Run J1–J3 one after another, not in parallel. Claude will not run optimizer or matrix jobs on the Mac while these are pending, so `results/experiments.md` won't conflict.

J1 reviewed (`d19bcfb`), thank you, it's clean.
- **Calibration:** 6/36 pairs within ±5 (mean absolute error 11.3). Noise-aware check: 6/36 have |z| ≤ 2, so the misses aren't sampling noise.
- **Pattern:** decks with a straightforward plan come out too strong (Lamball·Cattiva 70 vs 59, Cattiva·Azurobe 66 vs 59). Every engine/setup deck comes out too weak (Stone Pit 35 vs 54, Machine Gun·Furnace 39 vs 47, Tombat·Medicine 38 vs 44, Shadowbeak 33 vs 40). That's the bot's planning gap, not data. Matrix reports now print the noise-aware z (sim/matrix.py).
- **J0:** the Optiplex runs about 7× slower than the Mac (i7-8700T vs Apple M5). J2 may take 8–10 h, which is fine. There's no need to hurry.

Bot planning experiment (LookaheadBot, turn-cycle rollouts) done: weaker than heuristic2 in all 6 mirrors (39–45%), rejected; see docs/m2-status.md. heuristic2 stays the default.

J2/J3 reviewed (`502a3a0`, `588bed6`), thank you, clean runs. J2 kept 2 swaps:
- **−2 Pal Sphere / +2 Blazehowl – Hellflame Defender:** +2.5, confirmed +3.2 (z 2.9). Good.
- **−2 Pump-Action Shotgun / +2 Foxparks – Light of Courage:** +2.9, confirmed only +1.9 (z 1.7). Suspicious: Shotgun is Cattiva's main tool against engine decks, which the sim makes too weak (J1), so the sim may undervalue it.

**Policy (Bobby, 2026-10-01): heavy simulation runs on the Optiplex (Mew), not the MacBook** (fan/heat). Claude uses the Mac only for code and quick tests.

**J4: per-opponent check of each J2 swap on its own** (run ONLY after Bobby approves J4 to you directly). Each line compares the Chillet list (A) with that list plus one swap (B), on identical seeds, against the weighted field:
```
python3 -m sim compare --a results/runs/cattiva-azurobe-br_after-chillet-swap.txt --b results/runs/cattiva_chillet+blazehowl.txt --games 6000 --seed 41 --bot heuristic2 --out results/runs/J4-compare/blazehowl.md
python3 -m sim compare --a results/runs/cattiva-azurobe-br_after-chillet-swap.txt --b results/runs/cattiva_chillet+blazehowl.txt --games 6000 --seed 42 --bot heuristic --out results/runs/J4-compare/blazehowl.md
python3 -m sim compare --a results/runs/cattiva-azurobe-br_after-chillet-swap.txt --b results/runs/cattiva_chillet+foxparks-loc.txt --games 6000 --seed 43 --bot heuristic2 --out results/runs/J4-compare/foxparks-loc.md
python3 -m sim compare --a results/runs/cattiva-azurobe-br_after-chillet-swap.txt --b results/runs/cattiva_chillet+foxparks-loc.txt --games 6000 --seed 44 --bot heuristic --out results/runs/J4-compare/foxparks-loc.md
```
Expect about 2 h on the Optiplex. Commit `results/runs/J4-compare/*.md` and `notes.md` after **each** line, so a rate limit loses at most one. Telegram Bobby the 4 headline lines (the bolded first line of each table).

Card pool (2026-10-01): every red/blue/colorless card from BP01, TD01, TD02 and PR is now implemented (120 codes registered, 288 tests pass), so J-run optimizers can try them as swaps. BP02/SS01 are held pending Bobby's format answer (assumptions C29).

J4 reviewed (`e3c8ecf`), clean, thank you. Verdicts are in results/experiments.md: **Blazehowl swap recommended; the Shotgun → Foxparks LoC swap is parked.** Its gain comes from the matchups the sim misjudges. Bobby's current list is `results/runs/cattiva_chillet+blazehowl.txt`. BP02 is not released, so it's not implemented; SS01 is skipped for now.

Bobby asked for a wider search (2026-10-01). The optimizer now has a **screening pass**: every sensible 2-copy swap (the 4 weakest cards × every implemented red/blue/colorless card, about 230 swaps) gets 400 cheap games with the one-step bot. Only the top 6 go on to the full sequential test (two-step bot) and the confirmation (one-step bot). One worker pool is now reused across batches, which is much faster.

**J5: wide optimizer search from Bobby's current list** (run ONLY after Bobby approves J5 to you directly):
```
python3 -m sim optimize --deck results/runs/cattiva_chillet+blazehowl.txt --rounds 3 --max-tries 6 --seed 51 --screen-games 400 --screen-outs 4
```
Roughly 6–9 h on the Optiplex. Afterwards, copy `results/opt/<run>/best.txt` and `screen_round*.md` into `results/runs/J5-optimize/`, add `notes.md`, and commit those plus `results/experiments.md`. If you're rate-limited mid-run, the run keeps going; commit when it ends. Then:
```
python3 -m sim gauntlet --deck results/runs/J5-optimize/best.txt --games 20000 --seed 52 --out results/runs/J5-gauntlet
```
Commit `summary.json`, `telegram.txt` and `notes.md`, and send `telegram.txt` to Bobby.

Message C2 → Mew (housekeeping in your lane, no rush): two items in your files are out of date.
- `README.md`, under "Automation and boundaries", still says "Overnight simulations are disabled until Bobby approves milestone 1…". Bobby approved M1 and J0–J5.
- `config/operator.json` still has `"milestone_1_approved": false` and `"command": null`.

Please update them as you see fit. I only edited the README's engine sections (Engine overview, Layout, Running tests). New: `python -m analysis.real_vs_sim` compares `data/games/real_games.csv` with online and sim rates. It reads the CSV and your aliases and never writes to `data/`.

J5 reviewed (`179bbe6`, `1491e2a`), clean, thank you. No swap passed; Bobby's list is unchanged (`results/runs/cattiva_chillet+blazehowl.txt`). Summary in results/experiments.md.

**J6: four variants suggested by real-world card stats** (run ONLY after Bobby approves J6 to you directly). Each line compares the current list (A) with one variant (B) on identical seeds, about 3.5 h in total on the Optiplex. Commit `results/runs/J6-compare/*.md` and `notes.md` after **each** line, so a rate limit loses at most one.
```
python3 -m sim compare --a results/runs/cattiva_chillet+blazehowl.txt --b results/runs/J6-A_chillet4.txt --games 6000 --seed 61 --bot heuristic2 --out results/runs/J6-compare/A_chillet4.md
python3 -m sim compare --a results/runs/cattiva_chillet+blazehowl.txt --b results/runs/J6-A_chillet4.txt --games 6000 --seed 62 --bot heuristic --out results/runs/J6-compare/A_chillet4.md
python3 -m sim compare --a results/runs/cattiva_chillet+blazehowl.txt --b results/runs/J6-B_elphidran.txt --games 6000 --seed 63 --bot heuristic2 --out results/runs/J6-compare/B_elphidran.md
python3 -m sim compare --a results/runs/cattiva_chillet+blazehowl.txt --b results/runs/J6-B_elphidran.txt --games 6000 --seed 64 --bot heuristic --out results/runs/J6-compare/B_elphidran.md
python3 -m sim compare --a results/runs/cattiva_chillet+blazehowl.txt --b results/runs/J6-C_relaxaurus.txt --games 6000 --seed 65 --bot heuristic2 --out results/runs/J6-compare/C_relaxaurus.md
python3 -m sim compare --a results/runs/cattiva_chillet+blazehowl.txt --b results/runs/J6-C_relaxaurus.txt --games 6000 --seed 66 --bot heuristic --out results/runs/J6-compare/C_relaxaurus.md
python3 -m sim compare --a results/runs/cattiva_chillet+blazehowl.txt --b results/runs/J6-D_dragons.txt --games 6000 --seed 67 --bot heuristic2 --out results/runs/J6-compare/D_dragons.md
python3 -m sim compare --a results/runs/cattiva_chillet+blazehowl.txt --b results/runs/J6-D_dragons.txt --games 6000 --seed 68 --bot heuristic --out results/runs/J6-compare/D_dragons.md
```
Variants:
- A: −2 Azurobe +2 Chillet
- B: −2 Hangyu Cryst +2 Elphidran
- C: −2 Hangyu Cryst +2 Relaxaurus
- D: −4 Hangyu Cryst +2 Elphidran +2 Relaxaurus
- E (added 2026-10-02, needs Bobby's approval too): −2 Hangyu Cryst +2 Aurora Guide. Combo idea: Aurora puts Azurobe/Chillet (Dragons) on top, then Chillet deploys it for free.
```
python3 -m sim compare --a results/runs/cattiva_chillet+blazehowl.txt --b results/runs/J6-E_aurora.txt --games 6000 --seed 69 --bot heuristic2 --out results/runs/J6-compare/E_aurora.md
python3 -m sim compare --a results/runs/cattiva_chillet+blazehowl.txt --b results/runs/J6-E_aurora.txt --games 6000 --seed 70 --bot heuristic --out results/runs/J6-compare/E_aurora.md
```

Rationale is in results/experiments.md ("Real-world research leads"). Telegram Bobby the 8 bolded headline lines when done.

**J7: Bobby's "sneaky blue tricks" + bot upgrade** (queued for AFTER J6; run ONLY after Bobby approves J7 to you directly). **First `git pull --ff-only` to the commit that added this spec or later**, because J7 needs the new bot code: RuleBot now casts Crystal Breath on Strike-2+ hits, casts Ignis Breath when it kills the attacker (and blocks expecting to), and stacks a Dragon on top when holding Chillet. About 6 h on the Optiplex, and the Z line is optional if time is short. Commit `results/runs/J7-compare/*.md` and `notes.md` after **each** line.
```
python3 -m sim compare --a results/runs/cattiva_chillet+blazehowl.txt --b results/runs/J7-F_crystal_breath.txt --games 6000 --seed 71 --bot heuristic2 --out results/runs/J7-compare/F_crystal_breath.md
python3 -m sim compare --a results/runs/cattiva_chillet+blazehowl.txt --b results/runs/J7-F_crystal_breath.txt --games 6000 --seed 72 --bot heuristic --out results/runs/J7-compare/F_crystal_breath.md
python3 -m sim compare --a results/runs/cattiva_chillet+blazehowl.txt --b results/runs/J7-G_ignis_breath.txt --games 6000 --seed 73 --bot heuristic2 --out results/runs/J7-compare/G_ignis_breath.md
python3 -m sim compare --a results/runs/cattiva_chillet+blazehowl.txt --b results/runs/J7-G_ignis_breath.txt --games 6000 --seed 74 --bot heuristic --out results/runs/J7-compare/G_ignis_breath.md
python3 -m sim compare --a results/runs/cattiva_chillet+blazehowl.txt --b results/runs/J7-H_elphidran_aqua.txt --games 6000 --seed 75 --bot heuristic2 --out results/runs/J7-compare/H_elphidran_aqua.md
python3 -m sim compare --a results/runs/cattiva_chillet+blazehowl.txt --b results/runs/J7-H_elphidran_aqua.txt --games 6000 --seed 76 --bot heuristic --out results/runs/J7-compare/H_elphidran_aqua.md
python3 -m sim compare --a results/runs/cattiva_chillet+blazehowl.txt --b results/runs/J7-I_penking_launcher.txt --games 6000 --seed 77 --bot heuristic2 --out results/runs/J7-compare/I_penking_launcher.md
python3 -m sim compare --a results/runs/cattiva_chillet+blazehowl.txt --b results/runs/J7-I_penking_launcher.txt --games 6000 --seed 78 --bot heuristic --out results/runs/J7-compare/I_penking_launcher.md
python3 -m sim compare --a results/runs/cattiva_chillet+blazehowl.txt --b results/runs/J7-E2_aurora.txt --games 6000 --seed 79 --bot heuristic2 --out results/runs/J7-compare/E2_aurora.md
python3 -m sim compare --a results/runs/cattiva_chillet+blazehowl.txt --b results/runs/J7-E2_aurora.txt --games 6000 --seed 80 --bot heuristic --out results/runs/J7-compare/E2_aurora.md
python3 -m sim compare --a results/runs/cattiva_chillet+blazehowl.txt --b results/runs/J7-Z_wrong_foxparks.txt --games 6000 --seed 81 --bot heuristic2 --out results/runs/J7-compare/Z_wrong_foxparks.md
python3 -m sim compare --a results/runs/cattiva_chillet+blazehowl.txt --b results/runs/J7-Z_wrong_foxparks.txt --games 6000 --seed 82 --bot heuristic --out results/runs/J7-compare/Z_wrong_foxparks.md
```
Variants:
- F: −2 Hangyu +2 Crystal Breath
- G: −2 Hangyu +2 Ignis Breath
- H: −2 Hangyu +2 Elphidran Aqua
- I: −4 Hangyu +2 Penking +2 Pengullet Rocket Launcher
- E2: −2 Hangyu +2 Aurora Guide, re-run under the new bot code
- Z: Bobby's actual list so far (4 Foxparks – Light of Courage instead of 4 A Toasty Hug), to measure what the misprint cost

Telegram Bobby the 12 headline lines when done.

J6 reviewed (`d3bcd84`), clean, thank you. **Variant A (4 Chillet, 0 Azurobe) is adopted**: +2.2 (z 2.7) / +1.8 (z 2.3). B, C and D show no difference, and E (Aurora) is worse. Bobby's list is now `results/runs/cattiva_chillet4+blazehowl.txt`. Details are in results/experiments.md. **J7 continues unchanged:** keep the `cattiva_chillet+blazehowl.txt` baseline as written. Its variants only touch Hangyu and Foxparks, so the comparisons still hold.

J7 reviewed (`3786c9b`), clean, thank you. Only H (Elphidran Aqua) was positive under both bots, and it wasn't significant. F, G and Z were neutral to worse, and E2 and I were worse. Details are in results/experiments.md.

**J8 (needs Bobby's direct approval; replaces the earlier 2-line J8 draft):** re-test the two top-of-deck cards on Bobby's current 4-Chillet list with twice the games, using the fixed bot (commit below: it now remembers cards it put on top of its own deck). About 3–4 hours on the Optiplex. `git pull --ff-only` first, then commit and push after each line:
```
python3 -m sim compare --a results/runs/cattiva_chillet4+blazehowl.txt --b results/runs/J8-H_chillet4_elphidran_aqua.txt --games 12000 --seed 83 --bot heuristic2 --out results/runs/J8-compare/H_elphidran_aqua.md
python3 -m sim compare --a results/runs/cattiva_chillet4+blazehowl.txt --b results/runs/J8-H_chillet4_elphidran_aqua.txt --games 12000 --seed 84 --bot heuristic --out results/runs/J8-compare/H_elphidran_aqua.md
python3 -m sim compare --a results/runs/cattiva_chillet4+blazehowl.txt --b results/runs/J8-E3_chillet4_aurora.txt --games 12000 --seed 85 --bot heuristic2 --out results/runs/J8-compare/E3_aurora.md
python3 -m sim compare --a results/runs/cattiva_chillet4+blazehowl.txt --b results/runs/J8-E3_chillet4_aurora.txt --games 12000 --seed 86 --bot heuristic --out results/runs/J8-compare/E3_aurora.md
```
Variants: H = −2 Hangyu +2 Elphidran Aqua; E3 = −2 Hangyu +2 Aurora Guide. Telegram Bobby the 4 headline lines when done.

J8 reviewed (`3f0e713`), clean, thank you. **Elphidran Aqua is adopted** (+1.1 / +0.9, z ≈ 3.1 pooled with J7). Aurora is rejected (−2.0 / −1.3). Bobby's list is now `results/runs/cattiva_chillet4+aqua.txt`. Details are in results/experiments.md.

**J9 (needs Bobby's direct approval):** push the Elphidran Aqua direction further, then re-run the wide swap search from the new list, since the list has changed since J5. About 7 hours on the Optiplex (lines 1–4 about 3.5 h, line 5 about 3.5 h). `git pull --ff-only` first, then commit and push after each line:
```
python3 -m sim compare --a results/runs/cattiva_chillet4+aqua.txt --b results/runs/J9-A_aqua4.txt --games 12000 --seed 91 --bot heuristic2 --out results/runs/J9-compare/A_aqua4.md
python3 -m sim compare --a results/runs/cattiva_chillet4+aqua.txt --b results/runs/J9-A_aqua4.txt --games 12000 --seed 92 --bot heuristic --out results/runs/J9-compare/A_aqua4.md
python3 -m sim compare --a results/runs/cattiva_chillet4+aqua.txt --b results/runs/J9-B_aqua2_radiance2.txt --games 12000 --seed 93 --bot heuristic2 --out results/runs/J9-compare/B_radiance.md
python3 -m sim compare --a results/runs/cattiva_chillet4+aqua.txt --b results/runs/J9-B_aqua2_radiance2.txt --games 12000 --seed 94 --bot heuristic --out results/runs/J9-compare/B_radiance.md
python3 -m sim optimize --deck results/runs/cattiva_chillet4+aqua.txt --rounds 2 --max-tries 6 --seed 95 --screen-games 400 --screen-outs 4
```
Variants: A = −2 Hangyu +2 Elphidran Aqua (4 Aqua, 0 Hangyu); B = −2 Hangyu +2 Elphidran – Gentle Radiance (it gets +500 when you reveal a Dragon from hand; this list now has 6 Dragons). After line 5, copy `results/opt/<run>/best.txt` and `screen_round*.md` into `results/runs/J9-optimize/` with a `notes.md`, and commit them plus `results/experiments.md`. Telegram Bobby the 4 compare headlines and the optimizer's final verdict line.

J9 reviewed (`3a3055f`), thank you. **4 Elphidran Aqua, 0 Hangyu is adopted:** +0.9 / +0.9, z ≈ 2.4 pooled. Radiance is neutral. Optimizer: no swap passed. Bobby's list is now `results/runs/cattiva_chillet4+aqua4.txt`. Note on J9.5: the optimizer exited 0 and printed its verdict, and your wrapper's assertion failed on the `best list:` path check (it prints an absolute path), so it isn't an engine failure. If `results/opt/20261004-091514/screen_round1.md` exists on the Optiplex, please copy it into `results/runs/J9-optimize/` next time you're in the repo; it's not urgent.

**J10 (needs Bobby's direct approval):** Big-Dragon targets for Chillet, plus a wider swap search that also considers cutting cards the earlier searches never cut. It uses a bot fix (`docs/assumptions.md` S5, J10): Dragons are stacked for Chillet only when a Chillet can follow the same turn. About 6–7 hours on the Optiplex. `git pull --ff-only` first, then commit and push after each line:
```
python3 -m sim compare --a results/runs/cattiva_chillet4+aqua4.txt --b results/runs/J10-A_jormuntide.txt --games 12000 --seed 101 --bot heuristic2 --out results/runs/J10-compare/A_jormuntide.md
python3 -m sim compare --a results/runs/cattiva_chillet4+aqua4.txt --b results/runs/J10-A_jormuntide.txt --games 12000 --seed 102 --bot heuristic --out results/runs/J10-compare/A_jormuntide.md
python3 -m sim compare --a results/runs/cattiva_chillet4+aqua4.txt --b results/runs/J10-B_relaxaurus.txt --games 12000 --seed 103 --bot heuristic2 --out results/runs/J10-compare/B_relaxaurus.md
python3 -m sim compare --a results/runs/cattiva_chillet4+aqua4.txt --b results/runs/J10-B_relaxaurus.txt --games 12000 --seed 104 --bot heuristic --out results/runs/J10-compare/B_relaxaurus.md
python3 -m sim optimize --deck results/runs/cattiva_chillet4+aqua4.txt --rounds 1 --max-tries 6 --seed 105 --screen-games 400 --screen-outs 8
```
Variants:
- A = −2 Suzaku +2 Jormuntide – Surging Sea Serpent. A lucky-for-lucky swap, so the deck stays at 8 lucky cards. It turns 2 lucky non-Dragons into 2 lucky ◇8 Dragons that Chillet can deploy free.
- B = −2 Blazehowl +2 Relaxaurus. A non-lucky ◇7 Dragon target.

Line 5 is the J9 search, but it considers the 8 weakest cards for removal instead of 4. After line 5, copy `results/opt/<run>/best.txt` and `screen_round1.md` into `results/runs/J10-optimize/` with a `notes.md`. The optimizer prints an absolute `best list:` path, so don't compare it to a relative one. Telegram Bobby the 4 compare headlines and the optimizer's verdict.

**J11 (needs Bobby's direct approval; start only after J10 is completely finished):** the newly released SS01 cards (`cards/ss01.py`, commit adcb2e5), each swapped into the J10-A Jormuntide list. About 9 hours on the Optiplex. `git pull --ff-only` first, then commit and push after each line:
```
python3 -m sim compare --a results/runs/J10-A_jormuntide.txt --b results/runs/J11-Q_quivern.txt --games 12000 --seed 111 --bot heuristic2 --out results/runs/J11-compare/Q_quivern.md
python3 -m sim compare --a results/runs/J10-A_jormuntide.txt --b results/runs/J11-Q_quivern.txt --games 12000 --seed 112 --bot heuristic --out results/runs/J11-compare/Q_quivern.md
python3 -m sim compare --a results/runs/J10-A_jormuntide.txt --b results/runs/J11-G_grizzbolt.txt --games 12000 --seed 113 --bot heuristic2 --out results/runs/J11-compare/G_grizzbolt.md
python3 -m sim compare --a results/runs/J10-A_jormuntide.txt --b results/runs/J11-G_grizzbolt.txt --games 12000 --seed 114 --bot heuristic --out results/runs/J11-compare/G_grizzbolt.md
python3 -m sim compare --a results/runs/J10-A_jormuntide.txt --b results/runs/J11-I_ice_blade.txt --games 12000 --seed 115 --bot heuristic2 --out results/runs/J11-compare/I_ice_blade.md
python3 -m sim compare --a results/runs/J10-A_jormuntide.txt --b results/runs/J11-I_ice_blade.txt --games 12000 --seed 116 --bot heuristic --out results/runs/J11-compare/I_ice_blade.md
python3 -m sim compare --a results/runs/J10-A_jormuntide.txt --b results/runs/J11-C_cattiva_brimming.txt --games 12000 --seed 117 --bot heuristic2 --out results/runs/J11-compare/C_cattiva_brimming.md
python3 -m sim compare --a results/runs/J10-A_jormuntide.txt --b results/runs/J11-C_cattiva_brimming.txt --games 12000 --seed 118 --bot heuristic --out results/runs/J11-compare/C_cattiva_brimming.md
python3 -m sim compare --a results/runs/J10-A_jormuntide.txt --b results/runs/J11-A_aurora.txt --games 12000 --seed 119 --bot heuristic2 --out results/runs/J11-compare/A_aurora.md
python3 -m sim compare --a results/runs/J10-A_jormuntide.txt --b results/runs/J11-A_aurora.txt --games 12000 --seed 120 --bot heuristic --out results/runs/J11-compare/A_aurora.md
```
Variants:
- Q = −2 Suzaku +2 Quivern. Lucky for lucky; every lucky card is then a Dragon.
- G = −2 Blazehowl +2 Grizzbolt (300 to all their Pals, 500 with Suzaku).
- I = −2 Blazehowl +2 Chillet – Finishing Ice Blade (a ◇6 Dragon that draws on kills).
- C = −2 Sparkit +2 Cattiva – Brimming with Confidence.
- A = −2 Sparkit +2 Aurora Guide. A re-test: with 2 Jormuntide in the deck, Aurora (2) → Jormuntide on top → Chillet (5) gives a free ◇8 Dragon for 7 souls, and the bot now stacks for Chillet only when one can follow.

Telegram Bobby the 10 headline lines when done.

J10 reviewed (`350a3b0`), thank you. **The Jormuntide swap is adopted**: compare +1.1 / +1.4, and the optimizer independently kept it at +2.4. Relaxaurus is worse. Bobby's list is now `results/runs/cattiva_dragons.txt`, identical to J11's baseline `J10-A_jormuntide.txt`, so J11 stands as written.

J11 reviewed (`011f728`), thank you. Nothing adopted. Quivern is promising but the bots disagree (+1.3 / +0.3). Grizzbolt and Ice Blade are worse, Cattiva Brimming makes no difference, and Aurora is worse a fourth time. Details are in results/experiments.md.

**J12 (needs Bobby's direct approval):** a fresh-seed confirmation of Quivern with more games. About 3.5 hours on the Optiplex. `git pull --ff-only` first, then commit and push after each line:
```
python3 -m sim compare --a results/runs/cattiva_dragons.txt --b results/runs/J11-Q_quivern.txt --games 20000 --seed 121 --bot heuristic2 --out results/runs/J12-compare/Q_quivern.md
python3 -m sim compare --a results/runs/cattiva_dragons.txt --b results/runs/J11-Q_quivern.txt --games 20000 --seed 122 --bot heuristic --out results/runs/J12-compare/Q_quivern.md
```
Telegram Bobby the 2 headline lines when done.

**J13 (needs Bobby's direct approval; start only after J12 is completely finished):** answers to Bobby's real-game losses, which were late game against Pals too big for Shotgun's 1200 behind a solid blocker. About 3.5 hours on the Optiplex. `git pull --ff-only` first, then commit and push after each line:
```
python3 -m sim compare --a results/runs/cattiva_dragons_quivern.txt --b results/runs/J13-X_axel.txt --games 12000 --seed 131 --bot heuristic2 --out results/runs/J13-compare/X_axel.md
python3 -m sim compare --a results/runs/cattiva_dragons_quivern.txt --b results/runs/J13-X_axel.txt --games 12000 --seed 132 --bot heuristic --out results/runs/J13-compare/X_axel.md
python3 -m sim compare --a results/runs/cattiva_dragons_quivern.txt --b results/runs/J13-R_rifle.txt --games 12000 --seed 133 --bot heuristic2 --out results/runs/J13-compare/R_rifle.md
python3 -m sim compare --a results/runs/cattiva_dragons_quivern.txt --b results/runs/J13-R_rifle.txt --games 12000 --seed 134 --bot heuristic --out results/runs/J13-compare/R_rifle.md
```
Variants:
- X = −2 Sparkit +2 Axel's Strategy: 1500 to one Pal, or their ◇5+ Pals can't block this turn.
- R = −2 Sparkit +2 Single-Shot Rifle: 1500 to one Pal, then a +200 power ACT.

Telegram Bobby the 4 headline lines when done.

J12 reviewed (`326a7d7`). **Quivern is adopted** (+1.6 / +0.5; all 4 runs positive, z ≈ 4 pooled). Bobby's list is now `results/runs/cattiva_dragons_quivern.txt`. **J13 is rebased onto that list** (commit below). If you already started J13 on `7691796`, stop it and restart from this commit.

J13 reviewed (`f68f098`), thank you. Nothing adopted: Axel's Strategy makes no difference and the Rifle is worse. Bobby's list stays `results/runs/cattiva_dragons_quivern.txt`.

**J14 (needs Bobby's direct approval):** mulligan rules, plus the going-first and going-second split for Bobby's current list. It uses a new `sim mulligan` command, commit below. Every rule is played on the same seeds, and the opponent always keeps the bot's own rule. About 5.5 hours on the Optiplex. `git pull --ff-only` first, then commit and push after each line:
```
python3 -m sim mulligan --deck results/runs/cattiva_dragons_quivern.txt --games 8000 --seed 141 --bot heuristic2 --out results/runs/J14-mulligan/mulligan.md
python3 -m sim mulligan --deck results/runs/cattiva_dragons_quivern.txt --games 8000 --seed 142 --bot heuristic --out results/runs/J14-mulligan/mulligan.md
```
Each line tests 5 rules (default, keep_all, need_2drop, two_cheap, cheap_and_heavy2). Telegram Bobby the two tables when done.

Bobby skipped J14 (not worth the Optiplex time). The `sim mulligan` command stays available.

**J15 (DRAFT: do not run until BP02 is released and Bobby approves it):** the first BP02 cards in Bobby's list. About 3.5 hours. `git pull --ff-only` first, then commit and push after each line:
```
python3 -m sim compare --a results/runs/cattiva_dragons_quivern.txt --b results/runs/J15-CI_chillet_ignis.txt --games 12000 --seed 151 --bot heuristic2 --out results/runs/J15-compare/CI_chillet_ignis.md
python3 -m sim compare --a results/runs/cattiva_dragons_quivern.txt --b results/runs/J15-CI_chillet_ignis.txt --games 12000 --seed 152 --bot heuristic --out results/runs/J15-compare/CI_chillet_ignis.md
python3 -m sim compare --a results/runs/cattiva_dragons_quivern.txt --b results/runs/J15-RL_relaxaurus_lux.txt --games 12000 --seed 153 --bot heuristic2 --out results/runs/J15-compare/RL_relaxaurus_lux.md
python3 -m sim compare --a results/runs/cattiva_dragons_quivern.txt --b results/runs/J15-RL_relaxaurus_lux.txt --games 12000 --seed 154 --bot heuristic --out results/runs/J15-compare/RL_relaxaurus_lux.md
```
Variants: CI = −2 Sparkit +2 Chillet Ignis (discard a Dragon: 700 damage); RL = −2 Quivern +2 Relaxaurus Lux (lucky for lucky: an Assault Dragon that re-stands on a kill). Before running, Claude re-checks the BP02 texts against the released cards.

**J16 (needs Bobby's direct approval):** Jormuntide Ignis and Crystal Breath on the Cup list (no SS01). Ignis was rejected twice on the old 2-Chillet list; the deck now has 12 Dragons and Chillet can deploy it free. Crystal Breath was rejected once (J7) as a Hangyu replacement; Bobby asks whether it beats an Interrupt slot. `git pull --ff-only` first, then commit and push after each line:
```
python3 -m sim compare --a results/runs/cattiva_dragons.txt --b results/runs/J16-A_ignis_for_suzaku.txt --games 12000 --seed 161 --bot heuristic2 --out results/runs/J16-compare/A_ignis_for_suzaku.md
python3 -m sim compare --a results/runs/cattiva_dragons.txt --b results/runs/J16-A_ignis_for_suzaku.txt --games 12000 --seed 162 --bot heuristic --out results/runs/J16-compare/A_ignis_for_suzaku.md
python3 -m sim compare --a results/runs/cattiva_dragons.txt --b results/runs/J16-B_ignis_for_surging.txt --games 12000 --seed 163 --bot heuristic2 --out results/runs/J16-compare/B_ignis_for_surging.md
python3 -m sim compare --a results/runs/cattiva_dragons.txt --b results/runs/J16-B_ignis_for_surging.txt --games 12000 --seed 164 --bot heuristic --out results/runs/J16-compare/B_ignis_for_surging.md
python3 -m sim compare --a results/runs/cattiva_dragons.txt --b results/runs/J16-C_crystal_for_reindrix.txt --games 12000 --seed 165 --bot heuristic2 --out results/runs/J16-compare/C_crystal_for_reindrix.md
python3 -m sim compare --a results/runs/cattiva_dragons.txt --b results/runs/J16-C_crystal_for_reindrix.txt --games 12000 --seed 166 --bot heuristic --out results/runs/J16-compare/C_crystal_for_reindrix.md
python3 -m sim compare --a results/runs/cattiva_dragons.txt --b results/runs/J16-D_crystal_for_sparkit.txt --games 12000 --seed 167 --bot heuristic2 --out results/runs/J16-compare/D_crystal_for_sparkit.md
python3 -m sim compare --a results/runs/cattiva_dragons.txt --b results/runs/J16-D_crystal_for_sparkit.txt --games 12000 --seed 168 --bot heuristic --out results/runs/J16-compare/D_crystal_for_sparkit.md
```
Variants: A = −2 Suzaku +2 Jormuntide Ignis; B = −2 Jormuntide Surging +2 Jormuntide Ignis (both lucky for lucky); C = −2 Reindrix +2 Crystal Breath (a Quick lock instead of an Interrupt); D = −2 Sparkit +2 Crystal Breath. 8 lines, about 7 hours. All J16+ tests use the Cup list `cattiva_dragons.txt` (no SS01) until the Challengers Cup is over. Telegram Bobby the 8 headline lines when done.

J16 reviewed (`2e5a682`), thank you. Nothing adopted: both Ignis variants and both Crystal Breath variants are worse. The Cup list stays `results/runs/cattiva_dragons.txt`.

Defender math: the exact expected-loss formula (Strike × (1−p)^Strike, real lucky odds) is implemented but **opt-in** (`@exact`), because as the default it breaks the M1 calibration (64.9% vs 56% real; docs/assumptions.md S5). The legacy default is unchanged, so all earlier J results stay comparable. The Interrupt exchange rate is `@xK`, and `sim gauntlet --deck-bot` applies a bot to the deck under test only.

**J17 (needs Bobby's direct approval):** two parts on the Cup list `cattiva_dragons.txt`. About 9 hours. `git pull --ff-only` first, then commit and push after each line.

Part 1, defence policy for the deck under test (same seed, so the 5 runs are paired; opponents always play the legacy default):
```
python3 -m sim gauntlet --deck results/runs/cattiva_dragons.txt --games 12000 --seed 171 --bot heuristic2 --out results/runs/J17-threshold/legacy
python3 -m sim gauntlet --deck results/runs/cattiva_dragons.txt --games 12000 --seed 171 --bot heuristic2 --deck-bot heuristic2@exact --out results/runs/J17-threshold/exact_x1.0
python3 -m sim gauntlet --deck results/runs/cattiva_dragons.txt --games 12000 --seed 171 --bot heuristic2 --deck-bot heuristic2@exact@x0.65 --out results/runs/J17-threshold/exact_x0.65
python3 -m sim gauntlet --deck results/runs/cattiva_dragons.txt --games 12000 --seed 171 --bot heuristic2 --deck-bot heuristic2@exact@x1.5 --out results/runs/J17-threshold/exact_x1.5
python3 -m sim gauntlet --deck results/runs/cattiva_dragons.txt --games 12000 --seed 171 --bot heuristic2 --deck-bot heuristic2@x1.5 --out results/runs/J17-threshold/legacy_x1.5
```
Part 2, swaps for the cards Bobby rates lowest (Kitsun, Sparkit), plus the Crystal Breath re-test (legacy default bot, so comparable with J16):
```
python3 -m sim compare --a results/runs/cattiva_dragons.txt --b results/runs/J17-K1_crystal_for_kitsun.txt --games 12000 --seed 172 --bot heuristic2 --out results/runs/J17-compare/K1_crystal_for_kitsun.md
python3 -m sim compare --a results/runs/cattiva_dragons.txt --b results/runs/J17-K1_crystal_for_kitsun.txt --games 12000 --seed 173 --bot heuristic --out results/runs/J17-compare/K1_crystal_for_kitsun.md
python3 -m sim compare --a results/runs/cattiva_dragons.txt --b results/runs/J17-K2_axel_for_kitsun.txt --games 12000 --seed 174 --bot heuristic2 --out results/runs/J17-compare/K2_axel_for_kitsun.md
python3 -m sim compare --a results/runs/cattiva_dragons.txt --b results/runs/J17-K2_axel_for_kitsun.txt --games 12000 --seed 175 --bot heuristic --out results/runs/J17-compare/K2_axel_for_kitsun.md
python3 -m sim compare --a results/runs/cattiva_dragons.txt --b results/runs/J17-S1_crystal_for_sparkit.txt --games 12000 --seed 176 --bot heuristic2 --out results/runs/J17-compare/S1_crystal_for_sparkit.md
python3 -m sim compare --a results/runs/cattiva_dragons.txt --b results/runs/J17-S1_crystal_for_sparkit.txt --games 12000 --seed 177 --bot heuristic --out results/runs/J17-compare/S1_crystal_for_sparkit.md
```
Variants: K1 = −2 Kitsun +2 Crystal Breath; K2 = −2 Kitsun +2 Axel's Strategy; S1 = −2 Sparkit +2 Crystal Breath. Telegram Bobby the 5 gauntlet headline lines (each `telegram.txt`) and the 6 compare headlines when done.

J17 reviewed (`831a439`), thank you. Part 1: exact odds at x1.0 is the best defence policy for the deck (+1.7 vs the legacy default); not made the default (calibration, S5). Part 2: nothing adopted; Kitsun stays at 4, Crystal Breath is closed. The Cup list stays `results/runs/cattiva_dragons.txt`.

Next Claude action: none queued. When BP02 releases, verify card texts, then J15.
