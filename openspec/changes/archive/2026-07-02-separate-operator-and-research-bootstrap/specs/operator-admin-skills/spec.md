## ADDED Requirements

### Requirement: Operator Skills Exclude Research-Paradigm Bootstrap
Operator admin skills SHALL prepare Project, Topic Workspace, Topic Actor, topology, readiness-summary, approval, materialization, and launch orchestration surfaces without owning research-paradigm-specific bootstrap.

#### Scenario: Operator topic creation does not invoke v2 bootstrap
- **WHEN** active operator skill guidance for topic creation or manual research preparation is inspected
- **THEN** it does not instruct the operator to invoke `isomer-rsch-workspace-mgr-v2`
- **AND** it does not require selected v2 skill sets, v2 `placeholder-bindings.md` files, v2 placeholder binding registries, or accepted research artifact command shapes before reporting Topic Workspace or Topic Actor readiness

#### Scenario: Operator docs route v2 bootstrap to research skills
- **WHEN** operator docs mention research-paradigm-specific bootstrap, placeholder bindings, selected v2 research skills, or accepted research artifact recording
- **THEN** they identify that work as belonging to `skillset/research-paradigm/v2/isomer-rsch-workspace-mgr-v2` or later research-stage skills rather than operator skills

### Requirement: Retired Operator Compatibility Skills Are Removed
The operator admin skillset SHALL retire the deprecated `isomer-admin-topic-prepare` and `isomer-admin-manual-research-session` compatibility skills from active operator inventory.

#### Scenario: Retired compatibility folders are absent
- **WHEN** the active operator skillset is inspected
- **THEN** `skillset/operator/isomer-admin-topic-prepare/` is absent
- **AND** `skillset/operator/isomer-admin-manual-research-session/` is absent

#### Scenario: Active operator references avoid retired skills
- **WHEN** active operator skill docs, manifests, README files, and routing references are inspected
- **THEN** they do not route normal or delegated work to `isomer-admin-topic-prepare` or `isomer-admin-manual-research-session`
- **AND** any historical mention is clearly marked as archived provenance rather than active guidance

#### Scenario: Topic preparation uses current Topic Creator subcommands
- **WHEN** operator docs route topic creation, topic preparation, manual-research-ready setup, or human-orchestrated Topic Actor preparation
- **THEN** they use actual `isomer-admin-topic-creator` subcommands such as `fast-forward`, `step-by-step`, `run-to`, `status`, or `repair`
- **AND** they do not reference nonexistent `create`, `plan`, or `start-manual-research` Topic Creator subcommands
