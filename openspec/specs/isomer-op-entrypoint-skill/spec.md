# isomer-op-entrypoint-skill Specification

## Purpose
TBD - created by archiving change add-isomer-op-entrypoint-skill. Update Purpose after archive.
## Requirements
### Requirement: Entrypoint Operator Skill Inventory
The system SHALL provide `isomer-op-entrypoint` as the public core execution skill for informed-user task routing while providing `isomer-op-welcome` as a separate public newcomer skill.

#### Scenario: Entrypoint assets exist
- **WHEN** the packaged core skillset is inspected
- **THEN** it contains `operator/isomer-op-entrypoint/SKILL.md`, `agents/openai.yaml`, directly linked routing resources, and the declared protected subskill inventory
- **AND** it contains no protected `isomer-op-welcome` bundle

#### Scenario: Public core pair is distinct
- **WHEN** the core catalog is inspected
- **THEN** `isomer-op-entrypoint` has role `entrypoint` and `isomer-op-welcome` has role `welcome`
- **AND** both public skills belong to the same complete core pack without sharing private resources

#### Scenario: Entrypoint identity is consistent
- **WHEN** `operator/isomer-op-entrypoint` is inspected
- **THEN** its folder, frontmatter, UI metadata, and default prompt use `isomer-op-entrypoint`
- **AND** its description identifies route-and-proceed execution rather than newcomer tutorial ownership

#### Scenario: Entrypoint owns protected routes
- **WHEN** the parent route table is inspected
- **THEN** it maps every core scoped member to one nested protected logical capability
- **AND** it declares the standard object invocation notation

#### Scenario: Entrypoint has a workflow-shaped skill body
- **WHEN** the public `SKILL.md` is inspected
- **THEN** it has a near-top numbered Workflow that parses the task, discovers safe context when useful, selects a route, loads only the selected protected member or CLI guidance, proceeds, and reports the result
- **AND** it has a freeform fallback
### Requirement: Entrypoint Routes Then Proceeds
The entrypoint SHALL resolve a public command or concrete task to one protected member, optional public extension entrypoint, or CLI surface and proceed by default, while orientation-only requests route to the independent welcome skill.

#### Scenario: User invokes a public execution command
- **WHEN** the user supplies `$isomer-op-entrypoint use <command> to <task>`
- **THEN** the entrypoint resolves the command and proceeds through the matching route or reports a concrete blocker

#### Scenario: Invocation is empty
- **WHEN** the user invokes `$isomer-op-entrypoint` without a task or command
- **THEN** the entrypoint delegates read-only output to `$isomer-op-welcome` while preserving supplied context
- **AND** it does not load a private welcome subskill

#### Scenario: User asks how to use Isomer
- **WHEN** the request is orientation, command-learning, route comparison, or typical-use-case discovery rather than execution
- **THEN** the entrypoint delegates to `$isomer-op-welcome` without losing supplied context
- **AND** welcome remains non-mutating

#### Scenario: Concrete task has no command
- **WHEN** the user gives a concrete task, prompt, or file without asking only for help
- **THEN** the entrypoint selects one protected member, public extension entrypoint, or CLI command family
- **AND** it proceeds or reports a blocker instead of stopping after route enumeration

#### Scenario: Explanation-only task stays non-mutating
- **WHEN** the user asks only what route to use or what options exist
- **THEN** the entrypoint may explain routing without invoking mutating workflows

#### Scenario: Ambiguous mutation uses read-only preflight
- **WHEN** action lacks enough Project, Topic, actor, agent, or workspace context
- **THEN** the entrypoint uses read-only evidence before mutation and pauses for information only when the route cannot be resolved safely
### Requirement: Entrypoint Indexes All System Skill Families
The entrypoint SHALL index core protected operator, service, and shared capabilities while linking public welcome skills as orientation surfaces rather than protected owner routes.

#### Scenario: Operator routes are indexed
- **WHEN** the entrypoint protected route table is inspected
- **THEN** it contains Project lifecycle, GUI, identity, system-skill management, Toolbox management, Topic creation, Topic management, and Topic Team Specialization members
- **AND** it does not contain member `welcome`

#### Scenario: Welcome route is public
- **WHEN** entrypoint guidance explains orientation
- **THEN** it names `$isomer-op-welcome` as the public core learning surface
- **AND** it does not use `isomer-op-entrypoint->welcome` as an active designator

#### Scenario: Service and shared routes stay bounded
- **WHEN** service or shared support is needed
- **THEN** entrypoint routing uses the applicable protected member under its existing owner boundary
- **AND** public guidance does not present protected logical ids as peer welcome or entrypoint skills

#### Scenario: Retired routes are excluded
- **WHEN** active guidance is inspected
- **THEN** it does not present retired topic workspace, topic preparation, manual session, operator Houmao, admin, or research-v1 names as active routes
### Requirement: Entrypoint Includes Extension Skill Routing
The core entrypoint SHALL route optional research paradigms through their public extension entrypoints and SHALL point orientation-only extension questions to their public welcome skills.

#### Scenario: Extension public pairs are indexed
- **WHEN** entrypoint extension references are inspected
- **THEN** they identify `isomer-ext-deepsci-welcome` with `isomer-ext-deepsci-entrypoint` and `isomer-ext-kaoju-welcome` with `isomer-ext-kaoju-entrypoint`
- **AND** they distinguish learning from execution

#### Scenario: Prepared extension task is selected
- **WHEN** a concrete task maps to DeepSci or Kaoju and required readiness exists
- **THEN** the core entrypoint routes to the matching extension execution entrypoint
- **AND** the extension entrypoint selects its protected member while preserving existing callbacks, evidence, Gate, and output contracts

#### Scenario: Extension comparison is requested
- **WHEN** the user asks how to use one extension or compare its typical workflows without requesting execution
- **THEN** the core entrypoint routes to the applicable extension welcome or core welcome comparison guidance
- **AND** it performs no extension task mutation

#### Scenario: Missing DeepSci readiness routes to setup
- **WHEN** the user asks for DeepSci research work but required Topic Workspace, Topic Actor, Agent Workspace, or DeepSci bootstrap readiness is missing
- **THEN** the entrypoint routes to `isomer-op-topic-creator`, `isomer-op-topic-mgr`, `isomer-op-topic-team-specialize`, `isomer-srv-agent-env-setup` through its owner, or `isomer-deepsci-workspace-mgr` as appropriate
- **AND** it does not let an ordinary research-stage skill fabricate missing readiness

#### Scenario: Extension is unavailable
- **WHEN** a concrete task maps to an optional extension that is not declared or host-usable
- **THEN** the core entrypoint routes extension reconciliation through its protected `system-skills` member
- **AND** it resumes the public extension entrypoint after successful reconciliation
### Requirement: Entrypoint Includes CLI Surface Routing
The entrypoint SHALL include concise routing guidance for Isomer CLI command families without duplicating full CLI help.

#### Scenario: Read-only context discovery commands are named
- **WHEN** entrypoint CLI guidance is inspected
- **THEN** it names safe context discovery surfaces such as `isomer-cli project self queries`, `isomer-cli project self show`, `isomer-cli project validate`, `isomer-cli doctor`, `isomer-cli project topics list`, `isomer-cli project context show`, and Workspace Path Resolution commands

#### Scenario: Topic-owned record commands are named
- **WHEN** entrypoint CLI guidance is inspected
- **THEN** it routes structured research record create, list, show, update, delete, validate, render, query, index, and cleanup needs to `isomer-cli ext research records ...`
- **AND** it does not instruct agents to hand-edit record indexes

#### Scenario: Specialized CLI families are discoverable
- **WHEN** entrypoint CLI guidance is inspected
- **THEN** it mentions artifact-format processing, topic reset checkpoints, runtime, handoffs, team templates, team profiles, team instances, topic actors, topic-main guidance, paths, repositories, and outputs policy command families as CLI surfaces to inspect when the user task matches them

### Requirement: Entrypoint Output Contract
The entrypoint SHALL report concise routing and execution results by default, with complete routing evidence available on request.

#### Scenario: Essential output reports the route
- **WHEN** the entrypoint completes a routed task
- **THEN** it reports status, interpreted goal, selected route kind, selected skill or CLI family, context used, what changed or what was inspected, blockers, and next action

