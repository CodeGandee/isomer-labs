## 1. Data Model and Parsing

- [x] 1.1 Add User Plugin registration, runtime param import, runtime param definition, runtime param value, and effective resolution dataclasses or typed models.
- [x] 1.2 Define validation constants for User Plugin status values `active` and `disabled`, runtime param scopes, value types, param key syntax, import schema version, and effective param id parsing.
- [x] 1.3 Extend Project Manifest parsing to collect `user_plugins`, `user_plugin_runtime_param_imports`, and `user_plugin_runtime_params` rows while preserving raw TOML compatibility.
- [x] 1.4 Extend Topic Workspace Manifest parsing to collect the same User Plugin tables without affecting semantic path binding parsing or Workspace Path Resolution.
- [x] 1.5 Extend user-plugin manifest parsing to accept optional runtime param definitions and named default param bundle declarations.

## 2. Validation

- [x] 2.1 Validate Project Manifest User Plugin rows so project scope accepts only `scope = "project"` and rejects `research_topic`, `topic_actor`, and `topic_agent`.
- [x] 2.2 Validate Topic Workspace Manifest User Plugin rows so topic scope accepts only `research_topic`, `topic_actor`, and `topic_agent`.
- [x] 2.3 Validate `topic_actor` rows require `topic_actor_name` and check known Topic Actor bindings when available.
- [x] 2.4 Validate `topic_agent` rows require `topic_agent_name` and treat the value as an Effective Agent Context Agent Name selector.
- [x] 2.5 Validate runtime param value types, enum allowed values, inherited metadata compatibility, duplicate active explicit rows, and missing required values.
- [x] 2.6 Validate topic-scope runtime params without broader definitions only when they carry complete self-defining metadata.
- [x] 2.7 Reuse or share the existing secret-like material scanner so plugin registrations, params, imports, and imported files reject secret-like keys or values.
- [x] 2.8 Validate runtime param imports resolve relative to the declaring manifest file, reject absolute paths, stay within accepted project boundaries, point to readable TOML, contain param-only material, and remain layer-compatible.

## 3. Effective Resolution

- [x] 3.1 Implement User Plugin effective status resolution across project imports or explicit rows where applicable, Project Manifest rows, and Topic Workspace Manifest rows.
- [x] 3.2 Implement runtime param import loading for project-scope imports and topic-scope imports with deterministic diagnostics and source metadata.
- [x] 3.3 Implement runtime param effective value resolution in the order project-scope imports, project-scope explicit params, topic-scope imports, and topic-scope explicit params.
- [x] 3.4 Filter topic-scope param candidates by selected Research Topic, exact Topic Actor name, or exact Topic Agent name.
- [x] 3.5 Produce explain output that includes each candidate layer, source file, import file when present, selected value, overridden values, and diagnostics.

## 4. CLI Commands

- [x] 4.1 Add `isomer-cli project user-plugins install`, `list`, `show`, `explain`, `enable`, `disable`, `update-source`, `uninstall`, and `validate` command registrations.
- [x] 4.2 Add handlers for User Plugin registration CRUD that write only the selected Project Manifest or Topic Workspace Manifest layer.
- [x] 4.3 Add `isomer-cli project user-plugin-params define`, `set`, `get`, `list`, `explain`, `unset`, and `validate` command registrations.
- [x] 4.4 Add `isomer-cli project user-plugin-params import add`, `import list`, `import show`, and `import remove` command registrations.
- [x] 4.5 Support canonical `--topic-agent` selection for topic-agent-scoped plugin and param commands while preserving any existing `--agent` selector as a compatibility alias if needed.
- [x] 4.6 Ensure JSON output for read commands is small, stable, and includes `param_id`, `plugin_id`, `key`, `value`, `value_type`, `effective_scope`, selector metadata, source metadata, and diagnostics.

## 5. Callback Integration

- [x] 5.1 Update User Skill Callback resolution to consult effective User Plugin status for callbacks with `plugin_id` metadata.
- [x] 5.2 Skip plugin-installed callbacks when the effective plugin status is disabled for the selected Project, Research Topic, Topic Actor, or Topic Agent context.
- [x] 5.3 Preserve backward compatibility by treating plugin-installed callbacks as enabled when no matching User Plugin registration exists, while reporting explainable metadata or diagnostics.
- [x] 5.4 Update `project skill-callbacks install --plugin-dir` to ensure a matching User Plugin registration at the same selected scope while preserving plugin params, imports, and other scope rows.
- [x] 5.5 Include plugin gating metadata in callback list, show, resolve, and validate output.

## 6. Tests

- [x] 6.1 Add unit tests for Project Manifest parsing and validation of project-scope plugin registrations, imports, and runtime params.
- [x] 6.2 Add unit tests for Topic Workspace Manifest parsing and validation of research-topic, topic-actor, and topic-agent plugin rows.
- [x] 6.3 Add unit tests for runtime param import loading, layer ordering, explicit overrides, invalid import content, and explain source metadata.
- [x] 6.4 Add CLI tests for User Plugin CRUD commands against Project Manifest and Topic Workspace Manifest layers.
- [x] 6.5 Add CLI tests for runtime param define, set, get, list, explain, unset, validate, and import CRUD commands.
- [x] 6.6 Add callback resolution tests showing disabled plugin callbacks are skipped, missing plugin registration preserves existing callbacks, and disablement is context-specific.
- [x] 6.7 Add callback install tests showing `skill-callbacks install --plugin-dir` creates or refreshes User Plugin registration without deleting params or imports.
- [x] 6.8 Add user-plugin manifest parser tests for optional runtime param definitions and default param bundle declarations.

## 7. Documentation and Validation

- [x] 7.1 Update CLI documentation with `project user-plugins` and `project user-plugin-params` command examples and JSON-oriented skill usage examples.
- [x] 7.2 Update Topic Workspace Manifest documentation and canonical domain language to describe User Plugin configuration tables as topic-owned configuration, not Workspace Runtime state.
- [x] 7.3 Update callback or user-plugin documentation to explain plugin status gating and backward compatibility for existing callback records.
- [x] 7.4 Run `openspec validate add-user-plugin-runtime-params --strict`.
- [x] 7.5 Run focused unit and CLI tests for User Plugin registrations, runtime params, imports, and callback gating.
- [x] 7.6 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
