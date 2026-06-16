---
name: deepresearch-research-contract
description: Pre-launch (setup-time) skill. Before quest.create, expand a minimal operator Objective/Acceptance into a deeper, domain-neutral scientific done-bar using the research-contract rubric, get the operator to approve/edit/trim it, fold it into the canonical brief, and record a kind='research-contract' artifact the launch gate requires.
---

# Research-contract expansion (pre-launch, operator-run)

**Trigger:** quest setup, during the start-runbook **before `quest.create`** (Step 3a). Run by the
operator-facing agent, not by an in-loop role — no agents exist yet. One bounded pass + an operator approval.

**Why:** a minimal `Objective`/`Acceptance` collapses to a shallow threshold the loop can clear without
understanding. This step turns a weak prompt into a high-quality research contract *before* the loop starts,
so it optimizes a deep scientific done-bar — not a number. General-purpose and **domain-neutral** (ML,
systems, bio, social science, …). The rubric lives in `execplan/docs/research-contract.md`.

**Hard gate:** the move to `running` is blocked unless a `kind='research-contract'` artifact exists for the
quest (sibling of the clarification, GPU, and Claude-conditional effort-selection gates). This skill produces
it.

## Steps

1. **Read** the operator's `Objective` + `Acceptance` verbatim.
2. **Expand** them with the eight-dimension rubric (`research-contract.md`): question & falsifiable claim;
   mechanism/explanation; baseline & fair comparison; ablation / factor isolation; alternative-hypothesis
   falsification; scholarly positioning; scope & generalization boundaries; reproducibility & evidence
   traceability. Include only the dimensions that are *relevant and feasible* for this task and budget — this
   is a checklist to consider, not a quota to fill.
   Draft three files under `runs/<q>/objective/`:
   - `objective.md` (expanded) and `acceptance.md` (expanded — the deep, *checkable* done-conditions);
   - `contract.md` — the original → expanded **diff** plus a one-line rationale per added done-condition.
3. **Get operator approval** via `AskUserQuestion`: present each expansion block for **approve / edit /
   trim**. Honor the over-hardening guardrails (see below): default to the *minimal sufficient* set; the
   operator may drop any dimension, soften any threshold, or accept as-is. Do not proceed without an
   explicit decision.
4. **Fold** the approved edits back into `runs/<q>/objective/{objective,acceptance}.md` — these become the
   canonical brief the loop reads. Record the rationale + the operator's choices in `contract.md`.
5. **Record the artifact** (the launch-gate token):
   `record apply --json '{"record_type":"artifact.record","record_id":"<q>:research-contract",
   "at":"<iso>","quest_id":"<q>","kind":"research-contract","ref":"runs/<q>/objective/contract.md"}'`.
6. **Clarification too.** This step *subsumes* the 7-dimension pre-launch ambiguity check — while expanding,
   also resolve any unclear/underspecified parts of the prompt and record the existing
   `kind='clarification'` artifact (`runs/<q>/objective/clarification.md`). Both artifacts are required at
   launch: clarification (no blocking ambiguity) **and** research-contract (deepened, approved done-bar).

## Over-hardening guardrails (mandatory)

A deeper done-bar is useful only if the quest can still finish. Apply the `research-contract.md` guardrails:
- **Operator control is the safety valve** — expansion is a *proposal*; the operator approves/edits/trims.
- **Achievable & falsifiable, not merely hard** — every done-condition must be checkable within budget and
  able to fail informatively; avoid arbitrarily high thresholds.
- **Proportional rigor** — scale depth to stakes, scope, and `max_rounds`; don't impose flagship rigor on a
  scoping quest.
- **Graceful degradation** — an infeasible dimension downgrades to a documented limitation, not a quest
  failure.
- **No moving goalposts** — once approved, the contract is fixed for the run; changes need an operator
  decision.

## Output

- Expanded `runs/<q>/objective/{objective,acceptance}.md` (canonical brief), `contract.md` (diff +
  rationale + operator decisions), and **two** recorded artifacts: `kind='clarification'` and
  `kind='research-contract'`. After this, the runbook proceeds to `quest.create` → gpu confirm → move to
  `running` (the contract + clarification + GPU + Claude effort-selection gates all pass).

## Stop

- End after the operator approves the contract and both artifacts are recorded. Quest creation, GPU
  confirmation, and launch are the remaining runbook steps.
