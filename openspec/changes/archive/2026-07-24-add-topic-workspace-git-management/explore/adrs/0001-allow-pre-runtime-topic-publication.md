# Allow Topic Publication Before Workspace Runtime Exists

Remote publication may start as soon as a Research Topic and its Topic Workspace are registered, while local root Git mutations require a valid Workspace Runtime. Before Workspace Runtime exists, publication state lives only in the ignored Topic Publication Copy; a later approved publication mutation records the credential-safe binding under `<topic.runtime>/topic-git/` after runtime becomes available. This keeps publication available at every post-registration stage without letting Topic Git initialize Workspace Runtime or introduce another canonical state file at the Topic Workspace root.

## Status

accepted

## Considered Options

- Store pre-runtime publication state in the ignored Topic Publication Copy, then bind it into Workspace Runtime later.
- Create `<topic.runtime>/topic-git/` before `state.sqlite` exists.
- Add a dedicated publication-state file at the Topic Workspace root.

## Consequences

- Losing an unpushed pre-runtime Topic Publication Copy loses its local publication plan, which must be prepared again.
- After a successful pre-runtime push, sanitized remote manifests can support reconstruction when the user supplies the remote again.
- Topic Git never initializes Workspace Runtime and never treats creation of a publication copy as runtime readiness.
