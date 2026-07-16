---
name: isomer-op-entrypoint
description: Use when a Project Operator needs an informed-user entrypoint to route a concrete prompt, file, topic task, actor or agent task, extension-skill request, or Isomer CLI need to the correct Isomer system skill or CLI surface and proceed.
---

# Isomer Operator Entrypoint

## Overview

Use this skill as the informed-user route-and-proceed dispatcher for Isomer system skills and Isomer CLI functionality. It selects the smallest correct owner skill, extension skill, or CLI family for the user's concrete task, then proceeds with that route unless the user only asked for help or route explanation.

## When to Use

Use this skill when the user already knows Isomer enough to provide a task, prompt, file, Research Topic, Topic Actor, Agent, DeepSci research request, Kaoju survey request, or CLI-shaped operation, but wants the Project Operator to decide which Isomer surface to use next. Do not use this skill as the first-run welcome menu; use `isomer-op-welcome` for read-only orientation, visible usage paths, and safe owner-skill recommendations without execution.

Do not use this skill to bypass owner workflows. Project lifecycle work belongs to `isomer-op-project-mgr`, system-skill extension detection, reconciliation, installation, status, and repair belong to `isomer-op-system-skill-mgr`, Project Web GUI lifecycle and backend API reference belongs to `isomer-op-gui-mgr`, topic creation belongs to `isomer-op-topic-creator`, initialized-topic management belongs to `isomer-op-topic-mgr`, identity posture belongs to `isomer-op-switch-identity`, project-local Toolbox management belongs to `isomer-op-toolbox-mgr`, Topic Team Specialization belongs to `isomer-op-topic-team-specialize`, DeepSci bootstrap belongs to `isomer-deepsci-workspace-mgr`, Kaoju readiness belongs to `isomer-kaoju-workspace-mgr`, and research work belongs to the selected `isomer-deepsci-*` or `isomer-kaoju-*` skill.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Parse the task input**. Identify whether the user supplied a plain prompt, file path, Project root, Research Topic, Topic Workspace, Topic Actor, Agent, Domain Agent Team Template, DeepSci stage, Kaoju survey intent, CLI action, or explicit skill name. See [references/input-surfaces.md](references/input-surfaces.md).
2. **Run safe context discovery when useful**. Prefer read-only evidence such as `isomer-cli project self queries`, `isomer-cli project self show`, `isomer-cli project validate`, `isomer-cli doctor`, `isomer-cli project topics list`, `isomer-cli project context show`, or Workspace Path Resolution commands before ambiguous mutation. See [references/cli-index.md](references/cli-index.md).
3. **Check optional-extension availability**. Before selecting a DeepSci or Kaoju route, trust an existing Project declaration and attempt that route. For an undeclared extension, delegate ordered receipt and live-inventory resolution to `isomer-op-system-skill-mgr detect-extensions` or `reconcile-extensions` when the concrete request authorizes Project bookkeeping. Do not encode provider discovery paths in this entrypoint.
4. **Establish formal Agent Team intent before specialization**. Select `isomer-op-topic-team-specialize` only when the user explicitly invokes that skill or a named specialization route, or when the prompt or authoritative Project context establishes a formal Agent Team target. Name the Domain Agent Team Template, Topic Agent Team Profile or Bundle, Topic Team Instantiation Packet, Agent Team Instance, selected formal-team material, or equivalent evidence used. Generic topic preparation, launch-facing work, readiness gaps, missing summaries, or missing Agent Workspaces do not establish Agent Team intent.
5. **Classify exactly one route**. Use [references/routing-rules.md](references/routing-rules.md), [references/system-skill-index.md](references/system-skill-index.md), and [references/extension-skill-index.md](references/extension-skill-index.md) to select one owner skill, extension skill, or CLI family.
6. **Check owner boundaries**. Confirm the selected route owns the requested work, service skills are only bounded support unless explicitly invoked, misc helpers are explicit helper routes, and retired operator compatibility skills are not active routes.
7. **Preflight target prerequisites**. Before target mutation, let the selected owner resolve its required artifacts, accepted inputs, readiness evidence, and known producer routes. See [references/prerequisite-recovery.md](references/prerequisite-recovery.md).
8. **Route prerequisite recovery**. If a producible prerequisite is missing and run-to is not explicitly authorized, stop before prerequisite mutation, report `paused`, and offer run-to-target, next-prerequisite-only, alternate-route, and stop choices. If run-to is authorized, use the native planning tool to execute the target-scoped dependency closure through its owners and resume the original target. See [references/prerequisite-recovery.md](references/prerequisite-recovery.md).
9. **Proceed with the selected route**. Unless the user asked only for route explanation, load the selected owner skill or reference, follow its workflow, or run the selected CLI command family with the required read-only or mutation posture. Do not stop after only listing candidate routes. During authorized run-to, preserve each owner's separate mutation, Run, checkpoint, Gate, and terminal-report boundaries.
10. **Report the entrypoint result** using **Essential Output** by default and **Complete Output** when requested. Stop run-to after the original target completes or at a nondelegable boundary; do not continue into later recommended work.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step routing plan from this skill, the route references, current user request, available Project context, owner boundaries, and blockers, then execute the plan or stop on a concrete blocker.

## Reference Pages

