---
name: isomer-srv-topic-env-setup
description: Use when an Isomer Labs agent needs gate-driven enclosed Pixi development environment setup for a Topic Workspace independent of Topic Agent Team Profile or Agent Team Instance structure, including topic.intent.topic_env_requirements, topic.env.topic_setup_target_spec, explicit manual target specs, topic_standalone_pixi_bindings, Topic Main Development Repository setup, external repository target planning and verified registration, external repository projections, Python version selection, starter Python dependencies, Topic Workspace VCS ignores, PyPI/Pixi dependency inference, package-source evidence, Pixi command style, explicit external runtime wiring, topic-local user-space fallback, no-sudo blockers, or topic-root and repo-specific readiness checks.
skill_invocation_notation: >
  Top-level skill entrypoints use SKILL.md. Parent-scoped subskill entrypoints use
  SKILL-MAIN.md and are loaded explicitly through their parent; nested SKILL.md is
  accepted only as legacy input when SKILL-MAIN.md is absent.
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Isomer Service Topic Environment Setup

## Overview

- **Purpose**: set up and validate the Topic Workspace Pixi development environment for a user-specified runnable target.
- **Inputs**: use `topic.intent.topic_env_requirements` to create or update `topic.env.topic_setup_target_spec`; direct service calls may supply an explicit manual target spec. A dispatched canonical Service Request may instead supply the supported scope, task, authorization, expected outputs, research plan, and Run refs.
- **Readiness**: one agent or operator can run the required commands from the Topic Workspace root, Topic Main Development Repository, or a repo-specific working directory named by the target spec.
- **Resource classification**: ask `isomer-misc-bounded-run-tips` to classify resource-relevant setup and verification operations; record classification source, classification result, reason, resource dimensions, and whether bounded guidance is required.
- **Bounded proof**: operations classified as `heavy` or `unknown-risk` need bounded real-path verification; generic best-effort judgment is allowed only when no recipe applies. A generic smoke test is allowed only as supporting evidence.
- **Scope**: Topic environment setup is independent of Topic Agent Team structure. Do not require `<topic-workspace>/team-profile/`, Topic Agent Team Profile material, Topic Team Instantiation Packets, Agent Workspace plans, roles, or agent count.
- **Ownership**: this skill owns Topic Main Development Repository setup, Topic Main Development Repository Git state evidence, external repository requirements and target planning, post-verification semantic registration, and external repo projections when the target spec requires them. The acting user or agent selects and runs prompt-sensitive repository commands outside Isomer, with exact user commands taking priority. This skill does not read `topic.intent.agent_env_requirements`, create `topic.env.agent_setup_target_spec`, prepare Agent Workspace worktrees, or prove every `agent.workspace` cwd.
- **Enclosure**: prefer Pixi-managed dependencies, use explicit Pixi-run runtime wiring only when needed, use topic-local user-space fallback only as a secondary option, and block privileged or machine-global mutation.
- **Ad hoc package routing**: when a user or another skill asks only to install, add, repair, update, remove, or verify packages for a selected Topic Workspace, route that request to the matching `isomer-op-entrypoint->topic-manage env-*` command instead of treating this service as a competing ad hoc package mutation entrypoint.
- **Routing**: keep the entrypoint lean, choose one subcommand, then load that subcommand's reference page.

## When to Use

Use this skill for full gate-driven Topic Workspace environment setup, source-gate derivation, dependency installation from an existing target spec, Topic Main Development Repository setup, external repository acquisition orchestration or projection, or topic-root and repo-specific readiness checks.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Handle help intent**:
   - If the invocation has no prompt, or if the user asks for help, usage, or available functionality, answer from **Help**.
   - Stop unless they also ask for a concrete setup task.
2. **Route package-add intent**:
   - If the prompt asks only to install, add, repair, update, remove, or verify packages for a selected Topic Workspace, route to the matching `isomer-op-entrypoint->topic-manage env-install-packages`, `isomer-op-entrypoint->topic-manage env-update-packages`, `isomer-op-entrypoint->topic-manage env-remove-packages`, or verification command.
   - Continue in this service only when the user asks for full gate-driven Topic Workspace environment setup, source-gate derivation, dependency installation from an existing target spec, or environment verification.
