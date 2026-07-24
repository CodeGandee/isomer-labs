# Explore: Trial

## Workflow

1. **Clarify the execution goal**. Ask: reproduction claim, method trial, smoke check, or benchmark probe?
2. **Assess readiness needs**. Environment, dataset, dependencies, hardware, and access.
3. **Choose between `prepare-code-run`, `run-code-trial`, `method-trial-pass`, and `reproduce`.** Explain the fidelity boundary of each.
4. **Map to a Kaoju command** and produce the exact public invocation.
5. **Resolve plan review**. Ask for explicit human consent by default, or use explicit target-scoped prompt delegation to review and hand off without another user turn. Missing execution scope or protected resource authorization still pauses.

If the task does not map cleanly to these steps, use the native planning tool to separate trial from reproduction.

## Gates, Blockers, and Resume

Pause if the code source, environment, or authorized execution scope is missing. Resume by re-invoking `explore()->trial()` with the same context.