#### Scenario: Complete output reports evidence
- **WHEN** the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output
- **THEN** the entrypoint includes route candidates, route rationale, commands run, read-only versus mutation posture, selected Project or Topic context, selected actor or agent identity, extension-skill readiness checks, and service-skill delegation notes

### Requirement: Entrypoint Validation
The repository SHALL validate `isomer-op-entrypoint` as the public core execution surface and enforce its boundary with the independent welcome skill.

#### Scenario: Valid entrypoint passes
- **WHEN** operator validation runs against a valid core pack
- **THEN** it checks public execution invocation, route-and-proceed language, protected inventory, CLI routes, extension public pairs, service and shared boundaries, compatibility delegation, and retired-route exclusions
- **AND** it confirms that welcome is absent from the protected inventory

#### Scenario: Entrypoint retains private welcome
- **WHEN** the entrypoint contains a protected `welcome` member, private welcome resources, or active `isomer-op-entrypoint->welcome` guidance
- **THEN** validation reports that welcome must be the independent public `isomer-op-welcome` skill

#### Scenario: Compatibility command duplicates welcome content
- **WHEN** a retained entrypoint help or onboarding alias copies the welcome procedure instead of delegating to the public welcome skill
- **THEN** validation reports duplicate ownership and the canonical welcome route

#### Scenario: Valid core pack passes
- **WHEN** operator skill validation runs
- **THEN** it checks public invocation, empty-help behavior, route-and-proceed language, protected inventory, member mappings, CLI routes, extension entrypoints, object notation, service boundaries, shared boundaries, and retired-route exclusions

#### Scenario: Entrypoint validator rejects stale or unsafe routes
- **WHEN** active entrypoint guidance presents retired operator skills, old admin names, service skills as normal first-click owner routes, or `pixi run isomer-cli` command guidance
- **THEN** operator skill validation reports diagnostics

#### Scenario: Entrypoint validator rejects missing extension coverage
- **WHEN** active entrypoint guidance omits DeepSci extension-skill routing
- **THEN** operator skill validation reports that extension skill coverage is incomplete

#### Scenario: Direct protected public route is introduced
- **WHEN** active entrypoint guidance tells a user to invoke a protected logical id directly
- **THEN** validation reports the route and its required parent form

#### Scenario: Protected member coverage is incomplete
- **WHEN** a manifest core member is missing from the parent route table or a parent route lacks manifest metadata
- **THEN** validation fails with the member or route identity
### Requirement: Entrypoint Routes Toolbox Tasks
The public core entrypoint SHALL route project-local Toolbox tasks through protected member `toolbox`, whose logical id remains `isomer-op-toolbox-mgr`.

#### Scenario: System skill index includes Toolbox manager
- **WHEN** the entrypoint system skill index is inspected
- **THEN** it lists `isomer-op-toolbox-mgr` as the active operator owner for creating, converting, installing, inspecting, updating, disabling, uninstalling, and explaining project-local Toolboxes
- **AND** it includes Toolbox callback declarations, callback insertion points, Runtime Params, and effective-state inspection in that owner boundary

#### Scenario: Toolbox command is selected
- **WHEN** a user asks to create, convert, install, inspect, update, disable, uninstall, or explain a Project-local Toolbox
- **THEN** the entrypoint invokes `isomer-op-entrypoint->toolbox` and proceeds under the Toolbox Manager contract

#### Scenario: Toolbox and tool packs stay distinct
- **WHEN** a request concerns named dependency bundles rather than Toolbox configuration
- **THEN** the entrypoint may route to protected member `tool-packs`
- **AND** it does not conflate that helper with Toolbox management

### Requirement: Entrypoint Indexes Toolbox CLI Families
The `isomer-op-entrypoint` skill SHALL include concise CLI routing guidance for existing Toolbox command families.

#### Scenario: Toolbox CLI families are named
- **WHEN** entrypoint CLI guidance is inspected
- **THEN** it names `isomer-cli project toolboxes ...`, `isomer-cli project skill-callbacks ...`, and `isomer-cli project toolbox-params ...` as Toolbox-related CLI command families
- **AND** it describes `toolboxes` as full Toolbox registration, validation, install, enable, disable, update-source, uninstall, show, list, or explain work
- **AND** it describes `skill-callbacks` as callback insertion-point, registry, resolve, validation, and callback install or refresh work
- **AND** it describes `toolbox-params` as Runtime Param set, unset, import, get, explain, and validate work

