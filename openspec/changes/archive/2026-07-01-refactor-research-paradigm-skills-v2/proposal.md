## Why

The current `skillset/research-paradigm/isomer-rsch-*` skills preserve useful DeepScientist research workflow material, but they also carry too much storage, runtime, policy, and lifecycle bookkeeping in the active skill instructions. We need a concise v2 research-method layer that helps agents conduct research while letting Isomer Labs storage and runtime contracts handle implementation details.

## What Changes

- Create `skillset/research-paradigm/v2/isomer-rsch-<purpose>-v2/` skill bundles for the core research process: shared contract, scout, baseline, idea, optimize, experiment, analysis, decision, finalize, and science.
- Move every existing flat `skillset/research-paradigm/isomer-rsch-*` skill bundle into `skillset/research-paradigm/v1/` and rename each folder and skill frontmatter with a `-v1` suffix, preserving source provenance, license context, and references.
- Update research-paradigm documentation and validation so the root skillset has explicit `v1/` and `v2/` generations instead of treating the old flat skill folders as active current skills.
- Define v2 skills as concise methodology instructions with a small shared semantic-placeholder contract: name the research things a skill needs or produces, but do not bind those placeholders to Artifact, Evidence Item, Run, Gate, path, database, or storage labels yet.
- Treat paper, review, rebuttal, plotting, and figure-polish skills as preserved v1 material for now rather than part of the initial v2 core research loop.
- **BREAKING**: Active research-paradigm skill names move from `isomer-rsch-<purpose>` to generation-suffixed names such as `isomer-rsch-experiment-v2`; existing skill callers must update prompts, manifests, and validation expectations.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `research-paradigm-skills`: change the skillset layout, naming convention, active skill contract, v1 archive behavior, v2 core skill requirements, and validation rules for generation-suffixed research skills.

## Impact

- Affected files include `skillset/research-paradigm/`, `skillset/research-paradigm/README.md`, `skillset/research-paradigm/PROVENANCE.md`, `skillset/research-paradigm/validation.toml`, any local validation scripts that assume flat `isomer-rsch-*` folders, and any skill manifests or role maps that invoke old names.
- Existing DeepScientist-derived skill content remains available under `v1/`; the v2 implementation should draw from `context/explore/deepscientist-skill-analysis/` for core research-process structure without making that context path a runtime dependency.
- The change does not add a new storage layer, new storage labels, or storage bindings for v2 skill outputs. V2 skills should replace storage-facing nouns such as Artifact, Evidence Item, Run, Gate, Decision Record, and concrete paths with semantic placeholders whose meaning can be refined before a later storage-binding change.
