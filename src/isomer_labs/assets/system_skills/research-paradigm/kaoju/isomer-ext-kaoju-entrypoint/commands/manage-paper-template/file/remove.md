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

# Remove Paper Template File

Route: `isomer-ext-kaoju-entrypoint->manage-paper-template()->file()->remove()`.

## Workflow

1. Resolve `--kind content|latex`, one role-local template, current token, and safe relative file path.
2. Reject reserved paths, unsafe traversal, a required entrypoint removal, role-contract violations, or a stale token.
3. Run the bounded role-explicit file remove operation and validate the resulting tree.
4. Report the stable and audit refs, new token and digest, removed path, and diagnostics.

If the request does not map cleanly to these steps, use the native planning tool to build and execute a bounded plan from the parent manager contract without inventing another command.
