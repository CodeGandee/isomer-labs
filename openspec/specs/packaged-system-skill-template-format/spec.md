## Purpose

Define the current structural template and validation scope for active packaged Isomer system skills and their executable subpages.
## Requirements
### Requirement: Active Packaged Skill Scope
The system SHALL derive current-template conformance scope from every public welcome, public entrypoint, and protected subskill declared by the packaged system-skill manifest.

#### Scenario: Manifest pack is audited
- **WHEN** template conformance validation reads manifest v4
- **THEN** it audits every declared public skill and every protected subskill regardless of whether the pack is core or optional
- **AND** it does not infer active scope only from the designated entrypoint

#### Scenario: Public welcome resources are audited
- **WHEN** a welcome skill owns active command or reference pages
- **THEN** validation classifies those pages as active newcomer guidance
- **AND** it validates them independently from the sibling entrypoint's resources

#### Scenario: Historical or passive material is present
- **WHEN** a declared skill contains provenance under `org/`, migration notes under `migrate/`, or passive output material under `templates/`
- **THEN** template conformance validation does not classify that material as active packaged skill instructions

#### Scenario: Nested path is undeclared
- **WHEN** a `subskills/` directory contains an undeclared skill bundle
- **THEN** validation reports the undeclared path rather than silently treating it as active or ignoring it

### Requirement: Current-Template Skill Entrypoints
Every public pack and protected subskill `SKILL.md` SHALL conform to the current entrypoint template, and every page that uses object invocation notation SHALL declare the standard notation frontmatter.

#### Scenario: Public entrypoint is inspected
- **WHEN** a public pack `SKILL.md` is validated
- **THEN** its trigger description, Overview, When to Use, numbered Workflow, Subcommands or Subskills routing, and negative-only Guardrails conform to the current template
- **AND** empty invocation routes to help

#### Scenario: Protected entrypoint is inspected
- **WHEN** a declared protected member `SKILL.md` is validated
- **THEN** it follows the same structural template and preserves its logical-id frontmatter name
- **AND** it does not advertise itself as an independently installed public skill

#### Scenario: Object notation appears
- **WHEN** an active `SKILL.md`, command page, or reference page uses `X->Y`, `X->cmd()`, `X->parent()->child()`, or an equivalent object designator
- **THEN** its YAML frontmatter contains the exact standard `skill_invocation_notation` value
- **AND** bare components identify skill or subskill entrypoints while every parenthesized component identifies a subcommand

#### Scenario: Object notation has the wrong component form
- **WHEN** an active page writes a skill or subskill entrypoint with `()`, writes any object-style subcommand without `()`, or appends a bare component after a command component
- **THEN** `pixi run validate-skills` reports the file, designator, inferred declared kind, and required canonical form

#### Scenario: Nested command chain is inspected
- **WHEN** an active page invokes `X->parent()->child()`
- **THEN** the parent command page declares `child()` as a direct child and defines the generator context inherited by the child
- **AND** the child and its support files remain inside the containing skill or subskill's resource boundary

### Requirement: Current-Template Workflows
Every active packaged skill entrypoint and executable subpage SHALL present `## Workflow` as ordered numbered steps, keep detailed branches in named detail sections or bounded nested lists, and end with a fallback that uses the agent's native planning tool when the request does not map cleanly to the default steps.

#### Scenario: Entrypoint workflow is validated
- **WHEN** validation inspects an active `SKILL.md`
- **THEN** the entrypoint has numbered workflow steps and a freeform fallback

#### Scenario: Executable subpage workflow is validated
- **WHEN** a parent skill routes a command or procedure to an active subpage, or an active subpage declares `## Workflow`
- **THEN** that page has numbered workflow steps and a freeform fallback

#### Scenario: Explanatory reference page is inspected
- **WHEN** an active reference page contains no routed command, procedure, or workflow
- **THEN** validation does not require artificial entrypoint or executable-workflow sections on that page

