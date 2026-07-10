# Manual Mode Control Loop Design

## Status

Approved on 2026-06-17.

## Evidence

This design extends the approved manifested workspace engine design and the accepted manual-mode ADRs.

Relevant project evidence:

- `context/design/project-goal.md` says the human user steers work through an Operator Agent while multi-agent teams do the research work.
- `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md` defines the Operator Agent as the user-facing controller and defines Runs, handoffs, Coordination Policy, Agent Instances, Agent Team Instances, and Workspace Runtime as core Isomer concepts.
- `.imsight-arts/project-explore/designs/2026-06-15-manifested-workspace-engine-design.md` already gives Workspace Runtime durable control-plane state, handoff records, Run records, Gates, Artifact refs, and Operator Agent coordination.

Accepted ADRs:

- `0012-manual-mode-runtime-handoff-completion-authority.md`
- `0013-manual-direct-messages-open-handoffs-before-send.md`
- `0014-manual-completion-watchers-resolve-from-policy-to-handoff.md`
- `0015-manual-mode-advancement-follows-user-prompt-scope.md`
- `0016-manual-mode-is-run-level-control-mode.md`

## Overview

Manual mode is a Run-level control mode. A Run records whether it is controlled automatically or manually. In a manual Run, the Operator Agent directly drives delegated Agent Instances, but it does so through durable handoffs in Workspace Runtime. The user may give a single-stage prompt or a multi-step prompt. The Operator Agent uses that prompt scope to decide whether to wait after each completed handoff or continue through the user-declared steps.

Manual mode does not make file creation, channel replies, or direct inspection authoritative by themselves. Those are completion signal sources. A delegated task is complete only after the Operator Agent records the normalized handoff result, produced Artifact refs, and provenance in Workspace Runtime.

The design keeps the existing Isomer boundary intact: human commands, approvals, Gate decisions, and task-routing changes enter through the Operator Agent. Manual mode gives the user finer control over the Operator Agent's dispatch cadence without turning team Agent Instances into direct human-operated control surfaces.

## Actors & Entry Points

### Human User

The human user asks the Operator Agent to perform a manual operation. The prompt can define one stage, such as "ask the analyst to inspect these results and report risks", or multiple steps, such as "ask the scout to collect sources, then ask the reviewer to check evidence quality". The prompt scope is preserved as Run context so recovery can reconstruct whether the Operator Agent should wait or continue.

### Operator Agent

The Operator Agent owns the manual control loop. It opens handoffs before sending messages, resolves watcher contracts, sends direct instructions through the selected Execution Adapter, observes completion signals, validates produced Artifacts, records completion in Workspace Runtime, and decides whether to continue or wait according to the user's prompt scope.

### Delegated Agent Instance

A delegated Agent Instance receives a bounded task message and works inside its Agent Workspace. It may produce Agent Artifacts, write declared completion files, reply through a configured channel, expose adapter-visible status, or make progress that the Operator Agent can inspect. Its output becomes durable only when the Operator Agent records the accepted result and refs in Workspace Runtime.

### Execution Adapter

The Execution Adapter maps provider-specific send, inspect, channel, and event mechanisms into Isomer-neutral records. It may implement watcher mechanisms, but it must return enough metadata for the Operator Agent to attach outbound messages, observed signals, failures, and completion records to the pre-created handoff.

### Workspace Runtime

Workspace Runtime stores the authoritative manual-mode state: Run control mode, prompt-scope metadata, handoffs, resolved watcher contracts, signal observations, completion status, produced Artifact refs, Gate links, and provenance.

### CLI and GUI

The CLI and GUI expose manual Run state, open handoffs, stale handoffs, completion summaries, pending Gates, and next-action choices. They do not own manual execution semantics. User actions from these surfaces still route through the Operator Agent.

## Components & Responsibilities

### Run Control State

Run control state records the Run's control mode and prompt scope. The first implementation should use two control modes:

- `automatic`: the Operator Agent or scheduler may dispatch according to the approved workflow and Gate policy.
- `manual`: the Operator Agent dispatches direct messages according to user prompt scope.

Manual Runs also need a prompt ref, a prompt-scope kind, and enough prompt-scope summary metadata for recovery.

### Manual Handoff Dispatcher

