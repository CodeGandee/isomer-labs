## ADDED Requirements

### Requirement: Imsight Entrypoint Filenames Express Skill Scope
The Imsight skill-authoring convention SHALL use `SKILL.md` for host-discoverable skill roots, SHALL use `SKILL-MAIN.md` for parent-scoped subskill entrypoints, and SHALL use a non-`SKILL.md` filename for preserved non-executable source snapshots.

#### Scenario: Top-level skill is authored
- **WHEN** creation, formatting, or migration writes a standalone or host-discoverable skill root
- **THEN** its entrypoint is `SKILL.md`
- **AND** ordinary host discovery can register that root

#### Scenario: Parent-scoped subskill is authored
- **WHEN** a skill owns a child at `subskills/<subskill-name>/`
- **THEN** the child entrypoint is `subskills/<subskill-name>/SKILL-MAIN.md`
- **AND** that child directory does not contain `SKILL.md`

#### Scenario: Legacy subskill is inspected or migrated
- **WHEN** an existing parent-scoped child contains `SKILL.md` but not `SKILL-MAIN.md`
- **THEN** Imsight inspection and migration guidance may read it as a legacy subskill entrypoint
- **AND** creation or formatting normalizes the parent-scoped output to `SKILL-MAIN.md`

#### Scenario: Entrypoint candidates conflict
- **WHEN** a target skill folder contains both `SKILL.md` and `SKILL-MAIN.md`
- **THEN** the workflow reports an ambiguous scope contract and does not choose one silently

#### Scenario: Upstream entrypoint is preserved for provenance
- **WHEN** refactor-migration copies a source skill entrypoint under the target's non-executable provenance tree
- **THEN** the copied file uses `SKILL-SOURCE.md`
- **AND** recursive exact-`SKILL.md` discovery does not register the snapshot

## MODIFIED Requirements

### Requirement: Parent Skills Explain Subskill Selection
The Imsight skill-authoring convention SHALL require every skill that bundles subskills to provide one parent-oriented routing sentence for each direct subskill in the parent's role-canonical entrypoint. The sentence SHALL explain when the parent entrypoint routes to that subskill, SHALL adapt authoritative child trigger guidance to context already established by the parent, and SHALL leave the child subskill's complete `SKILL-MAIN.md` instructions authoritative.

#### Scenario: Parent skill lists bundled subskills
- **WHEN** a skill owns one or more direct subskills
- **THEN** its `## Subskills` section or combined routing table contains one `When to Route Here` sentence for each direct subskill
- **AND** the sentence provides enough information to distinguish that route from sibling routes before explicitly loading the child's `SKILL-MAIN.md`

#### Scenario: Child trigger metadata contains repeated parent context
- **WHEN** the child frontmatter or `## When to Use` guidance repeats context already established by the parent skill
- **THEN** the parent routing sentence omits that repetition and retains the decisive child-specific trigger or boundary
- **AND** it is not a verbatim copy of the child frontmatter description or agent short description

#### Scenario: Nested subskill owns children
- **WHEN** a bundled subskill owns further subskills
- **THEN** that subskill acts as their parent entrypoint and follows the same routing-sentence and `SKILL-MAIN.md` rule recursively

#### Scenario: Protected child route is described
- **WHEN** a subskill is scoped to its parent and is not independently discovered
- **THEN** the sentence describes parent routing rather than presenting the child as an independent user invocation surface

### Requirement: Imsight Creation and Design Capture Routing Guidance
The `imsight-agent-skill-handling` creation and design guidance SHALL capture a context-aware routing sentence and the role-canonical `SKILL-MAIN.md` entrypoint for each proposed or newly authored subskill and SHALL include that sentence in parent tables and design outputs.

#### Scenario: New skill is created with subskills
- **WHEN** `create` authors a parent skill with bundled subskills
- **THEN** it derives one routing sentence per subskill from the captured intent and child trigger guidance
- **AND** it writes each child entrypoint as `SKILL-MAIN.md` and checks the parent table for complete, context-aware coverage

#### Scenario: Skill design includes subskills
- **WHEN** `design` proposes bundled subskills before creating files
- **THEN** the subskill design table records `When to Route Here` and `SKILL-MAIN.md` for each proposed child
- **AND** the design distinguishes routing guidance from private-resource justification and invocation notation

### Requirement: Imsight Formatting Repairs Routing Guidance
The `imsight-agent-skill-handling` formatting guidance SHALL inspect a parent skill's subskill inventory, SHALL normalize parent-scoped child entrypoints to `SKILL-MAIN.md`, and SHALL add or revise routing sentences when they are missing, non-sentential, redundant with parent context, or copied directly from child metadata.

#### Scenario: Existing parent lists only subskill names or purposes
- **WHEN** `format` inspects a skill whose subskill table lacks usable selection conditions
- **THEN** it reads the affected child entrypoints and writes one context-aware routing sentence per child
- **AND** it preserves invocation designators, resource ownership, trigger boundaries, and public command behavior

#### Scenario: Existing routing guidance is already adequate
- **WHEN** every direct subskill already has one concise parent-oriented selection sentence consistent with its child instructions
- **THEN** `format` preserves the guidance unless a source trigger or structural edit makes it stale

#### Scenario: Legacy child filename is present
- **WHEN** `format` finds a parent-scoped child whose only entrypoint is `SKILL.md`
- **THEN** it renames that entrypoint to `SKILL-MAIN.md` and updates direct local references
- **AND** it does not leave a nested `SKILL.md` compatibility copy

#### Scenario: Formatting validation completes
- **WHEN** `format` finishes a skill with bundled subskills
- **THEN** its final inspection checks complete routing-sentence coverage, role-canonical entrypoint filenames, subskill structure, and invocation notation
