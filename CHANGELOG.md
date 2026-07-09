# Changelog

All notable changes to this project are documented here.

This changelog follows the GitHub release-note convention of keeping the newest changes first, grouping entries by change type, and linking release comparisons when a tag exists.

## [Unreleased]

## [0.2.3] - 2026-07-09

This bugfix release improves setup guidance for paper-writing workflows.

### Changed

- Added README prerequisite guidance for TeX rendering in paper-writing workflows, recommending Tectonic and showing the Pixi global install command.

## [0.2.2] - 2026-07-09

This bugfix release improves packaged system skill guidance for Pixi-scoped profiler, debugger, tracer, and memory-checker commands.

### Changed

- Added generic wrapper-tool command-shape guidance so Topic Workspace setup and verification prefer `pixi run <wrapper-tool> ... <target-command>` over `<wrapper-tool> pixi run ...`.
- Added bounded-run and NVIDIA-specific examples for tools such as `ncu`, `nsys`, `valgrind`, `gdb`, and `cuda-gdb`.
- Synced and archived the completed OpenSpec change for Pixi wrapper-tool command-shape guidance.

## [0.2.1] - 2026-07-09

This bugfix release updates published package metadata and README guidance so package indexes and new users can find the repository, documentation, and recommended CLI-agent setup path.

### Changed

- Added package project URLs so PyPI can display Repository, Documentation, Issues, and Changelog links.
- Added the GitHub Pages documentation link directly under the README title.
- Added README guidance for CLI-agent-driven usage, required Pixi setup, and optional Houmao installation.

## [0.2.0] - 2026-07-09

This release expands the Project operator surface, improves packaged system skill routing, and adds the Isomer-owned Houmao Topic Service Master identity contract.

### Added

- Added the system skill installer CLI and release verification workflow.
- Added `isomer-cli system-skills upgrade` to refresh installed packaged system skills, remove manifest-tracked stale skill paths, and preserve or override projection mode.
- Added target-root system skill manifests at `isomer-labs-skill-manifest.json` to record installed Isomer skill names, source paths, projection modes, package version, and update time.
- Added the toolbox manager system skill and routed toolbox-manager access from operator entrypoints.
- Added the GUI Manager operator skill and packaged it with the core system skill set.
- Added top-level `isomer-cli doctor` diagnostics and read-only host, Project, Pixi, and topic-environment checks.
- Added nested Isomer Project initialization and nearest-child Project discovery semantics.
- Added Isomer-managed Houmao skill routing with Project Manifest integration policy, Project-local projected Houmao skills, and skill-context CLI output.
- Added Topic Service Master name derivation, Houmao binding persistence in Topic Workspace Manifests, binding CLI commands, and self/skill-context identity payloads.
- Added project web GUI refinements for graph views, topic views, record summaries, and GUI details.
- Added design planning artifacts for Imsight agent skill handling.

### Changed

- Refined project CLI workflows.
- Changed packaged system-skill installation ownership to use reserved skill names under the target skill root instead of per-skill `.isomer-system-skill.json` marker files.
- Updated `system-skills install`, `status`, and `uninstall` output to report root manifest metadata, preserved existing paths, forced replacements, invalid projection shapes, and manifest updates.
- Updated packaged system skill documentation and CLI reference for name-based install slots, `--force`, root manifests, and upgrade behavior.
- Improved top-level and command-group help navigation, including empty invocation help and package version reporting.
- Unified the toolbox installation flow.
- Promoted doctor guidance out of the Project command group and into global CLI and operator skill guidance.
- Updated Topic Creator, Houmao interop, Topic Service Master lifecycle, Welcome, and Entrypoint skill guidance for the new routing and binding contracts.
- Reorganized public documentation and added research workflow tutorials.
- Defaulted toolbox skills to manual routing where appropriate.
- Restructured GPU toolbox priors and clarified toolbox creator example-content guidance.

### Fixed

- Included `README.md` in package metadata so built distributions carry the project readme.

### Breaking

- Removed per-skill hidden marker files as the ownership source for packaged system-skill install, status, and uninstall behavior. Existing same-name paths are now preserved unless users pass `system-skills install --force`.

### Maintenance

- Synced and archived completed OpenSpec changes for the `0.2.0` release set.
- Recorded system skill installer release verification.

## [0.1.0] - 2026-07-08

Initial tagged release of Isomer Labs.

### Added

- Added the Pixi-managed Python package, editable install setup, and `isomer-cli` entrypoint.
- Added Project discovery, Research Topic CRUD, topic profiles, project doctor groundwork, Project cleanup, and Project content-root relocation.
- Added Topic Workspace management, manifest path resolution, default Pixi binding resolution, standard workspace layout, local temporary surfaces, and semantic storage contracts.
- Added Topic Team instantiation, specialization, guided specialization, static specialization, and recovery paths.
- Added operator system skills including welcome, entrypoint, switch identity, project manager, topic creator, topic workspace manager, and topic package install routing.
- Added agent-facing context commands, topic guidance, self queries, worker output-root policy, and topic reset checkpoints.
- Added Houmao integration groundwork, handoffs, overlay relocation under Isomer config, and DeepSci mini team support.
- Added agent environment setup services, package repository resolution, resource-safe environment verification guidance, and agent-friendly CLI error reporting.
- Added research paradigm skillsets, validation, DeepSci migration support, v2 research skills, manual research workflows, and structured research records.
- Added research record query index, payload-file storage, artifact lineage DAG, idea source contract, and topic idea iteration web GUI.
- Added the project web GUI, workbench, state model, data contract schemas, callback insertion points, topic views, lineage graph interactions, and themed settings.
- Added GPU analytical modeling skills, GPU reference map skill, and GPU experiment evidence gates.
- Added toolbox runtime parameters and renamed the earlier user plugin system to toolbox terminology.
- Added release automation for PyPI and GitHub Pages publishing.

### Changed

- Modularized the CLI and source package structure.
- Consolidated module boundaries and topic team specialization skill boundaries.
- Promoted DeepSci research skills and decoupled team templates for PyPI packaging.
- Refined topic setup, Topic Creator staged flow, Topic Creator readiness flow, and DeepSci workflows.
- Updated system skill interfaces and operator templates.

### Fixed

- Declared package runtime dependencies for the `v0.1.0` release.
- Stabilized idea lineage graph interactions.
- Required concrete topic selection for `init-topic`.
- Required topic team prerequisite artifacts.
- Enforced project-wide Agent Instance id uniqueness.
- Used the global `isomer-cli` in skills.

### Documentation

- Documented the Isomer naming origin, project goal, workspace architecture, multi-agent domain language, GUI handling architecture, and domain topic team lifecycle.
- Added and archived OpenSpec proposals for research recording, research lifecycle state, research execution extensions, CLI topic context, topic reset checkpoints, GUI data contracts, and idea lineage.
- Added research workflow, environment setup, resource gate, team specialization, and external repository routing guidance.
- Updated `extern/orphan/README.md` with local checkout recreation instructions.

### Maintenance

- Added OpenSpec support assets and archived completed OpenSpec changes throughout the release.
- Removed generated Isomer project state and vendored skill creator material.
- Excluded local heavy folders from VS Code and updated local package lock metadata.

[Unreleased]: https://github.com/CodeGandee/isomer-labs/compare/v0.2.3...HEAD
[0.2.3]: https://github.com/CodeGandee/isomer-labs/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/CodeGandee/isomer-labs/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/CodeGandee/isomer-labs/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/CodeGandee/isomer-labs/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/CodeGandee/isomer-labs/releases/tag/v0.1.0
