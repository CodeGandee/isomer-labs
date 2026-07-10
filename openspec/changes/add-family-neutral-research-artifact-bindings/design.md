## Context

The research-recording layer is largely family-neutral: it can store lifecycle records, managed JSON payload snapshots, semantic labels, lineage, relationships, file hints, query facets, and rendered views. Its only built-in structured-record provider is currently DeepSci-branded, however, and production DeepSci skills supply the missing semantic-to-storage decision through a shared placeholder registry, per-skill `placeholder-bindings.md`, and workspace bootstrap.

Kaoju currently stops at semantic artifact definitions. It names Survey Contracts, Related-Work Catalogs, Source Digests, Comparison Intent Documents, Topic Dataset Manifests, Audit Reports, and other outputs, but permits either unspecified recording APIs or file-backed Markdown or JSON. No active file decides the canonical representation, record kind, semantic label, profile, create command, revision behavior, query identity, or reset posture. The `manage-survey` helper nevertheless assumes that these records can be listed, shown, statused, and exported deterministically.

This design keeps semantic meaning owned by Kaoju skills and moves physical and API binding into separate pages. It adds one family-neutral provider rather than making Kaoju consume DeepSci refs or creating a second copy of DeepSci's generic structured-record engine.

## Goals / Non-Goals

**Goals:**

- Provide stable family-neutral format refs under `isomer:research/record-format/*` without changing existing DeepSci refs.
- Give every durable Kaoju output one storage-neutral semantic id and one explicit binding authority.
- Make managed JSON payload snapshots canonical and human-facing Markdown, CSV, matrices, and dossiers derived views or explicit exports.
- Preserve exact record kinds, semantic labels, producers, consumers, lineage, revisions, validation, query facets, files, and lifecycle commands across agents and rounds.
- Make Kaoju workspace bootstrap and `manage-survey` deterministic over the existing Topic Workspace and Workspace Runtime.
- Keep large repositories, datasets, models, checkpoints, and raw outputs out of structured payload storage while preserving their identities and provenance in manifest records.
- Generalize validation by configured research family without weakening any DeepSci rule or diagnostic.

**Non-Goals:**

- Migrate or rename `isomer:deepsci/record-format/*` refs, DeepSci placeholders, or existing DeepSci records.
- Add a Kaoju-specific database, Topic Workspace layout, top-level semantic label family, execution adapter, provider binding, or scheduler.
- Store repository trees, datasets, model weights, checkpoints, logs, or raw experiment outputs inside JSON payload snapshots.
- Replace the existing research-record CLI, query index, lineage DAG, reset mechanism, or Project Web record views.
- Define a Domain Agent Team Template or require formal multi-agent execution.

## Decisions

### 1. Add One Family-Neutral Built-in Provider

Add a built-in provider with id `isomer.research.record-formats` and refs shaped as:

```text
isomer:research/record-format/profile/<family>/<class>/<semantic-id>/v1
isomer:research/record-format/schema/research-structured-record/v1
isomer:research/record-format/template/markdown/research-structured-record/v1
```

The provider owns a reusable structured-record schema and Markdown renderer. It loads declarative built-in profile catalogs, beginning with Kaoju. Each profile entry names its family, semantic id, artifact class, record-kind compatibility, required payload paths, relationship paths, file paths, facet paths, renderer, compatibility version, and status. Profile-specific requirements remain data in the catalog rather than Python branches.

This is preferred to `isomer:kaoju/...` because validation, rendering, payload snapshots, and profile resolution are platform research services. It is preferred to reusing `isomer:deepsci/...` because that would make Kaoju's durable contract depend on another optional extension's identity. Existing DeepSci provider registration and all 197 current profile names remain unchanged.

### 2. Separate Kaoju Semantics from Bindings

`isomer-kaoju-shared/references/artifact-semantics.md` becomes the storage-neutral semantic registry. Active skills refer to exact ids shaped as `kaoju:<semantic-id>`, for example `kaoju:survey-contract`, `kaoju:related-work-catalog`, `kaoju:source-digest`, and `kaoju:audit-report`. Each registry row defines meaning, required semantic content, producer, consumer, and update intent, but no path, record kind, profile, or command.

Every Kaoju skill that produces accepted durable records receives `artifact-bindings.md`. The binding page maps exact semantic ids to:

