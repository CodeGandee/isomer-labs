# Placeholder Bindings

This page binds the placeholders in `migrate/placeholders.md` to Isomer Topic Workspace storage operations. Keep the placeholders in workflow prose; use this page when a placeholder must become a durable record, structured payload, generated view, or queryable ref.

Use `isomer-cli ext research records` as the current transitional CRUD surface. Future native `project records ...` commands may replace these command shapes, but the placeholder tokens, producer, consumer, and profile metadata should remain stable.

When a Topic Actor creates or updates a record, add `--topic-actor <topic-actor-name>` and any known `--actor-kind`, `--runtime-kind`, `--controller-kind`, and `--adapter-ref` values. When a formal team agent creates or updates a record, include Agent Team Instance, Agent Instance, or Agent Workspace refs only when that formal context truly produced the record; do not fabricate those refs for Topic Actor work.

## Payload-first structured record flow

For structured rows, draft a JSON payload file, run `isomer-cli --print-json ext research records validate --topic <topic> --format-profile <format-profile-ref> --payload-file <payload-file>`, then create or update the record with `--payload-file <payload-file> --render markdown`. The generated Markdown view is review material; update the JSON payload and rerender rather than editing generated Markdown as the source of truth.

## Query-index metadata

When a structured payload has relationship facts, file outputs, or GUI facets, preserve them in the payload and pass explicit refs through `--relationships-json`, `--files-json`, and `--index-hints-json` when the producing skill knows them. Relationship metadata should name consumed, produced, routed, supported, superseded, summarized, or cited records; file metadata should name file role, semantic label, and source payload field or output pattern; facet metadata should leave ideas, route decisions, metrics, claims, artifact lists, and scalar facts in profile-backed payload sections so the query-index extractor can derive rows.

## Binding Rules

- Read `migrate/placeholders.md` first to understand the placeholder meaning, producer, consumer, and kind.
- Choose the binding row with the exact placeholder token; do not infer a nearby row by name similarity.
- Store exact placeholder, skill, producer, consumer, kind, format profile ref, payload file role, and generated view naming metadata on created records.
- Resolve generated view locations through the listed semantic label; do not invent hard-coded paths under the Topic Workspace.
- For paper-line polishing outputs, use paper-specific profiles such as `paper.prose-failure-diagnosis`, `paper.claim-boundary-check`, `paper.section-logic-rebuild`, `paper.draft.polished-manuscript-text`, and `paper.validation.manuscript-language` on existing generic semantic labels; do not add paper-specific top-level labels.
- Use `isomer-cli ext deepsci call ...` only for source-shaped compatibility behavior, then status the durable meaning through the binding row here.

## Kind Defaults

| Kind | Storage Item | Record Kind | Default Label | Profile Prefix | Note |
| --- | --- | --- | --- | --- | --- |
| decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision` | Record route choices, blockers, waivers, and closure decisions as Decision Records with linked evidence when available. |
| draft | Artifact with a draft profile | `artifact` | `topic.records.artifacts` | `draft` | Store drafts outside agent scratch once another skill may depend on them. |
| evidence | Evidence Item with an Artifact generated view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the generated Markdown view or source summary through the resolved topic records label. |
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store structured report payloads as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <PAPER_TYPE_DIAGNOSIS> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/paper-type-diagnosis/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-label topic.records.artifacts --placeholder '<PAPER_TYPE_DIAGNOSIS>' --format-profile isomer:deepsci/record-format/profile/decision/paper-type-diagnosis/v1 --skill isomer-deepsci-nature-polishing --producer 'isomer-deepsci-nature-polishing' --consumer 'nature-polishing' --payload-file <payload-file> --render markdown --content-name paper-type-diagnosis.md --metadata-json '{"paper_surface":"paper_type_diagnosis"}'` |
| <PROSE_FAILURE_DIAGNOSIS> | report | Prose failure diagnosis Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/paper/prose-failure-diagnosis/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<PROSE_FAILURE_DIAGNOSIS>' --format-profile isomer:deepsci/record-format/profile/paper/prose-failure-diagnosis/v1 --skill isomer-deepsci-nature-polishing --producer 'isomer-deepsci-nature-polishing' --consumer 'nature-polishing, write' --payload-file <payload-file> --render markdown --content-name prose-failure-diagnosis.md --metadata-json '{"paper_surface":"prose_failure_diagnosis"}'` |
| <CLAIM_BOUNDARY_CHECK> | evidence | Claim boundary Evidence Item | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/paper/claim-boundary-check/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-label topic.records.artifacts --placeholder '<CLAIM_BOUNDARY_CHECK>' --format-profile isomer:deepsci/record-format/profile/paper/claim-boundary-check/v1 --skill isomer-deepsci-nature-polishing --producer 'isomer-deepsci-nature-polishing' --consumer 'nature-polishing, write, review' --payload-file <payload-file> --render markdown --content-name claim-boundary-check.md --metadata-json '{"paper_surface":"claim_boundary_check"}'` |
| <SECTION_LOGIC_REBUILD> | draft | Section logic rebuild Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/paper/section-logic-rebuild/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<SECTION_LOGIC_REBUILD>' --format-profile isomer:deepsci/record-format/profile/paper/section-logic-rebuild/v1 --skill isomer-deepsci-nature-polishing --producer 'isomer-deepsci-nature-polishing' --consumer 'nature-polishing, write' --payload-file <payload-file> --render markdown --content-name section-logic-rebuild.md --metadata-json '{"paper_surface":"section_logic_rebuild"}'` |
| <POLISHED_MANUSCRIPT_TEXT> | draft | Polished manuscript text Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/paper/draft/polished-manuscript-text/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<POLISHED_MANUSCRIPT_TEXT>' --format-profile isomer:deepsci/record-format/profile/paper/draft/polished-manuscript-text/v1 --skill isomer-deepsci-nature-polishing --producer 'isomer-deepsci-nature-polishing' --consumer 'write, user' --payload-file <payload-file> --render markdown --content-name polished-manuscript-text.md --metadata-json '{"paper_surface":"polished_manuscript_text"}'` |
| <POLISHING_STYLE_QA> | report | Manuscript language validation View Manifest | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/paper/validation/manuscript-language/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-label topic.records.views --placeholder '<POLISHING_STYLE_QA>' --format-profile isomer:deepsci/record-format/profile/paper/validation/manuscript-language/v1 --skill isomer-deepsci-nature-polishing --producer 'isomer-deepsci-nature-polishing' --consumer 'nature-polishing, write' --payload-file <payload-file> --render markdown --content-name polishing-style-qa.md --metadata-json '{"paper_surface":"polishing_style_qa"}'` |
| <POLISHING_EVIDENCE_BLOCKER> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/polishing-evidence-blocker/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-label topic.records.artifacts --placeholder '<POLISHING_EVIDENCE_BLOCKER>' --format-profile isomer:deepsci/record-format/profile/decision/polishing-evidence-blocker/v1 --skill isomer-deepsci-nature-polishing --producer 'isomer-deepsci-nature-polishing' --consumer 'user, write, decision' --payload-file <payload-file> --render markdown --content-name polishing-evidence-blocker.md --metadata-json '{"paper_surface":"polishing_evidence_blocker"}'` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-payload --include-rendered-body` to inspect one stored record, payload, and generated view when the body is text.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --payload-file <payload-file> --render markdown` when the same semantic record receives a revised payload or status.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves generated view files by default.
