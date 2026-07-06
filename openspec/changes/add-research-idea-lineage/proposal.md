## Why

The current idea-lineage GUI must infer user-facing idea connections from record-level lineage and extracted record facets, so top-level ideas appear disconnected or mixed with route decisions, claims, and other details. Research topics need a canonical concept for durable ideas and their relationships so users can inspect how primary ideas branch, merge, revise, and lead to later hypotheses.

## What Changes

- Introduce canonical Research Idea concepts, including Primary Idea visibility, Idea Realization links to records, Idea Lineage Edge DAG relationships, and idea generation groups.
- Add Workspace Runtime persistence and validation for research ideas, idea realizations, idea lineage edges, and idea generation groups.
- Add `isomer-cli ext research ideas` commands for creating, realizing, linking, querying, validating, importing, and repairing idea-lineage data.
- Update research record write/read behavior so idea-bearing records can explicitly declare which Research Ideas they realize without overloading record lineage.
- Update query-index and graph-read behavior so the idea-lineage GUI prefers canonical idea DAG data and treats extracted record idea rows as fallback facets.
- Update DeepSci system skills so agents record idea identity and idea lineage when producing raw slates, candidate frontiers, pre-idea drafts, selected hypotheses, analysis follow-ups, experiment-driven idea updates, and route decisions.
- Hand-repair the `flash-attention-4-whitebox-runtime-model` topic workspace so its existing records expose a best-effort canonical primary-idea DAG and pass new integrity validation.

## Capabilities

### New Capabilities

- `research-idea-lineage`: Canonical Research Idea identity, realization, lineage, generation-group, query, validation, and GUI read-model behavior.

### Modified Capabilities

- `research-lifecycle-state`: Add Research Idea, Primary Idea, Idea Realization, and Idea Lineage Edge to the platform domain language.
- `workspace-runtime-persistence`: Persist and validate canonical idea-lineage tables in the Topic Workspace runtime database.
- `research-recording-contracts`: Let structured research records declare idea realizations and idea parentage separately from record lineage.
- `research-record-query-index`: Export canonical idea DAG data for query and graph views while preserving extracted idea facets as fallback metadata.
- `research-paradigm-skills`: Teach DeepSci skills to record idea identity, primary visibility, sibling candidate groups, and idea-level lineage during research workflows.

## Impact

- Affected code includes `src/isomer_labs/runtime`, `src/isomer_labs/records`, `src/isomer_labs/cli/commands`, `src/isomer_labs/web`, and the TypeScript project web GUI.
- Affected assets include `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md` and DeepSci system skills under `src/isomer_labs/assets/system_skills/research-paradigm/deepsci/`.
- Affected topic data includes `isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model/state.sqlite` and its structured research-record payloads where repair metadata is needed.
- Existing record lineage remains supported and keeps artifact provenance semantics; idea lineage is additive and should not break existing record queries.
