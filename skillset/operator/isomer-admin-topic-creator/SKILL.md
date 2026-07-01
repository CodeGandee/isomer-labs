---
name: isomer-admin-topic-creator
description: Create or resume an Isomer Research Topic from empty or partial Project state to a manual-research-ready Topic Workspace, coordinating Project setup, topic registration, runtime readiness, topic environment setup, Topic Actor workspaces, v2 research bootstrap, and start-pack handoff.
---

# Isomer Admin Topic Creator

Use this command-style operator skill when the user wants one front door for creating, initializing, preparing, starting, or repairing a Research Topic for manual or human-orchestrated research. This skill owns the user-facing ladder from blank or partial Project state to manual-research-ready Topic Workspace, while delegating lower-level mutation to `isomer-admin-project-mgr`, `isomer-srv-topic-env-setup`, `isomer-admin-topic-workspace-mgr`, `isomer-rsch-workspace-mgr-v2`, and compatibility workflow `isomer-admin-manual-research-session`.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Default help mode**:
   - Match when this skill is invoked without a prompt.
   - Select `help`, load [references/help.md](references/help.md), execute its workflow, and report its output.
2. **Select one command** from the **Commands** table that best matches the user's request:
   - Use `create` for the end-to-end happy path.
   - Use `plan` before mutation, `status` to inspect progress, and `repair` to resume from blockers.
   - Use a stage command for bounded work when the user names that stage.
3. **Load only the selected command page**:
   - Guardrail: load only the selected command page.
   - Execute that page's `## Workflow`.
   - Follow that page's delegation and mutation boundary rules.
4. **Preserve the initialization ladder**:
   - Project readiness.
   - Topic definition and registration.
   - Workspace Runtime readiness.
   - Topic environment and `topic.repos.main` readiness.
   - Topic Actor workspace readiness.
   - v2 research bootstrap.
   - Manual research start packs.
5. **Report topic creation output** using **Essential Output** by default and **Complete Output** when requested.

If the user's task does not map cleanly to these steps, use your native planning tool to build a bounded topic-creation plan from Project Manifest-backed context, selected Research Topic refs, Topic Workspace refs, semantic path evidence, delegated owner boundaries, blockers, and the user's intended first research action.

## Commands

Load only the selected reference page before executing a command.

| Command | Use For | Detail |
| --- | --- | --- |
| `help` | Print what this skill does, required inputs, commands, outputs, and guardrails | [references/help.md](references/help.md) |
| `plan` | Dry-run the topic initialization ladder without mutation | [references/plan.md](references/plan.md) |
| `create` | Run the end-to-end path to manual-research-ready Topic Workspace | [references/create.md](references/create.md) |
| `ensure-project` | Ensure Project bootstrap and basic Project health | [references/ensure-project.md](references/ensure-project.md) |
| `define-topic` | Resolve topic statement, topic id, topic overview, and topic intent | [references/define-topic.md](references/define-topic.md) |
| `register-topic` | Create or validate Research Topic and Topic Workspace registration | [references/register-topic.md](references/register-topic.md) |
| `init-runtime` | Initialize or validate Workspace Runtime for the selected topic | [references/init-runtime.md](references/init-runtime.md) |
| `setup-topic-env` | Prepare topic environment readiness and `topic.repos.main` evidence | [references/setup-topic-env.md](references/setup-topic-env.md) |
| `setup-actors` | Create or validate selected Topic Actors and Topic Actor Workspaces | [references/setup-actors.md](references/setup-actors.md) |
| `bootstrap-research` | Run or validate v2 research workspace bootstrap | [references/bootstrap-research.md](references/bootstrap-research.md) |
| `start-manual-research` | Produce per-actor manual research start packs and final cwd handoff | [references/start-manual-research.md](references/start-manual-research.md) |
| `status` | Report current ladder progress and the next command | [references/status.md](references/status.md) |
| `repair` | Resume from the first blocked or stale stage without rerunning ready stages | [references/repair.md](references/repair.md) |

## Required Inputs

- A Project root or permission to initialize one.
- A concrete Research Topic statement, topic id, or registered Research Topic ref.
- Operator intent for mutation before Project initialization, topic creation, runtime initialization, topic environment setup, Topic Actor registration, worktree materialization, research bootstrap, or start-pack writing.
- Requested manual Topic Actors, runtime kinds, role kinds, and controller kinds when the user wants workers beyond the default `operator`.
- An explicit opt-out when the user does not want the default `operator` Topic Actor or Topic Actor Workspace.
- Selected v2 research skill set or first intended research route when start packs should be specific.

## Output Contract

Default to **Essential Output** in chat. Print **Complete Output** only when the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output.

### Essential Output

Report `status`, Project root, Research Topic ref, Topic Workspace ref, `topic.repos.main` readiness, Workspace Runtime status, Topic Actor roster, each selected actor cwd, v2 bootstrap status, start-pack record refs, blockers, and next action.

### Complete Output

Include commands run, semantic labels, path sources, Project lifecycle evidence, topic registration evidence, runtime validation output, topic environment setup evidence, `topic.repos.main` evidence, actor binding JSON, actor-scoped semantic paths, placeholder binding entrypoints, storage recording command shapes, start-pack metadata, actor-local pointer paths, delegated owner evidence, skipped stages, and repair routes.

## Guardrails

Do not make this skill the authority for lower-level mutation. Delegate Project lifecycle work to `isomer-admin-project-mgr` or supported `isomer-cli project ...` commands, topic environment setup to `isomer-srv-topic-env-setup`, Topic Actor topology to `isomer-admin-topic-workspace-mgr` or `project topic-actors ...`, research bootstrap to `isomer-rsch-workspace-mgr-v2`, and start-pack compatibility workflows to `isomer-admin-manual-research-session`.

Do not infer Research Topics or Topic Workspaces by scanning sibling directories. Use Project Manifest-backed CLI/API surfaces and semantic path resolution.

Do not treat `topic.repos.main`, Topic Actor Workspaces, Agent Workspaces, or tmp surfaces as accepted research truth until artifacts are recorded or linked through Topic Workspace research records.

Do not route manual, human-orchestrated, or multiple manually controlled coding-agent research requests to Topic Team Specialization unless the user explicitly asks for a Domain Agent Team Template. Hand off formal team work to `isomer-admin-topic-team-specialize`.

Do not silently recreate the default `operator` Topic Actor after an explicit opt-out. Report a blocker if a later step requires it.
