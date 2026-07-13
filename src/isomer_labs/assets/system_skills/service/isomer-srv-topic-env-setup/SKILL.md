---
name: isomer-srv-topic-env-setup
description: Use when an Isomer Labs agent needs gate-driven enclosed Pixi development environment setup for a Topic Workspace independent of Topic Agent Team Profile or Agent Team Instance structure, including topic.intent.topic_env_requirements, topic.env.topic_setup_target_spec, explicit manual target specs, topic_standalone_pixi_bindings, Topic Main Development Repository setup, canonical external repo acquisition, external repository projections, Python version selection, starter Python dependencies, Topic Workspace VCS ignores, PyPI/Pixi dependency inference, package-source evidence, Pixi command style, explicit external runtime wiring, topic-local user-space fallback, no-sudo blockers, or topic-root and repo-specific readiness checks.
---

# Isomer Service Topic Environment Setup

## Overview

- **Purpose**: set up and validate the Topic Workspace Pixi development environment for a user-specified runnable target.
- **Inputs**: use `topic.intent.topic_env_requirements` to create or update `topic.env.topic_setup_target_spec`; direct service calls may supply an explicit manual target spec.
- **Readiness**: one agent or operator can run the required commands from the Topic Workspace root, Topic Main Development Repository, or a repo-specific working directory named by the target spec.
- **Resource classification**: ask `isomer-misc-bounded-run-tips` to classify resource-relevant setup and verification operations; record classification source, classification result, reason, resource dimensions, and whether bounded guidance is required.
- **Bounded proof**: operations classified as `heavy` or `unknown-risk` need bounded real-path verification; generic best-effort judgment is allowed only when no recipe applies. A generic smoke test is allowed only as supporting evidence.
- **Scope**: Topic environment setup is independent of Topic Agent Team structure. Do not require `<topic-workspace>/team-profile/`, Topic Agent Team Profile material, Topic Team Instantiation Packets, Agent Workspace plans, roles, or agent count.
- **Ownership**: this skill owns Topic Main Development Repository setup, Topic Main Development Repository Git state evidence, canonical external repo acquisition, clone-depth decisions, and external repo projections when the target spec requires them; it does not read `topic.intent.agent_env_requirements`, create `topic.env.agent_setup_target_spec`, prepare Agent Workspace worktrees, or prove every `agent.workspace` cwd.
- **Enclosure**: prefer Pixi-managed dependencies, use explicit Pixi-run runtime wiring only when needed, use topic-local user-space fallback only as a secondary option, and block privileged or machine-global mutation.
- **Ad hoc package routing**: when a user or another skill asks only to install, add, repair, update, remove, or verify packages for a selected Topic Workspace, route that request to the matching `$isomer-op-topic-mgr env-*` command instead of treating this service as a competing ad hoc package mutation entrypoint.
- **Routing**: keep the entrypoint lean, choose one subcommand, then load that subcommand's reference page.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Handle help intent**:
   - If the invocation has no prompt, or if the user asks for help, usage, or available functionality, answer from **Help**.
   - Stop unless they also ask for a concrete setup task.
2. **Route package-add intent**:
   - If the prompt asks only to install, add, repair, update, remove, or verify packages for a selected Topic Workspace, route to the matching `$isomer-op-topic-mgr env-install-packages`, `$isomer-op-topic-mgr env-update-packages`, `$isomer-op-topic-mgr env-remove-packages`, or verification command.
   - Continue in this service only when the user asks for full gate-driven Topic Workspace environment setup, source-gate derivation, dependency installation from an existing target spec, or environment verification.
3. **Select one subcommand** from the **Subcommands** tables:
   - Prefer procedural or misc subcommands.
   - Use a helper subcommand only if one is added later and the user explicitly asks for it.
   - If the prompt describes a concrete Topic Workspace setup task but does not name a subcommand, use `setup-topic-env`.
