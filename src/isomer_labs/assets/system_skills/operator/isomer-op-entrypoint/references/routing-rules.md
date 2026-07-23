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

# Routing Rules

## Workflow

1. Decide whether the user wants route explanation only or wants work performed. Explanation-only requests stay non-mutating.
2. If the user explicitly names a skill or CLI family, prefer that route unless it conflicts with owner boundaries or required readiness.
3. If no route is explicit, classify the task as operator workflow, service support, misc helper, extension research work, or CLI command-family work.
4. Before selecting Topic Team Specialization, require an explicit specialization invocation or prompt or authoritative context that establishes a formal Agent Team target. Generic topic preparation, launch-facing work, readiness gaps, missing summaries, and missing Agent Workspaces are insufficient.
5. Classify operation scope as `project`, `topic`, `topic-actor`, or `agent`; convert prompt targets to explicit selectors; and run `project self location` plus `project self check --scope <scope>` before context-sensitive mutation.
6. Stop on unresolved or conflicting target evidence. An explicit cross-topic target may be an `explicit_override`, while a manifest default is a visible fallback only. Project scope never inherits topic scope merely because a default exists.
7. Pin the accepted topic and worker selectors for every applicable downstream command. Rerun alignment after an intentional scope change, and require an explicit worker or active switch posture rather than a sole manifest actor for worker-scoped work.
8. Before optional-extension routing, treat a Project declaration as authoritative routing intent. Delegate current v5 receipt, explicit-root, and limited live-inventory resolution plus any authorized additive registration to `isomer-op-entrypoint->system-skills`. Register only a verified current-v5 complete public-pair pack.
9. Select one route as the initial owner route and let its owner preflight target prerequisites before mutation.
10. If the target is ready, proceed through the selected route; if a known producer can satisfy a missing input, return paused prerequisite recovery rather than a terminal blocker.
11. Present the recovery choices in `prerequisite-recovery.md` unless the user already gave explicit target-scoped run-to authorization.
12. During authorized run-to, coordinate the dependency closure across owners and stop after the original target or at a nondelegable boundary.

If the user's task does not map cleanly to these steps, use your native planning tool to build the smallest safe routing plan from candidate routes, owner boundaries, read-only context evidence, and missing inputs, then execute the plan or stop on a concrete blocker.

## Route Precedence

| Signal | Preferred Route |
| --- | --- |
| User asks what Isomer can do, asks for supported paths, or wants a safe menu. | Delegate to `$isomer-op-welcome`, read-only. |
| User gives a concrete task and asks the agent to handle it. | `isomer-op-entrypoint`, then route and proceed. |
| User names a valid skill directly. | Load that skill unless readiness or ownership makes it unsafe. |
| User names a valid `isomer-cli` command family. | Inspect CLI help and run the smallest safe command. |
| A Topic Actor or Agent operation set needs durable closeout, receipt resume, verification, or explicit legacy repair. | `isomer-op-entrypoint->operation-sets` or the explicit `isomer-cli ext research operation-sets ...` family. |
| Project bootstrap, validation, cleanup, relocation, context, or runtime setup. | `isomer-op-entrypoint->project`. |
| System-skill extension detection, reconciliation, installation, upgrade, status, registration, or repair. | `isomer-op-entrypoint->system-skills`. |
| Project-local Toolbox authoring, conversion, install, callback insertion, insertion-point discovery, Runtime Params, or effective-state inspection. | `isomer-op-entrypoint->toolbox`. |
| New or partial Research Topic setup. | `isomer-op-entrypoint->topic-create`. |
| Existing topic storage, actors, packages, environment verification, reset, or diagnostics. | `isomer-op-entrypoint->topic-manage`. |
| Explicit Source Topic Workspace root Git status, local initialization, local ignore or commit planning, or exact local root commit. | `isomer-op-entrypoint->topic-git->local()`. |
| Explicit sanitized Topic Publication Copy preparation, privacy planning, publication status, reconstruction, synchronization, or remote push. | `isomer-op-entrypoint->topic-git->publish()`. |
| Ambiguous request to track or version a Topic Workspace without local-versus-publication intent. | `isomer-op-entrypoint->topic-git->status()`, read-only before mutation. |
| Work as or on behalf of a Topic Actor or Agent. | `isomer-op-entrypoint->identity`. |
| Explicit specialization invocation, or deploy, specialize, instantiate, materialize, validate, repair, launch, or use a contextually established formal Agent Team. | `isomer-op-entrypoint->topic-team`; name the Domain Agent Team Template, Topic Agent Team Profile or Bundle, Topic Team Instantiation Packet, Agent Team Instance, or selected formal-team evidence. |
| Topic Service Master lifecycle preparation, launch, inspection, stop, or repair. | `isomer-op-entrypoint->topic-service` through the matching lifecycle subcommand after an operator owner delegates it. |
| Prepared DeepSci research-stage work. | `isomer-ext-deepsci-entrypoint` or its matching protected member designator. |
| DeepSci work before accepted bootstrap. | `isomer-ext-deepsci-entrypoint->workspace` or the missing platform owner. |
| Prepared evidence-led survey, source examination, method trial, or comparison work. | `isomer-ext-kaoju-entrypoint` or its matching protected member designator. |
| Kaoju work before Topic Workspace, survey, or dataset-registry readiness is established. | `isomer-ext-kaoju-entrypoint->workspace` or the missing platform owner. |

