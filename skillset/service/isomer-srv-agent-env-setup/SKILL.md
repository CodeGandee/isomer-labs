---
name: isomer-srv-agent-env-setup
description: Use when an Isomer Labs agent needs service-safe Agent Workspace environment setup after Topic Workspace predecessor evidence exists, including topic.intent.agent_env_requirements, topic.env.agent_setup_target_spec, explicit manual target specs, topic.env.topic_setup_target_spec predecessor evidence, Topic Main Repository worktrees, authoritative Agent Names from topic-team material, semantic path evidence, per-agent cwd verification through Pixi, selected-agent partial repair evidence, and runtime-boundary guardrails.
---

# Isomer Service Agent Environment Setup

## Overview

Set up and validate Agent Workspace cwd readiness for a registered Research Topic. This service is the owner of `topic.intent.agent_env_requirements`, `topic.env.agent_setup_target_spec`, selected-agent partial evidence, and overall per-Agent Workspace readiness. It consumes Topic Workspace predecessor evidence from `isomer-srv-topic-env-setup`, including Topic Workspace Pixi readiness, `topic.env.topic_setup_target_spec`, and the resolved Topic Workspace Pixi manifest and environment. It does not install dependencies by default and it does not create per-agent Pixi manifests, per-agent lockfiles, or per-agent `.pixi/` directories.

Agent env setup normally reads source intent from `topic.intent.agent_env_requirements`, derives or updates the per-agent operational target spec at `topic.env.agent_setup_target_spec`, prepares the shared Topic Main Repository resolved by `topic.repos.main`, creates or validates per-agent `agent.workspace` worktrees for authoritative Agent Names, and verifies the target spec from each Agent Workspace cwd with `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...`. Manual invocation may supply an explicit target spec file, prompt, or context instead of source intent.

This skill is a command-style router: keep the entrypoint lean, choose one subcommand, then load that subcommand's reference page. The full `setup-agent-env` flow verifies every authoritative planned Agent Name before reporting overall readiness. Direct verification can target one authoritative Agent Name only as selected-agent partial readiness evidence.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Handle help intent**. If the invocation has no prompt, or if the user asks for help, usage, or available functionality, answer from **Help** and stop unless they also ask for a concrete setup task.
2. **Select one subcommand** from the **Subcommands** tables. If the prompt describes concrete Agent Workspace environment setup but does not name another subcommand, use `setup-agent-env`.
3. **Load the selected reference file**. Load only that reference page before executing a direct subcommand. The `setup-agent-env` reference may load the procedural pages it orchestrates.
4. **Resolve that page's required inputs** from its `## Required Inputs` section, then execute its `## Workflow`.
5. **Report results** using **Output Contract**, including requester, confirmation source, optional Service Request or Provenance refs, semantic path evidence, commands run, readiness by agent, blockers, and next action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the subcommands, selected reference page, output contract, and guardrails in this skill, then execute the plan.

## Subcommands

Load only the subcommand pages needed for the user's task. Complex skills divide subcommands into three parts: procedural, helper, and misc.

### Procedural Subcommands

Procedural subcommands are the public single-step workflow API. Call them directly for manual setup, inspection, or partial repair.

| Subcommand | Use For | Reference |
| --- | --- | --- |
| `resolve-agent-env-context` | Resolve Project root, Research Topic, Topic Workspace, Topic Workspace Pixi binding, topic semantic labels, and invocation provenance posture. | [references/resolve-agent-env-context.md](references/resolve-agent-env-context.md) |
| `require-topic-env-ready` | Require predecessor Topic Workspace Pixi readiness and `topic.env.topic_setup_target_spec`. | [references/require-topic-env-ready.md](references/require-topic-env-ready.md) |
| `read-agent-env-gate` | Resolve and read `topic.intent.agent_env_requirements` and extract Agent Workspace cwd readiness requirements. | [references/read-agent-env-gate.md](references/read-agent-env-gate.md) |
| `plan-agent-workspaces` | Read authoritative Agent Names from Topic Team Instantiation Packet or derived Topic Agent Team Profile material and resolve agent labels. | [references/plan-agent-workspaces.md](references/plan-agent-workspaces.md) |
| `derive-agent-env-gate` | Generate or update `topic.env.agent_setup_target_spec`, or validate an explicit manual target spec. | [references/derive-agent-env-gate.md](references/derive-agent-env-gate.md) |
| `ensure-topic-main-repository` | Create, reuse, or validate the Topic Main Repository resolved by `topic.repos.main`. | [references/ensure-topic-main-repository.md](references/ensure-topic-main-repository.md) |
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

