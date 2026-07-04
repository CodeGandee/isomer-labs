## 1. Artifact Format Processing

- [x] 1.1 Create `isomer_labs.artifact_formats.processing` by consolidating resolver, payload/schema loading, validation, template loading, and rendering behavior.
- [x] 1.2 Update Artifact Format package exports and repository imports to use the consolidated processing module.
- [x] 1.3 Remove obsolete Artifact Format helper modules and guard against their return.

## 2. DeepScientist Extension Tools

- [x] 2.1 Create `isomer_labs.deepsci_ext.tools` by consolidating tool registry constants, tool listing, tool-name splitting, JSON input/output helpers, unsupported-tool payloads, `call_tool`, and compatibility service behavior.
- [x] 2.2 Update DeepScientist CLI, package exports, tests, and callers to use the consolidated tools module.
- [x] 2.3 Remove obsolete DeepScientist helper modules and guard against their return.

## 3. Topic Team Specialization

- [x] 3.1 Fold Domain Agent Team Template harness checks from `teams.template_harness` into `teams.templates`.
- [x] 3.2 Fold Topic Team Instantiation Packet validation from `teams.packet_validation` into `teams.instantiation`.
- [x] 3.3 Fold Topic Agent Team Profile provenance and bundle-layout validation from `teams.profile_bundle_validation` into `teams.profiles`.
- [x] 3.4 Update team imports, delete obsolete helper modules, and guard against their return.

## 4. Workspace Path Helpers

- [x] 4.1 Create `isomer_labs.workspace.surfaces` by consolidating Semantic Workspace Surface Label catalog, Default Layout Profile helpers, and Local Tmp Surface policy helpers.
- [x] 4.2 Rename Workspace Path Resolution implementation from `workspace.paths` to `workspace.path_resolution` and move Agent Workspace ref helpers into it.
- [x] 4.3 Update workspace, runtime, project, CLI, team, and test imports to use `workspace.surfaces` and `workspace.path_resolution`.
- [x] 4.4 Remove obsolete Workspace helper modules and guard against their return.

## 5. Validation

- [x] 5.1 Update source architecture tests for the new canonical module sets and removed helper-shard modules.
- [x] 5.2 Run lint, typecheck, unit tests, and focused CLI smoke checks for affected command groups.
