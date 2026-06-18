## Why

The research-paradigm skills now know where workspace files belong, but they still cannot say how research outputs become durable Isomer state. This leaves Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, and Gates as repeated TBD surfaces across the skillset, which blocks executable research workflows and later command, literature, scheduler, and GUI contracts.

## What Changes

- Define the core research recording contract for durable Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, and Gates.
- Define host-facing APIs for recording Artifacts and Provenance Records, querying and writing Findings, and opening, resolving, and recording Gates.
- Define minimum record fields, state semantics, linkage rules, and validation behavior for broken refs, missing files, unsupported claims, unresolved Gates, and stale Provenance Records.
- Treat Research Topic, Research Inquiry, Research Task, Run, Agent Team Instance, and Agent Instance ids as reference fields without defining the full lifecycle state machine in this change.
- Update research-paradigm skill requirements so recording API and record-schema TBD placeholders are replaced where this accepted contract applies.
- Leave command execution, literature providers, scheduler policy, Skill Binding, Agent Team State, and full lifecycle transitions for follow-up changes.

## Capabilities

### New Capabilities

- `research-recording-contracts`: Defines durable research records, recording/query APIs, linkage rules, and validation behavior for Isomer research state.

### Modified Capabilities

- `research-paradigm-skills`: Update skillset requirements so accepted recording contracts replace corresponding API and schema TBD placeholders while unrelated provider, execution, scheduler, and policy TBDs remain explicit.

## Impact

- Affected specs: `research-recording-contracts`, `research-paradigm-skills`.
- Affected documentation: `skillset/research-paradigm/isomer-rsch-shared/references/tbd-surface-registry.md`, local `isomer-research-contract.md` copies, and skill references that mention Artifact, Provenance, Finding, Evidence Item, Research Claim, Decision Record, or Gate placeholders.
- Affected future implementation: Workspace Runtime schema, Artifact and provenance service, Gate handling, Finding query/write surface, claim validation, View Manifest inputs, and future Execution Adapter/literature-provider integration.
- Dependencies: uses Workspace Path Resolution for Artifact file locations and path durability; does not add new runtime dependencies.
