## MODIFIED Requirements

### Requirement: Production Kaoju Skill Family
The package SHALL provide a self-contained production Kaoju research-paradigm skill family under `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/` using the `isomer-kaoju-<purpose>` namespace.

#### Scenario: Exact production inventory exists
- **WHEN** the packaged Kaoju root is inspected
- **THEN** it contains `isomer-kaoju-pipeline`, `isomer-kaoju-shared`, `isomer-kaoju-workspace-mgr`, `isomer-kaoju-frame`, `isomer-kaoju-discover`, `isomer-kaoju-acquire`, `isomer-kaoju-examine`, `isomer-kaoju-reproduce`, `isomer-kaoju-compare`, `isomer-kaoju-audit`, `isomer-kaoju-synthesize`, and `isomer-kaoju-write`
- **AND** no retired, version-suffixed, or generic `isomer-ext-*` Kaoju skill is active

#### Scenario: Skill identity is consistent
- **WHEN** a production Kaoju skill is inspected
- **THEN** its folder name, `SKILL.md` frontmatter name, `agents/openai.yaml` display name, and default-prompt invocation use the same `isomer-kaoju-*` name
- **AND** its active instructions and directly linked resources are self-contained within the skill directory

### Requirement: Kaoju Pipeline Command Surface
`isomer-kaoju-pipeline` SHALL use the complex-procedure shape with separate helper, procedural, and miscellaneous command groups.

#### Scenario: Procedural commands match survey use cases
- **WHEN** the pipeline command inventory is inspected
- **THEN** it exposes `landscape-pass`, `curated-intake-pass`, `direction-expansion-pass`, `theory-comparison-pass`, `method-trial-pass`, `comparative-pass`, `audit-survey-pass`, `paper-pass`, and `create-paper-template`
- **AND** each procedure links to one local command page containing its bounded stage recipe and terminal outputs

#### Scenario: CRUD actions are grouped by object
- **WHEN** helper commands are inspected
- **THEN** `manage-survey` groups `list`, `show`, `status`, and `export`
- **AND** `manage-dataset` groups `register`, `list`, `show`, `refresh`, and `remove`
- **AND** the pipeline does not expose one public subcommand for each CRUD verb

#### Scenario: Interaction and resume stay out of the procedure list
- **WHEN** a user requests clarification before work or resumes accepted prior state
- **THEN** clarification-first is represented as an interaction mode shared by procedures
- **AND** resume is represented by accepted input refs and a starting stage rather than a separate procedure

#### Scenario: Generic maintenance procedures are absent
- **WHEN** the pipeline public procedure list is inspected
- **THEN** it does not include standalone source-audit, reproduction, repository-refresh, environment-repair, full-Kaoju, or list-passes procedures
