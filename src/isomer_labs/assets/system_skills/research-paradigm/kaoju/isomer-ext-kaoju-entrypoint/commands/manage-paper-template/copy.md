---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Copy Paper Template

Route: `isomer-ext-kaoju-entrypoint->manage-paper-template()->copy()`. The containing Kaoju entrypoint owns this command's resources.

## Workflow

1. Resolve one role, existing source name, and distinct target name.
2. Verify that source and target remain inside the selected role.
3. Run `template create --kind KIND --name NEW --from-template EXISTING`.
4. Report the unchanged source and the new target ref, token, and digest.

If the request does not map cleanly to these steps, use the native planning tool to build and execute a bounded plan from the parent manager contract without inventing another command.