#### Scenario: Explicit CLI request may use CLI route
- **WHEN** the user explicitly asks for a Toolbox CLI command family
- **THEN** the entrypoint may route to the matching CLI family, inspect CLI help when flags are needed, and preserve read-only or mutation posture in its output\n

### Requirement: Entrypoint Delegates System Skill Management
The public core entrypoint SHALL route detection, reconciliation, installation, status, upgrade, and repair through protected member `system-skills`.

#### Scenario: Extension management request selects protected owner
- **WHEN** the user asks to find, install, register, reconcile, inspect, upgrade, or repair Isomer system-skill extensions
- **THEN** the entrypoint invokes `isomer-op-entrypoint->system-skills`
- **AND** the protected manager uses pack-aware evidence and operations

#### Scenario: Declared extension is trusted
- **WHEN** a concrete request maps to a Project-declared extension
- **THEN** the entrypoint attempts the matching public extension entrypoint
- **AND** later unavailable-pack evidence produces protected manager repair guidance

### Requirement: Entrypoint Does Not Encode Provider Discovery Paths
Entrypoint extension routing SHALL use Project declarations and the system-skill manager instead of hard-coded project or user-home skill roots.

#### Scenario: Entrypoint references remain provider-neutral
- **WHEN** entrypoint skill and routing references are inspected
- **THEN** they instruct the agent to use host-known roots and live inventory through the owner skill
- **AND** they do not require fixed Claude, Codex, Kimi, generic, plugin, or user-home paths as universal discovery rules

### Requirement: Entrypoint Requires Agent Team Intent for Specialization
The operator entrypoint SHALL select `isomer-op-topic-team-specialize` only after the user explicitly invokes that skill or the prompt or authoritative Project context establishes a formal Agent Team target.

#### Scenario: Explicit specialization invocation is preserved
- **WHEN** the user explicitly invokes `isomer-op-topic-team-specialize`, `specialize-team`, or an equivalent named Agent Team specialization route
- **THEN** the entrypoint selects the Topic Team Specialization owner
- **AND** it preserves the supplied Research Topic and formal Agent Team context

#### Scenario: Prompt establishes Agent Team intent
- **WHEN** the user asks to deploy, specialize, instantiate, materialize, validate, repair, launch, or use an Agent Team and supplies or selects formal team context
- **THEN** the entrypoint may select `isomer-op-topic-team-specialize`
- **AND** its routing rationale names the Agent Team, Domain Agent Team Template, Topic Agent Team Profile, Topic Team Instantiation Packet, Agent Team Instance, or equivalent formal-team evidence

#### Scenario: Generic topic preparation does not imply a team
- **WHEN** the user asks to prepare, create, initialize, start, or repair a Research Topic without explicit or contextual formal Agent Team intent
- **THEN** the entrypoint routes new or partial setup to `isomer-op-topic-creator` and initialized-topic operations to `isomer-op-topic-mgr` or the applicable setup owner
- **AND** it does not select Topic Team Specialization from the topic name, Topic Workspace, generic readiness, missing summary, missing Agent Workspace, or generic launch-facing language alone

#### Scenario: Extension readiness recovery respects selected topology
- **WHEN** an extension workflow reports missing platform readiness
- **THEN** the entrypoint selects the owner of the missing base topic, actor, environment, runtime, or extension readiness layer
- **AND** it selects `isomer-op-topic-team-specialize` only when the selected topology already includes a formal Agent Team layer

### Requirement: Entrypoint Offers Target-Scoped Run-To Recovery
The operator entrypoint SHALL preserve its single initial route selection for ordinary tasks and SHALL offer target-scoped run-to recovery when the selected owner reports producible missing prerequisites.

#### Scenario: Selected owner reports missing prerequisites
- **WHEN** the entrypoint routes an ordinary concrete task to one owner
- **AND** that owner reports missing or stale inputs with available producer routes
- **THEN** the entrypoint's numbered workflow pauses before invoking those producers
- **AND** it presents the missing inputs, recommended recovery sequence, inclusive run-to option, next-prerequisite-only option, alternative-route option, and stop option

