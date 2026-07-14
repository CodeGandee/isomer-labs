# Artifact Storage Layout

Status: Accepted
Date: 2026-07-14

## Question

Where should intermediate survey Artifacts such as direction sets, reading lists, Findings, source digests, claim-evidence ledgers, audits, and synthesis records be stored inside a Topic Workspace?

## Decision

Accepted durable survey content uses a generic record-owned canonical layout under the semantic surface selected by the Kaoju binding registry, normally `topic.records.artifacts`. Under `isomer-default.v1`, that surface resolves to `<topic-workspace>/records/artifacts`, but callers treat the semantic label rather than that physical path as the contract.

The artifact service allocates internal managed paths from record kind and opaque record or revision identity. The first implementation may reuse the current `research-records/<record-kind>/<record-id>/` shape, but this shape remains private to the service. Skills, schemas, binding entries, and user workflows do not construct, parse, or depend on those subpaths.

Structured records use validated JSON as authoritative content. Ordinary files remain authoritative for MyST, Markdown, TeX, PDFs, scripts, logs, and downloaded material. Directory Artifacts use a checksummed manifest. Canonical external repositories remain in their repository surfaces and are referenced by registered identity rather than copied into the records root.

Workspace Runtime stores the Artifact Core Record, semantic id, scope, status, current-candidate posture, lineage, provenance, checksum, and content locator. Agents discover survey state through DB-backed artifact queries. They do not scan or infer meaning from the generic directory layout.

Human-readable or workflow-organized representations are derived views. They may be rendered on demand, registered under `topic.records.views`, or explicitly exported or projected to a worker-visible surface. A derived view never becomes canonical structured state merely because its path is easier to browse.

Pre-acceptance notes and generated files follow the resolved worker-output or Local Tmp Surface policy. Promotion validates and stages the accepted content, moves or copies it into service-owned storage, and registers it in Workspace Runtime. Temporary files and working copies are not durable Artifacts.

## Illustrative Default Layout

The following tree explains the current implementation shape but does not establish a public subpath API:

```text
<topic-workspace>/
├── state.sqlite
├── records/
│   ├── artifacts/
│   │   └── research-records/
│   │       └── <record-kind>/
│   │           └── <record-id>/
│   │               ├── payload.json
│   │               └── manifest.json
│   ├── tasks/
│   ├── runs/
│   ├── views/
│   └── logs/
├── repos/
│   └── extern/
└── tmp/
```

## Consequences

- Semantic organization lives in the binding registry and Workspace Runtime indexes rather than duplicated directory names.
- Revisions can receive new opaque storage identities while the DB advances the scoped current candidate and retains prior history.
- Internal storage can migrate without changing skill instructions or public CLI contracts, provided registered locators remain valid or receive an explicit migration.
- Manual filesystem browsing is less informative. CLI queries and derived views provide the supported inspection experience.

## Rejected Alternatives

- A canonical Kaoju hierarchy such as `kaoju/<semantic-id>/<scope>/<revision>/` was rejected because it duplicates semantic state in paths and raises the cost of renaming, rescoping, and migration.
- Per-binding subdirectory conventions were rejected because they would make physical layout another distributed binding authority and create inconsistent storage behavior across skills.
