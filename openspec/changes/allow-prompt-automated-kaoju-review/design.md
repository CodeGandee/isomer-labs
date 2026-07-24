## Context

Kaoju currently uses the word “Gate” for several different interaction boundaries. Some are research-review checkpoints, such as selecting directions, accepting a Reading List, approving a paper structure, or accepting a bounded trial plan. Others protect credentials, restricted data, licensing decisions, destructive actions, unexpected resource use, public exposure, publication, or submission. Current skill text often requires a new human turn for both categories, and run-to authorization explicitly cannot satisfy any human Gate.

The requested behavior is narrower than removing Gates. When a prompt does not address review posture, Kaoju should continue to ask the user. When the current prompt explicitly delegates review for a named target or named checkpoints, the agent should be able to review, revise, and accept those checkpoints without another user turn. The implementation is skill-contract guidance and validation rather than a new CLI mode or durable schema.

## Goals / Non-Goals

**Goals:**

- Make human review the default for every automatable Kaoju review checkpoint.
- Recognize explicit prompt-scoped delegation of one or more review checkpoints.
- Allow agent review to accept, revise, narrow, or reject candidate material while preserving validation and evidence rules.
- Preserve review mode, prompt basis, rationale, accepted refs, and resume posture in existing Run, decision, Artifact, and provenance surfaces where applicable.
- Keep skill, command-page, shared-reference, README, projected-skill, and test language consistent.
- Maintain a clear boundary between automatable review and protected authorization.

**Non-Goals:**

- Add a global Project setting, CLI flag, Run Control Mode, or persistent “always approve” preference.
- Let run-to wording alone imply review delegation.
- Let automated review create missing evidence, bypass audit, accept invalid state, weaken validation, or cross owner boundaries.
- Let generic review automation authorize credentials, restricted data, material license decisions, destructive or irreversible actions, unexpected resource expansion, public network exposure, publication acceptance, external publication, or submission.
- Change Artifact schemas, Gate schemas, CLI service signatures, or historical records.

## Decisions

### Resolve a prompt-scoped review mode

Each automatable checkpoint resolves to `human` unless the current prompt explicitly delegates that checkpoint or a semantically clear set of review checkpoints for a named target. Phrases such as “review and approve the directions yourself,” “automate the review checkpoints through the local PDF,” or a target-scoped “automate everything” can select agent review when their scope is clear. A plain imperative, silence, ordinary continuation, or `run to <target>` does not.

The resolved mode is prompt-scoped and target-scoped. It expires when the named target completes, the user changes the target, or the workflow reaches a checkpoint outside the delegated set. This avoids introducing global state and matches existing run-to authorization semantics.

Alternative considered: make run-to automatically include every review. Rejected because users may want automatic prerequisite production while retaining editorial control over directions, evidence selection, or a paper.

### Define an explicit automatable review set

The shared Kaoju contract will name the checkpoints eligible for prompt delegation:

- explore plan review and handoff;
- Direction Set selection and acceptance;
- Reading List refinement and acceptance;
- empirical Comparison Intent review and Proceed Decision;
- bounded trial-plan review and execution authorization within pinned inputs, resources, and attempt bounds;
- paper structure and draft review;
- bounded local PDF build authorization within the accepted build policy.

Focused skills retain ownership of the actual decision and validation. Automated review does not turn these checkpoints into unconditional acceptance: the agent may revise, narrow, reject, or pause when the candidate does not meet the contract.

Alternative considered: allow every occurrence of “human” or “Gate” to become automated. Rejected because many occurrences protect external authority rather than editorial review.

### Keep protected boundaries nondelegable under generic review automation

Generic review delegation does not satisfy credential use, private or restricted data access, material license uncertainty, destructive or irreversible action, unexpected cost or resource expansion, accelerator use beyond the accepted boundary, public network exposure, publication acceptance, external publication, or submission. The applicable owner may still treat exact action-specific authorization in the prompt according to its existing contract, but it cannot infer that authorization from “automate reviews.”

Material changes are classified against the accepted prompt boundary. A revised plan may receive automatic review only when the change remains within explicitly delegated choices, resources, and meaning. A new dependency posture, resource expansion, protected data use, changed research meaning, public effect, or other protected trigger pauses.

Alternative considered: preserve all existing human Gates unchanged and automate only prose revisions. Rejected because it would leave comparison intent, bounded trial plans, and local build authorization as redundant turns even when the prompt explicitly delegates them.

### Record the decision through existing provenance

Skill guidance will require terminal reports and applicable durable records to identify whether review was human or agent-delegated, the prompt-scoped basis, the reviewing actor, the rationale, and the accepted or rejected refs. No new schema is required; existing decision, Run, Artifact metadata, and provenance fields carry the information allowed by their owner contracts.

If an owner surface cannot record required decision provenance, the procedure pauses or records the strongest supported existing provenance rather than inventing a file or field.

Alternative considered: add a new `review_mode` CLI option and database column. Rejected because review posture is an agent interaction policy, and the current request does not require a machine-enforced platform feature.

### Update source and projected skill copies together

The packaged source under `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/` is authoritative. Implementation will update it first, run focused and full skill validation, then refresh the project-scope `.agents` projection through the existing installation or synchronization workflow. Tests will assert both the default-human and explicit-agent paths and reject language that still says every review always requires a new human turn.

## Risks / Trade-offs

- [Ambiguous automation wording could produce unwanted acceptance] → Require semantic clarity about the named target or checkpoints; otherwise retain human review.
- [Agent review could be mistaken for user authorship] → Record the reviewing actor, prompt basis, and rationale and preserve authored user choices separately.
- [Broad automation could leak into safety Gates] → Define a closed automatable checkpoint set and retain the protected-boundary list in shared and run-to contracts.
- [Skill copies could drift] → Validate the packaged bundle and refresh the project-scope projection in the same implementation.
- [Static wording tests may miss semantic contradictions] → Add focused contract tests for both positive automation language and retained nondelegable language, then inspect all gate-related occurrences.
- [No new schema means provenance shape can vary by owner] → Require use of existing owner-supported fields and terminal reporting without inventing persistence.

## Migration Plan

1. Update the shared interaction and prerequisite-recovery rules and the public entrypoint.
2. Update focused command and subskill pages for explore, frame, discover, compare, trial, and write.
3. Update the Kaoju README examples and terminology.
4. Adjust contract tests and add coverage for silent prompts, explicit review delegation, ambiguous delegation, material changes, and protected boundaries.
5. Validate the packaged skills, refresh project-scope skills, and run the repository test suite.

Rollback consists of reverting the skill and test changes; no stored state or schema migration is required.

## Open Questions

None. The proposal deliberately treats this as prompt-scoped skill policy rather than a persistent platform mode.
