## Context

`isomer-srv-topic-env-setup` reads the user-authored `user-intent/src/env-gate.md`, prepares the Topic Workspace Pixi environment, and verifies `user-intent/derived/isomer-env-gate.md` for one operator or agent working from the Topic Workspace. `isomer-admin-topic-workspace-mgr` prepares Git-backed static workspace topology with one shared Topic Main Repository and per-agent Agent Workspace worktrees. `isomer-admin-topic-team-specialize setup-agent-workspace` currently treats that static workspace evidence as a prerequisite for later validation.

The missing layer is a service-safe workflow that reads a user-authored `user-intent/src/agent-env-gate.md`, configures or creates the shared Topic Main Repository, creates per-agent worktrees, and proves the required agent-cwd commands work from every planned Agent Workspace cwd. This matters because worker agents launch from `agent.workspace`, not from the Topic Workspace root. A target can pass from the Topic Workspace root while failing from an Agent Workspace because relative paths, editable installs, repo discovery, or cwd-sensitive scripts differ.

The current domain model also requires semantic path resolution: `topic.main_repo`, `agent.workspace`, and agent support labels are the contract; `isomer-default.v1` is only the default binding profile. The new service must therefore report semantic labels and path sources before mutating Git state or claiming readiness.

## Goals / Non-Goals

**Goals:**

- Add a service skill named `isomer-srv-agent-env-setup`.
- Require and interpret `user-intent/src/agent-env-gate.md` as the user-authored source gate for Agent Workspace cwd readiness.
- Prepare or validate the shared `topic.main_repo` normal repository and each planned `agent.workspace` as a Git worktree.
- Verify the already prepared Topic Workspace Pixi environment from every planned Agent Workspace cwd.
- Generate `user-intent/derived/isomer-agent-env-gate.md` as the per-agent operational readiness gate.
- Report semantic labels, path sources, branch plans, commands run, readiness by agent, blockers, and next action.
- Let operator skills delegate or consume this service output as durable static setup evidence.

**Non-Goals:**

- Do not create per-agent Pixi manifests, lockfiles, `.pixi/` directories, or dependency environments by default.
- Do not install or mutate dependencies unless a later explicit repair workflow authorizes rerouting back to topic env setup.
- Do not create Agent Instances, mutate Workspace Runtime records, launch Houmao agents, run Execution Adapters, or claim runtime launch readiness.
- Do not infer Agent Workspaces by scanning directories; use role bindings, explicit agent maps, or semantic path resolution.
- Do not overwrite, delete, clean, reset, reinitialize, or silently repair existing repos or worktrees.

## Decisions

### Decision: Split topic env readiness from agent cwd readiness

`isomer-srv-topic-env-setup` remains the dependency-installing Topic Workspace Pixi setup service. `isomer-srv-agent-env-setup` consumes its output, reads `user-intent/src/agent-env-gate.md`, and proves that the same topic env is usable from each Agent Workspace cwd for the commands required by the agent gate. This keeps dependency mutation in one place and makes the agent service focused on source agent gate interpretation, Git topology, Topic Main Repository configuration, and cwd-sensitive verification.

Alternative considered: extend `isomer-srv-topic-env-setup` with agent modes. That would blur topic-level dependency installation with per-agent workspace creation and make the topic service depend on topic-team role planning.

### Decision: Use one topic Pixi environment for all Agent Workspaces

Agent env setup does not create separate per-agent Pixi environments. Verification commands use the resolved Topic Workspace Pixi manifest and environment, even when the command cwd is the resolved `agent.workspace`. Successful readiness means the shared topic env is valid from every planned worker cwd.

Alternative considered: create per-agent Pixi environments. That would increase isolation, but it conflicts with the accepted Topic Workspace Pixi default and creates extra lockfiles, caches, and dependency drift for every agent.

### Decision: Make the new service a command-style skill