- storage item and record kind;
- existing semantic label;
- `isomer:research/.../kaoju/...` format profile;
- producer, consumer, and actor metadata;
- payload staging and canonical snapshot behavior;
- expected lineage parents, lineage kind, and generation group;
- revision, follow-up, or metadata-only update policy;
- relationship, file, and query-facet metadata;
- validate, create, list, show, revise, status-update, render, export, and archive commands.

Kaoju uses `artifact-bindings.md`, not DeepSci migration placeholders. The validator compares semantic ids referenced by active skill guidance and the shared registry against binding rows, reporting missing, extra, duplicated, or cross-family bindings.

### 3. Introduce Family-Neutral Semantic Record Identity

Add `semantic_id` metadata and CLI option `--semantic-id` to structured research record creation, update, revise, list, and query paths. It identifies the durable semantic object independently of its producing skill or profile. The query index stores it as a normalized field.

DeepSci `--placeholder` remains supported and retains its current behavior. Internally, a placeholder may populate the generalized semantic identity field for indexing, but responses continue exposing the original placeholder metadata and commands do not rewrite existing records. New Kaoju bindings use only `--semantic-id kaoju:<id>`.

This is preferred to overloading `--placeholder`, because Kaoju semantic ids are stable domain objects rather than migration placeholders.

### 4. Use Existing Record Labels and Typed Record Kinds

Kaoju does not add top-level semantic labels. Bindings use existing `topic.records.artifacts`, `topic.records.views`, `topic.records.runs`, `topic.records.tasks`, and `topic.records.logs` according to record meaning.

| Semantic class | Default record treatment |
| --- | --- |
| Contracts, catalogs, deltas, reports, comparisons, and dossiers | `artifact` under `topic.records.artifacts` |
| Source Digests and claim-bearing inspection evidence | `evidence_item` under `topic.records.artifacts` |
| Proceed Decisions and blocking route decisions | `decision_record` under `topic.records.artifacts` |
| Current ledgers, manifests, terminal status, and binding indexes | `view_manifest` under `topic.records.views` |
| First-hand method and comparison executions | `run` under `topic.records.runs` |
| Logs and raw outputs | File attachments or external locators under their existing labels, never embedded into the structured payload |

The initial binding inventory covers workspace readiness, Survey Contract, Comparison Intent Document, Proceed Decision, Discovery Ledger, Related-Work Catalog and deltas, curated intake delta, Source Digest, Source Access Blocker, Claim-Evidence Ledger, material acquisition, Topic Dataset Manifest, Generated Dataset, Method Trial, theory comparison, Comparison Matrix, Audit Report, Claim Status Table, Field Summary, Kaoju Dossier, terminal report, method-trial Runs, and comparison Runs. Validation fails if active Kaoju guidance names another accepted durable output without a registered semantic id and binding disposition.

### 5. Make Payloads Canonical and Views Derived

Accepted Kaoju structured records use a managed JSON payload snapshot with required top-level `title`, `summary`, `artifact_family: "kaoju"`, `semantic_id`, `artifact_type`, and `sections`. Bindings define required section paths and authored refs. The recording API validates the payload against the selected family-neutral profile and snapshots it under the resolved record label.

Markdown and other human-readable outputs are on-demand renders or explicit exports. Agents revise the JSON record rather than editing rendered Markdown as authoritative state. Plain staging files and intermediate tables remain operation-local worker outputs until promoted through a binding.

Current-state objects such as the Topic Dataset Manifest, Claim-Evidence Ledger, Related-Work Catalog, and terminal status use `revise` for content changes so history remains visible. Deltas, audits, attempts, failures, and Runs remain separate descendant records. Repaired or adapted Runs never revise faithful Runs.

### 6. Keep Large Materials Behind Manifest Records

Repository trees, papers, datasets, models, checkpoints, raw outputs, and generated data files remain external, provider-managed, execution-managed, or Topic Workspace-managed material. Structured records contain only immutable locator, revision or digest, size, media or source class, access and license posture, managed-link ref, availability or staleness state, and Provenance Record refs.

The Topic Dataset Manifest is a bound `view_manifest`, not the dataset store. Registration and link mutation remain owned by the Topic Workspace owner. Generated Dataset records reference generator inputs, schema, seeds, checks, and the actual file or directory Artifact refs without embedding the data.

### 7. Make Kaoju Workspace Bootstrap Binding-Aware

`isomer-kaoju-workspace-mgr` validates:

