## Why

The paper-writing v2 skills currently have placeholder binding pages, but their rows still bind many paper-specific artifacts through generic profiles such as `handoff.paper-contract`, `report.writing-plan`, or `evidence.source-material-ledger`. The storage plan now defines a sharper paper-line mapping, so working agents need those writing-related placeholders to point at consistent Isomer record kinds, semantic labels, profiles, and CRUD patterns before they create durable paper artifacts.

## What Changes

- Update writing-related `placeholder-bindings.md` pages across `skillset/research-paradigm/v2/*` so paper contract, outline, evidence ledger, experiment matrix, writing plan, draft, bibliography, validation, bundle, review, rebuttal, figure, and finalization placeholders use the paper-writing storage profiles from `context/plans/refactor-isomer-rsch-skills/required-storage-support.md`.
- Keep semantic placeholders in workflow prose and local `migrate/placeholders.md` registries unless a placeholder itself is missing or clearly misclassified.
- Prefer existing semantic labels such as `topic.records.views`, `topic.records.artifacts`, `topic.records.tasks`, `topic.records.runs`, and `topic.records.logs`; do not introduce paper-specific top-level semantic labels.
- Use `isomer-cli ext research records` command shapes with explicit `--semantic-label`, `--profile`, `--placeholder`, `--skill`, producer, consumer, and useful metadata for paper-line refs such as `selected_outline_ref`, `package_type`, `paper_surface`, section ids, reviewer item ids, or claim ids.
- Update shared guidance or validation documentation when needed so future v2 skill migrations follow the same paper-writing binding convention.

## Capabilities

### New Capabilities

### Modified Capabilities

- `research-paradigm-skills`: Requires writing-related v2 skill placeholder bindings to map paper-line artifacts to the shared paper-writing storage profiles while preserving workflow placeholders and research skill conventions.

## Impact

- Affects `skillset/research-paradigm/v2/*/placeholder-bindings.md` for paper-writing, review, rebuttal, finalize, plotting, figure, and Nature companion skills.
- May touch `skillset/research-paradigm/v2/*/migrate/placeholders.md` only when an existing placeholder is missing or has a clearly wrong kind for its durable storage role.
- May update shared v2 references or validation guidance if the current validator cannot catch paper-binding drift.
- Does not require new semantic labels, new runtime tables, or native `project records ...` commands.
