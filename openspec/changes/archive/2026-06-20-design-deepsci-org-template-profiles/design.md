## Context

Milestone 1 gives Isomer Labs a working `isomer-cli` for Project discovery, Project Manifest validation, Research Topic Config loading, Effective Topic Context inspection, and path previews. The next roadmap slice must make `teams/deepsci-org/execplan/` visible to that Project layer as a reusable Domain Agent Team Template and then specialize it into topic-specific Topic Agent Team Profiles without launching any Agent Team Instances.

`teams/deepsci-org/execplan/` already contains generated material that can act as a template source: `manifest.toml`, participant and topology contracts, role profiles, notifier prompts, generated skills, harness schemas, workspace and run contracts, a loop-local state contract, and an instantiation guide. That material intentionally keeps topic-specific values as placeholders. The design must preserve that boundary because later Houmao launch work depends on knowing which values are reusable template facts and which values belong to a Research Topic, Topic Workspace, Topic Agent Team Profile, or runtime Agent Team Instance.

Houmao is the planned execution substrate, but these milestones do not launch Houmao agents. Houmao-specific launch dossiers, mailbox refs, gateway refs, specialists, recipes, and managed-agent details remain adapter details for a later Houmao Execution Adapter change.

## Goals / Non-Goals

**Goals:**

- Register or discover `deepsci-org` as the seed Domain Agent Team Template.
- Validate generated template material before any topic-specific specialization.
- Add neutral models and validation for Domain Agent Team Templates, Agent Roles, Workflow Stages, Capability Binding slots, Skill Binding Projection slots, Coordination Policy refs, policy refs, and template parameters.
- Specialize `deepsci-org` into Topic Agent Team Profiles for concrete Research Topics using Effective Topic Context and Project Manifest or Research Topic Config refs.
- Keep multiple topic profiles isolated so one Project can prepare different `deepsci-org` profiles for different Research Topics.
- Add headless fixtures for UC-01, UC-02, UC-03, and UC-05 profile validation without starting agents.

**Non-Goals:**

- Do not launch Agent Team Instances or Houmao managed agents.
- Do not create Workspace Runtime state, Run records, handoff records, mailbox records, gateway records, or Agent Workspaces.
- Do not convert Houmao-specific concepts into Isomer core schema names.
- Do not implement GUI views, AG-UI payload routing, or use-case live execution.
- Do not move `teams/deepsci-org/` into a Topic Workspace or copy generated template material into every Project.

## Decisions

1. Treat `deepsci-org` as a seed Domain Agent Team Template with generic loaders. The implementation should include a built-in or repository-relative registration for `teams/deepsci-org/execplan/`, but the parser and validator should work from neutral Domain Agent Team Template records rather than hard-coding only that package. Alternative considered: special-case `deepsci-org` throughout validation. That would be faster but would make the next template migration messy.

2. Keep template source and profile records separate. A Domain Agent Team Template record names reusable source files, default Agent Roles, Workflow Stages, Coordination Policy expectations, Capability Binding slots, Skill Binding Projection slots, template parameters, and placeholder names. A Topic Agent Team Profile record stores selected roles, topic refs, policy refs, expected Artifacts, profile constraints, Agent Profile refs, Capability Binding refs, Skill Binding Projection refs, and Agent Workspace refs. Alternative considered: mutate the generated execplan in place during specialization. That would blur template source with topic state and make multi-topic reuse unsafe.

3. Store profile definitions in the Project Config Directory by manifest reference. The default generated profile path should be project-scoped, for example under `.isomer-labs/team-profiles/<profile-id>.toml`, and the Project Manifest or Research Topic Config should reference it. A Topic Workspace can reference selected profile identity later through Workspace Runtime, but it must not contain a workspace-local `teams/` directory. Alternative considered: store profiles under each Topic Workspace. That conflicts with the accepted domain language and complicates template reuse.

4. Validate template material in layers. The validator should parse `manifest.toml`, artifact paths, participants, role profiles, notifier prompts, generated skills, harness schemas, workspace contract, run contract, and state contract with structured parsers where possible. The generated harness command `teams/deepsci-org/execplan/harness/bin/deepsci-org validate` can provide an additional diagnostic input, but Isomer validation should not depend only on shelling out. Alternative considered: rely entirely on the harness. That would hide Isomer-specific boundary checks such as rejecting topic-specific refs inside template material.

5. Make profile specialization pure and side-effect free. `isomer-cli team-profiles specialize` should derive a candidate profile from a selected template and Effective Topic Context, then write or preview the profile record without creating Workspace Runtime state or launching agents. Alternative considered: combine specialization with launch preparation. That would make validation and review harder and would prevent the user from editing a Topic Agent Team Profile before launch.

6. Add a small CLI surface dedicated to templates and profiles. Proposed commands are `team-templates list`, `team-templates inspect`, `team-templates validate`, `team-profiles specialize`, and `team-profiles validate`. They should share existing Project selection, text output, JSON output, and Isomer diagnostics. Alternative considered: fold these into `schemas list` or `validate`. Separate commands are clearer because templates and profiles are project-level domain records, not built-in schema names.

7. Use use-case fixtures as profile validation targets. UC-01, UC-02, UC-03, and UC-05 should produce static fixtures that exercise different role selections, policy refs, expected Artifacts, and topic constraints without executing work. UC-04 depends on GUI component behavior and belongs to later milestones. Alternative considered: wait for live execution before adding use-case fixtures. Early fixtures will catch placeholder leakage and profile isolation bugs sooner.

## Risks / Trade-offs

- Template parser drifts from generated execplan format -> Keep tests pinned to `teams/deepsci-org/execplan/manifest.toml`, participant contracts, role profiles, and harness schemas, and report unknown fields as warnings before making them errors.
- Profile records become too Houmao-shaped -> Keep Houmao launch and mailbox fields out of generic profile models; reserve opaque adapter payload refs for the later Houmao Execution Adapter.
- Profile specialization writes invalid project-local paths -> Reuse existing Project path resolution and external-path rejection for profile output paths and Agent Workspace refs.
- Template validation becomes expensive or brittle -> Separate cheap structured checks from optional harness checks and make diagnostics identify the source file and Isomer concept.
- Multiple topic fixtures share refs accidentally -> Add negative tests where duplicate profile ids, Agent Workspace refs, policy refs, or topic refs are rejected when they cross Research Topic boundaries.

## Migration Plan

This change is additive. Existing Project Manifests and Research Topic Config files remain valid when they omit Domain Agent Team Template and Topic Agent Team Profile refs. New validation should treat missing template/profile sections as absent optional features, not as errors.

The implementation can land in stages: add models and parsers, add template registration and validation for `deepsci-org`, add CLI inspection, extend Project Manifest and Research Topic Config parsing, add profile specialization, then add multi-topic and use-case fixtures.

Rollback is straightforward because no Workspace Runtime state or live agent state is created. Removing the new commands and optional manifest fields should return projects to Milestone 1 behavior.

## Open Questions

- Should built-in `deepsci-org` discovery be enabled by default for every Isomer Project, or should the default Project Manifest explicitly register it during `isomer-cli init` only when a flag is provided?
- Should `team-profiles specialize` write a profile file by default or require `--write` after showing a preview?
- Which exact schema version names should profile records use before Workspace Runtime and Agent Team Instance records exist?
- Should generated harness validation failures be treated as errors, or should Isomer report them as warnings when structured Isomer validation passes?
