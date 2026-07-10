# Register External Local Datasets by Manifest and Link

Status: accepted

When a user provides a local dataset directory for possible later use, Isomer shall register it in the selected Topic Workspace through a topic-local Dataset Registration and a managed symlink rather than copying or moving the data. A machine-readable Topic Dataset Manifest provides stable discovery and metadata; the symlink is only an operational locator and never the dataset's sole identity.

## Considered Options

- Copy every user dataset into the Topic Workspace. This was rejected because datasets may be large, copying wastes storage, and ownership would become ambiguous.
- Record only the external filesystem path. This was rejected because paths are mutable, hard to discover consistently, and insufficient for identity, provenance, description, or staleness checks.
- Register the external directory itself as a `custom.datasets.*` semantic path. This was rejected because current Workspace Path Resolution expects topic-scoped semantic surfaces to resolve inside the Topic Workspace or Project trust boundary.
- Create an unrecorded symlink and rely on directory inspection. This was rejected because later agents could not distinguish managed data from incidental files or know whether the target moved or changed.

## Consequences

- The operator-owned registry root uses a topic-local custom semantic label such as `custom.datasets.registry`, normally backed by a durable `topic_records_dir` surface. Managed dataset links live below that root, for example under `links/<dataset-id>`; the external target is not itself a semantic surface binding.
- Each Dataset Registration records a stable `dataset_id`, name, description, aliases or tags, external source locator, workspace link locator, registration time and actor, access posture, license or sensitivity notes, availability, format and schema observations, version information when known, and a bounded fingerprint or staleness policy.
- The external directory remains user-owned and authoritative. Registration does not copy, move, rewrite, delete, or grant write authority over the target. `read-only` is an advisory Isomer access posture unless filesystem permissions enforce it.
- Symlink creation and manifest mutation belong to the Project Operator Session, Topic Service Master, or `isomer-op-topic-mgr` owner route. Kaoju requests and consumes the registration but does not bypass Topic Workspace topology and provenance ownership.
- The specialized registration is an explicit trust exception for a user-approved external local directory. Validation records the lexical path, resolved target, link path, and safety checks; general semantic paths and arbitrary Agent Workspace links remain subject to their existing containment rules.
- Before asking the user for a dataset or planning a new download, Kaoju framing, acquisition, method-trial, and empirical-comparison workflows query the Topic Dataset Manifest. A matching registration is reused only after availability, fingerprint, access, task, schema, split, license, and evaluator compatibility are checked.
- A moved, missing, or changed target becomes `unavailable` or `stale`; it is not silently trusted. Removing a registration unlinks only the managed link and updates the manifest, never deletes the external target.
- Worker access is exposed only through an approved topic-owned read-only projection, execution input binding, or service route when a Run needs it. The Topic Dataset Manifest remains the discovery authority.
