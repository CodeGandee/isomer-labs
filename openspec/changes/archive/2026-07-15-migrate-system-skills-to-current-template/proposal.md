## Why

The packaged Isomer system skills predate the current Imsight skill-authoring template: 44 active entrypoints and 13 active subpages still use `## Common Mistakes`, while existing Guardrails and executable-page workflows use several older shapes. The July 15 guide revisions make `## Guardrails` the required behavior contract, reserve optional `## Troubleshooting Guide` sections for recoverable problems, and apply the format to executable subpages, so Isomer should migrate its shipped skill assets and validate that format before release.

## What Changes

- Audit all 55 manifest-declared system skills across the core, DeepSci, and Kaoju groups, including their active command and reference pages.
- Bring every active `SKILL.md` entrypoint into the current template shape: discovery-oriented frontmatter, `## Overview`, `## When to Use`, a numbered `## Workflow` with a freeform fallback, and exactly one `## Guardrails` section.
- Replace active `## Common Mistakes` sections with sparse, skill-specific `DO NOT ...` and `MUST ...` guardrails; merge duplicate old and new sections without dropping behavioral constraints.
- Move genuine problem-and-recovery guidance into optional, two-level `## Troubleshooting Guide` sections instead of treating troubleshooting as a required placeholder.
- Apply the same Guardrails and troubleshooting rules to active subcommand and reference pages that contain behavioral guidance, and complete the current workflow contract on executable subpages.
- Add manifest-aware validation and unit coverage so future packaged skills cannot reintroduce the old template.
- Preserve runtime behavior, public subcommands, local links, callback insertion points, domain terminology, and agent metadata unless a metadata edit is required to keep trigger semantics synchronized.
- Leave immutable source provenance under `org/`, migration work under `migrate/`, and passive output templates under `templates/` unchanged; those files are not active packaged skill instructions.

## Capabilities

### New Capabilities

- `packaged-system-skill-template-format`: Defines the active packaged-skill boundary, required entrypoint and executable-page structure, and manifest-aware conformance validation.

### Modified Capabilities

- `skill-guardrails-format`: Extends the current Guardrails contract from Imsight source skills to all active packaged Isomer system-skill entrypoints and behavioral subpages.
- `skill-troubleshooting-guide-format`: Extends the optional troubleshooting contract to active packaged Isomer skill entrypoints and subpages while preserving its problem-and-recovery distinction.

## Impact

- Affected assets: active Markdown under the skill roots listed by `src/isomer_labs/assets/system_skills/manifest.toml`, across `misc/`, `operator/`, `service/`, `research-paradigm/deepsci/`, and `research-paradigm/kaoju/`.
- Affected validation: `scripts/validate_skillsets.py` and focused tests in `tests/unit/test_validate_skillsets.py`.
- Affected specifications: the two existing skill-format capabilities plus a new packaged-system-skill template-format capability.
- No CLI command, schema, installation layout, system-skill manifest entry, third-party dependency, or runtime API changes are intended.