#### Scenario: User authorizes run-to across owners
- **WHEN** the user selects the inclusive run-to option for the original target
- **THEN** the entrypoint uses the agent's native planning tool to coordinate the target's prerequisite closure across the applicable owner skills
- **AND** it resumes and executes the original target after its prerequisites are satisfied
- **AND** it does not claim ownership of lower-level mutation performed by those owner skills

#### Scenario: Entrypoint run-to reaches a nondelegable boundary
- **WHEN** an owner reports a Gate, material ambiguity, or external authorization boundary during run-to traversal
- **THEN** the entrypoint pauses with completed evidence and the exact decision needed
- **AND** it does not reinterpret the original target request as blanket approval

### Requirement: Entrypoint Reports Recovery Posture
The operator entrypoint SHALL make the difference between an ordinary paused request and an authorized run-to traversal visible in its user-facing result.

#### Scenario: Ordinary request pauses
- **WHEN** the target has producible missing prerequisites and run-to is not authorized
- **THEN** Essential Output states that the target was not executed
- **AND** it names the missing inputs, recommended next step, recovery choices, and target resume point

#### Scenario: Run-to traversal finishes
- **WHEN** run-to satisfies the prerequisite closure and completes the original target
- **THEN** Essential Output leads with the target outcome
- **AND** it summarizes prerequisite owner work, important Runs or accepted refs, preserved Gates, and target validation without presenting each intermediate terminal report as a separate user action request

### Requirement: Entrypoint Routes Operation Set Acceptance
`isomer-op-entrypoint` SHALL make operation-set inspection, acceptance, verification, and legacy repair discoverable through the focused core recording skill and research CLI family.

#### Scenario: Research output closeout selects focused skill
- **WHEN** a user asks to persist, reconcile, close, verify, or repair files in a worker operation set
- **THEN** the entrypoint routes to `isomer-research-operation-set-recording` and proceeds with that workflow when context is sufficient

#### Scenario: Explicit CLI request uses operation-set commands
- **WHEN** a user explicitly asks for the CLI surface
- **THEN** entrypoint guidance names `isomer-cli ext research operation-sets inspect`, `accept`, and `verify` and preserves preview-before-apply behavior

#### Scenario: Project manager does not own research semantics
- **WHEN** an operation-set task requires record kinds, semantic bindings, artifact lineage, or Research Idea effects
- **THEN** the entrypoint does not treat generic Project lifecycle management as the recording authority

#### Scenario: Entrypoint validation checks route coverage
- **WHEN** operator skill validation inspects entrypoint research routes
- **THEN** it reports missing focused-skill or operation-set CLI coverage and stale guidance that treats plain worker files as accepted records

### Requirement: Core Entrypoint Explains Every Protected Route
The `isomer-op-entrypoint` skill SHALL provide one context-aware `When to Route Here` sentence for every protected operator, service, and shared subskill in its protected-subskill table. The sentences SHALL convert the existing category labels into actionable selection conditions while preserving owner and delegation boundaries.

#### Scenario: Core protected inventory is inspected
- **WHEN** `isomer-op-entrypoint/SKILL.md` is inspected
- **THEN** all 20 protected-member rows contain one routing sentence
- **AND** the existing member names, logical ids, areas, and internal designators remain unchanged

#### Scenario: Project and Topic lifecycle routes overlap
- **WHEN** a request could relate to Project lifecycle, blank-state Research Topic setup, initialized Research Topic management, or formal Topic Agent Team specialization
- **THEN** the applicable routing sentences distinguish `project`, `topic-create`, `topic-manage`, and `topic-team` by lifecycle state and requested outcome

#### Scenario: Service or shared support is considered
- **WHEN** a task may require environment, package repository, Houmao, Topic Service Agent, bounded-run, NVIDIA, package-specific, Tool Pack, research-idea, or Operation Set support
- **THEN** the routing sentences identify the bounded support condition without replacing the normal operator-owner route

#### Scenario: Public command and protected member share a name
- **WHEN** the table explains a protected member such as `gui`
- **THEN** the sentence does not change the distinction between the bare protected designator and the parenthesized public subcommand designator

