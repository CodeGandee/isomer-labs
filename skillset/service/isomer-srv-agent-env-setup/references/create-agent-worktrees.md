# Create Agent Worktrees

Use this subcommand to create or validate each Agent Workspace as a Git worktree of the Topic Main Repository and prepare required support surfaces.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Agent env context | Require resolved Topic Workspace, `topic.main_repo`, `topic.agents_root`, requester, and confirmation source. |
| Agent plan | Require `plan-agent-workspaces` output with authoritative Agent Names, resolved `agent.workspace`, support labels, path sources, and branch plan. |
| Topic Main Repository state | Require `ensure-topic-main-repository` output with a normal non-bare repository and owner branch posture. |
| Derived agent env gate | Require `user-intent/derived/isomer-agent-env-gate.md` so worktree status can be recorded. |
| Optional selected agent | Optional. It must be one authoritative Agent Name and yields partial setup evidence only. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**: resolved context, authoritative agent plan, usable Topic Main Repository state, derived agent env gate, and mutation confirmation.
2. **Inspect Git worktree metadata** for the resolved `topic.main_repo` before creating any worktree.
3. **For each targeted authoritative Agent Name**, validate the expected branch `per-agent/<agent-name>/main` and resolved `agent.workspace` path.
4. **Report existing matching worktrees as ready** when the resolved `agent.workspace` path already exists as a worktree of `topic.main_repo` on the expected branch.
5. **Block existing nonmatching paths**. Do not overwrite, delete, move, clean, reset, or reinitialize an existing path that is not the expected worktree.
6. **Reject duplicate branch checkout** when `per-agent/<agent-name>/main` is already checked out in another worktree of the Topic Main Repository.
7. **Create missing safe worktrees** only for authoritative Agent Names and safe resolved paths. Use the Topic Main Repository as the Git anchor and the resolved `agent.workspace` path as the Agent Workspace path.
8. **Prepare or validate required support labels** for each ready worktree: `agent.isomer_managed`, `agent.runtime`, `agent.private_artifacts`, `agent.scratch`, `agent.logs`, `agent.public_share`, `agent.inbox`, `agent.topic_readonly`, `agent.topic_writable`, and `agent.links`. Include `agent.tmp` only as local ignored disposable posture when available.
9. **Write or validate advisory boundary material** naming cwd-friendly self-query guidance, Peer Read Access, owner/reader split, branch rules, and the fact that cwd inference is not filesystem-grade identity or access control.
10. **Update or report derived gate worktree evidence** with branch plan, worktree status by agent, support label posture, changed files, commands run, blockers, and selected-agent partial scope when present.

If the user's task does not map cleanly to these steps, use your native planning tool to inspect first, separate ready entries from blocked entries, and mutate only entries that are safe.

## Safety Rules

- Use idempotent Git worktree operations.
- Do not select agents by scanning existing directories.
- Do not create a worktree outside the selected Topic Workspace unless a later accepted external-root policy explicitly permits the semantic label.
- Do not create worktrees for unsafe Agent Names, unsafe branch names, unsafe custom semantic bindings, or branches checked out elsewhere.
- Do not describe tmp or private runtime material as a sharing surface.
- Do not claim Agent Workspace environment readiness until `verify-agent-env-gate` passes from cwd.
