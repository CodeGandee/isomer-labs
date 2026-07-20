# Ensure Topic Main Development Repository

Use this subcommand to create, reuse, configure, and verify the Topic Main Development Repository resolved by `topic.repos.main` as Topic Workspace predecessor evidence.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Workspace context | Require `project_root`, `research_topic_id`, `topic_workspace_dir`, `semantic_paths`, `topic.repos.main`, `topic.repos.main.isomer_managed`, `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, `topic.repos.main.projections.manifest`, `manifest_path_or_dir`, `manifest_path`, and `pixi_environment` from `resolve-topic-workspace`. |
| Topic env target spec | Require `topic.env.topic_setup_target_spec` from `derive-env-gate` or an explicit validated target spec. |
| Mutation confirmation | Require direct Project Operator Session mutation confirmation or equivalent service authorization before creating or changing files. |
| Optional modifiers | None for this step. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**:
   - Require workspace context, semantic path evidence, target spec evidence, and mutation confirmation.
2. **Inspect the resolved `topic.repos.main` path**:
   - The target must be a normal non-bare Git repository, a missing safe path, an empty safe directory, or an empty normal Git repository.
3. **Initialize safe missing or empty targets** only when mutation is confirmed:
   - Create or initialize a normal non-bare Topic Main Development Repository at the resolved path.
   - Create or validate the owner branch posture required by the target spec.
   - Create a minimal baseline commit only when the repository is newly initialized and the target spec accepts that posture.
4. **Reuse existing safe repositories**:
   - Do not rewrite, clean, reset, delete, move, reclone, pull, or silently repair them.
   - Keep Isomer-created material under the resolved `topic.repos.main.isomer_managed` namespace unless the user explicitly authorizes another path.
5. **Prepare the Isomer-managed namespace**:
   - Create or validate `isomer-managed/`, `isomer-managed/.gitignore`, tracked manifest directories, and projection roots required by the target spec.
   - Ensure the ignore policy ignores `topic-owned/` projection content while keeping `tracked/` and `tracked/manifests/extern-projections.toml` trackable.
6. **Ensure topic-main agent rule guidance**:
   - Use `isomer-cli --print-json project topic-main-guidance ensure --topic <topic> --yes` or the equivalent CLI-backed API as the only source of truth for creating, appending, updating, and reporting root `AGENTS.md` and `CLAUDE.md` guidance.
   - Treat `src/isomer_labs/assets/topic_main_guidance/isomer-labs-topic-main-guidance.v1.md.j2` as the canonical large-text template asset; do not copy the full rendered guidance body into this skill.
   - Preserve existing user-authored content outside the CLI-managed marked block.
   - Carry forward the CLI guidance version, target statuses, changed files, blockers, and next action.
7. **Record predecessor evidence**:
   - Report resolved path, path source, Git state, owner branch posture, Isomer-managed namespace posture, agent guidance posture, guidance block version, commands run, changed files, blockers, and readiness status.

If the user's task does not map cleanly to these steps, use your native planning tool to separate read-only repository inspection from confirmed mutation, then execute only the safe portion.

## Blockers

Report a blocker for:

- existing non-Git content;
- bare repositories;
- corrupt repositories;
- ambiguous existing history state;
- missing base branches without an accepted repair;
- destructive repair needs;
- unsafe custom semantic bindings;
- unconfirmed mutation;
- target spec requirements that would create top-level Isomer directories in an existing user repository.

## Agent Guidance Block

The canonical guidance body is rendered by `isomer-cli project topic-main-guidance render` from the packaged `.j2` template asset. This subcommand may name the marker contract, `<!-- BEGIN isomer-labs-topic-main-guidance v1 -->`, `<!-- END isomer-labs-topic-main-guidance v1 -->`, and fenced block tag `isomer-labs-topic-main-guidance`, but it must not duplicate the full rendered prose.

Use `isomer-cli --print-json project topic-main-guidance inspect --topic <topic>` for read-only posture checks and `isomer-cli --print-json project topic-main-guidance ensure --topic <topic> --yes` for authorized mutation. The rendered block remains topic-independent by design. Do not substitute resolved Research Topic ids, topic statements, Topic Workspace paths, Topic Actor names, Agent Names, runtime file paths, credentials, external repository paths, `manifest_path`, or `pixi_environment` into skill instructions.

## Operational Notes

- Root-level `AGENTS.md` and `CLAUDE.md` are the only standard top-level Isomer-injected worker-facing rule files.

## Guardrails

- DO NOT delete, reset, clean, rewrite history, reinitialize, reclone, pull, or silently repair existing repositories.
- DO NOT create top-level `extern/`, `shared/`, `tasks/`, `runs/`, `views/`, `logs/`, or `tools/` directories inside topic-main as standard Isomer material.
- DO NOT create Agent Workspace worktrees here; that belongs to `isomer-srv-agent-env-setup`.
- DO NOT claim per-agent readiness from a prepared Topic Main Development Repository alone.
