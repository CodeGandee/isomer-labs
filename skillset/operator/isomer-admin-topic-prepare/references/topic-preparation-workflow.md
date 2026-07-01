# Topic Preparation Workflow

## Workflow

When this reference is loaded, execute the following steps in order.

1. Resolve the Project root and selected Research Topic through Project Manifest-backed context. If the topic does not exist and the user gave a concrete topic statement, create it through `isomer-admin-project-mgr` or the supported `isomer-cli project topics create <topic-id> --statement "<research topic>"` surface.
2. Verify the Topic Workspace registration and Topic Workspace Pixi binding before topic environment setup. If the Project or topic registration is unhealthy, route repair to `isomer-admin-project-mgr`.
3. Initialize or validate Workspace Runtime with `isomer-cli project runtime init --topic <topic>` and `isomer-cli project runtime validate --topic <topic>` when runtime evidence is missing or stale.
4. Resolve `topic.intent.overview`, `topic.intent.topic_env_requirements`, and `topic.env.topic_setup_target_spec` through Workspace Path Resolution before reading or writing them.
5. Delegate Topic Workspace environment setup to `isomer-srv-topic-env-setup` when topic-main readiness, Pixi configuration, external repository setup, or projection materialization is missing.
6. Query `topic.repos.main` with `isomer-cli project paths get topic.repos.main --topic <topic> --configured` and report it as the Git anchor and integration surface, not as the universal cwd for manually controlled workers.
7. Materialize or verify the standard topic record labels needed by v2 research skills, including `topic.records.artifacts`, `topic.records.tasks`, `topic.records.runs`, `topic.records.views`, and `topic.records.logs`.
8. Continue to default operator Topic Actor handling unless the user explicitly opted out.

If the user's task does not map cleanly to these steps, build a topic-preparation checklist from the selected Project, selected Research Topic, registered Topic Workspace, runtime status, topic environment evidence, path labels, blockers, and next requested workflow.

## Readiness Signals

- Registered Research Topic and Topic Workspace refs exist in the Project Manifest.
- Workspace Runtime exists and validates for the selected topic.
- Topic intent and topic environment setup evidence exist when setup is in scope.
- `topic.repos.main` resolves through Workspace Path Resolution and is ready or has a named setup blocker.
- Topic record labels resolve or have explicit missing-label blockers.
- Existing Topic Actor bindings are preserved and reported; formal team material is preserved and reported when present.

## Boundary

Common topic preparation can satisfy reusable prerequisites for manual Topic Actor research and formal Topic Team Specialization, but it does not create Topic Agent Team Profile material, Agent Team Instance records, Agent Instance records, formal Agent Workspaces, or Houmao launch material.
