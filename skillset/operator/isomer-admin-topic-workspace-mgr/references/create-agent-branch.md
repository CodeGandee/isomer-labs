# Create Agent Branch

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require selected Topic Workspace context, a usable `repos/topic-main`, an `agent-key`, and a requested branch segment.
2. Normalize and validate the agent key using the same rules as `plan-agents`.
3. Validate the requested branch segment and compute `per-agent/<agent-key>/<branch-name>`.
4. Reject branch names outside `per-agent/<agent-key>/`, empty segments, `..`, leading slash, trailing slash, `.lock` endings, and branch names already checked out in another worktree.
5. Create the branch from the requested safe base ref, the agent's default branch, or the repository's base branch according to operator intent.
6. Report branch name, base ref, worktree checkout status, blockers, and next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to validate the requested branch namespace first and stop before mutation if intent is unclear.

## Branch Rules

The default per-agent branch is `per-agent/<agent-key>/main`.

Future branches must live under `per-agent/<agent-key>/<branch-name>`. A request for another agent's prefix is a blocker.
