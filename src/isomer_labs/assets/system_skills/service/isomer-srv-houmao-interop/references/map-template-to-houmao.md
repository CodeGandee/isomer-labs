# Isomer Service Houmao Interop — Map Template to Houmao

## Overview

Map Domain Agent Team Templates such as DeepScientist onto Houmao by understanding that the two systems have different shapes. DeepScientist is a **single-agent, prompt-driven research runtime** where one PI agent switches stage skills. Houmao is a **multi-agent gateway-managed runtime** where each managed agent has its own request queue, lifecycle kernel, and mailbox.

## DeepScientist Architecture Recap

Key directories in `extern/orphan/DeepScientist`:

| Path | Purpose |
| --- | --- |
| `src/skills/<skill_id>/SKILL.md` | Stage and companion skill definitions. |
| `src/deepscientist/skills/registry.py` | Discovers skills, classifies them as `stage`, `companion`, or `custom`. |
| `src/deepscientist/prompts/builder.py` | Assembles each turn prompt from system contract, shared interaction, runtime context, and active skill. |
| `src/deepscientist/quest/` | Quest lifecycle, layout, and state machine. |
| `src/deepscientist/runners/` | Codex/Claude/Kimi/OpenCode runners that launch the agent. |
| `src/prompts/system.md` | Global behavior contract. |
| `src/prompts/contracts/shared_interaction.md` | Continuity rules. |
| `AISB/catalog/aisb.*.yaml` | Topic/benchmark specialization YAMLs. |

DeepScientist always sets:

```python
DS_AGENT_ROLE = "pi"
DS_TEAM_MODE = "single"
```

The default macro loop from `src/prompts/system.md` is:

```
baseline → idea → experiment → analysis-campaign → write → finalize → decision
→ next loop idea/experiment if a new result becomes the incumbent
```

Stage handoffs happen by updating durable state (`quest.yaml`, `plan.md`, artifacts) and returning a recommended next anchor; the daemon schedules the next turn with the new skill.

## Concept Mapping

| Isomer / DeepScientist Concept | Houmao Equivalent | Notes |
| --- | --- | --- |
| DeepScientist quest | One Houmao-managed agent session | One PI agent runs the whole quest. |
| Stage skill (`scout`, `baseline`, `idea`, ...) | Agent-facing skill loaded by a preset | The skill Markdown becomes part of the prompt context. |
| Macro loop / active anchor | Prompt-driven state machine + gateway request queue | The loop advances by submitting prompts that carry the new anchor. |
| Companion skills (`paper-outline`, `review`, ...) | Additional skills in the preset `skills:` list or invoked on demand | Companions are not separate agents by default. |
| `startup_contract` | Launch profile / dossier extra fields or memo seed | Topic-specific policy and constraints. |
| Topic catalog YAML (`AISB/catalog/*.yaml`) | Houmao launch profile or specialist metadata | Topic description, launch commands, resource flags. |
| Runner (`claude.py`, `codex.py`, ...) | Houmao preset + tool adapter | The runner is replaced by Houmao's launch and gateway machinery. |

## How to Run DeepScientist Under Houmao

1. **Create a Houmao preset** that loads the DeepScientist stage skills and the global system prompt as agent-facing skills.
   - Preset location: `.houmao/agents/presets/deepscientist-pi.yaml`.
   - Include the tool adapter for the target backend (Claude, Codex, Kimi, etc.).
   - Include auth bundle for API keys.
2. **Create a launch profile or specialist** that points to the preset.
   - Use `source_kind=recipe` for a preset.
   - Use `source_kind=specialist` if you want a named specialist entry.
3. **Materialize the topic context** into the agent workspace:
   - Copy or reference the DeepScientist `startup_contract` fields.
   - Initialize quest layout (`brief.md`, `plan.md`, `status.md`, `artifacts/`, etc.).
4. **Launch one agent** with the preset/profile.
   - Command: `houmao-mgr agents launch --launch-profile <profile-name>`.
5. **Drive stage handoffs through prompts**, not by launching more agents.
   - Each prompt should carry the active stage skill and updated quest state.
   - The DeepScientist prompt builder logic can be reused as an agent-facing skill or reference.

## File Mapping

| DeepScientist File | Houmao File / Directory | Purpose |
| --- | --- | --- |
| `src/skills/<id>/SKILL.md` | `.houmao/agents/skills/<id>/SKILL.md` | Skill content. |
| `src/prompts/system.md` | `.houmao/agents/skills/deepscientist-system/SKILL.md` or prompt reference | Global contract. |
| `src/prompts/contracts/shared_interaction.md` | Skill reference or memo page | Continuity rules. |
| `AISB/catalog/<topic>.yaml` | Project catalog launch profile / specialist entry | Topic specialization. |
| `src/deepscientist/runners/*.py` | `.houmao/agents/presets/<preset>.yaml` + tool adapter | Launch mechanism. |
| `quest.yaml` | `.houmao/memory/` or agent workspace | Durable quest state. |

## Common Mistakes

- Mapping each DeepScientist stage to a separate Houmao agent. This breaks the DeepScientist single-PI design and complicates shared quest state.
- Treating DeepScientist `skill_role=stage` as a Houmao "role". A Houmao role is a preset ingredient; a DeepScientist stage is a prompt skill.
- Forgetting to translate runner-specific agent files (`agents/openai.yaml`, `agents/claude.md`) into the equivalent Houmao tool adapter or preset fields.
- Launching from template source instead of an approved Topic Agent Team Profile Bundle.
