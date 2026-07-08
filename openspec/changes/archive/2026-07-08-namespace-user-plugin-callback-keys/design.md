## Context

User Skill Callback registries already store an array of callback records and resolve multiple active callbacks for the same target skill and stage. Registration currently upserts by callback id, and validation rejects duplicate active ids. That is enough for hand-written callback registrations, but user-plugin manifests need a clearer contract: many plugins may target the same extension point, and plugin authors should not coordinate global ids with each other.

The GPU analytical-modeling plugin already uses stable callback ids in its manifest, but the manifest is not yet a runtime contract. This change replaces broad manifest `id` usage with explicit `plugin_id` and callback `key` fields, then makes the plugin identity and callback key model executable through installer behavior.

## Goals / Non-Goals

**Goals:**

- Let multiple user plugins target the same callback extension point without overwriting each other.
- Require plugin authors to manage only plugin-local callback key uniqueness.
- Use a required manifest `plugin_id` field as the stable plugin identity string.
- Derive a stable installed callback key as `<plugin_id>:<plugin-local-key>`.
- Restrict plugin-local callback keys to ASCII letters, digits, `-`, `_`, and `/`, with `/` recommended for hierarchy-like naming.
- Reject ambiguous unlabeled duplicate callbacks inside one plugin.
- Guarantee ordering inside a plugin by Python string comparison ascending order on plugin-local keys.
- Keep cross-plugin ordering deterministic for implementation stability but not exposed as a user-facing guarantee.

**Non-Goals:**

- Do not make user plugins packaged system skills or part of the distributed skill inventory.
- Do not introduce dependency ordering between different plugins.
- Do not make callback priority a user-facing plugin ordering mechanism.
- Do not keep broad manifest `id` as a supported alias for `plugin_id` or callback `key`.
- Do not allow callback material to override the owning system skill, current user request, or existing callback authority rules.

## Decisions

1. **Use `plugin_id` plus plugin-local keys.** A user-plugin manifest has a required top-level `plugin_id`. A manifest callback entry has a plugin-local `key`. If `key` is present, that exact string is the local key after validation. If absent, the local key is the canonical extension point key, initially `<target_skill>/<stage>`. The installed callback key stored in the callback registry is always `<plugin_id>:<local-key>`. This keeps plugin manifests readable while preserving global uniqueness in the installed registry.

Alternative considered: use top-level `id` and callback `id` fields. That is close to the existing local plugin file, but `id` is too broad in a manifest that has both plugin identity and callback identity. The explicit names `plugin_id` and `key` make the contract harder to misread.

2. **Reject duplicate local keys within one plugin.** During manifest validation or install planning, the system rejects two callbacks from the same plugin that produce the same local key. This includes two unlabeled callbacks for the same extension point, because both derive the same `<target_skill>/<stage>` key. The plugin author can still place multiple callbacks on one extension point by giving them explicit distinct keys.

Alternative considered: append numeric suffixes to derived keys. That would hide ordering and make repeated installs less predictable.

3. **Keep registry upsert keyed by installed callback key.** The installed registry remains a list of callback records. Installing a plugin callback writes or replaces only the record with the same installed key. Another plugin targeting the same extension point has a different installed key because its `plugin_id` differs, so both callbacks coexist and resolve together.

Alternative considered: key registry records by `(target_skill, stage)`. That would recreate the single-slot overwrite problem and conflict with the existing multi-callback resolution model.

4. **Order plugin callbacks by string comparison only inside a plugin.** Plugin-installed callbacks use equal callback priority. For callbacks from one plugin that match the same extension point, user-visible order is ascending Python `str` comparison on the plugin-local key. Cross-plugin ordering may use installed keys or another deterministic internal sort, but documentation and CLI output must not promise relative order between different plugins.

Alternative considered: keep user-facing numeric priorities for plugin manifests. Priorities create a false promise of cross-plugin coordination and make independent plugin composition harder to reason about.

5. **Constrain local keys and allow colon only as the namespace separator.** Plugin-local keys may contain only ASCII letters, digits, `-`, `_`, and `/`. The registry validation must accept one colon separator for installed keys such as `gpu-analytical-modeling:isomer-deepsci-scout/begin`. Plugin-local keys cannot contain `:`, so installed key parsing remains unambiguous.

Alternative considered: encode the separator as a dash or underscore. Those characters are already allowed inside plugin-local keys, so a colon makes the namespace boundary more visible.

6. **Install through the existing callback command group.** The installer surface belongs under `project skill-callbacks install --plugin-dir <path>` because the first supported user-plugin kind is a callback bundle, not a general provider package manager. The command should support the same Project discovery, topic selection, scope, and JSON output conventions as existing callback commands.

Alternative considered: introduce `project user-plugins install`. That may become useful once user plugins cover more than callbacks, but it would overstate the current scope.

7. **Store plugin metadata for installed callbacks.** Callback registry records installed from a user-plugin manifest should include optional `plugin_id` and `plugin_key` metadata in addition to the installed callback key. Resolution still keys by the installed callback id, but metadata improves diagnostics, list output, uninstall planning, and replace checks.

Alternative considered: derive all plugin metadata by splitting the installed callback key. That works for simple output, but it loses source intent and makes future migration harder.

8. **Require explicit replacement for same `plugin_id` from a different source.** If an install sees the same `plugin_id` from another plugin directory or source identity, it should reject by default and require an explicit replace flag. Reinstalling the same plugin source can update installed keys.

Alternative considered: always treat matching `plugin_id` as an update. That is convenient but makes accidental shadowing of a project-local plugin too easy.

## Risks / Trade-offs

- **Risk: Existing callback priority semantics conflict with plugin order expectations.** → Mitigation: plugin-installed callbacks use equal priority and plugin docs state that in-plugin order is key-based; direct hand-written callbacks can keep existing priority behavior.
- **Risk: Two plugin directories use the same `plugin_id`.** → Mitigation: treat `plugin_id` as the plugin identity and reject different-source replacement unless the user passes an explicit replace flag.
- **Risk: Cross-plugin ordering still appears in JSON output.** → Mitigation: return deterministic output for reproducibility, but phrase docs and specs so users cannot depend on one plugin running before another.
- **Risk: Namespaced ids affect prompt file names.** → Mitigation: store the installed key in registry metadata while percent-encoding managed prompt filenames when the raw installed key is not filesystem-safe.
