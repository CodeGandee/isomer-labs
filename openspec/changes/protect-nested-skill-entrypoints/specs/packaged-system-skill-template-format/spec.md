## ADDED Requirements

### Requirement: Template Validation Enforces Discovery-Safe Filenames
The repository SHALL validate entrypoint filenames by manifest role and SHALL reject recursively discoverable `SKILL.md` files that are not declared public roots.

#### Scenario: Public skill filename is validated
- **WHEN** validation inspects a manifest-declared public welcome or execution entrypoint
- **THEN** the bundle must contain `SKILL.md`
- **AND** it must not substitute `SKILL-MAIN.md` for the public entrypoint

#### Scenario: Protected skill filename is validated
- **WHEN** validation inspects a manifest-declared protected capability
- **THEN** the bundle must contain `SKILL-MAIN.md`
- **AND** it must not contain `SKILL.md`

#### Scenario: Provenance snapshot resembles a skill
- **WHEN** `org/`, `migrate/`, `templates/`, or another passive subtree contains a preserved entrypoint document
- **THEN** that document must use a non-`SKILL.md` filename such as `SKILL-SOURCE.md`
- **AND** passive validation exclusion does not permit a host-discovery filename

#### Scenario: Public pack contains an unexpected discovery file
- **WHEN** recursive validation finds a `SKILL.md` below a declared public root other than that root's own entrypoint
- **THEN** `pixi run validate-skills` fails with the public pack and nested file path

## MODIFIED Requirements

### Requirement: Current-Template Skill Entrypoints
Every public pack `SKILL.md` and protected subskill `SKILL-MAIN.md` SHALL conform to the current entrypoint template, and every page that uses object invocation notation SHALL declare the standard notation frontmatter.

#### Scenario: Public entrypoint is inspected
- **WHEN** a public pack `SKILL.md` is validated
- **THEN** its trigger description, Overview, When to Use, numbered Workflow, Subcommands or Subskills routing, and negative-only Guardrails conform to the current template
- **AND** empty invocation routes to help

#### Scenario: Protected entrypoint is inspected
- **WHEN** a declared protected member `SKILL-MAIN.md` is validated
- **THEN** it follows the same structural template and preserves its logical-id frontmatter name
- **AND** it does not advertise itself as an independently installed public skill

#### Scenario: Object notation appears
- **WHEN** an active entrypoint, command page, or reference page uses `X->Y`, `X->cmd()`, `X->parent()->child()`, or an equivalent object designator
- **THEN** its YAML frontmatter contains the exact standard `skill_invocation_notation` value
- **AND** the notice identifies `SKILL.md` for top-level skills, `SKILL-MAIN.md` for parent-selected subskills, bare components for skill paths, and parenthesized components for subcommands

#### Scenario: Object notation has the wrong component form
- **WHEN** an active page writes a skill or subskill entrypoint with `()`, writes any object-style subcommand without `()`, or appends a bare component after a command component
- **THEN** `pixi run validate-skills` reports the file, designator, inferred declared kind, and required canonical form

#### Scenario: Nested command chain is inspected
- **WHEN** an active page invokes `X->parent()->child()`
- **THEN** the parent command page declares `child()` as a direct child and defines the generator context inherited by the child
- **AND** the child and its support files remain inside the containing skill or subskill's resource boundary

### Requirement: Current-Template Workflows
Every active packaged public `SKILL.md`, protected `SKILL-MAIN.md`, and executable subpage SHALL present `## Workflow` as ordered numbered steps, keep detailed branches in named detail sections or bounded nested lists, and end with a fallback that uses the agent's native planning tool when the request does not map cleanly to the default steps.

#### Scenario: Entrypoint workflow is validated
- **WHEN** validation inspects an active public or protected entrypoint
- **THEN** the entrypoint has numbered workflow steps and a freeform fallback

#### Scenario: Executable subpage workflow is validated
- **WHEN** a parent skill routes a command or procedure to an active subpage, or an active subpage declares `## Workflow`
- **THEN** that page has numbered workflow steps and a freeform fallback

#### Scenario: Explanatory reference page is inspected
- **WHEN** an active reference page contains no routed command, procedure, or workflow
- **THEN** validation does not require artificial entrypoint or executable-workflow sections on that page

### Requirement: Public Entrypoints Explain Protected-Subskill Selection
Every public packaged system-skill entrypoint that owns protected subskills SHALL include a `When to Route Here` column in its `## Protected Subskills` table and SHALL provide one substantive routing sentence for every manifest-declared protected member. Each sentence SHALL express the decisive parent selection condition in the context of the owning entrypoint and SHALL preserve material boundaries with adjacent routes. After selecting a row, the public entrypoint SHALL explicitly load the selected member's `SKILL-MAIN.md` and SHALL leave that protected entrypoint's detailed workflow contract authoritative.

#### Scenario: Protected member table is inspected
- **WHEN** a public entrypoint owns manifest-declared protected members
- **THEN** its protected-subskill table contains exactly one row and one `When to Route Here` sentence for every declared member
- **AND** the sentence gives the entrypoint enough information to select that member before loading its full `SKILL-MAIN.md`

#### Scenario: Parent context already establishes the extension
- **WHEN** a DeepSci or Kaoju entrypoint summarizes one of its protected members
- **THEN** the routing sentence omits redundant pack context and focuses on the task condition or boundary that distinguishes the member
- **AND** it does not simply copy the protected member's frontmatter description or agent short description

#### Scenario: Protected workflow is selected
- **WHEN** the entrypoint selects a protected member using its routing sentence
- **THEN** it resolves the manifest-declared nested directory and loads only that member's `SKILL-MAIN.md` plus directly required bundle-local resources
- **AND** it follows the protected member's complete triggers, gates, callbacks, inputs, outputs, blockers, and handoffs rather than treating the parent sentence as a replacement workflow contract

#### Scenario: Protected visibility is preserved
- **WHEN** routing guidance names a protected member
- **THEN** the guidance describes when the parent routes internally to that member
- **AND** it does not advertise the member as an independently user-invokable or host-discoverable skill
