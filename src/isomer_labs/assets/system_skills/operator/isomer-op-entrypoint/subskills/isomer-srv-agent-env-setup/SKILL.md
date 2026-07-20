---
name: isomer-srv-agent-env-setup
description: Use when an Isomer Labs agent needs service-safe Agent Workspace environment setup after Topic Workspace and Topic Main Development Repository predecessor evidence exists, including topic.intent.agent_env_requirements, topic.env.agent_setup_target_spec, explicit manual target specs, topic.env.topic_setup_target_spec predecessor evidence, required projection predecessor evidence, authoritative Agent Names from topic-team material, semantic path evidence, per-agent worktree creation, per-agent cwd verification through Pixi, selected-agent partial repair evidence, and runtime-boundary guardrails.
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Isomer Service Agent Environment Setup

## Overview

- **Purpose**: set up and validate Agent Workspace cwd readiness for a registered Research Topic.
- **Inputs**: consume Topic Workspace predecessor evidence from `isomer-srv-topic-env-setup`, including Topic Workspace Pixi readiness, `topic.env.topic_setup_target_spec`, Topic Main Development Repository Git state, projection metadata when required, and the resolved Pixi manifest and environment.
- **Source and target specs**: read `topic.intent.agent_env_requirements` and derive or validate `topic.env.agent_setup_target_spec`; direct service calls may supply source intent or an explicit manual target spec.
- **Workspace scope**: create or validate per-agent `agent.workspace` worktrees for authoritative Agent Names, then verify from each cwd with `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...`.
- **Resource classification**: ask `isomer-misc-bounded-run-tips` to classify resource-relevant per-agent cwd operations as `light`, `heavy`, `unknown-risk`, or `not-applicable`; record classification source, classification result, reason, resource dimensions, and whether bounded guidance is required.
- **Bounded proof**: operations classified as `heavy` or `unknown-risk` need bounded real-path verification; generic best-effort judgment is allowed only when no recipe applies. A generic smoke test is only supporting evidence.
- **Boundaries**: this service does not install Topic Workspace dependencies and does not create per-agent Pixi manifests, per-agent lockfiles, or per-agent `.pixi/` directories.
- **Readiness**: the full `setup-agent-env` flow verifies every authoritative planned Agent Name before reporting overall readiness; direct verification for one Agent Name is selected-agent partial evidence only.
- **Routing**: keep the entrypoint lean, choose one subcommand, then load that subcommand's reference page.

## When to Use

Use this skill after Topic Workspace and Topic Main Development Repository predecessor evidence exists and the caller needs per-Agent Workspace worktree setup or cwd verification through the resolved Topic Workspace Pixi environment.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Handle help intent**:
   - If the invocation has no prompt, or if the user asks for help, usage, or available functionality, answer from **Help**.
   - Stop unless they also ask for a concrete setup task.
2. **Select one subcommand** from the **Subcommands** tables:
   - If the prompt describes concrete Agent Workspace environment setup but does not name another subcommand, use `setup-agent-env`.
3. **Load the selected reference file**:
   - Load only that reference page before executing a direct subcommand.
   - The `setup-agent-env` reference may load the procedural pages it orchestrates.
4. **Resolve that page's required inputs** from its `## Required Inputs` section, then execute its `## Workflow`.
5. **Report results** using **Essential Output** by default and **Complete Output** when requested:
   - Include requester, confirmation source, optional Service Request or Provenance refs, semantic path evidence, commands run, readiness by agent, blockers, and next action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the subcommands, selected reference page, output contract, and guardrails in this skill, then execute the plan.

## Subcommands

Load only the subcommand pages needed for the user's task. Complex skills divide subcommands into three parts: procedural, helper, and misc.

### Procedural Subcommands

Procedural subcommands are the public single-step workflow API. Call them directly for manual setup, inspection, or partial repair.

