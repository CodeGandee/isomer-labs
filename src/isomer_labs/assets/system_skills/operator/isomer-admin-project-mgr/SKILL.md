---
name: isomer-admin-project-mgr
description: Initialize, inspect, validate, clean up, move generated content, and manage Project lifecycle from a Project Operator Session. Use this skill for Project bootstrap, health, topic listing, context inspection, runtime lifecycle, cleanup, relocation, and routing; route blank-state topic creation or manual-research setup to isomer-admin-topic-creator.
---

# Isomer Admin Project Mgr

Use this as the operator workflow for Isomer Project lifecycle management. It helps an operator create, check, clean up, and move generated content for the Isomer Project config, Isomer-managed Houmao overlay, Research Topic and Topic Workspace registrations, Effective Topic Context, explicit Workspace Runtime readiness steps, and routing before topic work. Use `isomer-admin-topic-creator` as the front door for blank-state topic creation, Topic Actor-ready setup, and human-orchestrated Topic Actor research preparation.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Default help mode**:
   - Match when this skill is invoked without a prompt.
   - Select `help`, load [references/help.md](references/help.md), execute its workflow, and report its output.
2. **Resolve the Project root** from the user's prompt or current working directory. See [references/project-concepts.md](references/project-concepts.md).
3. **Select one subcommand** from the **Subcommands** table that best matches the user's request.
4. **Load only the selected subcommand page**:
   - Guardrail: load only the selected subcommand page.
   - Include any local support reference it names.
   - Execute that workflow for one bounded manual operation.
5. **Report the Project lifecycle output** using **Essential Output** by default and **Complete Output** when requested, and preserve the **Guardrails**.
6. **Hand off topic-oriented work** to the narrow owner:
   - Use `isomer-admin-topic-creator` for blank-state topic creation, topic initialization, Topic Actor-ready setup, and human-orchestrated Topic Actor research preparation.
   - Use `isomer-admin-topic-mgr` for initialized-topic storage inspection, Topic Actor CRUD, Topic Actor Workspace materialization, actor-scoped path diagnostics, branch helpers, package mutation, environment verification routing, and topology repair.
   - Use `isomer-admin-topic-team-specialize` only when the user explicitly asks to adapt or instantiate a Domain Agent Team Template.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the project context, subcommands, CLI boundaries, output contract, and guardrails in this skill, then execute the plan.

## Subcommands

Load only the subcommand pages needed for the user's task.

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `help` | Print what this skill does, how to invoke it, available subcommands, outputs, and guardrails | [references/help.md](references/help.md) |
| `init-project` | Initialize an Isomer Project and Isomer-managed Houmao overlay | [references/init-project.md](references/init-project.md) |
| `cleanup-project` | Plan or apply cleanup of selected Isomer-managed Project material | [references/cleanup-project.md](references/cleanup-project.md) |
| `move-content` | Plan or apply relocation of the Project generated content root | [references/move-content.md](references/move-content.md) |
| `check-project` | Validate and diagnose an existing Project without mutating runtime or live Houmao state | [references/check-project.md](references/check-project.md) |
| `list-topics` | List and inspect registered Research Topics and Topic Workspaces through Isomer CLI surfaces | [references/list-topics.md](references/list-topics.md) |
| `show-context` | Show Effective Topic Context and selected refs for topic-scoped work | [references/show-context.md](references/show-context.md) |
| `init-runtime` | Initialize or reopen Workspace Runtime for a selected Research Topic | [references/init-runtime.md](references/init-runtime.md) |
| `prep-runtime` | Prepare and validate launch-facing Topic Environment Readiness | [references/prep-runtime.md](references/prep-runtime.md) |
| `prepare-topic` | Route topic initialization or compatibility common preparation toward the correct owner | [references/prepare-topic.md](references/prepare-topic.md) |
| `manual-research` | Route human-orchestrated Topic Actor research setup to the topic creator without implying Topic Team Specialization | [references/manual-research.md](references/manual-research.md) |
| `specialize-team` | Resolve Project readiness and hand off full topic-team specialization | [references/specialize-team.md](references/specialize-team.md) |

## Output Contract

Default to **Essential Output** in chat. Print **Complete Output** only when the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output. When important handoff detail is omitted, say that Complete Output is available on request.

### Essential Output

Report:

- `status`: Project lifecycle, cleanup, relocation, runtime, or validation result.
- `project`: resolved `project_root` and Project Manifest status.
- `topic`: selected Research Topic or Topic Workspace when relevant.
- `what_changed`: important created, moved, removed, or validated paths.
- `blockers`: user-actionable blockers, warnings, or diagnostics.
- `next_action`: usually initialize, repair, validate, prepare runtime, run topic-team specialization, or stop on blockers.

### Complete Output

When requested, include grouped handoff and audit fields:

