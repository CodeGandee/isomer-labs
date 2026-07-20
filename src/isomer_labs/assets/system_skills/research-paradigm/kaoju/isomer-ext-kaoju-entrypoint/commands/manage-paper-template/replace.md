---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Replace Paper Template

Route: `isomer-ext-kaoju-entrypoint->manage-paper-template()->replace()`. The containing Kaoju entrypoint owns this command's resources.

## Workflow

1. Resolve one role, target name, source template name, and target's current token.
2. Verify that source and target are role-local and that no merge is intended.
3. Run `template update --kind KIND --name TARGET --from-template SOURCE --expected-state TOKEN`.
4. Report the unchanged source and resulting target ref, token, and digest.

If the request does not map cleanly to these steps, use the native planning tool to build and execute a bounded plan from the parent manager contract without inventing another command.