| Subcommand | Use For | Reference |
| --- | --- | --- |
| `resolve-agent-env-context` | Resolve Project root, Research Topic, Topic Workspace, Topic Workspace Pixi binding, topic semantic labels, and invocation provenance posture. | [references/resolve-agent-env-context.md](references/resolve-agent-env-context.md) |
| `require-topic-env-ready` | Require predecessor Topic Workspace Pixi readiness and `topic.env.topic_setup_target_spec`. | [references/require-topic-env-ready.md](references/require-topic-env-ready.md) |
| `require-topic-main-ready` | Require prepared Topic Main Development Repository and projection predecessor evidence from topic env setup. | [references/require-topic-main-ready.md](references/require-topic-main-ready.md) |
| `read-agent-env-gate` | Resolve and read `topic.intent.agent_env_requirements` and extract Agent Workspace cwd readiness requirements. | [references/read-agent-env-gate.md](references/read-agent-env-gate.md) |
| `plan-agent-workspaces` | Read authoritative Agent Names from Topic Team Instantiation Packet or derived Topic Agent Team Profile material and resolve agent labels. | [references/plan-agent-workspaces.md](references/plan-agent-workspaces.md) |
| `derive-agent-env-gate` | Generate or update `topic.env.agent_setup_target_spec`, or validate an explicit manual target spec. | [references/derive-agent-env-gate.md](references/derive-agent-env-gate.md) |
| `create-agent-worktrees` | Create or validate per-agent Agent Workspace worktrees and required support labels. | [references/create-agent-worktrees.md](references/create-agent-worktrees.md) |
| `verify-agent-env-gate` | Verify the agent env target spec from Agent Workspace cwd values, with optional selected-agent partial reruns. | [references/verify-agent-env-gate.md](references/verify-agent-env-gate.md) |

### Helper Subcommands

This skill currently exposes no private helper subcommands. If future helpers are added, list them here and keep them out of **Help** unless they become public workflow steps.

### Misc Subcommands

Misc subcommands are public support commands and shortcuts.

| Subcommand | Use For | Reference |
| --- | --- | --- |
| `help` | Explain this skill and list public subcommands. | [references/help.md](references/help.md) |
| `setup-agent-env` | Run the full all-agent setup flow. This is the default for concrete setup tasks that do not name another subcommand. | [references/setup-agent-env.md](references/setup-agent-env.md) |

Each executable reference page owns its `## Required Inputs` contract. Use the selected page as the self-contained input guide for direct calls.

## Help

`isomer-srv-agent-env-setup` prepares Git-backed Agent Workspace cwd readiness after Topic Workspace and Topic Main Development Repository predecessor evidence exists. It uses authoritative Agent Names from a Topic Team Instantiation Packet or Topic Agent Team Profile material derived from that packet, never from directory scans or ad hoc maps. It writes or validates `topic.env.agent_setup_target_spec` from `topic.intent.agent_env_requirements` or an explicit manual target spec when invoked directly, records semantic labels and path sources, consumes prepared topic-main and projection evidence from topic env setup, creates or validates per-agent worktrees, and verifies every required command from each resolved `agent.workspace` cwd through `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...`.

Public procedural subcommands:

| Subcommand | Purpose | Produces |
| --- | --- | --- |
| `resolve-agent-env-context` | Resolve Project, Research Topic, Topic Workspace, Pixi binding, topic labels, requester, confirmation source, and optional Service Request or Provenance refs. | Resolved setup refs, semantic paths, invocation posture, and blockers. |
| `require-topic-env-ready` | Check the Topic Workspace Pixi predecessor. | Topic env predecessor status and repair route to `isomer-srv-topic-env-setup`. |
| `require-topic-main-ready` | Check prepared topic-main and projection predecessor evidence. | Topic-main predecessor status, projection predecessor status, and repair route to `isomer-srv-topic-env-setup`. |
| `read-agent-env-gate` | Read the source gate. | Source agent gate summary, required commands, expected results, Topic Main Development Repository evidence requirements, cwd assumptions, and blockers. |
| `plan-agent-workspaces` | Plan workspaces from authoritative topic-team material. | Agent Names, branch plan, semantic paths, path sources, corroborating operator map evidence, and blockers. |
| `derive-agent-env-gate` | Write or validate the fixed-section per-agent target spec. | `topic.env.agent_setup_target_spec`, defaulting to `<topic-workspace-dir>/intent/derived/isomer-agent-env-gate.md`. |
| `create-agent-worktrees` | Prepare per-agent worktrees. | Worktree status by agent, support path status, boundary material posture, and blockers. |
| `verify-agent-env-gate` | Run or report cwd verification. | Readiness by agent, selected-agent partial evidence when requested, overall readiness only after the full matrix passes, commands run, and blockers. |

Misc subcommands:

| Subcommand | Purpose | Produces |
| --- | --- | --- |
| `setup-agent-env` | Run the full all-agent setup flow. | Combined report with Topic Workspace env predecessor, source intent or explicit target spec source, Topic Main Development Repository predecessor evidence, projection evidence, worktree status by agent, readiness by agent, and overall readiness. |
| `help` | Print what this skill does and how to use it. | Usage table and examples. |

Example prompts:

- `isomer-op-entrypoint->agent-env help`
- `isomer-op-entrypoint->agent-env setup-agent-env <topic-id>`
- `isomer-op-entrypoint->agent-env verify-agent-env-gate <topic-id> --agent analyst`
- `isomer-op-entrypoint->agent-env require-topic-env-ready for <topic-id>`

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format. When important handoff detail is omitted, say that Complete Output is available on request.

