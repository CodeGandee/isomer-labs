## MODIFIED Requirements

### Requirement: Skill Creator Bundle Layout
The core public pack SHALL preserve the Topic Team Specialization module as protected logical capability `isomer-op-topic-team-specialize` and scoped member `topic-team`.

#### Scenario: Protected bundle exists
- **WHEN** the core pack is inspected
- **THEN** it contains `operator/isomer-op-entrypoint/subskills/isomer-op-topic-team-specialize/SKILL.md` and `agents/openai.yaml`

#### Scenario: Frontmatter preserves identity
- **WHEN** the protected `SKILL.md` is inspected
- **THEN** its frontmatter contains `name: isomer-op-topic-team-specialize`, a trigger-oriented description, and standard invocation notation where required

#### Scenario: UI metadata is present
- **WHEN** the protected `agents/openai.yaml` is inspected
- **THEN** it contains display name, short description, release-aligned version, and default guidance that uses `$isomer-op-entrypoint use topic-team to <task>`

#### Scenario: Local subcommands exist
- **WHEN** the protected bundle is inspected
- **THEN** it retains `help`, `init-topic`, `clarify-topic`, `ensure-topic-registration`, `adapt-team-template`, `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, `resolve-project`, `inspect-template`, `resolve-context`, `map-placeholders`, `draft-profile`, `approve-profile`, `materialize-profile`, `fast-forward`, and `step-by-step`

#### Scenario: Subcommands remain grouped by contract
- **WHEN** protected help or workflow text lists commands
- **THEN** it preserves the accepted procedural, helper, and misc command grouping
- **AND** helper commands remain absent from ordinary public help unless explicitly promoted

#### Scenario: Parent routes specialization
- **WHEN** explicit or contextual formal Agent Team intent selects Topic Team Specialization
- **THEN** the public core entrypoint invokes `isomer-op-entrypoint->topic-team`
- **AND** internal command routing uses `isomer-op-entrypoint->topic-team-><command>()`

#### Scenario: Empty protected invocation defaults to help
- **WHEN** the protected member is entered without a selected routine
- **THEN** it executes its local help behavior

#### Scenario: Step-by-step remains guided
- **WHEN** the user requests interactive specialization
- **THEN** the protected member executes `step-by-step`, explains each stage, and waits for confirmation as before

#### Scenario: Service and launch routines remain absent
- **WHEN** the protected bundle is inspected
- **THEN** it does not contain `route-service` or `launch-team` as local subcommands

#### Scenario: Required support remains local
- **WHEN** the protected bundle and active resources are inspected
- **THEN** required domain and static-runtime boundary references remain inside the bundle
- **AND** they do not depend on `.imsight-arts/`, `docs/`, `extern/`, or absolute local paths

#### Scenario: Incorporated retired helpers remain absent
- **WHEN** the protected inventory is inspected
- **THEN** it does not restore the former standalone project-aware, template-inspect, topic-context, service-route, placeholder, draft, review, materialize, or launch helper skills

### Requirement: Skill Validation
Repository validation SHALL validate Topic Team Specialization through its protected bundle and parent route.

#### Scenario: Protected module is valid
- **WHEN** operator skill validation runs
- **THEN** it validates the nested bundle, logical identity, command inventory, parent member mapping, object notation, resources, and existing Topic Team behavior

#### Scenario: Direct public invocation is introduced
- **WHEN** active user guidance advertises `$isomer-op-topic-team-specialize` as a top-level skill
- **THEN** validation reports the stale invocation and requires `$isomer-op-entrypoint use topic-team to <task>`
