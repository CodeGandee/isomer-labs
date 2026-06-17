# Route Selection

Use this reference when the baseline stage needs a clearer decision among attach, import, verify-local-existing, reproduce, repair, waive, block, or route-change.

## Decision Rule

Choose the route that gives the best trust per unit time, compute, and coordination cost. Do not follow a fixed ritual if another route reaches a cleaner comparison contract faster.

## Route Meanings

| Route | Use when | Success boundary |
| --- | --- | --- |
| `attach` | A trustworthy reusable baseline package already exists and can support the current comparison contract. | Package identity, provenance, trusted-output pointers, metric contract, caveats, and Gate Decision Record are explicit. |
| `import` | The user or workspace already provides a prepared package, bundle, snapshot, or result set. | Imported Artifact package is readable, provenance is durable, metrics or outputs trace to evidence, and the metric contract is accepted. |
| `verify-local-existing` | A local implementation or evaluation Capability Binding already exists and can be checked cheaply. | Local comparator identity, evaluation path, output location, required metrics, and comparability verdict are verified. |
| `reproduce` | Source paper, repository, package, or protocol must be rerun to establish trust. | Source identity, evaluation path, expected outputs, deviations, verification evidence, and metric contract are explicit. |
| `repair` | A known baseline line failed but a bounded fix or route change could recover trust. | Broken point is identified, the fix or route switch is bounded, fresh evidence changes the trust state, and the result is accepted or blocked. |
| `waive` | The Research Task must continue without a baseline and the reason is real, explicit, and durable. | Decision Record states why the Gate is waived, what was tried or skipped, what risk remains, and how later work should carry the caveat. |
| `block` | No honest route can clear or waive the Gate within current constraints. | Blocker class, evidence, tried steps, missing dependency, and next best move are durable. |
| `route-change` | The active path no longer maximizes trust per cost. | Decision Record names the old route, new route, reason, preserved evidence, and next action. |

## Comparator-First Rule

The default question is: what is the lightest trustworthy comparator for the current downstream use? Do not start with full reproduction unless attach, import, or local verification cannot establish honest comparability.

Prefer reuse over redundant reproduction, but prefer reproduction or repair when reuse leaves dataset, split, metric, evaluator, source identity, or provenance too ambiguous. A heavier route is justified only when it removes a named unresolved comparison risk.

## Fast-Path Conditions

Use a fast path when all of the following are true:

- The comparator identity is concrete.
- The evaluation path, trusted-output pointer, or evaluation Capability Binding is known.
- The metric ids and directions are known or can be checked directly.
- The downstream stage needs comparison-ready evidence, not paper-grade reproduction or reusable package publication.

When fast-path conditions hold, skip broad discovery and full codebase audit. Run only the verification needed to establish trust.

## Escalation Conditions

Escalate to fuller audit, reproduction, or repair when:

- No concrete comparator can be cited.
- Trusted metrics cannot be traced to outputs, logs, source documents, Run records, or reusable package records.
- Dataset, split, evaluator, metric definition, or metric direction is unknown.
- A local implementation exists but may use a materially different protocol.
- The same failure class repeats without new evidence, code changes, environment changes, or a route change.

## Stop Rule

Stop baseline work once one accepted comparator, explicit waiver, explicit blocker, or explicit route change is durable. Extra baseline work must name the comparison risk it removes.
