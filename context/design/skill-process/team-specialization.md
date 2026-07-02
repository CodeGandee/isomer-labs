# Team Specialization Skill Process

## Purpose

This note records the intended process for **Topic Team Specialization** skill orchestration. It is a design-level process contract for aligning `isomer-admin-topic-team-specialize`, `isomer-admin-topic-mgr`, `isomer-srv-topic-env-setup`, and `isomer-srv-agent-env-setup`.

The key rule is that `isomer-admin-topic-team-specialize` is the only orchestrator across topic workspace setup, topic environment setup, and agent environment setup. Service skills and the topic manager return bounded evidence; they do not decide the next cross-skill process step.

## Concepts

- **Research Topic**: the root research problem or investigation intent that drives **Topic Team Specialization**.
- **Topic Workspace**: the project-local work area for one **Research Topic**. It owns topic runtime material, the **Topic Main Development Repository**, canonical external repositories, **Agent Workspaces**, and topic-local records.
- **Domain Agent Team Template**: the reusable research-field or method-specific team design that gets adapted for one **Research Topic**.
- **Topic Team Specialization**: the design-time process that adapts one **Domain Agent Team Template** into a topic-specific team profile. It ends before runtime launch.
- **Topic Agent Team Profile**: the topic-specific design-time team produced by **Topic Team Specialization**. It is not a running team.
- **Topic Agent Team Profile Bundle**: the fixed **Topic Workspace** directory that stores the authoritative **Topic Agent Team Profile** and related editable specialization material.
- **Topic Intent Overview**: the user-editable topic summary resolved by semantic label `topic.intent.overview`.
- **Topic Env Requirements**: the concise user-editable topic environment intent resolved by semantic label `topic.intent.topic_env_requirements`.
- **Topic Env Target Spec**: the operational topic environment setup spec resolved by semantic label `topic.env.topic_setup_target_spec`.
- **Agent Env Requirements**: the concise user-editable per-agent cwd intent resolved by semantic label `topic.intent.agent_env_requirements`.
- **Agent Env Target Spec**: the operational per-agent cwd verification spec resolved by semantic label `topic.env.agent_setup_target_spec`.
- **Topic Main Development Repository**: the topic-owned development repository for the **Topic Workspace**, resolved through semantic label `topic.repos.main`. Topic env setup creates, configures, and verifies it before agent env setup consumes it.
- **External Repository Projection**: a read-only or writable exposure of a canonical external repository inside the resolved **Topic Main Development Repository**, under `topic.repos.main.projections.readonly` or `topic.repos.main.projections.writable`, with metadata at `topic.repos.main.projections.manifest`.
- **Agent Workspace**: the per-agent work area inside a **Topic Workspace**, normally resolved through semantic label `agent.workspace`.
- **Agent Name**: the topic-local name used for default **Agent Workspace** bindings, such as `planner` or `analyst`.
- **Agent Team Instance**: the runtime team created later from a **Topic Agent Team Profile**. It is outside the setup flow described here.
- **Execution Adapter**: the launch and command-execution adapter layer used for runtime dispatch. It remains a later boundary in this document.

## High Level Process

```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant T as isomer-admin-topic-<br/>team-specialize
    participant TE as isomer-srv-<br/>topic-env-setup
    participant AE as isomer-srv-<br/>agent-env-setup
    participant F as validate-topic-team /<br/>finalize-topic-team

    U->>T: Start topic-team specialization<br/>for one Research Topic.
    T->>T: Resolve the Isomer Project<br/>and registered Topic Workspace.
    T->>T: Create or update<br/>topic.intent.overview.
    T->>T: Create topic env intent<br/>as user-editable requirements.
    T->>T: Create topic env target spec<br/>from topic env intent.
    T->>TE: Materialize topic env,<br/>topic-main, and projections.
    TE-->>T: Return Pixi, topic-main,<br/>projection evidence, blockers,<br/>and no per-agent claim.
    T->>T: Specialize the team<br/>and produce Agent Names.
    T->>T: Create agent env intent<br/>from Agent Names and cwd proof.
    T->>T: Create agent env target spec<br/>from agent env intent.
    T->>AE: Materialize agent worktrees<br/>and verify cwd readiness.
    AE-->>T: Return readiness by Agent Name,<br/>selected-agent evidence,<br/>blockers, and overall readiness.
    T->>F: Validate evidence streams<br/>and write final handoff.
    F-->>U: Return topic-team<br/>setup summary.
```

