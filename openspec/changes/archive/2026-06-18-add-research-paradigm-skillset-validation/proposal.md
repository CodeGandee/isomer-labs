## Why

The research-paradigm skills now consume accepted workspace, recording, lifecycle, CLI topic-context, and execution-extension contracts, but that consistency is still protected by manual searches. Stage 6 needs a deterministic validation harness so stale vocabulary, resolved TBD placeholders, hard-coded source paths, broken skill references, and manifest drift do not return as active skill guidance.

## What Changes

- Add a repository-runnable validation harness for `skillset/research-paradigm`.
- Add configurable allow zones so migration tables, provenance notes, and deferred-resource notes can mention source terms without becoming active guidance.
- Validate stale lifecycle/workspace terms, resolved workspace path TBDs, registered `[[tbd-surface:*]]` placeholders, hard-coded local/source paths, broken local references from `SKILL.md`, skill folder/frontmatter/manifest name consistency, and core skill layout.
- Add focused unit tests with fixture skillsets for validator behavior.
- Add a Pixi repository command for running the harness.
- Update the skill-gap plan after the harness exists and has been run.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `research-paradigm-skills`: require an executable repository validation harness for the existing research-paradigm skillset validation rules, including allow-zone handling for provenance and source-term mapping text.

## Impact

- Affects `scripts/`, `tests/unit/`, `pyproject.toml`, `openspec/specs/research-paradigm-skills/spec.md`, `context/plans/research-paradigm-skill-gaps.md`, and optional validation configuration under `skillset/research-paradigm/`.
- Does not change research workflow semantics, runtime APIs, or provider contracts.