1. Effective Topic Context and fresh Workspace Runtime state.
2. Required `topic.records.*` semantic labels.
3. Family-neutral provider and Kaoju profile resolution.
4. Shared semantic registry and selected skill binding coverage.
5. Topic-level Kaoju binding index and dataset-manifest posture.
6. Latest relevant records and duplicate or supersession posture.
7. Worker output policy for staging and exports.
8. Reset-checkpoint treatment for bootstrap records and any user-selected accepted survey state.

It records a binding index and readiness report or returns an explicit blocker. Ordinary Kaoju stages do not write accepted records until the selected semantic id resolves to one binding row and the required surface is ready.

### 8. Define `manage-survey` Through Canonical Queries

Extend list and query filters with `--artifact-family`, `--semantic-id`, and `--latest-only`. The query index derives family, semantic id, artifact type, procedure, terminal status, source class, verification depth, evidence verdict, claims, metrics, files, and explicit relationships from managed payloads and authored metadata.

`manage-survey` actions map to existing read and rendering operations:

- `list` queries `artifact_family=kaoju`, optionally by semantic id, status, procedure, or latest state;
- `show` opens the canonical payload and record metadata by stable record id;
- `status` resolves terminal and stage state from bound records and lineage;
- `export` renders or exports a selected canonical record without changing evidence or latest-state identity.

`manage-dataset` uses `kaoju:topic-dataset-manifest` and the same revision/query contract. Mutation still routes to the Topic Workspace owner.

### 9. Preserve DeepSci Compatibility

The existing DeepSci provider, catalog, schema versions, profile refs, binding files, placeholder CLI option, validators, and stored records remain active. Shared implementation helpers may be extracted to avoid duplicate schema loading or rendering code, but externally visible DeepSci behavior is unchanged.

No automatic alias from `isomer:deepsci/...` to `isomer:research/...` is introduced. This prevents profile identity drift and makes rollback the removal of the new provider registration, Kaoju profiles, semantic-id filters, and Kaoju bindings without rewriting DeepSci state.

## Risks / Trade-offs

- **A family-neutral provider can become an unbounded dumping ground** → Require explicit built-in catalog registration, stable family ownership, exact semantic ids, and deterministic collision validation.
- **A common schema may validate too little for individual Kaoju artifacts** → Let declarative profile entries add required payload paths and facet declarations while keeping validation code generic.
- **Binding pages can drift from the semantic registry or profile catalog** → Validate registry-to-binding-to-profile coverage in both directions and name the offending file, line, family, and semantic id.
- **Adding `semantic_id` can accidentally alter DeepSci placeholder queries** → Keep `--placeholder` behavior and output fields unchanged, add compatibility tests, and avoid rewriting existing records.
- **Large material locators may become stale while their manifest record remains valid JSON** → Require revision, digest or staleness policy, observed time, access status, and explicit refresh behavior in material bindings.
- **`latest-only` can hide competing ready records** → Resolve explicit revision and supersession metadata first; report ambiguity instead of silently choosing by timestamp.
- **Reset preservation may retain more state than the user expects** → Preserve only bootstrap state and user-selected survey refs, report the checkpoint delta, and leave ordinary post-checkpoint records subject to the accepted reset plan.

## Migration Plan

1. Add and register the family-neutral provider, schema, template, and Kaoju profile catalog without changing DeepSci registration.
2. Add `semantic_id` recording and query support with `--placeholder` compatibility and index migration or rebuild coverage.
3. Add the Kaoju semantic registry, per-skill binding pages, workspace bootstrap, and validator rules.
4. Update Kaoju skills and manager commands to use bound payload-first records, latest-context preflight, worker output policy, lineage, revisions, and reset posture.
5. Rebuild or validate query indexes for test Topic Workspaces and verify family, semantic-id, latest, facet, file, and lineage queries.
6. Run DeepSci provider, binding, query, reset, GUI, and record regression suites before enabling Kaoju bindings in packaged assets.
7. Rollback disables the new provider and removes Kaoju binding guidance and filters; existing Kaoju records remain generic durable records addressable by id and locator, while DeepSci records remain untouched.

## Open Questions

No implementation-blocking product choice remains. The exact initial required payload paths and facet paths for each Kaoju semantic id should be finalized while authoring the declarative profile catalog and binding tables, then locked by fixtures and validation tests.
