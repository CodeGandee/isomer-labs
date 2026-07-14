# Manage Survey

## Workflow

1. **Select an action**. Accept exactly one of `list`, `show`, `status`, or `export` plus the Research Topic or survey ref required by that action.
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

## Common Mistakes

- Using `status` to restart work. Return the resume context instead.
- Treating an export as a new canonical survey version.
- Adding create, update, or delete as separate public commands.
