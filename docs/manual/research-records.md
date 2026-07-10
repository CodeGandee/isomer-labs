# Research Records

Research records are durable artifacts that describe ideas, decisions, diagnostics, experiments, surveys, papers, and other outputs from a topic. Structured records use managed JSON payload snapshots as canonical state. The SQLite query index records identity, locators, lineage, files, and facets; rendered Markdown, CSV, matrices, and dossiers are derived views or explicit exports.

The GUI uses record metadata to build topic overview pages, idea lineage graphs, JSON inspectors, markdown previews, and artifact links. Agents should write records through the supported CLI or library APIs so the file index and relationship DAG stay consistent.

Records may contain more fields than the GUI currently displays. GUI data-contract schemas validate required fields and allow extra fields so newer agents can write richer payloads without breaking older viewers.

## Family-Neutral Structured Formats

Built-in extension-neutral profiles use `isomer:research/record-format/profile/<family>/<class>/<semantic-id>/v1`. They share `isomer:research/record-format/schema/research-structured-record/v1` and `isomer:research/record-format/template/markdown/research-structured-record/v1`. The packaged Kaoju catalog is declarative: each entry defines compatible record kinds, required payload paths, relationship and file paths, query facets, renderer, version, and status.

Every neutral payload contains non-empty `title`, `summary`, `artifact_family`, `semantic_id`, `artifact_type`, and `sections`. Create it with the exact producer binding:

```bash
isomer-cli --print-json ext research records create \
  --topic my-topic \
  --record-kind artifact \
  --semantic-label topic.records.artifacts \
  --semantic-id kaoju:survey-contract \
  --format-profile isomer:research/record-format/profile/kaoju/contract/survey-contract/v1 \
  --skill isomer-kaoju-frame \
  --producer isomer-kaoju-frame \
  --consumer isomer-kaoju-discover \
  --payload-file survey-contract.json
```

Use `revise` for content changes to current-state objects. Use metadata-only `update` for lifecycle or routing changes. Deltas, audits, failures, repaired attempts, and Runs remain separate descendants. The original DeepSci `--placeholder` contract and all `isomer:deepsci/record-format/*` refs remain supported without aliasing.

## Query and Material Boundaries

Query neutral records with exact `--artifact-family`, `--semantic-id`, `--procedure`, and optional `--latest-only` filters. Explicit revision and supersession metadata determine latest candidates; competing active records produce ambiguity diagnostics. Profile-declared paths drive relationship, file, claim, metric, catalog, source, evidence, procedure, and terminal-status facets without family-specific backend code.

Repository trees, papers, datasets, model weights, checkpoints, raw outputs, and logs remain external or Topic Workspace-managed material. Structured records store immutable locators, revisions or digests, access and license posture, managed links, file refs, observed time, staleness policy, and provenance. A Topic Dataset Manifest indexes datasets; it does not contain them.
