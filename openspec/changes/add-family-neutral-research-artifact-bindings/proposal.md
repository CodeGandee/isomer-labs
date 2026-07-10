## Why

Kaoju defines the meaning and minimum contents of survey artifacts but does not define their canonical record kinds, semantic labels, format profiles, lifecycle commands, query keys, or reset-survival behavior. This makes resumable surveys, audited deltas, multi-agent handoffs, dataset reuse, and `manage-survey` nondeterministic even though the platform already has most of the required structured-record machinery behind DeepSci-specific refs.

## What Changes

- Add a family-neutral `isomer:research/record-format/*` provider contract for structured research payload validation and rendering, with declarative profile catalogs that can name extension-specific artifact semantics without coupling them to DeepSci.
- Keep Kaoju artifact semantics in its shared vocabulary and place concrete storage bindings in separate binding pages, following the same semantic-versus-binding separation used by DeepSci.
- Bind every durable Kaoju survey object to an exact semantic id, record kind, semantic label, family-neutral format profile, producer and consumer, payload contract, lineage policy, revision policy, query metadata, and create/read/revise/archive command shape.
- Make structured JSON payload snapshots canonical for accepted Kaoju records; treat Markdown, CSV, dossiers, tables, and other human-facing materializations as derived views or explicit exports.
- Extend Kaoju workspace readiness to validate record surfaces, binding coverage, latest-context preflight, worker-output policy, queryability, and Topic Workspace reset survival before durable survey work proceeds.
- Give `manage-survey` deterministic list, show, status, lineage, and export behavior over bound Kaoju records instead of relying on unspecified “existing interfaces.”
- Keep repositories, datasets, models, checkpoints, raw outputs, and other large materials outside structured payload storage; record their immutable locators, revisions, digests, access, licenses, managed links, and provenance through bound material-manifest records.
- Preserve all existing `isomer:deepsci/record-format/*` refs and DeepSci binding behavior. A future DeepSci migration may reuse the family-neutral provider, but ref migration is outside this change.

## Capabilities

### New Capabilities

- `kaoju-artifact-bindings`: Defines the separated Kaoju semantic registry and concrete storage-binding inventory, canonical payload and view policy, lifecycle and lineage rules, material-manifest boundary, workspace bootstrap, and survey-management behavior.

### Modified Capabilities

- `artifact-format-processing`: Add the family-neutral `isomer:research/record-format/*` provider namespace, reusable structured-record schema and renderer, declarative family profile catalogs, and compatibility behavior alongside existing DeepSci refs.
- `research-recording-contracts`: Add a family-neutral semantic artifact id to structured research record creation, metadata, revision, and read APIs while retaining DeepSci placeholder compatibility.
- `research-placeholder-bindings`: Generalize binding-page and validation contracts so configured research families such as Kaoju can bind semantic artifact ids without adopting DeepSci migration placeholders.
- `research-record-query-index`: Add deterministic family and artifact-semantic filtering and profile-driven Kaoju relationship, file, claim, metric, catalog, and status facets needed by survey management.
- `research-paradigm-skills`: Require production Kaoju skills to use their binding authority, latest-context and worker-output rules, workspace storage bootstrap, canonical lineage and revision behavior, and explicit blockers when bindings or surfaces are unavailable.

## Impact

- New family-neutral Artifact Format provider assets and registration under `src/isomer_labs/`, plus compatibility-sensitive updates to artifact-format resolution, research-record storage, query indexing, CLI filters, and tests.
- New Kaoju semantic registry and binding pages under `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/`, with updates to shared, workspace manager, stage, pipeline, and manager guidance.
- Research-paradigm validation becomes binding-family aware while retaining every current DeepSci inventory, payload, display, lineage, and profile diagnostic.
- Topic Workspace records gain canonical Kaoju JSON payloads and derived views; large acquired materials remain external or workspace-managed and are referenced rather than embedded.
- Documentation gains the family-neutral profile namespace, Kaoju storage lifecycle, material boundary, migration compatibility, and survey-management query contract.
