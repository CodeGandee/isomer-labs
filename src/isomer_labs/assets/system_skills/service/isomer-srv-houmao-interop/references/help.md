# Isomer Service Houmao Interop — Help

## Purpose

This service skill bridges Isomer Labs project constructs and the Houmao agent runtime. Use it when a Project Operator Session, Operator Agent, Topic Service Agent, Topic Service Master, or Service Request needs bounded Houmao adapter support: loop explanation, customization points, Domain Agent Team Template mapping, or live runtime inspection.

## When to Use

Use this skill whenever the support request mentions:

- Houmao loop, agent loop, gateway loop, or runtime lifecycle.
- Houmao customization: roles, recipes, presets, specialists, launch dossiers, launch profiles, project overlays, credentials, mailbox, gateway, or runtime config.
- Running DeepScientist or another Domain Agent Team Template under Houmao.
- Mapping Isomer Research Topic / Topic Workspace constructs to Houmao.

Do not use this skill for full Topic Team Specialization, approval, profile materialization, launch orchestration, Gate decisions, or research task routing. Route those responsibilities back to the appropriate operator workflow such as `isomer-op-topic-team-specialize`.

## Workflow

1. Match the support request to one mode in the table below.
2. Load only the selected mode page and preserve its operator and service boundaries.
3. Report the selected mode, key files or commands, blockers, and next action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a bounded support plan from the available modes and ownership boundaries, then execute the plan.

## Modes

| Mode | Use When |
| --- | --- |
| `explain-loop` | The support request asks how the Houmao loop works |
| `customize-loop` | The support request asks what to edit to customize the loop |
| `map-template-to-houmao` | The support request asks how a template maps to Houmao |
| `inspect-runtime` | The support request asks how to inspect a running agent |

## Quick Reference

- Houmao source checkout: `extern/orphan/houmao`.
- Houmao loop engine: `src/houmao/agents/realm_controller/gateway_service.py`.
- Lifecycle timing kernel: `src/houmao/agents/lifecycle/rx_lifecycle_kernel.py`.
- Agent definition directory: `.houmao/agents/` inside a Houmao project overlay.
- Project overlay discovery: `src/houmao/project/overlay.py`.
- Launch profile resolution: `src/houmao/project/launch_profiles.py`.
- Houmao CLI: `houmao-mgr`.
- Passive API server: `houmao-passive-server`.

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

### Essential Output

Summarize the selected mode, key files, relevant commands, blockers, and next action.

### Complete Output

Group the complete explanation by mode, Houmao source root, key files, concept mapping, customization points, commands, blockers, and next action.
