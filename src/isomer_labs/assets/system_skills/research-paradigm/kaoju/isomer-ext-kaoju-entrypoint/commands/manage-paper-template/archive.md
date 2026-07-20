---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Archive Paper Template

Route: `isomer-ext-kaoju-entrypoint->manage-paper-template()->archive()`. The containing Kaoju entrypoint owns this command's resources.

## Workflow

1. Resolve one role-local name and current token, then inspect durable paper references to its stable ref.
2. Stop if durable paper state still depends on the template.
3. Run the role-explicit archive operation and report the retained audit and historical evidence.

If the request does not map cleanly to these steps, use the native planning tool to build and execute a bounded plan from the parent manager contract without inventing another command.