## Proceed Policy

Proceed when the user supplied a concrete task, the selected route owns it, and its required inputs are ready. Do not stop after only listing possible routes unless the user asked for route explanation, multiple alternatives, or a non-mutating status.

When an ordinary concrete task has missing or stale inputs with known in-scope producers, pause before invoking those producers and offer run-to-target, next-prerequisite-only, alternate-route, and stop choices. `Do <task>` alone does not authorize prerequisite mutation. Explicit `run to <task>`, `automate the prerequisites and then do <task>`, or an equivalent choice authorizes only the named target's transitive prerequisite closure and the target itself.

During run-to, use the native planning tool, preserve each owner's authority and separate durable execution records, refresh state after bounded results, and stop after the target. Pause at human Gates, material ambiguity, destructive or irreversible action, credentials or restricted data, material license decisions, unexpected resource authorization, public exposure, publication or submission, and repeated recovery without new accepted state.

When a typed command returns not-found, wrong-scope, or context-conflict diagnostics, compare its selected-context metadata with the pinned target. Correct selectors, rerun alignment, or route to the owning readiness workflow. Do not search sibling Topic Workspaces, select another manifest default, add an alternate target, or copy files into a Topic Actor Workspace, Agent Workspace, Topic Main, or arbitrary directory unless the user explicitly requests a separate unmanaged copy operation.

Use `blocked` when required context cannot be resolved safely, the selected route would bypass owner workflow boundaries, mutation needs approval not present in the prompt, or no available authorized owner can perform the external state change needed by the target. Use `paused` rather than `blocked` when an available in-scope owner can produce or repair the missing state.

If the request says only to prepare, create, initialize, start, or repair a Research Topic, route new or partial setup to `isomer-op-entrypoint->topic-create` and initialized-topic work to `isomer-op-entrypoint->topic-manage` or the applicable setup owner. Do not select `isomer-op-entrypoint->topic-team` unless the user explicitly invoked it or formal Agent Team intent is established by the prompt or authoritative context.

## Topic Team Specialization Examples

| Request or Context | Route |
| --- | --- |
| `prepare the topic <topic-name>` with no formal Agent Team target | `isomer-op-entrypoint->topic-create` for new or partial setup, or `isomer-op-entrypoint->topic-manage` for initialized-topic work |
| Prepare a topic for manual or human-orchestrated research | `isomer-op-entrypoint->topic-create` |
| A missing `isomer-topic-summary.md`, Agent Workspace, or readiness check with no formal Agent Team target | The owner of the missing base readiness or setup surface |
| Explicitly invoke the public `topic-team` route or a named specialization subcommand | `isomer-op-entrypoint->topic-team` |
| Deploy, specialize, instantiate, materialize, validate, repair, launch, or use a named or contextually selected formal Agent Team | `isomer-op-entrypoint->topic-team`, carrying the formal-team evidence |

A direct public extension invocation preserves explicit user intent. A Project declaration is authoritative routing state; later load failure receives stale-state repair guidance. Current-host readiness routes through `isomer-op-entrypoint->system-skills`, which may reconcile a verified current-v5 complete public-pair pack when the concrete request authorizes Project bookkeeping or return migration, installation, compatibility, or refresh advice.

## Boundary Rules

Normal user-facing requests route to operator owner skills before service delegation. Service skills are only bounded support unless explicitly invoked.

Houmao-backed work stays Isomer-first. Use `isomer-cli project integrations houmao ...` and returned skill-context paths before following Houmao-owned procedures; do not make ordinary users install or invoke Houmao system skills directly for standard Isomer workflows.

Protected shared members are explicit helper routes. `isomer-op-entrypoint->tool-packs` can resolve a named toolset contract only when explicitly requested as a helper, but package mutation for a Topic Workspace remains owned by topic or environment setup workflows.

Project-local Toolbox requests route to `isomer-op-entrypoint->toolbox`. Do not treat Toolbox callback management, insertion points, or Runtime Params as installable toolset requests.

Provider-specific project roots, user-home roots, plugin roots, and discovery layouts are not entrypoint rules. The system-skill manager obtains roots and live inventory from the current host and passes only explicit inputs to `isomer-cli`.

Retired compatibility skills are not active routes. Do not invoke `isomer-op-topic-workspace-mgr`, `isomer-op-topic-prepare`, `isomer-op-manual-research-session`, `isomer-op-houmao-interop`, or old `isomer-admin-*` names.
