---
name: isomer-op-topic-creator
description: Use when an operator needs to create or resume an Isomer Research Topic from empty or partial Project state to a prepared Topic Workspace, coordinating Project setup, topic registration, runtime readiness, topic environment setup, Topic Actor workspaces, actor onboarding, and final readiness summary.
---

# Isomer Admin Topic Creator

## Overview

Use this command-style operator skill when the user wants one front door for creating, initializing, preparing, or repairing a Research Topic for manual or human-orchestrated research. This skill owns the user-facing ladder from blank or partial Project state to prepared Topic Workspace, while delegating lower-level mutation to `isomer-op-project-mgr`, `isomer-srv-topic-env-setup`, and `isomer-op-topic-mgr`. Its `create-research-intent` boundary writes `topic.intent.overview` from a canonical template, and `clarify-research-intent` offers an interactive human-in-the-loop refinement path. Its `finalize` boundary writes `topic.workspace.summary` and creates or refreshes the first structured reset checkpoint from operator-level readiness evidence.

## When to Use

Concrete Research Topic substance is a hard gate. The topic can come from the prompt, a Markdown brief, selected context, or a registered concrete topic statement, but missing or generic topic material such as `default` must block before deriving a topic id, choosing or creating a Topic Workspace, registering a topic, or writing `topic.intent.overview`, `topic.intent.topic_env_requirements`, `topic.intent.actor_definitions`, or derived env gates.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Default help mode**:
   - Match when this skill is invoked without a prompt.
   - Select `help`, load [references/help.md](references/help.md), execute its workflow, and report its output.
2. **Select one subcommand** from the **Subcommands** tables that best matches the user's request:
   - If the user asks to create, initialize, prepare, or start a topic without explicitly asking for `fast-forward`, fully automatic execution, `step-by-step`, manual lower-level control, `run-to`, a stop-before/exclusion phrase, or another named mode, default to `run-to define-topic-env` with the `define-topic-env` target included by default.
   - Use `step-by-step` for the guided happy path with per-step acknowledgement.
   - Use `fast-forward` only when the user explicitly asks for fully automatic, fast-forward, no-stop, or equivalent end-to-end execution.
   - Use `run-to` to run automatically through a selected procedural step by default; stop before the selected target only when the user explicitly says `before`, `stop before`, `excluding`, or `up to but not including`.
   - Use `status` to inspect progress and `repair` to resume from blockers.
   - Use a procedural subcommand for bounded user-facing setup or finalization work.
   - Use a helper subcommand only when the user explicitly names a lower-level stage or `fast-forward`/`repair` needs it.
3. **Load only the selected subcommand page**:
   - Guardrail: load only the selected subcommand page.
   - Execute that page's `## Workflow`.
   - Follow that page's delegation and mutation boundary rules.
4. **Preserve the initialization ladder**:
   - Project readiness.
   - Topic input resolution and registration.
   - Research intent overview through `create-research-intent`.
   - Workspace Runtime readiness.
   - Topic env source gate through `define-topic-env`.
   - Topic environment and `topic.repos.main` readiness through `setup-topic-env`.
   - Actor definitions through `define-actors`.
   - Topic Actor workspace, derived actor env gate readiness, and actor onboarding context through `setup-actors`.
   - Topic Workspace readiness summary and first structured reset checkpoint through `finalize`.
5. **Report topic creation output** using **Essential Output** by default and **Complete Output** when requested.

If the user's task does not map cleanly to these steps, use your native planning tool to build a bounded topic-creation plan from Project Manifest-backed context, selected Research Topic refs, Topic Workspace refs, semantic path evidence, delegated owner boundaries, blockers, and the user's intended first research action.

## Subcommands

Load only the selected reference page before executing a subcommand.

### Procedural Subcommands

Procedural subcommands are user-facing setup and finalization operations in topic initialization order.

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `create-research-intent` | Create or update `topic.intent.overview` from the canonical template in `templates/topic-overview.md` | [references/create-research-intent.md](references/create-research-intent.md) |
| `define-topic-env` | Create or refine the topic env source gate and pause for user verification unless running under `fast-forward` | [references/define-topic-env.md](references/define-topic-env.md) |
| `setup-topic-env` | Prepare topic environment readiness and `topic.repos.main` evidence | [references/setup-topic-env.md](references/setup-topic-env.md) |
| `define-actors` | Create or refine Topic Actor definitions, defaulting to the `operator` actor when no actor details are supplied | [references/define-actors.md](references/define-actors.md) |
| `setup-actors` | Create or validate selected Topic Actors, Topic Actor Workspaces, derived actor env gates, and actor onboarding context | [references/setup-actors.md](references/setup-actors.md) |
| `finalize` | Validate Topic Workspace preparation, write `topic.workspace.summary`, create or refresh the first structured reset checkpoint, and print ready/verified/blocked state | [references/finalize.md](references/finalize.md) |

