---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Placeholder Bindings

This page binds the placeholders in `migrate/placeholders.md` to Isomer Topic Workspace storage operations. Keep the placeholders in workflow prose; use this page when a placeholder must become a durable record, structured payload-file record or queryable ref.

Use `isomer-cli ext research records` as the current transitional CRUD surface. Future native `project records ...` commands may replace these command shapes, but the placeholder tokens, producer, consumer, and profile metadata should remain stable.

When a Topic Actor creates or updates a record, add `--topic-actor <topic-actor-name>` and any known `--actor-kind`, `--runtime-kind`, `--controller-kind`, and `--adapter-ref` values. When a formal team agent creates or updates a record, include Agent Team Instance, Agent Instance, or Agent Workspace refs only when that formal context truly produced the record; do not fabricate those refs for Topic Actor work.

## Payload-first structured record flow

For structured rows, draft a JSON payload file, run `isomer-cli --print-json ext research records validate --topic <topic> --format-profile <format-profile-ref> --payload-file <payload-file>`, then create or update the record with `--payload-file <payload-file>`. Workspace Runtime snapshots the accepted payload into managed JSON file storage. Render Markdown on demand for human review; update the JSON payload rather than editing rendered Markdown as the source of truth.

Every structured payload file must include non-empty top-level `title` and `summary` strings. If the payload contains idea-bearing entries that can become canonical Research Ideas, each accepted idea object must include its own non-empty `title` and `summary`; labels, candidate ids, and aliases may be present but do not replace those display fields.

## Canonical lineage metadata

When a durable record is produced from prior durable records, pass immediate parents through `--parents-json`, choose `--lineage-kind`, and add `--generation-id` plus `--generation-purpose` for sibling candidate passes. Use `revision_of` only through `ext research records revise <record-id>` when accepted content changes; use `--relationships-json`, `--files-json`, and `--index-hints-json` only for non-lineage query metadata.

## Canonical idea metadata

Invoke `isomer-op-entrypoint->research-ideas` when accepted experiment output changes exploration or evidence assessment or creates a follow-up concept. Record explicit transitions with terminal Evidence Item, Artifact, Finding, Research Task, or Run refs and leave decision state unchanged without a separate decision. Use one exact idea object passed through `--source-json-path` for realization, never the result root, metrics, artifact list, notes, or rendered Markdown.

## Query-index metadata

When a structured payload has relationship facts, file outputs, or GUI facets, preserve them in the payload and pass explicit refs through `--relationships-json`, `--files-json`, and `--index-hints-json` when the producing skill knows them. Relationship metadata should name evidence, citations, file materialization, support links, summaries, routes, or other non-canonical refs; file metadata should name file role, semantic label, and source payload field or output pattern; facet metadata should leave ideas, route decisions, metrics, claims, artifact lists, and scalar facts in profile-backed payload sections so the query-index extractor can derive rows.

## Binding Rules

- Read `migrate/placeholders.md` first to understand the placeholder meaning, producer, consumer, and kind.
- Choose the binding row with the exact placeholder token; do not infer a nearby row by name similarity.
- Store exact placeholder, skill, producer, consumer, kind, format profile ref, payload file role, and payload file and optional export metadata on created records.
- Render Markdown on demand with `isomer-cli --print-json ext research records render <record-id> --topic <topic>`; add `--output-file <path>` only for an explicit Markdown export.
- Use `isomer-cli ext deepsci call ...` only for source-shaped compatibility behavior, then status the durable meaning through the binding row here.

## Kind Defaults

