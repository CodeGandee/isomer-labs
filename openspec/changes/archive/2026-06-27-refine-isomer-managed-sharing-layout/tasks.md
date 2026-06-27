## 1. Documentation and Domain Language

- [x] 1.1 Revise `docs/topic-workspace-definition.md` so the standard layout uses `repos/topic-main/isomer-managed/{tracked,agent-owned,topic-owned,links}/`, explains each directory with comments, and removes `.isomer-agent/` from the current layout.
- [x] 1.2 Update `docs/concepts.md`, `docs/runtime-and-files.md`, `docs/troubleshooting.md`, and related docs so worker-visible Isomer material lives under `isomer-managed/` and legacy `.isomer-agent/` or top-level `topic-main` collaboration paths appear only as migration diagnostics.
- [x] 1.3 Update `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md` so Agent Runtime, Worker Visibility Boundary, Peer Read Access, and Topic Main Repository language uses `isomer-managed/` and the tracked, agent-owned, topic-owned, and generated-link regimes.
- [x] 1.4 Update documentation validation or stale-term checks so `.isomer-agent/` and top-level `repos/topic-main/{shared,artifacts,tasks,runs,views,logs,tools}` guidance fails outside explicit migration notes.

## 2. Path Resolution and Runtime Records

- [x] 2.1 Update `src/isomer_labs/paths.py` to expose `topic_main_isomer_managed`, `topic_main_tracked*`, `agent_isomer_managed`, `agent_owned`, `agent_runtime`, `agent_artifacts`, `agent_scratch`, `agent_logs`, `agent_public_share`, `agent_inbox`, `agent_topic_readonly`, `agent_topic_writable`, and `agent_links` surfaces.
- [x] 2.2 Update supported `ISOMER_*` path overrides and diagnostics so legacy agent support variables map to `isomer-managed/agent-owned/*` with compatibility warnings.
- [x] 2.3 Update Workspace Runtime initialization and path-plan persistence to record `repos/topic-main/isomer-managed/` and owner-preserved `records/*` paths without creating per-agent untracked share directories before Agent Workspace setup.
- [x] 2.4 Update Agent Workspace runtime or lifecycle metadata so standard worktree records include topic-local agent name, branch namespace, `isomer-managed/` path plan, and boundary refs.
- [x] 2.5 Add runtime validation diagnostics for missing `isomer-managed/` support paths, stale `.isomer-agent/` refs, unsafe generated links, and unpromoted dependencies on untracked agent-owned or topic-owned material.

## 3. Topic Workspace Manager Skill

- [x] 3.1 Update `skillset/operator/isomer-admin-topic-workspace-mgr/SKILL.md` and reference pages to describe `isomer-managed/` as the standard worker-facing Isomer namespace and to stop creating `.isomer-agent/`.
- [x] 3.2 Update workspace preparation workflow text to create or validate `isomer-managed/.gitignore`, `tracked/{shared,artifacts,tasks,runs,views,tools,boundaries,manifests}/`, `agent-owned/{runtime,scratch,logs,artifacts,public,inbox}/`, `topic-owned/{readonly,writable}/`, and `links/`.
- [x] 3.3 Update validation workflow text to report legacy top-level `topic-main` Isomer directories, legacy `.isomer-agent/`, missing ignore policy, unsafe links, missing topic-owned writable policy, tracked conflict markers, and owner/reader split issues without repairing silently.
- [x] 3.4 Update summary and boundary output guidance so it reports agent names, worktree branches, `isomer-managed/` regime status, generated links, blockers, and next operator action.

## 4. Topic Team Specialization Integration

- [x] 4.1 Update `skillset/operator/isomer-admin-topic-team-specialize/references/setup-agent-workspace.md` to delegate Git worktree and `isomer-managed/` preparation to `isomer-admin-topic-workspace-mgr`.
- [x] 4.2 Update Topic Team Specialization validation and final-summary guidance so stale `.isomer-agent/` setup evidence no longer satisfies static Agent Workspace readiness.
- [x] 4.3 Update `skillset/operator/README.md` and any operator skill summaries that still describe `.isomer-agent/` or top-level `topic-main` Isomer collaboration directories as current layout.

## 5. Tests and Validation

- [x] 5.1 Update unit tests for path preview and Workspace Path Resolution to assert the new `isomer-managed/` surfaces and legacy compatibility diagnostics.
- [x] 5.2 Update skillset validation tests to require `isomer-managed/` guidance in topic workspace manager and Topic Team Specialization skills.
- [x] 5.3 Add or update docs validation tests for stale workspace path language.
- [x] 5.4 Run `openspec validate refine-isomer-managed-sharing-layout --strict`.
- [x] 5.5 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
