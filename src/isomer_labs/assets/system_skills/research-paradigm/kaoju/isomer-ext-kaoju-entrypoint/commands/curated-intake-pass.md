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

# Curated Intake Pass

## Workflow

1. **Frame the intake**. Accept the base survey refs, nominated items, intended priority, and update boundary; use clarification-first when disposition rules are unclear.
2. **Resolve every item**. Use `isomer-ext-kaoju-entrypoint->discover` to assign a stable intake id, attempt Source Identity resolution, detect duplicates, and retain one terminal disposition per item.
3. **Acquire and examine**. Use `isomer-ext-kaoju-entrypoint->acquire` and `isomer-ext-kaoju-entrypoint->examine` as needed to create a Source Digest or Source Access Blocker for each nomination.
4. **Propose a delta**. Map useful evidence to catalog, summary, Claim-Evidence Ledger, chronology, taxonomy, limitations, artifact links, or reading path changes.
5. **Audit**. Use `isomer-ext-kaoju-entrypoint->audit` against the base refs, all intake dispositions, and the Curated Source Intake Delta.
6. **Synthesize the accepted delta**. Use `isomer-ext-kaoju-entrypoint->synthesize` only after audit acceptance.
7. **Stop**. Return this bounded procedure's terminal report without executing curated code or selecting another procedure internally. An explicitly authorized prompt-level run-to controller may consume an in-closure recovery route after the report is recorded.

If the request does not map cleanly to this recipe, use the native planning tool to build and execute a bounded intake plan while preserving every nominated item's accounting and audit before synthesis.

## Trigger

Use when the user says that a list of important references or codebases is worth reading and should inform an existing survey.

## Inputs

Require the nominated locators or identities, base survey Artifact refs, active Survey Contract, desired inspection depth, and any stated reasons for priority. A nomination receives priority review, not automatic authority or inclusion.

## Outputs

- Stable intake ids and resolved or attempted Source Identities.
- One Source Digest or Source Access Blocker per nominated item.
- Dispositions: included, excluded, duplicate, or blocked, each with reason.
- Audited Curated Source Intake Delta and updated survey view refs.

## Stop Conditions

Stop only after every nominated item has a terminal disposition. Code execution remains out of scope unless the user separately selects `method-trial-pass` or `comparative-pass`.

## Guardrails

- DO NOT treat the user's list as ground truth.
- DO NOT drop inaccessible or duplicate nominations from the intake record.
- DO NOT mutate the base survey before the delta is audited.
