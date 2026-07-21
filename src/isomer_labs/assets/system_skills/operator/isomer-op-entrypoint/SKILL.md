---
name: isomer-op-entrypoint
description: Use when a Project Operator needs an informed-user entrypoint to route a concrete prompt, file, topic task, actor or agent task, extension-skill request, or Isomer CLI need to the correct Isomer system skill or CLI surface and proceed.
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Isomer Operator Entrypoint

## Overview

Use this public execution entrypoint as the route-and-proceed dispatcher for core Isomer work. It resolves public subcommands or task-only requests to protected operator, service, and shared members, optional public extension entrypoints, or an Isomer CLI family. Empty invocation and orientation-only requests delegate read-only output to the independent `$isomer-op-welcome` sibling.

## When to Use

Use this skill for a concrete task, prompt, file, Research Topic, Topic Actor, Agent, DeepSci request, Kaoju request, or CLI-shaped operation. Use `$isomer-op-welcome` directly for first contact, route comparison, typical use cases, or command learning; this entrypoint preserves compatibility by delegating those read-only requests with supplied context intact.

Do not use this skill to bypass owner workflows. Project lifecycle work belongs to `isomer-op-entrypoint->project`, system-skill lifecycle belongs to `isomer-op-entrypoint->system-skills`, Project Web GUI work belongs to `isomer-op-entrypoint->gui`, topic creation belongs to `isomer-op-entrypoint->topic-create`, initialized-topic management belongs to `isomer-op-entrypoint->topic-manage`, identity posture belongs to `isomer-op-entrypoint->identity`, project-local Toolbox management belongs to `isomer-op-entrypoint->toolbox`, and Topic Team Specialization belongs to `isomer-op-entrypoint->topic-team`. DeepSci bootstrap uses `isomer-ext-deepsci-entrypoint->workspace`, Kaoju readiness uses `isomer-ext-kaoju-entrypoint->workspace`, and focused research uses the selected protected member of its public extension pack.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Parse the task input and public invocation**. Accept `$isomer-op-entrypoint use <subcommand> to <task>`, a concrete task-only request, or empty invocation. Empty invocation, `help`, `show-options`, `show-extensions`, `choose-path`, `show-skill-map`, `show-command-map`, `next-step`, and the four retained research-start commands delegate read-only output to `$isomer-op-welcome` while preserving supplied context. Otherwise identify any supplied file, Project root, Research Topic, Topic Workspace, Topic Actor, Agent, Domain Agent Team Template, extension intent, CLI action, or logical capability id. See [references/input-surfaces.md](references/input-surfaces.md).
2. **Classify operation scope and prompt targets**. Classify the intended operation as `project`, `topic`, `topic-actor`, or `agent` before resolving defaults. Convert every prompt-named Research Topic, Topic Actor, or Agent into the matching explicit selector. A Project-scoped task stays Project-scoped even when Effective Context can resolve a topic fallback.
3. **Run context-sensitive preflight**. Run `isomer-cli --print-json project self location`, then run `isomer-cli --print-json project self check --scope <project|topic|topic-actor|agent>` with every prompt target supplied as `--topic`, `--topic-actor`, or `--agent`. Topic- or worker-scoped work with no explicit topic may use a valid reported default, but must report that fallback source. Worker-scoped work requires an explicit worker target or an active session switch posture; a sole manifest actor is only an Effective Context candidate and never proves active acting posture.
4. **Pin reconciled invocation context**. Stop before mutation on `unresolved` or `conflict`, report every conflicting source and the corrective selector, cwd, switch reset, or scope decision, and never choose a sibling topic, alternate worker, or alternate output directory. For `aligned` or `explicit_override`, pin the resolved target for the route: every applicable downstream command carries `--topic <resolved-topic>` plus `--topic-actor <resolved-topic-actor>` or `--agent <resolved-agent>`. Rerun context preflight whenever the user or workflow changes topic, worker, or operation scope.
5. **Run other safe context discovery when useful**. Prefer read-only evidence such as `isomer-cli project self queries`, `isomer-cli project self show`, `isomer-cli project validate`, `isomer-cli doctor`, `isomer-cli project topics list`, `isomer-cli project context show`, or Workspace Path Resolution commands before ambiguous mutation. See [references/cli-index.md](references/cli-index.md).
6. **Check optional-extension availability**. Before selecting a DeepSci or Kaoju route, treat an existing Project declaration as authoritative routing intent and attempt that public entrypoint. When current-host usability must be established, route ordered v5 receipt, explicit-root, and limited live-inventory resolution through `isomer-op-entrypoint->system-skills`. Only verified current-v5 public-pair pack evidence can support additive registration. Do not encode provider discovery paths in this entrypoint.
7. **Establish formal Agent Team intent before specialization**. Select `isomer-op-entrypoint->topic-team` only when the user explicitly invokes its public route or the prompt or authoritative Project context establishes a formal Agent Team target. Name the Domain Agent Team Template, Topic Agent Team Profile or Bundle, Topic Team Instantiation Packet, Agent Team Instance, selected formal-team material, or equivalent evidence used. Generic topic preparation, launch-facing work, readiness gaps, missing summaries, or missing Agent Workspaces do not establish Agent Team intent.
8. **Classify exactly one route**. Resolve a public command, one catalog-declared protected member, one public extension entrypoint, or one CLI family. Use [references/routing-rules.md](references/routing-rules.md), [references/system-skill-index.md](references/system-skill-index.md), and [references/extension-skill-index.md](references/extension-skill-index.md).
9. **Check owner boundaries**. Confirm the selected route owns the requested work, service skills are only bounded support unless explicitly invoked, misc helpers are explicit helper routes, and retired operator compatibility skills are not active routes.
10. **Preflight target prerequisites**. Before target mutation, let the selected owner resolve its required artifacts, accepted inputs, readiness evidence, and known producer routes without dropping the pinned invocation context. See [references/prerequisite-recovery.md](references/prerequisite-recovery.md).
11. **Route prerequisite recovery**. If a producible prerequisite is missing and run-to is not explicitly authorized, stop before prerequisite mutation, report `paused`, and offer run-to-target, next-prerequisite-only, alternate-route, and stop choices. If run-to is authorized, use the native planning tool to execute the target-scoped dependency closure through its owners and resume the original target. See [references/prerequisite-recovery.md](references/prerequisite-recovery.md).
12. **Proceed with the selected route**. Unless the user asked only for route explanation, invoke the selected protected member through its catalog designator, invoke the selected public extension, load the parent-owned command page, or run the selected CLI command family. Do not stop after only listing candidate routes. During authorized run-to, preserve each owner's separate mutation, Run, checkpoint, Gate, and terminal-report boundaries. If a typed operation fails, compare its returned selected context with the pinned target, correct or rerun preflight, and preserve the original target; do not search sibling topics, switch to a manifest default, or perform an unmanaged filesystem copy unless the user explicitly requests a separate operation.
13. **Report the entrypoint result** using **Essential Output** by default and **Complete Output** when requested. Include operation scope, pinned target and selection source, alignment verdict, and any context-bearing failure that affected execution. Stop run-to after the original target completes or at a nondelegable boundary; do not continue into later recommended work.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step routing plan from this skill, the route references, current user request, available Project context, owner boundaries, and blockers, then execute the plan or stop on a concrete blocker.

