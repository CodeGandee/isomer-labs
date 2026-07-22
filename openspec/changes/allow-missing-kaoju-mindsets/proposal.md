## Why

Applicable Kaoju paper and source-code workflows currently fail closed when their selected topic Mindset Source file is absent, even though mindset reflection is supplementary to the underlying survey workflow. A missing owner-editable Source should be a durable, visible opt-out posture that lets the Run proceed without fabricating a Source or Mindset Record.

## What Changes

- **BREAKING** Stop lazily recreating absent Mindset Sources as a prerequisite of concrete Kaoju work; explicit Kaoju topic creation remains the way to generate missing Sources.
- Resolve each applicable Run to either a recorded mindset posture with a Run-scoped Mindset Record ref or a skipped posture that records the selected key and missing-Source reason in the Run database record.
- Add a typed Run command that verifies and immutably records either posture after Run creation and exposes it through Run status.
- Let paper and source-code consumers proceed without mindset questions when the Run records the skipped posture, while continuing to block on invalid, unreadable, ambiguous, or mismatched existing Sources and Records.
- Make closeout require a terminal Mindset Record only for Runs whose recorded posture references one; a verified missing-Source posture satisfies mindset closeout with no placeholder Artifact.
- Re-evaluate Source availability for each later Run so a Source added after an earlier skipped Run becomes effective without rewriting historical Run state.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `kaoju-mindsets`: Define missing Source handling, per-Run recorded or skipped posture, immutable absence semantics, and conditional Record closeout.
- `kaoju-research-extension`: Update entrypoint, examination, reading-item, and source-code workflow injection so verified absence propagates and work continues without a Mindset Record.
- `kaoju-cli-services`: Add typed Run persistence and inspection for recorded and skipped mindset resolution.

## Impact

The change affects Kaoju Run state in `lifecycle_records.transition_metadata_json`, `project runs` CLI commands, mindset validation helpers, public and protected Kaoju skill guidance, README documentation, canonical process behavior, and focused unit and integration tests. It adds no Artifact semantic id, placeholder Mindset Record, SQLite table, installer callback, or package-default runtime fallback.