The skill should mirror the structure of `isomer-srv-topic-env-setup`: a lean `SKILL.md`, grouped subcommands, one executable reference page per subcommand, and a full-flow `setup-agent-env` misc subcommand. Direct subcommands support partial repair or inspection without forcing the full chain.

Recommended public subcommands:

- `resolve-agent-env-context`
- `require-topic-env-ready`
- `read-agent-env-gate`
- `plan-agent-workspaces`
- `derive-agent-env-gate`
- `ensure-topic-main-repository`
- `create-agent-worktrees`
- `verify-agent-env-gate`
- `setup-agent-env`
- `help`

Alternative considered: only add one monolithic `setup-agent-env` page. That would be simpler, but it would make failure recovery awkward when only one agent worktree or one gate command needs repair.

### Decision: Full flow verifies all agents; direct verification can target one agent

`setup-agent-env` verifies the complete planned Agent Name matrix and can report overall Agent Workspace env readiness only when every planned agent passes. Direct repair or inspection subcommands, especially `verify-agent-env-gate`, may accept one authoritative Agent Name for focused reruns after a failed or blocked full-flow attempt. A selected-agent run updates that agent's worktree or verification evidence and the derived gate execution log, but it reports partial readiness evidence and cannot by itself make `overall_readiness_status` ready.

Alternative considered: make every verification run cover all agents. That would simplify status semantics, but it would make repair loops slow when one agent or one cwd-sensitive command needs rerunning.

### Decision: Allow direct setup invocation while preserving provenance hooks

The service can be invoked directly by a Project Operator Session after the selected Project, Research Topic, Topic Workspace, topic env predecessor evidence, authoritative Agent Name plan, and requested mutation scope are confirmed. A Service Request is not required for the first implementation. When Service Request, support Artifact, or Provenance refs are available, the service records them in its output and in the derived agent env gate execution log. When they are absent, the service records the requester as a direct Project Operator Session and names the explicit mutation confirmation, changed files, commands run, blockers, and next action. These outputs remain static setup evidence and do not create Workspace Runtime records, Agent Team Instance records, or runtime truth.

Alternative considered: require explicit Service Request and Provenance refs before mutation. That better matches the long-term Service Team model, but Service Request dispatch and monitoring are not yet complete enough to block this service on those records.

### Decision: Use semantic labels before filesystem mutation

The service must resolve `topic.main_repo`, `topic.main_repo.isomer_managed`, `topic.agents_root`, `agent.workspace`, and the required `agent.*` support labels through Workspace Path Resolution before creating files. Default paths may appear in examples, but output must identify `isomer-default.v1` or manifest source rather than implying fixed path authority.

Alternative considered: reuse default paths inside the service and validate later. That would recreate the old implicit-layout contract and break custom Topic Workspace Manifest bindings.

### Decision: Treat `topic.main_repo` as the single Git anchor

The service creates or reuses one normal non-bare Topic Main Repository resolved by `topic.main_repo`; under `isomer-default.v1`, this is the default `repos/topic-main` repository. If the resolved path is missing, empty, or an empty normal Git repository, the service initializes it, creates the owner-managed branch `topic-owner/main`, and creates a minimal baseline commit so per-agent worktrees have a stable base. If the path is an existing safe normal Git repository, the service reuses it without rewriting history and creates or validates `topic-owner/main` from the current accepted base when needed. The service then applies non-destructive Topic Main Repository configuration required by the derived agent env gate before per-agent worktrees are created. Unsafe existing non-Git content, bare repositories, corrupt repositories, ambiguous history state, destructive repair needs, or non-destructive reuse uncertainty block setup.

Each Agent Workspace is a Git worktree of that repository on `per-agent/<agent-name>/main`. Agent Workspaces are not independent clones and should not get separate remotes unless a later Git policy adds one.

Alternative considered: clone one repository per agent. That would make each cwd look familiar, but it would lose the shared worktree topology, duplicate storage, and create a harder merge and provenance story.

### Decision: Derive an agent env gate from the source agent gate

