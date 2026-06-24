## Why

Isomer currently treats Domain Agent Team Template specialization as a deterministic Python transformation, but the project language expects agent-mediated inspection, placeholder reconciliation, approval, and only then profile bundle materialization or launch. This matters now because `deepsci-mini` is a placeholder-bearing Domain Agent Team Template, not an instantiated topic team, and UC-01 should prove topic-team instantiation without hardcoded product-code defaults.

The corrected domain split is important: a project operator can be any agent with Isomer system skills running from, or pointed at, an Isomer Project root. Topic-side operational support should be handled by Houmao-backed Topic Service Agents that belong to the Service Team and act through Service Requests.

## What Changes

- Add a backend-neutral Project Operator Session workflow for project discovery, topic discovery, Topic Service Agent discovery, Service Request routing, review, bundle-local approval provenance, and provenance recording.
- Add Topic Service Agent support for Topic Team Specialization: inspect a Domain Agent Team Template, inspect Effective Topic Context, build an instantiation packet, resolve or explicitly defer placeholders, plan copied template material, propose topic edits, prepare environment readiness, and present a reviewable Topic Agent Team Profile Bundle draft.
- Add Isomer-facing skills for project-operator-capable agents and Topic Service Agents: project awareness, template inspection, topic context resolution, placeholder reconciliation, copied material planning, topic edit drafting, profile bundle drafting, profile review and approval provenance preparation, profile bundle materialization, Service Request handling, and team launch orchestration.
- Change Topic Team Specialization so hardcoded Python defaults become preview-only or validation helpers; authoritative topic profile bundle creation comes from an approved instantiation packet produced through the project-operator and Topic Service Agent flow, copies approved template material into the Research Topic's one Topic Agent Team Profile Bundle under `<topic-workspace>/team-profile/`, applies topic edits there, records `approval_ref` bundle-local provenance, and keeps only a Project Manifest ref in Project Config.
- Extend Domain Agent Team Template validation and inspection to expose placeholder catalogs, instantiation schemas, role binding slots, workspace contracts, and required or optional topic-level decisions.
- Extend Workspace Runtime and Houmao adapter contracts so Agent Team Instance creation can be recorded as the result of an approved instantiation packet, not a direct hardcoded substitution path.
- Keep product code generic: no UC-01-specific profile creation in `src/`, and no template-specific hardcoded role or placeholder substitution outside generic validators and materializers.

## Capabilities

### New Capabilities

- `operator-agent-topic-team-instantiation`: Defines the Project Operator Session, Topic Service Agent, skill set, instantiation packet, user review and approval provenance, and orchestration responsibilities for Topic Team Specialization and launching Agent Team Instances.

### Modified Capabilities

- `domain-agent-team-template-registration`: Template inspection must expose placeholder catalogs, role binding slots, workspace contracts, and instantiation schemas without treating templates as launchable topic teams.
- `topic-agent-team-profile-specialization`: Topic Team Specialization must consume an approved instantiation packet, materialize exactly one authoritative profile bundle for the selected Research Topic, and reject unresolved required placeholders unless explicitly deferred with diagnostics and bundle-local approval provenance.
- `workspace-runtime-persistence`: Agent Team Instance record creation must link back to the approved Topic Agent Team Profile Bundle, instantiation packet, bundle-local approval ref, project operator provenance, and Topic Service Agent provenance when used, while rejecting competing active team launches for the same Research Topic.
- `houmao-cli-adapter-layer`: Houmao launch orchestration must consume approved profile bundle and runtime material, can launch or resolve Topic Service Agents, and must keep project-operator reasoning distinct from adapter-specific launch mechanics.
- `research-paradigm-skills`: The repository skillset must include Isomer system skills for project-operator-capable agents and topic-specific Service Team skills for Houmao-backed Topic Service Agents.

## Impact

- Affected code: `src/isomer_labs/team_templates.py`, `src/isomer_labs/team_profiles.py`, `src/isomer_labs/runtime/`, `src/isomer_labs/houmao/`, CLI surfaces for profile bundle materialization and preview, and generic validation helpers.
- Affected templates and skills: `teams/deepsci-mini/execplan/`, `skillset/`, and project-local Houmao Topic Service Agent definition material.
- Affected tests: unit tests for placeholder catalogs, copied material plans, proposed topic edits, instantiation packet validation, profile bundle materialization, deterministic packet-shaped approval fixtures, runtime provenance, Service Request provenance, and rejection of hardcoded or unresolved substitutions; manual tests for UC-01 using a project-operator and Topic Service Agent instantiation path.
- Affected docs: canonical domain language, domain-team lifecycle docs, workflow docs, Houmao adapter docs, troubleshooting, and ROADMAP wording for Milestone 6/7 acceptance.
