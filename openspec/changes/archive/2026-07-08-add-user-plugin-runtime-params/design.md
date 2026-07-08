## Context

User Skill Callback registries already let project-local user plugins attach instruction material to packaged system skill stages. The recently archived callback-key work gives plugin-installed callbacks stable ids in the form `<plugin_id>:<plugin-local-key>`, but plugin behavior is still static after installation. A plugin such as `gpu-analytical-modeling` may need topic-specific and worker-specific settings such as evidence strictness, preferred profiling tool, or reporting posture without duplicating callback entries or editing callback prompts.

The Project Manifest is the project-level discovery authority. The Topic Workspace Manifest is topic-owned configuration for one Topic Workspace and carries topic-local topology, worker output policy, and topic-scope User Plugin configuration. This change intentionally extends both files with the same user-plugin tables: Project Manifest rows define project defaults, while Topic Workspace Manifest rows define topic-scope layers and topic-local specializations. This does not make runtime params Workspace Runtime state.

## Goals / Non-Goals

**Goals:**
- Let users manage User Plugins as parent resources with enablement, source identity, and scope-specific status.
- Let users define and resolve plugin-specific runtime params through `isomer-cli` with stable JSON output that callback skills can query.
- Let one table shape work in both Project Manifest and Topic Workspace Manifest, with location and `scope` determining the layer.
- Support imports as default bundles before explicit local values, so users can apply a profile and override only selected params.
- Support topic-local specialization for Research Topic, Topic Actor, and Topic Agent values while keeping project scope singular.
- Keep callback records auditable while allowing effective plugin status to suppress plugin-installed callbacks.

**Non-Goals:**
- Do not store credentials, tokens, API keys, provider secrets, or other secret material as runtime params.
- Do not make runtime params executable code, hook scripts, or provider payloads.
- Do not introduce project-level actors or agents. Project scope has only the project operator and uses the project effective value.
- Do not replace User Skill Callback registries or the existing callback install command in this change.
- Do not treat `topic_agent` as a new durable Isomer actor type. It is a scope label for an existing topic-local Agent Name selected through Effective Agent Context.

## Decisions

1. **Use User Plugin registration as the parent resource.** The CLI gains `project user-plugins` for plugin-level CRUD and `project user-plugin-params` for param-level CRUD. A User Plugin registration records `plugin_id`, source path, status, scope, and optional topic-local selector. User Plugin registration status uses only `active` and `disabled`. Runtime params reference `plugin_id`. This keeps the mental model clear: plugin registration answers whether a plugin is available here, params answer how it behaves here, and callbacks answer where it hooks into skills.

Alternative considered: only add param commands and infer plugin availability from callback records. That would leave no parent object to disable, explain, or move as a whole, and it would force callback resolution to remain the only plugin inventory.

2. **Callback plugin install also ensures plugin registration.** `project skill-callbacks install --plugin-dir` remains the callback-focused installer, but it must create or update the matching `[[user_plugins]]` row at the same selected scope. This keeps the plugin inventory, callback records, and later plugin status gating aligned after a user installs callbacks. The operation must not delete runtime params, imports, or unrelated plugin scope rows.

Alternative considered: reserve User Plugin registration for `project user-plugins install`. That is cleanly separated, but it lets callback installation create plugin-owned callback records without a parent plugin registration, making status gating and inventory incomplete by default.

3. **Use the same TOML table shapes in Project Manifest and Topic Workspace Manifest.** Both files may contain `[[user_plugins]]`, `[[user_plugin_runtime_param_imports]]`, and `[[user_plugin_runtime_params]]`. Project Manifest accepts only `scope = "project"`. Topic Workspace Manifest accepts `scope = "research_topic"`, `scope = "topic_actor"`, and `scope = "topic_agent"`. The same shape matches user expectations while file location provides the layer.

Alternative considered: use separate `project_user_plugin_*` and `topic_user_plugin_*` table names. That is explicit for implementers but makes users learn two schemas for one concept.

4. **Resolve values by layer, then by topic-local specificity.** Effective param resolution applies project-scope imports, project-scope explicit rows, topic-scope imports, and topic-scope explicit rows. Within a topic layer, `research_topic` rows apply broadly to the selected Research Topic, `topic_actor` rows apply only to an exact Topic Actor name, and `topic_agent` rows apply only to an exact topic-local Agent Name.

Alternative considered: resolve by scope specificity first across all sources. That would let a project explicit value override a topic imported default, which contradicts the desired "Project defaults first, Project edits next, Topic defaults next, Topic edits last" user model.

5. **Keep imports param-only and layer-local.** Import rows name a TOML file that contains `[[user_plugin_runtime_params]]` rows. A project import contributes only project-scope values. A topic import contributes only research-topic, topic-actor, or topic-agent values. Imports do not register plugins, install callbacks, define callback sources, or read arbitrary nested imports in the initial implementation.

