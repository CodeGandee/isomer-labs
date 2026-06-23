## Context

Isomer's domain language already separates **Domain Agent Team Template**, **Topic Agent Team Profile**, and **Agent Team Instance**. `teams/deepsci-mini` is therefore a reusable template, not a topic team. It contains placeholder contracts for topic refs, runtime refs, role bindings, Agent Workspace refs, policies, and expected outputs. The current Python specialization path can synthesize plausible refs, but that bypasses the project model: an Isomer-skilled project operator should inspect project context, route topic-scoped service work when needed, produce or review a specialization, obtain approval, and only then create launch/runtime material.

The corrected operator model has two layers. A **Project Operator Session** is any agent session with Isomer system skills installed and a known Isomer Project root; it is backend-neutral and does not have to be a Houmao-managed agent. A **Topic Service Agent** is a Houmao-backed Service Team member scoped to one Research Topic or Topic Workspace; it handles helper tasks such as topic environment setup, template inspection support, placeholder reconciliation support, Agent Workspace readiness, team monitoring, diagnostics, and support Artifact creation through explicit Service Requests.

The near-term pressure comes from UC-01. The UC-01 manual harness can prove generic runtime record behavior, but it should not become the authority for converting `deepsci-mini` into a concrete topic team. This change introduces the missing agent-mediated layer: project-operator skills plus Topic Service Agent skills and Houmao definitions, with Python kept to validation, persistence, and adapter boundaries.

## Goals / Non-Goals

**Goals:**

- Treat Domain Agent Team Templates as generic, placeholder-bearing material until a project-operator and Topic Service Agent workflow specializes them.
- Define a Topic Team Instantiation Packet that records how template placeholders become Topic Agent Team Profile values or approved deferrals.
- Materialize deep specialization as the Research Topic's one Topic Agent Team Profile Bundle under `<topic-workspace>/team-profile/`, including `profile.toml`, copied topic-edited template material, packet, validation, and provenance files; Project Config keeps only the discovery ref to that bundle.
- Add Isomer system skills for project discovery, topic discovery, Topic Service Agent discovery, Service Request routing, template inspection, context resolution, placeholder reconciliation, profile drafting, review Gate preparation, materialization, and launch orchestration.
- Add topic-specific Service Team skills and Houmao-compatible Topic Service Agent definition material for topic setup, instantiation support, monitoring, and diagnostics.
- Make Python code validate, persist, and launch from approved packets instead of inventing topic-specific defaults as the authoritative path.
- Preserve generic product code and keep UC-01 or `deepsci-mini` special cases out of `src/isomer_labs` except as fixture/template data.

**Non-Goals:**

- Do not implement a full autonomous research loop in this change.
- Do not require live Houmao for deterministic tests; simulated packets and Topic Service Agent artifacts are acceptable for core validation.
- Do not make a Project Operator Session require Houmao launch or a durable Operator Agent identity.
- Do not make the Execution Adapter responsible for topic reasoning, placeholder choice, or user approval.
- Do not store credentials, live process state, or rich research outputs in Topic Agent Team Profile Bundle files.
- Do not store copied topic-team source under a Topic Workspace `teams/` directory.
- Do not support multiple active topic-team profiles or competing Agent Team Instances for one Research Topic; topic-level parallelism means multiple Research Topics researched by different dedicated teams.
- Do not remove CLI preview commands if they remain explicitly preview-only and side-effect-light.

## Decisions

### Decision: Project Operator Session Is Backend-Neutral

Any agent with Isomer system skills can act as a project operator after it is pointed at the Isomer Project root or starts with that root as its current working directory. The project operator discovers the Project Manifest, topics, Topic Workspaces, templates, profiles, runtimes, and service surfaces through generic Isomer CLI or API calls. It may be Codex, Houmao, Claude, Kimi, or another capable agent surface; the durable domain term is Project Operator Session unless Isomer records a launched Operator Agent.

Alternative considered: require a durable Houmao-managed operator actor before topic-team instantiation. That would overfit project operation to one backend and conflict with the intended workflow where the user can point an existing agent at the project.

### Decision: Topic Service Agent Is the Houmao-Backed Service-Team Actor

Topic operators should be modeled as **Topic Service Agents**: topic-scoped Service Agent Instances that belong to the Service Team. They can inspect topic context, prepare work-agent environments, assist template specialization, monitor Agent Team Instances, collect diagnostics, and write support Artifacts. They do not own research decisions, Gates, Research Claims, task routing, or Agent Team Instance membership. A **Topic Service Master** is allowed as a coordination posture or Agent Profile for a Topic Service Agent, not as a separate research authority.

Alternative considered: call these actors topic operators. That name collides with Operator Agent authority and makes service support look like research control.

### Decision: Introduce a Topic Team Instantiation Packet

The agent-mediated workflow should produce a structured packet before writing a Topic Agent Team Profile. The packet names the source Domain Agent Team Template, selected Research Topic, Topic Workspace, Workspace Runtime ref, target Topic Agent Team Profile Bundle path, role bindings, policy refs, expected Artifacts, unresolved or deferred placeholders, approval state, Project Operator Session provenance, Topic Service Agent provenance when used, and validation refs. The packet does not choose among multiple profile ids for the same topic.

Alternative considered: let `specialize_topic_agent_team_profile()` keep generating defaults. That is simple, but it makes Python the hidden operator and loses the reviewable reasoning that the domain model expects.

### Decision: Store Deep Specialization Inside the Topic Workspace

