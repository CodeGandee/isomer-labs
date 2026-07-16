# Research Records

Research records are durable artifacts that describe ideas, decisions, diagnostics, experiments, surveys, papers, and other outputs from a topic. Structured records use managed JSON payload snapshots as canonical state. The SQLite query index records identity, locators, lineage, files, and facets; rendered Markdown, CSV, matrices, and dossiers are derived views or explicit exports.

The GUI uses record metadata to build topic overview pages, idea lineage graphs, JSON inspectors, markdown previews, and artifact links. Agents should write records through the supported CLI or library APIs so the file index and relationship DAG stay consistent.

Records may contain more fields than the GUI currently displays. GUI data-contract schemas validate required fields and allow extra fields so newer agents can write richer payloads without breaking older viewers.

Idea-bearing records have an additional acceptance obligation. Their structured payload declares canonical Research Idea identity, known independent facets, exact Idea Realization paths, generation membership, justified Idea Lineage Edges, complete considered option sets, and transitions. The record and promised canonical effects commit in one transaction. A profile that promises those effects fails acceptance if any required effect fails; a non-idea-bearing profile does not infer ideas. See [Research Idea Portfolio](research-idea-portfolio.md).

## Family-Neutral Structured Formats

Built-in extension-neutral profiles use `isomer:research/record-format/profile/<family>/<class>/<semantic-id>/v1`. They share `isomer:research/record-format/schema/research-structured-record/v1` and `isomer:research/record-format/template/markdown/research-structured-record/v1`. The packaged Kaoju catalog is declarative: each entry defines compatible record kinds, required payload paths, relationship and file paths, query facets, renderer, version, and status.

Every neutral payload contains non-empty `title`, `summary`, `artifact_family`, `semantic_id`, `artifact_type`, and `sections`. Extension-owned durable artifact identities use exact uppercase `EXTENSION-NAME:WHAT` syntax. Kaoju producers inspect the installed contract with `ext kaoju bindings describe KAOJU:WHAT` and let the typed Artifact service infer record kind, profile, semantic label, content mode, scope policy, and managed locator:

```bash
isomer-cli --print-json project artifacts describe KAOJU:SURVEY-CONTRACT \
  --topic my-topic

isomer-cli --print-json project artifacts put \
  KAOJU:SURVEY-CONTRACT survey-contract.json \
  --topic my-topic \
  --producer isomer-kaoju-frame \
  --scope-key survey:main \
  --relationships-json '[]'
```

Use `project artifacts revise` for binding-permitted content changes to current-state objects. Use metadata-only record updates for lifecycle or routing changes. Deltas, audits, failures, repaired attempts, and Runs remain separate descendants. DeepSci create, update, revise, list, and query operations use exact uppercase `DEEPSCI:WHAT` values through `--semantic-id`; lowercase, wrapped, bare, mixed-case, and aliased forms are invalid.

## Query and Material Boundaries

Query Kaoju state through `project artifacts latest|list|show` with exact semantic id and binding-defined scope. Query other neutral records with exact `--artifact-family`, `--semantic-id`, `--procedure`, and optional `--latest-only` filters. Explicit revision and supersession metadata determine latest candidates; competing active records produce ambiguity diagnostics. Directory scanning is not a fallback for semantic discovery. Profile-declared paths drive relationship, file, claim, metric, catalog, source, evidence, procedure, and terminal-status facets without family-specific backend code.

Repository trees, papers, datasets, model weights, checkpoints, raw outputs, and logs remain external or Topic Workspace-managed material. Structured records store immutable locators, revisions or digests, access and license posture, managed links, file refs, observed time, staleness policy, and provenance. A Topic Dataset Manifest indexes datasets; it does not contain them.
