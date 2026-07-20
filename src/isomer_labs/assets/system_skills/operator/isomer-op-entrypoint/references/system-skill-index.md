---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# System Skill Index

## Workflow

1. Match the user's task to one core pack area: operator, service, or shared support. Use [extension-skill-index.md](extension-skill-index.md) for DeepSci and other domain-extension work.
2. Prefer the active parent-scoped operator route for user-facing Project, Topic, actor, agent, Toolbox, team, and routing tasks.
3. Treat service members as delegated protected routes from owner workflows unless the user's task explicitly requires advanced support.
4. Treat shared members as explicit helper routes, not default owner workflows.
5. Return the selected parent-scoped route, public invocation shape, owner boundary, and any prerequisite context needed before proceeding.

If the user's task does not map cleanly to these steps, use your native planning tool to build a skill-selection plan from the active system skills, the user's task, and owner-boundary constraints, then execute the plan or report the missing decision.

## Operator Routes

| Intent | Parent-Scoped Route | Public Invocation |
| --- | --- | --- |
| Read-only welcome, supported paths, first-run option menu, or route recommendations. | `$isomer-op-welcome` | Invoke `$isomer-op-welcome` directly, or use retained entrypoint help and welcome-style commands for compatibility delegation. |
| Project init, validation, doctor diagnostics, cleanup, content-root relocation, topic listing, context, runtime readiness, or Project-level routing. | `isomer-op-entrypoint->project` | `$isomer-op-entrypoint use project to <task>`. |
| System-skill extension detection, reconciliation, installation, upgrade, status, registration, compatibility diagnosis, or repair. | `isomer-op-entrypoint->system-skills` | `$isomer-op-entrypoint use system-skills to <task>`. |
| Project Web GUI lifecycle, GUI Backend launch or status, cache-mode debugging, GUI refresh, recent-errors inspection, backend API reference, or GUI troubleshooting. | `isomer-op-entrypoint->gui` | `$isomer-op-entrypoint use gui to <task>`. |
| Blank or partial Research Topic setup, manual-research-ready Topic Workspace, topic intent, Topic Actor preparation, or final readiness summary. | `isomer-op-entrypoint->topic-create` | `$isomer-op-entrypoint use topic-create to <task>`. |
| Initialized Research Topic storage, Topic Actors, actor workspaces, packages, environment verification, reset checkpoints, branch helpers, or diagnostics. | `isomer-op-entrypoint->topic-manage` | `$isomer-op-entrypoint use topic-manage to <task>`. |
| Switch the Project Operator to act as or on behalf of a selected Topic Actor or Agent workspace cwd. | `isomer-op-entrypoint->identity` | `$isomer-op-entrypoint use identity to <task>`. |
| Project-local Toolbox creation, conversion, install, inspection, update, disable, uninstall, callback insertion, insertion-point discovery, Runtime Params, or effective-state diagnostics. | `isomer-op-entrypoint->toolbox` | `$isomer-op-entrypoint use toolbox to <task>`. |
| Explicit Topic Team Specialization, or adaptation, deployment, use, static validation, approval, materialization, repair, or launch of a formal Agent Team identified by the prompt or authoritative context. Generic topic preparation and launch-facing work are excluded. | `isomer-op-entrypoint->topic-team` | `$isomer-op-entrypoint use topic-team to <task>`, naming the formal-team evidence. |
| Informed-user dispatch from a concrete task to a protected route, public extension, or CLI family. | `isomer-op-entrypoint` | `$isomer-op-entrypoint` with the concrete task. |

The public `$isomer-op-welcome` sibling owns read-only orientation. The public `isomer-op-entrypoint` skill owns route-and-proceed dispatch.

## Research Recording Routes

| Intent | Parent-Scoped Route | Boundary |
| --- | --- | --- |
| Accept, verify, resume, or explicitly repair all material files from one Topic Actor or Agent operation set. | `isomer-op-entrypoint->operation-sets` | Exhaustive staging reconciliation and receipt workflow; durable record and Research Idea semantics remain owned by existing canonical services. |
| Create or change canonical Research Ideas, facets, exact realizations, generations, decisions, transitions, or Idea Lineage. | `isomer-op-entrypoint->research-ideas` | Canonical concept-state owner; does not make worker staging durable by itself. |

Topic Team Specialization requires an explicit skill or specialization-route invocation, or a formal Agent Team target established by the prompt or authoritative Project context. A Research Topic, Topic Workspace, readiness gap, missing summary, missing Agent Workspace, or generic launch-facing request alone does not satisfy this route.

## Protected Service Routes

| Intent | Parent-Scoped Route | Boundary |
| --- | --- | --- |
| Topic Workspace environment setup, topic-main readiness, external repos, projections, and verification materialization. | `isomer-op-entrypoint->topic-env` | Delegated by Topic Creator, Topic Manager, or Topic Team Specialization after manifest-backed topic refs exist. |
| Agent Workspace worktree creation and cwd proof. | `isomer-op-entrypoint->agent-env` | Delegated by Topic Team Specialization or Topic Manager after topic-main predecessor evidence and authoritative Agent Names exist. |
| Houmao loop, adapter, mailbox, gateway, launch material, and runtime support. | `isomer-op-entrypoint->houmao` | Bounded internal provider support through Isomer CLI skill-context or an owning operator route. |
| Package repository resolution. | `isomer-op-entrypoint->package-repo` | Bounded service support for package or repo resolution. |
| Topic service agent support, including explicit Topic Service Master prepare, launch, inspect, stop, and repair lifecycle routes. | `isomer-op-entrypoint->topic-service` | Bounded service-team support, not a normal first-click owner route. Houmao remains an internal integration provider. |

## Protected Shared Routes

| Intent | Parent-Scoped Route | Boundary |
| --- | --- | --- |
| Bounded command-run planning for risky or heavy operations. | `isomer-op-entrypoint->bounded-run` | Helper guidance consulted by setup or verification workflows. |
| NVIDIA tooling guidance. | `isomer-op-entrypoint->nvidia` | Explicit helper guidance when GPU tooling is relevant. |
| Package-specific routing rules. | `isomer-op-entrypoint->package-specifics` | Helper guidance before generic package handling. |
| Named installable toolset contract such as paper-writing, paper-figures-python, paper2ppt, cuda-build, torch-gpu, or topic-python-starter. | `isomer-op-entrypoint->tool-packs` | Explicitly requested helper only; not automatic package mutation. |

Project-local Toolbox callback, insertion-point, Runtime Param, and registration management routes to `isomer-op-entrypoint->toolbox`; `isomer-op-entrypoint->tool-packs` remains an explicitly requested helper only.

Do not route active work to retired operator compatibility skills or old admin names.
