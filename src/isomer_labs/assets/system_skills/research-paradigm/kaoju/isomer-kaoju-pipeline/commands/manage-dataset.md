# Manage Dataset

## Workflow

1. **Select an action**. Accept exactly one of `register`, `list`, `show`, `refresh`, or `remove` and resolve the Topic Workspace.
2. **Inspect current manifest state**. Query `kaoju:topic-dataset-manifest` with `project artifacts latest`; report scope ambiguity rather than choosing by timestamp or scanning files. Validate the selected entry or candidate source without mutation.
3. **Route material mutations**. For `register`, `refresh`, or `remove`, send external inspection and managed-link mutation to the Topic Workspace owner. Never mutate the external target.
4. **Revise the manifest**. Consume the owner's immutable locator, managed-link, file, actor, and provenance refs; validate a new canonical payload and run typed `project artifacts revise` for `kaoju:topic-dataset-manifest`. Let the binding registry supply the record kind, profile, label, scope, and managed path. Preserve the prior version.
5. **Validate and return**. Check dataset id, locators, observed metadata, fingerprint or staleness policy, access, license, provenance, owner result, latest posture, and what later empirical stages may reuse.

If the request does not map cleanly to these actions, use the native planning tool to build and execute a bounded dataset-management plan without modifying the external dataset.

## Actions

| Action | Behavior |
| --- | --- |
| `register` | Assign a stable dataset id, ask the owner for the managed link, then revise the manifest with name, description, external source, managed locator, access, license, observed metadata, fingerprint or staleness policy, actor, and provenance. |
| `list` | Query the latest canonical manifest and list entries with id, name, summary, availability, fingerprint posture, and access state. |
| `show` | Show the canonical manifest payload and selected entry, then query lineage for exact locators, compatibility metadata, history, and staleness state. |
| `refresh` | Ask the owner to reinspect identity and metadata, then revise the manifest while preserving the prior fingerprint and observation. |
| `remove` | Ask the owner to remove only the managed link, then revise registration state as unavailable or removed; never alter or delete the external target. |

## Reuse Contract

Method trials and empirical comparisons query this manifest before asking the user for data or proposing acquisition. Reuse requires availability, fingerprint, access, task, schema, split, evaluator, and license compatibility; a matching name or path is insufficient.

## Guardrails

- DO NOT copy or move the external dataset during registration.
- DO NOT refresh a mutable path without preserving the previous fingerprint.
- DO NOT remove the external target rather than the managed link and registration.
