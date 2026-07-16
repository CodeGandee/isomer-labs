## Context

Isomer system skills currently use bounded owner workflows and pipeline procedures. This keeps evidence, mutation, Gate, and Run boundaries clear, but a missing accepted input commonly ends the user interaction with a resume recommendation even when another installed owner skill can produce that input. The user must then invoke each prerequisite manually and remember to return to the original target.

Topic Team Specialization already demonstrates the desired recovery shape: a selected target can offer inclusive targeted fast-forward, run missing predecessors in canonical order, and include the selected target after explicit permission. This change generalizes that interaction pattern without turning ordinary task requests into blanket automation.

Canonical Isomer Control Mode remains Run-level. Run-to is prompt-scoped authorization for a Project Operator Session or Operator Agent to coordinate multiple bounded owner invocations, not a new Control Mode or durable lifecycle object.

## Goals / Non-Goals

**Goals:**

- Stop before prerequisite mutation when an ordinary task request lacks required artifacts or inputs.
- Make prerequisite preflight and recovery selection visible in the controlling skill's numbered workflow.
- Explain the missing inputs, their known producers, and the recommended recovery sequence.
- Offer an inclusive run-to choice that satisfies transitive prerequisites and then executes the original target.
- Avoid repeated prompts for routine prerequisites discovered inside an authorized target closure.
- Preserve owner boundaries, separate Runs, terminal reports, audit rules, and nondelegable Gates.
- Use `paused` for recoverable prerequisite gaps and reserve `blocked` for conditions that need an unavailable external state change.
- Apply one consistent interaction contract to core operator routing, Kaoju, DeepSci, and user documentation.

**Non-Goals:**

- Adding an `isomer-cli run-to` command or a new dependency-graph API.
- Automatically satisfying prerequisites from an ordinary `do <task>` request.
- Treating run-to as a project-wide or session-wide yes-to-all setting.
- Merging prerequisite work and target work into one Run.
- Bypassing evidence acceptance, human Gates, resource policies, destructive-action safeguards, or owner skills.
- Continuing to stages after the selected target or performing unrelated cleanup and improvement work.
- Using generic troubleshooting entries as the primary contract for expected missing-prerequisite control flow.

## Decisions

### Use a Two-Layer Execution Model

Every owner workflow or pipeline procedure remains bounded and produces its existing checkpoint or terminal report. A prompt-level run-to controller, implemented as agent guidance, consumes those results and decides whether to invoke the next prerequisite owner or resume the target.

```text
requested target
      |
      v
prerequisite preflight -- ready --> bounded target execution
      |
      +-- missing --> pause and present recovery choices
                              |
                              +-- run-to authorized
                                      |
                                      v
                             internal dependency plan
                               |       |       |
                            owner A  owner B  target
                             Run      Run      Run
```

This preserves existing statements that a terminal report does not itself select another macro procedure. The separately described run-to controller may select the next bounded procedure only after explicit target-scoped authorization.

Alternative considered: let each procedure silently invoke its producers. Rejected because this hides procedure boundaries, weakens terminal semantics, and makes authorization difficult to audit.

### Keep Ordinary Requests Conservative

`Do <task>` authorizes the target but not mutation needed to manufacture missing prerequisites. When preflight finds a producible gap, the agent pauses and presents at least these semantic choices: run through all prerequisites and the target, execute only the recommended next prerequisite, inspect or choose another recovery route, or stop.

The run-to option may also be authorized directly with language such as `run to <task>`, `automate the prerequisites and then do <task>`, or `yes to all` in response to the recovery prompt. Phrase matching is semantic and does not require one exact command spelling.

Alternative considered: infer run-to from any imperative task request. Rejected because it removes the user-controlled boundary that motivated the design.

### Put Expected Prerequisite Recovery in the Workflow

The controlling `isomer-op-entrypoint`, `isomer-kaoju-pipeline`, and `isomer-deepsci-pipeline` entrypoints will include concise numbered workflow steps that preflight required inputs, pause and present recovery choices when a producer is available, and enter the run-to controller only after explicit authorization. A directly linked prerequisite-recovery reference will hold the detailed choice semantics, target-closure rules, status classification, and nondelegable boundaries so the workflow remains concise.

Missing prerequisites are an expected branch before target execution, not a post-failure diagnostic. The implementation will therefore not rely on a generic `## Troubleshooting Guide` entry to teach this behavior. Troubleshooting remains optional and sparse under the existing format contract and may still document a concrete failure encountered while computing or executing a recovery plan.

Subcommand and procedure pages that declare required predecessor artifacts will keep their local prerequisite checks in their own numbered workflows and point back to the controlling recovery contract when they return a producible gap.

Alternative considered: place the complete recovery procedure in `## Troubleshooting Guide`. Rejected because agents must encounter prerequisite handling during normal workflow execution, and the troubleshooting format is reserved for concrete problem-and-corrective-action entries rather than multi-step control modes.

