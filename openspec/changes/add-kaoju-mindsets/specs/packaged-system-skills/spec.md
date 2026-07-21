## MODIFIED Requirements

### Requirement: Packaged Kaoju Extension Group
The packaged system-skill manifest SHALL expose the complete Kaoju public pair and protected member inventory, including the Kaoju-specific topic-creation owner and its private default resources.

#### Scenario: Kaoju manifest group is classified and complete
- **WHEN** packaged skill metadata is loaded
- **THEN** the Kaoju extension declares public welcome and entrypoint bundles plus exactly fifteen protected members, including `isomer-kaoju-topic-creator`
- **AND** the public command metadata includes `create-topic` as topic preparation without exposing the protected owner as another public skill

#### Scenario: Kaoju topic creator is materialized
- **WHEN** the Kaoju pack or the topic-creator dependency closure is materialized
- **THEN** `isomer-kaoju-topic-creator` includes its local skill guidance and validated `assets/defaults/mindsets/*.json` resources
- **AND** the materialized bundle does not depend on a repository checkout, family-root symlink, or undeclared resource path

#### Scenario: Obsolete mindset manager is absent
- **WHEN** the packaged Kaoju inventory and public CLI documentation are inspected
- **THEN** they contain no protected `isomer-kaoju-mindsets` manager, eight-leaf mindset command tree, or specialized `ext kaoju mindsets` group
- **AND** Mindset Source editing is documented as owner-editable derived intent

### Requirement: Packaged Kaoju Shared Data Is CLI-Owned
The packaged Kaoju skill family SHALL keep canonical survey-process, binding-registry, and binding-schema data package-owned while allowing a declared skill bundle to own local schema-valid seed resources used only by that skill workflow.

#### Scenario: Packaged Kaoju resources are inspected
- **WHEN** package assets and the Kaoju Python package are inspected
- **THEN** canonical survey-process and binding data remain with the package-owned Kaoju extension implementation and load through its shared contract loader
- **AND** `isomer-kaoju-topic-creator` owns only its local generation guidance and validated default mindset JSON, and the system-skill family root contains only the seventeen declared skill bundles and family documentation needed for discovery

#### Scenario: Kaoju package is used without repository layout
- **WHEN** an installed package materializes Kaoju skills and an agent creates or repairs a Kaoju topic
- **THEN** skill-local default resources resolve inside `isomer-kaoju-topic-creator`, shared machine data resolves through the installed package, and topic files resolve through Workspace Path Resolution
- **AND** no operation requires `.kimi-code`, a repository symlink, or `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/contracts`

#### Scenario: Kaoju is installed after topics exist
- **WHEN** the pack is registered, installed, refreshed, or materialized while existing Research Topics are available
- **THEN** package lifecycle work does not enumerate Topic Workspaces, create `intent/derived/mindsets`, or invoke the generic Topic Creator
- **AND** extension-local lazy initialization remains the responsibility of a later concrete mutation-bearing Kaoju request with one reconciled topic
