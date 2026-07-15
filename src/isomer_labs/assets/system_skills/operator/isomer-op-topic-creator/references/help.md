# Help

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Print what `isomer-op-topic-creator` does: it is the front door for creating, initializing, resuming, or repairing a Research Topic until the Topic Workspace readiness summary is written or blockers are reported.
2. Print required inputs: Project root or init permission, concrete Research Topic statement or registered ref, mutation approval, requested Topic Actors beyond `operator`, and optional default-operator opt-out.
3. State the mode default: if the user asks to create, initialize, prepare, or start a topic without saying `fast-forward`, fully automatic, `step-by-step`, manual lower-level control, `run-to`, a stop-before/exclusion phrase, or another named mode, route to `run-to define-topic-env` with the `define-topic-env` target included by default. Mention that `clarify-research-intent` is available afterward for interactive refinement.
4. Print the subcommand tables with each public subcommand's functionality.
5. Explain the readiness ladder: Project, topic input resolution, topic registration, `topic.intent.overview`, Workspace Runtime, `topic.intent.topic_env_requirements`, topic environment and `topic.repos.main`, `topic.intent.actor_definitions`, Topic Actors and `topic.env.actor_env_gates`, actor onboarding context, and `finalize` writing `topic.workspace.summary`.
6. State the output contract and lower-level delegation guardrails.

If the user's task does not map cleanly to these steps, print the closest subcommand names and ask for the missing topic statement, Project root, actor roster, or mutation approval.

## Subcommand Functionalities

### Procedural Subcommands

| Subcommand | Functionality |
| --- | --- |
| `create-research-intent` | Create or update `topic.intent.overview` from the canonical template in `templates/topic-overview.md`; strip `>` example blocks and leave empty `Topic Breakdown` subsections for the user. The template uses `Research Topic`, `Motivation`, `Topic Breakdown` (`Do's`/`Don'ts`), `Expected Outcome`, and `Related Links`. The file resolves by default to `<topic-workspace>/intent/src/topic-overview.md`. |
| `define-topic-env` | Create or refine `topic.intent.topic_env_requirements`, wait for user verification unless in `fast-forward`, and report assumptions before setup. |
| `setup-topic-env` | Read the verified or fast-forward accepted topic env gate, derive `topic.env.topic_setup_target_spec`, and prepare topic environment readiness, `topic.repos.main`, and projection predecessor evidence through service setup. |
| `define-actors` | Create or refine `topic.intent.actor_definitions`, including each actor's duty, intended usage, and source env gate; default to the `operator` actor when details are absent. |
| `setup-actors` | Create or validate Topic Actors and Topic Actor Workspaces through Topic Manager actor topology, generate `topic.env.actor_env_gates`, verify derived actor env gates from actor cwd, and report actor onboarding context. |
| `finalize` | Validate Topic Workspace preparation, write `topic.workspace.summary`, and print ready, verified, blocked, and skipped state. |

### Helper Subcommands

| Subcommand | Functionality |
| --- | --- |
| `ensure-project` | Initialize or validate the Isomer Project through `isomer-op-project-mgr` or supported `isomer-cli project ...` commands. |
| `resolve-topic-input` | Resolve concrete topic source material, derive or confirm topic id, and identify the Topic Workspace candidate without writing intent files. |
| `register-topic` | Create or validate Research Topic and Topic Workspace registration through Project Manifest-backed CLI/API surfaces. |
| `init-runtime` | Initialize or validate Workspace Runtime for the selected Research Topic. |

### Misc Subcommands

| Subcommand | Functionality |
| --- | --- |
| `help` | Print what this skill does, required inputs, subcommand functionalities, outputs, and guardrails. |
| `fast-forward` | Run the end-to-end path from empty or partial Project state to `finalize` only when the user explicitly asks for fully automatic or fast-forward execution. |
| `step-by-step` | Guided mode for explicit step-by-step requests. Run the same main workflow as `fast-forward`, preview every step, show option tables for choices, and wait for user acknowledgement. |
| `run-to` | Run the main workflow through a selected procedural subcommand by default; stop before it only on explicit wording such as `before <target>`, `stop before <target>`, `excluding <target>`, or `up to but not including <target>`. |
| `status` | Report current readiness stage, ready evidence, summary freshness, blockers, and skipped stages. |
| `repair` | Resume from the first blocked or stale stage without rerunning ready destructive or expensive work. |
| `clarify-research-intent` | Interactively refine an existing `topic.intent.overview` by walking the `Research Topic`, `Motivation`, `Topic Breakdown` (`Do's`/`Don'ts`), `Expected Outcome`, and `Related Links` sections with the user and integrating answers directly into the file. |

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

Essential Output naturally summarizes the outcome, Project root, Research Topic and Topic Workspace, Topic Main Development Repository readiness, Workspace Runtime, Topic Actor roster and workspaces, actor onboarding, summary freshness, ready surfaces, verified checks, skipped stages, and blockers.

Complete Output adds commands run, semantic labels, path sources, delegated owner evidence, `topic.intent.overview`, `topic.intent.topic_env_requirements`, `topic.intent.actor_definitions`, `topic.env.actor_env_gates`, topic environment setup evidence, actor binding JSON, actor onboarding evidence, summary evidence, skipped stages, and blockers.

## Operational Contract

- Orchestrate existing owners rather than replace them. Project lifecycle belongs to `isomer-op-project-mgr`, topic environment setup belongs to `isomer-srv-topic-env-setup`, Topic Actor topology belongs to `isomer-op-topic-mgr`, and formal team specialization belongs to `isomer-op-topic-team-specialize`. Terminal Topic Creator output reports readiness and blockers without routing to a next research command.