| Reference | Use For |
| --- | --- |
| [references/input-surfaces.md](references/input-surfaces.md) | Resolve prompts, files, Project roots, topics, actors, agents, templates, and explicit skill or CLI requests. |
| [references/routing-rules.md](references/routing-rules.md) | Select route kind, handle read-only explanation, decide when to proceed, and preserve safety boundaries. |
| [references/prerequisite-recovery.md](references/prerequisite-recovery.md) | Preflight target inputs, present recovery choices, execute authorized run-to traversal, classify paused versus blocked state, and preserve nondelegable boundaries. |
| [references/system-skill-index.md](references/system-skill-index.md) | Route operator, service, and misc system skill requests. |
| [references/extension-skill-index.md](references/extension-skill-index.md) | Route DeepSci extension skill requests and readiness blockers. |
| [references/cli-index.md](references/cli-index.md) | Route Isomer CLI command-family requests and safe discovery commands. |

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

### Essential Output

Lead with whether the request was routed, executed, explained, paused for prerequisite recovery, blocked, or left unchanged. Explain in natural language how you understood the goal, name the selected skill or CLI family, and cite only the context that materially affected routing. For paused prerequisite recovery, state that the target was not executed, name the missing inputs, recommended next step, four recovery choices, and target resume point. For completed run-to traversal, lead with the original target outcome and summarize material prerequisite owner work, Runs or refs, and preserved Gates.

### Complete Output

Group the complete explanation by routing alternatives and rationale, commands and their mutation posture, selected Project or research context, extension readiness, prerequisite dependency plan and authorization posture, bounded owner and service delegation, and any retired routes excluded from consideration.

When this skill proceeds through another owner skill, compose the final answer around the user-visible outcome. Do not concatenate or merge the parent and child skills' field inventories.

## Operational Contract

- Prefer read-only context discovery before ambiguous mutation. Proceed only when the task implies action and the selected owner workflow or CLI command family owns that action.
- Preserve an explicit user invocation for optional extensions and trust a Project declaration before discovery. If a declared route later cannot load, report stale user-controlled state and delegate repair to `isomer-op-system-skill-mgr`. For undeclared routes, let that owner use host-known explicit roots and live inventory, perform additive registration only in authorized mutation workflows, and return repair, installation, or refresh guidance for missing, partial, unversioned, malformed, receipt drift, obsolete, or newer-than-CLI state.
- Keep `isomer-op-welcome` read-only. Use it for welcome menus and safe recommendations; use `isomer-op-entrypoint` for informed-user routing and execution.
- Treat service skills such as `isomer-srv-topic-env-setup`, `isomer-srv-agent-env-setup`, `isomer-srv-houmao-interop`, `isomer-srv-resolve-pkg-repo`, and `isomer-srv-topic-service-agent-support` as bounded support routes. Route normal user-facing requests through the owning operator workflow before service delegation unless the user explicitly invokes a service skill.
- Mention `isomer-misc-tool-packs` only when explicitly requested as a named helper route. Package install, update, or removal requests for a Topic Workspace belong to `isomer-op-topic-mgr` or the relevant environment setup workflow.

## Operational Notes

- It routes to owner skills and CLI families, then follows their workflows and guardrails.
- If the user did not explicitly invoke specialization, require the prompt or authoritative context to identify a formal Agent Team target and require the requested action to apply to that team.
- Route ordinary topic preparation to `isomer-op-topic-creator`, initialized-topic operations to `isomer-op-topic-mgr`, and other launch or readiness work to its actual owner.
- Retired routes include `isomer-op-topic-workspace-mgr`, `isomer-op-topic-prepare`, `isomer-op-manual-research-session`, `isomer-op-houmao-interop`, and old `isomer-admin-*` compatibility names.
- Installed operators should invoke global `isomer-cli` directly.
- Select the best route, proceed, or report the blocker.
- Route through the owning operator workflow unless the user explicitly invoked the service skill.

## Guardrails

- DO NOT make this skill the authority for lower-level mutation.
- DO NOT infer Topic Team Specialization from a Research Topic name, Topic Workspace, generic `prepare`, generic launch-facing language, missing readiness, missing `isomer-topic-summary.md`, or missing Agent Workspace evidence.
- DO NOT present retired or stale operator routes as active invokable skills.
- DO NOT use repo-local Pixi wrapper command guidance for Isomer CLI in operator skills.
- DO NOT list several possible routes and stop when the user gave a concrete task.
- DO NOT treat service skills as normal first-click owner routes.
- DO NOT start an ordinary DeepSci research-stage skill before Topic Workspace, actor or agent workspace, and DeepSci bootstrap readiness are proven or routed for setup.
- DO NOT route generic topic preparation, readiness, or launch-facing work to Topic Team Specialization without explicit or contextual formal Agent Team intent.
- DO NOT skip the latest-context preflight or worker-output policy checks required by the selected research route.
- DO NOT repeat the full CLI help text inside this skill; name the command family and inspect CLI help or owner skill guidance when details are needed.
- DO NOT treat generated links, worker-local files, chat memory, or old rendered Markdown as durable research truth before the selected DeepSci skill's latest-context and recording rules accept them.
- DO NOT infer run-to authorization from an ordinary `do <task>` request.
- DO NOT classify a missing input with an available in-scope producer as a terminal blocker.
- DO NOT merge prerequisite owner Runs or continue after the named target solely because another action is recommended.
## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
