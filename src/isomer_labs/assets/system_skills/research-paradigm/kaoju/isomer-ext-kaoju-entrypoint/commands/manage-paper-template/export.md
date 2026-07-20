---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Export Paper Template

Route: `isomer-ext-kaoju-entrypoint->manage-paper-template()->export()`. The containing Kaoju entrypoint owns this command's resources.

## Workflow

1. Resolve one role-local template name and authorized destination.
2. Run `template export --kind KIND --name NAME`; use `<exchange-root>/<kind>/<name>/` when no destination override is supplied.
3. Report the export ref, path, source token, and digest while keeping the tree non-canonical.

If the request does not map cleanly to these steps, use the native planning tool to build and execute a bounded plan from the parent manager contract without inventing another command.
