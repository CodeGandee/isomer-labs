# Placeholder Bindings

This page binds the placeholders in `migrate/placeholders.md` to Isomer Topic Workspace storage operations. Keep the placeholders in workflow prose; use this page when a placeholder must become a durable record, structured payload-file record or queryable ref.

Use `isomer-cli ext research records` as the current transitional CRUD surface. Future native `project records ...` commands may replace these command shapes, but the placeholder tokens, producer, consumer, and profile metadata should remain stable.

When a Topic Actor creates or updates a record, add `--topic-actor <topic-actor-name>` and any known `--actor-kind`, `--runtime-kind`, `--controller-kind`, and `--adapter-ref` values. When a formal team agent creates or updates a record, include Agent Team Instance, Agent Instance, or Agent Workspace refs only when that formal context truly produced the record; do not fabricate those refs for Topic Actor work.

## Payload-first structured record flow

For structured rows, draft a JSON payload file, run `isomer-cli --print-json ext research records validate --topic <topic> --format-profile <format-profile-ref> --payload-file <payload-file>`, then create or update the record with `--payload-file <payload-file>`. Workspace Runtime snapshots the accepted payload into managed JSON file storage. Render Markdown on demand for human review; update the JSON payload rather than editing rendered Markdown as the source of truth.

Every structured payload file must include non-empty top-level `title` and `summary` strings. If the payload contains idea-bearing entries that can become canonical Research Ideas, each accepted idea object must include its own non-empty `title` and `summary`; labels, candidate ids, and aliases may be present but do not replace those display fields.

## Canonical lineage metadata

When a durable record is produced from prior durable records, pass immediate parents through `--parents-json`, choose `--lineage-kind`, and add `--generation-id` plus `--generation-purpose` for sibling candidate passes. Use `revision_of` only through `ext research records revise <record-id>` when accepted content changes; use `--relationships-json`, `--files-json`, and `--index-hints-json` only for non-lineage query metadata.

## Query-index metadata

When a structured payload has relationship facts, file outputs, or GUI facets, preserve them in the payload and pass explicit refs through `--relationships-json`, `--files-json`, and `--index-hints-json` when the producing skill knows them. Relationship metadata should name evidence, citations, file materialization, support links, summaries, routes, or other non-canonical refs; file metadata should name file role, semantic label, and source payload field or output pattern; facet metadata should leave ideas, route decisions, metrics, claims, artifact lists, and scalar facts in profile-backed payload sections so the query-index extractor can derive rows.

## Binding Rules

- Read `migrate/placeholders.md` first to understand the placeholder meaning, producer, consumer, and kind.
- Choose the binding row with the exact placeholder token; do not infer a nearby row by name similarity.
- Store exact placeholder, skill, producer, consumer, kind, format profile ref, payload file role, and payload file and optional export metadata on created records.
- Render Markdown on demand with `isomer-cli --print-json ext research records render <record-id> --topic <topic>`; add `--output-file <path>` only for an explicit Markdown export.
- For paper-line outputs, use paper-specific profiles such as `rebuttal.reviewer-item-matrix`, `rebuttal.action-plan`, `rebuttal.reviewer-linked-evidence-todo`, `rebuttal.response-letter`, and `package.paper.revision-handoff-bundle` on existing generic semantic labels; do not add paper-specific top-level labels.
- Use `isomer-cli ext deepsci call ...` only for source-shaped compatibility behavior, then status the durable meaning through the binding row here.

## Kind Defaults

