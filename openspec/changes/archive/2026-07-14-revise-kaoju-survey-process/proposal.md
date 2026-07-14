## Why

The accepted Kaoju survey-process use cases require direction selection, reading-list curation, durable source ingestion, MyST-first paper production, LLM Wiki export, source-code acquisition, environment preparation, and approved code trials. The current Kaoju skills and CLI expose useful low-level records and LaTeX helpers, but they do not provide these user intents as a coherent, resumable process and their LaTeX-first paper path contradicts the accepted MyST decision.

## What Changes

- Refactor `isomer-kaoju-pipeline` into a thin intent router that supports all ten survey-process use cases while preserving existing public procedure names as compatibility routes.
- Refactor the Kaoju stage skills so research judgment remains in skills, while deterministic persistence, path resolution, conversion, repository acquisition, environment dispatch, builds, and viewer operations use typed `isomer-cli` services.
- Add direction-owned `kaoju:direction-set` and `kaoju:reading-list` workflows with clarification, human selection, query provenance, source identity, coverage warnings, revision history, and resumable state.
- Add durable reading-item and source-code ingestion that checks the artifact library first, resolves all managed paths through `isomer-cli`, registers local or online material, and produces claim-level evidence with immutable source locators.
- **BREAKING** Replace the canonical LaTeX-first Kaoju paper path with MyST structure, template, and draft artifacts. Markdown becomes a derived review view, while TeX and PDF become derived publication artifacts that retain agent inspection and build provenance.
- Add versioned MyST template export and apply operations with manifests, base digests, validation, conflict detection, and draft regeneration.
- Add a self-contained Isomer LLM Wiki exporter and compatible bundled viewer deployment path that does not invoke the external `imsight-llm-wiki` skill.
- Separate code-run environment preparation from trial execution. Environment mutation is performed through a recorded Service Request, while trials require an approved plan and produce durable Run, result, log, output, and timing records.
- Add a versioned semantic binding registry and canonical project artifact CLI that infer record kind, format profile, semantic workspace label, content mode, producer policy, and revision scope from an exact semantic artifact id.
- Add scoped latest-record lookup so direction-owned or source-owned current artifacts do not collide under a topic-wide semantic id.
- Supersede the LaTeX-first requirements and unfinished conflicting tasks in `add-kaoju-paper-writing`; retain compatible audit, evidence, validation, and build-provenance requirements.

## Capabilities

### New Capabilities

- `kaoju-survey-intents`: User-facing direction selection, reading-list curation, deep source ingestion, approval, audit prerequisites, and resumable routing for UC-01 through UC-03.
- `kaoju-paper-production`: MyST-first drafting, manual template exchange, derived Markdown, agent-refined TeX, PDF compilation, and revision provenance for UC-04 through UC-06.
- `kaoju-wiki-export`: Accepted-artifact export to an LLM Wiki, versioned mapping metadata, compatible viewer deployment, and local viewer launch for UC-07.
- `kaoju-code-execution`: Repository resolution and ingestion, Service Request-backed environment preparation, smoke verification, approved source-code trials, and generated-data capability probes for UC-08 through UC-10.
- `kaoju-cli-services`: Typed project artifact, Run, repository acquisition, Service Request, Kaoju paper, and Kaoju wiki CLI operations with compatibility aliases for current research record and template commands.

### Modified Capabilities

- `kaoju-artifact-bindings`: Add every survey-process semantic artifact, scoped revision rules, file and directory content modes, and a single machine-readable binding authority.
- `kaoju-research-extension`: Add the ten survey-process intents, their prerequisites and terminal behavior, new trial and export owners, and compatibility routing for existing procedures.
- `packaged-system-skills`: Package and validate the refactored Kaoju skill suite, new trial and export skills, direct resources, callbacks, and manifest-derived installation metadata.
- `research-paradigm-skills`: Change Kaoju skill behavior from prompt-encoded storage and LaTeX-first output to DB-resolved artifacts, MyST-first writing, Service Request-backed environment preparation, and adapter-backed execution.

## Impact

- Affected system skills: `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/`, relevant operator and service skills, packaged manifests, generated skill assets, and skill validation tests.
- Affected CLI and services: project artifact and Run commands, repository acquisition, Service Request dispatch, Kaoju paper and wiki commands, transitional research record aliases, and the current research template commands.
- Affected state and schemas: Workspace Runtime record queries, scoped current-record resolution, Artifact Format Profiles, Kaoju schemas and renderers, lineage and provenance, directory manifests, and migration aliases for legacy writing records.
- Affected execution paths: repository cloning, Pixi environment mutation, smoke runs, source-code trials, document builds, and viewer launch must route through registered Research Operation Extension Points and Execution Adapter Command Requests.
- New packaged assets may include MyST templates, conversion helpers, export schemas, and a licensed or independently implemented compatible LLM Wiki viewer.
- The change requires new unit and integration coverage for each use case plus compatibility, migration, resumption, Gate, path-resolution, and no-directory-scanning invariants.
