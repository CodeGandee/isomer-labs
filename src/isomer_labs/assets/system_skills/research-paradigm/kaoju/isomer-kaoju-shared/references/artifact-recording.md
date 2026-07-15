# Kaoju Artifact Recording

## Latest-Context Preflight

Before a durable write, resolve Effective Topic Context and fresh Workspace Runtime state. Read the applicable semantic id from `artifact-semantics.md`, resolve its physical contract with `isomer-cli --print-json ext kaoju bindings describe KAOJU:WHAT`, and read the producer skill's concise `artifact-bindings.md`. Query the state DB with `project artifacts latest|list|show`, the exact semantic id, and the binding-defined scope key. Inspect revision and supersession lineage, and stop with a storage blocker when the registry, profile, label, query surface, content mode, actor posture, or current choice is unavailable or ambiguous. Never scan directories to discover durable state.

## Canonical Payload

Accepted structured Kaoju state is a managed JSON payload snapshot. Author a staging payload with non-empty `title`, `summary`, `artifact_family: "kaoju"`, exact `semantic_id`, exact `artifact_type`, and a non-empty `sections` object. Include actor metadata, authored relationships, file refs, query facets, and direct lineage inputs required by the binding. Validate before creation or revision.

Operation-local notes, tables, payload staging, logs, and exports follow the resolved worker output policy. They remain pre-promotion or derived material. Never treat rendered Markdown, CSV, a matrix, or a dossier export as canonical structured state; render on demand or export explicitly from the accepted JSON record.

## Revision and Lineage

Use `project artifacts put` for a new current-state object or append-only event. Use `project artifacts revise` for a current-state content change only when the resolved binding permits revision, so the prior version remains historical. Create deltas, audits, attempts, failures, repairs, and Runs as separate descendants with immediate parents and the binding's lineage kind. Use metadata-only update only for lifecycle or routing fields that do not change accepted content. A repaired or adapted Run never revises a faithful Run.

## Structured Diagnostics

On validation failure, report the semantic id, binding page, profile ref, failing JSON path, diagnostic code, and repair route. If the selected binding cannot be resolved, return a storage blocker. Do not invent a location, use a DeepSci profile, write canonical Markdown, or leave accepted JSON untracked.

## Large-Material Boundary

Keep papers, repository trees, datasets, models, checkpoints, generated-data directories, raw outputs, and logs outside structured payload snapshots. The applicable material or dataset manifest stores immutable locator, revision or digest, source class, size when known, access and license posture, observed time, staleness policy, managed-link ref, file Artifact refs, and Provenance Record refs. The Topic Dataset Manifest indexes datasets; it is not a dataset store. Only the Topic Workspace owner mutates managed links, and removal never deletes or rewrites the external target.

## Content Authority

The managed JSON file is authoritative for structured content. An ordinary-file Artifact is authoritative through its recorded checksum, size, media type, and locator. A multi-file directory is authoritative through its versioned checksummed manifest. An authorized external path and Canonical External Repository remain externally owned. State-DB records link to content but do not make a rendered view, export, staged copy, source-tree file, or local temporary file canonical.

## Resumable Operations

Use a Service Request for supported owner mutation and an Execution Adapter Command Request for executable work. Record Gates separately from dispatch. Begin a Run before claim-bearing execution, checkpoint completed Artifact refs, pending Gate, blocker and Service Request refs, and the first incomplete stage, then complete it with immutable logs and outputs. A paused or blocked terminal report must carry a stable resume hint.