3. **Resolve a Service Request when present**:
   - Load the request with `isomer-cli --print-json project service-requests status`, verify that its scope is supported, authorization is sufficient, expected outputs are explicit, and linked research plan and Run refs resolve.
   - Keep the Service Request distinct from the Research Task, Workflow Stage, Gate, Execution Adapter Command Request, and Run. Do not copy provider-specific or dispatch-form implementation payloads into environment Artifacts.
   - Select `fulfill-service-request` for a dispatched environment-preparation request.
4. **Select one subcommand** from the **Subcommands** tables:
   - Prefer procedural or misc subcommands.
   - Use a helper subcommand only if one is added later and the user explicitly asks for it.
   - If the prompt describes a concrete Topic Workspace setup task but does not name a subcommand, use `setup-topic-env`.
5. **Load the selected reference file**.
6. **Resolve that page's required inputs** from its `## Required Inputs` section, then execute its `## Workflow`.
7. **Report results** using **Essential Output** by default and **Complete Output** when requested. Return environment, Gate revision, smoke script, smoke result, blocker, command request, Run, support Artifact, and Provenance Record refs when a Service Request asked for them.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the subcommands, selected reference page, output contract, and guardrails in this skill, then execute the plan.

## Subcommands

Load only the subcommand pages needed for the user's task. Complex skills divide subcommands into three parts: procedural, helper, and misc.

### Procedural Subcommands

Procedural subcommands are the public single-step workflow API. Call them directly for manual or partial setup.

| Subcommand | Use For | Reference |
| --- | --- | --- |
| `resolve-topic-workspace` | Resolve Project root, Research Topic, Topic Workspace, active Pixi binding, and setup preconditions. | [references/resolve-topic-workspace.md](references/resolve-topic-workspace.md) |
| `read-env-gate` | Resolve and read `topic.intent.topic_env_requirements` and identify the runnable target. | [references/read-env-gate.md](references/read-env-gate.md) |
| `derive-env-gate` | Generate or update `topic.env.topic_setup_target_spec`, or validate an explicit manual target spec. | [references/derive-env-gate.md](references/derive-env-gate.md) |
| `ensure-topic-main-repository` | Create, reuse, configure, and verify the Topic Main Development Repository resolved by `topic.repos.main`. | [references/ensure-topic-main-repository.md](references/ensure-topic-main-repository.md) |
| `ensure-topic-repos` | Reuse verified registered repositories or plan, externally acquire, verify, and register missing non-main `topic.repos.*` repositories. | [references/ensure-topic-repos.md](references/ensure-topic-repos.md) |
| `project-extern-repos` | Materialize or validate external repository projections inside topic-main and write projection metadata. | [references/project-extern-repos.md](references/project-extern-repos.md) |
| `install-topic-deps` | Infer package sources and install dependencies through the Topic Workspace Pixi environment. | [references/install-topic-deps.md](references/install-topic-deps.md) |
| `verify-env-gate` | Run the desired command through Pixi and report readiness. | [references/verify-env-gate.md](references/verify-env-gate.md) |

### Helper Subcommands

Helper subcommands are lower-level commands called by procedural subcommands. This skill currently exposes no helper subcommands. If future helpers are added, list them here and keep them out of **Help** unless they become public workflow steps.

### Misc Subcommands

Misc subcommands are public support commands and shortcuts.

| Subcommand | Use For | Reference |
| --- | --- | --- |
| `help` | Explain this skill and list public subcommands. | This entrypoint |
| `setup-topic-env` | Run the full gate-driven Topic Workspace setup workflow. This is the default for concrete setup tasks that do not name a subcommand. | [references/setup-topic-env.md](references/setup-topic-env.md) |
| `fulfill-service-request` | Consume one recorded environment-preparation Service Request, perform only its authorized synchronous work, and return typed support refs. | [references/fulfill-service-request.md](references/fulfill-service-request.md) |

