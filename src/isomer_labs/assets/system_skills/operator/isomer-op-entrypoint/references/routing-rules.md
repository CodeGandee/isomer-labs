# Routing Rules

## Workflow

1. Decide whether the user wants route explanation only or wants work performed. Explanation-only requests stay non-mutating.
2. If the user explicitly names a skill or CLI family, prefer that route unless it conflicts with owner boundaries or required readiness.
3. If no route is explicit, classify the task as operator workflow, service support, misc helper, extension research work, or CLI command-family work.
4. Before selecting Topic Team Specialization, require an explicit specialization invocation or prompt or authoritative context that establishes a formal Agent Team target. Generic topic preparation, launch-facing work, readiness gaps, missing summaries, and missing Agent Workspaces are insufficient.
5. Run read-only discovery before ambiguous mutation, especially when Project, Topic, actor, agent, workspace, DeepSci readiness, or Kaoju survey context is unclear.
6. Before optional-extension routing, trust a Project declaration first. For an undeclared extension, delegate receipt-backed explicit-root and live-inventory resolution plus any authorized additive registration to `isomer-op-system-skill-mgr`.
7. Select one route, proceed with that selected route by default, and report blockers instead of presenting a menu when a concrete task can be routed.

If the user's task does not map cleanly to these steps, use your native planning tool to build the smallest safe routing plan from candidate routes, owner boundaries, read-only context evidence, and missing inputs, then execute the plan or stop on a concrete blocker.

## Route Precedence

| Signal | Preferred Route |
| --- | --- |
| User asks what Isomer can do, asks for supported paths, or wants a safe menu. | `isomer-op-welcome`, read-only. |
| User gives a concrete task and asks the agent to handle it. | `isomer-op-entrypoint`, then route and proceed. |
| User names a valid skill directly. | Load that skill unless readiness or ownership makes it unsafe. |
| User names a valid `isomer-cli` command family. | Inspect CLI help and run the smallest safe command. |
| Project bootstrap, validation, cleanup, relocation, context, or runtime setup. | `isomer-op-project-mgr`. |
| System-skill extension detection, reconciliation, installation, status, registration, or repair. | `isomer-op-system-skill-mgr`. |
| Project-local Toolbox authoring, conversion, install, callback insertion, insertion-point discovery, Runtime Params, or effective-state inspection. | `isomer-op-toolbox-mgr`. |
| New or partial Research Topic setup. | `isomer-op-topic-creator`. |
| Existing topic storage, actors, packages, environment verification, reset, or diagnostics. | `isomer-op-topic-mgr`. |
| Work as or on behalf of a Topic Actor or Agent. | `isomer-op-switch-identity`. |
| Explicit specialization invocation, or deploy, specialize, instantiate, materialize, validate, repair, launch, or use a contextually established formal Agent Team. | `isomer-op-topic-team-specialize`; name the Domain Agent Team Template, Topic Agent Team Profile or Bundle, Topic Team Instantiation Packet, Agent Team Instance, or selected formal-team evidence. |
| Topic Service Master lifecycle preparation, launch, inspection, stop, or repair. | `isomer-srv-topic-service-agent-support` through the matching lifecycle subcommand after an operator owner delegates it. |
| Prepared DeepSci research-stage work. | Matching `isomer-deepsci-*` skill or `isomer-deepsci-pipeline`. |
| DeepSci work before accepted bootstrap. | `isomer-deepsci-workspace-mgr` or missing setup owner. |
| Prepared evidence-led survey, source examination, method trial, or comparison work. | Matching `isomer-kaoju-*` skill or `isomer-kaoju-pipeline`. |
| Kaoju work before Topic Workspace, survey, or dataset-registry readiness is established. | `isomer-kaoju-workspace-mgr` or the missing platform owner. |

## Proceed Policy

Proceed when the user supplied a concrete task and the selected route owns it. Do not stop after only listing possible routes unless the user asked for route explanation, multiple alternatives, or a non-mutating status.

Block when required context cannot be resolved safely, when the selected route would bypass owner workflow boundaries, when mutation needs approval not present in the prompt, or when the selected research extension's readiness is missing and no setup route can run without more input.

If the request says only to prepare, create, initialize, start, or repair a Research Topic, route new or partial setup to `isomer-op-topic-creator` and initialized-topic work to `isomer-op-topic-mgr` or the applicable setup owner. Do not select `isomer-op-topic-team-specialize` unless the user explicitly invoked it or formal Agent Team intent is established by the prompt or authoritative context.

## Topic Team Specialization Examples

| Request or Context | Route |
| --- | --- |
| `prepare the topic <topic-name>` with no formal Agent Team target | `isomer-op-topic-creator` for new or partial setup, or `isomer-op-topic-mgr` for initialized-topic work |
| Prepare a topic for manual or human-orchestrated research | `isomer-op-topic-creator` |
| A missing `isomer-topic-summary.md`, Agent Workspace, or readiness check with no formal Agent Team target | The owner of the missing base readiness or setup surface |
| Explicitly invoke `isomer-op-topic-team-specialize` or a named specialization subcommand | `isomer-op-topic-team-specialize` |
| Deploy, specialize, instantiate, materialize, validate, repair, launch, or use a named or contextually selected formal Agent Team | `isomer-op-topic-team-specialize`, carrying the formal-team evidence |

A direct extension-skill invocation preserves explicit user intent. A Project declaration is authoritative routing state; later load failure receives stale-state repair guidance. An undeclared extension routes through `isomer-op-system-skill-mgr`, which may reconcile a complete family when the concrete request authorizes Project bookkeeping or return installation, compatibility, or refresh advice.

## Boundary Rules

Normal user-facing requests route to operator owner skills before service delegation. Service skills are only bounded support unless explicitly invoked.

Houmao-backed work stays Isomer-first. Use `isomer-cli project integrations houmao ...` and returned skill-context paths before following Houmao-owned procedures; do not make ordinary users install or invoke Houmao system skills directly for standard Isomer workflows.

Misc helper skills are explicit helper routes. `isomer-misc-tool-packs` can resolve a named toolset contract only when explicitly requested as a helper, but package mutation for a Topic Workspace remains owned by topic or environment setup workflows.

Project-local Toolbox requests route to `isomer-op-toolbox-mgr`. Do not treat Toolbox callback management, insertion points, or Runtime Params as installable toolset requests.

Provider-specific project roots, user-home roots, plugin roots, and discovery layouts are not entrypoint rules. The system-skill manager obtains roots and live inventory from the current host and passes only explicit inputs to `isomer-cli`.

Retired compatibility skills are not active routes. Do not invoke `isomer-op-topic-workspace-mgr`, `isomer-op-topic-prepare`, `isomer-op-manual-research-session`, `isomer-op-houmao-interop`, or old `isomer-admin-*` names.
