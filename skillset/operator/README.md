# Operator Admin Skills

This subtree contains skills intended for Project Operator Sessions and Operator Agents. Operator skills use the `isomer-admin-<purpose>` naming convention because they operate project control surfaces: project discovery, topic creation, human-orchestrated Topic Actor setup, Topic Team Specialization orchestration, approval provenance, profile materialization, and team launch orchestration.

Install these skills into the agent surface that acts as the Project Operator Session or durable Operator Agent. Ordinary research team members should use research-stage skills from `skillset/research-paradigm/`; Service Team actors should use service skills from `skillset/service/`.

## Skill Purposes

| Skill | Purpose |
| --- | --- |
| `isomer-admin-welcome` | Manual invocation only. Show the action-oriented Isomer Labs operator menu and route users to the active owner skill. It exposes visible usage paths such as `start-research-manually` for human-orchestrated Topic Actor research through `isomer-admin-topic-creator` and `start-research-by-agent-team` for Domain Agent Team Template specialization through `isomer-admin-topic-team-specialize`; it also maps Project lifecycle work to `isomer-admin-project-mgr`, initialized-topic management to `isomer-admin-topic-mgr`, and Houmao interop questions to `isomer-admin-houmao-interop`. |
| `isomer-admin-project-mgr` | Run the operator Project lifecycle workflow. It exposes short local subcommands such as `help`, `init-project`, `check-project`, `list-topics`, `show-context`, `init-runtime`, `prep-runtime`, `prepare-topic`, `manual-research`, and `specialize-team`; it initializes `.isomer-labs/` and the Isomer-managed `.isomer-labs/.houmao/` overlay through `isomer-cli project init`, checks Project health, resolves context, prepares runtime, routes blank-state topic creation and manual-research setup to `isomer-admin-topic-creator`, and hands full topic-team specialization to `isomer-admin-topic-team-specialize fast-forward`. |
| `isomer-admin-topic-creator` | Create or resume a Research Topic from empty or partial Project state to a prepared Topic Workspace with a readiness summary. It exposes commands such as `help`, `fast-forward`, `step-by-step`, `run-to`, `ensure-project`, `resolve-topic-input`, `register-topic`, `init-runtime`, `create-research-intent`, `define-topic-env`, `setup-topic-env`, `define-actors`, `setup-actors`, `finalize`, `status`, and `repair`; it delegates Project lifecycle to `isomer-admin-project-mgr`, topic environment setup to `isomer-srv-topic-env-setup`, and Topic Actor topology to `isomer-admin-topic-mgr`. |
| `isomer-admin-topic-team-specialize` | Run the module-level Topic Team Specialization workflow. It exposes procedural subcommands from `init-topic` through `finalize-topic-team`, five helper subcommands for lower-level specialization work, and misc commands such as `help`, `step-by-step`, and `fast-forward`; it creates `topic.intent.overview`, resolves topic and agent environment intent, creates or validates derived topic and agent target specs, copies and adapts Domain Agent Team Template material under `<topic-workspace>/team-profile/`, orchestrates Topic Workspace predecessor setup through service skills, delegates per-agent worktree and cwd proof to agent env setup when requested, validates readiness, writes `isomer-topic-summary.md`, and keeps approval, materialization, and launch as explicit boundaries. |
| `isomer-admin-topic-mgr` | Manage an initialized Research Topic after Topic Creator handoff. It exposes scoped commands for `status`, storage, Topic Actors, topic agent team topology, package install/update/remove mutation, environment verification routing, boundary notes, and diagnostics. Canonical Topic Main Development Repository setup belongs to `isomer-srv-topic-env-setup`; canonical per-agent worktree creation and cwd proof belong to `isomer-srv-agent-env-setup`; production DeepSci research bootstrap belongs to `isomer-rsch-workspace-mgr`. |
| `isomer-admin-houmao-interop` | Bridge Isomer Labs project constructs and the Houmao agent runtime. It explains how the Houmao agent loop works, lists agent-loop customization points, maps Domain Agent Team Templates such as DeepScientist onto Houmao concepts, and guides runtime inspection. Use it when a topic-team specialization or launch task touches Houmao loop, roles, recipes, presets, specialists, launch dossiers, project overlays, credentials, mailbox, or gateway. |

