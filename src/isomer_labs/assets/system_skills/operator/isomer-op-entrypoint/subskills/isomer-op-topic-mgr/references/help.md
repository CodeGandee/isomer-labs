---
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

# Help

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Print a concise description: `isomer-op-topic-mgr` manages initialized-topic storage, Topic Actors, topic agent team topology, environment mutation, environment verification, reset checkpoints, and diagnostics after `isomer-op-topic-creator` has initialized a Research Topic.
2. Explain that invoking the skill without a prompt defaults to `status`, while explicit help prints this usage surface.
3. Print the available public subcommands as a three-column table with `Subcommand`, `Purpose`, and `Produces` columns.
4. Name the required inputs: Project Manifest context, initialized Research Topic, Topic Workspace, optional Topic Actor names, optional packet/profile material, requested Agent Name mapping, package mutation request, or environment verification target.
5. State the output contract: Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.
6. State the key guardrails: no blank-state topic initialization, no directory-scanning selection, no silent Git repair, no Git-based reset behavior, no cross-topic refs, no local virtualenv or ambient package mutation, no Agent Instance creation, no Houmao launch, no Execution Adapter operation, and no production DeepSci research bootstrap ownership.
7. Explain that explicit Source Topic Workspace root tracking, root-ignore, local root commit, sanitized Topic Publication Copy, remote binding, submodule publication, or publication synchronization requests delegate to `isomer-op-entrypoint->topic-git` with selected context preserved.

If the user's task does not map cleanly to these steps, use your native planning tool to decide which usage details to print, then execute the plan.

## Public Subcommands

| Subcommand | Purpose | Produces |
| --- | --- | --- |
| `status` | Summarize initialized-topic storage, actors, team topology, environment evidence, blockers, and next action. | Consumer-neutral report with paths, branches, tmp posture, `isomer-managed/` regimes, package evidence, verification evidence, blockers, and next action. |
| `doctor` | Diagnose stale or unsafe initialized-topic topology, storage, actor, team, environment, and retired-skill routing evidence. | Diagnostic report with warnings, blockers, owner command, and repair route. |
| `storage-resolve` | Resolve Project, Research Topic, Topic Workspace, and semantic paths through Project Manifest-backed context. | Topic Workspace path, semantic paths, path sources, packet/profile candidates, blockers. |
| `storage-inspect-main` | Inspect or validate the resolved `topic.repos.main` path, `topic.repos.main.tmp`, and tracked Isomer namespace. | `topic_main_repo_path`, `local_tmp_path_status`, `isomer_managed_path_status`, base branch, repo readiness, blockers. |
| `storage-validate` | Validate storage bindings, tmp posture, projection roots, custom labels, and unsafe path blockers. | `semantic_paths`, storage profile evidence, validation status, blockers, next action. |
| `storage-register-repo` | Register or inspect non-main `topic.repos.*` repositories through semantic labels and `storage_profile`. | Registered label, path source, storage profile, command evidence, blockers. |
| `actors-manage` | List, show, register, update, archive, materialize, repair, or diagnose Topic Actors and Topic Actor Workspaces. | Topic Actor bindings, `topic.actors.workspace` paths, branch plan, audit refs, blockers. |
| `actors-materialize` | Create, reuse, or repair selected Topic Actor Workspace worktrees and actor support labels. | Ready or created actor workspaces, support labels, branch posture, blockers. |
| `actors-diagnose` | Diagnose Topic Actor bindings, cwd labels, branches, support labels, runtime audit refs, and repair routes. | Actor diagnostics, readiness signals, blockers, repair route. |
| `team-plan` | Normalize Agent Names and map active role bindings to resolved `agent.workspace` paths and branches. | Agent Name map, semantic paths, derived compatibility refs, `per-agent/<agent-name>/main` branch plan. |
| `team-materialize-workspaces` | Inspect, validate, or manually create per-agent Git worktrees and ignored `agent.*` support paths. | Ready or created Agent Workspace worktrees, tmp posture, `isomer-managed/` regime status, skipped entries, blockers. |
| `team-write-boundaries` | Write advisory Workspace Boundary and Peer Read Access notes. | Boundary material paths, ownership notes, branch rules, generated-link notes. |
| `team-create-branch` | Create a future per-agent branch under the owning Agent Name prefix. | `per-agent/<agent-name>/<branch-name>` branch result, base ref, blockers. |
| `team-validate-workspaces` | Validate Git topology, local tmp posture, `isomer-managed/` layout, generated links, and packet/profile workspace refs. | `validation_status`, ready entries, tmp, cross-topic, layout, or Git blockers. |
| `env-install-packages` | Infer, install, and verify packages in the selected Topic Workspace Pixi environment from a prompt or description file. | Package install plan, Pixi commands, verification evidence, changed files, and blockers. |
| `env-update-packages` | Infer, update, constrain, or downgrade packages in the selected Topic Workspace Pixi environment. | Package update plan, Pixi commands, verification evidence, changed files, and blockers. |
| `env-remove-packages` | Infer package removal intent, remove packages when safe, and verify relevant checks. | Package removal plan, Pixi commands, post-removal verification, repair guidance, blockers. |
| `env-verify-topic` | Verify Topic Workspace environment readiness or route full gate-driven verification to `isomer-srv-topic-env-setup`. | Topic env verification evidence, service handoff, skipped checks, blockers. |
| `env-verify-actors` | Verify selected Topic Actor cwd gates and actor support labels. | Per-actor readiness, commands run, support-label evidence, blockers. |
| `env-verify-agents` | Route formal Agent Workspace cwd proof to `isomer-srv-agent-env-setup`. | Agent env service evidence, Agent Workspace readiness by Agent Name, blockers. |
| `reset-plan` | Create a read-only structured reset plan for an initialized Topic Workspace checkpoint. | Reset plan id, action summary, generated review path, and blockers. |
| `reset-inspect` | List and inspect reset checkpoints, reset plans, blockers, and review views. | Checkpoint or plan status, preserved setup evidence, generated review paths, and stale-plan guidance. |
| `reset-apply` | Apply an approved reset plan with explicit confirmation. | Reset outcome id, applied/skipped/failed action counts, diagnostics, and generated review path. |
| `help` | Print this usage information. | Public subcommand table, required inputs, outputs, guardrails. |

