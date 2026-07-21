---
skill_invocation_notation: >
  Top-level skill entrypoints use SKILL.md. Parent-scoped subskill entrypoints use
  SKILL-MAIN.md and are loaded explicitly through their parent; nested SKILL.md is
  accepted only as legacy input when SKILL-MAIN.md is absent.
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

Invoke `isomer-op-entrypoint->research-ideas` when optimization accepts durable candidate concepts, a promotion decision, fusion, split, follow-up, or exploration or evidence transition. Record exact candidate-object realizations, including the object path passed through `--source-json-path`, generation membership, complete promotion options, justified transitions with terminal refs, and concept lineage. Frontier boards, candidate lists, debug notes, metrics, artifact lists, implementation attempts, and rendered Markdown are not automatic Research Ideas.

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
| draft | Artifact with a draft profile | `artifact` | `topic.records.artifacts` | `draft` | Store drafts outside agent scratch once another skill may depend on them. |
| evidence | Evidence Item with an Artifact on-demand view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the on-demand Markdown view or source summary through the resolved topic records label. |
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store structured report payloads as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |
| run record | Run record with optional Artifact or Evidence links | `run` | `topic.records.runs` | `run` | Use Run records for commands, configs, logs, outputs, metrics, environment facts, and validation refs. |
| runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control` | Use this for boards, checklists, route cursors, continuity notes, and other resumable control surfaces. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| DEEPSCI:OPTIMIZATION-CONTEXT-BRIEF | evidence | Evidence Item with an Artifact on-demand view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/evidence/optimization-context-brief/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-id 'DEEPSCI:OPTIMIZATION-CONTEXT-BRIEF' --format-profile isomer:deepsci/record-format/profile/evidence/optimization-context-brief/v2 --skill isomer-deepsci-optimize --producer 'optimize, experiment, decision, or user context' --consumer 'isomer-deepsci-optimize' --payload-file <payload-file>` |
| DEEPSCI:OPTIMIZATION-FRONTIER | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/control/optimization-frontier/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-id 'DEEPSCI:OPTIMIZATION-FRONTIER' --format-profile isomer:deepsci/record-format/profile/control/optimization-frontier/v2 --skill isomer-deepsci-optimize --producer 'isomer-deepsci-optimize' --consumer 'ranking, experiment, decision' --payload-file <payload-file>` |
| DEEPSCI:OPTIMIZE-CHECKLIST | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/control/optimize-checklist/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-id 'DEEPSCI:OPTIMIZE-CHECKLIST' --format-profile isomer:deepsci/record-format/profile/control/optimize-checklist/v2 --skill isomer-deepsci-optimize --producer 'isomer-deepsci-optimize' --consumer 'optimize closeout and resume' --payload-file <payload-file>` |
| DEEPSCI:CANDIDATE-BOARD | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/control/candidate-board/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-id 'DEEPSCI:CANDIDATE-BOARD' --format-profile isomer:deepsci/record-format/profile/control/candidate-board/v2 --skill isomer-deepsci-optimize --producer 'isomer-deepsci-optimize' --consumer 'frontier review and ranking' --payload-file <payload-file>` |
| DEEPSCI:CANDIDATE-BRIEF | draft | Artifact with a draft profile | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/draft/candidate-brief/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-id 'DEEPSCI:CANDIDATE-BRIEF' --format-profile isomer:deepsci/record-format/profile/draft/candidate-brief/v2 --skill isomer-deepsci-optimize --producer 'isomer-deepsci-optimize' --consumer 'ranking or promotion' --payload-file <payload-file>` |
| DEEPSCI:METHOD-BRIEF | draft | Artifact with a draft profile | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/draft/method-brief/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-id 'DEEPSCI:METHOD-BRIEF' --format-profile isomer:deepsci/record-format/profile/draft/method-brief/v2 --skill isomer-deepsci-optimize --producer 'isomer-deepsci-optimize' --consumer 'ranking or promotion' --payload-file <payload-file>` |
| DEEPSCI:CANDIDATE-RANKING | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/report/candidate-ranking/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-id 'DEEPSCI:CANDIDATE-RANKING' --format-profile isomer:deepsci/record-format/profile/report/candidate-ranking/v2 --skill isomer-deepsci-optimize --producer 'isomer-deepsci-optimize' --consumer 'promotion or decision' --payload-file <payload-file>` |
| DEEPSCI:CODEGEN-ROUTE-PLAN | code | Code Artifact or promoted Agent Workspace material | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/code/codegen-route-plan/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-id 'DEEPSCI:CODEGEN-ROUTE-PLAN' --format-profile isomer:deepsci/record-format/profile/code/codegen-route-plan/v2 --skill isomer-deepsci-optimize --producer 'isomer-deepsci-optimize' --consumer 'implementation attempt' --payload-file <payload-file>` |
| DEEPSCI:PROMOTED-OPTIMIZATION-LINE | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/handoff/promoted-optimization-line/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-id 'DEEPSCI:PROMOTED-OPTIMIZATION-LINE' --format-profile isomer:deepsci/record-format/profile/handoff/promoted-optimization-line/v2 --skill isomer-deepsci-optimize --producer 'isomer-deepsci-optimize' --consumer 'experiment' --payload-file <payload-file>` |
| DEEPSCI:OPTIMIZATION-ATTEMPT-RECORD | run record | Run record with optional Artifact or Evidence links | `run` | `topic.records.runs` | `isomer:deepsci/record-format/profile/run/optimization-attempt-record/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind run --semantic-id 'DEEPSCI:OPTIMIZATION-ATTEMPT-RECORD' --format-profile isomer:deepsci/record-format/profile/run/optimization-attempt-record/v2 --skill isomer-deepsci-optimize --producer 'isomer-deepsci-optimize or experiment' --consumer 'frontier review' --payload-file <payload-file>` |
| DEEPSCI:DEBUG-RESPONSE | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/report/debug-response/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-id 'DEEPSCI:DEBUG-RESPONSE' --format-profile isomer:deepsci/record-format/profile/report/debug-response/v2 --skill isomer-deepsci-optimize --producer 'isomer-deepsci-optimize' --consumer 'implementation or frontier review' --payload-file <payload-file>` |
| DEEPSCI:FUSION-PLAN | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/handoff/fusion-plan/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-id 'DEEPSCI:FUSION-PLAN' --format-profile isomer:deepsci/record-format/profile/handoff/fusion-plan/v2 --skill isomer-deepsci-optimize --producer 'isomer-deepsci-optimize' --consumer 'implementation or experiment' --payload-file <payload-file>` |
| DEEPSCI:PLATEAU-RESPONSE | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/plateau-response/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-id 'DEEPSCI:PLATEAU-RESPONSE' --format-profile isomer:deepsci/record-format/profile/decision/plateau-response/v2 --skill isomer-deepsci-optimize --producer 'isomer-deepsci-optimize' --consumer 'frontier review and future optimize pass' --payload-file <payload-file>` |
| DEEPSCI:PROMPT-CONTRACT | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/control/prompt-contract/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-id 'DEEPSCI:PROMPT-CONTRACT' --format-profile isomer:deepsci/record-format/profile/control/prompt-contract/v2 --skill isomer-deepsci-optimize --producer 'isomer-deepsci-optimize' --consumer 'candidate shaping, debug, fusion, or codegen' --payload-file <payload-file>` |
| DEEPSCI:OPTIMIZATION-MEMORY-CARD | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/control/optimization-memory-card/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-id 'DEEPSCI:OPTIMIZATION-MEMORY-CARD' --format-profile isomer:deepsci/record-format/profile/control/optimization-memory-card/v2 --skill isomer-deepsci-optimize --producer 'isomer-deepsci-optimize' --consumer 'future optimize work' --payload-file <payload-file>` |
| DEEPSCI:FRONTIER-REVIEW | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/report/frontier-review/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-id 'DEEPSCI:FRONTIER-REVIEW' --format-profile isomer:deepsci/record-format/profile/report/frontier-review/v2 --skill isomer-deepsci-optimize --producer 'isomer-deepsci-optimize' --consumer 'route decision' --payload-file <payload-file>` |
| DEEPSCI:OPTIMIZE-ROUTE-DECISION | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/optimize-route-decision/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-id 'DEEPSCI:OPTIMIZE-ROUTE-DECISION' --format-profile isomer:deepsci/record-format/profile/decision/optimize-route-decision/v2 --skill isomer-deepsci-optimize --producer 'isomer-deepsci-optimize' --consumer 'any production DeepSci research skill' --payload-file <payload-file>` |
| DEEPSCI:OPTIMIZE-BLOCKER-RECORD | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/optimize-blocker-record/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-id 'DEEPSCI:OPTIMIZE-BLOCKER-RECORD' --format-profile isomer:deepsci/record-format/profile/decision/optimize-blocker-record/v2 --skill isomer-deepsci-optimize --producer 'isomer-deepsci-optimize' --consumer 'user or decision' --payload-file <payload-file>` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --semantic-id 'DEEPSCI:WHAT'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-payload` to inspect one stored record, payload, and metadata.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --semantic-id 'DEEPSCI:WHAT' --payload-file <payload-file>` for status, metadata, or repair updates. Use `isomer-cli --print-json ext research records revise <record-id> --topic <topic> --payload-file <payload-file>` when accepted content changes and must remain visible as a new descendant revision.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves managed payload files by default.