The manual handoff dispatcher creates a durable handoff before every direct message to an Agent Instance. The handoff records the target Agent Instance, Run, Workflow Stage when applicable, expected outputs, dispatch mode, prompt ref, attempt count, due times when known, and resolved watcher contract ref. Only after that record exists does the Operator Agent send the message.

The message body can remain direct and contextual. The stable handoff id is the durable identity for retries, duplicate sends, late signals, completion normalization, and produced Artifact refs.

### Watcher Resolver

The watcher resolver starts from Coordination Policy defaults in the Topic Agent Team Profile or Agent Team Instance. It resolves the watcher rules for the target role, Workflow Stage, communication mode, adapter, and handoff-specific overrides. It then copies the resolved watcher contract onto the handoff.

Supported watcher kinds should include:

- `agent_inspection`: inspect Agent Instance state or Agent Runtime through the Execution Adapter.
- `file_observation`: watch for declared files inside the Agent Workspace or declared readable paths.
- `channel_reply`: wait for a message on a configured channel that carries the handoff id or equivalent correlation metadata.
- `adapter_event`: consume provider-specific completion or status events mapped by the Execution Adapter.

The resolved watcher contract, not the Coordination Policy default, is the audit surface for a specific handoff.

### Signal Observers

Signal observers implement the watcher contract. They collect observations, attach timestamps and source refs, and record validation status. An observation can indicate progress, acknowledgement, candidate completion, failure, or ambiguity. Observations do not complete a handoff by themselves.

### Completion Normalizer

The completion normalizer evaluates observed signals, validates required Artifact refs, checks the handoff id or correlation metadata, and records the handoff result in Workspace Runtime. A handoff can complete only when the Operator Agent accepts the result and stores produced Artifact refs and provenance.

### Advancement Controller

The advancement controller decides what happens after a manual handoff completes:

- For a single-stage prompt, the Operator Agent summarizes completion and waits for the user's next instruction.
- For a multi-step prompt, the Operator Agent may continue to the next user-declared step.
- For any Gate, failed handoff, stale handoff, invalid Artifact, missing completion evidence, or step outside the prompt scope, the Operator Agent stops and asks the user.

Manual mode therefore remains user-driven without requiring a confirmation after every step that the user already asked the Operator Agent to perform.

### Validation and Recovery

Validation checks that manual Runs have prompt-scope metadata, manual handoffs have resolved watcher contracts, completion records have produced Artifact refs when required, and no downstream state depends on an uncompleted handoff. Recovery reads Run control mode, prompt scope, open handoffs, watcher contracts, observations, and Gates from Workspace Runtime. It does not replay live chat state or rescan arbitrary files as the source of truth.

## Data Model

The first implementation should keep rich instructions and watcher contracts as files or JSON Artifacts where appropriate, with SQLite storing compact refs and status values.

### Run Fields

- `control_mode`: `automatic` or `manual`.
- `prompt_scope_kind`: `single_stage` or `multi_step` for manual Runs.
- `prompt_ref`: Artifact or prompt record that stores the original user prompt.
- `prompt_scope_summary_ref`: concise normalized scope used by recovery and GUI summaries.
- `manual_plan_ref`: optional Artifact that lists declared steps for multi-step manual prompts.

### Handoff Fields

- `dispatch_mode`: `manual_direct` or an automatic dispatch value.
- `dispatch_prompt_ref`: prompt or message Artifact sent to the target Agent Instance.
- `target_agent_instance_id`: delegated Agent Instance that receives the message.
- `target_agent_role_id`: target Agent Role when role context matters.
- `workflow_stage_id`: Workflow Stage when the handoff belongs to a stage.
- `watcher_contract_ref`: resolved watcher contract used for this handoff.
- `signal_observation_refs`: observations collected from inspection, files, channels, or adapter events.
- `completion_status`: open, observing, completed, failed, stale, or blocked.
- `produced_artifact_refs`: accepted output Artifacts from the delegated Agent Instance.
- `completion_provenance_ref`: Provenance Record for how completion was accepted.

### Watcher Contract Artifact

A watcher contract should record:

- watcher kind
- expected source, such as Agent Instance, file path, channel id, or adapter event type
- correlation key, usually the handoff id
- expected output refs or file patterns
- validation rule for candidate completion
- timeout or staleness rule
- duplicate-signal handling
- retention posture for payload content

### Signal Observation Record

A signal observation should record:

- signal kind
- source ref
- observed time
- handoff id or correlation evidence
- validation status
- payload ref when retained
- diagnostic summary

## Data Flow

```text
User prompt
        |
        v
Operator Agent starts or resumes a Run with control_mode = manual
        |
        v
Operator Agent classifies prompt scope as single_stage or multi_step
        |
        v
Operator Agent opens a handoff in Workspace Runtime
        |
        v
Watcher Resolver copies resolved watcher contract from Coordination Policy to handoff
        |
        v
Execution Adapter sends the direct message to the target Agent Instance
        |
        v
Signal Observers collect inspection, file, channel, or adapter observations
        |
        v
Completion Normalizer validates signals and produced Artifacts
        |
        v
Operator Agent records handoff completion in Workspace Runtime
        |
        +-------------------------------+
        |                               |
        v                               v
Single-stage prompt              Multi-step prompt with remaining in-scope steps
summarize and wait               open next handoff and continue
        |
        v
Stop for Gates, failures, stale handoffs, invalid Artifacts, missing evidence, or out-of-scope steps
```

## Error Handling & Edge Cases

If sending a manual message fails, the handoff remains visible in Workspace Runtime with adapter diagnostics. The Operator Agent can retry with the same handoff id when that is safe, reroute to another Agent Instance, or mark the handoff failed.

Duplicate sends and duplicate completion signals attach to the existing handoff id. The receiver or observer should not create a second task unless the Operator Agent explicitly opens a new handoff.

File observation must guard against partial writes. A file signal is a candidate completion only after the expected file exists, any required companion metadata is present, and validation succeeds.

Channel replies must carry the handoff id or another adapter-provided correlation key. A reply without correlation evidence can be attached as a diagnostic observation, but it should not complete a handoff without Operator Agent confirmation.

Direct Agent Instance inspection is useful for manual recovery and ambiguous states, but inspection alone should be normalized into a signal observation before any handoff completes.

Stale handoffs should surface as recoverable state. The Operator Agent can inspect the target, resend, extend the due time, reroute, mark failed, or ask the user.

A multi-step manual prompt cannot bypass Gates. It must stop for irreversible or claim-shaping decisions, including baseline acceptance or waiver, follow-up Research Inquiry or Research Inquiry Relationship selection, Research Claim strengthening, finalization, destructive actions, and archival actions.

Manual mode cannot advance beyond the user's declared prompt scope. If the next step would require interpretation that was not in the prompt, the Operator Agent summarizes state and asks the user.

## Testing Strategy

Early tests should cover:

- Run creation with `control_mode = manual`.
- manual Run prompt-scope persistence for `single_stage` and `multi_step`.
- handoff-before-send ordering.
- resolved watcher contract copied from Coordination Policy to handoff.
- per-handoff watcher override behavior.
- file observation with partial file, valid file, and invalid file cases.
- channel reply normalization with matching, duplicate, and missing handoff ids.
- adapter inspection converted into signal observations.
- completion normalization requiring Workspace Runtime update before downstream state changes.
- duplicate signal deduplication.
- failed send and stale handoff recovery.
- prompt-scope advancement for single-stage and multi-step prompts.
- Gate blocking inside a multi-step prompt.
- GUI or CLI listing of manual Runs, open handoffs, stale handoffs, and completion summaries.

## Key Constraints

- Manual mode is Run-level, not Project-level, Research Topic-level, Research Inquiry-level, or Research Task-level.
- Human users still operate through the Operator Agent.
- Every manual direct message opens a handoff before send.
- Completion signal sources are not authoritative until normalized into Workspace Runtime.
- Watcher defaults live in Coordination Policy, but the resolved watcher contract is copied onto each handoff.
- Prompt scope controls advancement after completion.
- Existing Gate rules still apply.
- Execution Adapters implement backend-specific mechanics without changing Isomer core language.
- Recovery uses Workspace Runtime state, not live conversation memory.

## Implementation Open Questions

- Exact enum names for Run control mode, prompt scope, dispatch mode, and completion status.
- Exact JSON or TOML schema for watcher contract Artifacts.
- Whether signal observations should be a SQLite table, file-backed Artifacts with SQLite refs, or both.
- Initial set of watcher implementations for the first Execution Adapter.
- CLI command names for listing, retrying, inspecting, and closing manual handoffs.
