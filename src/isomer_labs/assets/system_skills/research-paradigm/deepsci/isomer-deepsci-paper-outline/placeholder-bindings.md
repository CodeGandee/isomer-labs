# Placeholder Bindings

This page binds the placeholders in `migrate/placeholders.md` to Isomer Topic Workspace storage operations. Keep the placeholders in workflow prose; use this page when a placeholder must become a durable record, structured payload-file record or queryable ref.

Use `isomer-cli ext research records` as the current transitional CRUD surface. Future native `project records ...` commands may replace these command shapes, but the placeholder tokens, producer, consumer, and profile metadata should remain stable.

When a Topic Actor creates or updates a record, add `--topic-actor <topic-actor-name>` and any known `--actor-kind`, `--runtime-kind`, `--controller-kind`, and `--adapter-ref` values. When a formal team agent creates or updates a record, include Agent Team Instance, Agent Instance, or Agent Workspace refs only when that formal context truly produced the record; do not fabricate those refs for Topic Actor work.

## Payload-first structured record flow

For structured rows, draft a JSON payload file, run `isomer-cli --print-json ext research records validate --topic <topic> --format-profile <format-profile-ref> --payload-file <payload-file>`, then create or update the record with `--payload-file <payload-file>`. Workspace Runtime snapshots the accepted payload into managed JSON file storage. Render Markdown on demand for human review; update the JSON payload rather than editing rendered Markdown as the source of truth.

## Query-index metadata

When a structured payload has relationship facts, file outputs, or GUI facets, preserve them in the payload and pass explicit refs through `--relationships-json`, `--files-json`, and `--index-hints-json` when the producing skill knows them. Relationship metadata should name consumed, produced, routed, supported, superseded, summarized, or cited records; file metadata should name file role, semantic label, and source payload field or output pattern; facet metadata should leave ideas, route decisions, metrics, claims, artifact lists, and scalar facts in profile-backed payload sections so the query-index extractor can derive rows.

## Binding Rules

- Read `migrate/placeholders.md` first to understand the placeholder meaning, producer, consumer, and kind.
- Choose the binding row with the exact placeholder token; do not infer a nearby row by name similarity.
- Store exact placeholder, skill, producer, consumer, kind, format profile ref, payload file role, and payload file and optional export metadata on created records.
- Render Markdown on demand with `isomer-cli --print-json ext research records render <record-id> --topic <topic>`; add `--output-file <path>` only for an explicit Markdown export.
- For paper-line outputs, use paper-specific profiles such as `paper.line-state`, `paper.outline.idea`, `paper.claim-evidence-map`, `paper.contract.evidence-view`, `paper.validation.academic-outline`, and `paper.writing-plan` on existing generic semantic labels; do not add paper-specific top-level labels.
- Use `isomer-cli ext deepsci call ...` only for source-shaped compatibility behavior, then status the durable meaning through the binding row here.

## Kind Defaults

