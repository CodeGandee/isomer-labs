---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Patch Paper Template Metadata

Route: `isomer-ext-kaoju-entrypoint->manage-paper-template()->metadata()->patch()`.

## Workflow

1. Resolve `--kind content|latex`, one role-local template, current token, and a bounded authored-metadata patch.
2. Validate reserved fields and the role-specific content or LaTeX composition contract before mutation.
3. Run the role-explicit metadata patch operation with the current token.
4. Report the stable and audit refs, new token and digest, applied fields, and diagnostics.

If the request does not map cleanly to these steps, use the native planning tool to build and execute a bounded plan from the parent manager contract without inventing another command.
