---
name: isomer-srv-topic-env-setup
description: Use when an Isomer Labs agent needs gate-driven enclosed Pixi development environment setup for a Topic Workspace independent of Topic Agent Team Profile or Agent Team Instance structure, including topic.intent.topic_env_requirements, topic.env.topic_setup_target_spec, explicit manual target specs, topic_standalone_pixi_bindings, Topic Main Development Repository setup, canonical external repo acquisition, external repository projections, Python version selection, starter Python dependencies, Topic Workspace VCS ignores, PyPI/Pixi dependency inference, package-source evidence, Pixi command style, explicit external runtime wiring, topic-local user-space fallback, no-sudo blockers, or topic-root and repo-specific readiness checks.
---

# Isomer Service Topic Environment Setup

## Overview

Set up and validate the Topic Workspace Pixi development environment for a user-specified runnable target. The normal operator flow reads source intent from `topic.intent.topic_env_requirements`, creates or updates the operational target spec at `topic.env.topic_setup_target_spec`, then materializes and verifies from that target spec. Manual invocation may supply an explicit target spec file, prompt, or context instead of source intent. Readiness means one agent or operator can run the commands needed to conduct the research from the selected Topic Workspace root, the Topic Main Development Repository, or a repo-specific working directory named by the target spec. Heavy work such as compilation, model inference, dataset processing, and benchmark execution still needs bounded real-path verification: design a small but real build, inference, dataset, or benchmark run that exercises the essential code path named by the source intent. A generic smoke test is allowed only as supporting evidence; it cannot replace a source-intent runnable target. The result is Topic Workspace predecessor evidence for later workflows, including Topic Main Development Repository Git state, each external repo projection status, and projection metadata, not proof that every Agent Workspace cwd can run. Keep setup enclosed and auditable: use Pixi-managed dependencies first, use explicit Pixi-run runtime wiring only when Pixi cannot fully provide a runtime piece, use topic-local user-space fallback only as a secondary option, and block privileged or machine-global mutation.

Topic environment setup is independent of Topic Agent Team structure. Do not require `<topic-workspace>/team-profile/`, Topic Agent Team Profile material, Topic Team Instantiation Packets, Agent Team Instance records, Agent Instance records, Agent Workspace plans, roles, or agent count before preparing the Topic Workspace environment.

Topic environment readiness is topic-scoped. This skill owns Topic Main Development Repository creation, configuration, and verification for the selected Topic Workspace; it also owns canonical external repository acquisition and external repository projection materialization when the target spec requires them. This skill does not read `topic.intent.agent_env_requirements`, does not create `topic.env.agent_setup_target_spec`, does not prepare Agent Workspace worktrees, and does not prove that every `agent.workspace` cwd can run gate commands. If a caller also needs per-Agent Workspace cwd proof, this skill reports that proof as not checked and leaves the follow-up decision to the operator or to `isomer-srv-agent-env-setup`.

This skill is a command-style router: keep the entrypoint lean, choose one subcommand, then load that subcommand's reference page.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Handle help intent**:
   - If the invocation has no prompt, or if the user asks for help, usage, or available functionality, answer from **Help**.
   - Stop unless they also ask for a concrete setup task.
2. **Select one subcommand** from the **Subcommands** tables:
   - Prefer procedural or misc subcommands.
   - Use a helper subcommand only if one is added later and the user explicitly asks for it.
   - If the prompt describes a concrete Topic Workspace setup task but does not name a subcommand, use `setup-topic-env`.
3. **Load the selected reference file**.
4. **Resolve that page's required inputs** from its `## Required Inputs` section, then execute its `## Workflow`.
5. **Report results** using **Output Contract**.

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

`isomer-srv-topic-env-setup` prepares a Topic Workspace Pixi development environment so the user-specified target in `topic.intent.topic_env_requirements` or an explicit manual target spec can run. It assumes a single capable agent or operator needs to execute research commands in the selected Topic Workspace; it does not need a topic team profile, live Agent Team Instance, role list, or agent count. It produces Topic Workspace predecessor evidence for later workflows, including Agent Workspace setup when a different caller requests that. It preserves environment enclosure by preferring Pixi-managed dependencies, recording any external runtime wiring that must be routed through Pixi-run commands, limiting fallback installs to topic-local user space, and refusing sudo or machine-global mutation. Public subcommands are grouped below.

Procedural subcommands:

