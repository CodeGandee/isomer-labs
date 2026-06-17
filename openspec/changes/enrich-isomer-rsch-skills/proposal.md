## Why

The current `isomer-rsch-*` skillset preserves the stage map, but most skills are still thin summaries that point back to source-analysis notes instead of carrying the reusable DeepScientist methods as self-contained Isomer skill bundles. `isomer-rsch-analysis` now shows the target shape: local references, provenance, correct concept mapping, and an Imsight-style workflow entrypoint.

## What Changes

- Enrich every non-analysis `isomer-rsch-*` skill with local references, templates, playbooks, checklists, assets, or scripts when the DeepScientist source contains reusable detail that is not already represented.
- Keep `SKILL.md` entrypoints concise and route long detail into one-level local `references/`, with `assets/` or `scripts/` only when directly useful and sanitized.
- Replace active dependencies on `context/explore/...`, `extern/orphan/...`, or other files outside the skill directory with local bundled references or provenance notes.
- Translate DeepScientist concepts into accepted Isomer terms and mark unsettled concrete paths, schemas, APIs, providers, commands, and policies with `[[tbd-surface:<id>]]`.
- Format each skill entrypoint through `$imsight-agent-skill-handling format-skill`, meaning a near-top `## Workflow`, numbered steps, concise reference routing, and a fallback for freeform tasks.
- Add or refresh `agents/openai.yaml` manifests for independently packaged skill bundles so `interface.display_name` is exactly the skill name and `default_prompt` invokes `$isomer-rsch-<purpose>`.
- Use parallel subagents during implementation with disjoint write scopes, then integrate and validate the resulting skill bundles.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `research-paradigm-skills`: Strengthen methodology preservation, self-containment, Imsight entrypoint formatting, manifest consistency, subagent implementation, and validation requirements for the existing research-paradigm skillset.

## Impact

- Affects `skillset/research-paradigm/isomer-rsch-*` skill folders, especially local `SKILL.md`, `references/`, `agents/openai.yaml`, and selected `assets/` or `scripts/`.
- May update `skillset/research-paradigm/isomer-rsch-shared/references/tbd-surface-registry.md` for missing placeholder ids discovered during enrichment.
- Updates `openspec/specs/research-paradigm-skills/spec.md` through a delta spec for stricter behavior and validation.
- Does not add Isomer runtime APIs, scheduler fields, storage layouts, provider integrations, or execution adapters.
