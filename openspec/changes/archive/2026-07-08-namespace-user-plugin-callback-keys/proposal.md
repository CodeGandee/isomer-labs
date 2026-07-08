## Why

User-plugin callback manifests need a stable way to compose multiple plugins that target the same skill callback extension point. The current callback registry already resolves multiple callbacks, but plugin installation needs an explicit key contract so entries from different plugins do not overwrite each other and users only manage local keys inside one plugin.

## What Changes

- Define user-plugin manifests with a required `plugin_id` field instead of a broad top-level `id` field.
- Define user-plugin callback keys as plugin-local strings, either explicitly provided by the plugin author or derived from the extension point name.
- Restrict plugin-local callback keys to letters, digits, `-`, `_`, and `/`; advise `/` as a naming hierarchy separator only.
- Define installed callback keys as `<plugin_id>:<key>`, so global uniqueness is owned by Isomer Labs rather than by plugin authors.
- Forbid a plugin from registering multiple callbacks into the same extension point without explicit keys, because unlabeled callbacks would derive the same plugin-local key.
- Define callback ordering as ascending Python string comparison of plugin-local callback keys, with user-facing order guarantees only within one plugin.
- Treat cross-plugin ordering as deterministic implementation detail and not as a user-facing API.
- Update callback key validation so installed keys can use the colon separator.
- Install plugin manifest callbacks through `project skill-callbacks install --plugin-dir`, using equal callback priority for plugin-installed callbacks so plugin order is key-based.

## Capabilities

### New Capabilities

- `user-plugin-callback-manifests`: Defines how user-plugin manifests declare callback keys, derive installed callback keys, reject ambiguous unlabeled duplicates, and expose ordering guarantees.

### Modified Capabilities

- `user-skill-callbacks`: Allows installed callback keys with plugin namespace separators and preserves multi-callback resolution keyed by global callback key, not by extension point.

## Impact

- Affected specs: `user-plugin-callback-manifests`, `user-skill-callbacks`.
- Affected code: callback id validation, plugin manifest parsing and install support, callback registration/upsert behavior, prompt filename handling, callback metadata serialization, and tests for multiple plugins targeting the same extension point.
- Affected data: installed callback registries may contain ids such as `gpu-analytical-modeling:isomer-deepsci-scout/begin`.
