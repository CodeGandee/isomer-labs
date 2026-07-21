# Explore: Comparison

## Workflow

1. **Clarify comparison intent**. Ask: theory comparison, empirical comparison, or method comparison? Which candidates and what fairness constraints matter?
2. **Decide evidence needs**. Source-only examination, actual-run metrics, or both?
3. **Identify required audits and Gates** before empirical work.
4. **Map to a Kaoju command**. Usually `theory-comparison-pass`, `comparative-pass`, or `compare`. Produce the exact public invocation.
5. **Ask for explicit consent** before handing off.

If the task does not map cleanly to these steps, use the native planning tool to design a comparison contract.

## Gates, Blockers, and Resume

Pause if candidates or comparison metrics are missing. Resume by re-invoking `explore()->comparison()` with the same context.
