# Payload Template

Use this reference when the baseline stage needs a stable Artifact, Evidence Item, or Decision Record shape. Keep payloads compact but audit-friendly.

## Route or Blocked Decision Record

Include:

- kind: baseline-route-decision, baseline-blocker, baseline-waiver, baseline-replacement, or baseline-route-change
- action:
- reason:
- baseline id:
- baseline variant id when relevant:
- acceptance target:
- comparator identity:
- source identity:
- evidence pointers:
- comparability verdict:
- next direction:
- caveats:

## Metric-Contract Artifact

Include:

- kind: metric-contract
- baseline id:
- baseline kind:
- route:
- task:
- dataset:
- split:
- evaluation path or Capability Binding:
- required metric ids:
- metric directions:
- primary metric:
- metrics summary:
- environment or resource facts that affect comparability:
- source identity:
- known deviations:
- verification verdict:
- summary:

## Accepted Baseline Decision Record

Include:

- kind: baseline-accepted
- baseline id:
- comparator identity:
- acceptance target:
- metric-contract Artifact:
- supporting Evidence Items:
- comparability verdict:
- caveats:
- next Workflow Stage Cursor:
- Gate reference:

## Variant Rules

Keep baseline identifiers and variant names stable enough that later stages can cite the same comparator without guesswork. Prefer one baseline id with stable variant names over many near-duplicate ids, and mark the primary downstream baseline when multiple comparators exist.

## Rules

- Do not omit the trusted comparison surface because one headline metric exists.
- Do not publish a blocked, waived, or verification-incomplete baseline payload as accepted.
- If concrete payload schemas must be named, use the accepted Decision Record fields, the accepted Evidence Item fields, or the accepted Gate fields.