### Scope Authorization to the Target Closure

The controller creates and maintains an internal todo plan whose terminal node is the original target. It adds known producer routes for missing inputs and may add newly discovered transitive prerequisites without another prompt when they are routine, in scope, and governed by the same authorization. After each owner completes, the controller refreshes durable context and either advances the plan or resumes the target.

Run-to permission ends when the target completes, the user interrupts, a nondelegable boundary is reached, or the closure cannot progress. It does not authorize later recommended work, unrelated repairs, broad refactoring, publication, or external communication.

Alternative considered: persist a global yes-to-all flag. Rejected because its lifetime and authority would be unclear across topics, agents, and unrelated requests.

### Classify Recoverable Dependencies Separately from Blockers

A missing or stale prerequisite with a known in-scope producer route is a recoverable dependency. The requested bounded operation reports `paused`, identifies the producer and resume point, and offers recovery choices. A condition is `blocked` only when the target cannot progress without an external state change that no available in-scope owner can perform.

Invalid evidence may still be a real blocker for the bounded consumer. Under run-to, the controller can route a separate repair procedure and later retry the consumer. Audit procedures remain non-repairing; the controller invokes the recommended repair owner and starts a new audit after repair.

Alternative considered: preserve `blocked` for every missing input and let the controller reinterpret it. Rejected because it prevents users and tools from distinguishing actionable dependency closure from an actual impasse.

### Preserve Nondelegable Boundaries

Run-to automatically covers routine, reversible, in-scope prerequisite work. It pauses for any required human Gate, material change to the requested goal, destructive or irreversible action, credentials or restricted data, material license uncertainty, unexpected cost or resource use, public exposure, publication or submission, or ambiguity whose alternatives change the task's meaning.

The initial target request may authorize operations inherently named by that target, but it does not satisfy a separate configured Gate unless that Gate contract explicitly accepts the recorded request as its decision evidence.

### Keep Durable Procedure Records Separate

Each prerequisite owner and the target retain separate Research Tasks, Runs, terminal reports, Artifacts, and provenance as required by their existing contracts. The native todo plan is orchestration state for the active agent interaction, while durable state remains reconstructable from accepted refs, checkpoints, and resume hints. No new schema, placeholder, or Control Mode value is introduced.

### Enforce the Guidance Through Focused Validation

Static validation and unit fixtures will require the numbered workflows of the operator entrypoint and both pipeline families to describe conservative prerequisite preflight, recovery-choice routing, target-scoped run-to, and Gate preservation, with detailed semantics reachable through directly linked references. Tests will reject implementations that place the normal control branch only in troubleshooting, automate prerequisites from every imperative request, or forbid authorized run-to orchestration entirely.

## Risks / Trade-offs

- **Risk: Natural-language authorization is interpreted too broadly.** Mitigation: require an explicit run-to or equivalent prerequisite-automation instruction and bind it to one named target.
- **Risk: A dependency traversal loops between repair routes.** Mitigation: keep the internal plan current, refresh durable state after each owner, preserve retry limits, and pause when traversal repeats without new accepted evidence or state.
- **Risk: Procedure-level `paused` status is mistaken for the end of run-to.** Mitigation: distinguish the bounded procedure terminal report from the controller's final user response and continue only when its recovery route remains inside the authorized closure.
- **Risk: Run-to bypasses a scientific or operational Gate.** Mitigation: state nondelegable boundaries in shared guidance and retain every wrapped owner's existing Gate checks.
- **Risk: Static dependency recommendations become stale.** Mitigation: treat skill pages and current durable records as planning evidence, re-run preflight before each owner, and avoid adding a new hard-coded dependency API.
- **Trade-off: Long run-to operations can produce several Runs and status records.** This is intentional because separate provenance is preferable to one opaque macro execution.

## Migration Plan

1. Add the directly linked run-to prerequisite-recovery guidance and its validation coverage.
2. Update the numbered `isomer-op-entrypoint` workflow plus routing and output guidance to present recovery choices and control authorized traversal.
3. Update the numbered Kaoju pipeline workflow, shared interaction, terminal, and relevant command guidance to distinguish bounded termination from run-to controller continuation.
4. Update the numbered DeepSci pipeline workflow, shared coordination, transition, and terminal guidance with the same two-layer contract.
5. Update research workflow tutorials with default-pause and run-to examples.
6. Run focused unit validation, then the repository lint, typecheck, and unit test commands.

No durable data migration is required. Rolling back the skill and documentation changes restores the prior step-by-step behavior without invalidating Runs or Artifacts created while run-to guidance was active.

## Open Questions

None. The user-facing canonical label is “run to the target,” while semantically equivalent natural-language authorization remains accepted.
