## MODIFIED Requirements

### Requirement: Topic Environment Binding Diagnostics
The system SHALL validate Project Manifest topic Pixi environment bindings for selected or default Research Topics without preparing environments, SHALL resolve Topic Workspace Pixi binding targets through Pixi, and SHALL accept the registered Topic Workspace directory as the implicit default target when no explicit standalone binding is present.

#### Scenario: Explicit project Pixi environment binding is valid
- **WHEN** the Project Manifest contains an active `topic_pixi_environment_bindings` entry that binds the selected Research Topic to a Pixi environment declared in the Project-level Pixi manifest
- **THEN** `project doctor` reports a passing topic environment check for that Research Topic

#### Scenario: Multiple project Pixi environment bindings are valid
- **WHEN** the Project Manifest contains multiple active `topic_pixi_environment_bindings` entries that bind the selected Research Topic to Pixi environments declared in the Project-level Pixi manifest
- **THEN** `project doctor` reports each bound environment and whether each environment exists without treating the environment names as topic semantics

#### Scenario: Missing topic environment binding is reported
- **WHEN** the selected Research Topic has no active Project Manifest `topic_pixi_environment_bindings` entry
- **AND** the selected Research Topic has no active Project Manifest `topic_standalone_pixi_bindings` entry
- **AND** Pixi cannot resolve the registered Topic Workspace directory as a Topic Workspace Pixi binding target
- **THEN** `project doctor` reports a failing topic check without inferring a Pixi environment from the Research Topic id or Pixi environment names

#### Scenario: Missing bound Pixi environment is reported
- **WHEN** the Project Manifest contains an active `topic_pixi_environment_bindings` entry whose `pixi_environment` is absent from the Project-level Pixi manifest
- **THEN** `project doctor` reports a failing topic check without editing the Pixi manifest or the Project Manifest

#### Scenario: Standalone Pixi isolation is inspected
- **WHEN** the Project Manifest contains an active `topic_standalone_pixi_bindings` entry for the selected Research Topic
- **THEN** `project doctor` verifies that the standalone Pixi binding target resolves inside the Project root, asks Pixi to resolve the target, and reports the target path, target kind, resolved manifest path, selected environment, environment prefix, and binding source without running installation

#### Scenario: Pixi tooling failure is reported
- **WHEN** topic Pixi binding diagnostics need Pixi-backed binding target resolution
- **AND** Pixi is unavailable, cannot execute, returns invalid JSON, or omits required binding-resolution fields
- **THEN** `project doctor` reports a failing Pixi tooling check with online and offline install guidance instead of reporting a missing topic binding

#### Scenario: Unresolvable standalone Pixi binding target is reported
- **WHEN** the Project Manifest contains an active `topic_standalone_pixi_bindings` entry whose target cannot be resolved by Pixi as a workspace
- **THEN** `project doctor` reports a failing topic check without creating a Pixi manifest or installing the standalone environment

#### Scenario: Escaping standalone Pixi binding target is reported
- **WHEN** Pixi resolves a standalone Pixi binding target
- **AND** the resolved manifest path or selected environment prefix is outside the registered Topic Workspace
- **THEN** `project doctor` reports a failing topic check without preparing the environment

#### Scenario: Implicit default standalone Pixi binding is accepted
- **WHEN** the Project Manifest contains no active `topic_standalone_pixi_bindings` entry for the selected Research Topic
- **AND** Pixi resolves the registered Topic Workspace directory as a confined Topic Workspace Pixi binding target
- **THEN** `project doctor` reports a passing topic check for the implicit default binding and identifies the binding source as implicit-default
