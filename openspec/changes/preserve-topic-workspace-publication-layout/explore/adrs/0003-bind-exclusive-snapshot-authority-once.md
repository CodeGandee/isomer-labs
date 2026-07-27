# Bind Exclusive Snapshot Authority Once

Publication initialization will require one explicit acknowledgement that the selected remote is dedicated exclusively to the current sanitized snapshot of one Topic Workspace. The resulting Publication Binding authorizes later approved syncs to force-replace or delete Git refs and tags across that remote without repeated branch-specific destructive approvals; content selection, privacy, remote inventory, and stale-plan checks remain current-plan requirements.

## Status

accepted

## Considered Options

- Persist exclusive-snapshot authority in the Publication Binding.
- Ask before each whole-repository replacement.
- Ask separately for every branch or tag replacement.

## Consequences

- Changing the remote identity, Topic Workspace identity, or snapshot mode requires a new explicit acknowledgement.
- A fresh synchronization plan inventories the complete remote ref and tag set before mutation.
- Remote changes after planning stale the plan rather than being overwritten from stale evidence.
- Manually added Git refs or tags are subject to deletion on the next approved sync.
- Provider settings and non-Git repository data are outside this Git snapshot authority unless another decision includes them.
