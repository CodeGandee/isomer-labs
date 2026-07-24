# Literature Observations and Local Queries

This page is for operators and agent authors who need to record provider output from a paper lookup and query that output later. The `isomer-cli ext research literature` surface reads and writes Isomer-owned local data only. It does not call Semantic Scholar, another literature provider, or the network.

## Provider Execution Boundary

The protected `isomer-ext-kaoju-entrypoint->paper-search` capability owns bounded paper identity resolution, paper queries, citation retrieval, citation-neighborhood traversal, and adjacent-paper retrieval. It resolves a Literature Provider Binding, chooses one compatible approach, and invokes an external provider-native CLI, a general-purpose CLI, or bounded HTTPS directly. Semantic Scholar is the first packaged approach, not the canonical data model.

`isomer-kaoju-discover` still owns search strategy, source-class coverage, candidate disposition, version families, the Discovery Ledger, and Reading Lists. `isomer-kaoju-acquire` owns accepted material access and immutable material identity. `isomer-kaoju-examine` owns exact source inspection and claim-bearing evidence. A provider observation does not create or revise any of those outputs.

## Canonical Observation

One logical paper-search action produces one immutable provider-output Artifact with schema version `isomer-literature-provider-observation.v1`. The observation consolidates every successful page, null or unresolved record, partial failure, continuation, requested and applied bound, normalized paper, and provider-reported citation edge from that action. It does not create one lifecycle record per provider page, paper, or edge.

The built-in Artifact Format Profile is `isomer:research/record-format/profile/literature/provider-output/provider-observation/v1`. The provider-neutral payload requires the action, purpose, evidence-use intent, observation time, provider binding, provider and access method, request, seeds, direction, bounds, pagination, filtering location, completeness, limitations, missing fields, unresolved and null records, partial failures, continuation posture, actor, source refs, and Provenance refs.

Normalized paper keys use the first available identity in this order: lowercase DOI, arXiv id without a version suffix, provider-qualified immutable id, then a Unicode-normalized title SHA-256 fallback. Citation edges store intrinsic citing and cited keys, the forward or backward route relative to the request, the parent seed, the source observation, and `provider_reported: true`.

Record a prepared provider-neutral JSON file:

```bash
isomer-cli --print-json ext research literature record --payload-file observation.json --topic my-topic
```

Recording validates the payload and commits the canonical Artifact through the normal research-record and structured-payload mechanisms before it examines the query projection. If the projection is absent or incompatible, the canonical commit still succeeds and the result returns the exact explicit rebuild command.

Inspect canonical observations:

```bash
isomer-cli --print-json ext research literature observations list --topic my-topic
isomer-cli --print-json ext research literature observations show literature-observation-1 --topic my-topic
```

These commands report validation, payload digest, completeness, Provenance refs, and projection posture without provider I/O.

## Optional Raw Attachments

A normalized observation does not require a raw provider response. When policy and reproducibility needs justify retention, `raw_attachments` may reference a local file with media type, SHA-256 checksum, `redaction_posture: redacted`, and Provenance refs. Recording rejects missing files, checksum drift, credentials, authorization headers, signed locators, secret query values, and secret-bearing attachment content.

The query projection never reads raw attachment bodies. Rebuilding from an observation with or without an attachment produces the same normalized rows.

## Literature Query Projection

`isomer-literature-query-index.v1` is a derived projection inside the Workspace Runtime database. It has its own metadata, observation, paper-occurrence, and citation-edge tables. Its version does not revise `isomer-workspace-runtime.v1`, and its rows never become canonical paper or citation records.

Create or replace only the derived literature rows explicitly:

```bash
isomer-cli --print-json ext research literature index rebuild --topic my-topic
isomer-cli --print-json ext research literature index validate --topic my-topic
```

Rebuild reads only validated canonical normalized payloads, ignores raw attachments, links every row to its source record and payload digest, and gives unchanged occurrences and edges deterministic identities. Repeated rebuilds remove duplicate derived rows. A failed replacement rolls back the projection transaction and does not rewrite canonical observations.

Validation is read-only. It reports missing or incompatible tables, missing source records, payload-digest drift, malformed paper keys, missing citation endpoints, duplicates, and orphaned rows. Repair always requires a separate explicit rebuild.

## Local Queries

Paper queries require at least one DOI, arXiv id, provider-qualified id, exact title, year, or source-observation selector:

```bash
isomer-cli --print-json ext research literature papers query --doi 10.1000/example --topic my-topic
isomer-cli --print-json ext research literature papers query --arxiv-id 2401.01234 --topic my-topic
isomer-cli --print-json ext research literature papers query --provider-qualified-id semantic-scholar:S2-ID --topic my-topic
isomer-cli --print-json ext research literature papers query --year 2026 --observation-ref literature-observation-1 --topic my-topic
```

Citation queries require a normalized paper key or source-observation selector. An optional direction filters the normalized route:

```bash
isomer-cli --print-json ext research literature citations query --paper-key doi:10.1000/example --direction forward --topic my-topic
isomer-cli --print-json ext research literature citations query --observation-ref literature-observation-1 --topic my-topic
```

Read-only queries never create, migrate, repair, or rebuild projection tables. A missing or incompatible projection returns `literature_projection_rebuild_required` and the exact `index rebuild` command. Returned occurrences and edges remain provider output until the applicable Kaoju owners accept and promote the information through their existing evidence workflows.
