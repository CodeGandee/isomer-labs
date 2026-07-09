## Context

The previous Houmao routing change gives Isomer system skills a Project-local Houmao skill projection and a `skill-context` command that returns `houmao_skill_path`, `houmao_project_path`, and selected Topic Workspace context. That is enough to reach Houmao-owned procedures, but Houmao's agent-definition skills still need concrete names for the specialist, launch profile, and managed agent they create or operate.

Today those names are not part of the Isomer contract. An agent could choose different names on repeated runs, or a later launch/inspect/repair route could lack the exact specialist/profile/agent identity prepared for the Topic Workspace. The durable binding belongs in the Topic Workspace Manifest because it is topic-owned configuration tying a specific Topic Workspace to its service operator actor.

## Goals / Non-Goals

**Goals:**

- Define deterministic Isomer-owned names for the Houmao specialist, launch profile, and managed agent associated with a Topic Workspace.
- Add an Isomer CLI query that returns suggested names from a Topic Workspace id without requiring Houmao state.
- Include those names in Houmao `skill-context` output when a Topic Workspace is selected.
- Persist the prepared or launched Houmao entity binding in `topic-workspace.toml`.
- Expose Topic Workspace id and Topic Service Master identity binding through agent/actor self-context commands.
- Update Topic Service Master skill guidance so prepare uses the suggested names and records the binding before launch.

**Non-Goals:**

- Do not move Houmao credential, profile creation, mailbox, gateway, or launch procedure implementation into `isomer-cli`.
- Do not require Topic Workspace creation to launch a live Topic Service Master.
- Do not store credentials, process ids, tmux session details, mailbox contents, or live runtime truth in the Topic Workspace Manifest.
- Do not make the names editable by ad hoc skill prose without CLI validation.

## Decisions

### Decision: derive a stable Topic Service Master name set from Topic Workspace id

Use the Topic Workspace id as the source of identity because it is Project Manifest-backed, stable, already selected by Effective Topic Context, and available to agents started inside the Topic Workspace.

The canonical stem is:

```text
isomer-tsm-<topic_workspace_slug>
```

The derived Houmao names are:

```text
specialist_name = "isomer-tsm-<topic_workspace_slug>-specialist"
launch_profile_name = "isomer-tsm-<topic_workspace_slug>-profile"
managed_agent_name = "isomer-tsm-<topic_workspace_slug>-agent"
```

`topic_workspace_slug` is produced by lowercasing `topic_workspace_id`, replacing non-`[a-z0-9]` runs with `-`, collapsing repeated dashes, and trimming leading or trailing dashes. If the slug would be empty, the CLI reports a diagnostic. If a derived name exceeds the accepted name length, the slug is shortened and suffixed with a deterministic short hash so the three names remain stable.

Alternative considered: derive names from Research Topic id. Research Topic id is also stable, but Topic Workspace id is the workspace entity Houmao runs from and avoids ambiguity if a future topic has more than one workspace.

### Decision: expose names as CLI context before Houmao procedure

Add a read-only CLI surface under the existing Houmao integration group:

```bash
isomer-cli --print-json project integrations houmao topic-service-master names --topic-workspace <topic-workspace-id>
```

The command resolves the Topic Workspace through Project Manifest data when possible and returns the source id, slug, stem, derived names, and diagnostics. It does not require Houmao integration to be enabled because it is pure Isomer naming context.

`skill-context <route> --topic <research-topic-id>` will embed the same payload under `topic_service_master.suggested_names` and include any existing Topic Workspace Manifest binding under `topic_service_master.binding`.

Alternative considered: ask agents to compute the names in skill prose. That repeats slug logic across agents and makes tests weak. Putting name derivation in the CLI gives every skill and actor the same answer.

### Decision: store binding in Topic Workspace Manifest with nested provider details

Persist the binding in `topic-workspace.toml` as topic-owned service configuration:

