## Why

`isomer-admin-topic-workspace-mgr` now manages more than workspace topology: it handles Topic Actor topology, Agent Workspace planning, boundary summaries, package installation, and diagnostics for an initialized Research Topic. Renaming and broadening it to `isomer-admin-topic-mgr` makes the operator surface match its actual responsibility while keeping Topic initialization owned by `isomer-admin-topic-creator`.

## What Changes

- **BREAKING**: Introduce `skillset/operator/isomer-admin-topic-mgr` as the canonical operator skill for managing initialized Research Topics after creator handoff.
- **BREAKING**: Rename and regroup the public subcommands by scope: status, storage, actors, agent team topology, environment mutation, and environment verification.
- Replace old workspace-manager command names such as `resolve-workspace`, `manage-actors`, `plan-agents`, `create-worktrees`, `validate-worktrees`, `install-packages`, and `topic-workspace` with scope-prefixed topic-manager commands.
- Add explicit environment mutation commands for install, update, and remove package requests against the selected Topic Workspace Pixi environment.
- Add explicit environment verification commands for Topic Workspace, Topic Actor, and Agent Workspace readiness checks, while preserving service-skill delegation for gate-driven setup.
- Keep `isomer-admin-topic-creator` as the initialization front door and route lower-level initialized-topic management to the new topic manager.
- Update operator, service, topic-team-specialization, project-manager, and research-paradigm guidance that currently points to `isomer-admin-topic-workspace-mgr`.
- Keep an implementation-level compatibility wrapper or migration route for old invocations during the transition, unless validation proves no active routes need it.

## Capabilities

### New Capabilities
- `topic-manager-skill`: Defines the `isomer-admin-topic-mgr` operator skill for initialized-topic management, scoped subcommands, package/environment mutation, environment verification, and compatibility routing from the old workspace-manager surface.

### Modified Capabilities
- `topic-workspace-manager-skill`: Retire the old full workspace-manager capability and reduce it to a deprecated compatibility wrapper for the new topic manager.
- `operator-admin-skills`: Replace the active workspace-manager inventory with the topic-manager inventory and validation expectations.
- `topic-creator-skill`: Route post-initialization actor, storage, environment, and topic-management work to `isomer-admin-topic-mgr` instead of `isomer-admin-topic-workspace-mgr`.
- `isomer-service-env-setup-skill`: Route ad hoc package-add, update, remove, or package verification requests to `isomer-admin-topic-mgr` environment subcommands while keeping full gate-driven setup in the service.
- `research-paradigm-skills`: Update v2 missing-package and setup-blocker handoffs to the new topic-manager environment route without giving direct install or local virtualenv instructions.
- `topic-team-specialization-module-skill`: Route optional topology inspection, branch helpers, boundary summaries, stale topology repair, and topic-team workspace diagnostics to the new topic-manager team and storage commands.
- `isomer-admin-project-manager-skill`: Update project-manager handoff text so initialized-topic operations go to `isomer-admin-topic-mgr`.
- `manual-research-topic-workflow`: Update Topic Actor management handoffs to the new topic-manager actor commands.

## Impact

- Affects `skillset/operator/isomer-admin-topic-workspace-mgr/`, adding or replacing it with `skillset/operator/isomer-admin-topic-mgr/` and a compatibility route for old invocations.
- Affects `skillset/manifest.toml`, `skillset/operator/README.md`, operator and service skill references, research-paradigm v2 package-routing text, and topic-team specialization guidance.
- Affects `scripts/validate_skillsets.py` so validation expects the new skill name, metadata, grouped subcommands, reference pages, output terms, and guardrails.
- Affects OpenSpec capabilities that currently name the old workspace-manager skill and old subcommands.
