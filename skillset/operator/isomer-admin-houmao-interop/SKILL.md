---
name: isomer-admin-houmao-interop
description: Use when an Isomer Labs operator agent must explain, customize, or bridge Houmao-managed agent teams and Isomer Labs project constructs, especially when the prompt mentions Houmao loop, agent loop customization, roles, recipes, presets, specialists, launch dossiers, project overlays, or mapping a Domain Agent Team Template to Houmao.
---

# Isomer Admin Houmao Interop

Use this skill as the operator bridge between Isomer Labs project concepts and the Houmao agent runtime. It explains how the Houmao agent loop works, where each customization point lives, and how Isomer constructs such as Domain Agent Team Templates, Research Topics, and Topic Workspaces map onto Houmao concepts such as presets, specialists, launch profiles, and project overlays.

## Operating Model

Run this workflow from a Project Operator Session or Operator Agent pointed at the Isomer Project root. Treat Houmao as the execution and adapter layer underneath Isomer Labs unless the Isomer domain language has explicitly promoted a Houmao term into core Isomer schema or UI language.

Use this skill for one bounded Houmao-interop task at a time. For full Topic Team Specialization, prefer `isomer-admin-topic-team-specialize`; this skill answers the Houmao-specific questions that arise while using that skill.

## Workflow

When this skill is invoked, choose one of the modes below.

1. **Default help mode**: If this skill is invoked without a prompt, select `help`, load [references/help.md](references/help.md), execute its workflow, and report its output.
2. **Explain-loop mode**: If the user asks how the Houmao agent loop works, what drives it, or what its stages are, select `explain-loop`, load [references/explain-loop.md](references/explain-loop.md), and report a concise architecture summary.
3. **Customize-loop mode**: If the user asks how to customize the Houmao agent loop, roles, recipes, presets, specialists, launch dossiers, project overlays, credentials, mailbox, gateway, or runtime, select `customize-loop`, load [references/customize-loop.md](references/customize-loop.md), and report the relevant customization points and file paths.
4. **Map-template mode**: If the user asks how a Domain Agent Team Template such as DeepScientist maps onto Houmao, or how to run DeepScientist stage skills under Houmao, select `map-template-to-houmao`, load [references/map-template-to-houmao.md](references/map-template-to-houmao.md), and report the concept mapping.
5. **Inspect-runtime mode**: If the user asks how to inspect a running Houmao agent, gateway, mailbox, or runtime state, select `inspect-runtime`, load [references/inspect-runtime.md](references/inspect-runtime.md), and report the appropriate commands or files.
6. If the request is ambiguous, prefer the mode that names the most specific concept the user mentioned. If no concept is clear, default to `help`.
7. Preserve the **Guardrails** and **Output Contract** for all modes.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the project context, subcommands, output contract, and guardrails in this skill, then execute the plan.

## Subcommands

Load only the subcommand pages needed for the user's task.

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `help` | Print what this skill does, how to invoke it, available modes, outputs, and guardrails | [references/help.md](references/help.md) |
| `explain-loop` | Explain the Houmao agent loop architecture and lifecycle | [references/explain-loop.md](references/explain-loop.md) |
| `customize-loop` | List Houmao agent-loop customization points and file paths | [references/customize-loop.md](references/customize-loop.md) |
| `map-template-to-houmao` | Map Isomer Domain Agent Team Templates and DeepScientist stage skills to Houmao concepts | [references/map-template-to-houmao.md](references/map-template-to-houmao.md) |
| `inspect-runtime` | Inspect live Houmao runtime, gateway, mailbox, and agent state | [references/inspect-runtime.md](references/inspect-runtime.md) |

## Output Contract

When reporting results, include these fields in structured prose or a JSON block:

- `mode`: the subcommand selected.
- `houmao_source_root`: resolved path to the Houmao source checkout, usually `extern/orphan/houmao`.
- `domain_template_root`: resolved path to the Domain Agent Team Template, if relevant.
- `key_files`: list of concrete files or directories the operator should read or edit.
- `concept_mapping`: table or prose mapping Isomer concepts to Houmao concepts.
- `customization_points`: list of customization points with file paths and when to use each.
- `commands`: relevant `houmao-mgr`, `houmao-passive-server`, or Houmao skill commands.
- `blockers`: unresolved items that prevent customization or launch.
- `next_operator_action`: what the operator should do next.

## Guardrails

Do not treat Houmao terms as Isomer core domain language unless the Isomer schema or UI explicitly uses them. Keep Houmao as the adapter/implementation layer.

Do not edit the Houmao source checkout (`extern/orphan/houmao`) to fix Isomer project behavior. If a Houmao bug blocks Isomer work, fix it in the Houmao checkout as separate local work and validate it with Houmao's own commands before depending on it.

Do not launch Houmao-managed agents from Domain Agent Team Template source directly. Route through the approved Topic Agent Team Profile Bundle and Workspace Runtime flow owned by `isomer-admin-topic-team-specialize`.

Do not conflate DeepScientist's single-agent stage-skill model with Houmao's multi-agent role/recipe model. One DeepScientist quest normally maps to one Houmao-managed agent that loads stage skills through prompts and state, not to one Houmao agent per stage.
