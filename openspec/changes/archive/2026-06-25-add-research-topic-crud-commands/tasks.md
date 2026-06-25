## 1. Project Initialization Contract

- [x] 1.1 Remove positional `<topic-id>`, `--topic-id`, and `--topic-statement` from `isomer-cli project init` registration and command handling, returning deterministic diagnostics for old topic-init forms.
- [x] 1.2 Refactor `initialize_project` so Project init writes only Project config, path defaults, content-root policy files, and the Isomer-managed Houmao overlay, with no Research Topic Config or Topic Workspace directory.
- [x] 1.3 Update Project Manifest rendering so a fresh Project contains schema version and `[paths]` defaults but no topic defaults, `[[research_topics]]`, or `[[topic_workspaces]]`.
- [x] 1.4 Preserve `--content-dir <content-dir>` validation and manifest path defaults while ensuring custom init does not create `<content-dir>/topic-ws/<topic-id>/`.

## 2. Empty Registry Validation and Context

- [x] 2.1 Relax Project Manifest parsing so zero Research Topics is valid.
- [x] 2.2 Audit Project validation paths so project-scoped commands succeed against an empty topic registry.
- [x] 2.3 Update Effective Topic Context resolution so topic-scoped commands in an empty Project return a clear diagnostic that the user must create a Research Topic with `isomer-cli project topics create`.
- [x] 2.4 Update topic and workspace list output so empty Projects report empty lists without errors.

## 3. Research Topic CRUD Implementation

- [x] 3.1 Add CLI command registrations for `isomer-cli project topics show`, `create`, `update`, and `delete` while preserving `topics list`.
- [x] 3.2 Implement `topics create <topic-id> --statement "<research topic>" [--workspace-dir <dir>] [--set-default]` with id validation, statement validation, duplicate checks, workspace path validation, manifest update, config file creation, and workspace directory creation.
- [x] 3.3 Implement `topics show <topic-id>` to report topic registration, config data, associated workspace registration, effective workspace path, status, and diagnostics.
- [x] 3.4 Implement `topics update <topic-id>` for statement, status, and `--set-default`, while refusing topic rename through this command.
- [x] 3.5 Implement `topics delete <topic-id> --dry-run` and `--yes` with plan output, dependent-material blockers, config removal, registration removal, default clearing, workspace preservation, and cleanup guidance.
- [x] 3.6 Add shared helpers for safe Project Manifest rewriting so topic CRUD mutations are atomic enough for the current file-based manifest model.

## 4. Tests

- [x] 4.1 Update Project init unit tests to assert no topic config, no topic workspace, no topic defaults, and no topic registrations are created.
- [x] 4.2 Add unit tests for rejected old Project init topic arguments and topic options.
- [x] 4.3 Add unit tests for `topics create` default workspace, custom workspace, duplicate rejection, invalid statement rejection, invalid path rejection, and `--set-default`.
- [x] 4.4 Add unit tests for `topics list` and `topics show` in empty, registered, and missing-topic cases.
- [x] 4.5 Add unit tests for `topics update` statement, status, default selection, and rename refusal.
- [x] 4.6 Add unit tests for `topics delete --dry-run`, missing confirmation, confirmed deletion, workspace preservation, default clearing, and dependent-material blockers.
- [x] 4.7 Add context-resolution tests for empty Project diagnostics on topic-scoped commands and success on project-scoped commands.

## 5. Documentation and Operator Skills

- [x] 5.1 Update CLI docs, getting started docs, workflows, runtime/files docs, troubleshooting, and system design text to describe Project-only init and explicit topic CRUD.
- [x] 5.2 Update `isomer-admin-project-mgr` skill guidance, help, command boundaries, project concepts, runtime boundaries, and validation fixtures to remove topic creation from Project init and document `project topics create`.
- [x] 5.3 Update `isomer-admin-topic-team-specialize` guidance so authoritative topic registration routes through `isomer-cli project topics create` and Project init is never suggested for topic creation.
- [x] 5.4 Update operator skill validation requirements and fixture tests for the new Project init and topic CRUD wording.

## 6. Validation

- [x] 6.1 Run `openspec validate add-research-topic-crud-commands --strict`.
- [x] 6.2 Run `openspec validate --specs --strict`.
- [x] 6.3 Run `pixi run lint`.
- [x] 6.4 Run `pixi run typecheck`.
- [x] 6.5 Run `pixi run test`.
- [x] 6.6 Run `pixi run validate-operator-skills`.
