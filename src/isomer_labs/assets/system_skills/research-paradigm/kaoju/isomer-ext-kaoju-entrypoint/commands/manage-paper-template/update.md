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

# Update Paper Template

Route: `isomer-ext-kaoju-entrypoint->manage-paper-template()->update()`. The containing Kaoju entrypoint owns this command's resources.

## Workflow

1. Resolve one role-local target, assessed source directory, and current expected-state token.
2. Report the target ref, token, digest, source, and assessed change before mutation.
3. Run `template update --kind KIND --name NAME --from PATH --expected-state TOKEN`.
4. On a lost-update conflict, reread state and stop for reconciliation instead of retrying with a stale token.

If the request does not map cleanly to these steps, use the native planning tool to build and execute a bounded plan from the parent manager contract without inventing another command.