## Example: Initialize and Check a Project

Use this flow when a user asks the operator to create, diagnose, or prepare an Isomer Project before topic-team work.

1. The operator can ask `isomer-admin-project-mgr init-project` to run the supported Project bootstrap path. Successful `isomer-cli project init` creates `.isomer-labs/`, the selected generated content root, and the Isomer-managed `.isomer-labs/.houmao/` overlay. Root `.houmao/` is external user-owned Houmao state if present. Research Topics and Topic Workspaces are created later through `isomer-cli project topics create`.
2. If the user wants usage information, call `isomer-admin-project-mgr help`; invoking `isomer-admin-project-mgr` without a prompt defaults to the same help output.
3. If the Project already exists, call `check-project` to run read-only Project validation, doctor diagnostics, and Houmao Project status checks.
4. Use `list-topics` and `show-context` to inspect registered Research Topics, Topic Workspaces, defaults, selected profile refs, and selected template refs.
5. Use `init-runtime` and `prep-runtime` only when the user explicitly wants Workspace Runtime state and launch-facing readiness.
6. When the user asks to create, prepare, or start a Research Topic for manual or future research work, call `isomer-admin-topic-creator fast-forward` for automatic setup, `step-by-step` for guided setup, or `run-to <procedural-subcommand>` for targeted preparation; it handles the ladder from Project readiness through `topic.workspace.summary` and delegates lower-level operations.
7. When the user asks for a narrow Project-only route, `prepare-topic` and `manual-research` hand off to `isomer-admin-topic-creator`.
8. When the user asks to specialize a Domain Agent Team Template over a Research Topic, call `specialize-team`; it resolves Project context and hands off to `isomer-admin-topic-team-specialize fast-forward` rather than to the internal `adapt-team-template` stage.

## Example: Prepare Human-Orchestrated Topic Actor Research

Use this flow when a user wants to do research manually or with multiple manually controlled agents without first launching a formal Topic Agent Team.

1. Call `isomer-admin-topic-creator fast-forward` when the user has approved automatic mutation, `step-by-step` when the user wants guided acknowledgement before each step, or `run-to <procedural-subcommand>` when the user wants to prepare up to a specific stage.
2. The creator ensures or delegates Project initialization, topic definition, Research Topic and Topic Workspace registration, Workspace Runtime readiness, topic environment setup, and `topic.repos.main` readiness.
3. The creator creates or reuses the default reserved `operator` Topic Actor Workspace unless the user explicitly opts out, and it sets up additional requested actors such as `claude-scout`, `codex-exp-a`, or `houmao-writer-a`.
4. The creator delegates actor registration, materialization, repair, and diagnostics to `isomer-admin-topic-mgr` through `project topic-actors ...`.
5. The creator gives each manually controlled worker its own `topic.actors.workspace` cwd, validates actor onboarding evidence, and writes `topic.workspace.summary` with ready, verified, skipped, and blocked state. `topic.repos.main` remains the Git anchor and integration surface, not the required shared cwd for every worker.

## Example: Specialize a Domain Team for a New Topic

Use this flow when a user gives a research topic and asks the operator to instantiate a topic-level team from a Domain Agent Team Template such as `deepsci-mini`.