## Boundary Notes

`isomer-op-topic-creator` owns topic initialization. If no initialized Research Topic and Topic Workspace can be resolved, route to the creator rather than deriving topic ids, registering topics, or writing topic intent from this skill.

`isomer-srv-topic-env-setup` owns full gate-driven topic environment setup, Topic Main Development Repository setup, external repository requirement planning, post-verification registration, and external repo projection materialization. The acting user or agent runs prompt-sensitive repository commands outside Isomer. Ad hoc package install, update, remove, and package verification requests enter through `isomer-op-topic-mgr env-*` commands.

`isomer-srv-agent-env-setup` owns formal Agent Workspace cwd proof. Use `env-verify-agents` when a caller asks the topic manager for that proof, and report returned service evidence without claiming runtime launch readiness.

`isomer-deepsci-workspace-mgr` owns production DeepSci research placeholder binding and storage bootstrap. This topic manager does not create research records, production DeepSci bootstrap outputs, accepted artifact instructions, Agent Instances, Houmao launch material, or Execution Adapter state.

Topic Workspace reset operations are initialized-topic management operations owned here: use `project topic-reset plan`, `project topic-reset show`, `project topic-reset show-plan`, and `project topic-reset apply` through structured records and Workspace Runtime state, not Git state.

Optional Topic Workspace Git work is a separate owner boundary. Delegate explicit local root history or sanitized remote publication requests to `isomer-op-entrypoint->topic-git`. Do not initialize either layer during ordinary storage, actor, team, environment, reset, or diagnostic work, and do not wrap Git mutation in Isomer CLI.
