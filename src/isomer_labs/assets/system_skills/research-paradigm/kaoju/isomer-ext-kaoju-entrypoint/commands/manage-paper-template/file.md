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

# Manage Paper Template File

Route: `isomer-ext-kaoju-entrypoint->manage-paper-template()->file()`. This intermediate command is an object generator and is a terminal task selector when no child is supplied.

## Subcommands

| Child Command | Use For | Detail |
| --- | --- | --- |
| `isomer-ext-kaoju-entrypoint->manage-paper-template()->file()->put()` | Put one bounded file with the current template token. | [commands/manage-paper-template/file/put.md](commands/manage-paper-template/file/put.md) |
| `isomer-ext-kaoju-entrypoint->manage-paper-template()->file()->remove()` | Remove one bounded file with the current template token. | [commands/manage-paper-template/file/remove.md](commands/manage-paper-template/file/remove.md) |

## Workflow

1. Resolve `--kind content|latex`, one role-local template, its current token, and exactly one child action.
2. When no child or unambiguous task is supplied, return the Subcommands table instead of guessing.
3. Apply the selected bounded edit without claiming a private resource root; all resources remain owned by the containing Kaoju entrypoint.

If the request does not map cleanly to these steps, use the native planning tool to build and execute a bounded plan from the parent manager contract without inventing another command.