### Requirement: Template Migration Preserves Skill Interfaces
Migration into protected subskills SHALL preserve each capability's behavior while intentionally replacing its standalone public invocation and path contracts with parent routing.

#### Scenario: Flat skill is migrated
- **WHEN** an existing skill bundle moves below an owning public pack
- **THEN** its purpose, trigger boundary, internal subcommands, resources, callbacks, domain terminology, approval rules, output contract, evidence requirements, and stop conditions remain intact
- **AND** active user guidance replaces direct `$<protected-logical-id>` prompts with the owning public entrypoint form

#### Scenario: Nested subcommands are migrated
- **WHEN** an existing parent command exposes child commands
- **THEN** migration preserves the parent-child command hierarchy, generator context, standalone parent behavior, and complete parenthesized invocation chain
- **AND** it does not flatten the children or convert the parent into a subskill unless the parent command family needs its own private resource bundle

#### Scenario: Pipeline becomes extension entrypoint
- **WHEN** a DeepSci or Kaoju pipeline bundle is migrated
- **THEN** its accepted public commands and workflow semantics move to the matching `isomer-ext-*-entrypoint`
- **AND** no extra protected pipeline facade is created

#### Scenario: Positive guardrail duplicates authoritative guidance
- **WHEN** a positive Guardrails bullet repeats complete guidance already present in an authoritative substantive section
- **THEN** the duplicate bullet is removed without creating another copy

### Requirement: Manifest-Aware Template Validation
The repository SHALL validate public skill roles, protected nesting, and role-specific formatting from the packaged manifest rather than a hard-coded skill inventory.

#### Scenario: Manifest public record drives validation
- **WHEN** a public skill record has role `welcome`
- **THEN** validation applies common skill structure plus the welcome teaching, command-map, read-only, and handoff rules
- **AND** it does not require the route-and-proceed execution contract

#### Scenario: Entrypoint record drives validation
- **WHEN** a public skill record has role `entrypoint`
- **THEN** validation applies route-and-proceed, protected inventory, public command, callback, and invocation-notation rules
- **AND** it does not require copied welcome teaching resources

#### Scenario: Protected record drives validation
- **WHEN** a protected capability record is encountered
- **THEN** validation recursively inspects its frontmatter, workflow, local resources, parent invocation designator, dependencies, and version
- **AND** it rejects a protected member that is also projected as an undeclared public skill

#### Scenario: Protected member is malformed
- **WHEN** a nested member has invalid frontmatter, workflow, Guardrails, resources, member mapping, or object notation
- **THEN** `pixi run validate-skills` fails with the public pack, logical id, file, and violated rule

#### Scenario: Parent omits declared member
- **WHEN** a manifest-declared protected member is absent from the parent route table
- **THEN** validation fails with the pack and missing scoped member

#### Scenario: Public guidance invokes protected skill directly
- **WHEN** active public guidance uses `$<protected-logical-id>` outside bounded migration text or a logical-id CLI field
- **THEN** validation reports the stale direct invocation and its owning public entrypoint

#### Scenario: Old-template section is introduced
- **WHEN** an active packaged skill page introduces a prohibited old-template heading or malformed current-template section
- **THEN** `pixi run validate-skills` fails with the affected file and rule

#### Scenario: Excluded material retains historical wording
- **WHEN** excluded provenance, migration, or passive-template material contains old direct invocation text
- **THEN** validation does not report an active-template violation for that material

#### Scenario: Non-prohibition Guardrails bullet is introduced
- **WHEN** an active packaged skill page contains a top-level Guardrails bullet that does not begin with `DO NOT`
- **THEN** `pixi run validate-skills` fails with the affected file and negative-only Guardrails rule

