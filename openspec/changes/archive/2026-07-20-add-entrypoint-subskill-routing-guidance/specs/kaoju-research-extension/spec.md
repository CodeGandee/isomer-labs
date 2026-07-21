## ADDED Requirements

### Requirement: Kaoju Entrypoint Explains Every Protected Route
The `isomer-ext-kaoju-entrypoint` skill SHALL provide one context-aware `When to Route Here` sentence for every protected Kaoju subskill in its protected-subskill table. Each sentence SHALL assume the Kaoju survey context and identify the evidence-stage condition, publication output, or bounded support need that selects the member.

#### Scenario: Kaoju protected inventory is inspected
- **WHEN** `isomer-ext-kaoju-entrypoint/SKILL.md` is inspected
- **THEN** all 13 protected-member rows contain one routing sentence
- **AND** the existing member names, logical ids, and internal designators remain unchanged

#### Scenario: Source-evidence routes overlap
- **WHEN** a task may require source discovery, acquisition, examination, comparison, or audit
- **THEN** the applicable routing sentences distinguish `discover`, `acquire`, `examine`, `compare`, and `audit` by evidence state and intended output

#### Scenario: Execution routes overlap
- **WHEN** a source-code task may be a bounded environment or method trial or a genuine reproduction claim
- **THEN** the routing sentences distinguish `trial` from `reproduce` by the requested fidelity and claim contract

#### Scenario: Closeout routes overlap
- **WHEN** accepted evidence may need synthesis, authored survey output, or export
- **THEN** the applicable routing sentences distinguish `synthesize`, `write`, and `export` by whether the task creates conclusions, prose, or a target projection

#### Scenario: Shared support is selected
- **WHEN** a Kaoju task needs cross-stage evidence, Gate, Artifact, lineage, or terminal-state rules rather than a standalone survey stage
- **THEN** the `shared` sentence identifies it as internal cross-stage support and does not present it as an independent public workflow