```toml
[topic_service_master]
provider = "houmao"
status = "prepared"
updated_by = "isomer-srv-topic-service-agent-support"

[topic_service_master.houmao]
specialist_name = "isomer-tsm-alpha-specialist"
launch_profile_name = "isomer-tsm-alpha-profile"
managed_agent_name = "isomer-tsm-alpha-agent"
specialist_ref = "houmao:specialist:isomer-tsm-alpha-specialist"
launch_profile_ref = "houmao:profile:isomer-tsm-alpha-profile"
managed_agent_ref = "houmao:agent:isomer-tsm-alpha-agent"
```

The top-level `topic_service_master` table carries Isomer-owned service identity metadata such as provider, status, update source, and timestamps. The nested `topic_service_master.houmao` table carries Houmao-specific specialist, launch profile, and managed-agent names or refs. This keeps the Topic Service Master binding first-class while containing Houmao vocabulary inside the provider-specific table.

The binding may also carry `prepared_at`, `launched_at`, and `updated_at` timestamps when available. It must not carry credentials, raw launch profiles, mailbox payloads, gateway queue state, process ids, tmux session names, or provider secrets.

Alternative considered: store the binding in the Project Manifest. The binding is specific to a Topic Workspace and should travel with topic-owned workspace configuration rather than Project-level integration policy.

Alternative considered: store all fields flat under `[topic_service_master]`. That is simpler to parse, but it promotes Houmao-specific fields into the top-level Topic Workspace Manifest shape. A generic repeated `[[service_agents]]` table was also considered but deferred because this change only defines one Topic Service Master per Topic Workspace.

### Decision: make successful prepare the binding writer and later routes binding consumers

`prepare-topic-service-master` will request suggested names before following the projected Houmao route. After Houmao-owned procedure creates or updates the specialist and launch profile, the Isomer service skill records the binding through a CLI command. Isomer does not write a `planned`, `blocked`, or `skipped` Topic Workspace Manifest binding before Houmao preparation succeeds; those outcomes stay in command output, readiness records, or diagnostics. `launch-topic-service-master`, `inspect-topic-service-master`, `stop-topic-service-master`, and `repair-topic-service-master` use the recorded binding when present and compare it to the current suggested names to detect drift.

Alternative considered: write the binding only after launch. That would make the launch route depend on implicit naming and would lose the prepared-but-not-launched state that Topic Creator needs.

Alternative considered: write a `planned` binding before calling Houmao. That would record intent early, but it would make the Topic Workspace Manifest look bound to Houmao entities before those entities exist.

### Decision: expose identity to agents and Topic Actors

Extend self/context query payloads so an agent or Topic Actor inside a Topic Workspace can read the selected `topic_workspace_id` and Topic Service Master identity context without manually parsing Project or Topic Workspace manifests. The minimum surfaces are `project self identity`, `project self show`, and Houmao `skill-context` output.

## Risks / Trade-offs

- Name collision after slug shortening → Include deterministic hash suffix when truncating and validate exact duplicate conflicts against existing binding data.
- Binding drift when a user edits Houmao directly → Inspect and repair routes compare suggested names, recorded binding, and Houmao observations and report drift instead of silently overwriting.
- Manifest grows provider-specific fields → Keep the table narrow and ref-oriented; reject credentials and live runtime fields.
- Topic Workspace id changes → Treat name derivation as id-based. If a workspace id is renamed later, a repair or migration command should reconcile the old binding explicitly.

## Migration Plan

1. Add name derivation helpers and CLI JSON payloads.
2. Add Topic Workspace Manifest parsing, validation, and write helpers for `topic_service_master` and its nested Houmao provider details.
3. Extend Houmao `skill-context` and self/context outputs with suggested names and current binding.
4. Update Topic Service Master system skill reference pages to require names and binding record/show operations.
5. Add tests for name derivation, manifest binding parse/write, CLI output, and skill asset text.

Rollback is safe because the binding table is additive. Older Isomer versions will ignore the new table unless their manifest validation rejects unknown top-level fields; implementation must preserve unknown tables when writing.

## Open Questions

- None for the current proposal. Future implementation may discover provider-specific Houmao validation constraints, such as exact name length limits, that should be handled as implementation details unless they change the public Isomer contract.
