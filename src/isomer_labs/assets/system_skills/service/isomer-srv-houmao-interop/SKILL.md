---
name: isomer-srv-houmao-interop
description: Use for bounded service-routed Houmao adapter support when a Project Operator Session, Operator Agent, or Service Request needs Houmao loop explanation, adapter customization guidance, Domain Agent Team Template mapping, or runtime inspection without making operator, launch, Gate, or research decisions.
---

# Isomer Service Houmao Interop

Use this skill as bounded Service Team support between Isomer Labs project concepts and the Houmao agent runtime. It explains how the Houmao agent loop works, where each customization point lives, and how Isomer constructs such as Domain Agent Team Templates, Research Topics, and Topic Workspaces map onto Houmao adapter concepts such as presets, specialists, launch profiles, and project overlays.

## Operating Model

Run this workflow at the command of a Project Operator Session, Operator Agent, Topic Service Agent, Topic Service Master, or explicit Service Request pointed at the Isomer Project root. Treat Houmao as the execution and adapter layer underneath Isomer Labs unless the Isomer domain language has explicitly promoted a Houmao term into core Isomer schema or UI language.

Use this skill for one bounded Houmao-interop support task at a time. For user-facing Project lifecycle, Topic Team Specialization, approval provenance, profile materialization, Agent Team Instance launch orchestration, Gate decisions, or research task routing, route back to the appropriate operator workflow such as `isomer-op-project-mgr`, `isomer-op-topic-team-specialize`, or generic Isomer CLI/API surfaces.

When this skill needs Houmao-owned procedure, do not assume the Project Operator has Houmao system skills installed in their ordinary tool home and do not rely on implicit Houmao project discovery. First request Isomer-provided context with `isomer-cli --print-json project integrations houmao skill-context <route-name>`. If the response is `disabled`, report skipped Houmao integration work. If the response is `not_configured`, report the Isomer next action. If the response is `enabled`, tell the agent to read the returned `houmao_skill_path` and run Houmao commands with `--project-dir <houmao_project_path>`.

## Workflow

When this service skill is invoked, choose one of the modes below.

1. **Default help mode**:
   - Match when this skill is invoked without a prompt.
   - Select `help`, load [references/help.md](references/help.md), execute its workflow, and report its output.
2. **Explain-loop mode**:
   - Match when the support request asks how the Houmao agent loop works, what drives it, or what its stages are.
   - Select `explain-loop`, load [references/explain-loop.md](references/explain-loop.md), and report a concise architecture summary.
3. **Customize-loop mode**:
   - Match when the support request asks how to customize the Houmao agent loop, roles, recipes, presets, specialists, launch dossiers, project overlays, credentials, mailbox, gateway, or runtime.
   - Select `customize-loop`, load [references/customize-loop.md](references/customize-loop.md), and report the relevant customization points and file paths.
4. **Map-template mode**:
   - Match when the support request asks how a Domain Agent Team Template such as DeepScientist maps onto Houmao, or how to run DeepScientist stage skills under Houmao.
   - Select `map-template-to-houmao`, load [references/map-template-to-houmao.md](references/map-template-to-houmao.md), and report the concept mapping.
5. **Inspect-runtime mode**:
   - Match when the support request asks how to inspect a running Houmao agent, gateway, mailbox, or runtime state.
   - Select `inspect-runtime`, load [references/inspect-runtime.md](references/inspect-runtime.md), and report the appropriate commands or files.
6. If the request is ambiguous, prefer the mode that names the most specific concept the user mentioned. If no concept is clear, default to `help`.
7. Preserve the **Guardrails** and **Output Contract** for all modes.

If the support request does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the project context, subcommands, output contract, and guardrails in this skill, then execute only the service-safe portion.

## Subcommands

Load only the subcommand pages needed for the support task.

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `help` | Print what this skill does, how to invoke it, available modes, outputs, and guardrails | [references/help.md](references/help.md) |
| `explain-loop` | Explain the Houmao agent loop architecture and lifecycle | [references/explain-loop.md](references/explain-loop.md) |
| `customize-loop` | List Houmao agent-loop customization points and file paths | [references/customize-loop.md](references/customize-loop.md) |
| `map-template-to-houmao` | Map Isomer Domain Agent Team Templates and DeepScientist stage skills to Houmao concepts | [references/map-template-to-houmao.md](references/map-template-to-houmao.md) |
| `inspect-runtime` | Inspect live Houmao runtime, gateway, mailbox, and agent state | [references/inspect-runtime.md](references/inspect-runtime.md) |
| `skill-context` | Resolve Isomer-managed Project-local Houmao skill routing context before following Houmao-owned procedure | [references/skill-context.md](references/skill-context.md) |

## Output Contract

Default to **Essential Output** in chat. Print **Complete Output** only when the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output.

### Essential Output

Report:

- `status`: interop, customization, or help result.
- `mode`: selected subcommand.
- `key_files`: the most important files or directories to inspect or edit.
- `commands`: relevant Houmao or Isomer commands.
- `blockers`: unresolved items that prevent safe support, customization guidance, inspection, or launch-facing handoff.
- `next_action`: safe operator follow-up, service repair route, adapter route, or stop condition.

### Complete Output

When requested, include:

- `mode`
- `houmao_source_root`
- `domain_template_root`
- `key_files`
- `concept_mapping`
- `customization_points`
- `commands`
- `blockers`
- `next_action`

## Guardrails

Do not treat Houmao terms as Isomer core domain language unless the Isomer schema or UI explicitly uses them. Keep Houmao as the adapter/implementation layer.

Do not edit the Houmao source checkout (`extern/orphan/houmao`) to fix Isomer project behavior. If a Houmao bug blocks Isomer work, fix it in the Houmao checkout as separate local work and validate it with Houmao's own commands before depending on it.

Do not launch Houmao-managed agents from Domain Agent Team Template source directly. Route through the approved Topic Agent Team Profile Bundle and Workspace Runtime flow owned by `isomer-op-topic-team-specialize`.

Do not conflate DeepScientist's single-agent stage-skill model with Houmao's multi-agent role/recipe model. One DeepScientist quest normally maps to one Houmao-managed agent that loads stage skills through prompts and state, not to one Houmao agent per stage.

Do not own Project lifecycle, Research Topic creation, Topic Team Specialization, approval provenance, Topic Agent Team Profile materialization, Agent Team Instance launch orchestration, Gate decisions, Research Claims, or research task routing. Route those decisions back to the Project Operator Session, Operator Agent, generic Isomer CLI/API surface, or Execution Adapter boundary.

Do not tell users that direct Houmao system-skill installation is required for ordinary Isomer operation. Houmao is an internal integration provider for this route; Project-local projected support material comes from `isomer-cli project integrations houmao prepare-skills`.
