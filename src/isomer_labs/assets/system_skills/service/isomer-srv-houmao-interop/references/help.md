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

Default to **Essential Output** in chat. Print **Complete Output** only when the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output.

### Essential Output

- `mode`
- `key_files`
- `commands`
- `blockers`
- `next_action`

### Complete Output

- `mode`
- `houmao_source_root`
- `key_files`
- `concept_mapping`
- `customization_points`
- `commands`
- `blockers`
- `next_action`
