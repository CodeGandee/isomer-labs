# Kaoju Artifact Recording

## Latest-Context Preflight

Before a durable write, resolve Effective Topic Context and fresh Workspace Runtime state. Read the applicable semantic id from `artifact-semantics.md`, then read the producer skill's `artifact-bindings.md`. Query current candidates by exact artifact family and semantic id, inspect revision and supersession lineage, and stop with a storage blocker when the binding, profile, label, query surface, actor posture, or latest choice is unavailable or ambiguous.

## Canonical Payload

Accepted structured Kaoju state is a managed JSON payload snapshot. Author a staging payload with non-empty `title`, `summary`, `artifact_family: "kaoju"`, exact `semantic_id`, exact `artifact_type`, and a non-empty `sections` object. Include actor metadata, authored relationships, file refs, query facets, and direct lineage inputs required by the binding. Validate before creation or revision.

Operation-local notes, tables, payload staging, logs, and exports follow the resolved worker output policy. They remain pre-promotion or derived material. Never treat rendered Markdown, CSV, a matrix, or a dossier export as canonical structured state; render on demand or export explicitly from the accepted JSON record.

## Revision and Lineage

Use revision for a current-state object's content change so the prior version remains historical. Create deltas, audits, attempts, failures, repairs, and Runs as separate descendants with immediate parents and the binding's lineage kind. Use metadata-only update only for lifecycle or routing fields that do not change accepted content. A repaired or adapted Run never revises a faithful Run.

## Structured Diagnostics

On validation failure, report the semantic id, binding page, profile ref, failing JSON path, diagnostic code, and repair route. If the selected binding cannot be resolved, return a storage blocker. Do not invent a location, use a DeepSci profile, write canonical Markdown, or leave accepted JSON untracked.

## Large-Material Boundary

Keep papers, repository trees, datasets, models, checkpoints, generated-data directories, raw outputs, and logs outside structured payload snapshots. The applicable material or dataset manifest stores immutable locator, revision or digest, source class, size when known, access and license posture, observed time, staleness policy, managed-link ref, file Artifact refs, and Provenance Record refs. The Topic Dataset Manifest indexes datasets; it is not a dataset store. Only the Topic Workspace owner mutates managed links, and removal never deletes or rewrites the external target.
