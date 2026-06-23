## Why

Isomer currently treats Domain Agent Team Template specialization as a deterministic Python transformation, but the project language expects agent-mediated inspection, placeholder reconciliation, approval, and only then profile materialization or launch. This matters now because `deepsci-mini` is a placeholder-bearing Domain Agent Team Template, not an instantiated topic team, and UC-01 should prove topic-team instantiation without hardcoded product-code defaults.

The corrected domain split is important: a project operator can be any agent with Isomer system skills running from, or pointed at, an Isomer Project root. Topic-side operational support should be handled by Houmao-backed Topic Service Agents that belong to the Service Team and act through Service Requests.

## What Changes

- Add a backend-neutral Project Operator Session workflow for project discovery, topic discovery, Topic Service Agent discovery, Service Request routing, review, approval, and provenance recording.
- Add Topic Service Agent support for topic-team instantiation: inspect a Domain Agent Team Template, inspect Effective Topic Context, build an instantiation packet, resolve or explicitly defer placeholders, prepare environment readiness, and present a reviewable Topic Agent Team Profile draft.
- Add Isomer-facing skills for project-operator-capable agents and Topic Service Agents: project awareness, template inspection, topic context resolution, placeholder reconciliation, topic profile drafting, profile review Gate preparation, profile materialization, Service Request handling, and team launch orchestration.
- Change Topic Agent Team Profile specialization so hardcoded Python defaults become preview-only or validation helpers; authoritative topic profile creation comes from an approved instantiation packet produced through the project-operator and Topic Service Agent flow.
- Extend Domain Agent Team Template validation and inspection to expose placeholder catalogs, instantiation schemas, role binding slots, workspace contracts, and required or optional topic-level decisions.
- Extend Workspace Runtime and Houmao adapter contracts so Agent Team Instance creation can be recorded as the result of an approved instantiation packet, not a direct hardcoded substitution path.
- Keep product code generic: no UC-01-specific profile creation in `src/`, and no template-specific hardcoded role or placeholder substitution outside generic validators and materializers.

## Capabilities

### New Capabilities

- `operator-agent-topic-team-instantiation`: Defines the Project Operator Session, Topic Service Agent, skill set, instantiation packet, user review Gate, and orchestration responsibilities for specializing Domain Agent Team Templates into Topic Agent Team Profiles and launching Agent Team Instances.

### Modified Capabilities

- `domain-agent-team-template-registration`: Template inspection must expose placeholder catalogs, role binding slots, workspace contracts, and instantiation schemas without treating templates as launchable topic teams.
- `topic-agent-team-profile-specialization`: Profile specialization must consume an approved instantiation packet and reject unresolved required placeholders unless explicitly deferred with diagnostics and approval context.
- `workspace-runtime-persistence`: Agent Team Instance record creation must link back to the approved Topic Agent Team Profile, instantiation packet, project operator provenance, and Topic Service Agent provenance when used.
- `houmao-cli-adapter-layer`: Houmao launch orchestration must consume approved profile/runtime material, can launch or resolve Topic Service Agents, and must keep project-operator reasoning distinct from adapter-specific launch mechanics.
- `research-paradigm-skills`: The repository skillset must include Isomer system skills for project-operator-capable agents and topic-specific Service Team skills for Houmao-backed Topic Service Agents.

## Impact

- Affected code: `src/isomer_labs/team_templates.py`, `src/isomer_labs/team_profiles.py`, `src/isomer_labs/runtime/`, `src/isomer_labs/houmao/`, CLI surfaces for profile/materialization preview, and generic validation helpers.
- Affected templates and skills: `teams/deepsci-mini/execplan/`, `skillset/`, and project-local Houmao Topic Service Agent definition material.
- Affected tests: unit tests for placeholder catalogs, instantiation packet validation, profile materialization, runtime provenance, Service Request provenance, and rejection of hardcoded or unresolved substitutions; manual tests for UC-01 using a project-operator and Topic Service Agent instantiation path.
- Affected docs: canonical domain language, domain-team lifecycle docs, workflow docs, Houmao adapter docs, troubleshooting, and ROADMAP wording for Milestone 6/7 acceptance.
