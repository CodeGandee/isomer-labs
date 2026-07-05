# Route Selection

Use this reference to choose the cheapest route that can make comparator trust real. Placeholder definitions live in `../migrate/placeholders.md`.

## Latest Context Freshness

Before producing or refreshing `<BASELINE_CONTEXT_BRIEF>` or `<COMPARATOR_ROUTE_RECORD>`, use the shared Latest Context Preflight. Include Effective Topic Context source, Workspace Runtime inspection, comparator-relevant placeholder records checked, duplicate-record judgment, prompt-versus-durable-context verdict, and route or blocker when the current comparator basis, metric contract, accepted waiver, or baseline target no longer matches durable topic state. Treat structured payload and record metadata as authoritative; on-demand Markdown views are review material.

## Guidance

When performing this step, execute these substeps in order.

1. **Name the acceptance target**. Choose comparison-ready, paper-repro-ready, registry-publishable, waived, or blocked before selecting the route.
2. **List concrete comparator evidence**. Identify requested or confirmed comparator references, packages, local paths, services, source repositories, metric contracts, outputs, and blockers in <BASELINE_CONTEXT_BRIEF>.
3. **Try the lightest trustworthy path first**. Prefer attach, import, or verify-local-existing when they can establish trust with less work than reproduction.
4. **Escalate only for named trust gaps**. Use reproduce when source establishment is needed, repair when a concrete failure point can change, publish only after verification, and waive only with an explicit durable reason.
5. **Keep one dominant route active**. Record <COMPARATOR_ROUTE_RECORD> and avoid running parallel baseline routes unless they are explicitly needed to resolve comparator trust.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer attach when a trustworthy reusable comparator already exists (if its outputs and metric contract can be inspected, otherwise import or verify).
- Prefer import when the user provides a package, bundle, or snapshot (if provenance and metrics are traceable, otherwise verify or block).
- Prefer verify-local-existing when a local path or service can be evaluated cheaply (if command, endpoint, split, and metrics are concrete, otherwise audit or reproduce).
- Prefer reproduce only when lighter routes leave the comparator incomparable (if a source audit is needed, otherwise start with `references/codebase-audit-checklist.md`).
- Prefer repair only when the broken point is identified (if the failure class repeats without new evidence, otherwise route to blocker, waiver, or decision).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- <COMPARATOR_ROUTE_RECORD> must choose one dominant route and acceptance target.
- A heavier route must name the unresolved comparison risk it removes.
- Waiver must not be used merely because reproduction is inconvenient.
- Publish must not occur before local trust and verification are complete.
- Route choice must not change accepted comparison meaning without recording the change.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Trust-per-cost rank: ordinal fit of the chosen route relative to lighter trustworthy routes that could satisfy the acceptance target; lower-cost trustworthy routes are better.
- Unresolved comparison-risk count: number of named comparison risks that still justify escalate, repair, reproduce, waive, or block routing; lower is better.

### Checks

- Target gate: acceptance target and current trust state are explicit.
- Comparator gate: candidate comparator identity, source identity, and evidence already available are listed.
- Trust-per-cost gate: chosen route explains why lighter routes are sufficient or insufficient.
- Escalation gate: reproduce, repair, publish, waive, or block has a concrete trigger.
- Stop gate: route selection ends once acceptance, waiver, blocker, or route change is clear.
