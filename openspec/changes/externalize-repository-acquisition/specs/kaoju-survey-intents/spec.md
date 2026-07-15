## MODIFIED Requirements

### Requirement: Associated Source Code Is Registered and Related
The system SHALL discover and register associated source code for a selected paper when an accessible and unambiguous repository can be established through externally executed acquisition and verification.

#### Scenario: Associated repository is found
- **WHEN** a paper, report, metadata page, or verified project reference identifies associated source code
- **THEN** the acting agent resolves the repository identity, runs the applicable external repository commands, verifies the resulting immutable identity, and registers the existing path as a Canonical External Repository
- **AND** it records `KAOJU:ASSOCIATED-SOURCE-CODE` with paper ref, semantic repository label, requested and resolved repository identity, immutable commit or digest, relationship basis, acquisition method, sanitized command evidence, and access provenance

#### Scenario: Repository relationship is uncertain
- **WHEN** multiple repositories plausibly correspond to the paper or the relationship cannot be verified
- **THEN** the system records the candidates and asks for clarification or creates a blocker
- **AND** it does not execute acquisition commands or register an arbitrary repository as associated source code

#### Scenario: Acquisition does not complete
- **WHEN** the selected external acquisition or identity-verification procedure fails
- **THEN** the system records a resumable source-access blocker and any safe partial-result posture
- **AND** it does not create a successful repository binding or associated-source-code record for the failed attempt
