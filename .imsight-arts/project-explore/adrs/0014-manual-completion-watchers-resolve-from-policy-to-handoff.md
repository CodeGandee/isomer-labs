# Manual Completion Watchers Resolve from Policy to Handoff

Manual mode will declare completion watcher defaults in Coordination Policy and copy the resolved watcher contract onto each handoff when the Operator Agent opens it. The Topic Agent Team Profile or Agent Team Instance can define normal watcher rules for roles, Workflow Stages, and communication modes, while a specific handoff can override those rules for a task that needs direct inspection, file observation, channel replies, adapter signals, or a combination of signals. The handoff record remains the audit surface for what the Operator Agent actually watched before recording completion.

## Status

accepted

## Considered Options

- Define watcher defaults in Coordination Policy and store resolved watcher rules on each handoff.
- Declare every watcher rule directly on each handoff.
- Let each Execution Adapter define watcher behavior without a provider-neutral Isomer contract.
- Use one Project-wide watcher default for all manual-mode tasks.

## Consequences

- Reusable team profiles can express normal manual-mode behavior without repeating watcher rules in every message.
- Each handoff still records the exact watcher contract used for completion, which supports recovery, validation, and later provenance review.
- Execution Adapters may provide watcher implementations, but they must expose enough provider-neutral metadata for Workspace Runtime to store the resolved watcher contract.
