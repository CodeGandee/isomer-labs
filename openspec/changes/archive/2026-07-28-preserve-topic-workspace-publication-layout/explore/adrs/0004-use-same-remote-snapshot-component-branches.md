# Use Same-Remote Snapshot Branches for the Topic Main Worktree Family

Topic Main is the Git anchor for Topic Actor Workspace and Agent Workspace worktrees in the Source Topic Workspace, but publication cannot retain their machine-local Git worktree control links. Publication will represent Topic Main and each selected worktree snapshot as same-remote submodules at their resolved Topic Workspace-relative paths, with exact sanitized commits reachable from replaceable `components/...` branches. The Publication Projection Manifest records each worktree snapshot's Topic Main anchor relationship, while registered third-party repositories remain exact-commit submodules of their credential-free upstream GitHub repositories.

## Status

accepted

## Considered Options

- Use same-remote `components/...` snapshot branches and record the Topic Main worktree-family relationship.
- Reuse source-style branches such as `topic-owner/main`.
- Create a separate publication repository for every topic-owned component.
- Flatten topic-owned repository files into superproject `main`.
- Publish only Topic Main and require a setup operation before actor or agent paths become visible.

## Consequences

- One publication remote contains the root snapshot, Topic Main snapshot, and every selected Topic Actor Workspace or Agent Workspace snapshot.
- Component branches carry reachability, not source ownership or historical meaning.
- Every sync may replace component branch commits under the exclusive-snapshot authority.
- Superproject `main` pins exact component commits through gitlinks at their original Topic Workspace paths.
- Recursive clone requires component refs to be published before `main`.
- A recursive clone materializes ordinary submodule checkouts rather than linked worktrees, and it never publishes source `.git` files or worktree administration data.
- The publication is an inspectable current-state snapshot, not a backup or an automatically restorable Topic Workspace. Any later recreation of operational directories, Artifacts, gitlinks, or worktrees is manual and outside the publication contract.
