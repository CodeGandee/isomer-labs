# gpu-analytical-modeling-toolbox Specification

## Purpose
Define the project-local GPU analytical modeling Toolbox package and its durable schema.

## Requirements
### Requirement: GPU Analytical Modeling Toolbox Package
The GPU analytical modeling guidance SHALL live as a project-local Toolbox package under `skillset/toolboxes/gpu-analytical-modeling`.

#### Scenario: Toolbox package path is canonical
- **WHEN** an operator installs, inspects, documents, or validates the GPU analytical modeling package
- **THEN** the canonical path is `skillset/toolboxes/gpu-analytical-modeling`

#### Scenario: Toolbox manifest uses Toolbox schema
- **WHEN** the package manifest is read
- **THEN** it uses `schema_version = "isomer-toolbox.v1"` and `toolbox_id = "gpu-analytical-modeling"`

#### Scenario: README examples use Toolbox commands
- **WHEN** the package README shows installation or runtime parameter commands
- **THEN** it uses `project toolboxes`, `project toolbox-params`, and `project skill-callbacks install --toolbox-dir`

### Requirement: GPU Analytical Modeling Toolbox Remains Generic
The GPU analytical modeling Toolbox SHALL remain generic to GPU kernel analytical modeling and not require a specific topic workspace, kernel, GPU SKU, host, paper venue, or artifact path as reusable Toolbox context.

#### Scenario: No topic-specific hard-coding
- **WHEN** Toolbox instructions use examples
- **THEN** examples may name common GPU components, source classes, and evidence roles but must not require topic-specific paths, tools, targets, or paper workflows