Load exactly one reference page for the selected subcommand. The `setup-topic-env` reference may then load the procedural subcommand references it orchestrates.

Each executable reference page owns its `## Required Inputs` contract. Use the selected page as the self-contained input guide for direct calls.

## Help

`isomer-srv-topic-env-setup` prepares a Topic Workspace Pixi development environment so the user-specified target in `topic.intent.topic_env_requirements` or an explicit manual target spec can run. It assumes a single capable agent or operator needs to execute research commands in the selected Topic Workspace; it does not need a topic team profile, live Agent Team Instance, role list, or agent count. It produces Topic Workspace predecessor evidence for later workflows, including Agent Workspace setup when a different caller requests that. It preserves environment enclosure by preferring Pixi-managed dependencies, recording any external runtime wiring that must be routed through Pixi-run commands, limiting fallback installs to topic-local user space, and refusing sudo or machine-global mutation. For ad hoc package install, update, remove, or package verification requests from users or research skills, route to `isomer-op-entrypoint->topic-manage env-install-packages`, `isomer-op-entrypoint->topic-manage env-update-packages`, `isomer-op-entrypoint->topic-manage env-remove-packages`, or the matching verification command; use this service for full gate-driven setup and verification. Public subcommands are grouped below.

Procedural subcommands:

| Subcommand | Purpose | Produces |
| --- | --- | --- |
| `resolve-topic-workspace` | Resolve the Project root, Research Topic, Topic Workspace, Pixi manifest, and selected Pixi environment. | Resolved setup refs and blockers; no environment mutation. |
| `read-env-gate` | Read the source gate and extract the runnable target, repo hints, commands, and success criteria. | Source gate summary and readiness blockers. |
| `derive-env-gate` | Write the fixed-section operational target spec, including the enclosure strategy for each dependency or runtime need. | `topic.env.topic_setup_target_spec`, defaulting to `<topic-workspace-dir>/intent/derived/isomer-env-gate.md`. |
| `ensure-topic-main-repository` | Prepare the topic-owned development repository resolved by `topic.repos.main`. | Git state, owner branch posture, Isomer-managed namespace posture, changed files, commands run, and blockers. |
| `ensure-topic-repos` | Reuse verified required repos or orchestrate external acquisition and post-verification registration at non-main `topic.repos.*` paths. | Repo inventory, selected external methods, verification and registration evidence, partial-result posture, inspection notes, and blockers. |
| `project-extern-repos` | Expose canonical external repos inside topic-main when the target spec requires agent-readable or writable projections. | Projection paths, projection access intent, projection mode, manifest entries, changed files, and blockers. |
| `install-topic-deps` | Install inferred dependencies from an existing topic env target spec during full gate-driven setup; ad hoc package install, update, remove, or package verification requests route to `isomer-op-topic-mgr env-*` commands. | Updated Topic Workspace Pixi environment files, `.gitignore`, dependency plan, enclosure records, and blockers. |
| `verify-env-gate` | Run the desired command through recorded Pixi-scoped commands and report Topic Workspace readiness. | Gate execution results, readiness status, enclosure warnings, and blockers; per-Agent Workspace readiness remains not checked. |

Misc subcommands:

| Subcommand | Purpose | Produces |
| --- | --- | --- |
| `setup-topic-env` | Run the full setup flow in `fast-forward`/`auto` or `step-by-step`/`manual` mode. | Combined setup report, selected mode, topic-main Git state, repo state, projection metadata, derived gate, Pixi environment files, enclosure strategy, and Topic Workspace readiness status. |
| `fulfill-service-request` | Fulfill one supported synchronous environment request. | Service Request status plus environment, Gate revision, smoke script, smoke result, blocker, command request, Run, support Artifact, and provenance refs. |
| `help` | Print what this skill does and how to use it. | Usage table and examples. |

Example prompts:

- `isomer-op-entrypoint->topic-env help`
- `isomer-op-entrypoint->topic-env`
- `isomer-op-entrypoint->topic-env setup-topic-env <topic-id> auto`
- `isomer-op-entrypoint->topic-env setup-topic-env <topic-id> manual`
- `isomer-op-entrypoint->topic-env read-env-gate for <topic-id>`
- `isomer-op-entrypoint->topic-env verify-env-gate for <topic-id>`

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format. When important handoff detail is omitted, say that Complete Output is available on request.

