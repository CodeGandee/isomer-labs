## Why

Topic initialization is currently correct internally but hard to operate from a blank state: users must jump across project management, topic preparation, workspace topology, manual session, and research bootstrap skills without a clear next-step ladder. A new `isomer-admin-topic-creator` skill should become the canonical front door for creating a Research Topic and making its Topic Workspace fully available for manual research.

## What Changes

- Add `isomer-admin-topic-creator` as the user-facing operator skill for end-to-end topic initialization from empty or partial Project state to manual-research-ready Topic Workspace.
- Give the skill command-style subcommands: `help`, `plan`, `create`, `ensure-project`, `define-topic`, `register-topic`, `init-runtime`, `setup-topic-env`, `setup-actors`, `bootstrap-research`, `start-manual-research`, `status`, and `repair`.
- Migrate user-facing initialization guidance from `isomer-admin-project-mgr`, `isomer-admin-topic-prepare`, and `isomer-admin-manual-research-session` into the new creator skill while keeping those existing skills available for compatibility and delegated lower-level steps.
- Mark `isomer-admin-topic-prepare` and `isomer-admin-manual-research-session` as deprecated for direct user invocation in their YAML frontmatter, with `replaced_by: isomer-admin-topic-creator`.
- Update Project Manager routing so blank-state topic creation and manual-research setup route to `isomer-admin-topic-creator`, while pure Project lifecycle operations remain in `isomer-admin-project-mgr`.
- Update operator docs, skill manifest grouping, installed skill symlink expectations, validation logic, and tests to recognize the new skill and the compatibility deprecation fields.
- Preserve lower-level ownership boundaries: Topic Actor topology remains delegated to `isomer-admin-topic-workspace-mgr`, topic environment setup remains delegated to `isomer-srv-topic-env-setup`, v2 research bootstrap remains delegated to `isomer-rsch-workspace-mgr-v2`, and formal Topic Team Specialization remains delegated to `isomer-admin-topic-team-specialize`.

## Capabilities

### New Capabilities

- `topic-creator-skill`: Defines the new `isomer-admin-topic-creator` operator skill, its commands, readiness ladder, output contract, guardrails, and compatibility delegation model.

### Modified Capabilities

- `operator-admin-skills`: Add `isomer-admin-topic-creator` to the active operator inventory and mark `isomer-admin-topic-prepare` plus `isomer-admin-manual-research-session` as compatibility skills deprecated for direct user invocation.
- `isomer-admin-project-manager-skill`: Route topic creation and manual-research setup to `isomer-admin-topic-creator` rather than asking users to invoke separate topic-preparation and manual-session skills.
- `manual-research-topic-workflow`: Name `isomer-admin-topic-creator` as the user-facing owner for manual-research-ready topic initialization while preserving the existing Topic Actor, research bootstrap, and start-pack semantics.

## Impact

- Affected skill bundles: new `skillset/operator/isomer-admin-topic-creator/`, plus frontmatter and routing updates in `isomer-admin-topic-prepare`, `isomer-admin-manual-research-session`, and `isomer-admin-project-mgr`.
- Affected docs and manifests: `skillset/operator/README.md`, `skillset/manifest.toml`, and `.kimi-code/skills/` symlink installation expectations.
- Affected validators and tests: operator skill validation, manifest validation, compatibility deprecation checks, and tests covering manual research topic workflows.
- Affected specs: new `topic-creator-skill`; modified `operator-admin-skills`, `isomer-admin-project-manager-skill`, and `manual-research-topic-workflow`.
