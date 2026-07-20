---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Manage Paper Template Metadata

Route: `isomer-ext-kaoju-entrypoint->manage-paper-template()->metadata()`. This intermediate command is an object generator and is a terminal task selector when no child is supplied.

## Subcommands

| Child Command | Use For | Detail |
| --- | --- | --- |
| `isomer-ext-kaoju-entrypoint->manage-paper-template()->metadata()->patch()` | Patch bounded authored metadata with the current template token. | [commands/manage-paper-template/metadata/patch.md](commands/manage-paper-template/metadata/patch.md) |

## Workflow

1. Resolve `--kind content|latex`, one role-local template, its current token, and the requested metadata patch.
2. When no child or unambiguous task is supplied, return the Subcommands table instead of guessing.
3. Apply the selected bounded patch without claiming a private resource root; all resources remain owned by the containing Kaoju entrypoint.

If the request does not map cleanly to these steps, use the native planning tool to build and execute a bounded plan from the parent manager contract without inventing another command.
