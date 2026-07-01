## Context

The v2 research skills deliberately keep workflow prose semantic. Each skill defines local placeholders in `migrate/placeholders.md`, and `isomer-rsch-workspace-mgr-v2` already has a bootstrap step that builds a placeholder binding registry from those local tables. The missing piece is a skill-consumable binding page that tells agents how those placeholders map to Topic Workspace record storage and which `isomer-cli ext` CRUD commands to use.

The current CLI has `ext deepsci`, but that namespace is a DeepScientist compatibility mock. It preserves source-shaped tool names and records mocked calls, so it is useful as a migration fallback but should not become the native storage contract for Isomer research records. The existing storage design also identifies `project records ...` as the future native API, but those commands do not exist yet.

## Goals / Non-Goals

**Goals:**
- Provide a first usable `isomer-cli ext research records` CRUD surface for topic-scoped research records backed by Workspace Runtime and semantic record labels.
- Add `placeholder-bindings.md` to each v2 research skill that has a placeholder registry.
- Preserve exact placeholder tokens as metadata on records and binding pages.
- Keep skill workflows semantic; agents read binding pages rather than replacing placeholder text with concrete paths.
- Validate that active v2 placeholder registries have corresponding binding coverage.

**Non-Goals:**
- Do not implement the final native `project records ...` command family.
- Do not replace or remove `ext deepsci`; it remains a compatibility fallback for source-shaped calls.
- Do not introduce dedicated tables for every research record kind in this change.
- Do not create a complete package, claim, gate, or provenance graph implementation beyond the generic record CRUD layer.

## Decisions

### Decision: Add `ext research records` as the transitional CRUD surface

The implementation will register `isomer-cli ext research records create/show/list/update/delete`. These commands use the normal topic selection options and write through Python service code, not ad hoc SQL or direct `state.sqlite` edits.

Rationale: this keeps real Isomer record CRUD separate from DeepScientist compatibility mocks while preserving the extension namespace requested for this stage. The future `project records ...` family can wrap or replace the same service later.

Alternative considered: extend `ext deepsci call artifact.record`. That would blur mocked source compatibility with native Isomer storage and make it hard for agents to know whether a result is real.

### Decision: Store records as generic runtime lifecycle rows plus optional file bodies

The first implementation will map storage item classes onto existing `RuntimeLifecycleRecord` kinds such as `artifact`, `evidence_item`, `decision_record`, `run`, `view_manifest`, and `provenance_record`. Rich bodies will be written below resolved semantic labels such as `topic.records.artifacts`, `topic.records.runs`, `topic.records.views`, or `topic.records.logs`.

Rationale: Workspace Runtime already supports these generic lifecycle kinds and content paths. This gives agents stable refs and durable bodies without committing to final dedicated tables too early.

Alternative considered: add dedicated tables for each record type now. That would be cleaner eventually, but it expands scope before the placeholder binding contract has settled through skill use.

### Decision: Keep `placeholder-bindings.md` local to each skill

Each v2 skill with `migrate/placeholders.md` will get a sibling `placeholder-bindings.md`. The page will state binding rules, kind defaults, CLI command patterns, and a table row for each local placeholder.

Rationale: local binding pages preserve self-contained skill bundles and let agents read the binding nearest to the workflow they are executing. The workspace manager can still aggregate those pages into `<RSCH_PLACEHOLDER_BINDING_REGISTRY>` during bootstrap.

Alternative considered: one global binding file for all skills. That centralizes maintenance but weakens progressive disclosure and makes standalone skill usage harder.

### Decision: Bind by placeholder kind first, then profile

The binding generator will use the placeholder registry's `Kind` column as the first routing signal. It will derive a storage item class, default semantic label, artifact profile, and CRUD command shape, while preserving the exact placeholder, producer, consumer, and meaning.

Rationale: this matches the existing storage plan and avoids brittle name-specific path rules. Specific placeholders can still override profiles later if the skill needs a tighter format.

Alternative considered: hand-author a custom binding for every placeholder. That would produce richer prose but risks drift across more than 180 placeholders.

## Risks / Trade-offs

- Generic runtime records may be too weak for later graph queries -> Keep metadata structured and preserve exact placeholder/profile fields so later migrations can upgrade rows.
- Generated binding pages may read repetitive -> Keep the per-placeholder table compact and rely on shared kind rules for interpretation.
- Agents may confuse `ext research records` with final `project records ...` -> Document the transitional status in binding pages and CLI docs.
- Deleting records could destroy evidence -> Implement `delete` as archival status mutation by default, with no file removal.
- Some future labels such as `topic.records.evidence` may not exist yet -> Route current bodies through existing labels and name planned labels as future binding targets only when available.

## Migration Plan

1. Add the research records service and CLI registration under `ext research records`.
2. Add docs and tests for create, show, list, update, and archive behavior.
3. Generate `placeholder-bindings.md` pages from each v2 skill's `migrate/placeholders.md`.
4. Update v2 skill entrypoints and relevant references so agents read binding pages before writing durable placeholder outputs.
5. Extend validation to require binding pages and placeholder coverage.
6. Validate with unit tests, research skillset validation, docs validation, and full unit tests when feasible.

Rollback is straightforward: remove the extension command registration and binding pages. Runtime rows created through the extension remain ordinary lifecycle records and can be archived or ignored.

## Open Questions

- Should `topic.records.evidence`, `topic.records.provenance`, and `topic.records.packages` become built-in labels before the native `project records ...` API lands?
- Should future record refs use short prefixes such as `artifact:<id>` or fully qualified refs such as `isomer-record:<topic-workspace>:artifact:<id>`?
- Which placeholder profiles deserve hand-authored stricter schemas after the first generated binding pass?
