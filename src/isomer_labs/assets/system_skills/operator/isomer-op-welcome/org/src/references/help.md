---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Isomer Operator Welcome Help

## Workflow

1. Describe the protected `welcome` member as the read-only capability menu and path chooser exposed through `$isomer-op-entrypoint`.
2. List the visible research paths `start-research-manually`, `start-research-by-agent-team`, `start-deepsci-research`, and `start-kaoju-survey`.
3. List the routing and support subcommands `help`, `show-options`, `show-extensions`, `choose-path`, `show-skill-map`, and `next-step`.
4. Name the public core skill `$isomer-op-entrypoint` and its active parent-scoped routes: `project`, `system-skills`, `gui`, `identity`, `toolbox`, `topic-create`, `topic-manage`, and `topic-team`.
5. Explain that DeepSci and Kaoju are optional system-skill extension paradigms, while manual versus Agent Team research selects execution topology.
6. State that the welcome member is read-only and invite the user to choose a path, inspect extensions, or describe a concrete task for `$isomer-op-entrypoint`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a bounded welcome response from the visible research paths, active operator routes, extension state distinctions, output contract, and guardrails, then recommend one safe next route or ask for the missing decision.

## Visible Research Paths

| Subcommand | Purpose | Owner or Entry Skill |
| --- | --- | --- |
| `start-research-manually` | Prepare a Research Topic for human-orchestrated research with Topic Actors. | `isomer-op-entrypoint->topic-create` |
| `start-research-by-agent-team` | Specialize a Domain Agent Team Template over a Research Topic. | `isomer-op-entrypoint->topic-team` |
| `start-deepsci-research` | Develop or evaluate a hypothesis through a production research loop. | `isomer-ext-deepsci-entrypoint` after extension and workspace readiness |
| `start-kaoju-survey` | Survey literature, code, datasets, or models with evidence, trials, comparisons, paper production, or wiki export. | `isomer-ext-kaoju-entrypoint` after extension and workspace readiness |

DeepSci or Kaoju selects a research paradigm. Manual or Agent Team setup selects execution topology. The user may combine one choice from each dimension when the selected paradigm and workspace are ready.

## Active Operator Routes

| User Goal | Route |
| --- | --- |
| Give Isomer a concrete task and have it select one owner route, extension skill, or CLI family and proceed. | `$isomer-op-entrypoint` with the concrete task. |
| Detect, reconcile, install, upgrade, inspect, or repair optional system-skill extensions. | `$isomer-op-entrypoint use system-skills to <task>`. |
| Initialize, validate, inspect, clean up, or route Project lifecycle work. | `$isomer-op-entrypoint use project to <task>`. |
| Start, inspect, refresh, debug, troubleshoot, or look up backend APIs for the Project Web GUI. | `$isomer-op-entrypoint use gui to <task>`. |
| Act from a selected Topic Actor or Agent workspace cwd. | `$isomer-op-entrypoint use identity to <task>`. |
| Create, convert, install, inspect, update, disable, uninstall, or explain project-local Toolboxes, callback insertion points, callback declarations, or Toolbox Runtime Params. | `$isomer-op-entrypoint use toolbox to <task>`. |
| Create or prepare a blank or partial Research Topic. | `$isomer-op-entrypoint use topic-create to <task>`. |
| Manage an initialized Research Topic, Topic Actors, packages, environments, reset checkpoints, or diagnostics. | `$isomer-op-entrypoint use topic-manage to <task>`. |
| Specialize, validate, approve, materialize, repair, or launch a contextually established formal Agent Team. | `$isomer-op-entrypoint use topic-team to <task>` with the formal-team target. |

## Routing and Support Subcommands

| Subcommand | Purpose | Produces |
| --- | --- | --- |
| `help` | Print usage, visible paths, operator routes, outputs, and guardrails. | Help output. |
| `show-options` | Print the default grouped capability menu. | Concise action menu. |
| `show-extensions` | Inspect package-catalog extensions and Project declarations without claiming host usability. | Extension capability and state summary. |
| `choose-path` | Interpret an ambiguous goal and recommend one visible path or operator route. | Route, safe invocation, blockers, and next action. |
| `show-skill-map` | Show direct invocation guidance. | Compact intent-to-route map. |
| `next-step` | Inspect Project context with read-only commands when requested. | Recommended route plus blockers. |

## Extension Vocabulary

- A system-skill extension is an optional installed public pack such as DeepSci or Kaoju. `isomer-op-entrypoint->system-skills` owns its availability and lifecycle.
- A Toolbox is project-local callback and Runtime Param customization. `isomer-op-entrypoint->toolbox` owns it.
- The `isomer-cli ext` namespace exposes runtime and compatibility commands. It does not install system-skill extensions.

Catalog-known, Project-declared, entrypoint-seen, pack-integrity-verified, and current-session-usable are different states. Do not call an extension complete or usable from catalog, declaration, or name-only live-inventory evidence.

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

### Essential Output

Explain naturally how the user's goal was understood, then give the recommended workflow, owner or entry skill, safe first command, relevant extension state, blockers, and next action.

### Complete Output

Group the full explanation by context evidence, read-only commands, extension catalog and declaration evidence, alternate routes, routing rationale, and retired route exclusions.
