## Context

The DeepScientist source exposes three MCP harness namespaces that the migrated skills rely on: `memory`, `artifact`, and `bash_exec`. `memory` provides `write`, `read`, `search`, `list_recent`, and `promote_to_global`; `artifact` acts as the quest control plane for records, branches, runtime refs, paper state, baselines, interaction state, and status reads; `bash_exec` owns durable shell-session state through modes such as `detach`, `await`, `read`, `kill`, `list`, and `history`.

Isomer Labs already has an explicit Workspace Runtime stored in Topic Workspace `state.sqlite`, plus CLI conventions for deterministic output. This change adds a DeepScientist-flavored extension layer over that runtime. The first implementation is a compatibility mock: it preserves command names, accepted argument shapes, and result envelope shapes, while leaving true Isomer research semantics for the skill-by-skill migration.

## Goals / Non-Goals

**Goals:**

- Provide `isomer-cli ext deepsci` as the first Isomer-side replacement for DeepScientist MCP harness calls.
- Support a canonical JSON compatibility entrypoint such as `isomer-cli ext deepsci call memory.list_recent --input-json '{...}'` so migrated skills can pass DeepScientist-style arguments without translating them into many CLI flags.
- Persist mock memory cards, artifact calls, artifact records, quest status state, and bash session state in Workspace Runtime SQLite tables.
- Implement memory lookup and search through Python code over SQLite rows, without depending on DeepScientist's markdown-file storage layout or SQLite FTS extensions.
- Return DeepScientist-compatible tool result objects for the supported commands, with an explicit mock marker where the result could otherwise be mistaken for real execution or real research validation.
- Use DeepScientist source tests and server signatures as golden compatibility fixtures.

**Non-Goals:**

- Do not implement the final Isomer research recording model in this change.
- Do not execute shell commands, create Git branches, mutate worktrees, fetch arXiv, submit papers, or contact external services.
- Do not recreate DeepScientist's quest directory layout, markdown memory files, virtualenv assumptions, or daemon behavior.
- Do not change existing Research Recording Contracts, Research Execution Extension Contracts, or Workspace Runtime requirements.

## Decisions

### Decision: Make `call <namespace>.<tool>` the compatibility surface

The extension will expose a generic compatibility command that accepts the DeepScientist tool name and a JSON object using the same argument names as the source MCP tool. Human-friendly aliases can be added under `memory`, `artifact`, and `bash-exec`, but the generic `call` command is the contract that migration work should target.

Rationale: the source tools have many optional arguments, especially `artifact` and `bash_exec`. A JSON call surface preserves the source shape, keeps the first implementation small, and avoids a large Click option tree that would drift while the skills are still being migrated.

Alternative considered: implement one natural CLI subcommand per MCP tool. That would be better for humans but poor for compatibility because the input shape would stop matching DeepScientist.

### Decision: Use raw DeepScientist-compatible output for compatibility calls

The compatibility call path will support emitting the DeepScientist tool result object directly. Isomer's normal `isomer-cli-output.v1` wrapper can remain available for human-facing aliases or diagnostics, but migrated skills need a raw result object when they are replacing MCP tool calls.

Rationale: the user-visible contract for this phase is input/output compatibility with DeepScientist, not ordinary Isomer CLI ergonomics.

Alternative considered: always wrap results in the existing Isomer CLI output envelope. That would be more uniform but would force every migrated skill to peel off Isomer-specific wrapper fields before it can use DeepScientist-compatible responses.

### Decision: Store compatibility state in Workspace Runtime SQLite

The mock implementation will add extension-owned tables in the selected Topic Workspace runtime database, using names such as `deepsci_compat_memory_cards`, `deepsci_compat_artifact_calls`, `deepsci_compat_artifact_records`, `deepsci_compat_bash_sessions`, and `deepsci_compat_bash_log_entries`.

Rationale: this follows Isomer Labs storage design by keeping durable topic-scoped runtime state in `state.sqlite`, while avoiding a dependency on DeepScientist's file-backed markdown memory system. The command implementation owns the table schema and writes through Python service APIs, not by ad hoc SQL from skills.

Alternative considered: mirror DeepScientist's files under the Topic Workspace. That would make inspection familiar to DeepScientist, but it would bypass the Isomer storage layer we want migrated skills to use.

### Decision: Mock behavior by tool family

`memory` mocks will store and return real rows, because memory read/write/search/list behavior is cheap and directly useful during migration. `artifact` mocks will record the tool call and return source-shaped minimal results for known read and write tools. `bash_exec` mocks will store fake session records and logs but will not run a subprocess.

Rationale: this split gives migrated skills realistic persistence where it matters for iterative context, while preventing false evidence from fake experiments, fake Git operations, or fake command execution.

Alternative considered: return static canned payloads for every tool. That would be simpler but would not let skills test handoff behavior across multiple calls.

### Decision: Keep Pixi out of the mock execution contract

The DeepScientist source assumes its own runtime environment, while Isomer Labs uses Pixi. In this mock change, Pixi only affects how developers run tests and how the CLI is installed. Since `bash_exec` does not actually execute commands yet, there is no venv-to-Pixi translation requirement in the first implementation.

Rationale: environment binding matters when real execution is introduced, but forcing it into the mock layer would confuse format compatibility with actual execution policy.

Alternative considered: immediately route `bash_exec` through Pixi. That would be a real execution feature, not a mock, and it belongs in a later migration step with gate, provenance, and scheduler policy.

## Risks / Trade-offs

- Mock responses can be mistaken for real research progress -> Include an explicit `mocked: true` marker for commands whose DeepScientist shape could otherwise imply execution, external lookup, Git mutation, or validated research state.
- Raw compatibility output can diverge from normal Isomer CLI output conventions -> Limit raw output to `ext deepsci call` and keep human aliases compatible with existing CLI rendering where practical.
- The artifact namespace is broad -> Register the source-discovered tool names up front, but implement only minimal source-shaped payloads until a migrated skill needs stronger semantics.
- SQLite schemas can harden too early -> Prefix tables as extension-owned compatibility storage and treat them as migration scaffolding until an accepted Isomer research-storage binding replaces individual mocks.
- Python-side search will be slower than indexed search -> Accept this for the first implementation because compatibility datasets are small; add indexed search later only when real usage requires it.

## Migration Plan

1. Add the `ext deepsci` command group and the generic JSON compatibility dispatcher.
2. Add the extension-owned SQLite tables and Python store/service layer.
3. Implement memory mocks with durable cards and Python filtering for `search` and `list_recent`.
4. Implement artifact mocks with a source tool registry, persisted call records, minimal known result shapes, and explicit mock markers for unsafe semantics.
5. Implement `bash_exec` mocks with durable session rows, fake log rows, read/list/history/kill behavior, and no subprocess execution.
6. Add golden fixture tests based on DeepScientist source signatures and observed test shapes.
7. During skill migration, replace individual mocked artifact or execution tools with real Isomer behavior only after the corresponding skill semantics and storage binding are accepted.

Rollback is straightforward because this change adds an extension command group and extension-owned runtime tables. Removing the command group disables new calls; existing compatibility rows can remain inert in `state.sqlite` until a cleanup task removes them.

## Open Questions

- Which migrated skill should be the first to replace a mocked `artifact` result with a real Isomer research record?
- Should a future MCP bridge call `isomer-cli ext deepsci call` internally, or should the CLI and MCP bridge share the same Python service directly?