| Kind | Storage Item | Record Kind | Default Label | Profile Prefix | Note |
| --- | --- | --- | --- | --- | --- |
| code | Code Artifact or promoted Agent Workspace material | `artifact` | `topic.records.artifacts` | `code` | Work in `topic.repos.main` or an Agent Workspace first, then promote durable code outputs into topic records. |
| decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision` | Record route choices, blockers, waivers, and closure decisions as Decision Records with linked evidence when available. |
| evidence | Evidence Item with an Artifact on-demand view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the on-demand Markdown view or source summary through the resolved topic records label. |
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |
| run record | Run record with optional Artifact or Evidence links | `run` | `topic.records.runs` | `run` | Use Run records for commands, configs, logs, outputs, metrics, environment facts, and validation refs. |
| runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control` | Use this for boards, checklists, route cursors, continuity notes, and other resumable control surfaces. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| DEEPSCI:EXPERIMENT-CONTEXT-BRIEF | evidence | Evidence Item with an Artifact on-demand view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/evidence/experiment-context-brief/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-id 'DEEPSCI:EXPERIMENT-CONTEXT-BRIEF' --format-profile isomer:deepsci/record-format/profile/evidence/experiment-context-brief/v2 --skill isomer-deepsci-experiment --producer 'idea, optimize, baseline, decision, or user context' --consumer 'isomer-deepsci-experiment' --payload-file <payload-file>` |
| DEEPSCI:EXPERIMENT-CONTRACT | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/handoff/experiment-contract/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-id 'DEEPSCI:EXPERIMENT-CONTRACT' --format-profile isomer:deepsci/record-format/profile/handoff/experiment-contract/v2 --skill isomer-deepsci-experiment --producer 'isomer-deepsci-experiment' --consumer 'execution and validation' --payload-file <payload-file>` |
| DEEPSCI:EXPERIMENT-PLAN | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/control/experiment-plan/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-id 'DEEPSCI:EXPERIMENT-PLAN' --format-profile isomer:deepsci/record-format/profile/control/experiment-plan/v2 --skill isomer-deepsci-experiment --producer 'isomer-deepsci-experiment' --consumer 'execution and validation' --payload-file <payload-file>` |
| DEEPSCI:EXPERIMENT-CHECKLIST | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/control/experiment-checklist/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-id 'DEEPSCI:EXPERIMENT-CHECKLIST' --format-profile isomer:deepsci/record-format/profile/control/experiment-checklist/v2 --skill isomer-deepsci-experiment --producer 'isomer-deepsci-experiment' --consumer 'execution and validation' --payload-file <payload-file>` |
| DEEPSCI:IMPLEMENTATION-CHANGE-MAP | code | Code Artifact or promoted Agent Workspace material | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/code/implementation-change-map/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-id 'DEEPSCI:IMPLEMENTATION-CHANGE-MAP' --format-profile isomer:deepsci/record-format/profile/code/implementation-change-map/v2 --skill isomer-deepsci-experiment --producer 'isomer-deepsci-experiment' --consumer 'execution' --payload-file <payload-file>` |
| DEEPSCI:SMOKE-CHECK-RECORD | run record | Run record with optional Artifact or Evidence links | `run` | `topic.records.runs` | `isomer:deepsci/record-format/profile/run/smoke-check-record/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind run --semantic-id 'DEEPSCI:SMOKE-CHECK-RECORD' --format-profile isomer:deepsci/record-format/profile/run/smoke-check-record/v2 --skill isomer-deepsci-experiment --producer 'isomer-deepsci-experiment' --consumer 'real run decision' --payload-file <payload-file>` |
| DEEPSCI:MAIN-RUN-RECORD | run record | Run record with optional Artifact or Evidence links | `run` | `topic.records.runs` | `isomer:deepsci/record-format/profile/run/main-run-record/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind run --semantic-id 'DEEPSCI:MAIN-RUN-RECORD' --format-profile isomer:deepsci/record-format/profile/run/main-run-record/v2 --skill isomer-deepsci-experiment --producer 'isomer-deepsci-experiment' --consumer 'analysis, decision, optimize, finalize' --payload-file <payload-file>` |
| DEEPSCI:EXPERIMENT-ARTIFACT-MANIFEST | evidence | Evidence Item with an Artifact on-demand view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/evidence/experiment-artifact-manifest/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-id 'DEEPSCI:EXPERIMENT-ARTIFACT-MANIFEST' --format-profile isomer:deepsci/record-format/profile/evidence/experiment-artifact-manifest/v2 --skill isomer-deepsci-experiment --producer 'isomer-deepsci-experiment' --consumer 'analysis, decision, optimize, finalize' --payload-file <payload-file>` |
| DEEPSCI:CLAIM-VALIDATION-RECORD | evidence | Evidence Item with an Artifact on-demand view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/evidence/claim-validation-record/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-id 'DEEPSCI:CLAIM-VALIDATION-RECORD' --format-profile isomer:deepsci/record-format/profile/evidence/claim-validation-record/v2 --skill isomer-deepsci-experiment --producer 'isomer-deepsci-experiment' --consumer 'analysis, write, decision, finalize' --payload-file <payload-file>` |
| DEEPSCI:EXPERIMENT-RESULT-SUMMARY | evidence | Evidence Item with an Artifact on-demand view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/evidence/experiment-result-summary/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-id 'DEEPSCI:EXPERIMENT-RESULT-SUMMARY' --format-profile isomer:deepsci/record-format/profile/evidence/experiment-result-summary/v2 --skill isomer-deepsci-experiment --producer 'isomer-deepsci-experiment' --consumer 'analysis, decision, optimize, finalize' --payload-file <payload-file>` |
| DEEPSCI:EXPERIMENT-ROUTE-DECISION | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/experiment-route-decision/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-id 'DEEPSCI:EXPERIMENT-ROUTE-DECISION' --format-profile isomer:deepsci/record-format/profile/decision/experiment-route-decision/v2 --skill isomer-deepsci-experiment --producer 'isomer-deepsci-experiment' --consumer 'analysis, optimize, decision, finalize, idea' --payload-file <payload-file>` |
| DEEPSCI:EXPERIMENT-BLOCKER-RECORD | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/experiment-blocker-record/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-id 'DEEPSCI:EXPERIMENT-BLOCKER-RECORD' --format-profile isomer:deepsci/record-format/profile/decision/experiment-blocker-record/v2 --skill isomer-deepsci-experiment --producer 'isomer-deepsci-experiment' --consumer 'user or decision' --payload-file <payload-file>` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --semantic-id 'DEEPSCI:WHAT'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-payload` to inspect one stored record, payload, and metadata.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --semantic-id 'DEEPSCI:WHAT' --payload-file <payload-file>` for status, metadata, or repair updates. Use `isomer-cli --print-json ext research records revise <record-id> --topic <topic> --payload-file <payload-file>` when accepted content changes and must remain visible as a new descendant revision.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves managed payload files by default.
