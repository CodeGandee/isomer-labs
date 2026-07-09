# isomer-op-entrypoint-skill Specification

## Purpose
TBD - created by archiving change add-isomer-op-entrypoint-skill. Update Purpose after archive.
## Requirements
### Requirement: Entrypoint Operator Skill Inventory
The system SHALL provide `isomer-op-entrypoint` as an active Project Operator Session and Operator Agent skill for informed-user task routing across Isomer system skills and CLI surfaces.

#### Scenario: Entrypoint skill assets exist
- **WHEN** the packaged operator skillset is inspected
- **THEN** it contains `operator/isomer-op-entrypoint/SKILL.md`
- **AND** it contains `operator/isomer-op-entrypoint/agents/openai.yaml`
- **AND** it contains directly linked local reference pages for routing rules, system skill indexes, CLI indexes, input surfaces, and extension skills

#### Scenario: Entrypoint identity is consistent
- **WHEN** `operator/isomer-op-entrypoint` is inspected
- **THEN** the folder name, `SKILL.md` frontmatter `name`, `agents/openai.yaml` display name, and default prompt use `isomer-op-entrypoint`
- **AND** the frontmatter description identifies the skill as an entrypoint to system skills and Isomer CLI functionality

#### Scenario: Entrypoint has a workflow-shaped skill body
- **WHEN** `operator/isomer-op-entrypoint/SKILL.md` is inspected
- **THEN** it has a near-top `## Workflow` section with numbered steps
- **AND** the workflow tells the agent to parse the user task, perform safe context discovery when useful, classify a route, load the selected route reference or owner skill, proceed with the chosen route, and report the result
- **AND** it includes a fallback for tasks that do not map cleanly to the default steps

### Requirement: Entrypoint Routes Then Proceeds
The entrypoint SHALL choose the next Isomer system skill or CLI surface from the user's task and proceed with that selected route by default.

#### Scenario: Concrete task is executed through selected route
- **WHEN** the user gives a concrete task, prompt, or file and does not ask only for help or explanation
- **THEN** the entrypoint selects one owner skill, extension skill, or CLI command family
- **AND** it proceeds with that route or reports a blocker that prevents safe execution
- **AND** it does not stop after only listing possible routes

#### Scenario: Explanation-only task stays non-mutating
- **WHEN** the user asks only what route to use, how Isomer routing works, or what options exist
- **THEN** the entrypoint may answer with a routing explanation
- **AND** it does not run mutating commands or invoke mutating owner workflows

#### Scenario: Ambiguous mutation uses read-only preflight first
- **WHEN** the user request implies action but lacks enough Project, Topic, actor, agent, or workspace context
- **THEN** the entrypoint uses read-only context commands or existing prompt evidence before mutation
- **AND** it asks for missing information or reports a blocker when the selected route cannot be resolved safely

### Requirement: Entrypoint Indexes All System Skill Families
The entrypoint SHALL include route guidance for operator, service, misc, and extension system skills while preserving their ownership boundaries.

#### Scenario: Operator owner routes are indexed
- **WHEN** the entrypoint skill index is inspected
- **THEN** it lists active operator routes for welcome, project lifecycle, topic creation, initialized-topic management, identity switching, and Topic Team Specialization
- **AND** it distinguishes `isomer-op-welcome` as read-only orientation from `isomer-op-entrypoint` as route-and-proceed dispatch

#### Scenario: Service skill routes are bounded
- **WHEN** service skills are mentioned in entrypoint guidance
- **THEN** the guidance identifies them as bounded support routes
- **AND** normal project, topic, environment, Houmao, or agent workspace requests route through the owning operator workflow before service delegation unless the user explicitly invokes a service skill

#### Scenario: Misc helper routes are explicit
- **WHEN** misc skills are mentioned in entrypoint guidance
- **THEN** `isomer-misc-tool-packs` is treated as an explicit named helper route rather than an automatic package mutation route
- **AND** package install, update, or removal requests for a Topic Workspace remain routed to the owning topic or environment setup workflow

#### Scenario: Retired routes are excluded
- **WHEN** active entrypoint guidance is inspected
- **THEN** it does not present `isomer-op-topic-workspace-mgr`, `isomer-op-topic-prepare`, `isomer-op-manual-research-session`, `isomer-op-houmao-interop`, or `isomer-admin-*` names as active invokable routes

### Requirement: Entrypoint Includes Extension Skill Routing
The entrypoint SHALL treat domain extension skills, including production DeepSci skills, as first-class system-skill routes.

#### Scenario: DeepSci extension index exists
- **WHEN** entrypoint references are inspected
- **THEN** they include DeepSci extension routes for workspace bootstrap, pipeline passes, scouting, baselines, ideation, optimization, experiments, analysis, decisions, finalization, science checks, writing, review, rebuttal, plotting, figure polish, Nature data, Nature figures, paper-to-PPT, and Nature-style polishing

#### Scenario: Prepared research-stage task routes to DeepSci
- **WHEN** the user asks for research-stage work and the Topic Workspace has the required readiness or the prompt supplies accepted DeepSci context
- **THEN** the entrypoint routes to the matching `isomer-deepsci-*` skill or `isomer-deepsci-pipeline`
- **AND** it preserves that skill's callbacks, latest-context preflight, worker-output policy, placeholder binding, and blocker rules

#### Scenario: Missing DeepSci readiness routes to setup
- **WHEN** the user asks for DeepSci research work but required Topic Workspace, Topic Actor, Agent Workspace, or DeepSci bootstrap readiness is missing
- **THEN** the entrypoint routes to `isomer-op-topic-creator`, `isomer-op-topic-mgr`, `isomer-op-topic-team-specialize`, `isomer-srv-agent-env-setup` through its owner, or `isomer-deepsci-workspace-mgr` as appropriate
- **AND** it does not let an ordinary research-stage skill fabricate missing readiness

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
The repository SHALL validate `isomer-op-entrypoint` as a routing contract, not merely as a generic skill folder.

#### Scenario: Entrypoint validator accepts valid skill
- **WHEN** operator skill validation runs against a valid `isomer-op-entrypoint`
- **THEN** validation passes the entrypoint's frontmatter, manifest, workflow, local references, output contract, route-and-proceed language, active owner routes, extension routes, CLI routes, service boundary, misc boundary, retired-route exclusions, and global `isomer-cli` command guidance

#### Scenario: Entrypoint validator rejects stale or unsafe routes
- **WHEN** active entrypoint guidance presents retired operator skills, old admin names, service skills as normal first-click owner routes, or `pixi run isomer-cli` command guidance
- **THEN** operator skill validation reports diagnostics

#### Scenario: Entrypoint validator rejects missing extension coverage
- **WHEN** active entrypoint guidance omits DeepSci extension-skill routing
- **THEN** operator skill validation reports that extension skill coverage is incomplete

