## ADDED Requirements

### Requirement: Topic Team Specialization Uses Semantic Workspace Surfaces
The Topic Team Specialization module skill SHALL consume and report workspace setup through semantic labels instead of treating default directory paths as the contract.

#### Scenario: Setup agent workspace requests semantic setup
- **WHEN** `setup-agent-workspace` determines that a specialized topic team needs Git-backed Agent Workspaces
- **THEN** it delegates to `isomer-admin-topic-workspace-mgr` with semantic surface expectations for Topic Main Repository and Agent Workspace preparation

#### Scenario: Delegated output records labels
- **WHEN** delegated Agent Workspace setup completes
- **THEN** `setup-agent-workspace` records the returned semantic labels, resolved paths, sources, Agent Names, branch namespaces, boundary material, validation refs, blockers, and next actions as static setup evidence

#### Scenario: Custom layout evidence is accepted
- **WHEN** delegated setup evidence shows safe manifest-backed paths that differ from `repos/topic-main` or `agents/<agent-name>`
- **THEN** the skill accepts the evidence when the semantic labels, ownership, and validation status are correct

#### Scenario: Hard-coded default-only evidence is insufficient
- **WHEN** setup evidence only says that default-looking directories exist without semantic label or manifest-backed validation
- **THEN** the skill reports the evidence as incomplete for static readiness

### Requirement: Topic Team Summaries Are Semantic Label First
The Topic Team Specialization module skill SHALL write summaries that name semantic workspace surfaces before concrete default paths.

#### Scenario: Final summary reports semantic layout
- **WHEN** `finalize-topic-team` writes or updates `isomer-topic-summary.md`
- **THEN** the Agent Workspace layout section reports semantic labels, Agent Names, resolved paths, path sources, Git branch plans, and validation status

#### Scenario: Default layout is described as default profile
- **WHEN** a summarized path comes from the built-in default layout
- **THEN** the summary identifies it as `isomer-default.v1` rather than implying that fixed paths are the workspace contract

#### Scenario: Custom layout remains understandable
- **WHEN** a summarized path differs from the default layout
- **THEN** the summary explains which semantic label the path satisfies and does not treat the path difference as a blocker by itself

### Requirement: Cwd-friendly Agent Guidance
The Topic Team Specialization module skill SHALL teach prepared agents to query their own Agent Workspace surfaces by semantic label from cwd.

#### Scenario: Boundary notes include self queries
- **WHEN** the skill records or summarizes Agent Workspace boundary material
- **THEN** it includes guidance that an agent running inside its own Agent Workspace can query agent-scoped labels without passing Agent Name

#### Scenario: Cross-agent queries remain explicit
- **WHEN** the skill describes peer inspection or integration behavior
- **THEN** it states that querying another agent's surface still requires an explicit Agent Name, Agent Instance, handoff, Artifact, or boundary-approved share

#### Scenario: Cwd inference is not security
- **WHEN** the skill describes cwd-derived agent context
- **THEN** it states that cwd inference is a convenience for path resolution and not filesystem-grade identity or access control

### Requirement: Static Readiness Checks Semantic Bindings
The Topic Team Specialization module skill SHALL validate static readiness against semantic workspace bindings when Agent Workspace setup is in scope.

#### Scenario: Missing required label blocks readiness
- **WHEN** the specialized team requires Agent Workspace setup and a required semantic label cannot be resolved
- **THEN** `validate-topic-team` reports an Agent Workspace setup blocker

#### Scenario: Manifest diagnostics remain visible
- **WHEN** Topic Workspace Manifest validation reports duplicate labels, unsafe paths, or unresolved agent templates
- **THEN** `validate-topic-team` includes those diagnostics in static readiness output

#### Scenario: Runtime readiness is not implied
- **WHEN** semantic workspace setup evidence is valid
- **THEN** the skill still does not claim Agent Team Instance creation, Workspace Runtime mutation, adapter preflight, or live launch readiness
