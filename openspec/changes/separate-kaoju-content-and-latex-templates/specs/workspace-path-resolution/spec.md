## ADDED Requirements

### Requirement: Paper Template Exchange Separates Content and LaTeX Working Copies
Workspace Path Resolution SHALL expose kind-specific safe children beneath the topic paper-template exchange root.

#### Scenario: Default content working path resolves
- **WHEN** a content-template export omits an explicit target
- **THEN** the service resolves `<exchange-root>/content/<name>/`
- **AND** content `main` resolves `<exchange-root>/content/main/`

#### Scenario: Default LaTeX working path resolves
- **WHEN** a LaTeX-template export omits an explicit target
- **THEN** the service resolves `<exchange-root>/latex/<name>/`
- **AND** LaTeX `main` resolves `<exchange-root>/latex/main/`

#### Scenario: Legacy working path is inspected
- **WHEN** migration finds `<exchange-root>/<name>/` with recognized legacy content-template metadata
- **THEN** it reports the compatibility source and may register or copy it to the content subdirectory without overwriting edited content
- **AND** it never infers that the legacy path is LaTeX solely from its location