| Kind | Storage Item | Record Kind | Default Label | Profile Prefix | Note |
| --- | --- | --- | --- | --- | --- |
| decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision` | Record route choices, blockers, waivers, and closure decisions as Decision Records with linked evidence when available. |
| draft | Artifact with a draft profile | `artifact` | `topic.records.artifacts` | `draft` | Store drafts outside agent scratch once another skill may depend on them. |
| evidence | Evidence Item with an Artifact on-demand view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the on-demand Markdown view or source summary through the resolved topic records label. |
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store structured report payloads as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |
| research task | Research Task for resumable paper-writing work | `research_task` | `topic.records.tasks` | `paper` | Use this when a writing plan or reviewer-facing TODO must be resumed, assigned, or queried as work. |
| runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control` | Use this for boards, checklists, route cursors, continuity notes, and other resumable control surfaces. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <PAPER_STATE_SNAPSHOT> | runtime state | View Manifest for active paper-line state | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/paper/line-state/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-label topic.records.views --placeholder '<PAPER_STATE_SNAPSHOT>' --format-profile isomer:deepsci/record-format/profile/paper/line-state/v1 --skill isomer-deepsci-paper-outline --producer 'isomer-deepsci-paper-outline' --consumer 'paper-outline, write' --payload-file <payload-file> --metadata-json '{"paper_surface":"state_snapshot"}'` |
| <ONE_SENTENCE_PAPER_IDEA> | draft | Paper outline Artifact on-demand view | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/paper/outline/idea/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<ONE_SENTENCE_PAPER_IDEA>' --format-profile isomer:deepsci/record-format/profile/paper/outline/idea/v1 --skill isomer-deepsci-paper-outline --producer 'isomer-deepsci-paper-outline' --consumer 'paper-outline, write, review' --payload-file <payload-file> --metadata-json '{"paper_surface":"outline_idea"}'` |
| <CLAIM_EVIDENCE_BOUNDARY> | evidence | Claim-evidence map View Manifest | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/paper/claim-evidence-map/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-label topic.records.views --placeholder '<CLAIM_EVIDENCE_BOUNDARY>' --format-profile isomer:deepsci/record-format/profile/paper/claim-evidence-map/v1 --skill isomer-deepsci-paper-outline --producer 'isomer-deepsci-paper-outline' --consumer 'write, review, rebuttal' --payload-file <payload-file> --metadata-json '{"paper_surface":"claim_evidence_boundary"}'` |
| <PAPER_VIEW> | handoff | Paper-view Artifact on-demand view for the selected outline contract | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/paper/outline/paper-view/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<PAPER_VIEW>' --format-profile isomer:deepsci/record-format/profile/paper/outline/paper-view/v1 --skill isomer-deepsci-paper-outline --producer 'isomer-deepsci-paper-outline' --consumer 'write, review' --payload-file <payload-file> --metadata-json '{"paper_surface":"paper_view"}'` |
| <EVIDENCE_VIEW> | evidence | Evidence-view View Manifest for the selected outline contract | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/paper/contract/evidence-view/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-label topic.records.views --placeholder '<EVIDENCE_VIEW>' --format-profile isomer:deepsci/record-format/profile/paper/contract/evidence-view/v1 --skill isomer-deepsci-paper-outline --producer 'isomer-deepsci-paper-outline' --consumer 'write, review, finalize' --payload-file <payload-file> --metadata-json '{"paper_surface":"evidence_view"}'` |
| <OUTLINE_VALIDATION_REPORT> | report | Academic outline validation View Manifest | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/paper/validation/academic-outline/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-label topic.records.views --placeholder '<OUTLINE_VALIDATION_REPORT>' --format-profile isomer:deepsci/record-format/profile/paper/validation/academic-outline/v1 --skill isomer-deepsci-paper-outline --producer 'isomer-deepsci-paper-outline' --consumer 'paper-outline, write, decision' --payload-file <payload-file> --metadata-json '{"paper_surface":"outline_validation"}'` |
| <SECTION_WRITING_PLAN> | research task | Research Task for section-level writing jobs | `research_task` | `topic.records.tasks` | `isomer:deepsci/record-format/profile/paper/writing-plan/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind research_task --semantic-label topic.records.tasks --placeholder '<SECTION_WRITING_PLAN>' --format-profile isomer:deepsci/record-format/profile/paper/writing-plan/v1 --skill isomer-deepsci-paper-outline --producer 'isomer-deepsci-paper-outline' --consumer 'write' --payload-file <payload-file> --metadata-json '{"paper_surface":"writing_plan"}'` |
| <PAPER_OUTLINE_ROUTE_DECISION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/paper-outline-route-decision/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-label topic.records.artifacts --placeholder '<PAPER_OUTLINE_ROUTE_DECISION>' --format-profile isomer:deepsci/record-format/profile/decision/paper-outline-route-decision/v1 --skill isomer-deepsci-paper-outline --producer 'isomer-deepsci-paper-outline' --consumer 'analysis, decision, write' --payload-file <payload-file> --metadata-json '{"paper_surface":"outline_route_decision"}'` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-payload` to inspect one stored record, payload, and metadata.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --payload-file <payload-file>` when the same semantic record receives a revised payload or status.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves managed payload files by default.
