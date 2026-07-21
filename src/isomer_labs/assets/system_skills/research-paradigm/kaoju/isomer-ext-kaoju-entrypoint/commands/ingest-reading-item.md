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

# Ingest Reading Item

## Workflow

1. Resolve the exact Reading List item, version family, source class, requested inspection depth, and existing Artifact Library entry from the state DB. Pause when skim or triage versus deep or full-text depth is ambiguous.
2. Require the Run-scoped Mindset Record handed off by the public entrypoint: `paper.skimming` for skim or triage and `paper.deep-dive` for deep or full-text inspection. Verify its pinned Research Topic, Survey Contract, Run scope, Source path and digest, immutable materialized question inventory, and initially checked state. Do not re-read a changed Mindset Source during this Run.
3. Use `isomer-ext-kaoju-entrypoint->acquire` for artifact-library-first lookup. Acquire by source type and use an authorized online fallback only when local material cannot satisfy the accepted depth.
4. Preserve inaccessible sources as `KAOJU:SOURCE-ACCESS-BLOCKER`; never reconstruct missing evidence from snippets or memory.
5. Use `isomer-ext-kaoju-entrypoint->examine` to inspect the primary work and linked material. Pass the Mindset Record ref and record exact page, section, equation, figure, table, or immutable commit plus file and line locators.
6. Answer and checkpoint every materialized question against the active survey context, mark unsupported answers unresolved or not applicable with rationale, cite exact evidence refs, and check the `additional-questions` collector. A conflicting or impossible question does not override instructions, Workflow boundaries, Gates, or authorization.
7. Keep source statements, interpretation, provisional visual evidence, code findings, and executed behavior distinct. Verify provisional figure or table evidence before promotion.
8. Persist or revise `KAOJU:ARTIFACT-LIBRARY`, `KAOJU:ASSOCIATED-SOURCE-CODE`, `KAOJU:SOURCE-DIGEST`, and `KAOJU:CLAIM-EVIDENCE-LEDGER` as applicable, then present them for approval or refinement. Ordinary mid-reading user questions and findings remain in these reading Artifacts unless the user explicitly targets the Mindset Record or both Record and Source.
9. Before completing, pausing, or blocking, checkpoint a terminal Mindset Record with every materialized and explicitly assigned supplemental question classified, the collector checked, evidence retained, and unresolved questions visible. Claim-bearing acceptance requires this terminal Record.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Owner, Inputs, and Outputs

Owners: `isomer-ext-kaoju-entrypoint->acquire` and `isomer-ext-kaoju-entrypoint->examine`. Inputs: Reading List ref, item id, and Run-scoped Mindset Record ref. Outputs: terminal Mindset Record, acquired-material, Source Digest, Claim-Evidence Ledger, associated-code, blocker, and provenance refs.

## Gates, Blockers, and Resume

Human acceptance governs claim-bearing digest output. Resume from lookup, acquire, inspect, verify-visual, refine, or approve using the recorded blocker and Run refs.
