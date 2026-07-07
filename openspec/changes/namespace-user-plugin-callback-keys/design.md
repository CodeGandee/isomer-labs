## Context

User Skill Callback registries already store an array of callback records and resolve multiple active callbacks for the same target skill and stage. Registration currently upserts by callback id, and validation rejects duplicate active ids. That is enough for hand-written callback registrations, but user-plugin manifests need a clearer contract: many plugins may target the same extension point, and plugin authors should not coordinate global ids with each other.

The GPU analytical-modeling plugin already uses stable callback ids in its manifest, but the manifest is not yet a runtime contract. This change makes the plugin identity and callback key model explicit before adding broader installer behavior.

## Goals / Non-Goals

**Goals:**

- Let multiple user plugins target the same callback extension point without overwriting each other.
- Require plugin authors to manage only plugin-local callback key uniqueness.
- Derive a stable installed callback key as `<plugin-name>:<plugin-local-key>`, where `<plugin-name>` is the stable plugin identity string.
- Reject ambiguous unlabeled duplicate callbacks inside one plugin.
- Guarantee ordering inside a plugin by Python string comparison ascending order on plugin-local keys.
- Keep cross-plugin ordering deterministic for implementation stability but not exposed as a user-facing guarantee.

**Non-Goals:**

- Do not make user plugins packaged system skills or part of the distributed skill inventory.
- Do not introduce dependency ordering between different plugins.
- Do not make callback priority a user-facing plugin ordering mechanism.
- Do not allow callback material to override the owning system skill, current user request, or existing callback authority rules.

## Decisions

1. **Use plugin-local keys plus an installed namespace.** A manifest callback entry has a plugin-local `key`. If present, that exact string is the local key. If absent, the local key is the canonical extension point name, initially `<target_skill>.<stage>`. The installed callback key stored in the callback registry is always `<plugin-name>:<local-key>`, where `<plugin-name>` is the stable plugin identity string, such as manifest `id`. This keeps plugin manifests readable while preserving global uniqueness in the installed registry.

Alternative considered: require every plugin author to provide globally unique callback ids. That would work mechanically, but it pushes cross-plugin coordination to users and makes copyable project-local plugins brittle.

2. **Reject duplicate local keys within one plugin.** During manifest validation or install planning, the system rejects two callbacks from the same plugin that produce the same local key. This includes two unlabeled callbacks for the same extension point, because both derive the same `<target_skill>.<stage>` key. The plugin author can still place multiple callbacks on one extension point by giving them explicit distinct keys.

Alternative considered: append numeric suffixes to derived keys. That would hide ordering and make repeated installs less predictable.

3. **Keep registry upsert keyed by installed callback key.** The installed registry remains a list of callback records. Installing a plugin callback writes or replaces only the record with the same installed key. Another plugin targeting the same extension point has a different installed key because its plugin name differs, so both callbacks coexist and resolve together.

Alternative considered: key registry records by `(target_skill, stage)`. That would recreate the single-slot overwrite problem and conflict with the existing multi-callback resolution model.

4. **Order plugin callbacks by string comparison only inside a plugin.** For callbacks from one plugin that match the same extension point, user-visible order is ascending Python `str` comparison on the plugin-local key. Cross-plugin ordering may use installed keys or another deterministic internal sort, but documentation and CLI output must not promise relative order between different plugins.

Alternative considered: keep user-facing numeric priorities for plugin manifests. Priorities create a false promise of cross-plugin coordination and make independent plugin composition harder to reason about.

5. **Allow colon in installed callback ids.** The registry validation must accept `:` so installed keys such as `gpu-analytical-modeling:isomer-deepsci-scout.begin` are valid. Any managed prompt path derived from a callback key should use a filesystem-safe representation if needed by the target platform.

Alternative considered: encode the separator as a dash or dot. Those characters are already common inside plugin names and local keys; a colon makes the namespace boundary visible.

## Risks / Trade-offs

- **Risk: Existing callback priority semantics conflict with plugin order expectations.** → Mitigation: document that plugin manifest order is key-based and scoped to callbacks from the same plugin; direct hand-written callbacks can keep existing fields unless the implementation intentionally migrates them.
- **Risk: Two plugin directories use the same plugin name.** → Mitigation: treat plugin name as the plugin identity and reject duplicate installed keys during validation or install unless the operation is an explicit update of the same plugin.
- **Risk: Cross-plugin ordering still appears in JSON output.** → Mitigation: return deterministic output for reproducibility, but phrase docs and specs so users cannot depend on one plugin running before another.
- **Risk: Colon in ids affects prompt file names.** → Mitigation: store the installed key in registry metadata while sanitizing managed prompt filenames when the platform requires it.
