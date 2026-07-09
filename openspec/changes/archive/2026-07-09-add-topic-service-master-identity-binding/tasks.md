## 1. Topic Service Master Naming

- [x] 1.1 Add a typed Topic Service Master naming helper that derives `stem`, `specialist_name`, `launch_profile_name`, and `managed_agent_name` from a Topic Workspace id.
- [x] 1.2 Implement slug normalization, empty-slug diagnostics, maximum-length handling, and deterministic hash suffixing.
- [x] 1.3 Add JSON serialization for suggested names so CLI, skill-context, and self-context payloads use the same structure.

## 2. Topic Workspace Manifest Binding

- [x] 2.1 Add a `TopicServiceMasterBinding` model for provider, status, optional timestamps, source metadata, and nested Houmao provider details.
- [x] 2.2 Parse `[topic_service_master]` and `[topic_service_master.houmao]` from `topic-workspace.toml` and include them in Topic Workspace Manifest JSON output.
- [x] 2.3 Validate provider, bounded status values, required nested Houmao names, name drift against suggested names, and forbidden secret or live-runtime fields.
- [x] 2.4 Add write helpers that create or update the Topic Service Master binding while preserving existing Topic Workspace Manifest content.

## 3. CLI Surfaces

- [x] 3.1 Add `isomer-cli project integrations houmao topic-service-master names --topic-workspace <id>` with JSON output for suggested names and Project Manifest workspace evidence.
- [x] 3.2 Add `isomer-cli project integrations houmao topic-service-master binding show --topic <id>` to inspect suggested names plus the current Topic Workspace Manifest binding.
- [x] 3.3 Add `isomer-cli project integrations houmao topic-service-master binding record --topic <id>` to record prepared, launched, stopped, stale, or archived binding state after Houmao entities exist, while reporting blocked or skipped outcomes without writing a binding.
- [x] 3.4 Ensure disabled Project Houmao integration skips binding writes cleanly while still allowing read-only suggested-name queries.
- [x] 3.5 Extend `skill-context <route> --topic <id>` to include `topic_service_master.suggested_names`, existing binding data, and drift diagnostics.

## 4. Agent and Actor Context

- [x] 4.1 Extend `project self show` and `project self identity` payloads with explicit `topic_workspace_id` in the topic summary or identity block.
- [x] 4.2 Include Topic Service Master suggested names and current binding status in self/context payloads when a Topic Workspace is selected.
- [x] 4.3 Ensure environment-selected `ISOMER_TOPIC_WORKSPACE_ID` is reported as a source and never stored as durable truth without validation.

## 5. System Skill Guidance

- [x] 5.1 Update `isomer-srv-topic-service-agent-support` lifecycle reference pages so `prepare-topic-service-master` obtains suggested names and records the binding after Houmao-owned preparation.
- [x] 5.2 Update launch, inspect, stop, and repair reference pages to consume the Topic Workspace Manifest binding before routing Houmao-owned procedures.
- [x] 5.3 Update `isomer-srv-houmao-interop` guidance so agents do not invent specialist, launch profile, or managed agent names.
- [x] 5.4 Update `isomer-op-topic-creator` setup/finalize/status guidance to report binding state, suggested names, and disabled-integration skip state.

## 6. Tests and Validation

- [x] 6.1 Add unit tests for Topic Service Master name derivation, slugging, truncation, and diagnostics.
- [x] 6.2 Add unit tests for Topic Workspace Manifest binding parse, validation, JSON output, and write preservation.
- [x] 6.3 Add CLI tests for suggested-name query, binding show, binding record, disabled skip, and skill-context identity output.
- [x] 6.4 Add self/context CLI tests showing Topic Workspace id and Topic Service Master identity context for agents or Topic Actors inside a Topic Workspace.
- [x] 6.5 Add skill asset validation tests for suggested-name lookup, binding record/show guidance, and no agent-invented Houmao names.
- [x] 6.6 Run `openspec validate add-topic-service-master-identity-binding --type change --strict --no-interactive --json`, `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
