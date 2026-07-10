---
name: isomer-kaoju-shared
description: Use when any Kaoju survey stage needs common evidence semantics, source identity, lineage, clarification, Gate, owner-routing, or terminal-status rules.
---

# Kaoju Shared Contracts

## Overview

Kaoju preserves what was inspected, what was executed, and how strongly each claim is supported. A later or stronger result adds evidence; it never rewrites the meaning of an earlier observation or Run.

## Workflow

1. **Resolve current context**. Identify the Research Topic, Research Inquiry, Effective Topic Context, fresh Workspace Runtime state, active procedure, accepted input refs, intended evidence use, latest candidates, and duplicate or supersession posture.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-shared --stage begin`; follow returned instructions within this skill, the user request, evidence, Gate, and owner constraints, while empty callback results continue normally and conflicts must be reported.
3. **Load the applicable contracts**. Read only the pages selected in **Reference Routing**. Before an accepted write, read `references/artifact-semantics.md`, `references/artifact-recording.md`, and the producer's `artifact-bindings.md`.
4. **Preserve evidence meaning**. Record identity, locator, verification depth, evidence verdict, Run purpose, execution fidelity, input basis, and Provenance Record as separate applicable fields.
5. **Route governed work**. Apply the worker output policy, then use the applicable owner for Topic Workspace mutation, environment work, provider access, execution, Gates, and bound durable recording.
6. **Apply end callbacks**. After tentative outputs exist, run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-shared --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
7. **Return terminal state**. Report `complete`, `paused`, or `blocked` with durable refs and a resume point when applicable.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan from these contracts without weakening them.

## When to Use

Use this skill with every Kaoju procedure or direct Kaoju stage invocation. Do not use it as a replacement for a stage skill, an owner skill, a provider binding, or an execution adapter.

## Foundational Principle

Evidence labels are part of the evidence. Violating their letter also violates their purpose, even when the resulting narrative looks plausible.

## Evidence Invariants

- Provider output becomes claim-bearing only after deliberate acceptance as an Evidence Item and linkage to a Research Claim.
- Source-only inspection never receives empirical `compared` depth.
- Generated-data results remain `capability-probe` evidence and never become paper reproduction or benchmark evidence.
- Upstream-faithful, adapted, repaired, failed, and blocked attempts remain separate Findings or Runs.
- Accepted structured records use canonical managed JSON with `title`, `summary`, `artifact_family`, `semantic_id`, `artifact_type`, and `sections`; readable views are derived.
- An audit diagnoses evidence; it does not silently repair, delete, relabel, or invent it.

## Reference Routing

| Need | Read |
| --- | --- |
| Evidence depth, verdict, Run purpose, fidelity, and input basis | `references/evidence-contract.md` |
| Survey Artifact vocabulary and minimum contents | `references/survey-artifacts.md` |
| Stable Kaoju artifact meanings and producer ownership | `references/artifact-semantics.md` |
| Latest-context, canonical payload, lineage, view, worker-output, and material rules | `references/artifact-recording.md` |
| Immutable work, repository, dataset, and model identity | `references/source-identity.md` |
| Clarification-first, Proceed Decision, and Gate behavior | `references/interaction-and-gates.md` |
| Topic Workspace, provider, environment, execution, and recording ownership | `references/external-owner-routing.md` |
| Evidence derivation and update lineage | `references/lineage.md` |
| Terminal report fields and stop semantics | `references/terminal-report.md` |

## Rationalization Table

| Rationalization | Required response |
| --- | --- |
| “The abstract or search result is enough.” | Mark the achieved inspection depth and do not attach stronger claim support. |
| “The repaired Run is what the authors intended.” | Keep the upstream-faithful attempt and repaired Run separate. |
| “All candidates produced numbers, so they are comparable.” | Apply the Comparison Contract and use `not-comparable` when semantics differ. |
| “The user will understand that generated data is only illustrative.” | Label the Artifact, Run purpose, input basis, and limitations explicitly. |
| “The missing source can be reconstructed from context.” | Record a Source Access Blocker and stop claim promotion. |

## Red Flags

- A claim has no exact Evidence Item or Run locator.
- A version family is treated as one immutable source.
- A later result overwrites an earlier verdict or patch state.
- A provider result is cited directly as accepted evidence.
- Expensive or private work starts without the required Gate or Proceed Decision.
- A terminal response omits blockers, failures, or accepted output refs.

## Common Mistakes

- Combining verification depth and evidence verdict into one confidence label. Store them separately.
- Treating a managed link as dataset identity. Record both the external source locator and the managed-link locator.
- Calling an inquiry exhaustive because a search converged. State `searched_through`, coverage bounds, and the remaining frontier.
- Starting another macro procedure after completion. Return the terminal report and let the caller choose the next procedure.
