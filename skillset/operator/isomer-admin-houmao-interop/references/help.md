# Isomer Admin Houmao Interop — Help

## Purpose

This skill bridges Isomer Labs project constructs and the Houmao agent runtime. Use it when an operator agent needs to explain the Houmao agent loop, locate customization points, map a Domain Agent Team Template to Houmao concepts, or inspect live Houmao runtime state.

## When to Use

Use this skill whenever the prompt mentions:

- Houmao loop, agent loop, gateway loop, or runtime lifecycle.
- Houmao customization: roles, recipes, presets, specialists, launch dossiers, launch profiles, project overlays, credentials, mailbox, gateway, or runtime config.
- Running DeepScientist or another Domain Agent Team Template under Houmao.
- Mapping Isomer Research Topic / Topic Workspace constructs to Houmao.

Do not use this skill for full Topic Team Specialization; use `isomer-admin-topic-team-specialize` for copying and adapting template material.

## Modes

| Mode | Use When |
| --- | --- |
| `explain-loop` | The user asks how the Houmao loop works |
| `customize-loop` | The user asks what to edit to customize the loop |
| `map-template-to-houmao` | The user asks how a template maps to Houmao |
| `inspect-runtime` | The user asks how to inspect a running agent |

## Quick Reference

- Houmao source checkout: `extern/orphan/houmao`.
- Houmao loop engine: `src/houmao/agents/realm_controller/gateway_service.py`.
- Lifecycle timing kernel: `src/houmao/agents/lifecycle/rx_lifecycle_kernel.py`.
- Agent definition directory: `.houmao/agents/` inside a Houmao project overlay.
- Project overlay discovery: `src/houmao/project/overlay.py`.
- Launch profile resolution: `src/houmao/project/launch_profiles.py`.
- Operator CLI: `houmao-mgr`.
- Passive API server: `houmao-passive-server`.

## Output Contract

Report `mode`, `houmao_source_root`, `key_files`, `concept_mapping`, `customization_points`, `commands`, `blockers`, and `next_operator_action`.
