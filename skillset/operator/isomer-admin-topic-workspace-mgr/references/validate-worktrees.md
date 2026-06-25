# Validate Worktrees

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require selected Topic Workspace context and expected agent plan or packet/profile material.
2. Validate that `<topic-workspace-dir>/repos/topic-main` exists as the usable shared non-bare topic repository.
3. Validate each expected `<topic-workspace-dir>/agents/<agent-key>` path as a worktree of `topic-main` on `per-agent/<agent-key>/main` unless a specific future branch is in scope.
4. Check Git worktree metadata for duplicate branch checkout and branches outside the owning `per-agent/<agent-key>/` namespace.
5. Check active role binding `agent_workspace_ref` values in packet or profile material and reject refs outside the selected Topic Workspace or inside another Research Topic's Topic Workspace.
6. Check that boundary material names write ownership, Peer Read Access, branch rules, and advisory boundary status when it is expected.
7. Report validation status, ready entries, blockers, deferrals, and next operator action without creating Agent Instances, Workspace Runtime records, Houmao agents, or Execution Adapter material.

If the user's task does not map cleanly to these steps, use your native planning tool to run read-only checks first, then report a partial validation status and missing inputs.

## Validation Status

Use `ready` when Git topology, refs, and boundary material match the plan. Use `ready-with-deferrals` when nonblocking static notes remain. Use `blocked` for unsafe repo state, missing worktrees, duplicate checkout, unsafe path, cross-topic ref, or unresolved role mapping.