### Helper Subcommands

Helper subcommands are lower-level ladder stages normally called by `fast-forward`, `repair`, or a procedural subcommand. Load them directly only when the user explicitly names that stage.

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `ensure-project` | Ensure Project bootstrap and basic Project health | [references/ensure-project.md](references/ensure-project.md) |
| `resolve-topic-input` | Resolve concrete topic source material, derive or confirm topic id, and identify the Topic Workspace candidate without writing intent files | [references/resolve-topic-input.md](references/resolve-topic-input.md) |
| `register-topic` | Create or validate Research Topic and Topic Workspace registration | [references/register-topic.md](references/register-topic.md) |
| `init-runtime` | Initialize or validate Workspace Runtime for the selected topic | [references/init-runtime.md](references/init-runtime.md) |

### Misc Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `help` | Print what this skill does, required inputs, subcommands, outputs, and guardrails | [references/help.md](references/help.md) |
| `fast-forward` | Run the end-to-end path to Topic Workspace readiness summary | [references/fast-forward.md](references/fast-forward.md) |
| `step-by-step` | Run the same main workflow as `fast-forward`, but preview each step and wait for acknowledgement before proceeding | [references/step-by-step.md](references/step-by-step.md) |
| `run-to` | Run the main workflow through a selected procedural subcommand by default, or stop before it when exclusion is explicit | [references/run-to.md](references/run-to.md) |
| `status` | Report current ladder progress, readiness evidence, summary freshness, blockers, and skipped stages | [references/status.md](references/status.md) |
| `repair` | Resume from the first blocked or stale stage without rerunning ready stages | [references/repair.md](references/repair.md) |
| `clarify-research-intent` | Interactively refine an existing `topic.intent.overview` by walking the template sections with the user | [references/clarify-research-intent.md](references/clarify-research-intent.md) |

## Required Inputs

- A Project root or permission to initialize one.
- A concrete Research Topic statement, topic id, or registered Research Topic ref.
- Operator intent for mutation before Project initialization, topic registration, topic env setup, runtime initialization, Topic Actor registration, worktree materialization, actor onboarding updates, or summary writing.
- Requested manual Topic Actors, runtime kinds, role kinds, and controller kinds when the user wants workers beyond the default `operator`.
- An explicit opt-out when the user does not want the default `operator` Topic Actor or Topic Actor Workspace.

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

### Essential Output

Lead with the topic-creation outcome. Name the Project, Research Topic, and Topic Workspace, then summarize Topic Main Development Repository readiness, Workspace Runtime status, Topic Actors and their workspaces, onboarding, summary freshness, any reset checkpoint, ready surfaces, verified checks, skipped stages, and blockers.

### Complete Output

Include commands run, semantic labels, path sources, Project lifecycle evidence, topic registration evidence, `topic.intent.overview`, `topic.intent.topic_env_requirements`, `topic.intent.actor_definitions`, `topic.env.actor_env_gates`, runtime validation output, topic environment setup evidence, `topic.repos.main` evidence, actor binding JSON, actor-scoped semantic paths, actor onboarding evidence, delegated owner evidence, summary evidence, reset checkpoint payload or review path when requested, skipped stages, and blockers.

## Operational Notes

- Delegate Project lifecycle work to `isomer-op-project-mgr` or supported `isomer-cli project ...` commands, topic environment setup to `isomer-srv-topic-env-setup`, and Topic Actor topology to `isomer-op-topic-mgr` or `project topic-actors ...`.
- Use Project Manifest-backed CLI/API surfaces and semantic path resolution.
- A Domain Agent Team Template, Topic Agent Team Profile or Bundle, Topic Team Instantiation Packet, Agent Team Instance, selected formal-team material, or equivalent evidence can establish that target when the requested action applies to the team.
- Generic topic preparation, launch-facing work, readiness gaps, missing summaries, and missing Agent Workspaces cannot.
- Hand off valid formal team work to `isomer-op-topic-team-specialize`.
- Report a blocker if a later step requires it.
- Report what is ready, verified, skipped, blocked, and where `topic.workspace.summary` was written.

## Guardrails

- DO NOT make this skill the authority for lower-level mutation.
- DO NOT infer Research Topics or Topic Workspaces by scanning sibling directories.
- DO NOT treat `topic.repos.main`, Topic Actor Workspaces, Agent Workspaces, or tmp surfaces as accepted research truth.
- DO NOT route manual, human-orchestrated, or multiple manually controlled coding-agent research requests to Topic Team Specialization unless the user explicitly invokes specialization or the prompt or authoritative context establishes a formal Agent Team target.
- DO NOT silently recreate the default `operator` Topic Actor after an explicit opt-out.
- DO NOT prescribe a next research command, research-stage route, Houmao launch, or formal team specialization route in terminal Topic Creator output.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
