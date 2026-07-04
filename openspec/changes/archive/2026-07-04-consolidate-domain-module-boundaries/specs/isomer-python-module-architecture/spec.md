## ADDED Requirements

### Requirement: Domain Module Boundary Consolidation
The system SHALL keep tightly coupled domain helper code in cohesive package modules whose names match canonical Isomer language or a concrete processing boundary.

#### Scenario: Artifact Format processing has one pipeline module
- **WHEN** a developer inspects Artifact Format resolution, validation, payload loading, or rendering code
- **THEN** that processing behavior is located in `isomer_labs.artifact_formats.processing` while Artifact Format models, provider registry code, and workspace-backed provider code remain in their own modules

#### Scenario: DeepScientist compatibility tools have one tool adapter module
- **WHEN** a developer inspects DeepScientist compatibility tool discovery, dispatch, service execution, JSON input loading, or unsupported-tool payload construction
- **THEN** that behavior is located in `isomer_labs.deepsci_ext.tools` while compatibility persistence and Artifact Format provider code remain in their own modules

#### Scenario: Topic Team Specialization helper shards are folded into owning modules
- **WHEN** a developer inspects Domain Agent Team Template harness validation, Topic Team Instantiation Packet validation, or Topic Agent Team Profile provenance and bundle-layout validation
- **THEN** those helpers are located in `isomer_labs.teams.templates`, `isomer_labs.teams.instantiation`, or `isomer_labs.teams.profiles` according to the domain object they validate

#### Scenario: Workspace path helpers use canonical concepts
- **WHEN** a developer inspects Semantic Workspace Surface Label catalogs, Default Layout Profile helpers, Local Tmp Surface policy, Workspace Path Resolution, or Agent Workspace ref validation
- **THEN** those helpers are located in `isomer_labs.workspace.surfaces` or `isomer_labs.workspace.path_resolution` according to whether they define surfaces or resolve paths

#### Scenario: Removed helper modules stay absent
- **WHEN** source architecture tests scan `src/isomer_labs`
- **THEN** obsolete helper-shard modules such as `artifact_formats.resolver`, `artifact_formats.validation`, `artifact_formats.rendering`, `deepsci_ext.registry`, `deepsci_ext.rendering`, `deepsci_ext.service`, `teams.template_harness`, `teams.packet_validation`, `teams.profile_bundle_validation`, `workspace.layout`, `workspace.semantic_surfaces`, `workspace.tmp`, and `workspace.refs` are reported if they return

#### Scenario: CLI interface remains stable
- **WHEN** users invoke existing `isomer-cli` command groups that depend on Artifact Format processing, DeepScientist compatibility tools, Topic Team Specialization, or Workspace Path Resolution
- **THEN** the commands, options, text output intent, and JSON output structure remain compatible even though internal imports use the consolidated modules
