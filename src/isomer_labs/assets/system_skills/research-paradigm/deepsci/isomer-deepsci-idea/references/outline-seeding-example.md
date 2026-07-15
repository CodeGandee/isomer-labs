# Outline Seeding Example

Use this reference when the idea stage is strong enough that the next serious route will likely become paper-facing. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Check paper-facing readiness**. Seed an outline only when the selected route has survived literature, feasibility, and selection checks.
2. **Create a lightweight paper view**. Create DEEPSCI:PAPER-OUTLINE-SEED with working title, central thesis, central insight, reader takeaway, story spine, core claims, and evidence gaps.
3. **Name research questions and designs**. Add one to three research questions, the first main experiment, and at least one likely follow-up analysis family.
4. **Link evidence needs**. Connect claims to required evidence items, falsifiers, controlled factors, and likely main-text or appendix roles.
5. **Defer if unstable**. Do not seed the outline when the frame, frontier, or main claim is still too unstable.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer a short evidence-first seed over a long narrative outline (if the main claim is not yet stable, otherwise leave DEEPSCI:PAPER-OUTLINE-SEED absent).
- Prefer naming evidence gaps early when the route is likely paper-facing (if the route is only an optimization brief, otherwise skip the paper-facing seed).
- Prefer linking claims to future evidence items rather than only prose.

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- DEEPSCI:PAPER-OUTLINE-SEED must not be created before the selected route has survived selection checks.
- DEEPSCI:PAPER-OUTLINE-SEED must not claim generality before robustness and boundary checks exist.
- The outline seed must not replace DEEPSCI:SELECTED-HYPOTHESIS; it only prepares later paper-facing work.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Research-question count: number of paper-facing research questions named in the seed; closer to the source 1-3 range is better.
- Evidence-gap coverage: fraction of core claims linked to required evidence items, falsifiers, controlled factors, and likely main-text or appendix roles; higher is better.

### Checks

- Readiness gate: the route has a clear likely contribution, one to three research questions, and a first main experiment.
- Evidence gate: the seed names evidence gaps and falsifiers.
- Scope gate: claims are limited to current benchmark, model, comparator, and metric contracts unless broader evidence exists.
- Utility gate: later experiment and writing stages can see what evidence the paper-facing line will need.