## Skill Call Graph

This graph shows the top-level skill calls used by this process. Route nodes name the operator surface or service setup stage that creates the edge.

```mermaid
flowchart TD
    classDef skill fill:#eef6ff,stroke:#2563eb,stroke-width:1.5px,color:#111827
    classDef route fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#334155

    PM["isomer-admin<br/>project-mgr"]:::skill
    TTS["isomer-admin<br/>topic-team-specialize"]:::skill
    TM["isomer-admin<br/>topic-mgr"]:::skill
    TENV["isomer-srv<br/>topic-env-setup"]:::skill
    AENV["isomer-srv<br/>agent-env-setup"]:::skill

    S0["S0<br/>specialize-team<br/>handoff to fast-forward"]:::route
    S1["S1<br/>optional topology<br/>inspection or branch helper"]:::route
    S2["S2<br/>resolve-topic-env-gate<br/>create target spec<br/>then setup-topic-env"]:::route
    S3["S3<br/>resolve-agent-env-gate<br/>create target spec<br/>then setup-agent-env"]:::route

    PM -.-> S0 -.-> TTS
    TTS --> S1 --> TM
    TTS --> S2 --> TENV
    TTS --> S3 --> AENV
```

| ID | Caller | Route | Callee | Calling condition |
| --- | --- | --- | --- | --- |
| S0 | `isomer-admin-project-mgr` | `specialize-team` handoff to `fast-forward` | `isomer-admin-topic-team-specialize` | Project-level work needs full **Topic Team Specialization** for one **Research Topic**. This is an optional entry route into the same process and should not call the internal `adapt-team-template` stage directly. |
| S1 | `isomer-admin-topic-team-specialize` | optional topology inspection or branch helper | `isomer-admin-topic-mgr` | The operator asks for read-only topology inspection, branch helper operations, boundary summaries, stale topology repair, or legacy compatibility diagnostics. The topic manager is not the canonical creator of the Topic Main Development Repository in the normal setup path. |
| S2 | `isomer-admin-topic-team-specialize` | `resolve-topic-env-gate`, create `topic.env.topic_setup_target_spec`, then `setup-topic-env` | `isomer-srv-topic-env-setup` | `topic.intent.topic_env_requirements` exists, can be created from a clear runnable target, or an explicit topic env target spec is provided. The service materializes the Topic Workspace environment, Topic Main Development Repository, canonical external repositories, external repository projections, Pixi dependencies, and verification evidence, and must not claim per-agent readiness. |
| S3 | `isomer-admin-topic-team-specialize` | `resolve-agent-env-gate`, create `topic.env.agent_setup_target_spec`, then `setup-agent-env` | `isomer-srv-agent-env-setup` | `topic.intent.agent_env_requirements` exists, can be created from requested cwd proof, or an explicit agent env target spec is provided. The service consumes topic env readiness, Topic Main Development Repository predecessor evidence, external projection evidence when needed, and authoritative **Agent Names** before creating worktrees or verifying cwd readiness. |

## Formal Skill Process

This sketch uses the Agent-Primitive Python vocabulary from `context/design/skill-pseudo-lang/definitions.md`. Python handles exact control flow and file checks. The `agent_*` calls mark semantic work, qualitative checks, and explicit cross-skill calls.

