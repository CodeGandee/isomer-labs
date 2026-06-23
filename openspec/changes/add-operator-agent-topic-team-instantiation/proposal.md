## Why

Isomer currently treats Domain Agent Team Template specialization as a deterministic Python transformation, but the project language says an Operator Agent should inspect a reusable template, resolve topic placeholders, ask for approval, and only then launch or resolve an Agent Team Instance. This matters now because `deepsci-mini` is a placeholder-bearing Domain Agent Team Template, and UC-01 should prove agent-mediated topic-team instantiation rather than hardcoded profile defaults.

## What Changes

- Add an Operator Agent orchestration capability for topic-team instantiation: inspect a Domain Agent Team Template, inspect Effective Topic Context, build an instantiation packet, resolve or explicitly defer placeholders, and present a reviewable Topic Agent Team Profile draft.
- Add Isomer-facing skills for the Houmao-backed Operator Agent: template inspection, topic context resolution, placeholder reconciliation, topic profile drafting, profile review Gate preparation, profile materialization, and team launch orchestration.
- Change Topic Agent Team Profile specialization so hardcoded Python defaults become preview-only or validation helpers; authoritative topic profile creation comes from an Operator Agent produced instantiation packet.
- Extend Domain Agent Team Template validation and inspection to expose placeholder catalogs, instantiation schemas, role binding slots, workspace contracts, and required/optional topic-level decisions.
- Extend Workspace Runtime and Houmao adapter contracts so Agent Team Instance creation can be recorded as the result of an approved Operator Agent instantiation packet, not a direct hardcoded substitution path.
- Keep product code generic: no UC-01-specific profile creation in `src/`, and no template-specific hardcoded role or placeholder substitution outside generic validators and materializers.

## Capabilities

### New Capabilities

- `operator-agent-topic-team-instantiation`: Defines the Operator Agent workflow, skill set, instantiation packet, user review Gate, and orchestration responsibilities for specializing Domain Agent Team Templates into Topic Agent Team Profiles and launching Agent Team Instances.

### Modified Capabilities

- `domain-agent-team-template-registration`: Template inspection must expose placeholder catalogs, role binding slots, workspace contracts, and instantiation schemas without treating templates as launchable topic teams.
- `topic-agent-team-profile-specialization`: Profile specialization must consume an Operator Agent instantiation packet and reject unresolved required placeholders unless explicitly deferred with diagnostics and approval context.
- `workspace-runtime-persistence`: Agent Team Instance record creation must link back to the approved Topic Agent Team Profile and Operator Agent instantiation packet/provenance.
- `houmao-cli-adapter-layer`: Houmao launch orchestration must consume approved profile/runtime material and keep Operator Agent orchestration distinct from adapter-specific launch mechanics.
- `research-paradigm-skills`: The repository skillset must include Isomer Operator Agent skills for topic-team instantiation and orchestration work.

## Impact

- Affected code: `src/isomer_labs/team_templates.py`, `src/isomer_labs/team_profiles.py`, `src/isomer_labs/runtime/`, `src/isomer_labs/houmao/`, CLI surfaces for profile/materialization preview, and generic validation helpers.
- Affected templates and skills: `teams/deepsci-mini/execplan/`, `skillset/`, and any project-local Houmao/Isomer Operator Agent definition material.
- Affected tests: unit tests for placeholder catalogs, instantiation packet validation, profile materialization, runtime provenance, and rejection of hardcoded or unresolved substitutions; manual tests for UC-01 using an Operator Agent instantiation path.
- Affected docs: domain-team lifecycle docs, workflow docs, Houmao adapter docs, troubleshooting, and ROADMAP wording for Milestone 6/7 acceptance.
