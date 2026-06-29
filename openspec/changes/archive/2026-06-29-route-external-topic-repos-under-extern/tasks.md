## 1. CLI Behavior

- [x] 1.1 Update `project repos create` so non-main topic repository labels default to `repos/extern/<repo-label-path>`.
- [x] 1.2 Add a guardrail so `project repos create main` and `project repos create topic.repos.main` do not create a conflicting `repos/main` target.
- [x] 1.3 Update CLI examples and tests for the new non-main repository default.

## 2. Documentation and Skills

- [x] 2.1 Update public docs to distinguish `repos/topic-main` from helper-created non-main repositories under `repos/extern/...`.
- [x] 2.2 Update topic environment setup skill references so independent repositories are resolved through semantic `topic.repos.*` paths and default under `repos/extern/...`.
- [x] 2.3 Update operator workspace-manager guidance so additional topic repositories are described as semantic external/supporting repositories, not worktree sources.

## 3. Validation

- [x] 3.1 Update validation fixtures or assertions that still require the old `repos/<repo-name>` default.
- [x] 3.2 Run focused unit tests and OpenSpec status checks for the change.