### Essential Output

Lead with Topic environment readiness and the selected setup mode. Name the Research Topic, Topic Workspace, Pixi manifest and environment, then summarize Topic Main Development Repository readiness, external repository projections, the critical environment gate, and important changed files. When dispatched, name the Service Request, support Artifact, command request, Run, Gate revision, smoke script and result, blockers, and next safe action. Clarify when per-Agent cwd readiness was not checked.

### Complete Output

When requested, include grouped handoff and audit fields:

- **Identity**: `subcommand`, `mode`, `project_root`, `research_topic_id`, `topic_workspace_dir`, `service_request_refs`, `research_plan_refs`, and `research_run_refs`.
- **Semantic paths**: `semantic_paths`, `topic.workspace`, `topic.repos.main`, `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, `topic.repos.main.projections.manifest`, `topic.records`, `topic.runtime`, `manifest_path_or_dir`, `manifest_path`, `pixi_environment`, and `path_diagnostics`.
- **Source and target specs**: `topic_env_source_label`, `topic_env_source_path`, `topic_env_source_storage_profile`, `topic_env_source`, `topic_env_source_detail`, `topic_env_target_spec_label`, `topic_env_target_spec_path`, `topic_env_target_spec_storage_profile`, `topic_env_target_spec_source`, and `topic_env_target_spec_source_detail`.
- **Repos and projections**: `repos`, `topic_main_repository`, `external_repo_projections`, `external_repo_projection_manifest`, and `inferred_source_warnings`.
- **External repository methods**: `external_repository_methods`, including requested and resolved source, semantic label, candidate target, user-supplied or agent-selected method, non-secret options and rationale, external verification evidence, registration result, partial-result posture, and blockers.
- **Dependencies and enclosure**: `dependency_plan`, `environment_enclosure`, `external_runtime_wiring`, `topic_local_fallbacks`, and `enclosure_warnings`.
- **Operations and resources**: `resource_check_status`, `operation_classification`, `resource_check_evidence`, and `resource_conservative_decisions`.
- **Execution result**: `commands_run`, `changed_files`, `readiness_status`, blockers, `per_agent_readiness_status`, and `next_action`.

## Operational Contract

- Allow direct Isomer setup mutation for the selected Topic Workspace Pixi environment, Topic Main Development Repository Isomer-managed namespace, post-verification non-main repository registration, and external projections under `isomer-managed/topic-owned/{readonly,writable}/extern/` after confirmation. Repository source-control or copy commands use the acting user or agent's external command surface and never a Service Request or Isomer command API.
- Consume only the authorized scope of a supplied canonical Service Request and complete it synchronously or return a stable timeout or interruption posture. Reject no-wait dispatch. Return typed support refs and keep dispatch-provider and Houmao details out of canonical schema, CLI labels, and Artifact payloads.
- Plan topic repository targets through semantic labels before external acquisition. Use `project paths default <label>` only as a read-only candidate query, honor safe explicit targets, verify source and immutable identity externally, and then use `project repos register <label> --path <existing-target>`. Do not rely on default-looking directories alone or create a binding before verification.
- Honor exact user-supplied repository procedures. When the user supplies none, select external commands that fit the requested source, revision, authentication posture, repository features, target spec, resources, and inspection needs. Record a sanitized method description, relevant non-secret options, rationale, result status, and observed immutable identity without imposing a default provider, remote name, clone depth, or history posture.
- When an external command fails, leaves partial content, or produces an unexpected identity, do not register the target and do not clean, repair, move, or delete it through Isomer. Record filesystem posture, impact, safe resume condition, and blockers; omit credentials, signed query strings, headers, environment values, credential-helper output, and raw stdout or stderr.
- Apply the enclosure ladder before dependency mutation or verification: Pixi-managed install first, Pixi-mediated external runtime wiring second, topic-local user-space fallback under `<topic-workspace-dir>/.isomer-user-env/` third, and blockers for privileged or machine-global mutation.
- Use `pixi add --manifest-path <manifest_path> ...` or `pixi install --manifest-path <manifest_path> --environment <pixi_environment>` when mutating dependencies so changes target the selected Topic Workspace manifest.
- Use `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <command>` for Topic Workspace setup, inspection, or verification commands inside the prepared environment instead of relying on the ambient shell environment. Explicitly sourced scripts and exported runtime paths are allowed only when recorded in `topic.env.topic_setup_target_spec` and the execution log.
- Ask `isomer-misc-bounded-run-tips` to classify each relevant setup or verification operation as `light`, `heavy`, `unknown-risk`, or `not-applicable` before resource-check planning. Treat `heavy` and `unknown-risk` as requiring bounded real-path guidance or a blocker. Treat examples such as CUDA compile, model inference, downloads, archive extraction, broad tests, or GPU jobs as examples only; bounded-run tips owns the classification decision. Do not replace the essential source-intent path with an unrelated smoke test.

## Operational Notes

- Accept an explicit `topic_standalone_pixi_bindings.manifest_path_or_dir` file or directory target, or the implicit registered Topic Workspace directory default when Pixi resolves it as a confined Topic Workspace Pixi workspace.
- If read-only diagnostics mention them, report them only as unrelated downstream context unless they also break Topic Workspace discovery, Pixi binding resolution, source gate reading, dependency setup, repo checks, or Pixi-scoped verification.
- Report per-Agent Workspace readiness as not checked when it is relevant to the caller.
- Use the Project Manifest for explicit bindings and the registered Topic Workspace directory only as the defined implicit default target.
- Route user-facing or research-skill package install, update, remove, or package verification handoffs to the matching `isomer-op-entrypoint->topic-manage env-*` command unless the user explicitly requests the full gate-driven setup workflow.
- Report those needs as blockers or external prerequisites.
- Resolve the appropriate topic repository label, register the appropriate non-main `topic.repos.*` label when needed, and use that path.
- Inspect it as read-only evidence and report blockers if it is unsuitable unless the target spec explicitly authorizes that repository mutation.
- Warning-label them in `topic.env.topic_setup_target_spec` and final output.

## Guardrails

- DO NOT install or mutate a Topic Workspace environment until the selected Topic Workspace and effective Topic Workspace Pixi binding are confirmed.
- DO NOT treat the Project-root Pixi environment as the Topic Workspace execution environment.
- DO NOT require or inspect Topic Agent Team Profile material, `<topic-workspace-dir>/team-profile/`, Topic Team Instantiation Packets, Agent Team Instances, Agent Instances, Agent Workspace plans, roles, or agent count as prerequisites for Topic Workspace environment setup.
- DO NOT read `topic.intent.agent_env_requirements`, create `topic.env.agent_setup_target_spec`, create Agent Workspace worktrees, verify commands from every `agent.workspace` cwd, or claim per-agent environment readiness from topic-root verification.
- DO NOT create or mutate per-agent Pixi environments unless a user task explicitly names an Agent Workspace-specific environment.
- DO NOT place required independent repos in the Project root, Agent Workspace, `.pixi/`, or another ad hoc location.
- DO NOT modify an existing canonical external repository at the resolved non-main `topic.repos.*` path during `ensure-topic-repos`
- DO NOT infer a binding from directory names or Research Topic ids.
- DO NOT choose repos, dependencies, Pixi install commands, setup commands, or verification commands before resolving `topic.intent.topic_env_requirements` or accepting an explicit operational target spec.
- DO NOT use this service as the public bypass for ad hoc package mutation requests.
- DO NOT run `sudo`, mutate system package managers, edit global shell profiles, install global Python or Node packages, change `/etc`, run `ldconfig`, install daemons, change kernel drivers, or perform other privileged or machine-global setup from this skill.
- DO NOT hide inferred repo sources.
- DO NOT launch Houmao agents, create Agent Instances, materialize Topic Agent Team Profiles, mutate unrelated Workspace Runtime records, perform GUI work, or make research decisions from this skill.
## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
