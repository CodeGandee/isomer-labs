## Why

The current `isomer-srv-env-setup` skill already prepares a Pixi environment for a Topic Workspace, but its name and some operator handoffs make it easy to treat environment setup as part of Topic Agent Team structure. Topic Workspace development environment readiness should be available before, after, or without Topic Team Specialization, because it only needs to prove that a single agent/operator can run the commands required by the research gate.

## What Changes

- **BREAKING**: Rename the service skill from `isomer-srv-env-setup` to `isomer-srv-topic-env-setup`.
- **BREAKING**: Rename public service subcommands to topic-env names: `resolve-topic-workspace`, `read-env-gate`, `ensure-topic-repos`, `derive-env-gate`, `install-topic-deps`, `verify-env-gate`, and `setup-topic-env`.
- Refocus the service skill contract on Topic Workspace development environment setup through Pixi, `env-gate.md`, and the derived `isomer-env-gate.md`.
- Make absent Topic Agent Team Profile material, absent `team-profile/`, absent Agent Team Instance records, and unknown agent roles non-blocking for environment setup.
- Update topic-team operator delegation to call the renamed service and treat environment setup as durable Topic Workspace preparation, not as a team-profile-dependent phase.
- Preserve the existing Pixi-first enclosure ladder, source-gate workflow, repo handling, dependency inference, and verification semantics.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `isomer-service-env-setup-skill`: Rename the service skill and public subcommands, and require Topic Workspace environment setup to be independent from Topic Agent Team Profile and Agent Team Instance structure.
- `isomer-service-env-setup-enclosure`: Update the enclosure policy references to the renamed skill while preserving the Pixi-first, auditable, no-sudo boundary.
- `topic-team-specialization-module-skill`: Update operator delegation to use the renamed service and allow Topic Workspace environment setup without requiring team-profile material as a predecessor.

## Impact

- Affected skill bundle: `skillset/service/isomer-srv-env-setup` will move to `skillset/service/isomer-srv-topic-env-setup`.
- Affected service skill docs: service `SKILL.md`, `agents/openai.yaml`, reference page names, examples, output fields, and service README entries.
- Affected operator skill docs: `skillset/operator/isomer-admin-topic-team-specialize` references that delegate to the env setup service or describe predecessor requirements for `setup-topic-env`.
- Affected validation: repo skillset validation and any tests that assert service skill names, subcommands, reference file names, README entries, or operator delegation text.
