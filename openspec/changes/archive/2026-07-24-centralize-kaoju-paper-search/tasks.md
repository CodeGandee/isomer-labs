## 1. Register the Protected Capability

- [x] 1.1 Add `isomer-kaoju-paper-search` to the Kaoju pack inventory and capability catalog with member name `paper-search`, the canonical protected path, the canonical designator, shared dependency, and begin/end callback stages.
- [x] 1.2 Add paper-search to `survey-process.v2.json` protected members and ordered skill inventory without changing the public survey-intent inventory.
- [x] 1.3 Add paper-search dependencies to every protected caller that directly requests paper retrieval, including `discover` and `acquire`, while keeping paper-search independent of discover.
- [x] 1.4 Update the Kaoju entrypoint protected-subskill table with a routing sentence that distinguishes paper retrieval from discovery strategy and evidence acceptance.
- [x] 1.5 Set the new bundle's `agents/openai.yaml` metadata version to the current `project.version` and use the parent entrypoint in its default prompt.

## 2. Build the Central Paper-Search Bundle

- [x] 2.1 Create `isomer-kaoju-paper-search/SKILL-MAIN.md` with the standard protected-skill structure, shared-contract routing, provider-neutral workflow, evidence boundary, callbacks, guardrails, and terminal report.
- [x] 2.2 Add the top-level six-action table for `resolve-paper`, `search-papers`, `find-citing-papers`, `explore-cited-papers`, `trace-citation-neighborhood`, and `find-related-papers` without listing provider endpoints or base URLs.
- [x] 2.3 Add one local command page per action with required inputs, bounds, direction semantics, provider request intent, normalized outputs, blockers, and handoffs.
- [x] 2.4 Add `references/provider-selection.md` for Literature Provider Binding resolution, explicit approach requests, missing-provider fallback, Gate posture, and future approach compatibility.
- [x] 2.5 Add `references/result-contract.md` for target and candidate identity, citation direction, parent seed, filters, pagination, completeness, provenance, missing fields, partial results, and continuation posture.
- [x] 2.6 Add `references/execution-and-errors.md` for relative-date resolution, default and maximum traversal bounds, cycle prevention, retry classes, partial-failure preservation, and safe terminal reporting.

## 3. Add the Semantic Scholar Approach

- [x] 3.1 Create bundle-local `references/approaches/s2.md` from current official Semantic Scholar documentation and the relevant portions of the referenced source skill, without retaining any external checkout dependency.
- [x] 3.2 Map each paper-search action to only the needed S2 paper detail, title or topic search, batch metadata, citations, references, and recommendations operations.
- [x] 3.3 Document supported S2 paper identifiers, minimal field projection, edge response shapes, offset or token pagination, null records, and provider-side versus local date filtering.
- [x] 3.4 Document selection and safe use of available provider-native or general-purpose CLI tools, plus bounded direct-HTTPS construction, URL encoding, retry, throttling, and preservation of successful pages as the fallback where policy permits.
- [x] 3.5 Restrict S2 credential resolution to an approved credential binding or non-empty `S2_API_KEY` process environment and prohibit keys in URLs, commands shown to users, logs, chat, Artifacts, and Provenance Records.
- [x] 3.6 Exclude author search, snippet search, Datasets API, bulk corpus export, and unrelated endpoint recipes from the initial approach.
- [x] 3.7 Require the agent to map provider-shaped S2 output into the provider-neutral observation contract and prohibit S2 invocation or response normalization through `isomer-cli`.

## 4. Centralize Existing Kaoju Workflows

- [x] 4.1 Revise `isomer-kaoju-discover` so paper query, target resolution, citation traversal, and adjacent-paper retrieval invoke paper-search while discover retains route planning, source-class coverage, candidate disposition, version families, and durable output ownership.
- [x] 4.2 Revise `isomer-kaoju-acquire` so bounded paper metadata and paper-to-repository association lookup invoke paper-search before acquisition judgment.
- [x] 4.3 Revise reading-list, landscape, curated-intake, direction-expansion, and other active Kaoju command pages that perform paper retrieval to use the centralized owner without changing their public command names.
- [x] 4.4 Audit remaining active Kaoju skills and command pages for paper-search procedure duplication, retaining only owner-specific strategy, selection, evidence, and handoff guidance outside paper-search.
- [x] 4.5 Preserve `isomer-kaoju-discover` as the sole producer of the Discovery Ledger, Reading List, and existing discovery deltas, and preserve acquire and examine as the owners of material and source evidence.
- [x] 4.6 Ensure direct bounded paper-search tasks record one normalized provider-output observation and its limitations without implicitly creating a Reading List, Discovery Ledger, Source Digest, Finding, or Evidence Item.

## 5. Add Normalized Literature Observation Recording

