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

# Legacy Operation Set Repair

Use this procedure only when a named historical operation set lacks a receipt. Do not scan all worker directories during installation, upgrade, validation, or ordinary closeout.

1. Run `inspect` on the explicitly selected operation-set root and preserve every missing-disposition, binding, parent, and idea-effect diagnostic.
2. Author a revision 1 manifest from current bytes. Classify every material file. Do not reconstruct historical semantics from filenames, timestamps, Markdown, or chat memory.
3. For an output already represented by a manually recovered durable record, use a `reference` intent with that exact `target_record_id`. Declare only canonical record parents and Idea effects already supported by durable evidence.
4. Preview acceptance. A reference must verify matching managed content and expected canonical lineage. If it cannot, preserve the uncertainty and use the owning corrective record workflow instead of forcing a receipt.
5. Apply and verify the repair manifest. Report that the receipt reconciles historical staging; it does not prove that unrecorded historical decisions or lineage once existed.

When old data cannot justify a Research Idea facet, decision option, transition, generation, or Idea Lineage Edge, leave it unknown or absent and record the limitation. Invoke `isomer-op-entrypoint->research-ideas` before any explicit canonical repair.
