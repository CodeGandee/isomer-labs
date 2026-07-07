# About Kimi Code Session Logs

Kimi Code persists chat sessions as append-only event logs, not as plain Markdown transcripts. The durable source of truth is each agent's `wire.jsonl`; the terminal transcript and web/visual replay views are projections rebuilt from those records.

## Storage layout

Kimi Code stores sessions under `$KIMI_CODE_HOME/sessions/`, defaulting to `~/.kimi-code/sessions/`. Sessions are grouped by a working-directory key:

```text
~/.kimi-code/
├── session_index.jsonl
└── sessions/
    └── <workDirKey>/
        └── <sessionId>/
            ├── state.json
            └── agents/
                ├── main/
                │   └── wire.jsonl
                └── <subagentId>/
                    └── wire.jsonl
```

`state.json` stores session metadata such as title, `lastPrompt`, timestamps, working directory, and agent home directories. `agents/*/wire.jsonl` stores the ordered agent event stream used for recovery and replay. The global `session_index.jsonl` maps `sessionId` to the session directory and working directory.

Relevant source files:

- `extern/orphan/kimi-code/docs/en/guides/sessions.md`
- `extern/orphan/kimi-code/packages/agent-core/src/session/store/session-store.ts`
- `extern/orphan/kimi-code/packages/agent-core/src/session/store/session-index.ts`
- `extern/orphan/kimi-code/packages/agent-core/src/session/store/workdir-key.ts`

## Write path during user chat

When a user sends a message in the TUI, `apps/kimi-code/src/tui/kimi-tui.ts` appends the user message to the live UI transcript, then calls `session.prompt(...)`.

The agent RPC maps that to `this.turn.prompt(payload.input)`. `TurnFlow.prompt()` immediately records a `turn.prompt` event, then launches the turn. When the turn runs, `runOneTurn()` appends the user prompt into the agent context with `appendUserMessage()`. That becomes a `context.append_message` record.

Assistant text, tool calls, tool results, step boundaries, and usage data flow through loop events. `appendLoopEvent()` records those as `context.append_loop_event` entries and mutates in-memory history so the live context stays aligned with the persisted event log.

Relevant source files:

- `extern/orphan/kimi-code/apps/kimi-code/src/tui/kimi-tui.ts`
- `extern/orphan/kimi-code/packages/agent-core/src/agent/index.ts`
- `extern/orphan/kimi-code/packages/agent-core/src/agent/turn/index.ts`
- `extern/orphan/kimi-code/packages/agent-core/src/agent/context/index.ts`

## Persistence mechanics

Agents get a filesystem persistence sink when constructed with a `homedir`. For the main agent, the homedir is `<sessionDir>/agents/main`, so records land in `<sessionDir>/agents/main/wire.jsonl`. Subagents use their own `<sessionDir>/agents/<subagentId>/wire.jsonl`.

`FileSystemAgentRecordPersistence` queues records in memory, batches pending records, converts each record to `JSON.stringify(record) + "\n"`, and writes the batch to `wire.jsonl`. Normal writes open the file in append mode; rewrites open it in truncate mode. After writing, it calls `fh.sync()`, closes the file, and syncs the directory once.

The persistence reader streams `wire.jsonl` line by line and parses each JSON record. It tolerates a truncated trailing line, which can happen if the process crashes mid-flush, but treats corrupted non-trailing lines as errors.

Relevant source files:

- `extern/orphan/kimi-code/packages/agent-core/src/agent/index.ts`
- `extern/orphan/kimi-code/packages/agent-core/src/agent/records/persistence.ts`
- `extern/orphan/kimi-code/packages/agent-core/src/agent/records/types.ts`

## Record shape

A simplified `agents/main/wire.jsonl` can look like this:

```jsonl
{"type":"metadata","protocol_version":"...","created_at":...}
{"type":"turn.prompt","input":[{"type":"text","text":"hello"}],"origin":{"kind":"user"},"time":...}
{"type":"context.append_message","message":{"role":"user","content":[...],"toolCalls":[],"origin":{"kind":"user"}},"time":...}
{"type":"context.append_loop_event","event":{"type":"step.begin",...},"time":...}
{"type":"context.append_loop_event","event":{"type":"content.part",...},"time":...}
{"type":"context.append_loop_event","event":{"type":"step.end",...},"time":...}
```

The record taxonomy is declared in `AgentRecordEvents`. Important chat-related records include `turn.prompt`, `turn.steer`, `turn.cancel`, `context.append_message`, `context.append_loop_event`, `context.apply_compaction`, `context.undo`, `usage.record`, and goal/config/permission/tool records.

## Metadata updates

Main-agent prompts also update session metadata before dispatch. `SessionAPIImpl.prompt()` calls `updatePromptMetadata()` for `agentId === "main"`. That extracts a sanitized text summary from the prompt, updates `lastPrompt`, updates `updatedAt`, and sets an automatic title for an untitled session. This metadata is written to `state.json`; it is not the canonical chat history.

Relevant source files:

- `extern/orphan/kimi-code/packages/agent-core/src/session/rpc.ts`
- `extern/orphan/kimi-code/packages/agent-core/src/session/prompt-metadata.ts`
- `extern/orphan/kimi-code/packages/agent-core/src/session/index.ts`

## Resume behavior

On resume, Kimi reads `state.json` to discover agents and their homedirs, instantiates the main agent, and replays that agent's `wire.jsonl`. `AgentRecords.replay()` expects the first record to be `metadata`, resolves wire migrations if needed, and restores each event through `restoreAgentRecord()`. Restore calls the same state mutation paths used during live execution, such as `appendMessage()` and `appendLoopEvent()`, while suppressing new record writes during replay.

The result is an event-sourced session model: `wire.jsonl` preserves ordered state transitions; `state.json` provides session metadata and agent discovery; UI transcript views are rebuilt from the event stream.

Relevant source files:

- `extern/orphan/kimi-code/packages/agent-core/src/session/index.ts`
- `extern/orphan/kimi-code/packages/agent-core/src/agent/records/index.ts`
- `extern/orphan/kimi-code/packages/agent-core/src/agent/context/index.ts`