Authoritative topic-team materialization should write the Research Topic's one Topic Agent Team Profile Bundle under `<topic-workspace>/team-profile/`. The bundle contains `profile.toml`, the approved instantiation packet, copied and topic-edited template material such as `execplan/`, validation outputs, and provenance refs. A Project Manifest registration points at the bundle's `profile.toml`; runtime records point back to the profile and packet provenance.

Alternative considered: keep only `.isomer-labs/team-profiles/<profile-id>.toml`. That is compact, but it cannot hold rewritten prompts, topic-specific skills, workflow contracts, or copied template material. Another rejected option was `.isomer-labs/team-profiles/<profile-id>/`, which would separate tightly coupled topic source from its Topic Workspace. A third rejected option was `<topic-workspace>/team-profiles/<profile-id>/`, which implies multiple selectable profiles under one topic. A fourth rejected option was `<topic-workspace>/teams/`, which makes profile bundles look like running teams.

### Decision: One Research Topic Has One Topic Team

Each Research Topic is handled by one topic-level team lineage. Topic-level parallelism means multiple Research Topics run at the same time, each with a different dedicated team, not one Research Topic running multiple competing teams. A materially different team strategy should become a revised profile or a new Research Topic.

Alternative considered: allow multiple Topic Agent Team Profile variants and Agent Team Instances under one Research Topic. That makes profile selection, task routing, and runtime diagnostics ambiguous.

### Decision: Use Skills for Agent Judgment, Python for Validation and Recording

Project-operator-capable agents should use explicit skills for project awareness, topic discovery, service routing, template inspection, topic context resolution, placeholder reconciliation, profile drafting, profile review Gate preparation, profile bundle materialization, and team launch orchestration. Topic Service Agents should use topic-specific Service Team skills for environment setup, template instantiation support, monitoring, diagnostics, and support Artifact writing. Python modules should expose parsers, validators, deterministic renderers, store APIs, and adapter APIs.

Alternative considered: encode orchestration as one product CLI command. That would hide the agent boundary again and make later multi-agent operation harder to test.

### Decision: Keep the Execution Adapter Below the Operator and Service Layers

Houmao remains the execution backend for launched service agents and research team agents. The Project Operator Session and Topic Service Agent prepare and approve Isomer packet/profile/runtime material, then call generic materialization or launch APIs. The Houmao adapter consumes approved runtime/profile state and records adapter refs; it does not choose placeholder substitutions or decide the research team shape.

Alternative considered: make the Houmao adapter read `teams/deepsci-mini` and generate launch profiles directly. That would collapse Isomer domain reasoning into provider-specific launch mechanics.

### Decision: Preserve Preview Paths as Non-Authoritative

Existing CLI profile specialization preview can remain, but it must label synthetic values as preview or candidate material. Authoritative materialization requires an approved instantiation packet or an explicit equivalent provided by a caller and validated against the same schema.

Alternative considered: remove preview immediately. That would reduce useful inspection behavior and make migration harder without improving the core model.

### Decision: UC-01 Should Exercise the Project-Operator and Topic-Service Path

Future UC-01 acceptance should prove that `deepsci-mini` is inspected as a Domain Agent Team Template, specialized into a Topic Agent Team Profile through project-operator and Topic Service Agent skills, approved or deterministically auto-approved in tests, then launched or simulated as an Agent Team Instance. The manual harness can still own UC-01-specific record assertions, but it should not hardcode team instantiation.

Alternative considered: keep UC-01 harness independent of agent-mediated instantiation. That would make the milestone pass while leaving the real topic-team lifecycle untested.

## Risks / Trade-offs

- Project-operator skills become too broad -> Keep each skill bounded to one artifact or decision: discover, inspect, resolve, route service, reconcile, draft, review, materialize, launch.
- Topic Service Agents accidentally gain research authority -> Keep Service Request scopes explicit and validation rules clear that Topic Service Agents cannot own Research Claims, Gates, task routing, or Agent Team Instance membership.
- Tests become dependent on live Houmao -> Use deterministic packet fixtures and simulated Topic Service Agent outputs for unit/manual tests; keep live launch optional and gated.
- Packets and copied material duplicate some template/profile fields -> Treat the bundle as the authoritative topic-specialized design material, and keep the packet as provenance and review material inside that bundle.
- Placeholder deferrals hide launch blockers -> Require explicit deferred-placeholder diagnostics and review state; block launch-facing operations when required launch placeholders remain unresolved.
- Existing CLI users depend on preview defaults -> Keep preview output, but mark it as candidate and require packet-backed materialization for authoritative creation.

## Migration Plan

1. Update the canonical domain language with Project Operator Session, Topic Service Agent, and Topic Service Master terminology.
2. Add packet schema, validators, and template placeholder inspection for `deepsci-mini` and generic templates.
3. Add Isomer system skills under the repository skillset for project-operator behavior and Topic Service Agent support.
4. Add Houmao launch/profile definition material for Topic Service Agents, including a Topic Service Master posture when a topic needs one coordinating service actor.
5. Update profile specialization APIs so they accept a validated packet, copy editable template material into a Topic Workspace Topic Agent Team Profile Bundle, and treat old synthetic preview generation as preview-only.
6. Update Agent Team Instance creation and Houmao launch flows to link runtime records to approved packet/profile bundle provenance and Topic Service Agent provenance when used.
7. Revise UC-01 manual acceptance to use a deterministic project-operator and Topic Service Agent packet path before creating or simulating the team.
8. Keep rollback simple: generated packet/profile bundle material is additive and can be ignored by older preview-only flows, but launch-facing tests should require the new provenance once this change lands.

## Open Questions

- Should packet approval be stored as a Gate or Decision Record immediately, or as profile provenance until a richer approval model lands?
- Should the first implementation materialize a Topic Service Agent fixture before launching a real Houmao Topic Service Agent?
