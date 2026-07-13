## Context

The research-template commands were registered through the shared research-record `_with_context` adapter. That adapter emits `dumps_raw_json(...)` for context failures, record failures, and results without consulting root-level output mode. Consequently, a Click usage failure under `ext research templates` is text by default, while a domain failure after command dispatch is unwrapped JSON.

The same adapter resolves Effective Topic Context through a full `build_project_state` call. In the current Project, most command time is spent validating User Skill Callback registries and repeatedly reading system-skill metadata that template operations do not consume. Separately, `templates list` still calls `list_records`, which materializes every lifecycle record and filters `kaoju:writing-template` metadata in Python. A prior change moved named-template lookup to `query_index_list`, but it intentionally left the list flow unchanged.

The command remains topic-scoped. Template files under the selected Topic Workspace are authoritative, while `kaoju:writing-template` records provide identity, status, metadata, lineage, and provenance.

## Goals / Non-Goals

**Goals:**

- Render research-template failures as text by default and as versioned JSON only when root-level `--print-json` is present.
- Preserve stable domain error codes, diagnostics, exit status, and known mutation state.
- Resolve a valid Effective Topic Context using only validation needed to select the Topic Workspace and operate on its template records and files.
- Use the query index for template listing and named-template lookup without changing externally visible template selection behavior.
- Prove through focused tests that unrelated Project callback volume and unrelated lifecycle-record volume do not drive template command work.

**Non-Goals:**

- Changing output behavior for `ext research records`, `ext research ideas`, or other CLI command families.
- Redesigning successful research-template payloads or template file generation.
- Weakening `project validate`, `project doctor`, or commands that consume User Skill Callback, Toolbox, profile, or system-skill configuration.
- Rebuilding or repairing the query index during a template read.
- Changing `paper-pass`, LaTeX compilation, template lineage, archival, or provenance semantics.

## Decisions

### Give research templates a dedicated command runner

Replace the injected generic research-record runner with a template-specific runner that still reuses common option merging, context discovery primitives, and record APIs. The runner owns template failure normalization and can request the bounded context-validation scope described below. Successful template payloads remain compatible; only failure rendering is mode-aware in this change.

The runner will retain the domain payload, including `ok`, `mutated`, and `error.code`. In text mode it will render existing diagnostics followed by a concise domain error message when diagnostics alone do not explain the failure. Under root-level `--print-json`, it will use the shared versioned JSON renderer with command path `ext research templates <subcommand>`.

Keeping this runner template-specific avoids changing the machine-oriented behavior of sibling research extension commands. Modifying the shared `_with_context` adapter was rejected because that would broaden compatibility and testing work beyond the requested surface.

### Add an opt-in template-operation validation scope

Extend the existing context-building boundary with an explicit opt-in scope for research-template operations. The scope still performs Project discovery, Project Manifest parsing, topic-selection precedence, Research Topic registration and config checks needed for selection, Topic Workspace mapping and path bounds, local active-context handling, and the consistency checks required to open the selected Workspace Runtime.

The scope does not load or validate User Skill Callback registries, Toolboxes, Domain Agent Team Templates, Topic Agent Team Profile files, or other configuration that no research-template subcommand consumes. Record creation or mutation continues to validate the artifact and runtime inputs at the point those APIs consume them. The default context-building scope remains full, so existing callers retain current validation behavior.

An explicit scope is preferred over command-name conditionals inside `build_project_state`: the caller declares what it consumes, tests can assert the boundary, and unrelated commands cannot silently inherit reduced validation. Caching the system-skill manifest alone was rejected as the primary fix because it would make unrelated validation cheaper while still performing work that templates do not need.

### Query template summaries through the existing read index

Change `templates list` to call `query_index_list` with exact semantic id `kaoju:writing-template` and no lifecycle-record fallback. Map indexed rows into the existing public template summary fields, including record id, status, transition metadata, and `is_default`. Apply `--venue` and `--paper-type` against indexed transition metadata.

Keep `_find_template_record` as the single named-template lookup path for `show`, `refresh`, `compile`, and `remove`. All such lookups use the query index and preserve the existing active-template status policy. Commands that need canonical detail reopen the selected record through the canonical record API after indexed identity lookup.

Using the query index matches its operator-inspection purpose and avoids scaling template work with unrelated lifecycle records. Direct SQL in the CLI and a template-specific secondary index were rejected because the existing query service already owns the derived read model and diagnostics.

### Test work boundaries rather than wall-clock thresholds

Unit tests will assert that template commands do not invoke callback-registry validation or `list_records`, that exact indexed filters are passed, and that mapped results remain stable. CLI tests will cover default text failures and root-level JSON failures. A fixture with unrelated callbacks and lifecycle records will exercise the complete template list path without using brittle timing thresholds.

Wall-clock assertions were rejected because Pixi startup, filesystem caches, and host load vary across development and CI environments.

## Risks / Trade-offs

- [Focused context validation can leave unrelated Project errors unreported during a template command] → Keep full validation as the default, skip only named capability groups that templates do not consume, and retain `project validate` as the complete diagnostic surface.
- [A stale query index can omit a canonical template record] → Preserve query diagnostics and explicit index-rebuild guidance; do not silently scan canonical lifecycle records or mutate the index during a read.
- [Failure output changes can break scripts that parsed unwrapped JSON without `--print-json`] → Document the compatibility break and test root-level `--print-json` as the stable automation contract.
- [Indexed metadata shape differs from lifecycle-record shape] → Centralize row-to-template-summary mapping and regression-test the public fields used by list and named lookup.

## Migration Plan

1. Add the opt-in template-operation validation scope while preserving full validation as the default.
2. Add the template-specific runner and failure renderers, then migrate all six template subcommands to it.
3. Move list and named-template reads to the shared indexed mapping and add regression fixtures.
4. Run focused unit tests, then repository lint, type checking, and unit tests.

Rollback restores the generic research-record runner and prior list implementation. No stored records, template files, manifests, or Workspace Runtime schema require migration.

## Open Questions

- None.
