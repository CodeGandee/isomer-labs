---
name: isomer-op-entrypoint
description: Use when a Project Operator needs an informed-user entrypoint to route a concrete prompt, file, topic task, actor or agent task, extension-skill request, or Isomer CLI need to the correct Isomer system skill or CLI surface and proceed.
---

# Isomer Operator Entrypoint

## Overview

Use this skill as the informed-user route-and-proceed dispatcher for Isomer system skills and Isomer CLI functionality. It selects the smallest correct owner skill, extension skill, or CLI family for the user's concrete task, then proceeds with that route unless the user only asked for help or route explanation.

## When to Use

Use this skill when the user already knows Isomer enough to provide a task, prompt, file, Research Topic, Topic Actor, Agent, DeepSci research request, or CLI-shaped operation, but wants the Project Operator to decide which Isomer surface to use next. Do not use this skill as the first-run welcome menu; use `isomer-op-welcome` for read-only orientation, visible usage paths, and safe owner-skill recommendations without execution.

Do not use this skill to bypass owner workflows. Project lifecycle work belongs to `isomer-op-project-mgr`, topic creation belongs to `isomer-op-topic-creator`, initialized-topic management belongs to `isomer-op-topic-mgr`, identity posture belongs to `isomer-op-switch-identity`, Topic Team Specialization belongs to `isomer-op-topic-team-specialize`, DeepSci bootstrap belongs to `isomer-deepsci-workspace-mgr`, and research-stage work belongs to the selected `isomer-deepsci-*` skill.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Parse the task input**. Identify whether the user supplied a plain prompt, file path, Project root, Research Topic, Topic Workspace, Topic Actor, Agent, Domain Agent Team Template, DeepSci stage, CLI action, or explicit skill name. See [references/input-surfaces.md](references/input-surfaces.md).
2. **Run safe context discovery when useful**. Prefer read-only evidence such as `isomer-cli project self queries`, `isomer-cli project self show`, `isomer-cli project validate`, `isomer-cli project doctor`, `isomer-cli project topics list`, `isomer-cli project context show`, or Workspace Path Resolution commands before ambiguous mutation. See [references/cli-index.md](references/cli-index.md).
3. **Classify exactly one route**. Use [references/routing-rules.md](references/routing-rules.md), [references/system-skill-index.md](references/system-skill-index.md), and [references/extension-skill-index.md](references/extension-skill-index.md) to select one owner skill, extension skill, or CLI family.
4. **Check owner boundaries**. Confirm the selected route owns the requested work, service skills are only bounded support unless explicitly invoked, misc helpers are explicit helper routes, and retired operator compatibility skills are not active routes.
5. **Proceed with the selected route**. Unless the user asked only for route explanation, load the selected owner skill or reference, follow its workflow, or run the selected CLI command family with the required read-only or mutation posture. Do not stop after only listing candidate routes.
6. **Report the entrypoint result** using **Essential Output** by default and **Complete Output** when requested.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step routing plan from this skill, the route references, current user request, available Project context, owner boundaries, and blockers, then execute the plan or stop on a concrete blocker.

## Reference Pages

| Reference | Use For |
| --- | --- |
| [references/input-surfaces.md](references/input-surfaces.md) | Resolve prompts, files, Project roots, topics, actors, agents, templates, and explicit skill or CLI requests. |
| [references/routing-rules.md](references/routing-rules.md) | Select route kind, handle read-only explanation, decide when to proceed, and preserve safety boundaries. |
| [references/system-skill-index.md](references/system-skill-index.md) | Route operator, service, and misc system skill requests. |
| [references/extension-skill-index.md](references/extension-skill-index.md) | Route DeepSci extension skill requests and readiness blockers. |
| [references/cli-index.md](references/cli-index.md) | Route Isomer CLI command-family requests and safe discovery commands. |

## Output Contract

Default to **Essential Output** in chat. Print **Complete Output** only when the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output.

### Essential Output

Report:

- `status`: routed, executed, explained, blocked, or unchanged.
- `interpreted_goal`: the normalized task, prompt, file, topic, actor, agent, extension, or CLI request.
- `selected_route`: route kind plus selected skill or CLI family.
- `context_used`: prompt evidence, file evidence, Project context, Research Topic, Topic Actor, Agent, or read-only command evidence used to route.
- `what_changed`: important mutation, generated output, inspection result, or `none`.
- `blockers`: missing context, unsafe mutation, unresolved topic or identity, missing readiness, unsupported CLI action, or owner-boundary conflict.
- `next_action`: continue through the selected route, provide missing input, approve mutation, inspect readiness, or stop.

### Complete Output

When requested, include:

- `route_candidates`: plausible route candidates and why they were accepted or rejected.
- `routing_rationale`: owner-boundary, extension-readiness, CLI-family, and service-support reasoning.
- `commands_run`: read-only and mutation commands, with command posture.
- `selected_context`: Project root, Research Topic, Topic Workspace, Topic Actor, Agent, Domain Agent Team Template, DeepSci skill, or CLI family.
- `extension_skill_readiness`: DeepSci workspace, topic, actor, agent, latest-context, placeholder-binding, and worker-output readiness checks when relevant.
- `service_delegation_notes`: bounded support delegation and why the service skill was not treated as the normal first-click owner route.
- `retired_route_exclusions`: retired or stale skill names excluded from active routing when relevant.

## Guardrails

Prefer read-only context discovery before ambiguous mutation. Proceed only when the task implies action and the selected owner workflow or CLI command family owns that action.

Keep `isomer-op-welcome` read-only. Use it for welcome menus and safe recommendations; use `isomer-op-entrypoint` for informed-user routing and execution.

Do not make this skill the authority for lower-level mutation. It routes to owner skills and CLI families, then follows their workflows and guardrails.

Service skills such as `isomer-srv-topic-env-setup`, `isomer-srv-agent-env-setup`, `isomer-srv-houmao-interop`, `isomer-srv-resolve-pkg-repo`, and `isomer-srv-topic-service-agent-support` are bounded support routes. Normal user-facing requests should route through the owning operator workflow before service delegation unless the user explicitly invokes a service skill.

Mention `isomer-misc-tool-packs` only when explicitly requested as a named helper route. Package install, update, or removal requests for a Topic Workspace belong to `isomer-op-topic-mgr` or the relevant environment setup workflow.

Do not present retired or stale operator routes as active invokable skills. This includes `isomer-op-topic-workspace-mgr`, `isomer-op-topic-prepare`, `isomer-op-manual-research-session`, `isomer-op-houmao-interop`, and old `isomer-admin-*` compatibility names.

Do not use repo-local Pixi wrapper command guidance for Isomer CLI in operator skills. Installed operators should invoke global `isomer-cli` directly.

## Common Mistakes

- Listing several possible routes and stopping even though the user gave a concrete task. Select the best route, proceed, or report the blocker.
- Treating service skills as normal first-click owner routes. Route through the owning operator workflow unless the user explicitly invoked the service skill.
- Starting an ordinary DeepSci research-stage skill before Topic Workspace, actor or agent workspace, and DeepSci bootstrap readiness are proven or routed for setup.
- Repeating the full CLI help text inside this skill. Name the command family and inspect CLI help or owner skill guidance when details are needed.
- Treating generated links, worker-local files, chat memory, or old rendered Markdown as durable research truth before the selected DeepSci skill's latest-context and recording rules accept them.
