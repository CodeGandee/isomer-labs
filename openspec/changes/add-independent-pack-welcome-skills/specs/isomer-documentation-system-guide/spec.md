## MODIFIED Requirements

### Requirement: Documentation Information Architecture
The documentation SHALL include welcome-first onboarding paths for core Isomer, DeepSci, and Kaoju alongside informed-user entrypoint and CLI references.

#### Scenario: Documentation tree is inspected
- **WHEN** public documentation navigation is inspected
- **THEN** installation and quickstart pages link to packaged system-skill onboarding, core welcome, extension welcomes, entrypoint execution, and CLI reference
- **AND** newcomer guidance is not buried only inside the complete command reference

#### Scenario: Packaged skill guide is inspected
- **WHEN** docs explain the packaged public surface
- **THEN** they present each pack as a welcome and entrypoint pair
- **AND** they distinguish protected subskills from both public roles

### Requirement: Intended Usage Workflows
The documentation SHALL show newcomer workflows that begin with welcome and informed-user workflows that begin directly with an execution entrypoint.

#### Scenario: First-time core user is guided
- **WHEN** a reader does not yet know Isomer task vocabulary or command ids
- **THEN** docs recommend `$isomer-op-welcome` to explore typical Project, Topic, topology, extension, GUI, and Toolbox patterns
- **AND** they show how welcome hands a selected task to `$isomer-op-entrypoint`

#### Scenario: First-time extension user is guided
- **WHEN** a reader wants to understand DeepSci or Kaoju before starting work
- **THEN** docs recommend the corresponding `$isomer-ext-<extension-id>-welcome`
- **AND** they show a representative exact execution request through `$isomer-ext-<extension-id>-entrypoint`

#### Scenario: Informed user has a concrete task
- **WHEN** a reader already knows the intended public command or can state a concrete task
- **THEN** docs allow direct entrypoint invocation without requiring a welcome step
- **AND** they explain that the entrypoint proceeds through protected owners and prerequisite recovery as applicable

#### Scenario: Routing cues are documented
- **WHEN** docs include representative user phrases or keywords
- **THEN** they label them as routing cues and pair them with deterministic public command forms
- **AND** they do not claim that natural-language routing depends on an undocumented exact keyword grammar

### Requirement: Documentation Verification
Documentation validation SHALL verify public welcome names, entrypoint names, role descriptions, and example command ids against the packaged manifest.

#### Scenario: Public pair drifts
- **WHEN** documentation omits a declared welcome, swaps welcome and entrypoint roles, or names a stale public skill
- **THEN** documentation validation reports the affected page and expected manifest identity

#### Scenario: Example command drifts
- **WHEN** a welcome or documentation example names a public entrypoint command absent from manifest v4
- **THEN** validation reports the stale command and owning entrypoint

#### Scenario: Protected direct invocation appears
- **WHEN** newcomer documentation tells users to invoke a protected logical id directly
- **THEN** validation reports the route and recommends the owning public entrypoint form
