# Result Contract

## Observation Unit

One logical paper-search action produces one `isomer-literature-provider-observation.v1` payload. Consolidate every accepted page, seed expansion, partial failure, and continuation posture from that action. Do not create one canonical record per provider page, paper, or edge.

## Required Envelope

Record:

- action, research purpose, evidence-use intent, observation time, and provider binding ref;
- provider and access method without credentials or provider request bodies;
- query, target, positive seeds, negative seeds, and normalized direction;
- requested and applied result, page, date, depth, node, per-node, retry, and resource bounds;
- normalized papers and normalized citation edges;
- parent query or seed, hop depth where applicable, and filtering location;
- pages and records inspected, retained count, searched-through date, pagination, and continuation posture;
- complete, truncated, partial, blocked, or unresolved posture;
- missing fields, null records, unresolved records, partial failures, limitations, and Provenance refs.

## Deterministic Paper Identity

Choose the first available stable key in this order:

1. normalized lowercase DOI as `doi:<doi>`;
2. normalized arXiv id without a version suffix as `arxiv:<id>`;
3. provider-qualified immutable id as `provider:<provider-slug>:<id>`;
4. lowercase, Unicode-normalized title digest as `title-sha256:<hex-digest>` only when no stable external or provider identity exists.

Preserve every available DOI, arXiv id, provider-qualified id, title, author name, venue, publication date or year, and locator. A title digest is an occurrence key, not proof that two records represent the same work.

## Citation Direction

Every provider-reported citation edge has `citing_paper_key`, `cited_paper_key`, `route_direction`, `parent_seed_key`, and `source_observation_ref`.

- `forward` means the requested target or expanded seed is cited by the returned citing paper.
- `backward` means the requested target or expanded seed cites the returned cited paper.
- A multi-hop edge retains its intrinsic citing-to-cited endpoints and records the parent seed and hop used to retrieve it.
- Recommendations and metadata similarity use `non-citation` and create no citation edge.

## Missing and Partial Data

Represent an omitted or null field as missing; never fill it from rank, title similarity, memory, or another unrecorded provider. Preserve null edge records and unresolved batch positions. Keep successful pages when a later page fails, record the exact failed operation and retry posture, and mark completeness `partial`.

`complete` means complete only within the declared action and bounds. `truncated` means an available continuation or frontier remained when a bound stopped execution. Record whether filtering happened at the provider, locally, both, or not at all.

## Raw Attachments

Raw provider responses are optional. A retained response must be a file-backed, redacted attachment with media type, SHA-256 checksum, redaction posture, and Provenance refs. Reject credentials, authorization headers, signed locators, secret query values, or unredacted sensitive content. Normalized validation and literature indexing ignore attachment bodies.

## Evidence Boundary

The observation remains provider output. Provider rank, metadata, citation edges, contexts, intents, and influence labels do not become Source Digests, Findings, Evidence Items, or accepted claim support. Hand accepted candidates through `discover`, `acquire`, and `examine` according to the intended use.
