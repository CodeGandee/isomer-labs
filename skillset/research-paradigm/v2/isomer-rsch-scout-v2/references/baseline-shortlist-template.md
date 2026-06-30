# Baseline Shortlist Template

Use this when scout must recommend a concrete comparator route before baseline or idea work can proceed. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Start from the evaluation contract**. Use `<EVALUATION_CONTRACT>` to decide which comparator candidates are relevant.
2. **Gather candidate evidence**. Use `<SCOUT_DISCOVERY_LEDGER>`, `<LITERATURE_SCOUTING_REPORT>`, repository inspection, and existing Artifacts, Evidence Items, Findings, or Decision Records.
3. **Score serious candidates only**. Keep the shortlist small and score provenance, metric and split fit, implementation availability, environment risk, expected cost, downstream value, why it matters, and main risk.
4. **Assign one route per candidate**. Mark each candidate as attach, import, reproduce, or reject.
5. **Recommend one next action**. End with `<BASELINE_SHORTLIST>`, `<NEXT_ROUTE_DECISION>`, and `<SCOUT_BLOCKER_RECORD>` if no candidate is responsible to use.

## Preferences

- Prefer one recommended comparator route over a broad option dump (if no candidate is usable, otherwise record the blocker).
- Prefer attach or import when provenance, metric fit, and implementation availability are already trustworthy (if not, otherwise route to reproduce or reject).
- Prefer a small decision-facing shortlist over a survey of every adjacent method (if a candidate cannot change baseline or idea routing, otherwise keep it out).

## Constraints

- `<BASELINE_SHORTLIST>` must start from `<EVALUATION_CONTRACT>`.
- Each serious comparator candidate must have provenance, metric and split match, implementation availability, expected cost, downstream value, main risk, and route.
- Scout must not route to idea when no comparator basis is durable enough.
- A rejected comparator should state the reason when the rejection prevents future rework.

## Quality Gates

- Comparator relevance: every retained candidate can affect `isomer-rsch-baseline-v2`, `isomer-rsch-idea-v2`, or `isomer-rsch-decision-v2`.
- Evidence sufficiency: the recommended route has enough paper, repository, benchmark, or local evidence to justify the next action.
- Route clarity: each candidate has exactly one route recommendation.
- Blocker clarity: if no candidate is usable, `<SCOUT_BLOCKER_RECORD>` names what evidence or decision is missing.
