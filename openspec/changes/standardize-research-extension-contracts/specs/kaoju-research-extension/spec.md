## MODIFIED Requirements

### Requirement: Production Kaoju Skill Family
The package SHALL provide a self-contained production Kaoju research-paradigm skill family under `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/` using the `isomer-kaoju-<purpose>` namespace and the skill/shared-resource contract.

#### Scenario: Exact production inventory exists
- **WHEN** the packaged Kaoju root is inspected
- **THEN** it contains `isomer-kaoju-pipeline`, `isomer-kaoju-shared`, `isomer-kaoju-workspace-mgr`, `isomer-kaoju-frame`, `isomer-kaoju-discover`, `isomer-kaoju-acquire`, `isomer-kaoju-examine`, `isomer-kaoju-reproduce`, `isomer-kaoju-trial`, `isomer-kaoju-compare`, `isomer-kaoju-audit`, `isomer-kaoju-synthesize`, `isomer-kaoju-write`, and `isomer-kaoju-export`
- **AND** no retired, version-suffixed, generic `isomer-ext-*`, or duplicate survey-facade Kaoju skill is active

#### Scenario: Skill identity and resource boundary are consistent
- **WHEN** a production Kaoju skill is inspected
- **THEN** its folder name, `SKILL.md` frontmatter name, `agents/openai.yaml` display name, and default-prompt invocation use the same `isomer-kaoju-*` name
- **AND** every active filesystem-linked resource resolves within that skill directory, shared machine data is queried through `isomer-cli ext kaoju`, and shared procedures are routed through `isomer-kaoju-shared`

#### Scenario: Artifact identity is consistent
- **WHEN** a production Kaoju skill names, resolves, produces, consumes, or queries a durable extension artifact
- **THEN** it uses the exact registered `KAOJU:WHAT` identifier in prose, local projections, source declarations, and commands
- **AND** it does not use an angle-wrapped token, a bare object name, lowercase or mixed case, or an artifact alias

#### Scenario: Trial and reproduction remain distinct
- **WHEN** the production inventory is inspected for executable evidence work
- **THEN** `isomer-kaoju-trial` owns bounded method trials and generated-data capability probes while `isomer-kaoju-reproduce` owns only work that satisfies the stronger reproduction contract
- **AND** neither skill treats a repaired or capability-probe result as faithful paper reproduction

## ADDED Requirements

### Requirement: Kaoju Survey Process Data Is Extension-Queried
Kaoju active guidance SHALL obtain the checked survey-process inventory through the package-owned Kaoju extension query instead of a family-root contract file.

#### Scenario: Pipeline loads its checked contract
- **WHEN** `isomer-kaoju-pipeline` starts a Kaoju routing task
- **THEN** it runs `isomer-cli --print-json ext kaoju process show` and treats the returned version, entry skill, skill inventory, survey intents, compatibility procedures, manager actions, aliases, and policy decisions as the checked machine contract
- **AND** it does not open `../contracts`, an absolute checkout path, or another skill's resources

#### Scenario: Pipeline loads a command process
- **WHEN** the selected survey intent, compatibility procedure, or grouped manager action has a procedure used only by the pipeline
- **THEN** the pipeline loads the corresponding command page from its own `commands/` directory
- **AND** the machine contract identifies the command without becoming a duplicate prose procedure

### Requirement: Kaoju Cross-Skill Procedures Are Shared-Skill Owned
Kaoju guidance used across multiple stages SHALL remain in `isomer-kaoju-shared` and SHALL be consumed through skill routing rather than sibling filesystem references.

#### Scenario: Stage needs common Kaoju discipline
- **WHEN** a stage needs common evidence semantics, source identity, lineage, latest-context, Gate, owner-routing, Artifact recording, or terminal-state procedure
- **THEN** it invokes or follows `isomer-kaoju-shared` and loads only its own bundle-local stage guidance
- **AND** it does not copy the complete shared command process or traverse into the shared skill directory
