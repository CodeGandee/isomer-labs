## Why

User-plugin callbacks can now customize system skills, but they have no supported way to branch on project, topic, Topic Actor, or Topic Agent preferences without hardcoding those choices into callback prompt material. Users need a declarative runtime configuration surface so one plugin can be installed once, given project defaults, and specialized per Research Topic, Topic Actor, or Topic Agent without editing every callback or duplicating plugin material.

## What Changes

- Add User Plugin registration CRUD under `isomer-cli project user-plugins` so users can install, list, show, explain, enable, disable, update-source, uninstall, and validate user plugins as parent resources.
- Add User Plugin Runtime Param CRUD under `isomer-cli project user-plugin-params` so users can define, set, get, list, explain, unset, validate, and manage imports for plugin-specific params.
- Store User Plugin registrations, runtime param imports, and runtime params with the same table shapes in the Project Manifest and Topic Workspace Manifest; file location determines the layer.
- Resolve effective param values in this order: project-scope imports, project-scope explicit params, topic-scope imports, topic-scope explicit params.
- Allow topic-scope param rows to specialize values for `research_topic`, `topic_actor`, or `topic_agent`; reject project-scope actor or agent specialization because project scope has only the project operator using the project value.
- Support TOML param imports as default bundles so users can import a plugin-provided or project-local profile and override only selected values locally.
- Extend user-plugin manifests so plugins may declare runtime param definitions and default param bundles in addition to callback entries.
- Gate plugin-installed callback resolution by the effective User Plugin status so disabling a plugin at a selected scope suppresses its callbacks without deleting callback records or param values.

## Capabilities

### New Capabilities
- `user-plugin-runtime-configuration`: User Plugin registration CRUD, runtime param CRUD, import handling, scope-specific effective value resolution, and plugin status resolution.

### Modified Capabilities
- `user-plugin-callback-manifests`: User-plugin manifests may declare runtime param definitions and imported default bundles in addition to callback entries.
- `user-skill-callbacks`: Callback resolution must honor effective User Plugin status and skip callbacks owned by disabled plugins.
- `topic-workspace-manifest`: Topic Workspace Manifests may carry User Plugin registrations, runtime param imports, and runtime params using the same table shapes as the Project Manifest for topic, Topic Actor, and Topic Agent specialization.

## Impact

- Affects Project Manifest parsing and validation, Topic Workspace Manifest parsing and validation, user-plugin manifest parsing, and CLI command registration under `isomer-cli project`.
- Adds new project modules for User Plugin registration and runtime param resolution, likely adjacent to `project/user_plugin_callbacks.py` and `project/skill_callback_commands.py`.
- Updates User Skill Callback resolution to consult effective plugin status for plugin-installed callbacks.
- Adds unit and CLI tests for Project Manifest values, Topic Workspace Manifest specialization, import precedence, plugin-level CRUD, param-level CRUD, disabled-plugin callback gating, and JSON output for `get` and `explain`.