```python
from pathlib import Path


# Entry point: this operator skill owns the whole setup decision sequence.
# Example input: project_root=Path("."), user_request="Set up this topic team through agent env readiness."
# Example output: StageResult(status="ready", evidence=["topic-team finalized"])
@skill(
    name="isomer-admin-topic-team-specialize",
    description="Specialize a Research Topic team and orchestrate topic workspace, topic env, and agent env setup.",
)
def specialize_topic_team(project_root: Path, user_request: str) -> StageResult:
    # Interpret user intent semantically, but keep the resulting route as exact Python data.
    # Example input: user_request="Set up agent env after topic env is ready."
    # Example output: "setup-agent-env"
    requested_route = agent_select(
        [
            "adapt-team-template",
            "inspect-topic-workspace",
            "setup-topic-env",
            "setup-agent-env",
            "full-topic-team-setup",
        ],
        criterion="Choose the narrowest route that satisfies the user's requested topic-team setup proof.",
        context={"user_request": user_request, "project_root": project_root},
    )

    # Resolve project and topic before writing any topic-local intent.
    # Example output: StageResult(status="ready", evidence=["registered Topic Workspace: alpha"])
    project_topic = agent_do(
        "Resolve the Isomer Project, Research Topic, and registered Topic Workspace for this request.",
        context={"project_root": project_root, "user_request": user_request, "requested_route": requested_route},
        returns=StageResult,
        constraints=[
            "Use Project Manifest-backed refs.",
            "Do not select a Topic Workspace by scanning sibling directories.",
        ],
    )
    if project_topic.status in {"blocked", "failed"}:
        # Condition matched when the project, Research Topic, or registered Topic Workspace cannot be resolved.
        return project_topic

    # Create the user-editable topic overview intent before setup requirements are derived.
    # Example output: StageResult(status="ready", evidence=["topic.intent.overview"])
    topic_intent = agent_do(
        "Create or update topic.intent.overview with the topic goal, metrics, datasets, explicitly mentioned repositories, libraries, and tools.",
        context={"project_topic": project_topic, "user_request": user_request},
        returns=StageResult,
        constraints=[
            "Keep the file concise and user-editable.",
            "Avoid dependency versions unless the topic context explicitly says them.",
        ],
    )
    if topic_intent.status in {"blocked", "failed"}:
        # Condition matched when the topic overview cannot be safely created or updated.
        return topic_intent

    if requested_route == "inspect-topic-workspace":
        # Condition matched when the operator asks for optional topology inspection, branch helpers, boundary summaries, or legacy diagnostics.
        # Example output: StageResult(status="ready", evidence=["semantic path summary", "worktree state", "projection roots"])
        return agent_invoke(
            "isomer-admin-topic-mgr",
            task="Inspect prepared topic-main and Agent Workspace topology without becoming the canonical topic-main creator.",
            context={"project_topic": project_topic, "topic_intent": topic_intent, "user_request": user_request},
            returns=StageResult,
            params={
                "subcommand": "status",
                "expect": ["semantic paths", "Git state", "projection roots", "blockers", "next actions"],
                "must_not_create": ["topic.repos.main"],
                "must_not_call": ["isomer-srv-agent-env-setup"],
            },
        )

    topic_env_routes = {"setup-topic-env", "setup-agent-env", "full-topic-team-setup"}

    if requested_route in topic_env_routes:
        # Condition matched when the route needs Topic Workspace environment predecessor evidence.
        # Create high-level source intent first; the service owns operational commands and mutation.
        # Example output: StageResult(status="ready", evidence=["topic.intent.topic_env_requirements"])
        topic_env_intent = agent_do(
            "Create or update topic.intent.topic_env_requirements as concise high-level topic environment intent.",
            context={"project_topic": project_topic, "topic_intent": topic_intent, "user_request": user_request},
            returns=StageResult,
            constraints=[
                "Name what must be runnable for the topic.",
                "Keep repo, dataset, tool, and runtime needs high level.",
                "Do not write Pixi commands or implementation details into the source intent.",
            ],
        )
        if topic_env_intent.status in {"blocked", "failed"}:
            # Condition matched when topic env requirements cannot be derived from the user request or topic material.
            return topic_env_intent

        # Cross-skill call: topic env setup owns topic target-spec use, Pixi mutation, topic-main setup, external repo acquisition, projection materialization, and verification.
        # Example output: StageResult(status="ready", evidence=["topic.env.topic_setup_target_spec", "Topic Workspace Pixi readiness", "Topic Main Development Repository ready", "extern-projections.toml"])
        topic_env = agent_invoke(
            "isomer-srv-topic-env-setup",
            task="Use topic.intent.topic_env_requirements to create or validate topic.env.topic_setup_target_spec, then materialize topic env, topic-main, external repos, projections, dependencies, and verification.",
            context={"project_topic": project_topic, "topic_intent": topic_intent, "topic_env_intent": topic_env_intent},
            returns=StageResult,
            params={
                "subcommand": "setup-topic-env",
                "expect": [
                    "topic.env.topic_setup_target_spec",
                    "Topic Workspace Pixi readiness",
                    "Topic Main Development Repository Git state",
                    "external repository projection metadata",
                    "dependency and verification evidence",
                    "Topic Workspace predecessor evidence",
                ],
                "must_not_read": ["topic.intent.agent_env_requirements"],
                "must_not_write": ["topic.env.agent_setup_target_spec"],
                "must_not_call": ["isomer-srv-agent-env-setup"],
                "per_agent_readiness_status": "not_checked",
            },
        )
        if topic_env.status in {"blocked", "failed"}:
            # Condition matched when topic env setup reports blocked or failed evidence.
            return topic_env
    else:
        # Condition matched when topic env setup is outside the requested route.
        topic_env = StageResult(
            status="not_checked",
            evidence=["Topic env setup was outside the requested route."],
        )

    if requested_route == "setup-topic-env":
        # Condition matched when the selected route stops after topic env setup.
        # Return after topic env setup, explicitly preserving that per-agent readiness was out of scope.
        # Example output: StageResult(status="ready", evidence=["topic env ready", "per_agent_readiness_status: not_checked"])
        return agent_do(
            "Write a topic env setup handoff. Include topic-main and projection evidence, and state that agent env readiness was not checked.",
            context={"project_topic": project_topic, "topic_intent": topic_intent, "topic_env": topic_env},
            returns=StageResult,
        )

    team_routes = {"adapt-team-template", "setup-agent-env", "full-topic-team-setup"}

    if requested_route in team_routes:
        # Adapt the team template after topic env predecessor evidence exists when that evidence is in scope.
        # Example output: StageResult(status="ready", evidence=["Topic Agent Team Profile", "Agent Names: planner, analyst"])
        team = agent_do(
            "Adapt the selected Domain Agent Team Template for this topic and produce authoritative Agent Names when available.",
            context={"project_topic": project_topic, "topic_intent": topic_intent, "topic_env": topic_env, "requested_route": requested_route},
            returns=StageResult,
            constraints=["Do not launch runtime teams."],
        )
        if team.status in {"blocked", "failed"}:
            # Condition matched when team specialization fails or a route that needs Agent Names cannot get them.
            return team

    if requested_route == "adapt-team-template":
        # Condition matched when the explicit internal route stops after copied template adaptation.
        return agent_do(
            "Write a template-adaptation handoff summary with deferred setup evidence clearly marked.",
            context={"project_topic": project_topic, "topic_intent": topic_intent, "team": team, "topic_env": topic_env},
            returns=StageResult,
        )

    agent_env_routes = {"setup-agent-env", "full-topic-team-setup"}

    if requested_route in agent_env_routes:
        # Condition matched when the route needs per-Agent Workspace cwd readiness evidence.
        # Create high-level source intent before the agent env service derives an operational matrix.
        # Example output: StageResult(status="ready", evidence=["topic.intent.agent_env_requirements"])
        agent_env_intent = agent_do(
            "Create or update topic.intent.agent_env_requirements from authoritative Agent Names, topic intent, topic env predecessor evidence, and requested cwd proof.",
            context={"project_topic": project_topic, "topic_intent": topic_intent, "team": team, "topic_env": topic_env, "user_request": user_request},
            returns=StageResult,
            constraints=[
                "Keep the source intent concise and high level.",
                "Do not write per-agent Pixi commands into the source intent.",
            ],
        )
        if agent_env_intent.status in {"blocked", "failed"}:
            # Condition matched when agent env requirements cannot be derived from the user request or topic material.
            return agent_env_intent

        # Semantic prerequisite check: evidence sufficiency is qualitative, so ask the agent.
        # Example output: True
        agent_env_inputs_ready = agent_check(
            "Do topic.env.topic_setup_target_spec, topic-main readiness evidence, projection evidence when needed, topic.intent.agent_env_requirements, and authoritative Agent Names satisfy the prerequisites for agent env setup?",
            context={
                "project_topic": project_topic,
                "team": team,
                "topic_env": topic_env,
                "agent_env_intent": agent_env_intent,
            },
            returns=bool,
            rubric="True only when Topic Workspace env readiness, Topic Main Development Repository evidence, required projection predecessor evidence, authoritative Agent Names, and agent env source intent or explicit target spec are ready or explicitly accepted.",
        )
        if not agent_env_inputs_ready:
            # Condition matched when existing evidence is insufficient for safe agent env setup.
            return StageResult(
                status="blocked",
                blockers=["Agent env setup prerequisites are not satisfied."],
                evidence=["topic.intent.agent_env_requirements", "topic.env.topic_setup_target_spec"],
                next_action="Repair missing topic env, topic-main, projection, or Agent Name evidence before setup-agent-env.",
            )

        # Cross-skill call: agent env setup owns per-Agent Workspace worktree creation and cwd readiness, using topic-main evidence from topic env setup.
        # Example output: StageResult(status="ready", evidence=["topic.env.agent_setup_target_spec", "Agent Workspace worktrees", "overall agent readiness"])
        agent_env = agent_invoke(
            "isomer-srv-agent-env-setup",
            task="Use topic.intent.agent_env_requirements and predecessor evidence to create or validate topic.env.agent_setup_target_spec, then create Agent Workspace worktrees and verify cwd readiness.",
            context={
                "project_topic": project_topic,
                "team": team,
                "topic_env": topic_env,
                "agent_env_intent": agent_env_intent,
            },
            returns=StageResult,
            params={
                "subcommand": "setup-agent-env",
                "expect": [
                    "topic.env.agent_setup_target_spec",
                    "Topic Main Development Repository predecessor evidence consumed",
                    "projection predecessor evidence consumed when required",
                    "Agent Workspace worktrees",
                    "readiness by Agent Name",
                    "selected-agent partial evidence when scoped",
                    "overall agent readiness",
                ],
                "must_not_call": ["isomer-srv-topic-env-setup"],
                "must_not_create": ["topic.repos.main", "topic.repos.main.projections.readonly", "topic.repos.main.projections.writable"],
            },
        )
        if agent_env.status in {"blocked", "failed"}:
            # Condition matched when agent env setup reports blocked or failed evidence.
            return agent_env
    else:
        # Condition matched when agent env setup is outside the requested route.
        agent_env = StageResult(
            status="not_checked",
            evidence=["Agent env setup was outside the requested route."],
        )

    # Final semantic write-up: validate the evidence streams without changing ownership boundaries.
    # Example output: StageResult(status="ready", evidence=["topic-main evidence", "topic env", "agent env"])
    return agent_do(
        "Validate the separate evidence streams and write the topic-team finalization summary.",
        context={
            "project_topic": project_topic,
            "topic_intent": topic_intent,
            "team": team,
            "topic_env": topic_env,
            "agent_env": agent_env,
        },
        returns=StageResult,
        constraints=[
            "Preserve missing or deferred evidence as explicit blockers.",
            "Do not launch runtime teams.",
        ],
    )
```

