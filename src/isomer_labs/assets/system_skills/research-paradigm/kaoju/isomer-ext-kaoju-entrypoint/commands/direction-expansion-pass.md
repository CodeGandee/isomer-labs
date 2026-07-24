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

# Direction Expansion Pass

## Workflow

1. **Frame the direction**. Accept seed Source Identities, the survey topic, relation criteria, time boundary, desired frontier, and base catalog ref.
2. **Inspect seeds**. Use `isomer-ext-kaoju-entrypoint->examine` when their citations, terminology, claimed lineage, or implementation relationships are not already accepted evidence.
3. **Expand routes**. Use `isomer-ext-kaoju-entrypoint->discover` to define bounded backward, neighboring, forward, and post-seed strategy. Discover invokes `isomer-ext-kaoju-entrypoint->paper-search` for target resolution, citation traversal, and adjacent-paper retrieval, then records parent seed or query, route, relevance rationale, `latest_after`, `searched_through`, and candidate disposition through its existing outputs.
4. **Acquire and examine selected candidates**. Reach the accepted depth with `isomer-ext-kaoju-entrypoint->acquire` and `isomer-ext-kaoju-entrypoint->examine`.
5. **Propose a catalog delta**. Preserve important additions, exclusions, duplicates, blockers, chronology effects, and the remaining frontier.
6. **Audit**. Use `isomer-ext-kaoju-entrypoint->audit` to check seed identity, route provenance, coverage, and claim traceability.
7. **Synthesize the accepted delta**. Use `isomer-ext-kaoju-entrypoint->synthesize` only after audit acceptance.
8. **Stop**. Return this bounded procedure's terminal report without claiming exhaustive coverage. An explicitly authorized prompt-level run-to controller may consume an in-closure recovery route after the report is recorded.

If the request does not map cleanly to this recipe, use the native planning tool to build and execute a bounded expansion plan from these routes while preserving audit before synthesis.

## Trigger

Use when the user identifies works A, B, and C as interesting and asks for important related work in that direction, including work that came before and closely related work published after the seeds.

## Inputs

Require seed identities, base survey refs, relevance boundary, coverage date, post-seed interpretation, desired evidence depth, and stop conditions.

## Outputs

- Route-provenance Discovery Ledger.
- Related-Work Catalog Delta with work families and material identities.
- Updated chronology, taxonomy, Field Summary, Claim-Evidence Ledger, and reading path where affected.
- `latest_after`, `searched_through`, remaining frontier, and unresolved blockers.

## Stop Conditions

Stop when every planned route reaches its accepted bound and important candidates have an audited disposition. Citation count, publication date, or provider rank alone never determines importance.

## Guardrails

- DO NOT follow only backward citations.
- DO NOT call any chronologically later item a continuation of the seed direction.
- DO NOT lose which seed or query produced each candidate.
