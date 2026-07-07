## 1. Callback Key Foundation

- [x] 1.1 Update User Skill Callback id validation to accept exactly one colon namespace separator for installed user-plugin callback keys while preserving bounded character checks for `plugin_id` and plugin-local `key`.
- [x] 1.2 Keep duplicate active callback diagnostics keyed by the full installed callback key, including namespaced keys.
- [x] 1.3 Ensure managed prompt-file paths created from namespaced callback keys use percent-encoded filenames when the raw installed key is not safe for the target platform.
- [x] 1.4 Add unit tests that namespaced callback ids validate, duplicate active namespaced ids are rejected, and distinct namespaced ids on the same target skill and stage resolve together.

## 2. User Plugin Manifest Parsing

- [x] 2.1 Add a user-plugin callback manifest parser for `schema_version = "isomer-user-plugin.v1"` and `kind = "user-skill-callback-bundle"`.
- [x] 2.2 Require manifest `plugin_id` as the stable plugin identity string used in installed callback keys and reject broad top-level `id` as an identity alias.
- [x] 2.3 Parse each callback entry's explicit plugin-local `key` when present.
- [x] 2.4 Reject callback entry `id` as a `key` alias with a deterministic diagnostic.
- [x] 2.5 Validate plugin-local `key` values so they contain only ASCII letters, ASCII digits, `-`, `_`, and `/`, and document `/` as naming hierarchy only.
- [x] 2.6 Derive the plugin-local key from the canonical extension point name `<target_skill>/<stage>` when `key` is absent.
- [x] 2.7 Validate that effective plugin-local keys are unique inside one plugin.
- [x] 2.8 Reject two unlabeled callbacks for the same `target_skill` and `stage` with a deterministic diagnostic.
- [x] 2.9 Validate callback source entries against the existing source union of `skill_dir`, `prompt_file`, and inline `prompt`, resolving relative paths from the plugin root.

## 3. Plugin Callback Installation

- [x] 3.1 Add `project skill-callbacks install --plugin-dir <path>` for user-plugin callback manifests, including scope, topic selection, explicit replace behavior, and JSON output.
- [x] 3.2 Convert each manifest callback entry into an installed callback key `<plugin_id>:<plugin-local-key>`.
- [x] 3.3 Install callbacks by upserting only records with the same installed callback key and preserving other records for the same extension point.
- [x] 3.4 Store optional plugin metadata fields for `plugin_id` and plugin-local key on callback records installed from manifests.
- [x] 3.5 Reject installing a different plugin source with the same `plugin_id` unless the command passes an explicit replace flag.
- [x] 3.6 Report `plugin_id`, plugin-local key, installed callback key, target skill, stage, scope, source summary, and diagnostics in install output.
- [x] 3.7 Add integration-style CLI tests that two plugins can install callbacks for the same extension point without overwriting each other.
- [x] 3.8 Add tests that one plugin can install multiple callbacks for the same extension point only when the entries have distinct explicit keys.
- [x] 3.9 Add tests that a different plugin source with the same `plugin_id` is rejected without explicit replace.

## 4. Ordering Contract

- [x] 4.1 Install manifest callbacks with equal callback priority so in-plugin callback ordering follows ascending Python string comparison of plugin-local keys.
- [x] 4.2 Keep cross-plugin output deterministic without documenting or testing a user-facing relative order between different plugins.
- [x] 4.3 Remove or de-emphasize numeric callback priority from user-plugin manifest examples so users do not treat priority as plugin ordering.
- [x] 4.4 Add tests for in-plugin ordering with keys such as `a`, `b`, and `group/z`.

## 5. Local Plugin and Documentation Updates

- [x] 5.1 Update `skillset/user-plugins/gpu-analytical-modeling/manifest.toml` to use top-level `plugin_id` and plugin-local callback `key` values that install as `gpu-analytical-modeling:<key>`.
- [x] 5.2 Update the GPU analytical-modeling plugin README to describe the plugin-local key rule, derived extension point keys, and duplicate unlabeled extension point rejection.
- [x] 5.3 Update callback or CLI documentation to state that cross-plugin ordering is an implementation detail and only in-plugin order is user-facing.

## 6. Validation

- [x] 6.1 Run `openspec validate namespace-user-plugin-callback-keys --strict`.
- [x] 6.2 Run `pixi run test`.
- [x] 6.3 Run focused CLI smoke tests for plugin install, callback resolution, callback list, and callback disable with namespaced keys.
