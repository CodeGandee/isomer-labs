## ADDED Requirements

### Requirement: Kaoju Welcome Maps the Complete Public Command Inventory
The Kaoju welcome skill SHALL maintain a manifest-validated command map and curated use-case guide for the current Kaoju public entrypoint.

#### Scenario: Command map is validated
- **WHEN** Kaoju welcome validation runs
- **THEN** every current public survey-intent, compatibility-procedure, manager, and help command appears exactly once
- **AND** missing, duplicate, extra, or stale command ids fail validation

#### Scenario: Typical use cases are curated
- **WHEN** default Kaoju welcome output is inspected
- **THEN** it prioritizes landscape discovery, reading-list work, evidence intake, comparison, trials, paper production, and wiki export
- **AND** it does not dump the complete command inventory before offering those representative patterns
