## ADDED Requirements

### Requirement: V2 Skills Author Structured Accepted Outputs
Active v2 research-paradigm skills SHALL treat accepted durable research outputs as structured payloads when their placeholder binding names a structured Artifact Format Profile or schema/template inputs.

#### Scenario: Skill routes accepted output through binding
- **WHEN** a v2 skill produces an accepted durable output for a registered placeholder with a structured binding
- **THEN** the skill directs the agent to follow the skill-local `placeholder-bindings.md` payload-first record guidance rather than authoring a Markdown body directly as the durable source of truth

#### Scenario: Skill authors payload before generated Markdown
- **WHEN** a v2 skill needs to create a structured accepted artifact
- **THEN** the expected agent workflow is to draft the JSON payload, validate it with `isomer-cli ext research records validate`, record it with `isomer-cli ext research records create` or `update`, and request Markdown materialization with explicit `--render markdown` when a generated Markdown view is needed

#### Scenario: Methodology prose remains storage-light
- **WHEN** active v2 `SKILL.md` prose describes the research method
- **THEN** it may reference structured record production through local placeholder bindings
- **AND** it does not embed profile-specific JSON schemas, Jinja2 templates, database schema details, or Workspace Runtime table details in the methodology workflow

### Requirement: V2 Structured Payload Guidance Is Self-contained
Active v2 research-paradigm skill bundles SHALL provide enough local guidance for an agent to produce structured payloads for their accepted outputs without reading discarded topic artifacts or external migration notes.

#### Scenario: Binding page names payload expectations
- **WHEN** a v2 skill owns placeholders that produce structured records
- **THEN** its active binding or directly linked active reference names the expected format profile or schema/template inputs and the minimal payload authoring surface for each structured output

#### Scenario: Active accepted-output set is covered
- **WHEN** active v2 placeholder bindings are updated for structured records
- **THEN** every active v2 accepted-output placeholder family that remains in scope has an explicit `isomer:deepsci/record-format/*` profile or an intentional non-structured exclusion recorded in the binding guidance

#### Scenario: Agent can repair validation errors
- **WHEN** `isomer-cli ext research records validate` returns schema diagnostics for a v2 skill payload
- **THEN** the skill's active guidance allows the agent to revise the JSON payload and rerun validation before recording the artifact

#### Scenario: Generated Markdown is not edited as source
- **WHEN** a v2 skill creates Markdown through the structured record pipeline
- **THEN** active guidance treats the Markdown as generated review material
- **AND** corrections to accepted structured content are made by updating the JSON payload and re-rendering through the CLI

### Requirement: Research Skill Validation Allows Accepted Structured Bindings
The research-paradigm validation harness SHALL allow accepted payload-first storage guidance in active v2 placeholder binding material while continuing to reject unbounded runtime coupling in methodology prose.

#### Scenario: Payload-first binding is allowed
- **WHEN** validation scans active v2 placeholder binding pages
- **THEN** it allows direct `isomer-cli ext research records validate`, `create`, `update`, `show`, `list`, and `render` command shapes for structured payload records using `--format-profile` or explicit schema/template inputs

#### Scenario: Database details remain disallowed in skill prose
- **WHEN** validation scans active v2 `SKILL.md` methodology prose and active references
- **THEN** it reports direct Workspace Runtime table names, raw SQL, or implementation-only state fields unless they are confined to accepted binding pages, provenance notes, or explicit implementation references

#### Scenario: Direct Markdown source guidance is reported
- **WHEN** validation scans active v2 structured-output guidance and finds direct Markdown body authoring presented as the normal accepted-artifact source of truth
- **THEN** it reports the guidance
