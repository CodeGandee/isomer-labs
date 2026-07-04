## Context

The repository already has a source architecture spec and tests that guard against package monoliths and obsolete compatibility shims. The Workspace Runtime refactor consolidated an overly fragmented package into `records.py`, `sqlite.py`, `store.py`, and `validation.py`; other packages now show the same pattern at a smaller scale. `artifact_formats`, `deepsci_ext`, `teams`, and `workspace` contain files whose names describe fragments such as resolver, rendering, refs, tmp, packet validation, and template harness, even though those files change with their neighboring domain modules.

The CLI command surface must remain stable. Internal non-CLI imports may break because the user explicitly allowed breaking changes except for `isomer-cli`.

## Goals / Non-Goals

**Goals:**

- Consolidate tightly coupled helper modules into fewer files with names grounded in Isomer domain language or concrete processing boundaries.
- Preserve `isomer-cli` commands, command options, and JSON/text behavior while migrating internal imports.
- Update source architecture tests so deleted helper modules cannot reappear unnoticed.
- Keep large workflow modules from absorbing unrelated behavior only to reduce file count.

**Non-Goals:**

- Do not redesign public CLI commands or handler structure.
- Do not refactor files under `isomer-history/`.
- Do not split the existing large `houmao`, `records`, `models`, `workspace/manifest.py`, `workspace/reset.py`, or CLI command modules.
- Do not introduce compatibility shims for removed internal modules.

## Decisions

1. Consolidate Artifact Format processing into `artifact_formats/processing.py`. Resolution, JSON payload/schema loading, validation, and rendering are one pipeline and already import each other. `models.py`, `registry.py`, and `workspace_provider.py` remain distinct because they represent data contracts, provider registration, and built-in workspace-backed providers.

2. Consolidate DeepScientist compatibility tools into `deepsci_ext/tools.py`. The registry constants, `call_tool` service entrypoint, compatibility service class, raw JSON input/output helpers, and unsupported-tool payload builder form one command-facing tool adapter. `store.py` remains separate because it owns SQLite persistence, and `record_formats.py` remains separate because it is an Artifact Format provider.

3. Fold Topic Team helper shards into their owning modules. `teams/template_harness.py` belongs in `teams/templates.py`, and `teams/packet_validation.py` belongs in `teams/instantiation.py`. `teams/profile_bundle_validation.py` can fold into `teams/profiles.py` because those checks validate Topic Agent Team Profile provenance and bundle layout during profile parsing and launch-facing validation.

4. Rename Workspace helpers around canonical concepts. `workspace/semantic_surfaces.py`, `workspace/layout.py`, and `workspace/tmp.py` become `workspace/surfaces.py`, covering Semantic Workspace Surface Labels, Default Layout Profile helpers, and Local Tmp Surface policy. `workspace/paths.py` becomes `workspace/path_resolution.py`, and Agent Workspace ref helpers move there because they support Workspace Path Resolution. `workspace/manifest.py`, `workspace/actors.py`, `workspace/pixi.py`, `workspace/reset.py`, `workspace/guidance.py`, and `workspace/self_query.py` remain separate.

5. Keep the CLI stable by changing imports behind commands and handlers only. The command registration modules and handler modules should continue to exist, so the user-facing `isomer-cli` interface remains unchanged.

## Risks / Trade-offs

- Import churn may touch many tests and command modules. Mitigation: migrate imports with targeted search, then run lint, typecheck, unit tests, and CLI smoke checks.
- `workspace/path_resolution.py` may become a large file after absorbing Agent Workspace refs. Mitigation: accept this only because Workspace Path Resolution is already a large transitional boundary and the merged helpers directly serve that boundary.
- Consolidating helper modules removes import paths that external callers might use. Mitigation: document this as a breaking internal change and preserve only the stable CLI entry point.
- Pending runtime consolidation changes are already in the worktree. Mitigation: layer this change on top of those canonical runtime paths without reverting or reintroducing removed runtime modules.

## Migration Plan

1. Create the consolidated modules and migrate implementations without changing function names where possible.
2. Update imports in `src/`, `tests/`, manual harnesses, and architecture tests.
3. Delete obsolete helper-shard modules.
4. Extend architecture guardrails for the new canonical module sets.
5. Validate with `pixi run lint`, `pixi run typecheck`, `pixi run test`, and focused CLI smoke checks for affected command groups.

## Open Questions

None.
