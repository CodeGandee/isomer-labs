## ADDED Requirements

### Requirement: Placeholder Bindings Use Global Isomer CLI
Active non-dev placeholder binding pages SHALL present record CRUD commands using the globally installed `isomer-cli` executable.

#### Scenario: Binding commands omit pixi prefix
- **WHEN** a non-dev `placeholder-bindings.md` row gives an `isomer-cli ext research records` create, list, show, update, or delete command
- **THEN** the command starts with `isomer-cli`
- **AND** it does not start with `pixi run isomer-cli`

#### Scenario: Binding metadata is preserved
- **WHEN** implementation removes the Pixi prefix from placeholder binding command rows
- **THEN** it preserves placeholders, record kinds, semantic labels, profiles, skill names, producer and consumer fields, metadata JSON, body flags, and content names
