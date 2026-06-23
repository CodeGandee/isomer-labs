## Context

Isomer's domain language already separates **Domain Agent Team Template**, **Topic Agent Team Profile**, and **Agent Team Instance**. `teams/deepsci-mini` is therefore a reusable template, not a topic team. It contains placeholder contracts for topic refs, runtime refs, role bindings, Agent Workspace refs, policies, and expected outputs. The current Python specialization path can synthesize plausible refs, but that bypasses the project model: the Operator Agent should inspect the template and topic context, produce a reviewable specialization, obtain approval, and only then create launch/runtime material.

The near-term pressure comes from UC-01. The UC-01 manual harness can prove generic runtime record behavior, but it should not become the authority for converting `deepsci-mini` into a concrete topic team. This change introduces the missing orchestration layer: a Houmao-backed Isomer Operator Agent with Isomer-specific skills for topic-team instantiation.

## Goals / Non-Goals

**Goals:**

- Treat Domain Agent Team Templates as generic, placeholder-bearing material until an Operator Agent specializes them.
- Define an Operator Agent instantiation packet that records how template placeholders become Topic Agent Team Profile values or approved deferrals.
- Add Isomer Operator Agent skills for template inspection, context resolution, placeholder reconciliation, profile drafting, review Gate preparation, materialization, and launch orchestration.
- Make Python code validate, persist, and launch from approved packets instead of inventing topic-specific defaults as the authoritative path.
- Preserve generic product code and keep UC-01 or `deepsci-mini` special cases out of `src/isomer_labs` except as fixture/template data.

**Non-Goals:**

- Do not implement a full autonomous research loop in this change.
- Do not require live Houmao for deterministic tests; simulated Operator Agent artifacts are acceptable for core validation.
- Do not make the Execution Adapter responsible for topic reasoning, placeholder choice, or user approval.
- Do not store credentials, live process state, or rich research outputs in Topic Agent Team Profile files.
- Do not remove CLI preview commands if they remain explicitly preview-only and side-effect-light.

## Decisions

### Decision: Introduce a Topic Team Instantiation Packet

The Operator Agent should produce a structured packet before writing a Topic Agent Team Profile. The packet names the source Domain Agent Team Template, selected Research Topic, Topic Workspace, Workspace Runtime ref, target Topic Agent Team Profile id, role bindings, policy refs, expected Artifacts, unresolved or deferred placeholders, approval state, and provenance refs.

Alternative considered: let `specialize_topic_agent_team_profile()` keep generating defaults. That is simple, but it makes Python the hidden Operator Agent and loses the reviewable reasoning that the domain model expects.

### Decision: Use Skills for Agent Judgment, Python for Validation and Recording

The Isomer Operator Agent should use explicit skills such as `isomer-template-inspect`, `isomer-topic-context-resolve`, `isomer-placeholder-reconcile`, `isomer-topic-profile-draft`, `isomer-profile-review-gate`, `isomer-profile-materialize`, and `isomer-team-launch-orchestrate`. These skills are allowed to reason over template docs, project context, and user intent. Python modules should expose parsers, validators, deterministic renderers, and store/adapter APIs.

Alternative considered: encode the orchestration as one product CLI command. That would hide the agent boundary again and make later Houmao-backed orchestration harder to test.

### Decision: Keep the Execution Adapter Below the Operator Agent

Houmao remains the execution backend. The Operator Agent prepares and approves the Isomer packet/profile, then calls generic materialization or launch APIs. The Houmao adapter consumes approved runtime/profile state and records adapter refs; it does not choose placeholder substitutions or decide the research team shape.

Alternative considered: make the Houmao adapter read `teams/deepsci-mini` and generate launch profiles directly. That would collapse Isomer domain reasoning into provider-specific launch mechanics.

### Decision: Preserve Preview Paths as Non-Authoritative

Existing CLI profile specialization preview can remain, but it must label synthetic values as preview or candidate material. Authoritative materialization requires an Operator Agent instantiation packet or an explicit equivalent provided by a caller and validated against the same schema.

Alternative considered: remove preview immediately. That would reduce useful inspection behavior and make migration harder without improving the core model.

### Decision: UC-01 Should Exercise the Operator-Agent Path

Future UC-01 acceptance should prove that `deepsci-mini` is inspected as a Domain Agent Team Template, specialized into a Topic Agent Team Profile by Operator Agent skills, approved or deterministically auto-approved in tests, then launched or simulated as an Agent Team Instance. The manual harness can still own UC-01-specific record assertions, but it should not hardcode team instantiation.

Alternative considered: keep UC-01 harness independent of Operator Agent instantiation. That would make the milestone pass while leaving the real topic-team lifecycle untested.

## Risks / Trade-offs

- Operator Agent skills become too broad -> Keep each skill bounded to one artifact or decision: inspect, resolve, reconcile, draft, review, materialize, launch.
- Tests become dependent on live Houmao -> Use deterministic packet fixtures and simulated Operator Agent outputs for unit/manual tests; keep live launch optional and gated.
- Packets duplicate profile fields -> Treat packets as provenance and review material; Topic Agent Team Profiles remain the durable design-time profile.
- Placeholder deferrals hide launch blockers -> Require explicit deferred-placeholder diagnostics and review state; block launch-facing operations when required launch placeholders remain unresolved.
- Existing CLI users depend on preview defaults -> Keep preview output, but mark it as candidate and require packet-backed materialization for authoritative creation.

## Migration Plan

1. Add packet schema, validators, and template placeholder inspection for `deepsci-mini` and generic templates.
2. Add Isomer Operator Agent skills under the repository skillset and a Houmao launch/profile definition for the Operator Agent.
3. Update profile specialization APIs so they accept a validated packet and treat old synthetic preview generation as preview-only.
4. Update Agent Team Instance creation and Houmao launch flows to link runtime records to the approved packet/profile provenance.
5. Revise UC-01 manual acceptance to use a deterministic Operator Agent packet path before creating/simulating the team.
6. Keep rollback simple: generated packet/profile material is additive and can be ignored by older preview-only flows, but launch-facing tests should require the new provenance once this change lands.

## Open Questions

- Should the Operator Agent be project-scoped by default or topic-scoped per Topic Workspace?
- Should packet approval be stored as a Gate/Decision Record immediately, or as profile provenance until a richer approval model lands?
- Should the first implementation use a simulated Operator Agent packet fixture before launching a real Houmao Operator Agent?