## Public Commands

Use `$isomer-op-entrypoint use <subcommand> to <task>`. Public execution commands expose the protected operator-member route keys, `package-specifics`, and `tool-packs`. Empty invocation, `help`, and the retained welcome-style commands delegate to `$isomer-op-welcome`; they do not copy or execute welcome procedure resources. Service and recording members remain task-selected support routes rather than ordinary first-click commands.

## Protected Subskills

| Member | Logical ID | Area | When to Route Here | Internal Designator |
| --- | --- | --- | --- | --- |
| `project` | `isomer-op-project-mgr` | operator | The request concerns Project bootstrap, health, context inspection, lifecycle, cleanup, or relocation rather than creating or managing one Research Topic. | `isomer-op-entrypoint->project` |
| `gui` | `isomer-op-gui-mgr` | operator | The Project Web GUI must be started, inspected, refreshed, configured, debugged, or mapped to a Backend API route. | `isomer-op-entrypoint->gui` |
| `identity` | `isomer-op-switch-identity` | operator | Operator work must run once or persistently under a selected Topic Actor or Agent posture, or return to normal operator identity. | `isomer-op-entrypoint->identity` |
| `system-skills` | `isomer-op-system-skill-mgr` | operator | An extension pack must be detected, reconciled, installed, upgraded, inspected, migrated, or repaired for a concrete agent host and scope. | `isomer-op-entrypoint->system-skills` |
| `toolbox` | `isomer-op-toolbox-mgr` | operator | A project-local Toolbox, callback declaration or insertion point, or Toolbox Runtime Param must be created, converted, installed, inspected, updated, disabled, or removed. | `isomer-op-entrypoint->toolbox` |
| `topic-create` | `isomer-op-topic-creator` | operator | Empty or partial Project state must become a prepared Research Topic and Topic Workspace through the Topic Creator readiness handoff. | `isomer-op-entrypoint->topic-create` |
| `topic-manage` | `isomer-op-topic-mgr` | operator | An initialized Research Topic after Topic Creator handoff needs storage, actor, topology, package, environment, checkpoint, or diagnostic management. | `isomer-op-entrypoint->topic-manage` |
| `topic-team` | `isomer-op-topic-team-specialize` | operator | The user explicitly requests Topic Team Specialization or established context names a formal Agent Team that must be initialized, specialized, validated, repaired, or materialized. | `isomer-op-entrypoint->topic-team` |
| `topic-env` | `isomer-srv-topic-env-setup` | service | An owning operator workflow needs bounded service support to prepare or repair the enclosed Pixi environment and development repository for a Topic Workspace, independent of Agent Team structure. | `isomer-op-entrypoint->topic-env` |
| `agent-env` | `isomer-srv-agent-env-setup` | service | Topic Workspace and repository predecessor evidence already exists, and an owning operator workflow needs service-safe per-Agent Workspace setup or repair. | `isomer-op-entrypoint->agent-env` |
| `package-repo` | `isomer-srv-resolve-pkg-repo` | service | A package manager needs repository or channel selection, mirror fallback, or NVIDIA channel priority because its default source is slow, blocked, or unsuitable. | `isomer-op-entrypoint->package-repo` |
| `houmao` | `isomer-srv-houmao-interop` | service | An owner or Service Request needs bounded Houmao adapter support for loop explanation, template mapping, customization guidance, or runtime inspection without delegating operator decisions. | `isomer-op-entrypoint->houmao` |
| `topic-service` | `isomer-srv-topic-service-agent-support` | service | A Topic Service Agent or Service Master needs bounded support for workspace, environment, team, monitoring, diagnostics, or support Artifact work under an owner route. | `isomer-op-entrypoint->topic-service` |
| `bounded-run` | `isomer-misc-bounded-run-tips` | shared | Resource-heavy execution needs risk classification, safe concurrency or memory bounds, CUDA architecture limits, or crash-avoidance guidance. | `isomer-op-entrypoint->bounded-run` |
| `nvidia` | `isomer-misc-nvidia-tools` | shared | A Pixi CUDA or C++ build needs NVIDIA Toolkit components, Conda packages, host-tool wiring, or CMake and Ninja integration. | `isomer-op-entrypoint->nvidia` |
| `package-specifics` | `isomer-misc-pkg-specifics` | shared | A named dependency needs package-specific source, variant, compatibility, or installation-caveat guidance rather than general repository selection. | `isomer-op-entrypoint->package-specifics` |
| `tool-packs` | `isomer-misc-tool-packs` | shared | The user explicitly requests a named installable toolset to be resolved into dependency, CLI-install, verification, and downstream setup contracts. | `isomer-op-entrypoint->tool-packs` |
| `research-ideas` | `isomer-research-idea-recording` | shared | A workflow has changed a durable research concept or portfolio decision and must record canonical Research Idea state, facets, transitions, generations, or lineage. | `isomer-op-entrypoint->research-ideas` |
| `operation-sets` | `isomer-research-operation-set-recording` | shared | A completed operation-set directory must be exhaustively classified, promoted into durable records or attachments, linked, accepted with a receipt, verified, or repaired before closeout. | `isomer-op-entrypoint->operation-sets` |

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
- Treat ambient workspace location, Effective Context, task-selected target, manifest fallback, and active acting posture as separate evidence. These values guide deterministic routing and cwd discipline; none is an access-control identity or proof of authorization.
- Preserve the pinned invocation context across owner routes, prerequisite Runs, cwd changes, and typed failures. A context-bearing failure does not authorize a different topic, worker, output surface, or raw copy.
- Preserve an explicit user invocation for optional extensions and treat a Project declaration as authoritative routing intent. If a declared route later cannot load, report stale user-controlled state and delegate repair to `isomer-op-entrypoint->system-skills`. Let that owner inspect current v5 receipts and host-known explicit roots before using live inventory as limited observation evidence. It performs additive registration only for verified current-v5 public-pair packs in authorized mutation workflows and returns migration, repair, installation, or refresh guidance for legacy, welcome-only, entrypoint-only, missing, partial, unversioned, malformed, receipt drift, obsolete, or newer-than-CLI state.
- Delegate empty invocation, `help`, and retained welcome-style commands to `$isomer-op-welcome`; keep concrete route-and-proceed work in this execution entrypoint.
- Treat `isomer-op-entrypoint->topic-env`, `isomer-op-entrypoint->agent-env`, `isomer-op-entrypoint->houmao`, `isomer-op-entrypoint->package-repo`, and `isomer-op-entrypoint->topic-service` as bounded support routes. Route normal user-facing requests through the owning operator workflow before service delegation.
- Mention `isomer-op-entrypoint->tool-packs` only when explicitly requested as a named helper route. Package install, update, or removal requests for a Topic Workspace belong to `isomer-op-entrypoint->topic-manage` or the relevant environment setup workflow.

## Operational Notes

- It routes to owner skills and CLI families, then follows their workflows and guardrails.
- If the user did not explicitly invoke specialization, require the prompt or authoritative context to identify a formal Agent Team target and require the requested action to apply to that team.
- Route ordinary topic preparation to `isomer-op-entrypoint->topic-create`, initialized-topic operations to `isomer-op-entrypoint->topic-manage`, and other launch or readiness work to its actual owner.
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