4. **Load the selected reference file**.
5. **Resolve that page's required inputs** from its `## Required Inputs` section, then execute its `## Workflow`.
6. **Report results** using **Essential Output** by default and **Complete Output** when requested.

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
| `ensure-topic-repos` | Find existing canonical external repos or acquire missing required repos at resolved non-main `topic.repos.*` paths. | [references/ensure-topic-repos.md](references/ensure-topic-repos.md) |
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

Load exactly one reference page for the selected subcommand. The `setup-topic-env` reference may then load the procedural subcommand references it orchestrates.

Each executable reference page owns its `## Required Inputs` contract. Use the selected page as the self-contained input guide for direct calls.

## Help

`isomer-srv-topic-env-setup` prepares a Topic Workspace Pixi development environment so the user-specified target in `topic.intent.topic_env_requirements` or an explicit manual target spec can run. It assumes a single capable agent or operator needs to execute research commands in the selected Topic Workspace; it does not need a topic team profile, live Agent Team Instance, role list, or agent count. It produces Topic Workspace predecessor evidence for later workflows, including Agent Workspace setup when a different caller requests that. It preserves environment enclosure by preferring Pixi-managed dependencies, recording any external runtime wiring that must be routed through Pixi-run commands, limiting fallback installs to topic-local user space, and refusing sudo or machine-global mutation. For ad hoc package install, update, remove, or package verification requests from users or research skills, route to `$isomer-op-topic-mgr env-install-packages`, `$isomer-op-topic-mgr env-update-packages`, `$isomer-op-topic-mgr env-remove-packages`, or the matching verification command; use this service for full gate-driven setup and verification. Public subcommands are grouped below.

Procedural subcommands:

| Subcommand | Purpose | Produces |
| --- | --- | --- |
| `resolve-topic-workspace` | Resolve the Project root, Research Topic, Topic Workspace, Pixi manifest, and selected Pixi environment. | Resolved setup refs and blockers; no environment mutation. |
| `read-env-gate` | Read the source gate and extract the runnable target, repo hints, commands, and success criteria. | Source gate summary and readiness blockers. |
| `derive-env-gate` | Write the fixed-section operational target spec, including the enclosure strategy for each dependency or runtime need. | `topic.env.topic_setup_target_spec`, defaulting to `<topic-workspace-dir>/intent/derived/isomer-env-gate.md`. |
| `ensure-topic-main-repository` | Prepare the topic-owned development repository resolved by `topic.repos.main`. | Git state, owner branch posture, Isomer-managed namespace posture, changed files, commands run, and blockers. |
| `ensure-topic-repos` | Find existing required repos or materialize missing canonical external repos at resolved non-main `topic.repos.*` paths, defaulting helper-created repos under `repos/extern/...`. | Repo inventory and inspection notes; acquired topic repos and inferred-source warnings only for missing repos. |
| `project-extern-repos` | Expose canonical external repos inside topic-main when the target spec requires agent-readable or writable projections. | Projection paths, projection access intent, projection mode, manifest entries, changed files, and blockers. |
| `install-topic-deps` | Install inferred dependencies from an existing topic env target spec during full gate-driven setup; ad hoc package install, update, remove, or package verification requests route to `isomer-op-topic-mgr env-*` commands. | Updated Topic Workspace Pixi environment files, `.gitignore`, dependency plan, enclosure records, and blockers. |
| `verify-env-gate` | Run the desired command through recorded Pixi-scoped commands and report Topic Workspace readiness. | Gate execution results, readiness status, enclosure warnings, and blockers; per-Agent Workspace readiness remains not checked. |

Misc subcommands:

| Subcommand | Purpose | Produces |
| --- | --- | --- |
| `setup-topic-env` | Run the full setup flow in `fast-forward`/`auto` or `step-by-step`/`manual` mode. | Combined setup report, selected mode, topic-main Git state, repo state, projection metadata, derived gate, Pixi environment files, enclosure strategy, and Topic Workspace readiness status. |
| `help` | Print what this skill does and how to use it. | Usage table and examples. |