Alternative considered: allow imports to include plugin registrations and callbacks. That is powerful, but it blurs installation with configuration and makes explain output harder to trust.

6. **Resolve import paths relative to the declaring manifest file.** A relative import path is resolved from the directory containing the file that declares the import row. Project Manifest imports therefore resolve relative to `.isomer-labs/`, Topic Workspace Manifest imports resolve relative to the Topic Workspace root, and imported files resolve any future local references relative to their own file if such references are later supported. Absolute import paths are rejected in the initial implementation.

Alternative considered: resolve all import paths relative to the Project root. That matches some existing project path selectors, but it makes topic-local profiles less portable and breaks the user's expectation that a manifest-adjacent config import is local to that manifest.

7. **Validate param ids and values before resolution.** Param ids use the same high-level namespace shape as plugin callbacks: effective ids are `<plugin_id>:<param-key>`. `plugin_id` follows the existing plugin id rules. Param keys allow ASCII letters, digits, `-`, `_`, and `/` for hierarchy-like naming. Values support `string`, `bool`, `integer`, `number`, `enum`, and `string_list` first. Secret-like keys and values are rejected using the existing callback secret scanner pattern.

Alternative considered: allow arbitrary TOML values. That would be convenient for complex plugins, but it makes validation, CLI setting, JSON output, and secret scanning less predictable.

8. **Require topic-scope params to be defined or self-defining.** A topic-scope explicit value should normally inherit its definition from an applicable Project Manifest row or project import for the same `<plugin_id>:<param-key>`. If no broader definition exists, the topic row may still be accepted only when it carries the full definition metadata itself, including `value_type` and `allowed_values` for enum params. This catches typo-like topic overrides while preserving deliberate topic-local params.

Alternative considered: allow topic values with no broader definition and infer `value_type` from TOML. That is easier to author but makes misspelled keys look like new params and weakens validation.

9. **Gate plugin-installed callbacks by effective plugin status.** Callback records remain installed and auditable. When `skill-callbacks resolve` sees callback metadata with `plugin_id`, it checks the effective User Plugin status for the selected Project, Research Topic, Topic Actor, or Topic Agent context. If disabled, the callback is skipped and explainable diagnostics or metadata show why.

Alternative considered: make disabling a plugin rewrite or disable all callback records. That loses scope-specific behavior and makes re-enabling a plugin risky.

10. **Expose `--topic-agent` as the canonical plugin selector.** New User Plugin and runtime param commands document `--topic-agent` as the canonical selector for topic-agent scoped values. Existing `--agent` spelling may remain as a compatibility alias where the CLI already accepts or later needs it. Both forms resolve to the same Effective Agent Context Agent Name internally, while manifests and JSON use `topic_agent_name`.

Alternative considered: keep only `--agent` at the CLI and use `topic_agent_name` only in manifests and JSON. That would reduce command-option churn but leave the new plugin surface asymmetric with `topic_actor`.

## Risks / Trade-offs

- **Risk: Topic Workspace Manifest becomes more than topology.** → Mitigation: document User Plugin rows as topic-owned configuration, not Workspace Runtime state, and keep runtime records out of these tables.
- **Risk: Imported defaults become hard to debug.** → Mitigation: require `user-plugin-params explain` to show every candidate layer, source file, selected value, and overridden value.
- **Risk: `topic_agent` conflicts with domain language.** → Mitigation: define it as a scope label for existing Effective Agent Context Agent Name and avoid presenting it as a new Agent Instance or Agent Role.
- **Risk: Plugin status gating surprises existing callback users.** → Mitigation: default missing User Plugin registration to enabled for already-installed callbacks unless validation or docs decide to require registration before gating.
- **Risk: Param values accidentally carry secrets.** → Mitigation: reject secret-like names and values in manifests, imports, and CLI writes, and keep credentials in provider or Capability Binding surfaces.

## Migration Plan

Existing callback registries remain valid. Plugin-installed callbacks that have `plugin_id` metadata continue to resolve as they do today until a User Plugin registration explicitly disables that plugin for the selected effective context. Existing user-plugin callback manifests remain valid because runtime param declarations are optional. Future callback install operations ensure a matching User Plugin registration, while pre-existing callback registries without such registration remain enabled for backward compatibility and should produce explanatory metadata rather than hard failures.

Rollback is straightforward: ignore the new tables and CLI command groups. The callback registry format is not changed by runtime params except for read-time gating behavior, which can be disabled by treating missing or unreadable plugin registration state as enabled with diagnostics.

## Open Questions

No open questions remain from the initial proposal pass.
