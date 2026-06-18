# Research Execution Open Questions

## Context

The active OpenSpec change defines a provider-neutral Research Execution and Extension Contract. The first design pass intentionally left four questions open: where to show TOML examples, whether baseline waiver is a Gate subtype or separate policy ref, how to record literature provider output that is only context, and whether service requests and agent launches share the Execution Adapter Command Request envelope.

## Accepted Direction

Accepted option: reference-first unified contract.

The contract should stay provider-neutral and ref-driven in the first implementation. Research Topic Config and Topic Agent Team Profile examples should both exist, baseline waiver should be a separate policy ref that may open a Gate, context-only literature should start as provider-output Artifacts, and Service Requests plus agent launches should use the Execution Adapter Command Request envelope with narrow operation kinds.

## Decisions

### Examples belong in both Research Topic Config and Topic Agent Team Profile

Research Topic Config examples should show topic-level defaults and selected extension refs. Topic Agent Team Profile examples should show role-scoped, Workflow Stage-scoped, Capability Binding, and Skill Binding projection availability. Neither example should contain provider-specific command bodies, credentials, scheduler internals, command outputs, or provider payloads.

### Baseline waiver remains a separate policy ref

Baseline-waiver policy answers whether a route may proceed without an accepted active baseline and what rationale or later promotion limits apply. When the policy requires human judgment, it opens or references a Gate. The Gate records the concrete pending or resolved human-return decision; the policy remains the reusable rule set.

### Context-only literature starts as provider-output Artifact

Literature provider output collected only for orientation, source review, adjacent-work scouting, or future comparison should first be recorded as a provider-output Artifact with source metadata and Provenance refs. A later Finding may distill it into reusable context. An Evidence Item should only be created when the result has a relation intent to support, contradict, contextualize, refute, or motivate withdrawal of a Research Claim.

### Service requests and agent launches share the command envelope

Service Request dispatch, Service Agent Instance launch, and Agent Team Instance launch should use the Execution Adapter Command Request envelope with operation kinds such as `service_request` and `agent_launch`. The domain objects remain distinct: Service Request, Service Agent Instance, Agent Team Instance, Agent Profile, Run, Artifacts, and Provenance Records keep their own semantics. The shared envelope only normalizes dispatch, preflight, monitoring, and recording.

## Evidence

- `openspec/changes/define-research-execution-extension-contract/design.md` already chooses provider-neutral extension points, one Execution Adapter Command Request envelope, scheduler/lifecycle separation, Gate policy preflight, literature/baseline typed extension points, durable-record reuse, and Skill Binding projection under Capability Binding.
- `openspec/changes/define-research-execution-extension-contract/specs/cli-topic-context-resolution/spec.md` says Research Topic Config and Effective Topic Context carry refs and must not store runtime truth, secrets, command outputs, provider payloads, scheduler internals, or implementation bodies.
- `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md` defines Research Topic Config as topic defaults and refs, Topic Agent Team Profile as topic-specialized team structure, Run as bounded execution, Gate as human-return control point, and Workspace Runtime as the durable record substrate.
- `.imsight-arts/project-explore/adrs/0018-workspace-path-resolver.md` keeps process environment and adapter overrides out of durable truth, which supports the ref-first execution contract.

## Rejected Alternatives

- Do not make Research Topic Config the complete execution binding, because role, stage, skill, and operation authority belong to team profile and binding material.
- Do not model baseline waiver only as a Gate subtype, because validation and later promotion checks need a reusable policy even when no Gate is open.
- Do not record context-only literature directly as Finding or Evidence Item, because raw provider output, distilled insight, and claim support have different evidence semantics.
- Do not create a separate service or launch dispatch envelope in the first contract, because those operations need the same permission, Gate, Run, Artifact, monitoring, and Provenance behavior as other executable operations.

## Follow-up

Apply-phase work should update the main specs, shared research-paradigm contracts, local skill contract copies, and stage-specific references to reflect these decisions. Validation should search for stale placeholders and confirm the skill text does not reintroduce provider-specific implementations into generic skills.
