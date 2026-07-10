# Manage Survey

## Workflow

1. **Select an action**. Accept exactly one of `list`, `show`, `status`, or `export` plus the Research Topic or survey ref required by that action.
2. **Resolve current state**. Use Workspace Path Resolution and canonical bound records; do not infer state from stale prompt memory or rendered files.
3. **Execute the action**. Apply the action contract below without changing evidence meaning, audit state, or lineage.
4. **Return results**. Report selected refs, current status, diagnostics, or export destination and provenance.

If the request does not map cleanly to these actions, use the native planning tool to build and execute a bounded read or export plan without inventing another manager action.

## Actions

| Action | Behavior |
| --- | --- |
| `list` | Run `isomer-cli --print-json ext research records query list --topic <topic> --artifact-family kaoju` with optional exact `--semantic-id`, `--procedure`, status, profile, and `--latest-only`; return stable id, title, summary, semantic id, revision posture, procedure, terminal status, validation state, and detail locator. |
| `show` | Run `isomer-cli --print-json ext research records show --topic <topic> <record-id> --include-payload`, then use `records query lineage` for accepted inputs, history, blockers, audit posture, and related outputs. |
| `status` | Query `kaoju:survey-terminal-report` and the requested procedure with `--latest-only`, then inspect lineage. Report every competing latest candidate as ambiguity; never select by timestamp alone. |
| `export` | Run `records render <record-id>` or `records render <record-id> --output-file <authorized-export-path>` through the recorded profile. Preserve source id and payload digest as export provenance without changing latest state. |

## Inputs and Outputs

`list` needs a resolved Research Topic. `show` and `status` need one stable record or procedure ref. `export` also needs the requested representation and destination authority. All actions are read-only except the explicit export file; none revise canonical content, evidence, lineage, or latest identity.

Export does not create new survey evidence or change an Audit Report. If the destination requires a Topic Workspace mutation or external side effect, route it to the applicable owner and Gate.

## Common Mistakes

- Using `status` to restart work. Return the resume context instead.
- Treating an export as a new canonical survey version.
- Adding create, update, or delete as separate public commands.
