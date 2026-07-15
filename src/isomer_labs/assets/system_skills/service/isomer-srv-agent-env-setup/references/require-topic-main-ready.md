# Require Topic Main Ready

Use this subcommand to require prepared Topic Main Development Repository predecessor evidence before Agent Workspace worktrees or cwd verification run.

Do not initialize, repair, or configure the Topic Main Development Repository here; route missing predecessor evidence to `isomer-srv-topic-env-setup`.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Agent env context | Require `topic.repos.main`, `topic.repos.main.isomer_managed`, projection labels, path sources, requester, and confirmation source from `resolve-agent-env-context`. |
| Topic env predecessor evidence | Require ready Topic Workspace environment evidence from `require-topic-env-ready`, including `topic.env.topic_setup_target_spec`, Topic Main Development Repository Git state, Isomer-managed namespace posture, projection metadata when the agent gate depends on projected external repos, changed files, commands run, blockers, and `per_agent_readiness_status: not_checked`. |
| Agent env target spec | Require resolved `topic.env.agent_setup_target_spec` from `derive-agent-env-gate` or an explicit validated target spec so projection requirements can be checked. |
| Optional modifiers | None for this step. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**:
   - Require resolved context, topic env predecessor evidence, and agent env target spec.
   - Refuse to run if semantic path evidence or predecessor evidence is missing.
2. **Check Topic Main Development Repository evidence**:
   - Confirm predecessor evidence names the resolved `topic.repos.main` path, path source, normal non-bare Git state, owner branch posture, Isomer-managed namespace posture, commands run, changed files, blockers, and readiness status.
3. **Check projection predecessor evidence when needed**:
   - If the agent env target spec requires projected external repos to be visible from each Agent Workspace cwd, confirm matching entries exist in `topic.repos.main.projections.manifest` evidence.
   - Confirm each required projection names intended access, projection mode, canonical source label, canonical source path, projected path, status, blockers, and source evidence.
4. **Inspect only for consistency**:
   - Read local Git and filesystem state only enough to detect stale predecessor evidence.
   - Do not create, initialize, configure, repair, reset, pull, or rewrite `topic.repos.main`.
   - Do not create external repo projections.
5. **Report readiness or repair route**:
   - If evidence is ready and consistent, pass `topic_main_ready` and projection evidence to `create-agent-worktrees` and `verify-agent-env-gate`.
   - If evidence is missing, stale, blocked, failed, or inconsistent, report a repair next action to `isomer-srv-topic-env-setup`.

If the user's task does not map cleanly to these steps, use your native planning tool to separate predecessor-evidence checks from local consistency checks, then execute only the read-only portion.

## Blockers

Report a blocker for:

- missing Topic Main Development Repository predecessor evidence;
- stale or inconsistent Git state;
- missing Isomer-managed namespace evidence;
- missing projection manifest evidence required by the agent env target spec;
- projection status that is blocked, failed, or inconsistent;
- unsafe custom semantic bindings;
- ambiguous gate requirements;
- any repair that requires topic-main creation, configuration, or projection materialization.

## Operational Contract

- Route missing or stale topic-main and projection evidence to `isomer-srv-topic-env-setup`.

## Guardrails

- DO NOT create, initialize, configure, repair, delete, reset, clean, rewrite history, reclone, pull, or silently repair `topic.repos.main`.
- DO NOT create external repo projections.
- DO NOT mutate topic dependencies.
- DO NOT create Agent Workspaces here; that belongs to `create-agent-worktrees`.
