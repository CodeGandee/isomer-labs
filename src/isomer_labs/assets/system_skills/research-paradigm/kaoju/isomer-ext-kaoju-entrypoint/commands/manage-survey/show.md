---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Show Survey

Route: `isomer-ext-kaoju-entrypoint->manage-survey()->show()`.

## Workflow

1. Resolve one stable survey artifact ref; report ambiguity instead of choosing by timestamp.
2. Run `isomer-cli --print-json project artifacts show --topic <topic> <artifact-ref>`.
3. Report payload, relationships, lineage, content authority, and validation state without revising canonical content.

If the request does not map cleanly to these steps, use the native planning tool to build and execute a bounded plan from the parent manager contract without inventing another command.
