## 1. CLI Package Skeleton

- [x] 1.1 Add `[project.scripts]` metadata so `isomer-cli` invokes the package CLI entrypoint.
- [x] 1.2 Create the Milestone 1 module structure under `src/isomer_labs/` for CLI orchestration, Project discovery, manifest parsing, topic config loading, Effective Topic Context, Workspace Path Resolution, validation, diagnostics, and built-ins.
- [x] 1.3 Implement `click` command wiring for `init`, `validate`, `topics list`, `workspaces list`, `context show`, `paths preview`, and `schemas list`.
- [x] 1.4 Add plain text and JSON rendering helpers shared by all commands.

## 2. Project Files and Models

- [x] 2.1 Define typed models for Project, Project Config Directory, Project Manifest, Research Topic registration, Topic Workspace registration, Research Topic Config, local active context, Effective Topic Context, resolved path entries, and diagnostics.
- [x] 2.2 Implement TOML loading helpers that preserve source path metadata and return structured diagnostics for malformed files.
- [x] 2.3 Implement Project discovery from explicit Project or Project Manifest selectors, current directory ancestor search, and supported Project environment overrides.
- [x] 2.4 Implement Project Manifest parsing for Research Topic registrations, Topic Workspace registrations, defaults, schema version fields, and optional artifact format or extension registrations needed by Milestone 1 validation.
- [x] 2.5 Implement Research Topic Config parsing for topic statement fields, Measurable Objective fields, default refs, extension refs, policy refs, artifact format defaults, and artifact extension refs.

## 3. Initialization

- [x] 3.1 Implement `isomer-cli init` for a default one-topic Project.
- [x] 3.2 Ensure no-argument `init` creates Research Topic id `default`, `.isomer-labs/research-topics/default.toml`, and `topic-workspaces/default/`.
- [x] 3.3 Add explicit topic id support for `init` and use that id consistently in the Research Topic registration, Research Topic Config path, and Topic Workspace directory.
- [x] 3.4 Ensure `init` refuses to overwrite an existing Project Manifest and does not expose a force-overwrite behavior.
- [x] 3.5 Ensure `init` does not create `state.sqlite` or Workspace Runtime directories beyond the Topic Workspace directory anchor.

## 4. Validation

- [x] 4.1 Implement duplicate id checks for Research Topic and Topic Workspace registrations.
- [x] 4.2 Validate Research Topic Config paths are project-scoped and registered by the Project Manifest, with no external-root allowlist in Milestone 1.
- [x] 4.3 Validate each Research Topic Config `research_topic_id` matches the Research Topic registration that referenced it.
- [x] 4.4 Validate Topic Workspace refs and built-in defaults for registered Research Topics.
- [x] 4.5 Reject runtime truth fields from Research Topic Config and `.isomer-labs/local.toml`.
- [x] 4.6 Reject inline secret-like fields from Project Manifest, Research Topic Config, and `.isomer-labs/local.toml` without printing secret values.
- [x] 4.7 Implement stable diagnostic codes, severity, file path, concept name, and message rendering.

## 5. Topic Context Resolution

- [x] 5.1 Implement topic selection precedence from explicit selectors, current-directory Topic Workspace selection, supported identity environment refs, `.isomer-labs/local.toml`, and Project Manifest defaults.
- [x] 5.2 Validate local active context contains only allowed candidate identity refs and schema version fields.
- [x] 5.3 Detect and report ambiguous or conflicting Research Topic, Topic Workspace, Research Task, Run, Agent Team Instance, Agent Instance, and Topic Agent Team Profile refs.
- [x] 5.4 Implement `context show` with text and deterministic JSON output for selected refs, schema versions, and source metadata.
- [x] 5.5 Report optional lifecycle refs that cannot yet be validated without Workspace Runtime support as bounded Milestone 1 diagnostics rather than silently accepting them.

## 6. Workspace Path Preview

- [x] 6.1 Implement built-in default paths for Topic Workspace root, `state.sqlite`, `artifacts/`, `agents/`, `tasks/`, `runs/`, `views/`, and `logs/`.
- [x] 6.2 Implement supported `ISOMER_*` path override handling for Project, Topic Workspace, Topic Workspace subdirectories, and Agent Workspace surfaces.
- [x] 6.3 Implement path precedence reporting for environment, Project Manifest, and built-in default sources.
- [x] 6.4 Ensure `paths preview` does not report any resolved path as coming from a recorded plan source in Milestone 1.
- [x] 6.5 Canonicalize resolved paths and reject paths outside the Project root with no external-root allowlist in Milestone 1.
- [x] 6.6 Implement `paths preview` with text and deterministic JSON output.
- [x] 6.7 Verify `paths preview` is side-effect free and does not create Workspace Runtime files or default subdirectories.

## 7. Listing and Built-Ins

- [x] 7.1 Implement `topics list` from Project Manifest registrations only.
- [x] 7.2 Implement `workspaces list` from Project Manifest registrations and valid built-in defaults.
- [x] 7.3 Ensure unregistered files under `.isomer-labs/research-topics/` are ignored by `topics list`.
- [x] 7.4 Implement `schemas list` for Milestone 1 Isomer built-in schema and contract names without copying schema files into `.isomer-labs/`.
- [x] 7.5 Ensure `schemas list` does not include OpenSpec capability names, active change names, or planning artifact names by default.

## 8. Tests and Validation

- [x] 8.1 Add unit-test fixtures or temp-project builders for valid Project, missing Project, malformed manifest, duplicate ids, mismatched topic config, external paths, local active context, and environment selector cases.
- [x] 8.2 Test CLI help and installed script behavior through the package entrypoint.
- [x] 8.3 Test `init` file creation and non-overwrite behavior.
- [x] 8.4 Test `validate`, `topics list`, `workspaces list`, `context show`, `paths preview`, and `schemas list` text and versioned JSON behavior.
- [x] 8.5 Test secret diagnostics do not include secret values.
- [x] 8.6 Run `pixi run lint`, `pixi run typecheck`, `pixi run test`, and `pixi run validate-research-skills`.

Validation note: `pixi run lint`, `pixi run typecheck`, `pixi run test`, and `pixi run validate-research-skills` pass after excluding `teams/lfeng-team` from Ruff scans.

## 9. Documentation and Roadmap

- [x] 9.1 Update README or developer notes with the Milestone 1 `isomer-cli` command examples.
- [x] 9.2 Mark completed Milestone 1 roadmap checklist items only after the implementation and tests pass.
- [x] 9.3 Keep existing design docs unchanged unless implementation discovers a spec or architecture mismatch that needs a follow-up OpenSpec change.
