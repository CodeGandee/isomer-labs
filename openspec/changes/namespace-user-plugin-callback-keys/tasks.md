## 1. Callback Key Foundation

- [ ] 1.1 Update User Skill Callback id validation to accept the colon namespace separator for installed user-plugin callback keys while preserving the existing allowed character checks for each side of the separator.
- [ ] 1.2 Keep duplicate active callback diagnostics keyed by the full installed callback key, including namespaced keys.
- [ ] 1.3 Ensure managed prompt-file paths created from namespaced callback keys use a filesystem-safe filename when the raw installed key is not safe for the target platform.
- [ ] 1.4 Add unit tests that namespaced callback ids validate, duplicate active namespaced ids are rejected, and distinct namespaced ids on the same target skill and stage resolve together.

## 2. User Plugin Manifest Parsing

- [ ] 2.1 Add a user-plugin callback manifest parser for `schema_version = "isomer-user-plugin.v1"` and `kind = "user-skill-callback-bundle"`.
- [ ] 2.2 Treat the manifest `id` as the stable plugin identity string used in installed callback keys.
- [ ] 2.3 Parse each callback entry's explicit plugin-local `key` when present.
- [ ] 2.4 Derive the plugin-local key from the canonical extension point name `<target_skill>.<stage>` when `key` is absent.
- [ ] 2.5 Validate that effective plugin-local keys are unique inside one plugin.
- [ ] 2.6 Reject two unlabeled callbacks for the same `target_skill` and `stage` with a deterministic diagnostic.
- [ ] 2.7 Validate callback source entries against the existing source union of `skill_dir`, `prompt_file`, and inline `prompt`, resolving relative paths from the plugin root.

## 3. Plugin Callback Installation

- [ ] 3.1 Add a project CLI install surface for user-plugin callback manifests under `project skill-callbacks`, including explicit plugin path, scope, topic selection, and JSON output.
- [ ] 3.2 Convert each manifest callback entry into an installed callback key `<plugin-id>:<plugin-local-key>`.
- [ ] 3.3 Install callbacks by upserting only records with the same installed callback key and preserving other records for the same extension point.
- [ ] 3.4 Report plugin id, plugin-local key, installed callback key, target skill, stage, scope, source summary, and diagnostics in install output.
- [ ] 3.5 Add integration-style CLI tests that two plugins can install callbacks for the same extension point without overwriting each other.
- [ ] 3.6 Add tests that one plugin can install multiple callbacks for the same extension point only when the entries have distinct explicit keys.

## 4. Ordering Contract

- [ ] 4.1 Implement in-plugin callback ordering by ascending Python string comparison of plugin-local keys when planning or reporting callbacks from one plugin.
- [ ] 4.2 Keep cross-plugin output deterministic without documenting or testing a user-facing relative order between different plugins.
- [ ] 4.3 Remove or de-emphasize numeric callback priority from user-plugin manifest examples so users do not treat priority as plugin ordering.
- [ ] 4.4 Add tests for in-plugin ordering with keys such as `a`, `b`, and `z`.

## 5. Local Plugin and Documentation Updates

- [ ] 5.1 Update `skillset/user-plugins/gpu-analytical-modeling/manifest.toml` to use plugin-local callback `key` values that install as `gpu-analytical-modeling:<key>`.
- [ ] 5.2 Update the GPU analytical-modeling plugin README to describe the plugin-local key rule, derived extension point keys, and duplicate unlabeled extension point rejection.
- [ ] 5.3 Update callback or CLI documentation to state that cross-plugin ordering is an implementation detail and only in-plugin order is user-facing.

## 6. Validation

- [ ] 6.1 Run `openspec validate namespace-user-plugin-callback-keys --strict`.
- [ ] 6.2 Run `pixi run test`.
- [ ] 6.3 Run focused CLI smoke tests for plugin install, callback resolution, callback list, and callback disable with namespaced keys.
