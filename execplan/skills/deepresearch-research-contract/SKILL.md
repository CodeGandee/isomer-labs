---
name: deepresearch-research-contract
description: "Use when an operator-facing agent is setting up a deepresearch quest during the start-runbook, BEFORE quest.create (Step 3a), and must deepen a minimal Objective/Acceptance into a checkable scientific done-bar and record the launch-gate token. Keywords: pre-launch, setup-time, research-contract artifact, kind='research-contract', kind='clarification', done-bar, Objective, Acceptance, runs/<q>/objective, research-contract rubric, eight-dimension expansion, over-hardening guardrails, launch gate, move to running."
---

# deepresearch-research-contract

## Overview
A pre-launch, operator-run skill that expands a minimal operator `Objective`/`Acceptance` into a deeper, domain-neutral scientific done-bar using the research-contract rubric, gets operator approval, folds the result into the canonical brief, and records the `kind='research-contract'` artifact the launch gate requires.

## When to Use
Trigger this skill at quest setup, during the start-runbook **before `quest.create`** (Step 3a), when:
- The operator has provided only a minimal `Objective`/`Acceptance` that would collapse to a shallow threshold the loop can clear without understanding.
- The launch gate to `running` needs a `kind='research-contract'` artifact (and a `kind='clarification'` artifact) recorded for the quest.

When NOT to use:
- Do not run from an in-loop role — this is operator-facing and runs while no agents exist yet (no mail trigger, no agent binding).
- Do not run after `quest.create` / after the loop is `running`; this is a one-time, bounded setup pass plus a single operator approval.
- Do not reach across quest boundaries: the objective files and both artifacts are scoped to the single quest `<q>` you are setting up.
- Do not re-open or "move the goalposts" once the operator has approved the contract — changes require a fresh operator decision.

## Inputs
- The operator's `Objective` and `Acceptance`, read verbatim.
- The research-contract rubric, which defines the eight expansion dimensions and the over-hardening guardrails (the canonical copy lives at `execplan/docs/research-contract.md`; the relevant substance is inlined in **Expansion rubric** and **Over-hardening guardrails** below).
- `<q>` = the quest id being set up. `<iso>` = current ISO timestamp.

## Workflow
1. **Read** the operator's `Objective` + `Acceptance` verbatim.
2. **Expand** them with the eight-dimension rubric (see **Expansion rubric**). Include only the dimensions that are *relevant and feasible* for this task and budget — a checklist to consider, not a quota to fill. Draft three files under `runs/<q>/objective/`:
   - `objective.md` (expanded) and `acceptance.md` (expanded — the deep, *checkable* done-conditions);
   - `contract.md` — the original → expanded **diff** plus a one-line rationale per added done-condition.
3. **Get operator approval** via `AskUserQuestion`: present each expansion block for **approve / edit / trim**. Honor the over-hardening guardrails: default to the *minimal sufficient* set; the operator may drop any dimension, soften any threshold, or accept as-is. Do not proceed without an explicit decision.
4. **Fold** the approved edits back into `runs/<q>/objective/{objective,acceptance}.md` — these become the canonical brief the loop reads. Record the rationale + the operator's choices in `contract.md`.
5. **Record the research-contract artifact** (the launch-gate token) — see **Commands**.
6. **Clarification too.** This step *subsumes* the 7-dimension pre-launch ambiguity check — while expanding, also resolve any unclear/underspecified parts of the prompt and record the existing `kind='clarification'` artifact (`runs/<q>/objective/clarification.md`). Both artifacts are required at launch: clarification (no blocking ambiguity) **and** research-contract (deepened, approved done-bar).
7. **Stop.** End after the operator approves the contract and both artifacts are recorded. `quest.create`, GPU confirmation, and launch are the remaining runbook steps (handled via `deepresearch-operator-control` and the start-runbook).

If the task does not map cleanly to these steps, use your native planning tool to build a plan from the commands/constraints in this skill, then execute it.

