# Use Literature-First Related-Work Catalogs

Status: accepted

Kaoju field-landscape investigations treat papers and technical reports as the primary related works. Repositories, models, datasets, and benchmarks remain linked implementation or evidence artifacts rather than peer entries, which keeps the field overview readable while preserving Kaoju's practical source traceability.

## Considered Options

- Treat every paper, repository, model, dataset, and benchmark as a peer related work. This was rejected because it mixes entity types and makes the catalog harder to interpret.
- Include literature only. This was rejected because it would omit the implementation and artifact context that distinguishes Kaoju from a conventional literature review.

## Consequences

- Each primary catalog entry represents a paper or technical report and may link to zero or more versioned repositories, models, datasets, and benchmark specifications.
- The Field Summary may synthesize evidence from both the primary works and their linked artifacts, but it must preserve the distinction between reported literature claims and inspected or executed evidence.