1. The operator can ask `isomer-admin-topic-team-specialize init-topic` to turn a new research topic idea into `topic.intent.overview` at the resolved Topic Workspace intent path. If the topic already exists in the Project Manifest, the skill can use the registered Research Topic and Topic Workspace instead.
2. If the user wants usage information, call `isomer-admin-topic-team-specialize help`; invoking `isomer-admin-topic-team-specialize` without a prompt defaults to the same help output.
3. The normal procedural flow is `resolve-project`, `resolve-topic-intent`, `ensure-topic-registration`, `resolve-topic-env-gate`, create or validate `topic.env.topic_setup_target_spec`, `setup-topic-env`, `adapt-team-template`, optional `clarify-topic-team`, `resolve-agent-env-gate`, create or validate `topic.env.agent_setup_target_spec`, `setup-agent-workspace`, `validate-topic-team`, and `finalize-topic-team`. Direct requests like `specialize <team-path> over topic <topic>` route to `fast-forward`, which runs this path automatically where possible. `finalize-topic-team` writes `isomer-topic-summary.md` with the topic team, goal, working logic, environment setup, Agent Workspace layout, validation status, blockers, and next actions.
4. If the user wants guided specialization, call `step-by-step`; it follows the same required path as `fast-forward` but explains each step and waits for user confirmation before continuing.
5. If the user wants manual lower-level work, call one helper subcommand at a time, such as `resolve-project`, `inspect-template`, `resolve-context`, `map-placeholders`, or `draft-profile`.
6. If the user explicitly approves continuing past finalization, the same skill's local `approve-profile`, `materialize-profile`, and `launch-team` subcommands handle approval provenance, validated bundle writing, and launch-facing runtime or adapter work.
7. The operator reports topic overview path, copied material paths, packet/profile inputs, environment status, Agent Workspace paths, validation refs, summary path, and blockers.

For Topic Workspace environment setup, `setup-topic-env` creates or validates `topic.env.topic_setup_target_spec`, delegates to `isomer-srv-topic-env-setup`, and records Topic Workspace, Topic Main Development Repository, and projection predecessor evidence, not per-agent cwd proof. For Topic Actor Workspace setup, delegate Topic Actor registration, materialization, repair, archive, and actor-scoped diagnostics to `isomer-admin-topic-mgr`. For Agent Workspace setup, `setup-agent-workspace` creates or validates `topic.env.agent_setup_target_spec` and delegates per-agent worktree creation plus cwd proof to `isomer-srv-agent-env-setup` only after topic env predecessor evidence, Topic Main Development Repository predecessor evidence, required projection predecessor evidence, and authoritative Agent Names exist.

```mermaid
sequenceDiagram
    participant User
    participant Operator as Project Operator Session
    participant Store as Isomer Project and Topic Workspace

    User->>Operator: Request topic team for research topic
    Operator->>Store: init-topic and ensure-topic-registration
    Store-->>Operator: Project, topic, workspace, template refs
    Operator->>Store: create topic env target spec and setup-topic-env for topic-main and projections
    Operator->>Store: adapt-team-template, create agent env target spec, and setup-agent-workspace
    Store-->>Operator: Copied guide, plan, topic edits, setup records, worktree evidence, packet/profile inputs
    Operator->>Store: validate-topic-team and finalize-topic-team
    Store-->>Operator: isomer-topic-summary.md
    Operator->>User: approve-profile
    User-->>Operator: Approval decision
    Operator->>Store: materialize-profile
    Store-->>Operator: Approved Topic Agent Team Profile Bundle
```

## Example: Launch an Approved Topic Team

Use this flow when a Topic Agent Team Profile Bundle already exists and the user asks the operator to create or launch the topic's runtime team.

1. `resolve-project` and `resolve-context` resolve the selected Research Topic, Topic Workspace, approved profile bundle, Workspace Runtime, and launch-relevant adapter refs.
2. The local `approve-profile` subcommand refreshes approval when the existing bundle has stale approval, unresolved launch blockers, or requires a fresh user decision before launch.
3. The local `launch-team` subcommand creates or selects the Agent Team Instance, preserves profile bundle and packet provenance, and routes adapter launch materialization.
4. The operator reports runtime refs, adapter refs, launch diagnostics, launch blockers, and the next operator action to the user.

