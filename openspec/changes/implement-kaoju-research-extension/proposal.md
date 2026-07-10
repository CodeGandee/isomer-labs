## Why

Isomer Labs has packaged research skills for hypothesis-driven DeepSci work but no built-in extension for evidence-led literature and codebase surveys that can continue into source checkout, model or dataset acquisition, first-hand method trials, and controlled comparisons. The approved Kaoju design now defines that missing survey workflow and is ready to become an optional packaged system-skill extension.

## What Changes

- Add the production `isomer-kaoju-*` skill family under `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/`, including the pipeline coordinator, shared and workspace contracts, and focused frame, discover, acquire, examine, reproduce, compare, audit, and synthesize stages.
- Implement the pipeline's survey procedures for field landscapes, curated-source intake, seed-direction expansion, theory comparison, paper-method trials, empirical comparison, and survey audit and synthesis.
- Implement grouped `manage-survey` and `manage-dataset` helper commands rather than separate CRUD verbs, with clarification-first as a shared interaction mode.
- Preserve source identity, exact locators, provenance, verification depth, evidence verdict, Run purpose, execution fidelity, generated-data limitations, comparison intent, and terminal pass status across skill handoffs.
- Register Kaoju as the optional packaged extension `kaoju`, expose begin and end callback insertion points, and make it discoverable and installable through the existing system-skill catalog and installer.
- Extend research-paradigm validation, namespace checks, package-asset tests, installer tests, and documentation for the Kaoju family without weakening DeepSci-specific validation.
- Reuse existing Topic Workspace, research-recording, artifact-format, provider-binding, execution-adapter, Gate, and bounded-run contracts; do not add a Kaoju-specific runtime database, provider, scheduler, or Domain Agent Team Template.

## Capabilities

### New Capabilities

- `kaoju-research-extension`: Defines the packaged Kaoju skill family, survey procedures and helpers, durable evidence semantics, guarded execution behavior, and user-visible terminal outputs.

### Modified Capabilities

- `packaged-system-skills`: Add the optional `kaoju` manifest group, packaged skill inventory, callback metadata, and safe materialization coverage.
- `system-skill-namespaces`: Recognize `isomer-kaoju-*` as the active namespace for the `research-paradigm/kaoju/` extension family and validate identity consistency.
- `research-paradigm-skills`: Extend the research-paradigm documentation and validation harness to cover the production Kaoju family while preserving existing DeepSci layout and validation rules.

## Impact

- New packaged assets under `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/` and updates to the research-paradigm README and system-skill manifest.
- Updates to `scripts/validate_research_paradigm_skillset.py` and its unit tests for family-aware validation.
- Updates to package-asset, namespace, callback, installer-selection, and materialization tests for the `kaoju` extension.
- Documentation and skill manifests gain Kaoju installation, routing, subcommand, evidence, and external-owner guidance.
- Existing generic extension selection and Project extension declarations will expose `kaoju` from catalog metadata without a new CLI command or persistence model.
