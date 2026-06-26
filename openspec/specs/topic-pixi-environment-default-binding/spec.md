# topic-pixi-environment-default-binding Specification

## Purpose
Define how Isomer resolves explicit and implicit Topic Workspace Pixi bindings while delegating workspace detection to Pixi.

## Requirements
### Requirement: Topic Workspace Pixi Binding Target Resolution
The system SHALL resolve a Topic Workspace Pixi binding from either an active explicit `topic_standalone_pixi_bindings` target or, when no active explicit binding exists, the registered Topic Workspace directory as an implicit default target.

#### Scenario: Explicit binding target may be a manifest file
- **WHEN** a registered Research Topic has a registered Topic Workspace
- **AND** the Project Manifest contains an active `topic_standalone_pixi_bindings` entry for that Research Topic whose `manifest_path_or_dir` value points to a Pixi manifest file inside the Topic Workspace
- **THEN** the effective standalone Pixi binding uses that file path as its explicit binding target

#### Scenario: Explicit binding target may be a directory
- **WHEN** a registered Research Topic has a registered Topic Workspace
- **AND** the Project Manifest contains an active `topic_standalone_pixi_bindings` entry for that Research Topic whose `manifest_path_or_dir` value points to a directory inside the Topic Workspace
- **THEN** the effective standalone Pixi binding uses that directory path as its explicit binding target and lets Pixi resolve the actual manifest from that target

#### Scenario: Superseded explicit binding target fields are rejected
- **WHEN** the Project Manifest contains an active `topic_standalone_pixi_bindings` entry for a Research Topic
- **AND** the entry uses a superseded explicit target field such as `manifest_path` or `path` instead of `manifest_path_or_dir`
- **THEN** Project Manifest validation reports the superseded field as invalid
- **AND** the entry is not used as an effective standalone Pixi binding target

#### Scenario: Missing explicit binding defaults to Topic Workspace directory
- **WHEN** a registered Research Topic has a registered Topic Workspace
- **AND** the Project Manifest contains no active `topic_standalone_pixi_bindings` entry for that Research Topic
- **THEN** the effective standalone Pixi binding target is the registered Topic Workspace directory with Pixi environment `default` and source `implicit-default`

#### Scenario: Pixi resolves binding target
- **WHEN** the Project Manifest contains an active `topic_standalone_pixi_bindings` entry for a Research Topic
- **OR** the implicit default Topic Workspace directory target is selected
- **THEN** the system resolves the target by invoking Pixi with an explicit manifest selector equivalent to `pixi info --json --manifest-path <binding-target>`

#### Scenario: Pixi is required for binding target resolution
- **WHEN** the system attempts to resolve a Topic Workspace Pixi binding target
- **AND** Pixi is unavailable, cannot execute, returns invalid JSON, or omits required binding-resolution fields
- **THEN** the system reports a Pixi tooling diagnostic with online and offline install guidance instead of treating the Research Topic as unbound

#### Scenario: Resolved binding is confined to Topic Workspace
- **WHEN** Pixi resolves a Topic Workspace Pixi binding target
- **THEN** the resolved Pixi manifest path MUST be inside the registered Topic Workspace
- **AND** the selected environment prefix MUST be inside the registered Topic Workspace `.pixi/` directory

#### Scenario: No effective binding when Pixi cannot resolve target
- **WHEN** the effective binding target is selected
- **AND** Pixi does not report a workspace manifest for that target
- **THEN** no effective standalone Pixi binding exists for that Research Topic

#### Scenario: Explicit binding overrides implicit default
- **WHEN** the Project Manifest contains an active `topic_standalone_pixi_bindings` entry for a Research Topic
- **THEN** that explicit binding target is used and the Topic Workspace directory default is not applied

#### Scenario: Binding target remains project-root-relative
- **WHEN** an effective binding target is reported
- **THEN** its original target path is reported relative to the Project root when possible
- **AND** Pixi's resolved manifest path is reported relative to the Project root when possible

#### Scenario: Resolved binding object is reported
- **WHEN** a consumer reports an effective standalone Pixi binding
- **THEN** it includes the binding source, target path, target kind, resolved manifest path, Pixi environment, and environment prefix

#### Scenario: Default binding source is reported
- **WHEN** a consumer reports the source of an effective standalone Pixi binding
- **THEN** a default-derived binding is distinguishable from an explicit Project Manifest binding