Example prompts:

- `$isomer-srv-topic-env-setup help`
- `$isomer-srv-topic-env-setup`
- `$isomer-srv-topic-env-setup setup-topic-env <topic-id> auto`
- `$isomer-srv-topic-env-setup setup-topic-env <topic-id> manual`
- `$isomer-srv-topic-env-setup read-env-gate for <topic-id>`
- `$isomer-srv-topic-env-setup verify-env-gate for <topic-id>`

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format. When important handoff detail is omitted, say that Complete Output is available on request.

### Essential Output

Lead with Topic environment readiness and the selected setup mode. Name the Research Topic, Topic Workspace, Pixi manifest and environment, then summarize Topic Main Development Repository readiness, external repository projections, the critical environment gate, and important changed files. State blockers or failed commands, clarify when per-Agent cwd readiness was not checked, and end with the next safe action.

### Complete Output

When requested, include grouped handoff and audit fields:

- **Identity**: `subcommand`, `mode`, `project_root`, `research_topic_id`, and `topic_workspace_dir`.
- **Semantic paths**: `semantic_paths`, `topic.workspace`, `topic.repos.main`, `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, `topic.repos.main.projections.manifest`, `topic.records`, `topic.runtime`, `manifest_path_or_dir`, `manifest_path`, `pixi_environment`, and `path_diagnostics`.
- **Source and target specs**: `topic_env_source_label`, `topic_env_source_path`, `topic_env_source_storage_profile`, `topic_env_source`, `topic_env_source_detail`, `topic_env_target_spec_label`, `topic_env_target_spec_path`, `topic_env_target_spec_storage_profile`, `topic_env_target_spec_source`, and `topic_env_target_spec_source_detail`.
- **Repos and projections**: `repos`, `topic_main_repository`, `external_repo_projections`, `external_repo_projection_manifest`, and `inferred_source_warnings`.
- **Repo acquisition**: `repository_acquisition_decisions`, including clone mode, clone depth, full-history evidence, and snapshot evidence.
- **Dependencies and enclosure**: `dependency_plan`, `environment_enclosure`, `external_runtime_wiring`, `topic_local_fallbacks`, and `enclosure_warnings`.
- **Operations and resources**: `resource_check_status`, `operation_classification`, `resource_check_evidence`, and `resource_conservative_decisions`.
- **Execution result**: `commands_run`, `changed_files`, `readiness_status`, blockers, `per_agent_readiness_status`, and `next_action`.

## Guardrails

- Do not install or mutate a Topic Workspace environment until the selected Topic Workspace and effective Topic Workspace Pixi binding are confirmed. Accept an explicit `topic_standalone_pixi_bindings.manifest_path_or_dir` file or directory target, or the implicit registered Topic Workspace directory default when Pixi resolves it as a confined Topic Workspace Pixi workspace.
- Direct setup mutation is allowed for the selected Topic Workspace Pixi environment, Topic Main Development Repository Isomer-managed namespace, missing canonical external repos at resolved non-main `topic.repos.*` paths, and external projections under `isomer-managed/topic-owned/{readonly,writable}/extern/` after confirmation; do not require a separate Service Request for dependency, lockfile, install, repo, projection, or gate-command mutation in this workflow.
- Do not treat the Project-root Pixi environment as the Topic Workspace execution environment.
- Resolve topic repository paths through semantic labels before acquiring code. Additional durable repos should be registered as `topic.repos.*` with explicit `storage_profile` through `project repos create` or `project paths register`; do not rely on default-looking directories alone.
- Before acquiring a Git repository, decide whether the work needs full Git history or only a source snapshot. Default to a shallow clone with `--depth=1` unless the prompt, Research Topic, topic env source intent, target spec, benchmark protocol, provenance need, bisect or debugging task, changelog analysis, branch comparison, tag traversal, or version-history requirement implies full history. Record the clone mode, clone depth, and evidence for the decision.
- Do not require or inspect Topic Agent Team Profile material, `<topic-workspace-dir>/team-profile/`, Topic Team Instantiation Packets, Agent Team Instances, Agent Instances, Agent Workspace plans, roles, or agent count as prerequisites for Topic Workspace environment setup. If read-only diagnostics mention them, report them only as unrelated downstream context unless they also break Topic Workspace discovery, Pixi binding resolution, source gate reading, dependency setup, repo checks, or Pixi-scoped verification.
- Do not read `topic.intent.agent_env_requirements`, create `topic.env.agent_setup_target_spec`, create Agent Workspace worktrees, verify commands from every `agent.workspace` cwd, or claim per-agent environment readiness from topic-root verification. Report per-Agent Workspace readiness as not checked when it is relevant to the caller.
- Do not create or mutate per-agent Pixi environments unless a user task explicitly names an Agent Workspace-specific environment.
- Do not place required independent repos in the Project root, Agent Workspace, `.pixi/`, or another ad hoc location; resolve the appropriate topic repository label, register the appropriate non-main `topic.repos.*` label when needed, and use that path.
- Do not modify an existing canonical external repository at the resolved non-main `topic.repos.*` path during `ensure-topic-repos`; inspect it as read-only evidence and report blockers if it is unsuitable unless the target spec explicitly authorizes that repository mutation.
- Do not infer a binding from directory names or Research Topic ids. Use the Project Manifest for explicit bindings and the registered Topic Workspace directory only as the defined implicit default target.
- Do not choose repos, dependencies, Pixi install commands, setup commands, or verification commands before resolving `topic.intent.topic_env_requirements` or accepting an explicit operational target spec.
- Do not use this service as the public bypass for ad hoc package mutation requests. Route user-facing or research-skill package install, update, remove, or package verification handoffs to the matching `$isomer-op-topic-mgr env-*` command unless the user explicitly requests the full gate-driven setup workflow.
- Apply the enclosure ladder before dependency mutation or verification: Pixi-managed install first, Pixi-mediated external runtime wiring second, topic-local user-space fallback under `<topic-workspace-dir>/.isomer-user-env/` third, and blockers for privileged or machine-global mutation.
- When mutating dependencies, use `pixi add --manifest-path <manifest_path> ...` or `pixi install --manifest-path <manifest_path> --environment <pixi_environment>` so changes target the selected Topic Workspace manifest.
- When running Topic Workspace setup, inspection, or verification commands inside the prepared environment, use `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <command>` instead of relying on the ambient shell environment. Explicitly sourced scripts and exported runtime paths are allowed only when recorded in `topic.env.topic_setup_target_spec` and the execution log.
- Before resource-check planning, ask `isomer-misc-bounded-run-tips` to classify each relevant setup or verification operation as `light`, `heavy`, `unknown-risk`, or `not-applicable`. Treat `heavy` and `unknown-risk` as requiring bounded real-path guidance or a blocker. Treat examples such as CUDA compile, model inference, downloads, archive extraction, broad tests, or GPU jobs as examples only; bounded-run tips owns the classification decision. Do not replace the essential source-intent path with an unrelated smoke test.
- Do not run `sudo`, mutate system package managers, edit global shell profiles, install global Python or Node packages, change `/etc`, run `ldconfig`, install daemons, change kernel drivers, or perform other privileged or machine-global setup from this skill. Report those needs as blockers or external prerequisites.
- Do not hide inferred repo sources; warning-label them in `topic.env.topic_setup_target_spec` and final output.
- Do not launch Houmao agents, create Agent Instances, materialize Topic Agent Team Profiles, mutate unrelated Workspace Runtime records, perform GUI work, or make research decisions from this skill.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
