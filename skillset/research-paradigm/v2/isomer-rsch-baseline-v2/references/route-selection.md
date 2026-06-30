# Route Selection

Use this reference to choose the cheapest route that can make comparator trust real. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Name the acceptance target**. Choose comparison-ready, paper-repro-ready, registry-publishable, waived, or blocked before selecting the route.
2. **List concrete comparator evidence**. Identify requested or confirmed comparator references, packages, local paths, services, source repositories, metric contracts, outputs, and blockers in <BASELINE_CONTEXT_BRIEF>.
3. **Try the lightest trustworthy path first**. Prefer attach, import, or verify-local-existing when they can establish trust with less work than reproduction.
4. **Escalate only for named trust gaps**. Use reproduce when source establishment is needed, repair when a concrete failure point can change, publish only after verification, and waive only with an explicit durable reason.
5. **Keep one dominant route active**. Record <COMPARATOR_ROUTE_RECORD> and avoid running parallel baseline routes unless they are explicitly needed to resolve comparator trust.

## Preferences

- Prefer attach when a trustworthy reusable comparator already exists (if its outputs and metric contract can be inspected, otherwise import or verify).
- Prefer import when the user provides a package, bundle, or snapshot (if provenance and metrics are traceable, otherwise verify or block).
- Prefer verify-local-existing when a local path or service can be evaluated cheaply (if command, endpoint, split, and metrics are concrete, otherwise audit or reproduce).
- Prefer reproduce only when lighter routes leave the comparator incomparable (if a source audit is needed, otherwise start with `references/codebase-audit-checklist.md`).
- Prefer repair only when the broken point is identified (if the failure class repeats without new evidence, otherwise route to blocker, waiver, or decision).

## Constraints

- <COMPARATOR_ROUTE_RECORD> must choose one dominant route and acceptance target.
- A heavier route must name the unresolved comparison risk it removes.
- Waiver must not be used merely because reproduction is inconvenient.
- Publish must not occur before local trust and verification are complete.
- Route choice must not change accepted comparison meaning without recording the change.

## Quality Gates

- Target gate: acceptance target and current trust state are explicit.
- Comparator gate: candidate comparator identity, source identity, and evidence already available are listed.
- Trust-per-cost gate: chosen route explains why lighter routes are sufficient or insufficient.
- Escalation gate: reproduce, repair, publish, waive, or block has a concrete trigger.
- Stop gate: route selection ends once acceptance, waiver, blocker, or route change is clear.
