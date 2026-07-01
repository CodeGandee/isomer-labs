## Why

The v2 research skills now name durable handoff objects through per-skill placeholder registries, but a fully initialized Topic Workspace still lacks a research-specific bootstrap pass that prepares the storage surfaces and placeholder binding map those skills should use. Without that pass, each v2 skill is left to interpret labels, directories, and generated links on its own after Topic Team Specialization.

## What Changes

- Add a new `isomer-rsch-workspace-mgr-v2` research-paradigm skill that runs after Topic Team Specialization and Topic Workspace initialization.
- Define a consistent placeholder registry for the manager using the same `migrate/placeholders.md` pattern as the other v2 skills.
- Have the manager validate existing and planned research storage semantic labels, prepare or describe required directories, and emit a bootstrap report, agent access plan, placeholder binding registry, validation report, and blocker record.
- Document the manager's boundary relative to `isomer-admin-topic-workspace-mgr`, Topic Service Master, Project Operator Session, Operator Agent, and the ordinary v2 research skills.
- Update research skill validation so the new v2 skill is recognized and its placeholder contract is checked.

## Capabilities

### New Capabilities

### Modified Capabilities

- `research-paradigm-skills`: Adds the `isomer-rsch-workspace-mgr-v2` skill and its post-specialization workspace bootstrap contract.

## Impact

- Affected skillset material: `skillset/research-paradigm/v2/`, `isomer-rsch-shared-v2` references, and the research-paradigm storage support plan.
- Affected validation: `scripts/validate_research_paradigm_skillset.py` and unit tests for the expected v2 skill list.
- No runtime API or database implementation is required by this change; the manager may describe planned storage labels as blockers until the platform implements them.
