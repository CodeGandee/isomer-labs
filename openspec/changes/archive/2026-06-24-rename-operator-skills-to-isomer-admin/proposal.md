## Why

The topic-team instantiation change introduced several project-operator orchestration skills under `skillset/research-paradigm/` with `isomer-rsch-*` names, but those skills are intended to be installed into a Project Operator Session or Operator Agent rather than into ordinary research-stage workers. Keeping operator/admin skills in the research-paradigm namespace blurs installation targets, makes Topic Service Agent profiles overbroad, and conflicts with the existing convention that `isomer-rsch-*` means reusable research-stage method.

## What Changes

- Introduce an operator/admin skill namespace under `skillset/operator/`.
- Rename operator-installable skills to `isomer-admin-<purpose>`, with matching folder names, `SKILL.md` frontmatter names, and agent manifests.
- Move project operation, Service Request routing, template inspection, topic context resolution, placeholder reconciliation, profile drafting, profile review and approval, profile materialization, and team launch orchestration skills out of `skillset/research-paradigm/` when those skills are intended for the operator surface.
- Keep research-stage method skills under `skillset/research-paradigm/` with `isomer-rsch-*` names.
- Keep Service Team-only support skills under a service-appropriate namespace instead of treating them as operator admin skills.
- Update Topic Service Master and documentation references so operator/admin skill names and service-agent skill names reflect their actual installation target.
- **BREAKING**: Active references to the moved operator skills by their old `isomer-rsch-*` names must switch to the new `isomer-admin-*` names.

## Capabilities

### New Capabilities
- `operator-admin-skills`: Defines the operator/admin skillset layout, `isomer-admin-*` naming convention, installation target, required skill manifests, validation rules, and migration mapping for Project Operator Session and Operator Agent skills.

### Modified Capabilities
- `research-paradigm-skills`: Narrows `skillset/research-paradigm/` to research-stage method skills and removes project-operator/admin orchestration skills from the `isomer-rsch-*` namespace.

## Impact

- Affected skill directories: `skillset/research-paradigm/`, new `skillset/operator/`, and existing service skill folders under `skillset/service/`.
- Affected docs and manifests: `skillset/README.md`, `skillset/research-paradigm/README.md`, Topic Service Master profile material under `teams/deepsci-mini/execplan/agents/service/`, OpenSpec docs for topic-team instantiation, and any fixtures or tests that name the moved skills.
- Affected validation: `pixi run validate-research-skills` should continue to validate research-stage skills, and a new or extended validation path should validate operator/admin skills.
- Affected runtime behavior: no runtime schema change is required, but launch/profile/service artifacts must preserve the new skill refs where they record skill installation or provenance.