## Skill Process Explanation

The process is a chain of readable intent and bounded service evidence. `isomer-admin-topic-team-specialize` stays in charge of the whole process, but it does not do every job itself. It writes the user-facing intent, delegates operational setup to the right service, then checks the returned evidence before moving on.

- Route and resolve the topic:
  - The operator request first becomes a concrete route, such as `full-topic-team-setup`, `setup-topic-env`, or `setup-agent-env`. Natural-language requests like `specialize <team-path> over topic <topic>` map to `full-topic-team-setup`; `adapt-team-template` is the internal static-material stage.
  - The skill resolves the <u>*Research Topic*</u> and registered <u>*Topic Workspace*</u> from Project Manifest-backed context.
  - It writes `topic.intent.overview` so later stages share the same topic goal, metrics, datasets, explicit repositories, libraries, and tools.
  - If the topic is ambiguous, this stage blocks instead of guessing.
- Specialize the team:
  - The skill applies the selected <u>*Domain Agent Team Template*</u> to the topic overview.
  - For setup routes, this happens after topic env predecessor evidence exists, so <u>*Agent Names*</u> and cwd intent can reflect the prepared topic-main repository.
  - It produces the <u>*Topic Agent Team Profile*</u> and authoritative <u>*Agent Names*</u> when the selected route needs per-agent setup.
  - This stage still stops before runtime launch. It does not create an <u>*Agent Team Instance*</u>.
