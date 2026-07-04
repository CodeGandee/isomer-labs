# Isomer Service Houmao Interop — Customize Loop

## Overview

Customize the Houmao agent loop by editing the agent-definition directory, the project overlay, loop packages, gateway config, and runtime/mailbox bindings. Avoid changing Houmao source files unless you are fixing a Houmao bug.

## Customization Layers

### 1. Agent Definition Directory

Location inside a Houmao project overlay: `.houmao/agents/`

| Subdirectory | Purpose | Example Files |
| --- | --- | --- |
| `tools/` | Tool adapters declare launch executable, home selector, setup/skills/auth projection. | `src/houmao/project/assets/starter_agents/tools/<tool>/adapter.yaml` in Houmao source; project-local copies under `.houmao/agents/tools/`. |
| `roles/` | Role definitions loaded by presets. | `.houmao/agents/roles/*.yaml` |
| `setups/` | Setup bundles for tool homes. | `.houmao/agents/setups/*.yaml` |
| `auth/` | Credential bundle descriptors. | `.houmao/agents/auth/*.yaml` |
| `presets/` | Recipes that bind role + tool + setup + skills + auth + launch + mailbox + extra. | `.houmao/agents/presets/*.yaml` |
| `skills/` | Agent-facing skills loaded by presets. | `.houmao/agents/skills/<skill-name>/SKILL.md` |

Preset YAML is parsed by `AgentPreset` in `src/houmao/agents/definition_parser.py`.

### 2. Project Overlay

Location inside an Isomer/Houmao project: `.houmao/`

| Concept | Where It Lives | Notes |
| --- | --- | --- |
| Specialists | `.houmao/easy/specialists/` (legacy) or the project catalog | `SpecialistCatalogEntry` resolves to a preset path. |
| Launch profiles / dossiers | Project SQLite catalog (`src/houmao/project/catalog.py`) and `src/houmao/project/launch_profiles.py` | `LaunchProfileCatalogEntry` points to a recipe (`source_kind=recipe`) or a specialist (`source_kind=specialist`). |
| Profiles | `src/houmao/project/easy.py` | `EasyProfileMetadata` = launch profile with `profile_lane == "easy_profile"`. |
| Credentials | Tool `auth/` directories and `houmao-mgr credentials ...` | Mapped env vars (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `KIMI_MODEL_API_KEY`) and files. |
| Mailbox | `.houmao/mailbox/` or configured mailbox root | Filesystem or Stalwart JMAP store. |
| Memory | `.houmao/memory/` | `houmao-memo.md` and pages. |
| Runtime state | `.houmao/runtime/` | Gateway config, queue, status, tmux state. |

Project overlay class: `src/houmao/project/overlay.py` (`HoumaoProjectOverlay`).

### 3. Loop Packages

Houmao ships built-in agent-loop skills for authoring/operating loop packages:

| Package | Location | Use Case |
| --- | --- | --- |
| `houmao-agent-loop-pro` | `src/houmao/agents/assets/system_skills/houmao-agent-loop-pro/` | Schema-rich execplans and topology-aware loop contracts. |
| `houmao-agent-loop-lite` | `src/houmao/agents/assets/system_skills/houmao-agent-loop-lite/` | Markdown/direct-SQL loop packages. |

System skill catalog: `src/houmao/agents/assets/system_skills/catalog.toml`.

Loop graph analysis utilities: `src/houmao/agents/loop_graph/`.

### 4. Gateway and Runtime Config

| Config | File / Command | Notes |
| --- | --- | --- |
| Gateway models | `src/houmao/agents/realm_controller/gateway_models.py` | `GatewayTuiTrackingTimingConfigV1` controls stability timers. |
| Gateway storage | `src/houmao/agents/realm_controller/gateway_storage.py` | Persists desired config, queue, status under agent runtime root. |
| Gateway client | `src/houmao/agents/realm_controller/gateway_client.py` | HTTP client to a live gateway. |
| Mailbox binding | `src/houmao/agents/mailbox_runtime_support.py` | `resolve_live_mailbox_binding`, `bootstrap_resolved_mailbox`. |

### 5. CLI Commands

Main Houmao CLI: `houmao-mgr`.

| Command Group | Typical Commands |
| --- | --- |
| Agent lifecycle | `houmao-mgr agents launch --agents <selector>`, `houmao-mgr agents single --agent-id <id> prompt|interrupt|stop|relaunch|state` |
| Gateway | `houmao-mgr agents single --agent-id <id> gateway status|prompt|interrupt|...` |
| Mailbox | `houmao-mgr agents single --agent-id <id> mailbox ...`, `houmao-mgr mailbox ...` |
| Memory | `houmao-mgr agents single --agent-id <id> memory ...` |
| Credentials | `houmao-mgr credentials claude|codex|gemini|kimi add|list|remove|show ...` |
| Project | `houmao-mgr project ...` |
| System skills | `houmao-mgr system-skills ...` |

Passive API server: `houmao-passive-server serve --host ... --port ...`.

## How to Add a New Stage Skill

1. Author the skill Markdown under `.houmao/agents/skills/<skill-name>/SKILL.md` or `skillset/<area>/<skill-name>/SKILL.md` if it is Isomer-specific.
2. Add or update a preset in `.houmao/agents/presets/` that includes the skill in its `skills:` list.
3. Register the preset in the project catalog if it is a launch-facing recipe.
4. If the skill should be available as a standalone specialist, add a specialist entry pointing to the preset.
5. Validate with `houmao-mgr system-skills validate` or equivalent project validator before launch.

## Common Mistakes

- Editing `extern/orphan/houmao/src/...` to change Isomer project behavior. Prefer project-local `.houmao/` overrides.
- Creating one Houmao agent per stage skill for a DeepScientist-like template. DeepScientist is a single PI agent that switches stage skills; map it to one Houmao-managed agent, not many.
- Confusing a Houmao "role" (preset ingredient) with a DeepScientist "stage skill" (prompt contract). A stage skill is closer to a Houmao agent-facing skill loaded by a preset.
- Skipping catalog registration. A preset file alone is not launchable until the project catalog or launch profile points to it.
