# Explore: Reading List

## Workflow

1. **Clarify the source need**. Ask: seed papers, query terms, venues, date range, language, and whether code or datasets are required.
2. **Propose a discovery strategy**. Choose between broad discovery, curated intake, or direction expansion.
3. **Estimate the candidate list size and selection criteria** with the user.
4. **Map to a Kaoju command**. Usually `build-reading-list`, `curated-intake-pass`, or `direction-expansion-pass`. Produce the exact public invocation.
5. **Resolve plan review**. Ask for explicit human consent by default, or use explicit target-scoped prompt delegation to review and hand off without another user turn. A missing seed or query basis still pauses.

If the task does not map cleanly to these steps, use the native planning tool to compare discovery strategies.

## Gates, Blockers, and Resume

Pause if the seed or query basis is missing. Resume by re-invoking `explore()->reading-list()` with the same context.
