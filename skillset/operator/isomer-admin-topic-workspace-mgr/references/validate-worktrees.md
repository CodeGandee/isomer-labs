# Validate Worktrees

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require selected Topic Workspace context and expected agent plan or packet/profile material.
2. Validate that `<topic-workspace-dir>/repos/topic-main` exists as the usable shared non-bare topic repository.
3. Validate each expected `<topic-workspace-dir>/agents/<agent-name>` path as a worktree of `topic-main` on `per-agent/<agent-name>/main` unless a specific future branch is in scope.
4. Check Git worktree metadata for duplicate branch checkout and branches outside the owning `per-agent/<agent-name>/` namespace.
5. Check active role binding `agent_name`, `agent_branch`, and derived compatibility `agent_workspace_ref` values in packet or profile material and reject refs outside the selected Topic Workspace or inside another Research Topic's Topic Workspace.
6. Check `isomer-managed/.gitignore`, `tracked/{shared,artifacts,tasks,runs,views,tools,boundaries,manifests}/`, `agent-owned/{runtime,scratch,logs,artifacts,public,inbox}/`, `topic-owned/{readonly,writable}/`, and `links/`, and report missing paths without creating them silently.
7. Report legacy top-level Topic Main Repository Isomer directories, legacy support roots, missing ignore policy, unsafe links, missing topic-owned writable policy, tracked conflict markers, and owner/reader split issues without deleting, moving, or repairing files.
8. Check that boundary material names write ownership, Peer Read Access, branch rules, generated-link status, topic-owned writable policy when needed, and advisory boundary status when it is expected.
9. Report validation status, ready entries, blockers, deferrals, and next operator action without creating Agent Instances, Workspace Runtime records, Houmao agents, or Execution Adapter material.

If the user's task does not map cleanly to these steps, use your native planning tool to run read-only checks first, then report a partial validation status and missing inputs.

## Validation Status

Use `ready` when Git topology, refs, `isomer-managed/` layout, generated links, and boundary material match the plan. Use `ready-with-deferrals` when nonblocking static notes remain. Use `blocked` for unsafe repo state, missing worktrees, missing required support paths, unsafe generated links, duplicate checkout, unsafe path, cross-topic ref, tracked conflict markers, missing writable policy, owner/reader split issues, or unresolved role mapping.
