## Why

Isomer can prepare topic workspaces, topic-main repositories, semantic storage labels, and research record surfaces without launching a formal Topic Agent Team, but the operator-facing path still assumes either one shared manual cwd or full team specialization. Users need a first-class human-orchestrated research workflow where the Project Operator can register multiple manually controlled Topic Actors, such as Claude Code, Codex, Houmao-backed agents, or a mixed set, each with its own Topic Actor Workspace while still sharing the same Topic Workspace and durable research records.

## What Changes

- Add a human-orchestrated manual research workflow for preparing a Research Topic with a default `operator` Topic Actor Workspace unless the user explicitly opts out, zero or more additional Topic Actors managed by the Topic Workspace Manager, and zero or more formal Agent Team Instance members.
- Add Topic Actor bindings to the Topic Workspace Manifest so manually controlled workers have stable topic-local names, enum-validated actor kind, role kind, runtime kind, controller metadata, worktree branch, default cwd label, status, and optional adapter refs, with `custom.*` escape hatches for future runtimes.
- Add actor-scoped semantic workspace labels such as `topic.actors.workspace` so human-orchestrated workers can use separate Topic Actor Workspaces under `<topic-workspace>/actors/<topic-actor-name>` instead of sharing `topic.repos.main`.
- Keep `topic.repos.main` as the only supported Git anchor and integration surface for Topic Actor Workspace worktrees in the first pass, and do not support alternate worktree source repositories in this change.
- Split common topic preparation from team specialization so topic registration, topic intent, topic environment setup, runtime readiness, topic-main readiness, Topic Actor Workspace management, and research storage bootstrapping can be reused by manual actor and formal team workflows.
- Generalize the v2 research workspace bootstrap so it validates base topic readiness, operator/Topic Actor readiness, and optional formal team readiness as composable layers rather than mutually exclusive manual/team modes.
- Preserve storage boundaries: accepted research state goes through semantic research record labels, source code and notebooks live in actor or agent worktrees until recorded or integrated, and local temporary surfaces remain disposable.
- Update operator routing so requests like "prepare this topic for manual research" route Topic Actor CRUD and Topic Actor Workspace materialization through the Topic Workspace Manager's `project topic-actors ...` surface without implying Topic Agent Team specialization, while still allowing formal teams to be added later or coexist.
- Store authoritative per-actor start packs as Topic Workspace research records, with small actor-local copies or pointers for worker convenience.
- Defer formal adoption of Topic Actor-produced work into Agent Instance or Agent Team Instance identity to a later change.

## Capabilities

### New Capabilities

- `manual-research-topic-workflow`: Covers operator-prepared human-orchestrated research using prepared Topic Actors, Topic Actor Workspaces, v2 research skills, semantic storage bindings, and no required formal Topic Agent Team.

### Modified Capabilities

- `isomer-admin-project-manager-skill`: Route manual or human-orchestrated research preparation to common topic preparation, Topic Workspace Manager actor management, and the human-orchestrated research session while keeping project initialization, topic listing, runtime preparation, and team specialization handoffs explicit.
- `isomer-documentation-system-guide`: Update canonical domain language so Topic Actor Workspace is a third managed workspace type alongside Topic Workspace and Agent Workspace.
- `topic-workspace-manifest`: Add Topic Actor bindings and default Topic Actor Workspace semantic labels that can be queried and materialized without creating formal Agent Instance records.
- `workspace-path-resolution`: Resolve actor-scoped semantic labels through a Topic Actor selector, environment, cwd, or lifecycle refs, separately from formal `agent.*` Effective Agent Context.
- `topic-team-specialization-module-skill`: Narrow team specialization to consume prepared topic and actor-aware context, then produce team/profile/Agent Workspace material without deleting or replacing manually orchestrated Topic Actors.
- `research-paradigm-skills`: Allow v2 research skills and the research workspace bootstrap to operate from Topic Actor Workspaces, topic-main, or formal Agent Workspaces by reading explicit readiness and skill-local placeholder binding material, with a topic-level binding index as readiness evidence.
- `topic-workspace-manager-skill`: Make the workspace manager responsible for Topic Actor CRUD, Topic Actor Workspace materialization or repair, actor-scoped path diagnostics, and topology inspection across Topic Actor Workspaces, formal Agent Workspaces, and topic-main, while keeping topic-main, topic env readiness, and research records owned by their existing workflows.
- `topic-main-development-repository`: Define `topic.repos.main` as the Git anchor and integration surface for topic worktrees rather than the universal manual-agent cwd.
- `research-recording-contracts`: Allow accepted research artifacts written by Topic Actors, Project Operator Sessions, Operator Agents, or formal Agent Instances, with queryable actor metadata and without requiring Agent Team Instance identity.

## Impact

- Affects operator skills under `skillset/operator/`, especially project management, topic workspace management, manual research preparation, and topic team specialization.
- Affects canonical domain language, Topic Workspace Manifest parsing, validation, rendering, semantic label catalog, path resolution, and CLI path commands for actor-scoped labels.
- Affects service/research skill routing through topic environment setup, research workspace bootstrap, v2 research placeholder binding references, topic-level binding index generation, and actor start-pack recording.
- Affects research storage guidance in `context/plans/refactor-isomer-rsch-skills/required-storage-support.md` and any generated actor start-pack or readiness documentation.
- May require CLI validation and tests around `project topic-actors ...`, default `operator` Topic Actor Workspace creation, actor path queries, runtime audit records, research record actor metadata, and coexistence with formal Agent Team Instance material.