```mermaid
sequenceDiagram
    participant User
    participant Operator as Project Operator Session
    participant Runtime as Workspace Runtime
    participant Adapter as Execution Adapter

    User->>Operator: Launch approved topic team
    Operator->>Runtime: resolve-project
    Runtime-->>Operator: Topic, profile bundle, runtime refs
    Operator->>Runtime: resolve-context
    Runtime-->>Operator: Readiness and launch diagnostics
    alt Approval refresh needed
        Operator->>User: approve-profile
        User-->>Operator: Approval decision
    end
    Operator->>Runtime: launch-team
    Runtime-->>Operator: Agent Team Instance refs
    Operator->>Adapter: Materialize or launch approved team
    Adapter-->>Operator: Adapter command, payload, and launch refs
    Operator-->>User: Launch result and blockers if any
```

## Example: Explain or Customize Houmao for a Topic Team

Use this flow when a topic-team specialization or launch task touches Houmao-managed agents.

1. If the user asks how the Houmao agent loop works, call `explain-loop`; it reports the gateway-driven request queue, the three daemon loops, the TUI-tracking lifecycle kernel, and the concrete source files.
2. If the user asks what to edit to customize the loop, call `customize-loop`; it reports agent-definition directory layout, project overlay concepts, loop packages, gateway/runtime config, and CLI commands.
3. If the user asks how a Domain Agent Team Template such as DeepScientist maps onto Houmao, call `map-template-to-houmao`; it explains the single-PI-agent stage-skill model and maps it to Houmao presets, launch profiles, and agent-facing skills.
4. If the user asks how to inspect a running agent, gateway, mailbox, or runtime state, call `inspect-runtime`; it reports CLI commands, filesystem paths, and passive API endpoints.
5. Preserve the guardrails: keep Houmao as the adapter/implementation layer, do not edit the Houmao source checkout for Isomer behavior, and do not launch from template source without an approved Topic Agent Team Profile Bundle.

## Naming Contract

Operator skill folders must be named `isomer-admin-<purpose>`, and `SKILL.md` frontmatter `name:` must match the folder name. If present, `agents/openai.yaml` must use the same skill name for `interface.display_name` and invoke the same skill in `interface.default_prompt`.

Operator skills must preserve Isomer domain boundaries. They can direct validation, approval, materialization, and launch orchestration, but they must not bypass Isomer validators, Gates, Workspace Runtime recording, or adapter preflight.

`isomer-admin-project-mgr` is the canonical entrypoint for Project lifecycle operations before topic work. It owns Project bootstrap, Project checks, topic and workspace listing, context inspection, runtime initialization, readiness preparation, and routing to topic creation, manual research setup, or formal topic-team adaptation.

`isomer-admin-topic-creator` is the canonical user-facing entrypoint for topic initialization. It owns the happy path from empty or partial Project state to prepared Topic Workspace readiness summary and delegates lower-level mutation to the existing owner skills and CLI surfaces.

`isomer-admin-topic-team-specialize` is the canonical entrypoint for Domain Agent Team Template understanding and topic adaptation. Its local subcommands are the normal implementation path. Do not add standalone operator skills for project awareness, template inspection, topic context resolution, placeholder reconciliation, topic profile drafting, profile review approval, profile materialization, or team launch orchestration unless a future OpenSpec change explicitly reverses the consolidation.

`isomer-admin-topic-mgr` is the entrypoint for initialized-topic management after Topic Creator handoff, including storage inspection, Topic Actor CRUD, Topic Actor Workspace materialization or repair, actor-scoped path diagnostics, topic agent team topology inspection, branch helper operations, package install/update/remove requests, environment verification routing, Workspace Boundary summaries, manual topology operations, and diagnostics. It is not the canonical creator of the Topic Main Development Repository, normal per-agent worktrees, or production DeepSci research bootstrap outputs.

`isomer-admin-houmao-interop` is the canonical entrypoint for Houmao-specific explanation and customization questions that arise during topic-team work. It answers how the Houmao loop works and how Isomer templates map onto Houmao, but it does not replace `isomer-admin-topic-team-specialize` for full specialization workflows.
