# Help

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Print what `isomer-admin-topic-creator` does: it is the front door for creating, initializing, resuming, or repairing a Research Topic until the Topic Workspace is ready for manual v2 research.
2. Print required inputs: Project root or init permission, concrete Research Topic statement or registered ref, mutation approval, requested Topic Actors beyond `operator`, optional default-operator opt-out, and selected v2 research route when known.
3. Print the subcommand tables with each public subcommand's functionality.
4. Explain the readiness ladder: Project, topic input resolution, topic registration, `topic.intent.overview`, Workspace Runtime, `topic.intent.topic_env_requirements`, topic environment and `topic.repos.main`, `topic.intent.actor_definitions`, Topic Actors and `topic.env.actor_env_gates`, v2 research bootstrap, start packs, and final handoff.
5. State the output contract and lower-level delegation guardrails.

If the user's task does not map cleanly to these steps, print the closest subcommand names and ask for the missing topic statement, Project root, actor roster, or mutation approval.

## Subcommand Functionalities

### Procedural Subcommands

| Subcommand | Functionality |
| --- | --- |
| `create-research-intent` | Create or update only `topic.intent.overview`, which resolves by default to `<topic-workspace>/intent/src/topic-overview.md`. |
| `define-topic-env` | Create or refine `topic.intent.topic_env_requirements`, wait for user verification unless in `fast-forward`, and report assumptions before setup. |
| `setup-topic-env` | Read the verified or fast-forward accepted topic env gate, derive `topic.env.topic_setup_target_spec`, and prepare topic environment readiness, `topic.repos.main`, and projection predecessor evidence through service setup. |
| `define-actors` | Create or refine `topic.intent.actor_definitions`, including each actor's duty, intended usage, and source env gate; default to the `operator` actor when details are absent. |
| `setup-actors` | Create or validate Topic Actors and Topic Actor Workspaces through Topic Workspace Manager actor topology, generate `topic.env.actor_env_gates`, and verify derived actor env gates from actor cwd. |
| `start-manual-research` | Produce start-pack records, actor-local pointers, actor cwd instructions, selected v2 skills, and accepted-artifact recording commands. |

### Helper Subcommands

| Subcommand | Functionality |
| --- | --- |
| `ensure-project` | Initialize or validate the Isomer Project through `isomer-admin-project-mgr` or supported `isomer-cli project ...` commands. |
| `resolve-topic-input` | Resolve concrete topic source material, derive or confirm topic id, and identify the Topic Workspace candidate without writing intent files. |
| `register-topic` | Create or validate Research Topic and Topic Workspace registration through Project Manifest-backed CLI/API surfaces. |
| `init-runtime` | Initialize or validate Workspace Runtime for the selected Research Topic. |
| `bootstrap-research` | Run or validate `isomer-rsch-workspace-mgr-v2` base topic and Topic Actor readiness. |

### Misc Subcommands

| Subcommand | Functionality |
| --- | --- |
| `help` | Print what this skill does, required inputs, subcommand functionalities, outputs, and guardrails. |
| `fast-forward` | Run the end-to-end path from empty or partial Project state to manual-research-ready Topic Workspace. |
| `status` | Report current readiness stage, ready evidence, blockers, skipped stages, and next subcommand. |
| `repair` | Resume from the first blocked or stale stage without rerunning ready destructive or expensive work. |

## Output Contract

Default to **Essential Output** in chat. Print **Complete Output** only when the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output.

Essential Output reports `status`, Project root, Research Topic ref, Topic Workspace ref, `topic.repos.main` readiness, Workspace Runtime status, Topic Actor roster, each selected actor cwd, v2 bootstrap status, start-pack record refs, blockers, and next action.

Complete Output adds commands run, semantic labels, path sources, delegated owner evidence, `topic.intent.overview`, `topic.intent.topic_env_requirements`, `topic.intent.actor_definitions`, `topic.env.actor_env_gates`, topic environment setup evidence, actor binding JSON, placeholder binding entrypoints, storage recording command shapes, start-pack metadata, actor-local pointer paths, and repair routes.

## Guardrails

This skill orchestrates existing owners rather than replacing them. Project lifecycle belongs to `isomer-admin-project-mgr`, topic environment setup belongs to `isomer-srv-topic-env-setup`, Topic Actor topology belongs to `isomer-admin-topic-workspace-mgr`, research bootstrap belongs to `isomer-rsch-workspace-mgr-v2`, compatibility start-pack finalization may use `isomer-admin-manual-research-session`, and formal team specialization belongs to `isomer-admin-topic-team-specialize`.
