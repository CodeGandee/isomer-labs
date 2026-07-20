---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Ingest Reading Item

## Workflow

1. Resolve the exact Reading List item, version family, source class, requested inspection depth, and existing Artifact Library entry from the state DB.
2. Use `isomer-ext-kaoju-entrypoint->acquire` for artifact-library-first lookup. Acquire by source type and use an authorized online fallback only when local material cannot satisfy the accepted depth.
3. Preserve inaccessible sources as `KAOJU:SOURCE-ACCESS-BLOCKER`; never reconstruct missing evidence from snippets or memory.
4. Use `isomer-ext-kaoju-entrypoint->examine` to inspect the primary work and linked material. Record exact page, section, equation, figure, table, or immutable commit plus file and line locators.
5. Keep source statements, interpretation, provisional visual evidence, code findings, and executed behavior distinct. Verify provisional figure or table evidence before promotion.
6. Persist or revise `KAOJU:ARTIFACT-LIBRARY`, `KAOJU:ASSOCIATED-SOURCE-CODE`, `KAOJU:SOURCE-DIGEST`, and `KAOJU:CLAIM-EVIDENCE-LEDGER` as applicable, then present them for approval or refinement.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Owner, Inputs, and Outputs

Owners: `isomer-ext-kaoju-entrypoint->acquire` and `isomer-ext-kaoju-entrypoint->examine`. Inputs: Reading List ref and item id. Outputs: acquired-material, Source Digest, Claim-Evidence Ledger, associated-code, blocker, and provenance refs.

## Gates, Blockers, and Resume

Human acceptance governs claim-bearing digest output. Resume from lookup, acquire, inspect, verify-visual, refine, or approve using the recorded blocker and Run refs.