`isomer-srv-agent-env-setup` prepares Git-backed Agent Workspace cwd readiness after Topic Workspace predecessor evidence exists. It uses authoritative Agent Names from a Topic Team Instantiation Packet or Topic Agent Team Profile material derived from that packet, never from directory scans or ad hoc maps. It writes or validates `topic.env.agent_setup_target_spec` from `topic.intent.agent_env_requirements` or an explicit manual target spec, records semantic labels and path sources, prepares the Topic Main Repository and per-agent worktrees, and verifies every required command from each resolved `agent.workspace` cwd through `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...`.

Public procedural subcommands:

| Subcommand | Purpose | Produces |
| --- | --- | --- |
| `resolve-agent-env-context` | Resolve Project, Research Topic, Topic Workspace, Pixi binding, topic labels, requester, confirmation source, and optional Service Request or Provenance refs. | Resolved setup refs, semantic paths, invocation posture, and blockers. |
| `require-topic-env-ready` | Check the Topic Workspace Pixi predecessor. | Topic env predecessor status and repair route to `isomer-srv-topic-env-setup`. |
| `read-agent-env-gate` | Read the source gate. | Source agent gate summary, required commands, expected results, Topic Main Repository configuration requirements, cwd assumptions, and blockers. |
| `plan-agent-workspaces` | Plan workspaces from authoritative topic-team material. | Agent Names, branch plan, semantic paths, path sources, corroborating operator map evidence, and blockers. |
| `derive-agent-env-gate` | Write or validate the fixed-section per-agent target spec. | `topic.env.agent_setup_target_spec`, defaulting to `<topic-workspace-dir>/intent/derived/isomer-agent-env-gate.md`. |
| `ensure-topic-main-repository` | Prepare the shared Git anchor. | Topic Main Repository state, owner branch, changed files, commands run, and blockers. |
| `create-agent-worktrees` | Prepare per-agent worktrees. | Worktree status by agent, support path status, boundary material posture, and blockers. |
| `verify-agent-env-gate` | Run or report cwd verification. | Readiness by agent, selected-agent partial evidence when requested, overall readiness only after the full matrix passes, commands run, and blockers. |

Misc subcommands:

| Subcommand | Purpose | Produces |
| --- | --- | --- |
| `setup-agent-env` | Run the full all-agent setup flow. | Combined report with Topic Workspace env predecessor, source intent or explicit target spec source, Topic Main Repository, worktree status by agent, readiness by agent, and overall readiness. |
| `help` | Print what this skill does and how to use it. | Usage table and examples. |

Example prompts:

- `$isomer-srv-agent-env-setup help`
- `$isomer-srv-agent-env-setup setup-agent-env <topic-id>`
- `$isomer-srv-agent-env-setup verify-agent-env-gate <topic-id> --agent analyst`
- `$isomer-srv-agent-env-setup require-topic-env-ready for <topic-id>`

## Output Contract

Report:

