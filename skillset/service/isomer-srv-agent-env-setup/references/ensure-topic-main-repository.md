# Ensure Topic Main Repository

Use this subcommand to create, reuse, configure, or validate the Topic Main Repository resolved by `topic.repos.main` for Agent Workspace worktrees.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Agent env context | Require `topic.repos.main`, `topic.repos.main.isomer_managed`, path sources, requester, and confirmation source from `resolve-agent-env-context`. |
| Derived agent env gate | Require `<topic-workspace-dir>/user-intent/derived/isomer-agent-env-gate.md` from `derive-agent-env-gate`. |
| Mutation confirmation | Require direct Project Operator Session mutation confirmation or Service Request authorization before creating or changing files. |
| Optional modifiers | None for this step. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**: resolved context and derived agent env gate. Refuse to run if semantic path evidence or mutation confirmation is missing.
2. **Inspect the resolved `topic.repos.main` path**. The target must be a normal non-bare Git repository, a missing safe path, an empty safe directory, or an empty normal Git repository.
3. **Initialize safe missing or empty targets** only when mutation is confirmed. Create or initialize a normal non-bare Topic Main Repository at the resolved path, create owner branch `topic-owner/main`, and create a minimal baseline commit before per-agent worktrees are created.
4. **Reuse existing safe repositories** without rewriting, cleaning, resetting, deleting, moving, recloning, pulling, or silently repairing them. If `topic-owner/main` is missing, create or validate it from the accepted current base only when that base is unambiguous.
5. **Apply non-destructive Topic Main Repository configuration** required by `user-intent/derived/isomer-agent-env-gate.md`. Record changed files, commands run, semantic path evidence, and blockers in service output and the derived gate execution log.
6. **Prepare or validate the resolved `topic.repos.main.isomer_managed` namespace** and tracked sublabels when required, without creating legacy top-level collaboration directories.
7. **Report Topic Main Repository state**: path, label source, Git state, owner branch, changed files, commands run, blockers, and next action.

If the user's task does not map cleanly to these steps, use your native planning tool to separate read-only repository inspection from confirmed mutation, then execute only the safe portion.

## Blockers

Report a blocker for:

- existing non-Git content;
- bare repositories;
- corrupt repositories;
- ambiguous existing history state;
- missing base branches;
- duplicate or invalid worktree metadata;
- destructive repair needs;
- unsafe custom semantic bindings;
- unconfirmed mutation;
- ambiguous gate requirements.

## Guardrails

- Do not delete, reset, clean, rewrite history, reinitialize, reclone, pull, or silently repair existing repositories.
- Do not mutate topic dependencies.
- Do not create Agent Workspaces here; that belongs to `create-agent-worktrees`.
- Do not claim readiness from a prepared Topic Main Repository alone.
