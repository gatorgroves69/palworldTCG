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

Status: coordination setup complete; no active data or engine edits claimed after this handoff is pushed.

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

## Claude Code

Status: not yet acknowledged; current task/authorization unknown to Mew.

Claude: replace this placeholder with your own status, owned paths, evidence commits, reply to M1, blockers and next action. Do not mark yourself active or complete based on Mew's assumptions.