- `subcommand`: selected subcommand.
- `project_root`: resolved Isomer Project root.
- `research_topic_id`: selected Research Topic.
- `topic_workspace_dir`: Project Manifest-declared Topic Workspace directory.
- `topic_workspace_pixi_binding`: `manifest_path_or_dir`, `manifest_path`, `pixi_environment`, and binding source.
- `requester`: Project Operator Session, Operator Agent, Service Request ref, or explicit blocker.
- `confirmation_source`: direct mutation confirmation, Service Request authorization, or read-only invocation.
- `service_request_refs`: optional Service Request refs when available.
- `support_artifact_refs`: optional support Artifact refs when available.
- `provenance_refs`: optional Provenance refs when available.
- `semantic_paths`: resolved labels, paths, storage profiles, sources, source details, diagnostics, readiness, and blockers for `topic.repos.main`, `topic.repos.main.isomer_managed`, `topic.agents_root`, `topic.records`, `topic.runtime`, `topic.env.topic_setup_target_spec`, `topic.intent.agent_env_requirements`, `topic.env.agent_setup_target_spec`, `agent.workspace`, and required agent support labels.
- `topic_environment_status`: predecessor evidence status: ready, missing, stale, blocked, failed, or not checked.
- `topic_env_target_spec_label`: `topic.env.topic_setup_target_spec`.
- `topic_env_target_spec_path`: resolved predecessor target spec path.
- `agent_env_source_label`: `topic.intent.agent_env_requirements` when source intent is used.
- `agent_env_source_path`: resolved source intent path, defaulting to `<topic-workspace-dir>/intent/src/agent-env-gate.md`.
- `agent_env_source_storage_profile`: storage profile for the resolved source intent path.
- `agent_env_source_source`: manifest, default profile, explicit override, or missing.
- `agent_env_source_source_detail`: specific binding, default, or override detail.
- `agent_env_source_diagnostics`: path-resolution warnings and blockers.
- `agent_env_target_spec_label`: `topic.env.agent_setup_target_spec` when the operational target spec is used or written.
- `agent_env_target_spec_path`: resolved target spec path, defaulting to `<topic-workspace-dir>/intent/derived/isomer-agent-env-gate.md`.
- `agent_env_target_spec_storage_profile`: storage profile for the resolved target spec path.
- `agent_env_target_spec_source`: manifest, default profile, explicit input, or missing.
- `agent_env_target_spec_source_detail`: specific binding, explicit file, explicit prompt/context, or default detail.
- `agent_env_target_spec_diagnostics`: path-resolution warnings and blockers.
- `topic_main_repository`: resolved `topic.repos.main` path, label source, Git state, owner branch, changed files, and blockers.
- `agent_workspace_paths`: Agent Name, role id, resolved `agent.workspace`, source, branch, worktree status, and blockers.
- `branch_plan`: owner branch `topic-owner/main`, default `per-agent/<agent-name>/main` branches, and any future branch namespace notes.
- `worktree_status_by_agent`: ready, created, blocked, failed, or not checked for each authoritative Agent Name.
- `readiness_by_agent`: ready, failed, blocked, or not checked for each authoritative Agent Name.
- `overall_readiness_status`: ready only after every authoritative planned Agent Name has a valid worktree, required support paths, path evidence, and passing cwd verification.
- `selected_agent_partial`: selected Agent Name and partial evidence status when a direct subcommand targets one authoritative Agent Name.
- `commands_run`: commands executed, in order, including every `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...` verification command.
- `changed_files`: files created or changed, including the resolved `topic.env.agent_setup_target_spec`, boundary material, support path policy files, and Git metadata-affecting commands.
- `blockers`: missing inputs, missing Topic Workspace env predecessor, missing source gate, agent-plan-conflict, unsafe path, unsafe existing repository, nonmatching worktree, duplicate branch checkout, failing cwd gate command, out-of-scope request, or repair requirement.
- `next_action`: safe follow-up, repair route, selected-agent rerun, route to `isomer-srv-topic-env-setup`, route to Topic Team Specialization, or stop condition.

## Guardrails

- Do not create per-agent Pixi manifests, per-agent lockfiles, per-agent `.pixi/` directories, or dependency environments by default.
- Do not install or mutate Topic Workspace dependencies. Report missing or stale Topic Workspace dependency readiness as a repair next action for `isomer-srv-topic-env-setup`.
- Do not create Agent Instances, mutate Workspace Runtime records, launch Houmao agents, run Execution Adapters, create Houmao launch material, or make research decisions.
- Do not infer Agent Names from directories, branches, provider ids, or ad hoc maps. Use the Topic Team Instantiation Packet or Topic Agent Team Profile material derived from that packet as the Agent Name authority. A matching explicit operator-provided map is only corroborating evidence; a disagreement is an `agent-plan-conflict` blocker.
- Do not overwrite, delete, clean, reset, reinitialize, reclone, rewrite history, or silently repair existing repositories or Agent Workspace paths.
- Resolve semantic labels before filesystem mutation. Default paths may appear only as examples from `isomer-default.v1`; semantic labels and path sources remain the contract.
- Keep the resolved `topic.repos.main` path as a normal non-bare Topic Main Repository and each resolved `agent.workspace` path as a worktree of that repository on `per-agent/<agent-name>/main`.
- Treat `topic.repos.main.tmp` and `agent.tmp` as local ignored disposable surfaces when available. Do not use tmp contents as durable readiness evidence.
- Direct Project Operator Session invocation is allowed after selected Project, Research Topic, Topic Workspace, topic env predecessor evidence, authoritative Agent Name plan, and mutation scope are confirmed. Record optional Service Request, support Artifact, and Provenance refs when available.
- Selected-agent direct verification is partial evidence. It must not report `overall_readiness_status` as ready unless the complete planned Agent Name matrix has passed.
