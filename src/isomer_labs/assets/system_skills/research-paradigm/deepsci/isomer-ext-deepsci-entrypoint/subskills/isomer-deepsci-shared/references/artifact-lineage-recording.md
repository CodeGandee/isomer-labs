# Artifact Lineage Recording

Use canonical artifact lineage when a durable record is produced from prior durable records. Pass parent records with `--parents-json`, choose one lineage kind with `--lineage-kind`, and use `--generation-id` plus `--generation-purpose` when sibling candidates are created from the same parent set.

Use these lineage kinds:

- `derived_from`: the child is produced from parent content, evidence, board state, or a prior artifact.
- `revision_of`: the child is the next content version of the same semantic artifact; use `ext research records revise <record-id>` for accepted content changes.
- `selected_from`: the child is selected from one or more candidate parents.
- `merged_from`: the child combines multiple parent records.
- `follow_up_to`: the child continues a prior result, decision, question, or route.

Siblings are not pairwise edges. When one pass produces alternative candidates, give all children the same generation group and parent set, for example `--generation-id idea-pass-20260706-01 --generation-purpose "candidate frontier from current board and survey"`.

Keep canonical lineage separate from query-index hints. Use `--relationships-json`, `--files-json`, and `--index-hints-json` for citations, evidence links, file outputs, GUI facets, and non-lineage relationships.

Before writing a durable record, identify its immediate durable parents from current Workspace Runtime records. If the parent is unknown, record a blocker or omit lineage with a clear diagnostic note; do not infer authoritative parents from generated Markdown prose.
