---
name: isomer-research-operation-set-recording
description: Use when an Isomer Topic Actor or Agent has produced an operation-set directory whose material files must be exhaustively classified, promoted into durable research records or managed attachments, correlated through canonical record or Research Idea lineage, accepted with a resumable receipt, verified, or explicitly repaired from legacy records before workflow completion.
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Research Operation Set Recording

## Overview

Close the boundary between worker-local staging files and durable Topic Workspace research state. Use the receipt-backed `isomer-cli ext research operation-sets` family to account for every material file, delegate records and authored Research Idea effects to their canonical services, and prove completion without interpreting filenames or prose as research semantics.

Read `references/manifest-contract.md` before authoring or changing a manifest. Read `references/command-reference.md` before running the CLI. Read `references/recovery.md` for a partial receipt or failed verification. Read `references/legacy-repair.md` only for an operation set whose outputs were already recovered manually.

## When to Use

Use this skill when a worker operation set needs durable closeout, when a receipt is partial or fails verification, or when a named legacy operation set must be reconciled to existing recovered records. Use `isomer-op-entrypoint->research-ideas` as a separate owner whenever the accepted output creates or changes durable research concepts.

## Workflow

1. **Resolve one worker boundary**. Establish Effective Topic Context and select exactly one Topic Actor or Agent. Confirm that the operation-set directory is below that worker's resolved output root. Stop on ambiguity, traversal, symlinks, special files, or an unavailable root.
2. **Inspect every material file**. Run `operation-sets inspect`. Treat every regular file outside `.isomer-operation-set/` as staging material regardless of Git status. Use `--write-scaffold` only when the user wants a new incomplete manifest; never overwrite an existing manifest.
3. **Author explicit dispositions and record intents**. Classify each file as `record_payload`, `record_attachment`, or `disposable`. Give disposable files a concrete reason. Map durable files to named `create`, `revise`, or `reference` intents through existing record bindings. Resolve semantic ids, profiles, scope keys, producers, and lifecycle refs from authoritative contracts; do not infer them.
4. **Author both lineage layers separately**. Declare each immediate record parent or an explicit root reason. Use `revision_of` only through the existing revise action. If the accepted payload creates or changes durable research concepts, invoke `isomer-op-entrypoint->research-ideas`, author exact `research_idea_effects`, and keep Idea Lineage independent from record lineage.
5. **Preview the whole plan**. Run `operation-sets accept <manifest-path>` without `--apply`. Review ordered actions, result ids, managed-copy destinations, record parents, Idea effects, receipt identity, and every diagnostic. Do not proceed while any file, binding, payload, parent, idea ref, digest, or destination is invalid.
6. **Apply the unchanged plan**. Add `--apply` only after the preview is valid. Preserve the returned receipt id, per-intent record ids, managed file refs, lineage refs, and Research Idea effect refs. A later item failure leaves earlier records durable and changes the receipt to `partial`.
7. **Verify before completion**. Run `operation-sets verify <receipt-or-operation-set-id>`. Require a `complete` receipt, exhaustive staged-file reconciliation, matching managed digests, queryable records, canonical record lineage, and every promised Research Idea effect. Report the durable refs and receipt instead of worker paths.

If the request does not map cleanly to this workflow, use the native planning tool to build a bounded recording plan from current Topic Context, worker output policy, the manifest contract, authoritative record bindings, and unresolved semantics, then execute only the authorized steps or stop on a concrete blocker.

## Chat Response

Present normal chat responses in natural-language Markdown. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.

## Completion Boundary

An operation set is accepted only when apply returns a complete receipt and independent verification succeeds. A valid preview, Git commit, worker path, Markdown summary, query-index extraction, or chat statement does not satisfy this boundary. If the workflow opened no operation set, its owning closeout contract may report explicit `not_applicable`; losing the path or leaving unclassified files does not qualify.

## Guardrails

- DO NOT scan unrelated worker roots or accept an arbitrary directory.
- DO NOT omit ignored, untracked, low-value, or inconvenient files from inventory.
- DO NOT guess record kinds, semantic ids, scope keys, profiles, producers, parents, Research Ideas, facet transitions, decisions, generations, or lineage.
- DO NOT index a worker-staging path as a durable attachment. Use the planned owner-preserved managed copy.
- DO NOT edit receipt rows, query-index rows, canonical lineage, or Idea state by hand to make verification pass.
- DO NOT delete a committed record because a later acceptance item failed.
- DO NOT change a manifest after partial apply. Resume with the identical revision and digest, or author an explicit higher revision that names the superseded receipt.
- DO NOT use a `reference` intent unless the existing record and managed content digest or attachment relationship can be verified.
