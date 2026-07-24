## MODIFIED Requirements

### Requirement: Production Kaoju Skill Family
The package SHALL provide a self-contained production Kaoju pack with independent public welcome and execution entrypoint bundles plus the protected `isomer-kaoju-<purpose>` capabilities required by its checked command and process contracts.

#### Scenario: Kaoju public pair exists
- **WHEN** packaged Kaoju assets are inspected
- **THEN** sibling bundles `isomer-ext-kaoju-welcome` and `isomer-ext-kaoju-entrypoint` contain valid public skill metadata
- **AND** the sixteen current Kaoju capabilities remain protected below the entrypoint

#### Scenario: Exact production inventory exists
- **WHEN** the packaged Kaoju root is inspected
- **THEN** it contains public directory `isomer-ext-kaoju-entrypoint`
- **AND** that pack contains protected bundles for `isomer-kaoju-shared`, `isomer-kaoju-workspace-mgr`, `isomer-kaoju-topic-creator`, `isomer-kaoju-frame`, `isomer-kaoju-paper-search`, `isomer-kaoju-discover`, `isomer-kaoju-acquire`, `isomer-kaoju-examine`, `isomer-kaoju-reproduce`, `isomer-kaoju-trial`, `isomer-kaoju-compare`, `isomer-kaoju-audit`, `isomer-kaoju-synthesize`, `isomer-kaoju-write`, `isomer-kaoju-export`, and `isomer-kaoju-explore`
- **AND** no `isomer-kaoju-mindsets` manager, `isomer-kaoju-pipeline` folder, or duplicate public facade is active

#### Scenario: Topic creator is privately projected
- **WHEN** `isomer-kaoju-topic-creator` is selected for bounded private projection
- **THEN** its local generation guidance and default mindset JSON resources remain available inside the projected bundle
- **AND** it can delegate generic creation through the public operator entrypoint without copying the generic Topic Creator into its bundle

#### Scenario: Artifact identity is consistent
- **WHEN** a protected Kaoju member names durable mindset output
- **THEN** it uses exact registered id `KAOJU:MINDSET-RECORD`
- **AND** it does not assign an Artifact id to a Mindset Source file

#### Scenario: Kaoju welcome is self-contained
- **WHEN** `isomer-ext-kaoju-welcome` is copied or linked as part of the pack
- **THEN** it resolves its active typical-use-case and command-map resources without loading private files from the entrypoint or protected subskills
- **AND** it may reference public entrypoint invocation names without becoming an execution owner

#### Scenario: Shared machine contracts remain package-owned
- **WHEN** welcome or entrypoint needs current Kaoju command or process metadata
- **THEN** checked machine contracts remain owned by the installed Kaoju Python package and manifest
- **AND** welcome does not introduce a second survey-process registry

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

### Requirement: Seed Direction Expansion
The `direction-expansion-pass` procedure SHALL expand a survey direction from named seed works through backward, neighboring, forward, and post-seed discovery routes.

#### Scenario: Expansion records route and time provenance
- **WHEN** a user asks for more work related to selected seed works
- **THEN** each candidate records its parent seed or query, discovery route, relevance rationale, inclusion decision, `latest_after`, and `searched_through`
- **AND** citation count, publication date, or provider rank alone does not determine inclusion

#### Scenario: Expansion centralizes paper traversal
- **WHEN** backward, forward, neighboring, or post-seed expansion requires paper lookup, citation traversal, or adjacent-paper retrieval
- **THEN** `discover` defines the bounded expansion strategy and invokes `isomer-ext-kaoju-entrypoint->paper-search` for paper-specific retrieval
- **AND** `discover` retains candidate disposition, cross-source-class coverage, and durable delta ownership

#### Scenario: Expansion produces a bounded delta
- **WHEN** important additions have been selected and audited
- **THEN** Kaoju produces a Related-Work Catalog Delta and updates affected survey views
- **AND** it states the remaining frontier and does not claim exhaustive coverage

### Requirement: Kaoju Entrypoint Explains Every Protected Route
The `isomer-ext-kaoju-entrypoint` skill SHALL provide one context-aware `When to Route Here` sentence for every protected Kaoju subskill in its protected-subskill table.

#### Scenario: Kaoju protected inventory is inspected
- **WHEN** `isomer-ext-kaoju-entrypoint/SKILL.md` is inspected
- **THEN** all 16 protected-member rows contain one routing sentence
- **AND** `paper-search` uses logical id `isomer-kaoju-paper-search` and designator `isomer-ext-kaoju-entrypoint->paper-search`, while existing member names and designators remain unchanged

#### Scenario: Topic creation and framing overlap
- **WHEN** a task has a Research Topic but lacks derived Kaoju Mindset Sources, Direction Set, or Survey Contract
- **THEN** `topic-creator` owns missing derived intent while `frame` owns survey directions, boundary, evidence depth, and Survey Contract after topic preparation
- **AND** neither owner writes the other's state

#### Scenario: Explore and topic creation overlap
- **WHEN** a user needs read-only planning for an unprepared Kaoju topic
- **THEN** `explore` may diagnose and recommend `create-topic`, while `topic-creator` owns authorized generic delegation and Mindset Source writes
- **AND** `explore` does not mutate the derived-intent root

#### Scenario: Shared support is selected
- **WHEN** a Kaoju task needs cross-stage evidence, Gate, Artifact, lineage, or terminal-state rules rather than topic creation or a standalone survey stage
- **THEN** the `shared` sentence identifies it as internal cross-stage support and does not present it as an independent public workflow

#### Scenario: Discovery and paper-search routes overlap
- **WHEN** a task needs paper retrieval as part of broader survey discovery
- **THEN** the routing sentences distinguish `paper-search` as the owner of bounded paper lookup and citation retrieval from `discover` as the owner of strategy, cross-source coverage, selection, and durable discovery outputs

#### Scenario: Source-evidence routes overlap
- **WHEN** a task may require paper search, broader source discovery, acquisition, examination, comparison, or audit
- **THEN** the applicable routing sentences distinguish `paper-search`, `discover`, `acquire`, `examine`, `compare`, and `audit` by evidence state and intended output

#### Scenario: Execution routes overlap
- **WHEN** a source-code task may be a bounded environment or method trial or a genuine reproduction claim
- **THEN** the routing sentences distinguish `trial` from `reproduce` by the requested fidelity and claim contract

#### Scenario: Closeout routes overlap
- **WHEN** accepted evidence may need synthesis, authored survey output, or export
- **THEN** the applicable routing sentences distinguish `synthesize`, `write`, and `export` by whether the task creates conclusions, prose, or a target projection
