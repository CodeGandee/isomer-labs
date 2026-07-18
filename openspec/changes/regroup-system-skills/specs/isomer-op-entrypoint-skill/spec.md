## MODIFIED Requirements

### Requirement: Entrypoint Operator Skill Inventory
The system SHALL provide `isomer-op-entrypoint` as the sole public core pack for Project Operator Session and Operator Agent routing across protected core capabilities, optional public extension entrypoints, and CLI surfaces.

#### Scenario: Entrypoint pack assets exist
- **WHEN** the packaged core skillset is inspected
- **THEN** it contains `operator/isomer-op-entrypoint/SKILL.md`, `agents/openai.yaml`, directly linked routing resources, and the complete declared protected subskill inventory
- **AND** no other core Isomer skill is an ordinary top-level install unit

#### Scenario: Entrypoint identity is consistent
- **WHEN** `operator/isomer-op-entrypoint` is inspected
- **THEN** its folder, `SKILL.md` frontmatter name, UI metadata, and public default prompt use `isomer-op-entrypoint`
- **AND** its default prompt uses `$isomer-op-entrypoint use help` or a specific public subcommand form

#### Scenario: Entrypoint owns protected routes
- **WHEN** the parent route table is inspected
- **THEN** it maps every core scoped member to one nested protected logical capability
- **AND** it declares the standard object invocation notation

#### Scenario: Entrypoint has a workflow-shaped skill body
- **WHEN** the public `SKILL.md` is inspected
- **THEN** it has a near-top numbered Workflow that parses the task, discovers safe context when useful, selects a route, loads only the selected protected member or CLI guidance, proceeds, and reports the result
- **AND** it has a freeform fallback

### Requirement: Entrypoint Routes Then Proceeds
The entrypoint SHALL resolve a public subcommand or concrete task to one protected member, optional public extension entrypoint, or CLI surface and proceed by default.

#### Scenario: User invokes public subcommand
- **WHEN** the user supplies `$isomer-op-entrypoint use <subcommand> to <task>`
- **THEN** the entrypoint resolves the public subcommand and proceeds through the matching route

#### Scenario: Invocation is empty
- **WHEN** the user invokes `$isomer-op-entrypoint` without a task or subcommand
- **THEN** the entrypoint executes `help`
- **AND** it presents public commands and visible usage paths without instructing direct protected invocation

#### Scenario: Concrete task has no subcommand
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
The entrypoint SHALL index core protected operator, service, and shared areas while preserving each logical capability's owner boundary.

#### Scenario: Operator routes are indexed
- **WHEN** the entrypoint route table is inspected
- **THEN** it contains scoped members for welcome, Project lifecycle, GUI, identity, system-skill management, Toolbox management, Topic creation, Topic management, and Topic Team Specialization
- **AND** each maps to its preserved `isomer-op-*` logical id

#### Scenario: Service routes are bounded
- **WHEN** service support is needed
- **THEN** the entrypoint or selected operator member routes through the applicable `topic-env`, `agent-env`, `package-repo`, `houmao`, or `topic-service` protected member
- **AND** public guidance does not present an `isomer-srv-*` capability as a normal first-click skill

#### Scenario: Shared routes are explicit
- **WHEN** bounded-run, NVIDIA, package-specific, tool-pack, research-idea, or operation-set support is needed
- **THEN** routing uses the applicable protected shared member
- **AND** package mutation remains with its owning operator or service workflow

#### Scenario: Retired routes are excluded
- **WHEN** active guidance is inspected
- **THEN** it does not present retired topic workspace, topic preparation, manual session, operator Houmao, admin, or research-v1 names as active routes

### Requirement: Entrypoint Includes Extension Skill Routing
The core entrypoint SHALL route optional research paradigms through their public extension entrypoints and SHALL NOT directly expose their protected stage members to users.

#### Scenario: Extension entrypoints are indexed
- **WHEN** entrypoint references are inspected
- **THEN** they identify `isomer-ext-deepsci-entrypoint` and `isomer-ext-kaoju-entrypoint`, their extension ids, and their package-derived public command summaries

#### Scenario: Prepared DeepSci task is selected
- **WHEN** a task maps to DeepSci and required readiness exists
- **THEN** the core entrypoint routes the task to `isomer-ext-deepsci-entrypoint`
- **AND** the extension parent selects the matching protected DeepSci member while preserving its callbacks, preflight, output policy, bindings, and blocker rules

#### Scenario: Prepared Kaoju task is selected
- **WHEN** a task maps to Kaoju and required readiness exists
- **THEN** the core entrypoint routes the task to `isomer-ext-kaoju-entrypoint`
- **AND** the extension parent preserves the selected survey intent and protected member boundaries

#### Scenario: Extension is unavailable
- **WHEN** a concrete task maps to an optional extension that is not declared or host-usable
- **THEN** the core entrypoint routes extension reconciliation through its protected `system-skills` member
- **AND** it resumes the public extension entrypoint after successful reconciliation

### Requirement: Entrypoint Validation
The repository SHALL validate `isomer-op-entrypoint` as a public pack and protected routing contract.

#### Scenario: Valid core pack passes
- **WHEN** operator skill validation runs
- **THEN** it checks public invocation, empty-help behavior, route-and-proceed language, protected inventory, member mappings, CLI routes, extension entrypoints, object notation, service boundaries, shared boundaries, and retired-route exclusions

#### Scenario: Direct protected public route is introduced
- **WHEN** active entrypoint guidance tells a user to invoke a protected logical id directly
- **THEN** validation reports the route and its required parent form

#### Scenario: Protected member coverage is incomplete
- **WHEN** a manifest core member is missing from the parent route table or a parent route lacks manifest metadata
- **THEN** validation fails with the member or route identity

### Requirement: Entrypoint Routes Toolbox Tasks
The public core entrypoint SHALL route project-local Toolbox tasks through protected member `toolbox`, whose logical id remains `isomer-op-toolbox-mgr`.

#### Scenario: Toolbox command is selected
- **WHEN** a user asks to create, convert, install, inspect, update, disable, uninstall, or explain a Project-local Toolbox
- **THEN** the entrypoint invokes `isomer-op-entrypoint->toolbox` and proceeds under the Toolbox Manager contract

#### Scenario: Toolbox and tool packs stay distinct
- **WHEN** a request concerns named dependency bundles rather than Toolbox configuration
- **THEN** the entrypoint may route to protected member `tool-packs`
- **AND** it does not conflate that helper with Toolbox management

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
