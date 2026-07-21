## ADDED Requirements

### Requirement: LaTeX Template Stock Has a Dedicated Binding
The Kaoju binding registry SHALL define `KAOJU:PAPER-TEMPLATE-LATEX` as a managed-directory mutable-state Artifact with template-name scope and mutable-named selection.

#### Scenario: Binding is described
- **WHEN** a caller describes `KAOJU:PAPER-TEMPLATE-LATEX`
- **THEN** the registry reports producer `isomer-kaoju-write`, directory-manifest content, required template-name scope, mutable-state revision mode, mutable-named selection, and ready or blocked validation posture
- **AND** the semantic registry describes it as named LaTeX presentation stock rather than canonical paper content

#### Scenario: Generic Artifact mutation is attempted
- **WHEN** a caller uses generic Artifact put or revise for `KAOJU:PAPER-TEMPLATE-LATEX`
- **THEN** the service rejects the mutation and directs the caller to the named-template owner
- **AND** no alternate stable record is created

### Requirement: Paper Lineage Distinguishes Both Template Roles
Paper bindings SHALL distinguish content-template, LaTeX-template, TeX-snapshot, and TeX-draft relationships.

#### Scenario: Canonical MyST draft is recorded
- **WHEN** `KAOJU:PAPER-DRAFT-MYST` is created or revised
- **THEN** its `paper_template` relationship identifies the observed content template
- **AND** it does not claim a LaTeX presentation relationship

#### Scenario: TeX snapshot is recorded
- **WHEN** `KAOJU:PAPER-TEMPLATE-TEX` is created or revised from stocked LaTeX state
- **THEN** its required relationship identifies `paper_template_latex`
- **AND** its manifest records the observed state token and digest

#### Scenario: TeX draft is recorded
- **WHEN** `KAOJU:PAPER-DRAFT-TEX` is composed
- **THEN** it relates separately to `paper_draft_myst` and `paper_template_tex`
- **AND** publication bundles preserve both upstream template roles through lineage

### Requirement: Template Exchange Evidence Records Its Kind
Mutation audits, exports, and export manifests SHALL record whether the subject is a content template or LaTeX template.

#### Scenario: Same name exists in both kinds
- **WHEN** content `main` and LaTeX `main` each produce audits or working-copy exports
- **THEN** every record contains an exact template kind and stable target ref
- **AND** query and discovery logic can distinguish them without inspecting file extensions
