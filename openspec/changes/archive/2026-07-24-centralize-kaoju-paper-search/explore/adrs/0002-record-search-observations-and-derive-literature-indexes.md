# Record Search Observations and Derive Literature Indexes

A logical paper-search action can inspect several provider pages and return many candidate papers and citation edges. Isomer will record one immutable provider-output Artifact for the complete logical action and derive rebuildable paper and citation-edge index rows for local query instead of promoting every provider observation to a canonical research record.

## Status

Accepted.

## Considered Options

- Store one search Artifact without paper-level indexes.
- Store each observed paper and citation edge as an independent canonical record.
- Store one canonical search observation and derive literature-specific query indexes.
- Record only candidates later selected into a Discovery Ledger or Reading List.

## Consequences

- The canonical recording unit is one logical paper-search action, not one HTTP request, provider page, paper candidate, or citation edge.
- The observation schema must preserve the action, purpose, target or query, resolved bounds, pagination, candidates, citation direction and relationships, provider provenance, completeness, limitations, and observation time.
- Derived paper and citation-edge index rows are query accelerators, not Artifacts, Findings, Evidence Items, or independent evidence.
- Index rows must be reproducible from the canonical observation and safe to delete and rebuild.
- `isomer-cli` may query the derived literature indexes without invoking the literature provider.
- Discovery remains responsible for selection decisions and for promoting candidates into the Discovery Ledger and Reading List.
- The canonical Artifact stores normalized data; ADR 0003 permits redacted raw provider responses only as optional file-backed attachments.
