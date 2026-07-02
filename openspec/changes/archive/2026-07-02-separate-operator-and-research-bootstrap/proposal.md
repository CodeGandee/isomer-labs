## Why

Operator skills currently leak research-paradigm v2 concerns into topic setup: `isomer-admin-topic-creator` delegates to `isomer-rsch-workspace-mgr-v2`, reports v2 placeholder binding readiness, and older deprecated manual-session guidance writes research-specific start packs. This blurs the boundary between preparing Topic Actor workspaces and preparing a specific research paradigm.

We need to retire the deprecated compatibility skills and make the boundary explicit: operator skills prepare Project, Topic Workspace, Topic Actor, and cwd topology; research-paradigm skills prepare v2-specific storage, placeholders, and research recording guidance.

## What Changes

- **BREAKING**: Retire `skillset/operator/isomer-admin-topic-prepare` as an invokable/delegated operator skill.
- **BREAKING**: Retire `skillset/operator/isomer-admin-manual-research-session` as an invokable/delegated operator skill.
- Remove operator-skill references to research-paradigm v2 specifics, including selected v2 skill sets, `placeholder-bindings.md`, v2 bootstrap records, accepted-research-artifact command shapes, and delegation to `isomer-rsch-workspace-mgr-v2`.
- Reframe `isomer-admin-topic-creator` as a v2-independent topic preparation front door ending at Topic Workspace and Topic Actor readiness.
- Fold the v2-independent useful parts of old start packs into `setup-actors` as actor workspace onboarding material: actor identity, cwd, branch, support labels, integration surface, boundary notes, verification evidence, and blockers.
- Move all v2-specific research bootstrap ownership to `skillset/research-paradigm/v2/isomer-rsch-workspace-mgr-v2`.
- Update operator documentation and project-manager routing so normal topic preparation uses `isomer-admin-topic-creator fast-forward`, `step-by-step`, `run-to`, `status`, or `repair`, with no stale `create`, `plan`, or `start-manual-research` subcommands.
- Update formal topic-team specialization references so reusable common preparation means Topic Creator / Topic Workspace readiness evidence, not retired `isomer-admin-topic-prepare` output.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `operator-admin-skills`: Operator skills must stay independent of research-paradigm v2 setup and must no longer list retired compatibility skills as supported operator skills.
- `manual-research-topic-workflow`: Human-orchestrated preparation must produce v2-independent Topic Actor readiness and actor onboarding material, while research-paradigm bootstrap belongs to the v2 research workspace manager.
- `research-paradigm-skills`: `isomer-rsch-workspace-mgr-v2` is the owner for v2 placeholder binding, research storage, selected v2 skill readiness, and accepted-research-artifact command guidance.
- `topic-workspace-manager-skill`: Topic Workspace Manager remains the owner for Topic Actor topology and actor-scoped path diagnostics, but it must not own research handoff records or v2 bootstrap.

## Impact

- Affected skill docs under `skillset/operator/`, especially `isomer-admin-topic-creator`, `isomer-admin-project-mgr`, `isomer-admin-topic-workspace-mgr`, `isomer-admin-topic-team-specialize`, and `skillset/operator/README.md`.
- Retired folders: `skillset/operator/isomer-admin-topic-prepare/` and `skillset/operator/isomer-admin-manual-research-session/`.
- Affected v2 research skill docs under `skillset/research-paradigm/v2/isomer-rsch-workspace-mgr-v2/`.
- Affected validation may include operator skill inventory checks, stale reference checks, and any docs tests that scan active skill references.