The service reads `user-intent/src/agent-env-gate.md` and writes `user-intent/derived/isomer-agent-env-gate.md`. The derived file records source agent gate path, topic env gate path, topic Pixi binding, Topic Main Repository configuration plan, agent plan, worktree plan, semantic path evidence, verification matrix, expected results, blockers, and execution log. It should not duplicate dependency planning from `isomer-env-gate.md`; it should reference the topic env gate as predecessor evidence while treating `agent-env-gate.md` as the source contract for Agent Workspace cwd readiness.

Alternative considered: append per-agent results to `isomer-env-gate.md`. That would make one file do two jobs and make it harder to distinguish topic-level dependency readiness from agent-cwd readiness.

### Decision: Readiness is a per-agent matrix

The service reports `ready` only when every expected agent passes worktree validation and every required command from the derived agent env gate runs successfully from that agent's cwd. Individual failures are reported as `failed` or `blocked` per agent, with an overall `blocked` or `failed` status. A topic env that passes only from the Topic Workspace root is not sufficient.

Alternative considered: verify one representative Agent Workspace. That is faster, but it misses per-agent path, branch, support-label, and cwd inference failures.

### Decision: Agent Names come from topic-team material

Agent env setup treats Agent Names as authoritative only when they come from the Topic Team Instantiation Packet or the Topic Agent Team Profile material derived from that packet. An explicit operator-provided agent map cannot define a different Agent Name, and it cannot override packet or profile material. If an operator map disagrees with topic-team material, the service reports an `agent-plan-conflict` blocker and routes the operator back to Topic Team Specialization to repair the packet or profile. If the service cannot find authoritative Agent Names in topic-team material, setup blocks rather than inventing names from directory scans or ad hoc maps.

Alternative considered: let an explicit operator map override stale packet material. That would make manual repair faster, but it would turn Agent Names into session-local hints instead of durable topic-team design material.

### Decision: Keep runtime mutation out of scope

The service can create static Git worktrees and boundary material, but Workspace Runtime remains authoritative only when later runtime workflows create Agent Team Instance records and path plans. Service output becomes static evidence, not runtime truth.

Alternative considered: have the service record runtime Agent Workspace records directly. That would mix static preparation with runtime lifecycle creation and bypass the existing Agent Team Instance workflow.

## Risks / Trade-offs

- Cwd-sensitive gates may fail after topic env setup already passed -> The agent service reports a specific `gate-cwd-incompatible` blocker and points back to gate repair or topic env setup.
- Existing nonmatching Agent Workspace paths can block setup -> The service refuses destructive repair and reports the exact path, expected semantic label, and safe next action.
- Verifying every agent can be slow -> The service can report per-agent progress and stop only on safety blockers; command failures remain useful evidence.
- Operator and service skills may overlap -> The operator skill should remain orchestration and summary; the service skill owns concrete service-safe per-agent env setup and verification.
- Missing `tmp/` implementation may lag this change -> The skill should include `agent.tmp` and `topic.main_repo.tmp` as expected labels when the tmp change is present, while keeping tmp material out of durable readiness evidence.

## Migration Plan

1. Add the `isomer-srv-agent-env-setup` skill bundle and references.
2. Add service skill validation for the new bundle, subcommands, semantic path evidence, per-agent gate file, and guardrails.
3. Update `isomer-admin-topic-workspace-mgr` to delegate agent env readiness or explicitly route users to the service when env verification is requested.
4. Update `isomer-admin-topic-team-specialize` to consume `isomer-srv-agent-env-setup` output in `setup-agent-workspace`, `validate-topic-team`, and `finalize-topic-team`.
5. Update docs or skill help text that lists service skills.
6. Validate with skillset tests, docs validation, and strict OpenSpec validation.

Rollback is simple before adoption: remove the new service skill and validation checks, and leave the existing topic env setup plus operator workspace manager behavior in place. After adoption, rollback should preserve generated `isomer-agent-env-gate.md` as static evidence but stop treating it as required readiness input.

## Open Questions

None.
