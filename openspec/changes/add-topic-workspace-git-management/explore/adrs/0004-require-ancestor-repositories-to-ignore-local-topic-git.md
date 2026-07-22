# Require Ancestor Repositories to Ignore Local Topic Git

Before `local init`, every ancestor Git repository must treat the Source Topic Workspace as untracked and effectively ignored. Topic Git reports tracked or unignored ancestor state as a prerequisite failure and never edits an ancestor `.gitignore`, removes ancestor index entries, or otherwise repairs the enclosing repository.

## Status

accepted

## Considered Options

- Require untracked and effectively ignored ancestor state without mutating the ancestor.
- Let Topic Git add an approved managed ignore rule to the ancestor repository.
- Permit unignored but untracked Topic Workspaces with a warning.

## Consequences

- Local tracking remains scoped to the Source Topic Workspace.
- Users may need a separate Project repository operation before local tracking can begin.
- Ancestor ignore checks use effective Git evidence rather than `.gitignore` text matching alone.
