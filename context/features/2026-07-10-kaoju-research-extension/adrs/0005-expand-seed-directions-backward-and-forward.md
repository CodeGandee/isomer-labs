# Expand Seed Directions Backward and Forward

Status: accepted

When a user identifies works A, B, and C as an interesting direction, Kaoju shall treat them as a seed set for survey expansion. It traces their cited predecessors, discovers topic-relevant neighboring works, and searches for closely related post-seed work through an explicit search cutoff before selecting important additions to the survey.

## Considered Options

- Follow only references cited by the seed works. This was rejected because it recovers intellectual predecessors but misses later developments and related work outside the seeds' bibliographies.
- Search only for recent papers with similar keywords. This was rejected because keyword recency does not establish conceptual lineage, close relevance, or historical context.
- Add every discovered candidate to the survey. This was rejected because an uncurated expansion would dilute the direction and hide why each work matters.

## Consequences

- A Seed Direction Expansion Contract records stable seed work identities, the direction boundary, inclusion and importance criteria, search budget, stopping rule, `latest_after`, and `searched_through`.
- Unless the user sets another date boundary, `latest_after` is the latest resolved publication date among the seed work families. `searched_through` records the actual cutoff of the current search rather than presenting “latest” as a permanent property.
- Candidate works preserve one or more discovery routes: `backward-citation`, `topic-neighbor`, `forward-citation`, or `post-seed-latest`, together with their seed or query provenance.
- Importance is justified from multiple signals such as direct relevance, foundational lineage, distinct method contribution, field influence, contradictory evidence, or a meaningful new setting. Citation count or publication date alone cannot decide inclusion.
- The selected additions follow ADR 0001: papers and technical reports become primary Related-Work Catalog entries, while repositories, datasets, and models remain linked artifacts. Discovery still records the five source classes required by ADR 0002.
- The expansion produces an auditable Related-Work Catalog Delta and updates the survey taxonomy, chronology, Field Summary, coverage record, and source provenance without claiming exhaustive coverage.
