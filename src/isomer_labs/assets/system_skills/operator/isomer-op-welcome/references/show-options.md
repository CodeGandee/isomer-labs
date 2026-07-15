# Show Options

## Workflow

1. Print the visible usage paths first, beginning with research setup: `start-research-manually` and `start-research-by-agent-team`.
2. Print the optional research paradigm paths `start-deepsci-research` and `start-kaoju-survey`; explain that paradigm and execution topology are independent choices.
3. Show Project operation routes for Project lifecycle, Topic management, Project Web GUI, identity posture, and formal Agent Team work.
4. Show customization routes for system-skill extensions and project-local Toolboxes, keeping their ownership and meanings distinct.
5. Offer `Use $isomer-op-entrypoint` when the user already has a concrete task and wants Isomer to route and proceed.
6. Ask the user to choose a visible path, inspect extensions, describe a goal, or invoke the named owner skill directly.

If the user's task does not map cleanly to these steps, use your native planning tool to build the shortest helpful menu from the visible research paths, package-catalog extension metadata, active owner skills, and guardrails, then print that menu without mutating state.

## Start and Organize Research

| User Goal | Owner Skill | Direct Invocation |
| --- | --- | --- |
| Start research manually with human-orchestrated Topic Actors. | `isomer-op-topic-creator` | `Use $isomer-op-topic-creator fast-forward` or `Use $isomer-op-topic-creator step-by-step`. |
| Start research by formal Agent Team from a Domain Agent Team Template. | `isomer-op-topic-team-specialize` | `Use $isomer-op-topic-team-specialize fast-forward`. |

## Choose an Optional Research Paradigm

| User Goal | Entry Skill | Safe Route |
| --- | --- | --- |
| Develop or evaluate a hypothesis with experiments, analysis, decisions, writing, review, rebuttal, or submission. | `isomer-deepsci-pipeline` | Select `start-deepsci-research`; use `$isomer-op-entrypoint` with the concrete goal when readiness is not already established. |
| Survey literature, codebases, datasets, or models; run bounded trials or comparisons; produce a paper or wiki. | `isomer-kaoju-pipeline` | Select `start-kaoju-survey`; use `$isomer-op-entrypoint` with the concrete goal when readiness is not already established. |

These rows describe package-catalog capabilities, not proof of current host installation. Use `show-extensions` for catalog and Project declaration state, and `isomer-op-system-skill-mgr` for host usability, installation, compatibility, or repair.

## Operate the Project

Use these routes for Project setup or checks, Topic management, identity posture, Project Web GUI work, and contextually established Topic Team work.

| User Goal | Owner Skill | Direct Invocation |
| --- | --- | --- |
| Initialize or check an Isomer Project, list topics, inspect context, or prepare runtime. | `isomer-op-project-mgr` | `Use $isomer-op-project-mgr check-project`, `list-topics`, or the needed Project subcommand. |
| Start, inspect, refresh, debug, or troubleshoot the Project Web GUI, or look up GUI Backend API routes. | `isomer-op-gui-mgr` | `Use $isomer-op-gui-mgr help`, `launch`, `status`, `api-reference`, `refresh-records`, or `troubleshoot`. |
| Act from a selected Topic Actor or Agent workspace cwd for takeover or one-time prompt execution. | `isomer-op-switch-identity` | `Use $isomer-op-switch-identity switch` or `Use $isomer-op-switch-identity act-as`. |
| Manage an initialized Research Topic, Topic Actors, package mutation, environment verification, reset checkpoints, or diagnostics. | `isomer-op-topic-mgr` | `Use $isomer-op-topic-mgr status` or a scoped initialized-topic subcommand. |
| Need Houmao adapter support during Project or formal Agent Team work. | Owning operator workflow | Use `isomer-op-project-mgr` for Project bootstrap or checks. Use `isomer-op-topic-team-specialize` only when the prompt or authoritative context establishes a formal Agent Team target. |

## Extend and Customize

| User Goal | Owner Skill | Direct Invocation |
| --- | --- | --- |
| Detect, reconcile, install, inspect, or repair optional system-skill extensions such as DeepSci or Kaoju. | `isomer-op-system-skill-mgr` | `Use $isomer-op-system-skill-mgr detect-extensions`, `status`, `install-extension`, or `repair`. |
| Create, convert, install, inspect, update, disable, uninstall, or explain project-local Toolboxes, callback insertion points, callback declarations, or Toolbox Runtime Params. | `isomer-op-toolbox-mgr` | `Use $isomer-op-toolbox-mgr help` or a specific Toolbox subcommand. |

A system-skill extension installs an optional agent-skill family. A Toolbox provides project-local callback and Runtime Param customization. The `isomer-cli ext` namespace exposes runtime or compatibility commands and is not the system-skill installer.

## Route a Concrete Task

When the user already knows the desired outcome, recommend `Use $isomer-op-entrypoint` with the concrete task. The entrypoint selects one owner skill, extension skill, or CLI family and proceeds under that route's readiness and mutation rules. The welcome skill itself remains read-only.

Do not list retired operator compatibility skills as active invocations. Do not list service skills such as `isomer-srv-houmao-interop` as direct first-click owner routes. Mention `isomer-misc-tool-packs` only when the user explicitly asks for installable toolsets. Do not infer a formal Agent Team from generic topic preparation, launch-facing work, readiness gaps, missing summaries, or missing Agent Workspaces.