- [x] 5.1 Add provider-neutral `isomer-literature-provider-observation.v1` JSON Schema and Artifact Format Profile assets without S2-specific required fields.
- [x] 5.2 Require action, purpose, evidence-use intent, observation time, provider binding, provider and access method, query or target, seeds, direction, requested and applied bounds, normalized papers, normalized citation edges, pagination, filtering location, completeness, limitations, missing fields, partial failures, and Provenance refs.
- [x] 5.3 Define deterministic normalized paper keys and citation endpoints while preserving DOI, arXiv id, provider-qualified id, title, authors, venue, publication date or year, and locator when available.
- [x] 5.4 Permit redacted raw provider responses only as optional file-backed attachments with media type, checksum, redaction posture, and Provenance refs; reject credentials, authorization headers, and secret-bearing attachments.
- [x] 5.5 Add `isomer-cli ext research literature record --payload-file` so one valid logical action creates one immutable provider-output Artifact through existing research-record storage before any projection refresh.
- [x] 5.6 Add local `observations list` and `observations show` commands with validation, provenance, completeness, payload digest, and projection posture.
- [x] 5.7 State in group and command help that `ext research literature` performs no provider I/O and expose no provider-facing search, resolution, recommendation, citation-fetch, or reference-fetch commands.

## 6. Add the Versioned Literature Query Projection

- [x] 6.1 Define `isomer-literature-query-index.v1` metadata and derived observation, paper-occurrence, and citation-edge tables inside Workspace Runtime without changing `isomer-workspace-runtime.v1`.
- [x] 6.2 Derive literature rows only from validated normalized observation payloads, link every row to its source record and payload digest, and ignore raw provider attachments.
- [x] 6.3 Add `papers query` selectors for normalized DOI, arXiv id, provider-qualified id, title, year, and observation ref without promoting occurrences to canonical records.
- [x] 6.4 Add `citations query` selectors for normalized paper key, source observation, and forward or backward direction while labeling edges as provider-reported.
- [x] 6.5 Add explicit `index rebuild` that creates or replaces only derived literature rows and produces deterministic identities for unchanged canonical observations.
- [x] 6.6 Add read-only `index validate` for schema compatibility, source-record existence, payload-digest drift, malformed paper keys, missing citation endpoints, duplicates, and orphaned rows.
- [x] 6.7 Ensure read-only literature queries never create, migrate, repair, or rebuild tables and report the exact explicit rebuild command when the projection is absent or incompatible.
- [x] 6.8 Ensure canonical recording succeeds when the projection is absent or incompatible and reports projection refresh or rebuild posture separately from the Artifact commit.

## 7. Extend Validation and Automated Tests

- [x] 7.1 Update Kaoju contract, skill-asset, manifest, installer, inspection, projection, and routing tests from fifteen to sixteen protected members and from sixteen to seventeen total execution skills where applicable.
- [x] 7.2 Add exact paper-search bundle tests for logical identity, metadata, six command pages, required local references, callback guidance, and dependency closure.
- [x] 7.3 Add validation that rejects an endpoint inventory, base-URL catalog, credential value, or external checkout path in paper-search `SKILL-MAIN.md`.
- [x] 7.4 Add validation that requires S2 action coverage, provider-selection guidance, result normalization, bounds, direction, pagination, filtering-location, null, partial-failure, external-tool, and redaction guidance in bundle-local resources.
- [x] 7.5 Add tests that paper-search remains protected, materializes with all direct resources, and can be privately projected without sibling or repository dependencies.
- [x] 7.6 Add tests that known paper-retrieval callers route through paper-search and do not embed S2 endpoint mechanics.
- [x] 7.7 Add schema fixtures for complete, truncated, partial, missing-field, unresolved-record, optional-raw-attachment, secret-bearing, and provider-specific-invalid observations.
- [x] 7.8 Add CLI tests proving local literature commands perform no network access, record one Artifact per logical action, and do not create canonical paper or citation records.
- [x] 7.9 Add projection tests for deterministic rebuild, query selectors, direction, duplicate occurrences, digest drift, missing tables, incompatible schema, orphaned rows, read-only no-write behavior, and canonical-record preservation.
- [x] 7.10 Keep automated tests network-free and add only an explicitly gated manual S2 smoke check if live request validation is useful.

## 8. Reconcile Documentation and Inventory Counts

- [x] 8.1 Update Kaoju package, research-paradigm, packaged-system-skill, developer, manual, and tutorial documentation to list paper-search and report sixteen protected members.
- [x] 8.2 Correct existing stale Kaoju counts that still report thirteen or fifteen members and update protected-member tables without exposing paper-search actions as public commands.
- [x] 8.3 Document the discover versus paper-search ownership split, S2 as one approach, agent-direct provider execution, normalized provider-output evidence limits, and the unchanged public survey command surface.
- [x] 8.4 Document `ext research literature` as a local-data-only surface, the one-observation-per-logical-action rule, optional raw attachments, and explicit projection rebuild and validation.
- [x] 8.5 Document `isomer-literature-query-index.v1` independently from Workspace Runtime v1 and state that projection cleanup or rollback never rewrites canonical observations.
- [x] 8.6 Verify all packaged Kaoju `agents/openai.yaml` versions still exactly match `project.version` as required for release.

## 9. Validate the Change

- [x] 9.1 Run focused Kaoju contract, skill-asset, installer, recording, literature-query, projection, and validation unit tests and fix every new inventory, routing, schema, or data-boundary failure.
- [x] 9.2 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
- [x] 9.3 Run the repository skillset and OpenSpec validation commands, including `openspec validate --change centralize-kaoju-paper-search`, and confirm the change remains apply-ready.
