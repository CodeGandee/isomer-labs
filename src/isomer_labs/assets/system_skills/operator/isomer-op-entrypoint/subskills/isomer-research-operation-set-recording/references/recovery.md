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

# Acceptance Recovery

## Partial Apply

Do not remove records from completed items. Inspect the receipt and failed item diagnostics, then correct only external prerequisites or transient conditions that do not change manifest inputs. Retry the same `accept <manifest-path> --apply` command with the unchanged manifest. The coordinator verifies completed items and resumes pending or failed items.

If a staged file, disposition, binding, parent, or authored effect must change, do not overwrite the applied revision. Author a higher manifest revision, set `supersedes_receipt_id` to the prior receipt, preview it, and apply it. The old receipt remains queryable.

## Verification Failure

Run `verify` and classify each diagnostic before mutation:

- Staged-file drift requires restoring the exact accepted bytes or authoring a new manifest revision.
- Missing or changed managed attachments require evidence-based restoration from the accepted digest; do not repoint the index to worker staging.
- A missing record or canonical lineage edge requires the owning record correction workflow. Do not hand-edit the query index.
- A missing Research Idea effect requires `isomer-op-entrypoint->research-ideas` or a new corrective record operation with authored semantics. Do not infer historical facets or Idea Lineage.
- A non-queryable record requires the supported record index refresh or validation surface after confirming that the durable record exists.

Verification never repairs state and does not change a complete receipt to hide drift. Preserve its diagnostics in the paused handoff.

## Resume Handoff

Report the operation-set root, manifest path and digest, receipt id and status, completed and failed intent keys, committed record refs, diagnostic codes, the exact resume command, and the first unresolved owner action. Do not describe a partial receipt as complete.