- **Project identity**: `project_root`, `project_manifest_path`, `houmao_project_dir`, and `houmao_overlay_dir`.
- **Topic context**: `research_topic_refs`, `topic_workspace_refs`, and `effective_topic_context`.
- **Runtime**: `runtime_status` and related diagnostics.
- **Cleanup**: `cleanup_plan`, selected parts, dry-run or confirmed mode, planned targets, skipped targets, and removed targets.
- **Relocation**: `relocation_plan`, old and new generated content roots, managed moves, manifest updates, unmanaged leftovers, warnings, and applied moves.
- **Commands and diagnostics**: `commands_run`, read-only or mutation posture, diagnostics, blockers, and `next_operator_action`.

## Guardrails

Use `isomer-cli project init` for fresh Project bootstrap. A successful init creates `.isomer-labs/`, the selected generated content root (`isomer-content/` by default or `--content-dir <content-dir>` when supplied), generated content-root policy files, and the Isomer-managed Houmao overlay at `.isomer-labs/.houmao/`, but it must not create a Research Topic, Topic Workspace, Workspace Runtime state, Agent Workspaces, adapter launch material, mailboxes, gateways, managed agents, sessions, or launch dossiers. Root `.houmao/` is external user-owned Houmao state if present, not Isomer-managed Project bootstrap state.

Use `isomer-cli project topics create <topic-id> --statement "<research topic>"` as the authoritative Research Topic creation path. It normally creates `isomer-content/topic-ws/<topic-id>/`; when init selected `--content-dir <content-dir>`, it normally creates `<content-dir>/topic-ws/<topic-id>/`. Use `project topics show`, `project topics update`, and plan-first `project topics delete <topic-id> --dry-run` before `project topics delete <topic-id> --yes` for topic lifecycle changes.

Use `isomer-cli project cleanup --part <part> --dry-run` before destructive cleanup, and use `isomer-cli project cleanup --part <part> --yes` only after the user has reviewed the plan. Preserve unknown files by default; whole content-root removal requires `--purge-content-root`.

Use `isomer-cli project content-root move --to <content-dir> --dry-run` before moving generated content, and use `isomer-cli project content-root move --to <content-dir> --yes` only after the user has reviewed the plan. Relocation updates Project Manifest paths and moves Isomer-managed content containers only. It preserves unmanaged leftovers and does not rewrite Workspace Runtime records, Pixi environments, installed packages, adapter runtime material, logs, stored path plans, or generated runtime internals. Warn the user that moved runtimes may need reinstall or reinitialization.

Use read-only commands for checks unless the user explicitly requests initialization or preparation. `isomer-cli project validate`, `isomer-cli project doctor`, `isomer-cli project topics list`, `isomer-cli project workspaces list`, `isomer-cli project context show`, `isomer-cli project paths preview`, and Houmao project status checks must not mutate Project config, Workspace Runtime, or live Houmao agents.

Keep Workspace Runtime creation explicit through `isomer-cli project runtime init`, and keep launch-facing readiness explicit through `isomer-cli project runtime prepare` and `isomer-cli project runtime validate --require-ready-readiness`. When explaining runtime initialization, distinguish worker-facing `repos/topic-main` and `agents/<agent-name>` from owner-preserved `records/*`, runtime-internal `runtime/*`, and `state.sqlite`.

Hand off blank-state topic creation, Topic Actor-ready setup, and human-orchestrated Topic Actor research preparation to `isomer-admin-topic-creator`. Hand off per-agent worktree setup and cwd proof to `isomer-srv-agent-env-setup` after topic env predecessor evidence exists. Use `isomer-admin-topic-mgr` for initialized-topic storage inspection, optional topology inspection, branch helper operations, boundary summaries, package mutation, environment verification routing, diagnostics, and Topic Actor CRUD or Topic Actor Workspace materialization.

Do not scan unregistered directories as authority for Research Topics or Topic Workspaces. Use Project Manifest-backed CLI surfaces.

Do not route manual, human-orchestrated, or multiple manually controlled coding-agent research requests to Topic Team Specialization unless the user explicitly asks for a Domain Agent Team Template. Use `isomer-admin-topic-creator`, with Topic Manager actor management underneath, for those requests.

Do not duplicate Topic Team Specialization. When the user asks to adapt or instantiate a Domain Agent Team Template for a Research Topic, use `specialize-team` to hand off to `isomer-admin-topic-team-specialize fast-forward`.

## Local References

- [references/project-concepts.md](references/project-concepts.md): Project, Research Topic, Topic Workspace, and Isomer-managed Houmao overlay concepts.
- [references/cli-command-boundaries.md](references/cli-command-boundaries.md): supported Isomer CLI command shapes and mutation boundaries.
- [references/cleanup-project.md](references/cleanup-project.md): cleanup planning, confirmation, parts, and safety boundaries.
- [references/move-content.md](references/move-content.md): generated content-root relocation planning, confirmation, manifest updates, and runtime warnings.
- [references/houmao-bootstrap.md](references/houmao-bootstrap.md): Project-level Houmao bootstrap and status checks.
- [references/runtime-boundaries.md](references/runtime-boundaries.md): Workspace Runtime, readiness, and launch boundary rules.
