## Why

The research-paradigm skillset now includes a much larger v2 surface, including refactor-migrated paper-writing and Nature-facing skills, while the OpenSpec contract and validator tests still reflect earlier assumptions about a smaller v2 set and active-only Markdown. This change aligns the spec, validation harness, and tests with the current skillset layout so migration/provenance material remains traceable without being treated as active runtime guidance.

## What Changes

- Update the `research-paradigm-skills` specification to include the current v2 skill inventory, including paper-writing, review, rebuttal, plotting, figure-polish, and Nature-facing companion skills.
- Replace stale “v2 excludes paper-production skills” expectations with requirements for the migrated v2 companion-skill bundle and its provenance layout.
- Clarify validation boundaries between active runtime skill guidance and non-active migration, provenance, analysis, source-copy, template, and license material.
- Require validator and unit-test coverage for expected skill inventory, active-file classification, local reference integrity, placeholder registration, pattern references, manifest consistency, and rule-specific allow zones.
- Keep v1 preservation and v2 storage-binding deferral intact; this change updates tests/specs around the current migration state rather than introducing storage-bound runtime APIs.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `research-paradigm-skills`: Update skillset layout and validation requirements to cover the expanded v2 skill inventory and migration-aware validation surface.

## Impact

- Affects the OpenSpec contract for `research-paradigm-skills`, especially layout and validation scenarios.
- Affects `scripts/validate_research_paradigm_skillset.py`, `tests/unit/test_validate_research_paradigm_skillset.py`, and the `pixi run validate-research-skills` command behavior.
- Affects documentation and provenance expectations under `skillset/research-paradigm/`, including `README.md`, `PROVENANCE.md`, `validation.toml`, v1/v2 skill folders, and migrated v2 `migrate/` and `org/` subtrees.