## Expansion rubric (eight dimensions)
Expand the minimal prompt against these dimensions; the result is general-purpose and **domain-neutral** (ML, systems, bio, social science, …). Include only what is relevant and feasible for the task and budget:
1. Question & falsifiable claim.
2. Mechanism / explanation.
3. Baseline & fair comparison.
4. Ablation / factor isolation.
5. Alternative-hypothesis falsification.
6. Scholarly positioning.
7. Scope & generalization boundaries.
8. Reproducibility & evidence traceability.

## Commands
Record the research-contract artifact (the launch-gate token) verbatim:
```
record apply --json '{"record_type":"artifact.record","record_id":"<q>:research-contract","at":"<iso>","quest_id":"<q>","kind":"research-contract","ref":"runs/<q>/objective/contract.md"}'
```
The clarification artifact is recorded as `kind='clarification'` with ref `runs/<q>/objective/clarification.md` (existing artifact; see Step 6).

## Gates / Output
- **Hard gate:** the move to `running` is blocked unless a `kind='research-contract'` artifact exists for the quest. This is a sibling of the clarification, GPU, and Claude-conditional effort-selection gates. This skill produces the research-contract artifact.
- **Output:** expanded `runs/<q>/objective/{objective,acceptance}.md` (canonical brief), `contract.md` (diff + rationale + operator decisions), and **two** recorded artifacts: `kind='clarification'` and `kind='research-contract'`.
- After this, the runbook proceeds to `quest.create` → GPU confirm → move to `running` (the contract + clarification + GPU + Claude effort-selection gates all pass).

## Over-hardening guardrails (mandatory)
A deeper done-bar is useful only if the quest can still finish:
- **Operator control is the safety valve** — expansion is a *proposal*; the operator approves/edits/trims.
- **Achievable & falsifiable, not merely hard** — every done-condition must be checkable within budget and able to fail informatively; avoid arbitrarily high thresholds.
- **Proportional rigor** — scale depth to stakes, scope, and `max_rounds`; don't impose flagship rigor on a scoping quest.
- **Graceful degradation** — an infeasible dimension downgrades to a documented limitation, not a quest failure.
- **No moving goalposts** — once approved, the contract is fixed for the run; changes need an operator decision.

## Common Mistakes
- **Running this in-loop or treating it as mail-triggered.** It is operator-run at setup, before any agents exist. There is no agent binding and no event trigger.
- **Running it after `quest.create`.** It must complete *before* `quest.create` (Step 3a); the artifact it records is what unblocks the later move to `running`.
- **Skipping the operator approval.** Step 3 must collect an explicit approve/edit/trim decision per block; do not fold or record without it.
- **Over-hardening into an unfinishable bar.** Treat the eight dimensions as a checklist to consider, not a quota to fill; default to the *minimal sufficient* set and apply the guardrails above.
- **Moving the goalposts mid-run.** Once approved the contract is fixed; later changes require a fresh operator decision.
- **Forgetting the clarification artifact.** Both `kind='clarification'` and `kind='research-contract'` are required at launch; recording only one leaves the gate blocked.
- **Altering the record command.** Record the artifact with the exact `record_id` (`<q>:research-contract`), `kind`, and `ref` shown in **Commands**.

## Rationalizations vs. red-flags
| Rationalization | Red flag / correct action |
| --- | --- |
| "The prompt is already detailed, I can skip the expansion." | The hard gate still requires a recorded `kind='research-contract'` artifact. Run the pass and record it. |
| "I'll just accept all eight dimensions to be safe." | Over-hardening. Default to the minimal sufficient set; let the operator trim. |
| "The operator is busy, I'll approve on their behalf." | Operator control is the safety valve. No proceeding without an explicit operator decision. |
| "A threshold looks low, I'll raise it to be rigorous." | Achievable & falsifiable, not merely hard. Keep thresholds checkable within budget; the operator softens, not you. |
| "This dimension is infeasible, so the quest fails." | Graceful degradation. Downgrade it to a documented limitation, not a failure. |
| "Let me tighten the done-bar after the loop started." | No moving goalposts. The contract is fixed once approved; changes need a fresh operator decision. |
| "Clarification is covered elsewhere." | This step subsumes the 7-dimension ambiguity check; record the `kind='clarification'` artifact here too. |
