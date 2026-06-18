## Why

Research-paradigm skills now have settled workspace, recording, lifecycle, and topic-context contracts, but they still cannot describe executable workflows without open TBD placeholders for command execution, scheduler policy, Skill Binding, baseline waiver policy, cost/privacy Gate policy, and literature providers. The next change should make those surfaces specified at the contract level while leaving research-topic-specific implementations as explicit user-fillable extension points.

## What Changes

- Define a provider-neutral Research Execution and Extension Contract that covers Execution Adapter Command Requests, operation extension points, typed capability refs, scheduler and continuation boundaries, Gate policy preflight, literature provider refs, baseline-waiver policy refs, and user-filled topic-specific details.
- Replace the remaining research-paradigm TBD placeholders with accepted extension-point vocabulary and validation rules.
- Clarify that skills declare required extension points and expected Artifacts, but Research Topic Config, Topic Agent Team Profiles, Capability Bindings, and provider-specific adapters supply the concrete implementation refs.
- Preserve existing Workspace Path Resolution, Research Recording Contracts, Research Lifecycle State, and CLI Topic Context Resolution as authorities for paths, durable records, lifecycle objects, and topic context.
- Avoid implementing command runners, schedulers, credential backends, literature providers, baseline systems, or provider-specific APIs in this change.

## Capabilities

### New Capabilities

- `research-execution-extension-contract`: Defines provider-neutral execution command requests, typed research operation extension points, user-filled topic capability refs, scheduler boundaries, Gate policy preflight, literature provider refs, baseline-waiver policy refs, validation, and skill consumption rules.

### Modified Capabilities

- `cli-topic-context-resolution`: Clarify how Effective Topic Context carries typed extension-point refs without storing runtime truth, secrets, command outputs, or provider-specific implementation bodies.
- `research-paradigm-skills`: Replace remaining TBD-surface guidance with accepted extension-point contracts and require skills to declare needed operation extension points instead of inventing host APIs or provider names.
- `research-recording-contracts`: Clarify how execution, provider, baseline-waiver, scheduler, and Gate-policy extension decisions are recorded through existing Run, Artifact, Evidence Item, Finding, Decision Record, Gate, and Provenance Record surfaces without adding rich runtime state to core records.

## Impact

- Affects OpenSpec docs under `openspec/specs/` and the new change artifacts.
- Affects `skillset/research-paradigm` shared guidance, the shared TBD registry, local `isomer-research-contract.md` copies, and stage-specific references that currently mention the six remaining placeholders.
- Affects architecture and domain language notes that mention Execution Adapter command surfaces, Capability Bindings, Skill Bindings, literature providers, baseline-waiver policy, scheduler policy, and cost/privacy Gate thresholds.
- Does not require application code, runtime adapters, provider integrations, command execution code, scheduler loops, credential storage, or generated assets.
