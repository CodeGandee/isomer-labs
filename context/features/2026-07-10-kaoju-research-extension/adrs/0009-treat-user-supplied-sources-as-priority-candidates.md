# Treat User-Supplied Sources as Priority Candidates

Status: accepted

When a user supplies references or codebases that they consider important to an existing survey, Kaoju shall give every supplied item priority review and a recorded terminal disposition. User nomination guarantees accounting and inspection effort within the accepted access and resource bounds, but it does not make an item authoritative, relevant, or eligible for automatic inclusion.

## Considered Options

- Add every nominated item directly to the survey. This was rejected because the list may contain duplicates, mutable versions, unsupported claims, unrelated material, or a codebase that should be linked to a primary paper rather than presented as a peer work.
- Treat nominated items like unprioritized search candidates. This was rejected because it ignores the user's domain knowledge and permits an explicitly requested item to disappear without explanation.
- Summarize the items only in the chat response. This was rejected because later survey work could not reuse the source identities, exact locators, findings, relationships, or inclusion decisions.

## Consequences

- A Curated Source Intake Contract records the target survey, the user-supplied list, any stated reason or theme, requested inspection depth, access and resource bounds, and the default prohibition on code execution.
- Discovery resolves each item to stable work and source identities, type, version family, and paper-to-code or other artifact relationships. It deduplicates against both the supplied list and the existing Related-Work Catalog.
- Examination produces a Source Digest for each accessible item. The digest records the item's contribution or purpose, relevant claims, method or implementation structure, evaluation basis, assumptions, limitations, contradictions, linked artifacts, exact source locators, achieved Verification Depth, and useful information proposed for the survey.
- Every supplied item receives one terminal disposition: `included-primary-work`, `linked-artifact`, `contextual-reference`, `merged-duplicate`, `excluded`, or `blocked`. Exclusion and blocker dispositions require a reason; inaccessible items are never silently omitted.
- Papers and technical reports enter or update primary Related-Work Catalog entries under ADR 0001. Codebases, datasets, and models remain linked implementation or evidence artifacts unless supported source relationships establish another role.
- Useful supported information updates the catalog, taxonomy, chronology, Field Summary, Claim-Evidence Ledger, limitations, artifact links, and reading path as applicable. Conflicts with existing survey claims remain visible rather than being reconciled by unsupported inference.
- Curated intake acquires codebases at an immutable revision for read-only inspection and does not build or run them unless the user separately requests an execution-oriented pass.
- The resulting Curated Source Intake Delta preserves per-item provenance and can be applied to the survey after audit. A user-curated list improves a survey but does not establish broad coverage or replace the five-source-class search required for a work survey under ADR 0002.
