## MODIFIED Requirements

### Requirement: Active Packaged Skill Scope
The system SHALL derive current-template conformance scope from every public pack and protected capability declared in the packaged manifest.

#### Scenario: Manifest pack is audited
- **WHEN** template conformance validation reads the packaged manifest
- **THEN** it audits each public entrypoint and recursively audits every declared protected `subskills/<logical-id>/SKILL.md`
- **AND** it audits their active command, procedure, binding, scenario, and reference pages

#### Scenario: Nested path is undeclared
- **WHEN** a `subskills/` directory contains an undeclared skill bundle
- **THEN** validation reports the undeclared path rather than silently treating it as active or ignoring it

#### Scenario: Historical source copy is present
- **WHEN** a declared pack or member contains copied upstream material below `org/`, migration notes below `migrate/`, or passive output below `templates/`
- **THEN** template validation excludes that material from active instructions

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

### Requirement: Manifest-Aware Template Validation
The repository validator SHALL enforce current-template and protected-routing requirements through the existing all-skills validation command.

#### Scenario: Protected member is malformed
- **WHEN** a nested member has invalid frontmatter, workflow, Guardrails, resources, member mapping, or object notation
- **THEN** `pixi run validate-skills` fails with the public pack, logical id, file, and violated rule

#### Scenario: Parent omits declared member
- **WHEN** a manifest-declared protected member is absent from the parent route table
- **THEN** validation fails with the pack and missing scoped member

#### Scenario: Public guidance invokes protected skill directly
- **WHEN** active public guidance uses `$<protected-logical-id>` outside bounded migration text or a logical-id CLI field
- **THEN** validation reports the stale direct invocation and its owning public entrypoint

#### Scenario: Excluded material retains historical wording
- **WHEN** excluded provenance, migration, or passive-template material contains old direct invocation text
- **THEN** validation does not report an active-template violation for that material
