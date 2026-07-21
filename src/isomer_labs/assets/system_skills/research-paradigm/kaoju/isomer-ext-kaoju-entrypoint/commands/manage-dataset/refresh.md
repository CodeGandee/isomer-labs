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

# Refresh Dataset

Route: `isomer-ext-kaoju-entrypoint->manage-dataset()->refresh()`.

## Workflow

1. Resolve one registered dataset and preserve its previous fingerprint and observation.
2. Ask the Topic Workspace owner to reinspect identity, access, license, and observed metadata without mutating the external target.
3. Revise the canonical manifest with the new observation and owner provenance.
4. Report changes, staleness posture, and resulting reuse eligibility.

If the request does not map cleanly to these steps, use the native planning tool to build and execute a bounded plan from the parent manager contract without inventing another command.
