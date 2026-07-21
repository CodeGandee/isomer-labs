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

# Export Paper Template

Route: `isomer-ext-kaoju-entrypoint->manage-paper-template()->export()`. The containing Kaoju entrypoint owns this command's resources.

## Workflow

1. Consume the reconciled Research Topic as `TOPIC`, resolve one role-local template name, and distinguish registered exchange from any separately requested unmanaged copy.
2. For “export or get the LaTeX template for me to edit” with no custom destination, run `isomer-cli --print-json ext kaoju paper template export --topic TOPIC --kind latex --name main` without `--target`; use the returned `<exchange-root>/latex/main/` path.
3. For another role-local export, run `template export --topic TOPIC --kind KIND --name NAME`; use `<exchange-root>/<kind>/<name>/` when no destination override is supplied.
4. Compare returned selected-context metadata with `TOPIC`. If the typed export fails, preserve this target and exchange surface; stop, correct the selector, or route readiness. Do not use a raw copy, actor-local path, Agent Workspace, Topic Main, sibling topic, or arbitrary target as implicit recovery.
5. Report selected context, export ref, path, source token, and digest while keeping the tree non-canonical. A separately requested unmanaged copy must follow the successful registered export, retain its provenance, and never become canonical stock implicitly.

If the request does not map cleanly to these steps, use the native planning tool to build and execute a bounded plan from the parent manager contract without inventing another command.
