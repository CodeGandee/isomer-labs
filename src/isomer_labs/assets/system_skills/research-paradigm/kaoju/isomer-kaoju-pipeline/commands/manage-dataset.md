# Manage Dataset

## Workflow

1. **Select an action**. Accept exactly one of `register`, `list`, `show`, `refresh`, or `remove` and resolve the Topic Workspace.
2. **Inspect current manifest state**. Read the Topic Dataset Manifest and validate the selected entry or candidate source without mutating it.
3. **Route mutations**. For `register`, `refresh`, or `remove`, send the managed-link and manifest operation to the Topic Workspace owner and retain its returned refs.
4. **Validate the result**. Check dataset id, external and managed locators, observed metadata, fingerprint or staleness policy, access, license, and provenance.
5. **Return results**. Report action status, manifest ref, affected entry, blockers, and what later empirical stages may reuse.

If the request does not map cleanly to these actions, use the native planning tool to build and execute a bounded dataset-management plan without modifying the external dataset.

## Actions

| Action | Behavior |
| --- | --- |
| `register` | Assign a stable dataset id, create an owner-governed managed link, and record name, description, external source, managed locator, access, license, observed metadata, fingerprint or staleness policy, and provenance. |
| `list` | List registered datasets with id, name, summary, availability, fingerprint posture, and access state. |
| `show` | Show one manifest entry, exact locators, compatibility metadata, lineage, and staleness state. |
| `refresh` | Reinspect external identity and metadata through the owner; record drift as a new observation rather than overwriting old evidence silently. |
| `remove` | Remove only the managed link and registration state through the owner; never alter or delete the external target. |

## Reuse Contract

Method trials and empirical comparisons query this manifest before asking the user for data or proposing acquisition. Reuse requires availability, fingerprint, access, task, schema, split, evaluator, and license compatibility; a matching name or path is insufficient.

## Common Mistakes

- Copying or moving the external dataset during registration.
- Refreshing a mutable path without preserving the previous fingerprint.
- Removing the external target rather than the managed link and registration.
