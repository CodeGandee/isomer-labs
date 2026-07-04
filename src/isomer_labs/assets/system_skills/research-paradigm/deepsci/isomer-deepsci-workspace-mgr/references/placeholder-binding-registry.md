# Placeholder Binding Registry

## Workflow

1. Collect the active production DeepSci skill placeholder rows from each skill's `migrate/placeholders.md`.
2. Read the same skill's `placeholder-bindings.md` to recover storage item class, record kind, default semantic label, profile, accepted research artifact command shape, and Topic Actor or formal agent metadata guidance.
3. Read or create the topic-level placeholder binding index as readiness evidence, but use skill-local `placeholder-bindings.md` rows as authority.
4. Normalize each row by skill name, placeholder name, kind, producer, consumer, semantic meaning, semantic target, profile, command shape, metadata guidance, and storage-binding status.
5. Route by kind first. Use the production DeepSci storage item mapping for `evidence`, `report`, `handoff`, `decision`, `runtime state`, `draft`, `run record`, `figure`, and `code`.
6. Preserve the exact placeholder name as queryable metadata. Do not rename another skill's placeholder unless this manager is explicitly repairing inconsistent migration material.
7. Produce <RSCH_PLACEHOLDER_BINDING_REGISTRY> with binding status values such as available, planned, custom-needed, blocked, or deferred.

If the user's task does not map cleanly to these steps, use your native planning tool to build a partial registry for the selected skill or route, then state which skills remain unchecked.

## Binding Rules

- Placeholder kind is the first routing signal.
- Placeholder name is semantic metadata, not a directory name.
- `placeholder-bindings.md` is the local binding authority for the current extension-backed accepted research artifact command shape.
- Topic Actor runs should add `--topic-actor`, `--actor-kind`, `--runtime-kind`, and `--controller-kind` when creating or updating accepted records.
- Formal team runs should supply real Agent Team Instance, Agent Instance, or Agent Workspace refs only when the record was actually produced inside that formal context.
- Producer and consumer must remain visible so handoffs can be audited.
- Missing storage support becomes a blocker or deferred binding, not a hidden path convention.
- `isomer-deepsci-shared` owns vocabulary consistency; this manager owns the post-specialization binding pass.

## Minimum Registry Columns

| Field | Meaning |
| --- | --- |
| skill | The production DeepSci skill that defines the placeholder. |
| placeholder | The exact placeholder token. |
| kind | The placeholder kind from the skill registry. |
| semantic target | The intended semantic item class or label group. |
| producer | The skill or actor expected to produce the object. |
| consumer | The skill, actor, or route expected to consume the object. |
| record kind | The Workspace Runtime lifecycle record kind used by the current binding. |
| default label | The semantic workspace label used for body storage. |
| profile | The artifact or record profile attached to created records. |
| command shape | The current accepted research artifact command shape, such as `isomer-cli ext research records`, or the future command family when upgraded. |
| metadata guidance | Topic Actor metadata or formal agent metadata to supply for the selected topology. |
| binding status | Available, planned, custom-needed, blocked, or deferred. |
| note | Caveat, blocker, or validation detail. |
