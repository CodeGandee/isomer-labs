## Context

The current extension package model is named with plugin terminology across CLI commands, TOML tables, schema versions, callback registry metadata, Python data models, OpenSpec specs, docs, tests, and the project-local GPU analytical modeling package. Recent runtime parameter work made this model broader than a narrow callback plugin: it now covers installation status, callback manifest identity, runtime parameter definitions, imported default bundles, Project Manifest configuration, Topic Workspace Manifest configuration, and agent/actor specialization.

This change is a breaking domain-language and durable-schema rename. The target product language is Toolbox. After the change, current behavior, docs, specs, and persisted schema use Toolbox names rather than preserving the old term as a compatibility concept.

## Goals / Non-Goals

**Goals:**

- Make Toolbox the public and durable name for the project-local extension package concept.
- Rename the manifest tables, schema versions, JSON keys, callback registry metadata, CLI groups, CLI options, docs, specs, tests, and example package path to Toolbox terms.
- Move the GPU analytical modeling package to `skillset/toolboxes/gpu-analytical-modeling`.
- Keep the existing semantics: project scope, topic scope, Topic Actor specialization, Topic Agent specialization, imported defaults, explicit overrides, callback install, callback ordering, and callback gating.
- Fail clearly when users provide the old command names, table names, schema versions, or field names after the breaking rename.

**Non-Goals:**

- No legacy parser, command alias, deprecation warning, migration command, or dual-written manifest support is introduced by this change.
- No change to callback execution authority, skill callback safety, runtime parameter value types, or topic path binding semantics beyond the rename.
- No broad redesign of Toolboxes as a marketplace, package manager, dependency system, or executable extension runtime.

## Decisions

1. Toolbox is the canonical domain term.

   The canonical domain language will define a Toolbox as a user-managed, project-local extension package that can provide skill callbacks, runtime parameter declarations, default parameter bundles, and future Toolbox-owned instruction material. The implementation should avoid retaining the old concept name in current user-facing strings, schema names, tests, docs, or spec requirements.

2. Durable schema names move with the public language.

   Project Manifest and Topic Workspace Manifest rows become `[[toolboxes]]`, `[[toolbox_runtime_param_imports]]`, and `[[toolbox_runtime_params]]`. The stable identity field becomes `toolbox_id`; callback manifest local callback identifiers become toolbox-local keys; callback registry source metadata uses Toolbox names. Runtime parameter ids remain two-part ids, now rendered as `<toolbox_id>:<param-key>`.

3. CLI names are replaced, not aliased.

   `isomer-cli project toolboxes` replaces `project user-plugins`, and `isomer-cli project toolbox-params` replaces `project user-plugin-params`. `project toolboxes install --toolbox-dir <path>` and `project skill-callbacks install --toolbox-dir <path>` derive `toolbox_id` from the Toolbox manifest. Commands that operate on an already-known Toolbox, such as show, explain, enable, disable, update-source, and uninstall, remain id-based. Help text, examples, JSON command summaries, and diagnostics should expose only Toolbox wording.

4. Existing semantic behavior stays intact.

   The implementation should preserve current scope behavior: Project Manifest rows are project-scoped, Topic Workspace Manifest rows may target Research Topic, Topic Actor, or Topic Agent scope, imports resolve relative to the manifest file that declares them, and effective values resolve in the established order: project imports, project explicit rows, topic imports, topic explicit rows.

5. Example package paths move.

   The GPU analytical modeling package moves from `skillset/user-plugins/gpu-analytical-modeling` to `skillset/toolboxes/gpu-analytical-modeling`. Specs and docs that previously constrained package-only changes must be updated because this rename intentionally changes CLI/runtime/schema surfaces too.

6. Rejection is explicit.

   Old table names, field names, command names, callback manifest schema versions, callback bundle kinds, and callback registry metadata are invalid after this change. Parsers and validators should produce deterministic diagnostics instead of silently ignoring old material.

7. Toolbox source fields are context-sensitive.

   A `[[toolboxes]]` row uses `source_path` because the table already supplies the Toolbox context. Cross-record callback registry metadata uses explicit Toolbox names such as `toolbox_source_path_input`.

## Risks / Trade-offs

- Existing projects with old manifests break immediately → This is intentional for the change; tests should assert deterministic diagnostics for old table names and fields so failures are clear.
- Renaming Python modules and dataclasses is noisy → Keep edits mechanical and scoped; update architecture transition tests and imports in the same implementation pass.
- Callback registry records and manifest rows must change together → Update install, resolve, list, show, validate, and gating tests together so mixed metadata does not silently pass.
- OpenSpec archive may leave old capability directories if removal deltas are incomplete → Include removal deltas for old capability requirements and new Toolbox capability specs for the target contract.
- Search hygiene can be difficult because archived change history still contains old wording → Treat active code, docs, specs, tests, and example packages as the target surface; archived historical artifacts may remain historical unless a later repository-cleanup change rewrites them.

## Migration Plan

1. Rename current OpenSpec requirements to the Toolbox contract, removing old capability requirements where the capability itself is replaced.
2. Update canonical domain language, docs, and example package paths to use Toolbox terminology.
3. Rename Python modules, dataclasses, parser functions, manifest model fields, TOML renderers, CLI option fields, and handlers from the old names to Toolbox names.
4. Replace CLI groups and options with `project toolboxes`, `project toolbox-params`, and `--toolbox-dir`.
5. Replace TOML table names, schema version constants, callback manifest fields, callback registry metadata, and JSON output keys with Toolbox names.
6. Move `skillset/user-plugins/gpu-analytical-modeling` to `skillset/toolboxes/gpu-analytical-modeling` and update its manifest and README.
7. Rename and update unit tests to cover the new command names, table names, schema versions, field names, callback gating metadata, and moved package path.
8. Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.

## Open Questions

None. The user selected a breaking public-language and durable-schema rename with no deprecation or alias period.
