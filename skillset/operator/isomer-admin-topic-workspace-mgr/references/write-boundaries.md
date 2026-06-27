# Write Boundaries

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require selected Topic Workspace context and a worktree plan or validation result.
2. Write or update topic-level boundary material that names `topic.main_repo`, `topic.main_repo.isomer_managed`, resolved paths, path sources, branch namespace rules, and integration expectations.
3. Write or update per-agent Agent Workspace boundary material under each prepared resolved `agent.workspace` path when the path is ready or explicitly planned.
4. State write ownership for the owning agent name, required `agent.*` support labels, approved `agent.public_share` Peer Read Access, topic-owned projection policies, generated `agent.links` targets, and Peer Read Access expectations for other topic-local agents.
5. State that Workspace Boundaries and Peer Read Access are advisory collaboration contracts, not filesystem-grade security isolation.
6. Report boundary material paths, skipped paths, blockers, and next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to draft the smallest boundary material that makes ownership and peer-read rules explicit.

## Boundary Content

Boundary material should name the owner, expected branch prefix, resolved `agent.workspace` path, path source, `isomer-managed/` tracked and untracked regimes, peer-readable labels, generated links, integration branch expectations, topic-owned writable policy when present, and any forbidden direct writes by peers. Include guidance that an agent running inside its own Agent Workspace can query its own `agent.*` labels without passing Agent Name; cwd inference is not filesystem-grade identity or access control.

Do not claim operating-system sandboxing or hard access control.
