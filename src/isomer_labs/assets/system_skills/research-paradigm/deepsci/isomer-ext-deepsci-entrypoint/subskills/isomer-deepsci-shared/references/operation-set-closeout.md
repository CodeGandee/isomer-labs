---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Operation Set Closeout

Use this contract after the owning production DeepSci skill has applied all end callbacks and before it returns a final response, hands output to another skill, advances a pipeline, or reports successful completion. End callbacks can create or change material files, so any inventory taken before them is provisional.

## Closeout Procedure

1. Determine whether closeout is applicable. If the workflow opened an operation set or wrote a payload staging file, report, code deliverable, table, figure, note, log, build, or other material plain file, closeout is required. If it opened no operation set and used or created only already durable records, record `closeout: not_applicable` with those durable refs.
2. Invoke `isomer-op-entrypoint->operation-sets` and inspect the operation set after end callbacks. Inventory every regular material file regardless of Git status. A Git commit, rendered Markdown file, terminal summary, or worker path does not make an artifact durable.
3. Author or confirm the versioned acceptance manifest. Give every file an explicit `record_payload`, `record_attachment`, or reasoned `disposable` disposition. Resolve record kinds, semantic ids, profiles, actions, parents, and existing refs from authoritative bindings; never derive them from names or prose.
4. Keep the two lineage layers explicit. Record canonical immediate record parents for every created or revised record. For idea-bearing payloads, invoke `isomer-op-entrypoint->research-ideas` and pass exact `research_idea_effects`, including exact realization paths, through the same atomic record transaction. Do not infer Idea Lineage Edges from record lineage.
5. Preview, apply, and verify the unchanged manifest with the focused recording workflow. Require a receipt whose status is `complete`, exhaustive dispositions, queryable durable records, matching managed attachments, verified record lineage, and every promised Research Idea effect. Preserve the receipt id, durable record refs, record-lineage refs, and returned idea refs.
6. Return one terminal closeout result. A successful applicable closeout reports `closeout: complete`, the receipt id, and durable refs. A file-free durable workflow reports `closeout: not_applicable` and its durable refs. Any `applying`, `partial`, stale, invalid, or unverifiable result reports `closeout: paused`, preserves accepted refs and the partial receipt when present, lists deterministic diagnostics, and gives the exact resume command.

If the task does not map cleanly to this procedure, pause before final response or handoff and use the native planning tool to classify the unresolved outputs without broadening the owning skill's authority.

## Terminal Result Contract

| Closeout | Required Evidence | May Report Workflow Success |
| --- | --- | --- |
| `complete` | Verified complete receipt id, durable record refs, and any record-lineage or Research Idea refs promised by the manifest | Yes |
| `not_applicable` | Statement that no operation set was opened, plus the durable refs used or created | Yes |
| `paused` | Accepted refs, partial receipt when present, diagnostics, unresolved owner action, and exact resume command | No |

A missing path, forgotten operation-set id, unclassified file, absent receipt, or file-only terminal claim is a paused closeout, not `not_applicable`.

## Pipeline Use

A pipeline stage can hand an artifact to the next stage only through a verified durable record ref. The stage entry also carries either its complete receipt id or explicit `closeout: not_applicable` evidence. A missing, partial, stale, or unverifiable receipt stops progression at that stage. The pipeline applies this same contract to its terminal report and any other pipeline-level material files before it can report `status: complete`.

## Guardrails

- DO NOT run closeout before end callbacks.
- DO NOT treat Git tracking, a worker path, a render, or terminal prose as durable acceptance.
- DO NOT use `not_applicable` when material files exist or an operation set was opened.
- DO NOT infer record lineage, Idea Realizations, facets, lifecycle transitions, decisions, generations, or Idea Lineage from filenames or from the other lineage layer.
- DO NOT report success or advance a pipeline from a partial or unverifiable receipt.
