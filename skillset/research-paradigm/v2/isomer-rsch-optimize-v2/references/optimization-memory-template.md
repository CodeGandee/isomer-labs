# Optimization Memory Template

Use this reference only when an optimize pass produced a reusable success pattern, repeated failure pattern, fusion lesson, or explicit non-retry rule. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Choose memory type**. Classify success pattern, failure pattern, fusion lesson, or non-retry rule.
2. **Record context**. State task, line, candidate id, strategy, mechanism family, and route state.
3. **Record observation**. State what actually happened and what evidence supports it.
4. **Explain why it matters**. Connect the lesson to future frontier decisions.
5. **Write retrieval and reuse hints**. Include query keywords, closest line or mechanism family, when to recall first, when to reuse, and when to avoid.

## Preferences

- Prefer retrieval-friendly lessons over generic summaries (if nothing reusable was learned, otherwise record why the pass was still necessary).
- Prefer local same-line lessons before broad search during seed, loop, and debug (if same-line evidence exists, otherwise inspect broader prior lessons).
- Prefer one useful <OPTIMIZATION_MEMORY_CARD> over several vague notes.

## Constraints

- <OPTIMIZATION_MEMORY_CARD> must not say only that optimization was attempted.
- Reuse hint must include when the lesson should not be reused.
- Non-retry rules should name the repeated low-information move to avoid.
- Memory should not replace frontier records or candidate board updates.

## Quality Gates

### Metrics

- Lesson-field coverage: fraction of lesson type, situation, action, evidence, reuse condition, and avoid condition fields completed; higher is better.
- Overbroad-reuse count: number of optimization lessons without a clear boundary for when to reuse or avoid the lesson; lower is better.

### Checks

- Type gate: success, failure, fusion, or non-retry type is explicit.
- Evidence gate: observation is tied to result, failure, or route evidence.
- Retrieval gate: keywords and mechanism family make the card findable.
- Reuse gate: reuse and avoid conditions are both stated.

## Template

### Type

- success pattern / failure pattern / fusion lesson / non-retry rule:

### Context

- task:
- line or candidate:
- strategy:
- mechanism family:

### Observation

- what happened:
- evidence:

### Why It Matters

- future decision impact:

### Retrieval Hint

- query keywords:
- closest line or mechanism family:
- recall first when:

### Reuse Hint

- reuse when:
- avoid when:
