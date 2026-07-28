## 1. Source Schemas and Validation

- [x] 1.1 Add the closed Mindset Source v2 JSON schema with bounded question sets, reserved `default`, `question_ids` support for `"all"` or an ordered reference list, and no per-question triggering condition.
- [x] 1.2 Update Source loading and semantic diagnostics to accept v1 and v2, expand `"all"`, validate many-to-many membership and exactly one `default` set, and normalize v1 as an implicit default-only Source without rewriting it.
- [x] 1.3 Update Source rendering and replacement checks to display v2 question-set membership and preserve dual-version observed-digest behavior.

## 2. Question-Set Selection and Records

- [x] 2.1 Add the typed question-set selection boundary that validates one selected set id, `matched`, `default-fallback`, or `legacy-default` selection kind, the exact v2 triggering condition, and a nonempty rationale.
- [x] 2.2 Change Mindset Record materialization to copy only the selected set's expanded canonical questions in deterministic order while always materializing the additional-question collector.
- [x] 2.3 Extend the Mindset Record v1 schema, immutable-snapshot validation, renderers, and Markdown template with additive Source-version and question-set-selection fields while preserving historical Records without those fields.
- [x] 2.4 Update Kaoju entrypoint and shared mindset guidance to inspect specialized set conditions against the concrete task and pinned Run context, select one best set or `default`, and keep `project runs resolve-mindset` unchanged.

## 3. Packaged Sources and Topic Creation

- [x] 3.1 Convert the three packaged mindset seeds to v2 with their existing question catalogs and one `default` set that uses `question_ids: "all"`.
- [x] 3.2 Update the checked survey-process contract and Python contract checks to emit Source v2 while declaring v1 compatibility.
- [x] 3.3 Update topic-creation guidance and validation so newly derived or explicitly regenerated Sources emit v2, retain one nonempty `default` set, and reuse canonical questions across specialized sets.

## 4. Domain Language and Tests

- [x] 4.1 Update the canonical Mindset Source and Mindset Record domain-language definitions for reusable questions, many-to-many question sets, set-only triggering conditions, one selected set, and default fallback.
- [x] 4.2 Add unit tests for valid and invalid v2 Sources, shared question membership, missing or duplicate `default`, unresolved references, bounds, rendering, and preserved v1 Sources.
- [x] 4.3 Add unit tests for specialized, ambiguous-best-match, default-fallback, and legacy-default Record materialization, selection diagnostics, immutable snapshots, and historical Record compatibility.
- [x] 4.4 Update packaged-skill, contract, record-format, and integration tests for v2 defaults, topic derivation, Artifact persistence, rendering, Run resolution, and the unchanged CLI surface.

## 5. Validation

- [x] 5.1 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`, then fix all failures caused by the change.
- [x] 5.2 Run strict OpenSpec validation for `add-kaoju-mindset-question-sets` and confirm the implementation matches the proposal, design, and delta specification.
