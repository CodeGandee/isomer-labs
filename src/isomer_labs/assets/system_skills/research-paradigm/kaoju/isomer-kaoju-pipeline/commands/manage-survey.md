# Manage Survey

## Workflow

1. **Select an action**. Accept exactly one of `list`, `show`, `status`, or `export` plus the Research Topic or survey ref required by that action.
2. **Resolve current state**. Use Workspace Path Resolution and existing research-recording or Artifact interfaces; do not infer state from stale prompt memory.
3. **Execute the action**. Apply the action contract below without changing evidence meaning, audit state, or lineage.
4. **Return results**. Report selected refs, current status, diagnostics, or export destination and provenance.

If the request does not map cleanly to these actions, use the native planning tool to build and execute a bounded read or export plan without inventing another manager action.

## Actions

| Action | Behavior |
| --- | --- |
| `list` | List survey Artifacts visible in the resolved Topic Workspace with id, title, summary, version, procedure, and terminal status. |
| `show` | Show one survey Artifact, its accepted inputs, audit posture, lineage, and related output refs. |
| `status` | Summarize procedure state, stage outcomes, blockers, Gates, resource posture, and resume point from durable refs. |
| `export` | Render or copy an existing accepted survey view into a requested representation while recording source refs and export provenance. |

## Inputs and Outputs

`list` needs a resolved Research Topic. `show` and `status` need one stable survey or procedure ref. `export` also needs the requested representation and destination authority. Structured entries use non-empty top-level `title` and `summary`.

Export does not create new survey evidence or change an Audit Report. If the destination requires a Topic Workspace mutation or external side effect, route it to the applicable owner and Gate.

## Common Mistakes

- Using `status` to restart work. Return the resume context instead.
- Treating an export as a new canonical survey version.
- Adding create, update, or delete as separate public commands.
