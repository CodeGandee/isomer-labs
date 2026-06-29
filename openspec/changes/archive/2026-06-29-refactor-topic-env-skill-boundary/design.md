## Context

The current service skill boundary is overloaded. `isomer-srv-topic-env-setup` is intended to prepare a selected Topic Workspace Pixi environment from `user-intent/src/env-gate.md`, but its top-level text and reference pages also mention downstream per-Agent Workspace verification, package-source decisions, NVIDIA channel policy, and Service Team routing. Those concerns are real, but they belong to different owners.

The domain model already separates the filesystem surfaces. A Topic Workspace owns the topic-level Pixi environment, Topic Agent Team Profile Bundle, Topic Main Repository, Agent Workspaces, Workspace Runtime, records, and tmp surfaces. An Agent Workspace is a per-agent work area inside a Topic Workspace. Topic Workspace readiness can be predecessor evidence for Agent Workspace setup, but it is not proof that each Agent Workspace cwd can run `agent-env-gate.md`.

The existing capability specs already encode most of the desired split: `isomer-service-env-setup-skill` owns `env-gate.md`, `isomer-env-gate.md`, Topic Workspace Pixi mutation, dependency enclosure, and topic-root verification; `isomer-agent-env-setup-service-skill` owns `agent-env-gate.md`, `isomer-agent-env-gate.md`, authoritative Agent Names, Topic Main Repository and worktree setup, and per-agent cwd verification. This change tightens the skill texts, call graph, and operator orchestration docs so they express that split consistently.

## Goals / Non-Goals

**Goals:**

- Make `isomer-srv-topic-env-setup` stop at Topic Workspace predecessor readiness and never appear to own Agent Workspace readiness.
- Make `isomer-srv-agent-env-setup` the sole owner of `agent-env-gate.md`, `isomer-agent-env-gate.md`, per-Agent Workspace cwd verification, and overall Agent Workspace readiness.
- Keep operator orchestration explicit: `isomer-admin-topic-team-specialize` decides when to call topic setup versus agent setup, while `isomer-admin-topic-workspace-mgr` owns Git topology when requested.
- Reduce embedded package-source and CUDA/NVIDIA policy in topic env setup by routing those choices through `isomer-srv-resolve-pkg-repo` and `isomer-misc-nvidia-tools` when they are materially needed.
- Update `skillset/callgraph.md` so it no longer shows `isomer-srv-topic-env-setup` calling `isomer-srv-agent-env-setup` as a responsibility edge.

**Non-Goals:**

- Do not change the Topic Workspace Pixi layout, `env-gate.md`, or `isomer-env-gate.md` file locations.
- Do not remove `ensure-topic-repos`, dependency inference, Pixi install, or topic-root verification from topic env setup in this change.
- Do not add a new service skill unless implementation discovers a hard boundary that cannot be expressed by existing skills.
- Do not change Workspace Runtime, Agent Team Instance, Execution Adapter, or Houmao launch behavior.
- Do not introduce new Python runtime APIs or data migrations.

## Decisions

### Decision: Treat Topic Workspace readiness as predecessor evidence

`isomer-srv-topic-env-setup` will produce auditable predecessor evidence: resolved Project and Research Topic, Topic Workspace path, Topic Workspace Pixi binding, source and derived topic env gates, dependency and enclosure records, commands run, changed files, readiness status, blockers, and next action. It will not read `agent-env-gate.md`, create `isomer-agent-env-gate.md`, prepare Agent Workspace worktrees, or verify commands from `agent.workspace` cwd values.

Alternative considered: keep topic env setup as the hub that tells the user to run agent env setup after topic readiness. That keeps a convenient workflow hint, but it makes the skill look responsible for downstream proof. The better shape is that topic env setup may report `per-agent readiness not checked` and expose predecessor evidence; the operator or agent env setup then decides what to do.

### Decision: Keep Agent Workspace readiness entirely in agent env setup

