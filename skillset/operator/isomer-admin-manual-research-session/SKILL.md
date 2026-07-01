---
name: isomer-admin-manual-research-session
description: Start or repair a human-orchestrated research session over a prepared Topic Workspace by selecting Topic Actors, delegating actor workspace readiness to the Topic Workspace Manager, running v2 research bootstrap, and writing per-actor start packs.
---

# Isomer Admin Manual Research Session

Use this operator skill when the user wants to conduct research manually or with several manually controlled agents, including mixed Codex, Claude Code, shell, or Houmao-backed workers, without requiring a formal Topic Agent Team. This skill consumes common preparation evidence from `isomer-admin-topic-prepare`, delegates all Topic Actor CRUD and Topic Actor Workspace materialization to `isomer-admin-topic-workspace-mgr`, runs `isomer-rsch-workspace-mgr-v2` over the selected topology, and writes authoritative per-actor start packs as Topic Workspace research records with actor-local copies or pointers for startup convenience.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Consume prepared-topic evidence**. Verify the selected Research Topic, Topic Workspace, Workspace Runtime, topic environment readiness, `topic.repos.main` readiness, topic record labels, and default `operator` Topic Actor status. If common preparation is missing, route to `isomer-admin-topic-prepare` before continuing. Read [references/manual-research-session.md](references/manual-research-session.md).
2. **Resolve requested Topic Actors**. Build the selected actor roster from the user's requested workers and existing Topic Actor bindings. Include the reserved `operator` actor unless the user opted out and the session does not require it. Read [references/actor-roster.md](references/actor-roster.md).
3. **Delegate actor topology work**. For every missing, stale, or blocked Topic Actor, delegate registration, update, materialization, repair, archive, and diagnostics to `isomer-admin-topic-workspace-mgr` or the backed `project topic-actors ...` CLI surface. Read [references/actor-roster.md](references/actor-roster.md).
4. **Run research workspace bootstrap**. Invoke `isomer-rsch-workspace-mgr-v2` for base topic readiness, selected Topic Actor readiness, and optional formal team readiness when present. Read [references/research-bootstrap.md](references/research-bootstrap.md).
5. **Write per-actor start packs**. Create one authoritative Topic Workspace research record per selected actor, then write a small actor-local copy or pointer under that actor's Isomer-managed namespace. Read [references/start-pack-template.md](references/start-pack-template.md).
6. **Report next actions**. Tell the user which Topic Actor Workspace cwd to open for each worker, which v2 skills and placeholder-binding files to install or read, which commands record accepted artifacts, and which blockers remain.

If the user's task does not map cleanly to these steps, use your native planning tool to build a bounded manual-session plan from prepared-topic evidence, requested actors, Topic Actor Workspace readiness, bootstrap output, storage bindings, blockers, and the user's intended first research skill.

## Required Inputs

- Prepared-topic evidence or permission to run common topic preparation first.
- Requested Topic Actor names, runtime kinds, and roles when the user wants additional workers beyond `operator`.
- Selected v2 research skill set or the first intended research route.
- Operator intent for mutation before registering actors, materializing workspaces, running bootstrap, or writing start packs.

## Output Contract

Default to **Essential Output** in chat. Print **Complete Output** only when the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output.

### Essential Output

Report `status`, selected topic refs, Topic Actor roster, each actor cwd, runtime kind, role kind, bootstrap record refs, start-pack record refs, actor-local pointer paths, blockers, and next action.

### Complete Output

Include prepared-topic evidence, actor binding JSON, actor-scoped semantic paths, topic-main integration status, optional formal team refs, placeholder binding index or readiness report refs, per-skill `placeholder-bindings.md` entrypoints, `isomer-cli ext research records` command shapes, start-pack record metadata, actor-local copy paths, and repair routes.

## Guardrails

Do not require Topic Agent Team Profile material, Agent Team Instance records, formal Agent Workspaces, Agent Instance ids, Houmao launch dossiers, mailboxes, or gateways for human-orchestrated Topic Actor research.

Do not own Topic Actor CRUD in this skill. Route actor registration, update, materialization, repair, archive, diagnostics, branch validation, and worktree source checks to `isomer-admin-topic-workspace-mgr`.

Do not make every manually controlled worker use `topic.repos.main` as cwd. `topic.repos.main` remains the Git anchor and integration surface; each actor gets its own `topic.actors.workspace` cwd when it needs independent work.

Do not treat files in Topic Actor Workspaces, Agent Workspaces, `topic.repos.main`, or local tmp surfaces as accepted research truth until the workflow records or links them through Topic Workspace research records.

Do not claim formal adoption of Topic Actor-produced work into Agent Instance or Agent Team Instance identity. Preserve original Topic Actor metadata and report formal adoption as out of scope for this change.
