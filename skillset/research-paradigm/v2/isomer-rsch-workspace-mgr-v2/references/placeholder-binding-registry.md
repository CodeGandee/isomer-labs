# Placeholder Binding Registry

## Workflow

1. Collect the active v2 skill placeholder rows from each skill's `migrate/placeholders.md`.
2. Normalize each row by skill name, placeholder name, kind, producer, consumer, semantic meaning, and storage-binding status.
3. Route by kind first. Use the v2 storage item mapping for `evidence`, `report`, `handoff`, `decision`, `runtime state`, `draft`, `run record`, `figure`, and `code`.
4. Preserve the exact placeholder name as queryable metadata. Do not rename another skill's placeholder unless this manager is explicitly repairing inconsistent migration material.
5. Produce <RSCH_PLACEHOLDER_BINDING_REGISTRY> with binding status values such as available, planned, custom-needed, blocked, or deferred.

If the user's task does not map cleanly to these steps, use your native planning tool to build a partial registry for the selected skill or route, then state which skills remain unchecked.

## Binding Rules

- Placeholder kind is the first routing signal.
- Placeholder name is semantic metadata, not a directory name.
- Producer and consumer must remain visible so handoffs can be audited.
- Missing storage support becomes a blocker or deferred binding, not a hidden path convention.
- `isomer-rsch-shared-v2` owns vocabulary consistency; this manager owns the post-specialization binding pass.

## Minimum Registry Columns

| Field | Meaning |
| --- | --- |
| skill | The v2 skill that defines the placeholder. |
| placeholder | The exact placeholder token. |
| kind | The placeholder kind from the skill registry. |
| semantic target | The intended semantic item class or label group. |
| producer | The skill or actor expected to produce the object. |
| consumer | The skill, actor, or route expected to consume the object. |
| binding status | Available, planned, custom-needed, blocked, or deferred. |
| note | Caveat, blocker, or validation detail. |