`isomer-srv-agent-env-setup` remains downstream of topic env setup. Its `require-topic-env-ready` step consumes Topic Workspace predecessor evidence and routes missing or stale dependency readiness back to `isomer-srv-topic-env-setup`. After that, agent env setup owns source agent gate reading, derived agent gate writing, authoritative Agent Name planning, Topic Main Repository configuration, Agent Workspace worktrees, support paths, and per-agent cwd verification.

Alternative considered: move worktree setup fully back to `isomer-admin-topic-workspace-mgr`. That would make agent env setup thinner, but the existing agent env setup spec already owns env-gate-aware worktree preparation and gate-driven configuration. The workspace manager can still own Git-only topology and validation evidence when called directly.

### Decision: Let operator skills own orchestration

`isomer-admin-topic-team-specialize` should decide whether the user is asking for Topic Workspace setup, Agent Workspace setup, or both. Its `setup-topic-env` subcommand prepares the topic env handoff and delegates heavy Topic Workspace setup to `isomer-srv-topic-env-setup`. Its `setup-agent-workspace` subcommand prepares or confirms `agent-env-gate.md` when needed, delegates Git topology to `isomer-admin-topic-workspace-mgr`, then delegates per-agent readiness to `isomer-srv-agent-env-setup`.

Alternative considered: teach topic env setup to call agent env setup when a source gate mentions Agent Workspaces. This would couple topic setup to topic-team material and Agent Name authority, which conflicts with its stated independence from Topic Agent Team Profile material.

### Decision: Preserve current setup mechanics but slim native policy wording

Topic env setup can still infer dependencies, mutate the selected Topic Workspace Pixi environment, and verify the topic env gate. However, broad package-source resolution and CUDA/NVIDIA preference text should become routing guidance rather than native policy where possible. If mirror reachability, registry selection, or NVIDIA channel choice is uncertain, the setup flow should consult `isomer-srv-resolve-pkg-repo`. If CUDA build settings or Pixi CUDA/C++ setup details are needed, it should consult `isomer-misc-nvidia-tools`.

Alternative considered: split topic env setup into several new skills, such as repo acquisition, dependency planning, and verification. That could be cleaner someday, but this change can remove the immediate boundary confusion without adding more skill surfaces.

### Decision: Make the call graph document a boundary test

`skillset/callgraph.md` should represent actual top-level skill calls or handoffs. It should not include a `topic-env-setup -> agent-env-setup` edge unless topic env setup truly invokes or owns that downstream work. The graph can still mention that agent env setup consumes topic env predecessor evidence and routes repair back to topic env setup.

Alternative considered: keep the edge with a note that it is only a next action. That was the source of confusion; call graph edges should not need that caveat.

## Risks / Trade-offs

- Existing docs may rely on the word "route" ambiguously → Replace ambiguous routing language with explicit caller ownership: operator calls agent env setup; agent env setup may route repair back to topic env setup; topic env setup reports only topic readiness.
- Slimming topic env setup too aggressively could hide useful next actions → Keep `next_action` fields, but phrase them as operator follow-ups, not as skill-owned downstream responsibilities.
- Package-source and NVIDIA policy may become harder to find → Add concise cross-references to `isomer-srv-resolve-pkg-repo` and `isomer-misc-nvidia-tools` instead of deleting policy context entirely.
- OpenSpec delta specs may overlap with existing broad requirements → Add focused requirements rather than rewriting large existing blocks unless implementation needs to alter a current requirement verbatim.

## Migration Plan

1. Update the delta specs to encode the narrowed Topic Workspace predecessor boundary and the Agent Workspace readiness owner.
2. Refactor `isomer-srv-topic-env-setup` entrypoint and reference pages to remove downstream agent-readiness responsibility language.
3. Refactor `isomer-srv-agent-env-setup` docs where needed so predecessor consumption and repair routing are explicit.
4. Refactor operator specialization and workspace manager references so orchestration calls happen from operator context, not from topic env setup.
5. Update service/operator READMEs and `skillset/callgraph.md` to match the new ownership model.
6. Run skill validation, OpenSpec validation, and relevant unit tests.

Rollback is documentation-only: revert the skill and OpenSpec documentation changes if the narrowed boundary prevents a required operator workflow from being represented.
