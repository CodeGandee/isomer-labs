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

# Manage Survey

## Subcommands

`manage-survey()` is a terminal task selector when invoked without a child. It presents these actions and waits for or infers exactly one selection from the user's task.

| Child Command | Use For | Detail |
| --- | --- | --- |
| `isomer-ext-kaoju-entrypoint->manage-survey()->list()` | List canonical survey artifacts for one Research Topic. | [commands/manage-survey/list.md](commands/manage-survey/list.md) |
| `isomer-ext-kaoju-entrypoint->manage-survey()->show()` | Inspect one stable survey artifact and its lineage. | [commands/manage-survey/show.md](commands/manage-survey/show.md) |
| `isomer-ext-kaoju-entrypoint->manage-survey()->status()` | Report scoped terminal or active-procedure status. | [commands/manage-survey/status.md](commands/manage-survey/status.md) |
| `isomer-ext-kaoju-entrypoint->manage-survey()->export()` | Render or export one accepted survey representation. | [commands/manage-survey/export.md](commands/manage-survey/export.md) |

## Workflow

1. **Select an action**. Accept exactly one of `list`, `show`, `status`, or `export` plus the Research Topic or survey ref required by that action. When no child command or unambiguous task is supplied, return the Subcommands table as the terminal result instead of guessing.
2. **Resolve current state**. Query canonical bound records through the state DB and typed Artifact service; do not infer state from stale prompt memory, rendered files, or directory scans.
3. **Execute the action**. Apply the action contract below without changing evidence meaning, audit state, or lineage.
4. **Return results**. Report selected refs, current status, diagnostics, or export destination and provenance.

If the request does not map cleanly to these actions, use the native planning tool to build and execute a bounded read or export plan without inventing another manager action.

## Actions

| Action | Behavior |
| --- | --- |
| `list` | Run `isomer-cli --print-json project artifacts list --topic <topic>` with optional exact semantic-id and scope filters; return stable ref, title, summary, semantic id, scope, revision posture, terminal status, validation state, and content diagnostics. |
| `show` | Run `isomer-cli --print-json project artifacts show --topic <topic> <artifact-ref>` and inspect returned payload, relationships, lineage, content authority, and validation state. |
| `status` | Use `project artifacts latest` for the scoped terminal report and `project runs status` for the active procedure. Report every competing current candidate as ambiguity; never select by timestamp alone. |
| `export` | Use the typed renderer for a single record, `ext kaoju paper` for paper exchange or derivation, and `ext kaoju wiki` for a survey wiki. Preserve source revisions and checksums without changing canonical state. |

## Inputs and Outputs

`list` needs a resolved Research Topic. `show` and `status` need one stable record or procedure ref. `export` also needs the requested representation and destination authority. All actions are read-only except the explicit export file; none revise canonical content, evidence, lineage, or latest identity.

Export does not create new survey evidence or change an Audit Report. If the destination requires a Topic Workspace mutation or external side effect, route it to the applicable owner and Gate.

## Operational Notes

- Return the resume context instead.

## Guardrails

- DO NOT use `status` to restart work.
- DO NOT treat an export as a new canonical survey version.
- DO NOT add create, update, or delete as separate public commands.