| Kind | Storage Item | Record Kind | Default Label | Profile Prefix | Note |
| --- | --- | --- | --- | --- | --- |
| decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision` | Record route choices, blockers, waivers, and closure decisions as Decision Records with linked evidence when available. |
| draft | Artifact with a draft profile | `artifact` | `topic.records.artifacts` | `draft` | Store drafts outside agent scratch once another skill may depend on them. |
| evidence | Evidence Item with an Artifact on-demand view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the on-demand Markdown view or source summary through the resolved topic records label. |
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |
| research task | Research Task for resumable paper-writing work | `research_task` | `topic.records.tasks` | `rebuttal` | Use this when a reviewer-linked TODO must be resumed, assigned, or queried as work. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| DEEPSCI:REVIEW-PACKAGE-NORMALIZATION | evidence | Review package normalization Evidence Item | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/rebuttal/review-package-normalization/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-label topic.records.artifacts --semantic-id 'DEEPSCI:REVIEW-PACKAGE-NORMALIZATION' --format-profile isomer:deepsci/record-format/profile/rebuttal/review-package-normalization/v2 --skill isomer-deepsci-rebuttal --producer 'isomer-deepsci-rebuttal' --consumer 'rebuttal' --payload-file <payload-file> --metadata-json '{"paper_surface":"review_package_normalization"}'` |
| DEEPSCI:REVIEWER-ITEM-MATRIX | handoff | Reviewer item matrix Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/rebuttal/reviewer-item-matrix/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --semantic-id 'DEEPSCI:REVIEWER-ITEM-MATRIX' --format-profile isomer:deepsci/record-format/profile/rebuttal/reviewer-item-matrix/v2 --skill isomer-deepsci-rebuttal --producer 'isomer-deepsci-rebuttal' --consumer 'rebuttal, analysis, write' --payload-file <payload-file> --metadata-json '{"paper_surface":"reviewer_item_matrix"}'` |
| DEEPSCI:REBUTTAL-ACTION-PLAN | handoff | Rebuttal action-plan Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/rebuttal/action-plan/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --semantic-id 'DEEPSCI:REBUTTAL-ACTION-PLAN' --format-profile isomer:deepsci/record-format/profile/rebuttal/action-plan/v2 --skill isomer-deepsci-rebuttal --producer 'isomer-deepsci-rebuttal' --consumer 'analysis, write, scout, baseline' --payload-file <payload-file> --metadata-json '{"paper_surface":"rebuttal_action_plan"}'` |
| DEEPSCI:REVIEWER-LINKED-EVIDENCE-TODO | research task | Research Task for reviewer-linked evidence work | `research_task` | `topic.records.tasks` | `isomer:deepsci/record-format/profile/rebuttal/reviewer-linked-evidence-todo/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind research_task --semantic-label topic.records.tasks --semantic-id 'DEEPSCI:REVIEWER-LINKED-EVIDENCE-TODO' --format-profile isomer:deepsci/record-format/profile/rebuttal/reviewer-linked-evidence-todo/v2 --skill isomer-deepsci-rebuttal --producer 'isomer-deepsci-rebuttal' --consumer 'analysis, experiment, decision' --payload-file <payload-file> --metadata-json '{"paper_surface":"reviewer_linked_evidence_todo"}'` |
| DEEPSCI:REBUTTAL-EVIDENCE-UPDATE | evidence | Rebuttal Evidence Item update | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/rebuttal/evidence-update/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-label topic.records.artifacts --semantic-id 'DEEPSCI:REBUTTAL-EVIDENCE-UPDATE' --format-profile isomer:deepsci/record-format/profile/rebuttal/evidence-update/v2 --skill isomer-deepsci-rebuttal --producer 'isomer-deepsci-rebuttal and routed skills' --consumer 'rebuttal, write, finalize' --payload-file <payload-file> --metadata-json '{"paper_surface":"rebuttal_evidence_update"}'` |
| DEEPSCI:MANUSCRIPT-TEXT-DELTA | draft | Manuscript text-delta Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/rebuttal/text-deltas/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --semantic-id 'DEEPSCI:MANUSCRIPT-TEXT-DELTA' --format-profile isomer:deepsci/record-format/profile/rebuttal/text-deltas/v2 --skill isomer-deepsci-rebuttal --producer 'isomer-deepsci-write or rebuttal' --consumer 'rebuttal, finalize' --payload-file <payload-file> --metadata-json '{"paper_surface":"manuscript_text_delta"}'` |
| DEEPSCI:RESPONSE-LETTER-DRAFT | draft | Response letter Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/rebuttal/response-letter/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --semantic-id 'DEEPSCI:RESPONSE-LETTER-DRAFT' --format-profile isomer:deepsci/record-format/profile/rebuttal/response-letter/v2 --skill isomer-deepsci-rebuttal --producer 'isomer-deepsci-rebuttal' --consumer 'user, finalize' --payload-file <payload-file> --metadata-json '{"paper_surface":"response_letter_draft"}'` |
| DEEPSCI:REVISION-HANDOFF-BUNDLE | handoff | Revision handoff bundle Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/package/paper/revision-handoff-bundle/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --semantic-id 'DEEPSCI:REVISION-HANDOFF-BUNDLE' --format-profile isomer:deepsci/record-format/profile/package/paper/revision-handoff-bundle/v2 --skill isomer-deepsci-rebuttal --producer 'isomer-deepsci-rebuttal' --consumer 'finalize, user' --payload-file <payload-file> --metadata-json '{"paper_surface":"revision_handoff_bundle"}'` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --semantic-id 'DEEPSCI:WHAT'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-payload` to inspect one stored record, payload, and metadata.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --semantic-id 'DEEPSCI:WHAT' --payload-file <payload-file>` for status, metadata, or repair updates. Use `isomer-cli --print-json ext research records revise <record-id> --topic <topic> --payload-file <payload-file>` when accepted content changes and must remain visible as a new descendant revision.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves managed payload files by default.