- Prepare topic environment intent:
  - The skill writes `topic.intent.topic_env_requirements` as a short user-editable description of what must be runnable for the topic.
  - This source intent should mention goals, datasets, repositories, tools, and success criteria at a high level.
  - It should not contain Pixi commands, concrete install plans, or host-specific runtime wiring.
- Materialize the Topic Workspace environment:
  - `isomer-admin-topic-team-specialize` owns creating or updating `topic.env.topic_setup_target_spec` in the normal operator flow; direct service invocation may still accept an explicit target spec.
  - The target spec is where repo acquisition details, dependency plans, Pixi commands, package-source choices, expected outputs, blockers, runtime wiring, fallbacks, and execution logs belong.
  - `isomer-srv-topic-env-setup` prepares the <u>*Topic Workspace*</u> environment, the <u>*Topic Main Development Repository*</u>, canonical external repositories, <u>*External Repository Projections*</u>, Pixi dependencies, and verification evidence.
  - It returns predecessor evidence and must leave per-agent readiness as `not_checked`.
- Prepare agent environment intent:
  - The skill writes `topic.intent.agent_env_requirements` only after topic env predecessor evidence and authoritative <u>*Agent Names*</u> are known or intentionally accepted.
  - This source intent describes what each <u>*Agent Workspace*</u> cwd must be able to run.
  - It stays high level and user-editable; the service later derives the operational matrix.
