## MODIFIED Requirements

### Requirement: Operator Skills Exclude Research-Paradigm Bootstrap
Operator admin skills SHALL prepare Project, Topic Workspace, Topic Actor, topology, readiness-summary, approval, materialization, and launch orchestration surfaces without owning research-paradigm-specific bootstrap.

#### Scenario: Operator topic creation does not invoke research bootstrap
- **WHEN** active operator skill guidance for topic creation or manual research preparation is inspected
- **THEN** it does not instruct the operator to invoke `isomer-rsch-workspace-mgr`
- **AND** it does not require selected DeepSci skill sets, production `placeholder-bindings.md` files, placeholder binding registries, or accepted research artifact command shapes before reporting Topic Workspace or Topic Actor readiness

#### Scenario: Operator docs route research bootstrap to research skills
- **WHEN** operator docs mention research-paradigm-specific bootstrap, placeholder bindings, selected DeepSci research skills, or accepted research artifact recording
- **THEN** they identify that work as belonging to `skillset/research-paradigm/deepsci/isomer-rsch-workspace-mgr` or later research-stage skills rather than operator skills
