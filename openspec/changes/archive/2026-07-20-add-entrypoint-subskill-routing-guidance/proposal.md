## Why

System-skill compaction makes each public entrypoint responsible for selecting protected subskills, but the current entrypoint tables expose mostly names and internal designators. The protected subskills retain detailed trigger metadata, yet an entrypoint needs concise routing guidance before it can select and load the correct protected member.

## What Changes

- Add one context-aware routing sentence for every protected subskill listed by `isomer-op-entrypoint`, `isomer-ext-deepsci-entrypoint`, and `isomer-ext-kaoju-entrypoint`.
- Write each sentence from the owning entrypoint's perspective, using the protected subskill's frontmatter and agent metadata as source evidence while removing context already established by the entrypoint and distinguishing nearby routes where necessary.
- Keep protected subskills parent-routed and omit language that presents them as independently user-invokable skills.
- Extend packaged-skill validation so every manifest-declared protected member has exactly one substantive routing sentence in its public entrypoint table.
- Update the bundled `imsight-agent-skill-handling` authoring convention so its style guide, skill creation workflow, formatting workflow, layout guidance, and design template require the same parent-oriented routing sentence for every bundled subskill.

## Capabilities

### New Capabilities

- `imsight-subskill-routing-guidance`: Define the reusable Imsight authoring and formatting rule that a parent skill must explain, in one context-aware sentence per bundled subskill, when its entrypoint should route to that subskill.

### Modified Capabilities

- `packaged-system-skill-template-format`: Require public entrypoints to provide validated, context-aware routing guidance for every protected subskill they own.
- `isomer-op-entrypoint-skill`: Add one-sentence routing guidance for every protected operator, service, misc, and shared member in the core entrypoint.
- `isomer-deepsci-pipeline`: Add one-sentence routing guidance for every protected DeepSci workflow member in the DeepSci entrypoint.
- `kaoju-research-extension`: Add one-sentence routing guidance for every protected Kaoju workflow member in the Kaoju entrypoint.

## Impact

The change updates the three public entrypoint `SKILL.md` files and the system-skill validator and its tests. It also updates `imsight-agent-skill-handling` in the separate `houmao-agents` checkout under `extern/orphan/`; those edits remain separate Houmao repository work and are not committed through the Isomer repository. The change depends on the protected-pack layout introduced by `regroup-system-skills`, but it does not change public command syntax, protected invocation designators, manifest identities, callback targets, resource ownership, or host projection behavior.
