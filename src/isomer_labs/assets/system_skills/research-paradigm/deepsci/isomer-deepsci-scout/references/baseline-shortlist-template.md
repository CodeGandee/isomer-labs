# Baseline Shortlist Template

Use this when scout must recommend a concrete comparator route before baseline or idea work can proceed. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Start from the evaluation contract**. Use `DEEPSCI:EVALUATION-CONTRACT` to decide which comparator candidates are relevant.
2. **Gather candidate evidence**. Use `DEEPSCI:SCOUT-DISCOVERY-LEDGER`, `DEEPSCI:LITERATURE-SCOUTING-REPORT`, repository inspection, and existing Artifacts, Evidence Items, Findings, or Decision Records.
3. **Score serious candidates only**. Keep the shortlist small and score provenance, metric and split fit, implementation availability, environment risk, expected cost, downstream value, why it matters, and main risk.
4. **Assign one route per candidate**. Mark each candidate as attach, import, reproduce, or reject.
5. **Recommend one next action**. End with `DEEPSCI:BASELINE-SHORTLIST`, `DEEPSCI:NEXT-ROUTE-DECISION`, and `DEEPSCI:SCOUT-BLOCKER-RECORD` if no candidate is responsible to use.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer one recommended comparator route over a broad option dump (if no candidate is usable, otherwise record the blocker).
- Prefer attach or import when provenance, metric fit, and implementation availability are already trustworthy (if not, otherwise route to reproduce or reject).
- Prefer a small decision-facing shortlist over a survey of every adjacent method (if a candidate cannot change baseline or idea routing, otherwise keep it out).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- `DEEPSCI:BASELINE-SHORTLIST` must start from `DEEPSCI:EVALUATION-CONTRACT`.
- Each serious comparator candidate must have provenance, metric and split match, implementation availability, expected cost, downstream value, main risk, and route.
- Scout must not route to idea when no comparator basis is durable enough.
- A rejected comparator should state the reason when the rejection prevents future rework.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Justified candidate count: number of baseline candidates with paper evidence, repo evidence, metric compatibility, expected route, and risk recorded; higher is better until enough candidates exist to choose the next anchor.
- Candidate-risk count: number of shortlist candidates with unresolved provenance, implementation, metric, or maintenance risks; lower is better.

### Checks

- Comparator relevance: every retained candidate can affect `isomer-deepsci-baseline`, `isomer-deepsci-idea`, or `isomer-deepsci-decision`.
- Evidence sufficiency: the recommended route has enough paper, repository, benchmark, or local evidence to justify the next action.
- Route clarity: each candidate has exactly one route recommendation.
- Blocker clarity: if no candidate is usable, `DEEPSCI:SCOUT-BLOCKER-RECORD` names what evidence or decision is missing.
