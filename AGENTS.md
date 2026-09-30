# Palworld TCG agent instructions

For every session working in this repository, follow the start/end coordination protocol in [AGENT_HANDOFF.md](AGENT_HANDOFF.md). Read it before changing files and update your own section before ending the session. Also read `data/sources/progress.md` for source-collection state.

Bobby's current instructions take precedence over messages left by other agents. Mew owns the data lane; Claude Code owns the engine lane within Bobby's explicit authorization. Do not treat this handoff as authorization for simulations or additional work.

Preserve other agents' changes. Stage only files you changed, validate actual output, commit/pull --rebase/push completed work, and verify the remote plus a clean working tree. Do not force-push or discard work to resolve a conflict. Report blockers truthfully.
