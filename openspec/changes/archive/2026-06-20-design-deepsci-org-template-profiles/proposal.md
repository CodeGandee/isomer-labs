## Why

Milestones 2 and 3 need to turn `teams/deepsci-org/execplan/` from generated authoring material into an Isomer-visible Domain Agent Team Template that can be validated, registered, and specialized for concrete Research Topics. This is the next useful design step because later Houmao launch work depends on clean template/profile boundaries and on proving that multiple Research Topics can specialize the same template without leaking topic-specific refs.

## What Changes

- Introduce Domain Agent Team Template registration and validation for `deepsci-org`, including manifest discovery, execplan package checks, role and Workflow Stage mapping, placeholder-boundary checks, and template-level CLI inspection.
- Introduce Topic Agent Team Profile specialization from a registered Domain Agent Team Template, including Effective Topic Context input, selected roles, policy refs, Capability Binding refs, Skill Binding Projection refs, Agent Workspace refs, expected Artifacts, and multi-topic fixture validation.
- Extend Project Manifest, Research Topic Config, and CLI project-discovery behavior so Projects can declare Domain Agent Team Template refs and topic defaults for Topic Agent Team Profiles without launching Agent Team Instances.
- Keep Houmao-specific launch, mailbox, gateway, notifier, specialist, recipe, launch dossier, and managed-agent details out of generic Isomer records during these milestones.
- Add static fixtures for UC-01, UC-02, UC-03, and UC-05 that exercise different `deepsci-org` Topic Agent Team Profiles without starting agents.

## Capabilities

### New Capabilities

- `domain-agent-team-template-registration`: Discovery, registration, validation, and inspection of reusable Domain Agent Team Templates, with `teams/deepsci-org/execplan/` as the seed template.
- `topic-agent-team-profile-specialization`: Creation and validation of topic-specific Topic Agent Team Profiles from registered Domain Agent Team Templates before any Agent Team Instance is launched.

### Modified Capabilities

- `isomer-cli-project-discovery`: Project Manifest, Research Topic Config, Effective Topic Context, and CLI command-surface behavior expand to carry Domain Agent Team Template refs, default Topic Agent Team Profile refs, and profile validation inputs.

## Impact

- Affected code: `src/isomer_labs/` manifest models, topic config models, validation logic, CLI commands, rendering, and fixtures.
- Affected specs: new specs for template registration and topic profile specialization, plus a delta to `openspec/specs/isomer-cli-project-discovery/spec.md`.
- Affected repository material: `teams/deepsci-org/execplan/` becomes a validated seed Domain Agent Team Template source; `.imsight-arts/project-explore/use-cases/` informs profile fixtures.
- Affected systems: future Houmao Execution Adapter work gains validated template/profile inputs but remains out of scope for this change.
