## Why

The Flash Attention sample Topic Workspace has enough record-level history for an idea iteration GUI demo, but its idea metadata still looks like an older run: raw idea rows are duplicated, serious candidates are not normalized, generation groups are missing, and one query-index record warning remains. We need this topic to behave like data produced by the latest `isomer-cli` and DeepSci skills so new agents and the GUI can use it as a trustworthy fixture.

## What Changes

- Repair `isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model` data in place using current `isomer-cli` write/maintenance paths where possible.
- Add or revise structured records so raw ideas, serious candidates, selected hypotheses, follow-up hypotheses, experiment results, analysis summaries, and route decisions expose enough typed metadata for the topic idea iteration map.
- Add canonical lineage generation groups for sibling alternatives and candidate sets instead of leaving branching to filename or Markdown inference.
- Fill missing relationship metadata needed by the GUI: predecessor/successor links, selected-from links, rejected/deferred alternatives, evidence basis, route rationale, and status hints.
- Rebuild or refresh query-index rows explicitly after data repair and remove integrity warnings that would confuse a fresh agent session.
- Do not change generic GUI behavior, CLI schemas, or DeepSci skills in this change; this is a targeted topic data repair.

## Capabilities

### New Capabilities
- `topic-idea-iteration-fixture-data`: Defines the integrity and metadata expectations for a repaired sample Topic Workspace that supports the topic idea iteration map without topic-specific GUI code.

### Modified Capabilities
- `research-record-query-index`: Clarifies that repaired fixture data must validate through existing query-index and lineage validation APIs with no read-time repair.
- `workspace-runtime-persistence`: Clarifies that topic-local Workspace Runtime fixture repairs must use canonical runtime tables and leave no missing record, stale index, or lineage integrity diagnostics.

## Impact

- Affected data: `isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model/state.sqlite` and any topic-owned structured payload files needed to make the data self-describing.
- Affected validation commands: `isomer-cli ext research records lineage validate`, `isomer-cli ext research records query export --view ideas`, query-index validation/rebuild commands, and representative lineage/facet queries.
- Affected consumers: Project Web GUI idea iteration map, project operator sessions, and new agents reading the topic with current Isomer CLI/system skills.
