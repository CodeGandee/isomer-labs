## ADDED Requirements

### Requirement: Tool Packs Remain Misc Helper Interface
The tool-pack skill SHALL remain in the `isomer-misc-*` namespace as a public cross-domain helper interface, not a domain extension skill.

#### Scenario: Tool-pack skill name remains stable
- **WHEN** the misc skillset is inspected after the namespace rename
- **THEN** the tool-pack skill remains `isomer-misc-tool-packs`
- **AND** it is not renamed to `isomer-ext-tool-packs`

#### Scenario: Tool-pack helper routes remain current
- **WHEN** the tool-pack skill returns a pack contract
- **THEN** package-source concerns route to `isomer-srv-resolve-pkg-repo`
- **AND** NVIDIA/CUDA environment concerns route to `isomer-misc-nvidia-tools`
- **AND** PyTorch variant concerns route to `isomer-misc-pkg-specifics`
- **AND** heavy or unknown-risk setup work routes to `isomer-misc-bounded-run-tips`

#### Scenario: Tool-pack skill avoids DeepSci coupling
- **WHEN** the tool-pack skill and its active references are inspected
- **THEN** they do not require or reference production DeepSci skill paths as consumers or dependencies
- **AND** domain extension families may consume tool-pack contracts without making the tool-pack skill part of that extension family
