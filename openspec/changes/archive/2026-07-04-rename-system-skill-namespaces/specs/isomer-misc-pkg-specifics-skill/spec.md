## ADDED Requirements

### Requirement: Package Specifics Remain Misc Helper Interface
The package-specifics skill SHALL remain in the `isomer-misc-*` namespace as a public cross-domain helper interface consumed by service, operator, and domain extension skills.

#### Scenario: Package-specifics skill name remains stable
- **WHEN** the misc skillset is inspected after the namespace rename
- **THEN** the package-specifics skill remains `isomer-misc-pkg-specifics`
- **AND** it is not renamed to `isomer-ext-pkg-specifics`

#### Scenario: Package-specifics consumers use stable helper name
- **WHEN** service, operator, or domain extension guidance references package-specific caveats
- **THEN** it references `isomer-misc-pkg-specifics`
- **AND** it does not duplicate the full caveat text into the consuming skill

#### Scenario: Package-specifics is not a domain extension
- **WHEN** documentation explains extension family naming
- **THEN** it treats `isomer-misc-pkg-specifics` as shared helper infrastructure
- **AND** it reserves `isomer-<extension-name>-<purpose>` for concrete domain extension families such as `isomer-deepsci-*`
