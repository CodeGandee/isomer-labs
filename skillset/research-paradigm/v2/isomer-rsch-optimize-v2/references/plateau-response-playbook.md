# Plateau Response Playbook

Use this reference when one line keeps producing non-improving results or near-duplicate proposals. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Name the plateau**. State repeated non-improving results, repeated small tweaks, same-family collapse, or a candidate queue full of near duplicates.
2. **Identify root cause**. Explain whether the plateau is mechanism, data, evaluation, implementation, search-family, or resource driven.
3. **Choose a route change**. Select widen search, promote stronger alternative, fuse, debug a strategically valuable blocked candidate, or stop.
4. **Record a non-repeat rule**. Create <PLATEAU_RESPONSE> with what the next pass must not retry.
5. **Apply family-shift trigger**. If recent attempts stay in one mechanism family without improvement, or patience is exhausted, avoid another same-family Tier1 tweak.

## Preferences

- Prefer route review over another local tweak after repeated non-improvement (if new evidence changes the cause, otherwise proceed deliberately).
- Prefer Tier2, Tier3, orthogonal family, fusion, or stop when same-family Tier1 attempts stall.
- Prefer explicit non-retry rule over vague "try something else" language.

## Constraints

- <PLATEAU_RESPONSE> must not hide plateau under one more tiny edit.
- Same unchanged candidate must not be rerun.
- Fusion must not be chosen without complementary strengths.
- Stop must be allowed when remaining routes are low value.

## Quality Gates

### Metrics

- Same-family retry count: number of repeated same-family Tier1 tweaks after plateau or patience exhaustion; lower is better.
- Plateau-response field coverage: fraction of plateau description, root cause, route change, non-repeat rule, and family-shift trigger fields completed; higher is better.

### Checks

- Plateau gate: repeated non-improvement or same-family collapse is documented.
- Cause gate: likely root cause is named.
- Route gate: widen, alternative, fusion, debug, or stop is selected.
- Non-repeat gate: forbidden repeat move is explicit.
- Family-shift gate: same-family Tier1 tweak is blocked when trigger fires.
