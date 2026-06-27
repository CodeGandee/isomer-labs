# Write Boundaries

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require selected Topic Workspace context and a worktree plan or validation result.
2. Write or update topic-level boundary material that names `<topic-workspace-dir>/repos/topic-main`, the `agents/` worktree root, branch namespace rules, and integration expectations.
3. Write or update per-agent Agent Workspace boundary material under each prepared `<topic-workspace-dir>/agents/<agent-name>` when the path is ready or explicitly planned.
4. State write ownership for the owning agent name, `.isomer-agent/` support layout, approved `.isomer-agent/links/` symlink targets, and Peer Read Access expectations for other topic-local agents.
5. State that Workspace Boundaries and Peer Read Access are advisory collaboration contracts, not filesystem-grade security isolation.
6. Report boundary material paths, skipped paths, blockers, and next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to draft the smallest boundary material that makes ownership and peer-read rules explicit.

## Boundary Content

Boundary material should name the owner, expected branch prefix, current worktree path, peer-readable surfaces, integration branch expectations, and any forbidden direct writes by peers.

Do not claim operating-system sandboxing or hard access control.
