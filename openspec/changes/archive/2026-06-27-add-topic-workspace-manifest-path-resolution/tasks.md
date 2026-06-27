## 1. Topic Workspace Manifest Model

- [x] 1.1 Add Topic Workspace Manifest data models, parser, serializer helpers, schema version constant, and diagnostics for `topic-workspace.toml`.
- [x] 1.2 Add a bounded semantic surface label catalog with scope, owner, durability, sharing, required-context, command-required label metadata, and compatibility surface metadata.
- [x] 1.3 Add the built-in `isomer-default.v1` layout profile that maps current Topic Workspace and Agent Workspace defaults to semantic labels.
- [x] 1.4 Add manifest-backed path validation for duplicate labels, unsafe paths, unsupported schema versions, Project Config Directory collisions, cross-topic leakage, and unresolved agent path templates.
- [x] 1.5 Add fixtures for missing manifest, valid default materialization manifest, custom topic paths, custom agent workspace templates, duplicate labels, and unsafe bindings.

## 2. Effective Context and Semantic Path Resolution

- [x] 2.1 Load or synthesize Topic Workspace Manifest bindings during Effective Topic Context or path resolver setup without treating the manifest as Project Config Directory state.
- [x] 2.2 Add Effective Agent Context representation with Agent Name, optional Agent Instance id, Agent Workspace path, and source metadata.
- [x] 2.3 Implement agent context resolution precedence: explicit agent selector, supported environment context, cwd-derived Agent Workspace match, then missing-context diagnostic.
- [x] 2.4 Implement cwd Agent Workspace matching against runtime path plans, bounded manifest `agent.workspace` templates with one `{agent_name}` segment, and the default layout profile, while rejecting Topic Main Repository cwd as an Agent Workspace.
- [x] 2.5 Extend Workspace Path Resolution to resolve semantic labels through path plans, environment overrides, Topic Workspace Manifest bindings, Project Manifest defaults where applicable, and default-profile bindings.
- [x] 2.6 Preserve compatibility for existing snake-case path surfaces and map them to semantic labels in new output.
- [x] 2.7 Add conflict diagnostics for explicit, environment, cwd, runtime, and cross-topic agent-context mismatches.

## 3. CLI Path Query and Materialization

- [x] 3.1 Add public CLI support for `project paths get <semantic-label>` with deterministic JSON and text output.
- [x] 3.2 Add public CLI support for `project paths list` with label, scope, required context, resolved status, path, source, and diagnostics.
- [x] 3.3 Update `project paths preview` to include semantic labels and source metadata while preserving existing preview behavior.
- [x] 3.4 Add explicit default-layout materialization behavior that writes or updates `topic-workspace.toml`, creates only selected owned default surfaces, and requires agent context before creating `agent.*` paths.
- [x] 3.5 Add or update CLI options for Agent Name or Agent Instance selection so cross-agent semantic queries are explicit.
- [x] 3.6 Ensure read-only path commands do not create manifests, directories, Workspace Runtime records, Git repositories, branches, or worktrees.

## 4. Workspace Runtime Persistence and Validation

- [x] 4.1 Add first-class PathPlanRecord `semantic_label` and `scope_ref` fields, preserving compatibility with existing path plan rows and compatibility surface ids.
- [x] 4.2 Update Workspace Runtime initialization to resolve command-scoped required runtime paths through semantic labels and store source metadata.
- [x] 4.3 Update Agent Team Instance creation to resolve `agent.workspace` and required agent support labels before creating Agent Workspace records.
- [x] 4.4 Update runtime inspection to report semantic labels, compatibility surface ids, path sources, and source detail for path plans.
- [x] 4.5 Add runtime validation for manifest drift, missing current semantic bindings, unsafe manifest-backed plans, and cross-topic semantic path leakage.
- [x] 4.6 Ensure validation preserves historical path plans and never silently rewrites, moves, deletes, or rebinds dependent runtime records.

## 5. Documentation and Domain Language

- [x] 5.1 Update the canonical domain language to define Topic Workspace Manifest, semantic workspace surface labels, default layout profile, and Effective Agent Context.
- [x] 5.2 Update Topic Workspace documentation so semantic labels are the contract and default directories are described as `isomer-default.v1` bindings.
- [x] 5.3 Keep Directory Meanings as Markdown nested lists or prose rather than a table-only presentation.
- [x] 5.4 Update `docs/isomer-cli.md`, getting started, runtime files, concepts, and assumptions docs for `paths get`, `paths list`, materialization side effects, cwd-derived agent inference, and selector precedence.
- [x] 5.5 Update docs validation to detect stale fixed-path-only wording, missing semantic path command coverage, and future `tmp/` wording that bypasses semantic labels.

## 6. Operator and Service Skill Guidance

- [x] 6.1 Update `isomer-admin-topic-workspace-mgr` entrypoint and reference pages to resolve, create, validate, and summarize Topic Main Repository and Agent Workspaces through semantic labels.
- [x] 6.2 Update topic workspace manager output expectations to report labels, paths, sources, readiness, blockers, branch plans, and cwd-friendly self-query guidance.
- [x] 6.3 Update `isomer-admin-topic-team-specialize` setup, validation, and final summary guidance to consume delegated semantic workspace evidence.
- [x] 6.4 Update `isomer-srv-topic-env-setup` guidance to resolve setup gates, repositories, Pixi surfaces, and any agent-scoped targets through semantic labels.
- [x] 6.5 Update skillset validation tests and required terms so the skills reject hard-coded default-only workspace evidence where semantic labels are required.

## 7. tmp Change Alignment

- [x] 7.1 Update or supersede `openspec/changes/add-local-tmp-workspace-surfaces` so `tmp/` is expressed as semantic labels such as `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp`.
- [x] 7.2 Ensure the downstream `tmp/` change depends on this manifest-backed semantic path model before implementation.
- [x] 7.3 Preserve the `tmp/` semantics that it is local, ignored, disposable, not shared, and not durable evidence.

## 8. Tests and Verification

- [x] 8.1 Add unit tests for Topic Workspace Manifest parsing, default-profile synthesis, semantic label classification, and path safety diagnostics.
- [x] 8.2 Add unit tests for semantic path resolution precedence, compatibility surface aliases, and missing required label diagnostics.
- [x] 8.3 Add unit tests for cwd-derived Effective Agent Context, including runtime match, bounded manifest-template match, unsupported template diagnostics, default-layout match, Topic Main Repository non-match, and conflict cases.
- [x] 8.4 Add CLI tests for `paths get`, `paths list`, `paths preview`, explicit agent selector behavior, and read-only non-mutation.
- [x] 8.5 Add runtime tests for semantic path-plan persistence, Agent Workspace creation, manifest drift diagnostics, and historical path-plan preservation.
- [x] 8.6 Add docs and skill validation tests for semantic label wording, Directory Meanings nested lists, and downstream `tmp/` label posture.
- [x] 8.7 Run `openspec validate add-topic-workspace-manifest-path-resolution --strict`.
- [x] 8.8 Run `pixi run docs-validate`, `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