| Subcommand | Purpose | Produces |
| --- | --- | --- |
| `resolve-topic-workspace` | Resolve the Project root, Research Topic, Topic Workspace, Pixi manifest, and selected Pixi environment. | Resolved setup refs and blockers; no environment mutation. |
| `read-env-gate` | Read the source gate and extract the runnable target, repo hints, commands, and success criteria. | Source gate summary and readiness blockers. |
| `derive-env-gate` | Write the fixed-section operational target spec, including the enclosure strategy for each dependency or runtime need. | `topic.env.topic_setup_target_spec`, defaulting to `<topic-workspace-dir>/intent/derived/isomer-env-gate.md`. |
| `ensure-topic-main-repository` | Prepare the topic-owned development repository resolved by `topic.repos.main`. | Git state, owner branch posture, Isomer-managed namespace posture, changed files, commands run, and blockers. |
| `ensure-topic-repos` | Find existing required repos or materialize missing canonical external repos at resolved non-main `topic.repos.*` paths, defaulting helper-created repos under `repos/extern/...`. | Repo inventory and inspection notes; acquired topic repos and inferred-source warnings only for missing repos. |
| `project-extern-repos` | Expose canonical external repos inside topic-main when the target spec requires agent-readable or writable projections. | Projection paths, projection access intent, projection mode, manifest entries, changed files, and blockers. |
| `install-topic-deps` | Install inferred dependencies with Pixi first, record explicit external runtime wiring when needed, and use topic-local fallback only when Pixi cannot satisfy the gate. | Updated Topic Workspace Pixi environment files, `.gitignore`, dependency plan, enclosure records, and blockers. |
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

Report:

