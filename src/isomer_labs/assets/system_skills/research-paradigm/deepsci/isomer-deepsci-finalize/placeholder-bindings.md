# Placeholder Bindings

This page binds the placeholders in `migrate/placeholders.md` to Isomer Topic Workspace storage operations. Keep the placeholders in workflow prose; use this page when a placeholder must become a durable record, structured payload, generated view, or queryable ref.

Use `isomer-cli ext research records` as the current transitional CRUD surface. Future native `project records ...` commands may replace these command shapes, but the placeholder tokens, producer, consumer, and profile metadata should remain stable.

When a Topic Actor creates or updates a record, add `--topic-actor <topic-actor-name>` and any known `--actor-kind`, `--runtime-kind`, `--controller-kind`, and `--adapter-ref` values. When a formal team agent creates or updates a record, include Agent Team Instance, Agent Instance, or Agent Workspace refs only when that formal context truly produced the record; do not fabricate those refs for Topic Actor work.

## Payload-first structured record flow

For structured rows, draft a JSON payload file, run `isomer-cli --print-json ext research records validate --topic <topic> --format-profile <format-profile-ref> --payload-file <payload-file>`, then create or update the record with `--payload-file <payload-file> --render markdown`. The generated Markdown view is review material; update the JSON payload and rerender rather than editing generated Markdown as the source of truth.

## Binding Rules

- Read `migrate/placeholders.md` first to understand the placeholder meaning, producer, consumer, and kind.
- Choose the binding row with the exact placeholder token; do not infer a nearby row by name similarity.
- Store exact placeholder, skill, producer, consumer, kind, format profile ref, payload file role, and generated view naming metadata on created records.
- Resolve generated view locations through the listed semantic label; do not invent hard-coded paths under the Topic Workspace.
- For paper-line outputs, use paper-specific profiles such as `paper.finalize-context`, `paper.claim-ledger`, `paper.final-summary`, `package.paper.resume-packet`, and `paper.finalize-continuity` on existing generic semantic labels; do not add paper-specific top-level labels.
- Use `isomer-cli ext deepsci call ...` only for source-shaped compatibility behavior, then status the durable meaning through the binding row here.

## Kind Defaults

| Kind | Storage Item | Record Kind | Default Label | Profile Prefix | Note |
| --- | --- | --- | --- | --- | --- |
| decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision` | Record route choices, blockers, waivers, and closure decisions as Decision Records with linked evidence when available. |
| evidence | Evidence Item with an Artifact generated view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the generated Markdown view or source summary through the resolved topic records label. |
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store structured report payloads as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |
| runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control` | Use this for boards, checklists, route cursors, continuity notes, and other resumable control surfaces. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <FINALIZE_CONTEXT_BRIEF> | evidence | Finalize context View Manifest | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/paper/finalize-context/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-label topic.records.views --placeholder '<FINALIZE_CONTEXT_BRIEF>' --format-profile isomer:deepsci/record-format/profile/paper/finalize-context/v1 --skill isomer-deepsci-finalize --producer 'isomer-deepsci-finalize' --consumer 'closure gate' --payload-file <payload-file> --render markdown --content-name finalize-context.md --metadata-json '{"paper_surface":"finalize_context"}'` |
| <CLAIM_LEDGER> | report | Claim ledger Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/paper/claim-ledger/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<CLAIM_LEDGER>' --format-profile isomer:deepsci/record-format/profile/paper/claim-ledger/v1 --skill isomer-deepsci-finalize --producer 'isomer-deepsci-finalize' --consumer 'final summary, writing, archive' --payload-file <payload-file> --render markdown --content-name claim-ledger.md --metadata-json '{"paper_surface":"claim_ledger"}'` |
| <FINAL_LIMITATIONS_REPORT> | report | Final limitations Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/paper/final-limitations-report/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<FINAL_LIMITATIONS_REPORT>' --format-profile isomer:deepsci/record-format/profile/paper/final-limitations-report/v1 --skill isomer-deepsci-finalize --producer 'isomer-deepsci-finalize' --consumer 'final summary and user' --payload-file <payload-file> --render markdown --content-name final-limitations-report.md --metadata-json '{"paper_surface":"final_limitations"}'` |
| <FINAL_SUMMARY> | report | Final summary Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/paper/final-summary/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<FINAL_SUMMARY>' --format-profile isomer:deepsci/record-format/profile/paper/final-summary/v1 --skill isomer-deepsci-finalize --producer 'isomer-deepsci-finalize' --consumer 'user and future work' --payload-file <payload-file> --render markdown --content-name final-summary.md --metadata-json '{"paper_surface":"final_summary"}'` |
| <RESUME_PACKET> | handoff | Resume packet package Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/package/paper/resume-packet/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<RESUME_PACKET>' --format-profile isomer:deepsci/record-format/profile/package/paper/resume-packet/v1 --skill isomer-deepsci-finalize --producer 'isomer-deepsci-finalize' --consumer 'future work' --payload-file <payload-file> --render markdown --content-name resume-packet.md --metadata-json '{"paper_surface":"resume_packet"}'` |
| <CLOSURE_DECISION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/closure-decision/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-label topic.records.artifacts --placeholder '<CLOSURE_DECISION>' --format-profile isomer:deepsci/record-format/profile/decision/closure-decision/v1 --skill isomer-deepsci-finalize --producer 'isomer-deepsci-finalize or decision' --consumer 'user and future work' --payload-file <payload-file> --render markdown --content-name closure-decision.md --metadata-json '{"paper_surface":"closure_decision"}'` |
| <FINALIZE_BLOCKER_RECORD> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/finalize-blocker-record/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-label topic.records.artifacts --placeholder '<FINALIZE_BLOCKER_RECORD>' --format-profile isomer:deepsci/record-format/profile/decision/finalize-blocker-record/v1 --skill isomer-deepsci-finalize --producer 'isomer-deepsci-finalize' --consumer 'decision or upstream skill' --payload-file <payload-file> --render markdown --content-name finalize-blocker-record.md --metadata-json '{"paper_surface":"finalize_blocker"}'` |
| <FINALIZE_CONTINUITY_UPDATE> | runtime state | Finalize continuity View Manifest | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/paper/finalize-continuity/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-label topic.records.views --placeholder '<FINALIZE_CONTINUITY_UPDATE>' --format-profile isomer:deepsci/record-format/profile/paper/finalize-continuity/v1 --skill isomer-deepsci-finalize --producer 'isomer-deepsci-finalize' --consumer 'future work' --payload-file <payload-file> --render markdown --content-name finalize-continuity.md --metadata-json '{"paper_surface":"finalize_continuity"}'` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-payload --include-rendered-body` to inspect one stored record, payload, and generated view when the body is text.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --payload-file <payload-file> --render markdown` when the same semantic record receives a revised payload or status.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves generated view files by default.
