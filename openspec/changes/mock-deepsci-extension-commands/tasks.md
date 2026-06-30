## 1. Source Contract Fixtures

- [x] 1.1 Capture the DeepScientist memory, artifact, and bash_exec tool registry from `extern/orphan/DeepScientist/src/deepscientist/mcp/server.py` into a test fixture.
- [x] 1.2 Capture representative DeepScientist-compatible response fixtures for memory write/search/list_recent, artifact get_quest_state/read_quest_documents, and bash_exec detach/read/list/history.
- [x] 1.3 Add a fixture assertion helper that checks required response keys without requiring byte-for-byte DeepScientist output.

## 2. CLI Extension Surface

- [x] 2.1 Create a `src/isomer_labs/deepsci_ext/` module for compatibility registry, store, service, and rendering code.
- [x] 2.2 Register an `isomer-cli ext deepsci` command group without changing existing project command behavior.
- [x] 2.3 Implement `isomer-cli ext deepsci call <namespace.tool>` with JSON input loading from an inline argument or stdin.
- [x] 2.4 Implement raw DeepScientist-compatible JSON output for compatibility calls and deterministic JSON errors for unsupported tools.
- [x] 2.5 Add tests that verify input field names are passed through without Isomer-specific renaming or nesting.

## 3. SQLite Compatibility Store

- [x] 3.1 Add extension-owned runtime tables for memory cards, artifact calls, artifact records, bash sessions, and bash log entries.
- [x] 3.2 Add store APIs that open the selected Workspace Runtime and create only the extension tables needed by the mock layer.
- [x] 3.3 Add serialization helpers for JSON metadata, tags, request payloads, and response payloads.
- [x] 3.4 Add tests that verify compatibility rows survive process-level store reopen.

## 4. Memory Mock Implementation

- [x] 4.1 Implement `memory.write` with DeepScientist-compatible card ids, fields, metadata, excerpts, and tag normalization.
- [x] 4.2 Implement `memory.read` by card id or path with source-shaped missing-card errors.
- [x] 4.3 Implement `memory.search` with Python-side text filtering over SQLite rows and DeepScientist-compatible `ok`, `count`, and `items`.
- [x] 4.4 Implement `memory.list_recent` with scope, limit, and kind filtering.
- [x] 4.5 Implement `memory.promote_to_global` by updating compatibility visibility state.
- [x] 4.6 Add unit tests for all memory tools against the captured fixture key sets.

## 5. Artifact Mock Implementation

- [x] 5.1 Implement the source-discovered artifact tool registry and dispatcher.
- [x] 5.2 Persist artifact tool calls with tool name, input JSON, output JSON, mock marker, timestamp, and selected runtime context.
- [x] 5.3 Implement source-shaped mock responses for `artifact.get_quest_state` and `artifact.read_quest_documents`.
- [x] 5.4 Implement generic source-shaped mock responses for the remaining registered artifact tools.
- [x] 5.5 Ensure Git, branch, arXiv, paper, baseline, summary, interaction, and quest-completion tools do not perform external mutation.
- [x] 5.6 Add unit tests for artifact registry coverage, known response shapes, call persistence, and no-external-mutation behavior.

## 6. Bash Exec Mock Implementation

- [x] 6.1 Implement `bash_exec.bash_exec` mode normalization for `detach`, `await`, `create`, `read`, `kill`, `list`, and `history`.
- [x] 6.2 Persist mock session rows with DeepScientist-compatible session fields and timestamps.
- [x] 6.3 Implement read/list/history result builders with bounded log-window metadata.
- [x] 6.4 Implement kill by updating mock session state without sending operating-system signals.
- [x] 6.5 Add unit tests proving no subprocess is launched and no real process is killed.

## 7. Verification

- [x] 7.1 Run `pixi run lint`.
- [x] 7.2 Run `pixi run typecheck`.
- [x] 7.3 Run `pixi run test`.
- [x] 7.4 Run `openspec verify mock-deepsci-extension-commands` or the repo-supported equivalent verification command.
