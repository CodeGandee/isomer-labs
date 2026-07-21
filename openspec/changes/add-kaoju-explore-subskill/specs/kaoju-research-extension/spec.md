# kaoju-research-extension Delta Specification

## MODIFIED Requirements

### Requirement: Production Kaoju Skill Family
The package SHALL provide a self-contained production Kaoju pack with independent public welcome and execution entrypoint bundles plus the existing protected `isomer-kaoju-<purpose>` capabilities.

#### Scenario: Kaoju public pair exists
- **WHEN** packaged Kaoju assets are inspected
- **THEN** sibling bundles `isomer-ext-kaoju-welcome` and `isomer-ext-kaoju-entrypoint` contain valid public skill metadata
- **AND** the fourteen current Kaoju capabilities remain protected below the entrypoint

#### Scenario: Kaoju welcome is self-contained
- **WHEN** `isomer-ext-kaoju-welcome` is copied or linked as part of the pack
- **THEN** it resolves its active typical-use-case and command-map resources without loading private files from the entrypoint or protected subskills
- **AND** it may reference public entrypoint invocation names without becoming an execution owner

#### Scenario: Shared machine contracts remain package-owned
- **WHEN** welcome or entrypoint needs current Kaoju command or process metadata
- **THEN** checked machine contracts remain owned by the installed Kaoju Python package and manifest
- **AND** welcome does not introduce a second survey-process registry

#### Scenario: Exact production inventory exists
- **WHEN** the packaged Kaoju root is inspected
- **THEN** it contains public directory `isomer-ext-kaoju-entrypoint`
- **AND** that pack contains protected bundles for `isomer-kaoju-shared`, `isomer-kaoju-workspace-mgr`, `isomer-kaoju-frame`, `isomer-kaoju-discover`, `isomer-kaoju-acquire`, `isomer-kaoju-examine`, `isomer-kaoju-reproduce`, `isomer-kaoju-trial`, `isomer-kaoju-compare`, `isomer-kaoju-audit`, `isomer-kaoju-synthesize`, `isomer-kaoju-write`, `isomer-kaoju-export`, and `isomer-kaoju-explore`
- **AND** no `isomer-kaoju-pipeline` skill folder or duplicate facade is active

#### Scenario: Public identity is consistent
- **WHEN** the Kaoju public pack is inspected
- **THEN** its folder, frontmatter, metadata, and public default prompt use `isomer-ext-kaoju-entrypoint`

#### Scenario: Protected identity is consistent
- **WHEN** a protected Kaoju bundle is inspected
- **THEN** its folder and frontmatter retain its `isomer-kaoju-*` logical id
- **AND** its active resources remain self-contained

#### Scenario: Trial and reproduction remain distinct
- **WHEN** executable evidence members are inspected
- **THEN** `trial` maps to `isomer-kaoju-trial` and `reproduce` maps to `isomer-kaoju-reproduce`
- **AND** neither capability weakens the accepted evidence distinction

#### Scenario: Artifact identity is consistent
- **WHEN** a protected Kaoju member names a durable extension artifact
- **THEN** it continues to use the exact registered `KAOJU:WHAT` identifier

### Requirement: Kaoju Pipeline Command Surface
`isomer-ext-kaoju-entrypoint` SHALL remain the single Kaoju execution entrypoint, and `isomer-ext-kaoju-welcome` SHALL provide a separate read-only teaching surface for its survey intents, compatibility procedures, exploration procedures, and grouped managers.

#### Scenario: Concrete Kaoju task uses entrypoint
- **WHEN** a user requests reading-list work, source ingestion, direction selection, comparison, code preparation, trial execution, paper production, wiki export, or task planning
- **THEN** `isomer-ext-kaoju-entrypoint` selects and executes the applicable public command or protected capability
- **AND** existing interaction, evidence, Gate, checkpoint, and terminal contracts remain in force

