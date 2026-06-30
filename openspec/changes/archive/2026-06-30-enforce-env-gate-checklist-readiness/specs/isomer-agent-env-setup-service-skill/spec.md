## MODIFIED Requirements

### Requirement: Agent Env Gate File
The service skill SHALL resolve a derived per-agent readiness target spec before Agent Workspace materialization. In the normal operator flow, that target spec is `topic.env.agent_setup_target_spec`; in manual service invocation, it can be an explicit derived gate file, prompt, or context supplied by the caller.

#### Scenario: Source and derived agent gate paths are paired in operator flow
- **WHEN** `derive-agent-env-gate` resolves gate paths
- **THEN** it reads the source gate at `topic.intent.agent_env_requirements`
- **AND** it writes the derived gate at `topic.env.agent_setup_target_spec`

#### Scenario: Explicit agent target spec source is recorded
- **WHEN** the service receives an explicit derived gate file, target-spec prompt, or target-spec context from a manual invocation
- **THEN** it records that source in service output and in the execution log when a canonical derived gate is written

#### Scenario: Target spec has fixed sections
- **WHEN** the service generates or accepts the target spec
- **THEN** the file includes sections named `Source Agent Gate`, `Gate Checklist`, `Topic Env Gate`, `Topic Pixi Binding`, `Topic Main Development Repository Predecessor`, `Agent Plan`, `Semantic Paths`, `Worktree Plan`, `Verification Matrix`, `Resource Check Plan`, `Expected Results`, `Blockers`, and `Execution Log`
- **AND** every section is present even when the section content is `None.` or a short reason that it does not apply

#### Scenario: Gate checklist records required per-agent readiness work
- **WHEN** the service generates `topic.env.agent_setup_target_spec`
- **THEN** every required predecessor, worktree, semantic path, projection visibility, resource, verification, expected-result, and blocker-resolution item needed for Agent Workspace readiness is represented as a Markdown checkbox under `Gate Checklist`
- **AND** optional diagnostics or supporting smoke checks that are not required for readiness are recorded outside `Gate Checklist`

#### Scenario: Gate records per-agent cwd commands
- **WHEN** verification commands are defined by the target spec
- **THEN** each command records the source `topic.intent.agent_env_requirements` requirement, related checklist item, Agent Name, cwd as the resolved `agent.workspace`, the `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...` command, and expected result

#### Scenario: Gate records path evidence
- **WHEN** the gate records an Agent Workspace
- **THEN** it includes the relevant semantic labels, resolved paths, path sources, branch plan, and worktree status

#### Scenario: Gate does not record tmp as durable evidence
- **WHEN** the gate mentions tmp labels
- **THEN** it describes them as local ignored disposable surfaces
- **AND** it does not use tmp contents as readiness evidence

### Requirement: Agent Cwd Env Verification
The service skill SHALL verify the Topic Workspace environment from each planned Agent Workspace cwd and SHALL compute readiness from required `Gate Checklist` completion.

#### Scenario: Commands run from Agent Workspace cwd
- **WHEN** `verify-agent-env-gate` runs a verification command for Agent Name `alice`
- **THEN** the process cwd is the resolved `agent.workspace` for `alice`
- **AND** the command uses the resolved Topic Workspace Pixi manifest and selected Pixi environment

#### Scenario: Passing means required checklist items are complete
- **WHEN** `verify-agent-env-gate` reports Agent Name `alice` as ready
- **THEN** every required checklist item from `topic.env.agent_setup_target_spec` that applies to `alice` is checked and backed by evidence from the resolved `agent.workspace` cwd
- **AND** every required command for `alice` has passed with the resolved `agent.workspace` as process cwd
- **AND** a command passing from the Topic Workspace root alone does not satisfy the agent gate

#### Scenario: Cwd-friendly agent path query is verified
- **WHEN** an Agent Workspace is prepared
- **THEN** verification includes or records a check that an agent-scoped semantic label can be resolved from inside that Agent Workspace without passing Agent Name

#### Scenario: Topic-root-only pass is insufficient
- **WHEN** the topic env gate passes from the Topic Workspace root but fails from an Agent Workspace cwd
- **THEN** the service does not report agent env readiness
- **AND** it reports a `gate-cwd-incompatible` or equivalent blocker naming the failing agent and command

#### Scenario: Overall readiness requires every agent checklist
- **WHEN** the service reports overall readiness as `ready`
- **THEN** every planned agent has a ready worktree, required support paths, complete path evidence, cwd-friendly query evidence, and every required checklist item for that agent checked with passing evidence from that agent's cwd

#### Scenario: Selected-agent verification does not imply overall readiness
- **WHEN** `verify-agent-env-gate` is run for one selected Agent Name
- **THEN** the service updates or reports that agent's verification evidence
- **AND** it labels the result as selected-agent partial readiness evidence
- **AND** it does not report `overall_readiness_status` as `ready` unless the complete planned Agent Name matrix has already passed

#### Scenario: Unchecked checklist item blocks readiness
- **WHEN** any required item under `Gate Checklist` remains unchecked for a targeted Agent Name after setup or verification
- **THEN** the service does not report that agent as ready
- **AND** it reports `blocked` when the item could not be run, `failed` when it ran and missed its expected result, or `not checked` only when verification was explicitly not requested
- **AND** it names the exact checklist item, Agent Name, reason, and next safe action in `Blockers`, `Execution Log`, or the final output

#### Scenario: Bounded real-path evidence can complete heavy per-agent checklist item
- **WHEN** a required checklist item names heavy work such as compilation, model inference, dataset processing, benchmark execution, large archive extraction, a broad test suite, or repeated full-matrix checks
- **THEN** the service may check the item only after a bounded real-path command exercises the same critical path named by the item and passes its expected result from the required Agent Workspace cwd
- **AND** bounded real-path evidence may use selected-agent partial runs, reduced parallelism, selected build targets, tiny model or tensor shapes, sample data, reduced iterations, reduced batch size, selected tests, or short benchmark cases

#### Scenario: Unrelated smoke test cannot complete critical per-agent checklist item
- **WHEN** a required checklist item names a critical build, inference, dataset, benchmark, projection-dependent, or repo-specific runtime path
- **THEN** the service does not mark that item checked merely because a weaker smoke test passed
- **AND** generic import success, device visibility, Pixi install success, projection path visibility, or worktree existence counts only for a checklist item that specifically asks for that smoke evidence

#### Scenario: User downgrade is explicit evidence
- **WHEN** the user explicitly instructs the agent to accept a weaker check instead of the original critical-path checklist item
- **THEN** the service records the user instruction, original checklist item, affected Agent Name or matrix scope, weaker evidence, and resulting limitation in the execution log or blocker record
- **AND** it does not silently present the weaker check as proof that the original critical path passed

#### Scenario: Partial results remain visible
- **WHEN** one or more agents fail or block
- **THEN** the service reports readiness by agent, commands run, command outcomes, incomplete checklist items, blockers, and the next safe repair action
