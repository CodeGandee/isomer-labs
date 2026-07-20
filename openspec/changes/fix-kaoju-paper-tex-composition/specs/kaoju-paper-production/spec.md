# kaoju-paper-production Delta: fix-kaoju-paper-tex-composition

## ADDED Requirements

### Requirement: Venue LaTeX Template Adoption Packs Full Template Content
The system SHALL adopt a LaTeX venue template by packing the complete actor-selected template tree (entrypoint source, class files, included files, assets) into managed artifact storage, and SHALL reject placeholder or reference-only shims presented as a venue template.

#### Scenario: Actor adopts a real template tree
- **WHEN** the actor selects a template directory and says it is the venue template to store
- **THEN** the template procedure copies the whole directory content into managed storage and creates the template record with per-file checksums and authored metadata
- **AND** the stored entrypoint is the actual venue template source, usable for composition without external lookup

#### Scenario: A shim is presented as a venue template
- **WHEN** the candidate directory's entrypoint is a short hand-written file that merely names or checksums an external official template without containing its structure
- **THEN** adoption validation rejects the candidate and reports that the real template tree is required
- **AND** no template record is created or updated from the shim

#### Scenario: Venue structure is present
- **WHEN** a template claims a specific venue (for example IEEE Transactions)
- **THEN** validation checks the stored tree actually contains that venue's document class and title, author, abstract, and keywords constructs
- **AND** missing venue constructs are reported before the template can be selected for composition

## MODIFIED Requirements

### Requirement: TeX Is Initialized as a Derived Publication Artifact
The system SHALL create `kaoju:paper-template-tex` and `kaoju:paper-draft-tex` as derived artifacts from selected canonical MyST revisions, following the agent-mediated composition contract: MyST holds all TeX content, TeX drift is presentation-only, and the agent fills the real venue template rather than relying on mechanical conversion.

#### Scenario: TeX initialization succeeds with a fill contract
- **WHEN** the selected MyST template and draft use supported structures and an adopted venue template exists
- **THEN** the paper service materializes the real template tree, scaffolds the draft TeX tree with lineage to its MyST sources, and writes a fill manifest of composition obligations
- **AND** it records the template compatibility fingerprint, tool identity, source checksums, citation inputs, included files, and diagnostics
- **AND** obligations cover frontmatter-to-title mapping, abstract and keywords environments, section mapping, bibliography materialization, tables, floats, and venue constructs

#### Scenario: Existing TeX template remains compatible
- **WHEN** a later MyST revision preserves the selected venue or document class, toolchain policy, and required construct set
- **THEN** the system reuses the current `kaoju:paper-template-tex` and regenerates only `kaoju:paper-draft-tex`
- **AND** prior human TeX-template refinements remain intact

#### Scenario: TeX template compatibility changes
- **WHEN** the venue or document class, toolchain policy, or required MyST construct set changes incompatibly
- **THEN** the system creates a revision of `kaoju:paper-template-tex` before regenerating the TeX draft
- **AND** it records the changed fingerprint dimensions and migration diagnostics

#### Scenario: Conversion requires agent repair
- **WHEN** MyST directives, tables, citations, floats, raw blocks, or venue rules cannot be converted faithfully
- **THEN** the initializer marks the affected TeX locations and returns a non-terminal repair requirement
- **AND** the write agent directly inspects and edits the TeX files before build readiness

#### Scenario: Mechanical pass-through is reported, not hidden
- **WHEN** scaffolded TeX contains raw frontmatter, placeholder title or author, literal Title or Abstract sections, citation keys without a bibliography, or unrepaired markers
- **THEN** the initializer or validator reports each as an unfilled obligation with file location
- **AND** the tree cannot be recorded as inspected or build-ready while any obligation is open

#### Scenario: Script output is not accepted without inspection
- **WHEN** TeX was initialized mechanically
- **THEN** the system requires a recorded agent fill and inspection result before it can be selected for PDF build
- **AND** successful file creation alone does not establish publication readiness
