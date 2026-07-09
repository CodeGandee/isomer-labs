# Bind Only After Houmao Entities Exist

Status: accepted

The Topic Workspace Manifest binding means the Topic Workspace is bound to concrete Houmao Topic Service Master entities. Isomer will compute suggested names before preparation, but it will write the binding only after the Houmao-owned preparation procedure reports created or updated entities.

## Considered Options

- Write no binding until Houmao preparation succeeds.
- Write a `planned` binding before calling Houmao.
- Write a `planned` binding only after an intermediate preparation checkpoint.

## Consequences

`planned`, `blocked`, and `skipped` are command or readiness outcomes, not Topic Workspace Manifest binding statuses. Retry and repair workflows recompute suggested names from the Topic Workspace id when no binding exists.
