## Why

The extension package concept has outgrown the old name: it now carries callback manifests, runtime parameter defaults, and project/topic specialization rather than behaving like a narrow plugin hook. Isomer should use the single public and durable term **Toolbox** across CLI commands, TOML schema, specs, docs, examples, and code-visible data contracts.

## What Changes

- **BREAKING** Replace User Plugin terminology with Toolbox terminology everywhere in current product language, persisted manifests, command names, schema versions, JSON keys, docs, OpenSpec specs, tests, and examples.
- **BREAKING** Replace Project Manifest and Topic Workspace Manifest tables with `[[toolboxes]]`, `[[toolbox_runtime_param_imports]]`, and `[[toolbox_runtime_params]]`.
- **BREAKING** Replace durable identity fields such as `plugin_id`, `plugin_key`, and plugin source metadata with Toolbox equivalents such as `toolbox_id`, toolbox-local keys, and toolbox source metadata.
- **BREAKING** Replace `project user-plugins` with `project toolboxes`, and replace `project user-plugin-params` with `project toolbox-params`.
- **BREAKING** Replace callback install option `--plugin-dir` with `--toolbox-dir`.
- **BREAKING** Replace toolbox manifest schema names with `isomer-toolbox.v1` and `isomer-toolbox-runtime-params.v1`.
- **BREAKING** Move project-local Toolbox examples from `skillset/user-plugins/` to `skillset/toolboxes/`.
- Remove old public names rather than adding deprecated aliases; this change intentionally does not preserve the former concept name in current behavior or documentation.

## Capabilities

### New Capabilities

- `toolbox-callback-manifests`: Defines Toolbox callback manifest identity, installed callback key derivation, install semantics, ordering, and runtime parameter declarations.
- `toolbox-runtime-configuration`: Defines Toolbox registration, enablement, scoped runtime parameter CRUD, import defaults, and effective value resolution.
- `gpu-analytical-modeling-toolbox`: Defines the project-local GPU analytical modeling Toolbox package and its expected location under `skillset/toolboxes/`.

### Modified Capabilities

- `user-plugin-callback-manifests`: Remove the old capability contract in favor of Toolbox callback manifests.
- `user-plugin-runtime-configuration`: Remove the old capability contract in favor of Toolbox runtime configuration.
- `user-skill-callbacks`: Change callback registry metadata, install option naming, resolution gating, and JSON output from plugin terminology to Toolbox terminology.
- `topic-workspace-manifest`: Change topic-scope extension configuration tables and JSON output from plugin terminology to Toolbox terminology.
- `gpu-analytical-modeling-skill-guidance`: Change the guidance package location and language to Toolbox.
- `gpu-experiment-evidence-gates`: Change the evidence-gate guidance package location and language to Toolbox.
- `gpu-reference-map-skill`: Change references to the GPU analytical modeling package language and location where present.

## Impact

The change touches the Project Manifest and Topic Workspace Manifest data model, CLI command tree, callback manifest loader, callback registry metadata, runtime parameter resolver, TOML renderers, JSON output keys, OpenSpec specs, domain language docs, CLI docs, example skillset package paths, and unit tests. Existing manifests and commands that still use the old names will no longer be valid after this breaking rename.