- Materialize Agent Workspace readiness:
  - `isomer-admin-topic-team-specialize` owns creating or updating `topic.env.agent_setup_target_spec` in the normal operator flow; direct service invocation may still accept an explicit target spec.
  - The target spec is the per-agent cwd verification matrix.
  - `isomer-srv-agent-env-setup` consumes topic env readiness, <u>*Topic Main Development Repository*</u> predecessor evidence, required <u>*External Repository Projection*</u> evidence, and authoritative <u>*Agent Names*</u>.
  - The service creates or validates <u>*Agent Workspace*</u> worktrees and reports readiness by <u>*Agent Name*</u> and overall readiness.
- Inspect optional topology:
  - `isomer-admin-topic-mgr` remains available for read-only topology inspection, branch helper operations, boundary summaries, stale topology repair, and legacy compatibility diagnostics.
  - It is not the normal creator of the <u>*Topic Main Development Repository*</u> and should not replace topic env or agent env setup.
- Validate and finalize:
  - Team specialization validates topic overview, topic env evidence, topic-main/projection evidence, and agent env evidence as separate streams.
  - The final handoff should say what is ready, what was intentionally not checked, and what remains blocked.
  - Runtime launch, Houmao launch, <u>*Agent Team Instance*</u> creation, and <u>*Execution Adapter*</u> work remain outside this setup process.

## Evidence Handoffs

| Producing skill | Evidence | Consuming stage |
| --- | --- | --- |
| `isomer-admin-topic-team-specialize` | `topic.intent.overview` | `resolve-topic-env-gate`, `adapt-team-template`, validation, finalization |
| `isomer-admin-topic-team-specialize` | `topic.intent.topic_env_requirements` | `isomer-srv-topic-env-setup setup-topic-env` |
| `isomer-srv-topic-env-setup` | `topic.env.topic_setup_target_spec`, Pixi binding, Topic Main Development Repository Git state, projection metadata, dependency/enclosure evidence, verification commands, `per_agent_readiness_status: not checked` when relevant | `resolve-agent-env-gate`, `isomer-srv-agent-env-setup require-topic-env-ready`, `isomer-srv-agent-env-setup require-topic-main-ready`, validation, finalization |
| `isomer-admin-topic-team-specialize` | `topic.intent.agent_env_requirements` | `isomer-srv-agent-env-setup setup-agent-env` |
| `isomer-srv-agent-env-setup` | `topic.env.agent_setup_target_spec`, Agent Workspace worktrees, projection predecessor evidence consumed when required, readiness by **Agent Name**, selected-agent partial evidence, overall readiness | `isomer-admin-topic-team-specialize validate-topic-team`, finalization, later runtime handoff |
| `isomer-admin-topic-mgr` | optional topology inspection, branch helper output, boundary summaries, stale topology repair, legacy compatibility diagnostics | operator troubleshooting and validation context only |
