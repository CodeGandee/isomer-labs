## ADDED Requirements

### Requirement: Host identifiers are masked in published files
The system SHALL replace occurrences of the original username, hostname, and host-specific absolute paths with generic placeholders in all published text files.

#### Scenario: Username replacement
- **WHEN** the sanitization script processes a file containing the original username
- **THEN** the published file contains a generic placeholder such as `<USER>` or `researcher`

#### Scenario: Hostname replacement
- **WHEN** the sanitization script processes a file containing the original GPU hostname
- **THEN** the published file contains a generic placeholder such as `<GPU_HOST>`

#### Scenario: Absolute path replacement
- **WHEN** the sanitization script processes a file containing the original project root path
- **THEN** the published file contains a placeholder such as `<PROJECT_ROOT>` or a relative path

### Requirement: Private conversation history is excluded
The published repository SHALL omit raw encrypted chatlog files and any other conversational artifacts that are not required for reproduction.

#### Scenario: Chatlog exclusion
- **WHEN** the publication script runs
- **THEN** `chatlogs/raw/` and its contents are not present in the published repository
- **AND** a sanitized `chatlogs/README.md` may be present

### Requirement: Sanitization is applied before the initial public commit
The system SHALL apply sanitization to a fresh export of the workspace before creating the first commit in the public repository.

#### Scenario: Clean initial history
- **WHEN** a user inspects the public repository history
- **THEN** no commit contains the original username, hostname, or host-specific absolute path
