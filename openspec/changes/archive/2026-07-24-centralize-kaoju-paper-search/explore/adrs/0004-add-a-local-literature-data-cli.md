# Add a Local Literature Data CLI

Agents need a concise way to record normalized literature observations and query previously recorded papers and citation edges without routing external provider work through Isomer. Isomer will add a provider-neutral `isomer-cli ext research literature` command group dedicated to local data recording, inspection, indexing, and query.

## Status

Accepted.

## Considered Options

- Extend only the generic `ext research records` commands.
- Add a provider-neutral `ext research literature` local-data group.
- Add Kaoju-specific paper-search data commands.
- Introduce a new top-level `data literature` command family.

## Consequences

- `ext research literature record` validates and records a normalized literature observation from a local payload file.
- Observation inspection and paper and citation queries read only Isomer-owned local data.
- Literature index rebuild and validation commands manage only derived local projections.
- The command group must state that it does not contact literature providers.
- Provider-facing verbs such as `search`, `resolve`, `recommend`, `find-citing-papers`, and `explore-cited-papers` remain agent-facing paper-search actions rather than `isomer-cli` commands.
- The command group is reusable by Kaoju, DeepSci, and other research extensions without making literature observations Kaoju-owned.
- The implementation may reuse generic research-record storage internally, but its public options must establish the correct profile, schema, provenance, and index behavior without requiring callers to assemble low-level record flags.
