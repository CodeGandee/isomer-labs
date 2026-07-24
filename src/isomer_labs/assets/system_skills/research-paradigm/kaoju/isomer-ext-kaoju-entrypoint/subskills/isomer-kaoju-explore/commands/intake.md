# Explore: Intake

## Workflow

1. **Clarify what to intake**. Ask: paper, report, source code, dataset, or model? Identity clues (title, URL, DOI, arXiv id, repository) and what the user wants to learn.
2. **Choose an intake path**. Map to single-item intake, batch intake, or source-code ingestion.
3. **Discuss verification depth and downstream use** (examine, audit, compare, or trial).
4. **Map to a Kaoju command**. Usually `ingest-reading-item`, `ingest-source-code`, `curated-intake-pass`, or `audit-survey-pass`. Produce the exact public invocation.
5. **Resolve plan review**. Ask for explicit human consent by default, or use explicit target-scoped prompt delegation to review and hand off without another user turn. Unresolved identity or protected access authorization still pauses.

If the task does not map cleanly to these steps, use the native planning tool to sequence intake and verification.

## Gates, Blockers, and Resume

Pause if the source identity is unresolved or the required access credentials are missing. Resume by re-invoking `explore()->intake()` with the same context.
