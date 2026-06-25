## Context

`isomer-cli project init` currently creates a Project Manifest, a generated content root, a Research Topic Config, and a Topic Workspace in one operation. The CLI accepts a positional topic id, `--topic-id`, and `--topic-statement`; if no topic id is supplied it creates a registered `default` topic and `isomer-content/topic-ws/default/`. This makes Project bootstrap and Research Topic creation inseparable, and it allows an operator agent to fill the topic id from the Project or repository name.

The desired model is an empty Project registry after bootstrap. Project init establishes `.isomer-labs/`, the Project Manifest, the generated content root policy files, and the Isomer-managed Houmao overlay. Research Topic lifecycle then lives under `isomer-cli project topics ...`, with explicit topic creation and plan-first destructive behavior.

## Goals / Non-Goals

**Goals:**

- Make `project init` unable to initialize, infer, or register any Research Topic.
- Add explicit topic CRUD surfaces for registration, inspection, metadata updates, and deletion planning/application.
- Allow a Project Manifest with zero Research Topics to be valid for Project-scoped commands.
- Keep topic-scoped commands strict: they fail clearly when no registered topic exists or when a selected topic is missing.
- Preserve generated content-root behavior and path defaults so later topic creation can derive `isomer-content/topic-ws/<topic-id>/` or `<content-dir>/topic-ws/<topic-id>/`.
- Update operator skills and docs so agents never pass a Project name as a topic id during Project initialization.

**Non-Goals:**

- Do not implement topic id rename in the first CRUD surface.
- Do not create Workspace Runtime state from topic CRUD commands.
- Do not launch, prepare, or inspect live Houmao agents from topic CRUD commands.
- Do not silently delete Topic Workspace contents during topic deletion.
- Do not infer Research Topics from directories, filenames, repository names, or topic overview material.

## Decisions

### Decision: Project init writes an empty Project registry

`isomer-cli project init` will write a manifest containing schema version and `[paths]` defaults only. It will not write `[defaults].research_topic_id`, `[defaults].topic_workspace_id`, `[[research_topics]]`, or `[[topic_workspaces]]`. It will create the selected generated content root with `README.md` and `.gitignore`, but it will not create `topic-ws/<topic-id>/`.

Alternative considered: keep a synthetic `default` topic and mark it provisional. This preserves old tests but keeps the accidental-topic problem alive. A Project name or placeholder remains too easy to treat as user intent.

### Decision: Topic creation is explicit and statement-bearing

`isomer-cli project topics create <topic-id> --statement "<research topic>"` will be the authoritative mutation for new topics. It writes `.isomer-labs/research-topics/<topic-id>.toml`, adds `[[research_topics]]`, adds the associated `[[topic_workspaces]]`, and creates the Topic Workspace directory. If `--workspace-dir <dir>` is omitted, the workspace path derives from Project Manifest `topic_workspace_base_dir`, otherwise from the built-in generated content layout.

Alternative considered: let `init-topic` in the operator skill hand-edit the manifest after writing `topic-overview.md`. This would duplicate authority outside the CLI and weaken cleanup and validation safety.

### Decision: Project-scoped commands accept empty topic registries

Manifest parsing and validation will no longer treat zero `[[research_topics]]` as an error. Project-scoped commands such as `validate`, `doctor`, `topics list`, `workspaces list`, and content-root relocation can run on an empty Project. Topic-scoped commands still resolve Effective Topic Context and report a diagnostic when no topic can be selected.

Alternative considered: create a separate "uninitialized Project" schema state. That adds complexity without a clear benefit because an empty registry is a natural Project state.

### Decision: Topic deletion is plan-first and preserves workspace contents

`topics delete <topic-id> --dry-run` will report the manifest updates, Research Topic Config removal, default clearing, dependent registrations, runtime/profile blockers, and preserved workspace path. `--yes` applies the reviewed plan. The first implementation will not physically remove Topic Workspace directories; users who want filesystem removal must use supported cleanup surfaces after reviewing the preserved path.

Alternative considered: make deletion remove the workspace automatically. That is too destructive for a command that primarily edits Project registrations and config.

### Decision: Updates are conservative

`topics update <topic-id>` can update topic statement, measurable objectives, status, and default selection. It will not rename topic ids. Renaming can be added later with a separate plan-first command because ids may appear in Topic Agent Team Profiles, Workspace Runtime records, adapter material, launch material, and logs.

Alternative considered: include rename in CRUD now. It would broaden the migration surface and delay the core fix.

### Decision: Operator skills use CLI boundaries for authoritative registration

`isomer-admin-project-mgr init-project` will describe Project-only init and direct topic creation to `isomer-cli project topics create`. `isomer-admin-topic-team-specialize init-topic` may continue to create provisional topic material from a user-supplied Research Topic, but when the topic must become authoritative it must route through `project topics create` rather than editing `.isomer-labs/manifest.toml`.

Alternative considered: merge Project Manager and Topic Team Specialization into one lifecycle skill. Keeping them separate preserves the existing boundary between Project lifecycle and topic-team static material production.

## Risks / Trade-offs

- [Risk] Existing tests and docs assume `project init` creates `default`. -> Mitigation: update tests and docs together with the CLI contract, and add explicit tests for empty Project manifests.
- [Risk] Commands that assume at least one topic may fail with low-level errors. -> Mitigation: audit `default_research_topic_id`, single-topic fallback, workspace listing, cleanup topic selection, and Effective Topic Context resolution paths.
- [Risk] Topic deletion can break profiles or runtime records if it unregisters a topic too freely. -> Mitigation: make delete plan-first and block or warn on dependent Topic Agent Team Profiles, team instances, runtime records, and adapter material.
- [Risk] Users may expect `project init --topic-id` from old docs or muscle memory. -> Mitigation: reject removed topic init options with deterministic diagnostics that name `isomer-cli project topics create`.
- [Risk] A topic create command without a clear statement could recreate placeholder topics. -> Mitigation: require a non-placeholder statement and reject generic values such as empty strings, `default Research Topic`, or a statement derived only from the Project name.

## Migration Plan

1. Change Project Manifest parsing to allow zero Research Topics and adjust validation for empty registries.
2. Remove topic arguments and topic file/workspace creation from Project init.
3. Add `project topics create`, `show`, `update`, and `delete` command handlers and tests.
4. Update topic context resolution and topic-scoped command tests for empty Project diagnostics.
5. Update docs, specs, and operator skills to use the new two-step flow: Project init first, topic create second.
6. Leave existing Projects with registered topics valid; no automatic migration is needed.

Rollback is straightforward before users adopt the new command surface: restore old Project init topic creation and re-enable the parser requirement for at least one Research Topic. After adoption, rollback would require preserving `topics create` or providing equivalent migration guidance.

## Open Questions

None for the first implementation. `topics create` sets Project defaults only when the user passes `--set-default`, `topics delete` preserves workspace directories and reports cleanup guidance, and `topics update` is limited to statement, status, and default selection.
