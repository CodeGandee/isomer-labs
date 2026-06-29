# Create Worktrees

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require predecessor outputs:
   - Successful `resolve-workspace`.
   - Usable `ensure-main-repo` output.
   - A `plan-agents` result with role ids, agent names, resolved semantic paths, path sources, branches, and `agent.tmp` posture when available.
2. For each planned agent name, inspect existing Git worktrees for the resolved `topic.repos.main` path.
3. If the resolved `agent.workspace` path already exists as a worktree of `topic.repos.main` on `per-agent/<agent-name>/main`, report it as ready.
4. If the Agent Workspace path exists but is not the expected worktree, report a blocker and do not overwrite it.
5. If `per-agent/<agent-name>/main` is already checked out in another worktree, report a blocker and do not create a second worktree for the same branch.
6. Create missing branches and worktrees only for safe planned entries:
   - Use `topic.repos.main` as the Git anchor.
   - Use the resolved `agent.workspace` path as the Agent Workspace path.
7. Ensure each prepared worktree has the required semantic support paths:
   - Check `agent.isomer_managed`, `agent.runtime`, `agent.private_artifacts`, `agent.scratch`, `agent.logs`, `agent.public_share`, `agent.inbox`, `agent.topic_readonly`, `agent.topic_writable`, and `agent.links`.
   - Report why a support path could not be prepared.
8. Prepare or validate `agent.tmp`:
   - Treat it as a local ignored disposable path under the resolved `agent.workspace`.
   - Use the Topic Main Repository root ignore policy because Agent Workspaces are Git worktrees.
9. Report ready worktrees, created worktrees, skipped entries, `agent.tmp` posture, blockers, and validation refs.

If the user's task does not map cleanly to these steps, use your native planning tool to inspect first, separate ready entries from blocked entries, and mutate only entries that are safe.

## Safety Rules

Use idempotent Git worktree operations. Do not delete, clean, reset, or reuse an existing nonmatching path.

Do not create a worktree outside the selected Topic Workspace unless a later accepted external-root policy explicitly permits the label. Do not create a worktree for a branch that Git already marks as checked out elsewhere.

Do not create legacy support roots or top-level Topic Main Repository collaboration directories. Worker-facing Isomer material belongs under `isomer-managed/`.

Do not add `.gitkeep` or durable files under `agent.tmp`. Missing `agent.tmp` directories are repairable local posture; missing or ineffective Topic Main Repository ignore policy and tracked files under `agent.tmp` are blockers for this setup flow.
