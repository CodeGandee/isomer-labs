# Manual Research Session

## Workflow

When this reference is loaded, execute the following steps in order.

1. Read or request prepared-topic evidence from `isomer-admin-topic-prepare`: Research Topic ref, Topic Workspace ref, Workspace Runtime validation, topic environment readiness, `topic.repos.main` readiness, topic record label readiness, current Topic Actor roster, and operator opt-out status.
2. Preserve optional formal team material if it exists, but do not require it. Report Topic Agent Team Profile, Agent Team Instance, and Agent Workspace refs only as optional coexistence context.
3. Check the selected v2 research skill route and whether research bootstrap has already produced current `<RSCH_WORKSPACE_CONTEXT>`, `<RSCH_STORAGE_LABEL_PLAN>`, `<RSCH_PLACEHOLDER_BINDING_REGISTRY>`, `<RSCH_AGENT_ACCESS_PLAN>`, and `<RSCH_BOOTSTRAP_VALIDATION_REPORT>` records.
4. Stop with a repairable blocker when base topic readiness is missing. Route common blockers to `isomer-admin-topic-prepare`, topic-main or topic env blockers to `isomer-srv-topic-env-setup`, actor topology blockers to `isomer-admin-topic-workspace-mgr`, and research storage/bootstrap blockers to `isomer-rsch-workspace-mgr-v2`.
5. Continue to actor roster resolution only when the topic layer is concrete enough that actors can read and write accepted artifacts through storage bindings.

If the user's task does not map cleanly to these steps, summarize the missing readiness signal and name the owning repair workflow.

## Minimal Required Readiness

- Registered Research Topic and Topic Workspace refs.
- Initialized and valid Workspace Runtime.
- Topic overview and topic environment readiness when setup is in scope.
- Ready `topic.repos.main` as the Git anchor and integration surface.
- Materialized or explicitly blocked topic research record labels.
- Skill-local `placeholder-bindings.md` guidance for selected v2 skills.
- Selected Topic Actor bindings and `topic.actors.workspace` readiness for every worker that will run.
