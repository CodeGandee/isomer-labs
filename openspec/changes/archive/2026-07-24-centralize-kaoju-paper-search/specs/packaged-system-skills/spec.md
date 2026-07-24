## MODIFIED Requirements

### Requirement: Packaged Kaoju Extension Group
The packaged system-skill manifest SHALL expose the complete Kaoju public pair and protected member inventory, including the Kaoju-specific topic-creation owner, centralized paper-search owner, and their private resources.

#### Scenario: Kaoju manifest group is classified and complete
- **WHEN** packaged skill metadata is loaded
- **THEN** the Kaoju extension declares public welcome and entrypoint bundles plus exactly sixteen protected members, including `isomer-kaoju-topic-creator` and `isomer-kaoju-paper-search`
- **AND** the public command metadata includes `create-topic` as topic preparation without exposing either protected owner as another public skill

#### Scenario: Kaoju topic creator is materialized
- **WHEN** the Kaoju pack or the topic-creator dependency closure is materialized
- **THEN** `isomer-kaoju-topic-creator` includes its local skill guidance and validated `assets/defaults/mindsets/*.json` resources
- **AND** the materialized bundle does not depend on a repository checkout, family-root symlink, or undeclared resource path

#### Scenario: Kaoju paper search is materialized
- **WHEN** the Kaoju pack or paper-search dependency closure is materialized
- **THEN** `isomer-kaoju-paper-search` includes its local action guidance, normalized-result contract, and provider-approach references including S2
- **AND** the materialized bundle does not depend on `imsight-paper-search`, an external source checkout, or undeclared provider documentation

#### Scenario: Obsolete mindset manager is absent
- **WHEN** the packaged Kaoju inventory and public CLI documentation are inspected
- **THEN** they contain no protected `isomer-kaoju-mindsets` manager, eight-leaf mindset command tree, or specialized `ext kaoju mindsets` group
- **AND** Mindset Source editing is documented as owner-editable derived intent

#### Scenario: Kaoju paths resolve inside their owners
- **WHEN** Kaoju catalog metadata loads
- **THEN** the welcome path resolves as an independent sibling bundle
- **AND** every protected path resolves below `research-paradigm/kaoju/isomer-ext-kaoju-entrypoint/subskills/`

#### Scenario: Kaoju materializes safely
- **WHEN** extension `kaoju` is selected
- **THEN** output includes core plus both Kaoju public skills and the complete protected entrypoint inventory
- **AND** it does not include DeepSci unless selected

#### Scenario: Kaoju discovery distinguishes learning and execution
- **WHEN** extension discovery metadata is queried for `kaoju`
- **THEN** it reports `isomer-ext-kaoju-welcome` as the onboarding surface and `isomer-ext-kaoju-entrypoint` as the execution surface
- **AND** it reports entrypoint commands and protected logical members from manifest metadata

#### Scenario: Kaoju paths resolve inside the pack
- **WHEN** Kaoju catalog metadata loads
- **THEN** every protected path resolves below `research-paradigm/kaoju/isomer-ext-kaoju-entrypoint/subskills/`
- **AND** every member contains its required skill metadata and active resources

#### Scenario: Kaoju callback insertion points are cataloged
- **WHEN** callback insertion-point metadata is queried for extension `kaoju`
- **THEN** every manifest-listed Kaoju skill exposes its approved callback stages in deterministic manifest order
- **AND** the target skill name and manifest-relative path match the packaged skill identity

#### Scenario: Kaoju entry surface declares survey intents
- **WHEN** extension discovery metadata is queried for `kaoju`
- **THEN** it reports `isomer-ext-kaoju-entrypoint`, the accepted ordered public command inventory, and protected logical members from manifest metadata

#### Scenario: Kaoju role-aware baseline is packaged
- **WHEN** the Kaoju public pack and protected `write` member are materialized
- **THEN** public template-manager commands retain explicit content-versus-LaTeX role handling and the protected writer retains its private role-aware paper-production resources
- **AND** package-owned `isomer_labs.kaoju` services remain the machine authority for template state, composition, migration, validation, bindings, semantics, and process data

#### Scenario: Kaoju package is self-contained
- **WHEN** an installed package materializes the Kaoju extension
- **THEN** every skill can resolve its active direct resources, semantic and binding references, command pages, templates, and helper scripts without a repository checkout
- **AND** no active skill requires feature-design files, archived OpenSpec changes, external source checkouts, provider credentials, or the external `imsight-llm-wiki` skill merely to load or validate