### Essential Output

Lead with overall or selected-Agent readiness. Name the Research Topic and Topic Workspace, summarize Topic environment and Topic Main Development Repository predecessors, and report worktree readiness by Agent Name. Include cwd verification, important changed files, blockers at Agent or matrix scope, and the next safe action.

### Complete Output

When requested, include grouped handoff and audit fields:

- **Identity and authorization**: `subcommand`, `project_root`, `research_topic_id`, `topic_workspace_dir`, `topic_workspace_pixi_binding`, `requester`, `confirmation_source`, `service_request_refs`, `support_artifact_refs`, and `provenance_refs`.
- **Semantic paths**: full `semantic_paths` and path diagnostics.
- **Topic predecessor evidence**: `topic_environment_status`, `topic_env_target_spec_label`, `topic_env_target_spec_path`, `topic_main_repository`, and `external_repo_projection_predecessors`.
- **Agent source and target specs**: `agent_env_source_label`, `agent_env_source_path`, `agent_env_source_storage_profile`, `agent_env_source_source`, `agent_env_source_source_detail`, `agent_env_source_diagnostics`, `agent_env_target_spec_label`, `agent_env_target_spec_path`, `agent_env_target_spec_storage_profile`, `agent_env_target_spec_source`, `agent_env_target_spec_source_detail`, and `agent_env_target_spec_diagnostics`.
- **Workspace matrix**: `agent_workspace_paths`, `branch_plan`, `worktree_status_by_agent`, `readiness_by_agent`, `overall_readiness_status`, and `selected_agent_partial`.
- **Operations and resources**: `operation_classification`, `resource_check_status`, `resource_check_evidence`, and `resource_conservative_decisions`, with affected Agent Name or matrix scope.
- **Execution result**: `commands_run`, `changed_files`, blockers, and `next_action`.

## Operational Contract

- Resolve semantic labels before filesystem mutation. Default paths may appear only as examples from `isomer-default.v1`; semantic labels and path sources remain the contract.
- Keep the resolved `agent.workspace` path as a worktree of the already-prepared normal non-bare Topic Main Development Repository on `per-agent/<agent-name>/main`.
- Treat `topic.repos.main.tmp` and `agent.tmp` as local ignored disposable surfaces when available. Do not use tmp contents as durable readiness evidence.
- Allow direct Project Operator Session invocation after the selected Project, Research Topic, Topic Workspace, topic env predecessor evidence, authoritative Agent Name plan, and mutation scope are confirmed. Record optional Service Request, support Artifact, and Provenance refs when available.
- Treat selected-agent direct verification as partial evidence; do not claim overall readiness unless the complete planned Agent Name matrix has passed.
- Ask `isomer-misc-bounded-run-tips` to classify each resource-relevant per-agent cwd verification operation before resource-check planning. Treat `heavy` and `unknown-risk` classifications as requiring bounded guidance, lightweight read-only resource probes, and the smallest real command that satisfies the gate. Apply a matching bounded-run tips subcommand when available, or record generic best-effort judgment when no specific recipe applies. Examples include selected-agent partial checks, fewer build jobs, selected build targets, tiny model or tensor shapes, sample data, reduced iterations, reduced batch size, selected tests, and short benchmark cases; bounded-run tips owns the classification decision. If no bounded real-path command can safely exercise the required path, record that the resource check is blocked and give the command to retry later instead of claiming readiness.

## Operational Notes

- Report missing or stale Topic Workspace dependency readiness as a repair next action for `isomer-srv-topic-env-setup`.
- Do not create, initialize, configure, repair, or project external repos into `topic.repos.main`; report missing or stale topic-main or projection evidence as a repair next action for `isomer-srv-topic-env-setup`.
- Use the Topic Team Instantiation Packet or Topic Agent Team Profile material derived from that packet as the Agent Name authority.
- A matching explicit operator-provided map is only corroborating evidence; a disagreement is an `agent-plan-conflict` blocker.

## Guardrails

- DO NOT create per-agent Pixi manifests, per-agent lockfiles, per-agent `.pixi/` directories, or dependency environments by default.
- DO NOT install or mutate Topic Workspace dependencies.
- DO NOT initialize, repair, or configure the Topic Main Development Repository.
- DO NOT create Agent Instances, mutate Workspace Runtime records, launch Houmao agents, run Execution Adapters, create Houmao launch material, or make research decisions.
- DO NOT infer Agent Names from directories, branches, provider ids, or ad hoc maps.
- DO NOT overwrite, delete, clean, reset, reinitialize, reclone, rewrite history, or silently repair existing repositories or Agent Workspace paths.
## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
