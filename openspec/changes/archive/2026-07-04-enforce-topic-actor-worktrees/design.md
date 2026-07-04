## Context

Topic Actor Workspace surfaces already use `topic_actor_worktree` semantics, and the specs already identify `topic.repos.main` as the Git anchor for actor workspaces. The current materializer creates a Git worktree only when the actor workspace path is missing; if the path already exists, it can report readiness without proving the path is the expected worktree or branch.

Formal Agent Workspace setup already has the stricter behavior needed here: inspect existing worktree metadata, accept matching worktrees, block nonmatching paths, and block duplicate branch checkouts. Topic Actors should follow that same topology rule while keeping their separate actor identity, manual controller model, and `per-topic-actor/<topic-actor-name>/main` branch namespace.

## Goals / Non-Goals

**Goals:**

- Make `actors-materialize`, actor diagnostics, and creator/manual actor readiness treat a matching topic-main worktree as required evidence.
- Preserve existing filesystem content by blocking on nonmatching actor workspace paths instead of overwriting, moving, cleaning, resetting, or reinitializing them.
- Keep actor workspace support labels under the actor workspace after worktree readiness is confirmed.
- Report worktree source, branch, path, readiness, blockers, and next action consistently across actor materialization and diagnostics.

**Non-Goals:**

- Do not introduce alternate actor workspace source repositories.
- Do not merge Topic Actor identity with formal Agent Workspace identity.
- Do not launch or manage human-controlled actors through Houmao.
- Do not migrate existing non-worktree actor directories automatically.

## Decisions

- Reuse the agent worktree validation pattern for Topic Actor Workspaces. The materializer should inspect `git -C <topic-main> worktree list --porcelain`, compare the resolved actor workspace path and expected branch, and accept only an exact match or a missing path that can be safely created.
- Treat missing or non-Git `topic.repos.main` as a blocker for worktree-backed readiness. A placeholder actor directory does not satisfy the `topic_actor_worktree` contract and must not be reported as ready.
- Keep branch names deterministic with `actor.effective_branch`, defaulting to `per-topic-actor/<topic-actor-name>/main`. If that branch is checked out in another worktree of topic-main, actor materialization reports a blocker instead of force-moving the branch.
- Make diagnostics use the same worktree inspection helper as materialization. This prevents `actors-diagnose` and `actors-materialize` from disagreeing about actor readiness.
- Materialize actor support paths only after the actor workspace is created or validated as the expected worktree. This keeps actor-local Isomer support files inside the correct repository checkout.

## Risks / Trade-offs

- Existing plain actor directories become blocked until an operator migrates or removes them. Mitigation: diagnostics should identify the path, expected source, expected branch, and safe next action.
- Git worktree inspection can be brittle if paths differ by symlink or relative spelling. Mitigation: compare resolved paths with `Path.resolve(strict=False)` and include raw Git evidence in diagnostics when useful.
- Requiring a real topic-main repository may expose earlier topic setup gaps. Mitigation: actor materialization should point to topic environment setup or topic-main repair as the predecessor.

## Migration Plan

1. Add worktree inspection and validation to actor materialization and diagnostics.
2. Update actor setup skills and readiness text so they require matching worktree evidence.
3. Add tests for missing workspace creation, existing matching worktree reuse, existing nonmatching path blocker, duplicate branch checkout blocker, and non-Git topic-main blocker.
4. For existing topics with plain actor directories, operators can rename or archive the old directory, then rerun actor materialization to create the correct worktree.

## Open Questions

- None.
