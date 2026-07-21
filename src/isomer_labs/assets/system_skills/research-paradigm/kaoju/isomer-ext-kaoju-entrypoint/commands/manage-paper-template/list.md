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

# List Paper Templates

Route: `isomer-ext-kaoju-entrypoint->manage-paper-template()->list()`. The containing Kaoju entrypoint owns this command's resources.

## Workflow

1. Resolve `--kind content|latex`; do not infer a route component from the role.
2. Run `isomer-cli --print-json ext kaoju paper template list --kind KIND`.
3. Report role, name, stable ref, token, digest, authored metadata, status, and working path without mutation.

If the request does not map cleanly to these steps, use the native planning tool to build and execute a bounded plan from the parent manager contract without inventing another command.
