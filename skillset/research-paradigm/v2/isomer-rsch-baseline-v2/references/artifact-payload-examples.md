# Baseline Payload Examples

Use this reference when baseline needs a stable payload shape without re-expanding the whole skill body. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Choose the payload type**. Use route decision, accepted baseline, waiver, or blocker shape based on the closeout state.
2. **Keep payloads compact but audit-friendly**. Include enough source, metric, provenance, caveat, and next-route information for later stages.
3. **Preserve the comparison surface**. Keep metric summary, variants, directions, environment facts, source identity, and deviations when they affect downstream comparison.
4. **Do not publish incomplete trust**. Keep blocked, waived, or verification-incomplete payloads separate from accepted baseline payloads.

## Preferences

- Prefer compact structured fields over long prose (if a caveat affects comparison, otherwise include both field and explanation).
- Prefer explicit baseline variant ids when variants matter (if one comparator is primary, otherwise mark default variant).
- Prefer source and environment facts only when they affect trust or comparability (if incidental, otherwise omit).

## Constraints

- <BASELINE_PAYLOAD_RECORD> must not omit the trusted comparison surface because one headline metric exists.
- Accepted baseline payloads must not represent blocked, waived, or incomplete verification states.
- Route and blocker payloads must include reason, evidence sources, and next direction.
- Accepted payloads must include baseline id, kind, task, dataset, primary metric, metrics summary, environment, source, and summary when available.

## Quality Gates

- Type gate: payload type matches accepted, waived, blocked, or route decision state.
- Audit gate: reason, evidence, source, metrics, caveats, and next direction are recoverable.
- Metric gate: required metric ids, primary metric, and metric summary are not collapsed into an untraceable scalar.
- Variant gate: default variant and variant list are present when variants matter.
- Trust gate: blocked or incomplete states are not represented as accepted.

## Route or Blocker Fields

- kind:
- action:
- reason:
- baseline id:
- baseline variant id:
- evidence sources:
- next direction:

## Accepted Baseline Fields

- kind:
- baseline id:
- baseline kind:
- path or package identity:
- task:
- dataset:
- primary metric:
- metrics summary:
- default variant id:
- baseline variants:
- environment:
- source:
- summary:
