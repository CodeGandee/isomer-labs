## ADDED Requirements

### Requirement: Public Template Management Distinguishes Template Roles
The public Kaoju `manage-paper-template` command SHALL retain one grouped action surface while resolving content-template and LaTeX-template roles explicitly.

#### Scenario: Help is requested
- **WHEN** a user inspects `manage-paper-template` help
- **THEN** it explains content templates, LaTeX templates, their independent `main` defaults, and supported management actions
- **AND** it does not describe all paper templates as MyST-oriented trees

#### Scenario: Natural-language task is routed
- **WHEN** task language names MyST structure, content sections, LaTeX, TeX, a document class, a style, or a venue template
- **THEN** the entrypoint routes the task with the corresponding template role
- **AND** existing evidence, Gate, Run, and owner boundaries remain unchanged