- `subcommand`: selected subcommand.
- `mode`: selected `setup-topic-env` mode when relevant.
- `project_root`: resolved Isomer Project root.
- `research_topic_id`: selected Research Topic.
- `topic_workspace_dir`: Project Manifest-declared Topic Workspace directory.
- `semantic_paths`: resolved labels, paths, sources, storage profiles, source details, diagnostics, and blockers for setup surfaces such as `topic.workspace`, `topic.repos.main`, `topic.repos.main.isomer_managed`, `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, `topic.repos.main.projections.manifest`, `topic.records`, `topic.runtime`, `topic.intent.topic_env_requirements`, and `topic.env.topic_setup_target_spec`.
- `manifest_path_or_dir`: explicit binding target when present, otherwise the registered Topic Workspace directory default.
- `manifest_path`: Pixi-resolved Topic Workspace Pixi manifest path.
- `pixi_environment`: selected Pixi environment.
- `topic_env_source_label`: `topic.intent.topic_env_requirements` when source intent is used.
- `topic_env_source_path`: resolved source intent path, defaulting to `<topic-workspace-dir>/intent/src/topic-env-gate.md`.
- `topic_env_source_storage_profile`: usually `topic_intent_source_file`.
- `topic_env_source`: resolver source such as `default_profile`, `topic_workspace_manifest`, `env`, or `path_plan`.
- `topic_env_source_detail`: resolver source detail such as `isomer-default.v1` or manifest binding detail.
- `topic_env_target_spec_label`: `topic.env.topic_setup_target_spec` when the operational target spec is used or written.
- `topic_env_target_spec_path`: resolved target spec path, defaulting to `<topic-workspace-dir>/intent/derived/isomer-env-gate.md`.
- `topic_env_target_spec_storage_profile`: usually `topic_env_target_spec_file`.
- `topic_env_target_spec_source`: resolver source or explicit manual target spec source.
- `topic_env_target_spec_source_detail`: resolver source detail or explicit target spec detail.
- `path_diagnostics`: Workspace Path Resolution diagnostics for source and target spec surfaces.
- `repos`: required repo names, paths, sources, and whether any source was inferred.
- `topic_main_repository`: resolved `topic.repos.main` path, source, Git state, owner branch posture, Isomer-managed namespace posture, commands run, changed files, blockers, and readiness evidence.
- `external_repo_projections`: projection access intent, canonical source label, canonical source path, projection path, projection mode, mutation policy, status, blockers, and evidence for each projected external repo.
- `external_repo_projection_manifest`: resolved `topic.repos.main.projections.manifest` path, status, changed flag, and blockers.
- `inferred_source_warnings`: warnings for repos acquired from inferred or discovered sources.
- `dependency_plan`: selected Python version, version evidence, starter Python dependencies, package sources, Pixi/PyPI choices, channels, editable installs, native tools, Python glue baseline, and enclosure strategy.
- `environment_enclosure`: dependency and runtime classification as Pixi-managed, Pixi-mediated external runtime wiring, topic-local user-space fallback, or blocked.
- `external_runtime_wiring`: any PATH, library path, compiler path, package-config path, CUDA variable, sourced script, or external runtime path used through Pixi-run commands.
- `topic_local_fallbacks`: any fallback installs under `<topic-workspace-dir>/.isomer-user-env/`, including commands, installed paths, changed files, and portability warnings.
- `enclosure_warnings`: warnings for external runtime wiring, topic-local fallbacks, host-specific paths, relocation risk, or missing enclosure records.
- `resource_check_status`: ready, deferred, blocked, or not needed for resource-heavy setup or verification commands.
- `resource_check_evidence`: lightweight host-capacity checks used before heavy operations, such as CPU load, memory, disk space, GPU availability and active GPU processes when relevant, plus the reason a check was skipped when not relevant.
- `resource_conservative_decisions`: bounded real-path choices such as reduced parallelism, selected build targets, tiny model/input shapes, sample data, reduced iterations, or small benchmark cases used to exercise essential code paths without overloading the system; blockers when no bounded real-path check can be run safely.
- `commands_run`: commands executed, in order.
- `changed_files`: environment files changed, especially `pixi.toml`, `pixi.lock`, `.pixi/`, `.gitignore`, `.isomer-user-env/` when used, topic-main `isomer-managed/.gitignore`, `isomer-managed/tracked/manifests/extern-projections.toml`, and the resolved `topic.env.topic_setup_target_spec` target spec.
- `readiness_status`: ready, failed, blocked, or not checked.
- `blockers`: missing inputs, failed preconditions, command failures, out-of-scope requests, or repair requirements.
- `per_agent_readiness_status`: always not checked by this skill when reported.
- `next_action`: safe operator follow-up, repair route, or stop condition.

## Guardrails

- Do not install or mutate a Topic Workspace environment until the selected Topic Workspace and effective Topic Workspace Pixi binding are confirmed. Accept an explicit `topic_standalone_pixi_bindings.manifest_path_or_dir` file or directory target, or the implicit registered Topic Workspace directory default when Pixi resolves it as a confined Topic Workspace Pixi workspace.
- Direct setup mutation is allowed for the selected Topic Workspace Pixi environment, Topic Main Development Repository Isomer-managed namespace, missing canonical external repos at resolved non-main `topic.repos.*` paths, and external projections under `isomer-managed/topic-owned/{readonly,writable}/extern/` after confirmation; do not require a separate Service Request for dependency, lockfile, install, repo, projection, or gate-command mutation in this workflow.
- Do not treat the Project-root Pixi environment as the Topic Workspace execution environment.
- Resolve topic repository paths through semantic labels before acquiring code. Additional durable repos should be registered as `topic.repos.*` with explicit `storage_profile` through `project repos create` or `project paths register`; do not rely on default-looking directories alone.
- Do not require or inspect Topic Agent Team Profile material, `<topic-workspace-dir>/team-profile/`, Topic Team Instantiation Packets, Agent Team Instances, Agent Instances, Agent Workspace plans, roles, or agent count as prerequisites for Topic Workspace environment setup. If read-only diagnostics mention them, report them only as unrelated downstream context unless they also break Topic Workspace discovery, Pixi binding resolution, source gate reading, dependency setup, repo checks, or Pixi-scoped verification.
- Do not read `topic.intent.agent_env_requirements`, create `topic.env.agent_setup_target_spec`, create Agent Workspace worktrees, verify commands from every `agent.workspace` cwd, or claim per-agent environment readiness from topic-root verification. Report per-Agent Workspace readiness as not checked when it is relevant to the caller.
- Do not create or mutate per-agent Pixi environments unless a user task explicitly names an Agent Workspace-specific environment.
- Do not place required independent repos in the Project root, Agent Workspace, `.pixi/`, or another ad hoc location; resolve the appropriate topic repository label, register the appropriate non-main `topic.repos.*` label when needed, and use that path.
- Do not modify an existing canonical external repository at the resolved non-main `topic.repos.*` path during `ensure-topic-repos`; inspect it as read-only evidence and report blockers if it is unsuitable unless the target spec explicitly authorizes that repository mutation.
- Do not infer a binding from directory names or Research Topic ids. Use the Project Manifest for explicit bindings and the registered Topic Workspace directory only as the defined implicit default target.
- Do not choose repos, dependencies, Pixi install commands, setup commands, or verification commands before resolving `topic.intent.topic_env_requirements` or accepting an explicit operational target spec.
- Apply the enclosure ladder before dependency mutation or verification: Pixi-managed install first, Pixi-mediated external runtime wiring second, topic-local user-space fallback under `<topic-workspace-dir>/.isomer-user-env/` third, and blockers for privileged or machine-global mutation.
- When mutating dependencies, use `pixi add --manifest-path <manifest_path> ...` or `pixi install --manifest-path <manifest_path> --environment <pixi_environment>` so changes target the selected Topic Workspace manifest.
- When running Topic Workspace setup, inspection, or verification commands inside the prepared environment, use `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <command>` instead of relying on the ambient shell environment. Explicitly sourced scripts and exported runtime paths are allowed only when recorded in `topic.env.topic_setup_target_spec` and the execution log.
- Before running resource-heavy setup or verification work, check system resources with lightweight read-only probes and choose the smallest real execution that satisfies the gate. Treat compilation, deep model inference, full dataset download, large archive extraction, broad test suites, multi-process training, or large GPU jobs as heavy, but do not replace the essential source-intent path with an unrelated smoke test. Use bounded real-path tactics such as fewer build jobs, selected kernel targets, tiny model or tensor shapes, sample data, reduced iterations, reduced batch size, metadata-limited downloads, and short benchmark cases. If no bounded real-path command can safely exercise the required path, record a blocker instead of claiming readiness.
- Do not run `sudo`, mutate system package managers, edit global shell profiles, install global Python or Node packages, change `/etc`, run `ldconfig`, install daemons, change kernel drivers, or perform other privileged or machine-global setup from this skill. Report those needs as blockers or external prerequisites.
- Do not hide inferred repo sources; warning-label them in `topic.env.topic_setup_target_spec` and final output.
- Do not launch Houmao agents, create Agent Instances, materialize Topic Agent Team Profiles, mutate unrelated Workspace Runtime records, perform GUI work, or make research decisions from this skill.
