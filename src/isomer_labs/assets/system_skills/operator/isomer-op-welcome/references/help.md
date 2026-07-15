# Isomer Operator Welcome Help

## Workflow

1. Describe `isomer-op-welcome` as the read-only capability menu and path chooser for Isomer Labs.
2. List the visible research paths `start-research-manually`, `start-research-by-agent-team`, `start-deepsci-research`, and `start-kaoju-survey`.
3. List the routing and support subcommands `help`, `show-options`, `show-extensions`, `choose-path`, `show-skill-map`, and `next-step`.
4. Name the active operator routes: `isomer-op-entrypoint`, `isomer-op-project-mgr`, `isomer-op-system-skill-mgr`, `isomer-op-gui-mgr`, `isomer-op-switch-identity`, `isomer-op-toolbox-mgr`, `isomer-op-topic-creator`, `isomer-op-topic-mgr`, and `isomer-op-topic-team-specialize`.
5. Explain that DeepSci and Kaoju are optional system-skill extension paradigms, while manual versus Agent Team research selects execution topology.
6. State that the welcome skill is read-only and invite the user to choose a path, inspect extensions, describe a concrete task for `isomer-op-entrypoint`, or invoke a named owner directly.

If the user's task does not map cleanly to these steps, use your native planning tool to build a bounded welcome response from the visible research paths, active operator routes, extension state distinctions, output contract, and guardrails, then recommend one safe next route or ask for the missing decision.

## Visible Research Paths

| Subcommand | Purpose | Owner or Entry Skill |
| --- | --- | --- |
| `start-research-manually` | Prepare a Research Topic for human-orchestrated research with Topic Actors. | `isomer-op-topic-creator` |
| `start-research-by-agent-team` | Specialize a Domain Agent Team Template over a Research Topic. | `isomer-op-topic-team-specialize` |
| `start-deepsci-research` | Develop or evaluate a hypothesis through a production research loop. | `isomer-deepsci-pipeline` after extension and workspace readiness |
| `start-kaoju-survey` | Survey literature, code, datasets, or models with evidence, trials, comparisons, paper production, or wiki export. | `isomer-kaoju-pipeline` after extension and workspace readiness |

DeepSci or Kaoju selects a research paradigm. Manual or Agent Team setup selects execution topology. The user may combine one choice from each dimension when the selected paradigm and workspace are ready.

## Active Operator Routes

| User Goal | Route |
| --- | --- |
| Give Isomer a concrete task and have it select one owner skill, extension skill, or CLI family and proceed. | `Use $isomer-op-entrypoint` with the concrete task. |
| Detect, reconcile, install, inspect, or repair optional system-skill extensions. | `Use $isomer-op-system-skill-mgr detect-extensions`, `status`, `install-extension`, or `repair`. |
| Initialize, validate, inspect, clean up, or route Project lifecycle work. | `Use $isomer-op-project-mgr` with the applicable subcommand. |
| Start, inspect, refresh, debug, troubleshoot, or look up backend APIs for the Project Web GUI. | `Use $isomer-op-gui-mgr help` or the applicable GUI subcommand. |
| Act from a selected Topic Actor or Agent workspace cwd. | `Use $isomer-op-switch-identity switch` or `act-as`. |
| Create, convert, install, inspect, update, disable, uninstall, or explain project-local Toolboxes, callback insertion points, callback declarations, or Toolbox Runtime Params. | `Use $isomer-op-toolbox-mgr help` or a specific Toolbox subcommand. |
| Create or prepare a blank or partial Research Topic. | `Use $isomer-op-topic-creator fast-forward` or `step-by-step`. |
| Manage an initialized Research Topic, Topic Actors, packages, environments, reset checkpoints, or diagnostics. | `Use $isomer-op-topic-mgr status` or a scoped subcommand. |
| Specialize, validate, approve, materialize, repair, or launch a contextually established formal Agent Team. | `Use $isomer-op-topic-team-specialize` with the formal-team target. |

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

- A system-skill extension is an optional installed agent-skill family such as DeepSci or Kaoju. `isomer-op-system-skill-mgr` owns its availability and lifecycle.
- A Toolbox is project-local callback and Runtime Param customization. `isomer-op-toolbox-mgr` owns it.
- The `isomer-cli ext` namespace exposes runtime and compatibility commands. It does not install system-skill extensions.

Catalog-known, Project-declared, and host-usable are different states. Do not call an extension installed or usable from catalog or declaration evidence alone.

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

### Essential Output

Explain naturally how the user's goal was understood, then give the recommended workflow, owner or entry skill, safe first command, relevant extension state, blockers, and next action.

### Complete Output

Group the full explanation by context evidence, read-only commands, extension catalog and declaration evidence, alternate routes, routing rationale, and retired route exclusions.
