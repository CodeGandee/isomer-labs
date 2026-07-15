---
name: isomer-kaoju-shared
description: Use when any Kaoju survey stage needs common evidence semantics, source identity, lineage, clarification, Gate, owner-routing, or terminal-status rules.
---

# Kaoju Shared Contracts

## Overview

Kaoju preserves what was inspected, what was executed, and how strongly each claim is supported. A later or stronger result adds evidence; it never rewrites the meaning of an earlier observation or Run.

## When to Use

Use this skill with every Kaoju procedure or direct Kaoju stage invocation. Do not use it as a replacement for a stage skill, an owner skill, a provider binding, or an execution adapter.

## Workflow

1. **Resolve current context**. Identify the Research Topic, Research Inquiry, Effective Topic Context, fresh Workspace Runtime state, active procedure, accepted input refs, intended evidence use, latest candidates, and duplicate or supersession posture.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-shared --stage begin`; follow returned instructions within this skill, the user request, evidence, Gate, and owner constraints, while empty callback results continue normally and conflicts must be reported.
3. **Resolve bindings through the extension query**. Read only the pages selected in **Reference Routing**. Before an accepted write, run `isomer-cli --print-json ext kaoju bindings describe KAOJU:WHAT`, then read `references/artifact-semantics.md`, `references/artifact-recording.md`, and the producer's concise `artifact-bindings.md`. The extension query is authoritative; local pages are bundle-local projections and procedures.
4. **Discover durable state through the state DB**. Use `project artifacts latest|list|show` with the binding-defined scope key. Never scan the Topic Workspace filesystem to find a durable Artifact. Reject ambiguous current candidates and stale or corrupt content links.
5. **Preserve evidence meaning**. Record identity, locator, verification depth, evidence verdict, Run purpose, execution fidelity, input basis, and Provenance Record as separate applicable fields.
6. **Route governed work and checkpoint it**. Apply the worker output policy. Use a Service Request for supported Isomer-owned mutation, an Execution Adapter Command Request for registered research execution, a human Gate for material authorization, and an immutable Run plus checkpoint for claim-bearing or resumable work. Repository acquisition and source verification are external user or agent commands; only their verified result, semantic registration, sanitized evidence, or blocker enters Isomer.
7. **Persist through typed operations**. Use `project artifacts put` for a new current-state object or append-only event and `project artifacts revise` only when the binding permits revision. Let the service infer record kind, profile, semantic label, content mode, scope policy, and managed locator.
8. **Apply end callbacks**. After tentative outputs exist, run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-shared --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
9. **Return terminal state**. Report `complete`, `paused`, or `blocked` with durable refs, Run checkpoint, pending Gate, blocker and Service Request refs, and the first incomplete stage as the resume point.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan from these contracts without weakening them.

## Foundational Principle

Evidence labels are part of the evidence. Violating their letter also violates their purpose, even when the resulting narrative looks plausible.

## Evidence Invariants

- Provider output becomes claim-bearing only after deliberate acceptance as an Evidence Item and linkage to a Research Claim.
- Source-only inspection never receives empirical `compared` depth.
- Generated-data results remain `capability-probe` evidence and never become paper reproduction or benchmark evidence.
- Upstream-faithful, adapted, repaired, failed, and blocked attempts remain separate Findings or Runs.
- Accepted structured records use canonical managed JSON with `title`, `summary`, `artifact_family`, `semantic_id`, `artifact_type`, and `sections`; readable views are derived.
- An audit diagnoses evidence; it does not silently repair, delete, relabel, or invent it.

## Durable State and File Authority

The Topic Workspace state DB is the discovery authority for every accepted durable output. A structured Artifact's managed JSON file is its content authority. An ordinary-file Artifact names its media type, checksum, size, and managed or authorized external locator. A directory Artifact is authoritative only through its versioned checksummed manifest. A Canonical External Repository remains externally owned: the Topic Workspace Manifest owns its semantic path binding, while typed Artifacts own requested and resolved locators, immutable identity, acquisition evidence, relationships, and revision history.

Files in an Agent Workspace, Local Tmp Surface, export directory, source checkout, or rendered view are staging or derived material until a typed Artifact operation registers them. Producers never choose internal record-store subpaths. Consumers never reconstruct those paths or use directory scanning as a fallback.

## Gates, Service Requests, and Runs

A Gate records a human authorization decision; it does not execute work. A Service Request records requested operational work and remains distinct from the Research Task, Workflow Stage, command request, and Run. The Service Team returns support Artifact, blocker, Gate, command request, Run, and provenance refs without exposing provider-specific dispatch payloads in Kaoju records.

Every Isomer-managed executable research stage uses the applicable Research Operation Extension Point and an Execution Adapter Command Request. Repository clone, fetch, copy, checkout, repair, feature setup, and source verification remain outside Isomer and use the acting user or agent's ordinary command surface. Begin or resume a Run before managed research execution, checkpoint completed refs and the first incomplete stage, and complete it with immutable command, inputs, outputs, logs, timing, status, and resume posture. Identical transient retries may use the approved bound; any material change requires a revised plan and Gate and creates a separate Run.

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

## Operational Notes

- Store them separately.
- Record both the external source locator and the managed-link locator.
- State `searched_through`, coverage bounds, and the remaining frontier.
- Return the terminal report and let the caller choose the next procedure.

## Guardrails

- DO NOT combine verification depth and evidence verdict into one confidence label.
- DO NOT treat a managed link as dataset identity.
- DO NOT call an inquiry exhaustive because a search converged.
- DO NOT start another macro procedure after completion.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