### Requirement: Public Entrypoints Explain Protected-Subskill Selection
Every public packaged system-skill entrypoint that owns protected subskills SHALL include a `When to Route Here` column in its `## Protected Subskills` table and SHALL provide one substantive routing sentence for every manifest-declared protected member. Each sentence SHALL express the decisive parent selection condition in the context of the owning entrypoint, SHALL preserve material boundaries with adjacent routes, and SHALL leave the protected member's detailed workflow contract authoritative.

#### Scenario: Protected member table is inspected
- **WHEN** a public entrypoint owns manifest-declared protected members
- **THEN** its protected-subskill table contains exactly one row and one `When to Route Here` sentence for every declared member
- **AND** the sentence gives the entrypoint enough information to select that member before loading its full `SKILL.md`

#### Scenario: Parent context already establishes the extension
- **WHEN** a DeepSci or Kaoju entrypoint summarizes one of its protected members
- **THEN** the routing sentence omits redundant pack context and focuses on the task condition or boundary that distinguishes the member
- **AND** it does not simply copy the protected member's frontmatter description or agent short description

#### Scenario: Protected workflow is selected
- **WHEN** the entrypoint selects a protected member using its routing sentence
- **THEN** it loads and follows the protected member's complete triggers, gates, callbacks, inputs, outputs, blockers, and handoffs
- **AND** it does not treat the parent sentence as a replacement workflow contract

#### Scenario: Protected visibility is preserved
- **WHEN** routing guidance names a protected member
- **THEN** the guidance describes when the parent routes internally to that member
- **AND** it does not advertise the member as an independently user-invokable or host-discoverable skill

### Requirement: Protected-Subskill Routing Guidance Is Validated
The packaged system-skill validator SHALL validate protected-subskill routing-table coverage, sentence shape, substance, and source adaptation through the existing all-skills validation command and SHALL report file-specific diagnostics.

#### Scenario: Routing column or member sentence is missing
- **WHEN** a public entrypoint omits the `When to Route Here` column or any declared protected member lacks one populated routing sentence
- **THEN** `pixi run validate-skills` fails with the affected entrypoint and member

#### Scenario: Routing cell is not one substantive sentence
- **WHEN** a routing cell is empty, contains only a short category phrase, or contains multiple logical sentences
- **THEN** `pixi run validate-skills` fails with a routing-guidance diagnostic

#### Scenario: Routing sentence copies member metadata
- **WHEN** a routing sentence equals the protected member's frontmatter description or agent short description after superficial normalization
- **THEN** `pixi run validate-skills` fails and requires a parent-contextual rewrite

#### Scenario: Context-aware routing table is complete
- **WHEN** every declared protected member has one valid, adapted routing sentence and all existing table identities and designators remain correct
- **THEN** protected-subskill routing-guidance validation passes

### Requirement: Welcome Skills Use a Newcomer Teaching Format
Every public welcome `SKILL.md` SHALL use a concise progressive-disclosure format that introduces typical use cases before exhaustive command detail.

#### Scenario: Welcome entrypoint is inspected
- **WHEN** a public welcome `SKILL.md` is inspected
- **THEN** it contains `## Overview`, `## When to Use`, a near-top numbered `## Workflow`, a typical-use-case surface, a complete command-map route, an output contract, and exactly one negative-only `## Guardrails`
- **AND** it links only the selected one-level command or reference resources needed for each route

#### Scenario: Typical use-case table is inspected
- **WHEN** a welcome use-case table or equivalent structured section is inspected
- **THEN** every row has a one-sentence use condition, representative routing cues, required context, canonical entrypoint route, exact example, expected action, mutation posture, and next step
- **AND** the prose is adapted to the welcome context instead of duplicating source metadata verbatim

#### Scenario: Complete map follows progressive disclosure
- **WHEN** a welcome skill documents the sibling entrypoint's full command inventory
- **THEN** the exhaustive map is loaded only through `show-command-map`, `help`, or an explicit complete-output request
- **AND** default welcome output remains a concise selection of high-value patterns

