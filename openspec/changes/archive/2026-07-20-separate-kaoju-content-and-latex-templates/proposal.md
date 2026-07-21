## Why

Kaoju currently manages only named MyST templates, while LaTeX templates are transient paper-line derivations that are not actually composed into PDF builds. This prevents a user from stocking a multi-file LaTeX directory as the default, exporting it for editing, applying the edits back, and relying on later paper builds to use the selected presentation state.

## What Changes

- Name MyST-oriented paper templates “content templates” in user-facing CLI, skill, documentation, and status output while preserving `KAOJU:PAPER-TEMPLATE-MYST` as their durable identity.
- Add a separate named mutable “LaTeX template” namespace backed by a new `KAOJU:PAPER-TEMPLATE-LATEX` directory-tree Artifact. Each Topic Workspace may stock `main` plus other named LaTeX templates.
- Generalize named-template create, copy, update, file, metadata, export, observe, archive, delete, and migration behavior across the content and LaTeX namespaces without conflating their defaults or working copies.
- Require stocked LaTeX templates to declare an entrypoint, composition contract, build profile, source provenance, and multi-file integrity metadata.
- Change TeX initialization into composition from an exact canonical MyST draft and an exact observed LaTeX template state. Retain `KAOJU:PAPER-TEMPLATE-TEX` as a derived paper-line snapshot rather than stocked mutable state.
- Make PDF builds consume the selected template snapshot and declared entrypoint instead of validating and then ignoring the template tree or always compiling `main.tex`.
- Record content-template and LaTeX-template names, stable refs, state tokens, and observed digests separately in paper contracts, TeX manifests, status output, validation reports, and publication lineage.
- Detect working-copy drift, stocked-template drift, and paper-local TeX repair drift without silently propagating any of them.
- Preserve historical `KAOJU:PAPER-TEMPLATE-TEX` and `KAOJU:WRITING-TEMPLATE` records, and provide explicit adoption into a named LaTeX template without inferring or changing canonical MyST content.
- Migrate every currently registered Topic Workspace to the latest template contract, including adopting its selected active presentation template as `latex/main` when the source is unambiguous.
- **BREAKING** Reserve unqualified “template” wording for compatibility only. New agent guidance and new CLI examples must identify either a content template or a LaTeX template.

## Capabilities

### New Capabilities

None. The change completes the existing Kaoju paper-production and template-management capabilities instead of creating a separate subsystem.

### Modified Capabilities

- `kaoju-paper-production`: Separate canonical content-template state from named LaTeX presentation state and define deterministic composition, drift, and migration behavior.
- `kaoju-cli-services`: Add format-explicit template CRUD and exchange commands, template adoption, composition, entrypoint-aware builds, and migration diagnostics.
- `kaoju-artifact-bindings`: Add the named LaTeX-template binding and update paper, template, snapshot, draft, audit, export, and publication relationships.
- `research-paradigm-skills`: Teach Kaoju routing and writing skills to distinguish content templates from LaTeX templates throughout drafting, export, update, composition, repair, and status reporting.
- `kaoju-research-extension`: Keep `manage-paper-template` public while making its content-versus-LaTeX selection and defaulting rules explicit.
- `workspace-path-resolution`: Separate content-template and LaTeX-template working copies beneath the resolved paper-template exchange root while retaining the legacy content-template path during migration.

## Impact

The change affects Kaoju binding and semantic resources, structured record profiles, named-template services, paper composition and build services, CLI command registration, Workspace Path Resolution, migration logic, packaged Kaoju skills and process data, documentation, unit and integration tests, and all existing Topic Workspace runtime records. No new database table is required; both template namespaces use the existing lifecycle-record and managed-directory infrastructure.
