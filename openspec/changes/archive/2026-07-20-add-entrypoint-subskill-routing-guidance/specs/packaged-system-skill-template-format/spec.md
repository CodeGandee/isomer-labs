## ADDED Requirements

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
