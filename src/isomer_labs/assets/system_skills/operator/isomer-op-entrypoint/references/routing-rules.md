# Routing Rules

## Workflow

1. Decide whether the user wants route explanation only or wants work performed. Explanation-only requests stay non-mutating.
2. If the user explicitly names a skill or CLI family, prefer that route unless it conflicts with owner boundaries or required readiness.
3. If no route is explicit, classify the task as operator workflow, service support, misc helper, extension research work, or CLI command-family work.
4. Run read-only discovery before ambiguous mutation, especially when Project, Topic, actor, agent, workspace, or DeepSci readiness is unclear.
5. Select one route, proceed with that selected route by default, and report blockers instead of presenting a menu when a concrete task can be routed.

If the user's task does not map cleanly to these steps, use your native planning tool to build the smallest safe routing plan from candidate routes, owner boundaries, read-only context evidence, and missing inputs, then execute the plan or stop on a concrete blocker.

## Route Precedence

| Signal | Preferred Route |
| --- | --- |
| User asks what Isomer can do, asks for supported paths, or wants a safe menu. | `isomer-op-welcome`, read-only. |
| User gives a concrete task and asks the agent to handle it. | `isomer-op-entrypoint`, then route and proceed. |
| User names a valid skill directly. | Load that skill unless readiness or ownership makes it unsafe. |
| User names a valid `isomer-cli` command family. | Inspect CLI help and run the smallest safe command. |
| Project bootstrap, validation, cleanup, relocation, context, or runtime setup. | `isomer-op-project-mgr`. |
| Project-local Toolbox authoring, conversion, install, callback insertion, insertion-point discovery, Runtime Params, or effective-state inspection. | `isomer-op-toolbox-mgr`. |
| New or partial Research Topic setup. | `isomer-op-topic-creator`. |
| Existing topic storage, actors, packages, environment verification, reset, or diagnostics. | `isomer-op-topic-mgr`. |
| Work as or on behalf of a Topic Actor or Agent. | `isomer-op-switch-identity`. |
| Domain Agent Team Template specialization. | `isomer-op-topic-team-specialize`. |
| Topic Service Master lifecycle preparation, launch, inspection, stop, or repair. | `isomer-srv-topic-service-agent-support` through the matching lifecycle subcommand after an operator owner delegates it. |
| Prepared DeepSci research-stage work. | Matching `isomer-deepsci-*` skill or `isomer-deepsci-pipeline`. |
| DeepSci work before accepted bootstrap. | `isomer-deepsci-workspace-mgr` or missing setup owner. |

## Proceed Policy

Proceed when the user supplied a concrete task and the selected route owns it. Do not stop after only listing possible routes unless the user asked for route explanation, multiple alternatives, or a non-mutating status.

Block when required context cannot be resolved safely, when the selected route would bypass owner workflow boundaries, when mutation needs approval not present in the prompt, or when DeepSci readiness is missing and no setup route can run without more input.

## Boundary Rules

Normal user-facing requests route to operator owner skills before service delegation. Service skills are only bounded support unless explicitly invoked.

Houmao-backed work stays Isomer-first. Use `isomer-cli project integrations houmao ...` and returned skill-context paths before following Houmao-owned procedures; do not make ordinary users install or invoke Houmao system skills directly for standard Isomer workflows.

Misc helper skills are explicit helper routes. `isomer-misc-tool-packs` can resolve a named toolset contract only when explicitly requested as a helper, but package mutation for a Topic Workspace remains owned by topic or environment setup workflows.

Project-local Toolbox requests route to `isomer-op-toolbox-mgr`. Do not treat Toolbox callback management, insertion points, or Runtime Params as installable toolset requests.

Retired compatibility skills are not active routes. Do not invoke `isomer-op-topic-workspace-mgr`, `isomer-op-topic-prepare`, `isomer-op-manual-research-session`, `isomer-op-houmao-interop`, or old `isomer-admin-*` names.