#### Scenario: Newcomer asks how to use Kaoju
- **WHEN** a user asks what Kaoju is designed for, which procedure fits, or how to form a request
- **THEN** `isomer-ext-kaoju-welcome` presents curated typical use cases and exact entrypoint examples
- **AND** it does not run a Kaoju manager or research procedure

#### Scenario: Historical pipeline identity is used
- **WHEN** compatibility lookup encounters `isomer-kaoju-pipeline`
- **THEN** it resolves to `isomer-ext-kaoju-entrypoint`
- **AND** it does not resolve to the welcome skill

#### Scenario: Nested manager form is taught
- **WHEN** welcome explains a grouped manager or nested subcommand such as paper-template management
- **THEN** it shows the accepted public entrypoint command form and representative task
- **AND** it does not expose internal object-generator notation as the ordinary user invocation

#### Scenario: Survey-process commands match ten use cases
- **WHEN** public help is inspected
- **THEN** it exposes `choose-directions`, `build-reading-list`, `ingest-reading-item`, `draft-paper`, `manage-paper-template`, `build-paper-pdf`, `export-survey-wiki`, `ingest-source-code`, `prepare-code-run`, and `run-code-trial`
- **AND** each command page preserves its bounded recipe, owners, decisions, durable outputs, terminal states, and resume inputs

#### Scenario: Exploration procedure is public
- **WHEN** public help or the command map is inspected
- **THEN** it exposes `explore` as an exploration procedure
- **AND** `explore` routes to the protected `isomer-kaoju-explore` member
- **AND** the `explore` command page delegates interactive planning to that member and routes to the selected command after consent

#### Scenario: Existing procedures remain callable
- **WHEN** compatibility procedures are inspected
- **THEN** the accepted landscape, intake, expansion, theory comparison, method trial, comparative, audit, paper, and template procedures remain public commands of the new entrypoint

#### Scenario: CRUD actions remain grouped by object
- **WHEN** manager actions are inspected
- **THEN** survey and dataset actions remain grouped under their accepted public manager commands

#### Scenario: Paper-template actions remain grouped by object
- **WHEN** the role-aware paper-template manager is migrated into the public pack
- **THEN** `manage-paper-template()` remains one parent command with declared children `list()`, `show()`, `create()`, `copy()`, `update()`, `replace()`, `merge()`, `file()`, `metadata()`, `export()`, `observe()`, `archive()`, `delete()`, and `migrate()`
- **AND** `file()` declares `put()` and `remove()` children while `metadata()` declares `patch()`
- **AND** internal routes may use complete chains such as `isomer-ext-kaoju-entrypoint->manage-paper-template()->file()->put()`

#### Scenario: Paper-template role remains command context
- **WHEN** a paper-template action selects content authoring or LaTeX presentation state
- **THEN** the manager resolves explicit `--kind content|latex` context before role-local discovery or mutation
- **AND** content and LaTeX do not become skills, subskills, or command-path components

#### Scenario: Compatibility template creation remains content-only
- **WHEN** the retained `create-paper-template` procedure is invoked
- **THEN** it creates or updates a named content template backed by `KAOJU:PAPER-TEMPLATE-MYST`
- **AND** LaTeX stock creation routes through `manage-paper-template()` with `--kind latex`

#### Scenario: Interaction and resume stay out of the procedure list
- **WHEN** a user requests clarification before work or resumes accepted prior state
- **THEN** clarification-first is represented as an interaction mode shared by procedures
- **AND** resume is represented by a Research Task, Run checkpoint, accepted input refs, and starting stage rather than a separate procedure

#### Scenario: Generic maintenance remains absent
- **WHEN** the public command list is inspected
- **THEN** it excludes standalone source-audit, repository-refresh, generic environment-repair, full-Kaoju, resume, and list-passes commands

#### Scenario: Empty invocation uses help
- **WHEN** the public entrypoint is invoked without a task or command
- **THEN** it executes help and reports the public command groups including survey intents, compatibility procedures, exploration procedures, and grouped managers
