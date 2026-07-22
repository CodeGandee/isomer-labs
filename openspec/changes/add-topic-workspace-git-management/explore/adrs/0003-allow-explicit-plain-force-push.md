# Allow Explicit Plain Force Push for Incompatible Publication Branches

One remote repository is dedicated to one Research Topic publication and is expected to be empty initially. Normal synchronization requires absent or compatible publication branches, but when an existing deterministic publication branch is incompatible, the skill may use plain `--force` only after a fresh plan identifies the exact branch, observed remote commit, replacement commit, and commits that will become unreachable, and the user explicitly approves that replacement.

## Status

accepted

## Considered Options

- Use plain `--force` after explicit state-bound permission.
- Use branch-scoped `--force-with-lease` after permission.
- Never force and require external remote cleanup.

## Consequences

- A remote change after approval makes the plan stale and requires a new fetch, plan, warning, and permission even though the eventual command uses plain `--force`.
- Force permission applies only to the deterministic publication branches and exact replacement commits named in the approved plan.
- The skill never uses `--all`, `--mirror`, branch deletion, or force against unrelated branches.
