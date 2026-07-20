# Show Core Entrypoint Command Map

## Workflow

1. Load this exhaustive map only for `show-command-map`, `help`, or an explicit complete-output request.
2. Present every current `isomer-op-entrypoint` public command exactly once in manifest order.
3. Explain that the welcome-style commands delegate read-only guidance to `$isomer-op-welcome` during the compatibility window.
4. Preserve the task context in the exact public invocation and explain mutation posture without executing it.

If the requested goal does not map cleanly to one command, use the native planning tool to compare this map with the user's context, then recommend a concrete task-only `$isomer-op-entrypoint` request or ask for the missing decision.

## Complete Command Map

| Command | When to Use | Exact Public Invocation |
| --- | --- | --- |
| `help` | Use when an established entrypoint prompt asks for public usage help; the entrypoint delegates the read-only result to welcome. | `$isomer-op-entrypoint use help to explain the public execution surface` |
| `show-options` | Use when an established entrypoint prompt asks for typical core workflows. | `$isomer-op-entrypoint use show-options to compare typical Isomer workflows` |
| `show-extensions` | Use when an established entrypoint prompt asks which packaged research extensions exist. | `$isomer-op-entrypoint use show-extensions to explain packaged extensions` |
| `choose-path` | Use when an established entrypoint prompt asks for a read-only route recommendation. | `$isomer-op-entrypoint use choose-path to map the supplied goal to one public route` |
| `show-skill-map` | Use for compatibility with the former core skill-map command; the read-only result comes from welcome's command guidance. | `$isomer-op-entrypoint use show-skill-map to show the compatibility route map` |
| `show-command-map` | Use when the complete current entrypoint command inventory is needed. | `$isomer-op-entrypoint use show-command-map to list every public command` |
| `next-step` | Use when read-only Project or extension context should inform one recommendation. | `$isomer-op-entrypoint use next-step to recommend the next public command` |
| `start-research-manually` | Use when a newcomer needs human-orchestrated Research Topic setup guidance. | `$isomer-op-entrypoint use start-research-manually to explain manual research setup` |
| `start-research-by-agent-team` | Use when a newcomer needs formal Agent Team setup guidance. | `$isomer-op-entrypoint use start-research-by-agent-team to explain formal team setup` |
| `start-deepsci-research` | Use when a newcomer needs DeepSci orientation before concrete research execution. | `$isomer-op-entrypoint use start-deepsci-research to explain the DeepSci path` |
| `start-kaoju-survey` | Use when a newcomer needs Kaoju orientation before concrete survey execution. | `$isomer-op-entrypoint use start-kaoju-survey to explain the Kaoju path` |
| `project` | Use for Project initialization, validation, context, runtime, cleanup, or relocation work. | `$isomer-op-entrypoint use project to <task>` |
| `gui` | Use for Project Web GUI lifecycle, refresh, debugging, troubleshooting, or Backend API reference. | `$isomer-op-entrypoint use gui to <task>` |
| `identity` | Use to inspect, switch, reset, or act once under a Topic Actor or Agent posture. | `$isomer-op-entrypoint use identity to <task>` |
| `system-skills` | Use to detect, install, upgrade, inspect, reconcile, migrate, or repair packaged skill extensions. | `$isomer-op-entrypoint use system-skills to <task>` |
| `toolbox` | Use for project-local Toolbox, callback, insertion-point, and Runtime Param work. | `$isomer-op-entrypoint use toolbox to <task>` |
| `topic-create` | Use to turn empty or partial Project state into a prepared Research Topic and Topic Workspace. | `$isomer-op-entrypoint use topic-create to <task>` |
| `topic-manage` | Use to manage an initialized Research Topic after Topic Creator handoff. | `$isomer-op-entrypoint use topic-manage to <task>` |
| `topic-team` | Use only for explicit or contextually established formal Agent Team specialization work. | `$isomer-op-entrypoint use topic-team to <task>` |
| `package-specifics` | Use when a named package needs source, variant, compatibility, or installation-caveat guidance. | `$isomer-op-entrypoint use package-specifics to <task>` |
| `tool-packs` | Use when the user explicitly asks for a named installable toolset and its verification contract. | `$isomer-op-entrypoint use tool-packs to <task>` |

The first eleven commands are retained read-only welcome compatibility routes. Concrete mutation remains with the execution commands or a task-only entrypoint request.
