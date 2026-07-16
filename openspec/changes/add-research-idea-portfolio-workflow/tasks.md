## 1. Domain and Runtime Schema

- [ ] 1.1 Update the canonical domain-language document to define independent Research Idea exploration, decision, evidence, archive, and visibility facets, closure reasons, state transitions, and decision option membership.
- [ ] 1.2 Add typed Research Idea facet vocabularies, transition records, decision-option records, operation correlation, and deprecated compatibility-status projection to runtime record models.
- [ ] 1.3 Add an additive SQLite migration for Research Idea facet columns, state-transition rows, decision-option membership rows, idempotency records, constraints, and query indexes while preserving existing status data.
- [ ] 1.4 Implement runtime store create, read, list, and atomic mutation methods for facets, transitions, decision options, and operation ids with topic-boundary and ref validation.
- [ ] 1.5 Add unit tests for valid independent facet combinations, invalid vocabularies, closure reason requirements, topic isolation, transaction rollback, and compatibility-status projection.

## 2. CLI, Validation, and Legacy Migration

- [ ] 2.1 Extend `ext research ideas upsert` with initial canonical facet arguments and deprecate direct status mutation without removing compatibility reads.
- [ ] 2.2 Add deterministic Research Idea transition and decision-option maintenance commands that require actor, rationale or reason, expected state, and applicable durable refs.
- [ ] 2.3 Extend Research Idea query commands with facet, archive, visibility, generation, and Decision Record filters and complete decision-context output.
- [ ] 2.4 Add bounded ancestor and descendant traversal commands with relation-kind, depth, node, and edge limits plus explicit completeness metadata.
- [ ] 2.5 Implement preview and apply legacy-status migration using the conservative mapping in `design.md`, preserved original values, migration provenance, and `unknown` diagnostics.
- [ ] 2.6 Extend Research Idea validation to cover invalid facets, incomplete transitions, compatibility projection conflicts, missing decision options, stale refs, and ambiguous legacy classifications.
- [ ] 2.7 Add CLI and runtime tests for JSON determinism, preview non-mutation, apply idempotency, partial historical decision context, traversal bounds, and migration rollback safety.

## 3. Recording Contracts and Producer Integration

- [ ] 3.1 Extend structured idea-bearing payload and profile mappings to accept authored facets, transition context, decision option sets, closure reasons, and exact Idea Realization paths.
- [ ] 3.2 Make record acceptance and promised canonical Research Idea effects one transaction, returning all created or updated idea, realization, lineage, decision, and transition refs.
- [ ] 3.3 Reject partial canonical effects for profiles that promise idea recording while continuing to accept non-idea-bearing records without inferred ideas.
- [ ] 3.4 Add recording tests for raw slates, candidate frontiers, exploration outputs, evidence assessments, selected hypotheses, rejected or deferred ledgers, reopening decisions, and atomic failure.

## 4. System-skill Guidance

- [ ] 4.1 Update the shared Research Idea Recording reference with the new facet vocabulary, transition commands, decision-option requirements, migration posture, and accepted-output verification checklist.
- [ ] 4.2 Update idea-producing DeepSci skill workflows and placeholder bindings to record canonical facets, exact realizations, lineage, generations, considered option sets, and terminal result refs at acceptance time.
- [ ] 4.3 Audit other packaged research-paradigm skills and extensions that create, select, defer, close, reopen, support, or refute Research Ideas and route them through the shared recording contract.
- [ ] 4.4 Add skill-content tests that reject overloaded status-only instructions, Markdown-only completion claims, copied divergent vocabularies, and missing canonical write verification.

## 5. Query Index and GUI Backend Read Models

- [ ] 5.1 Project canonical idea facets, decision summaries, transition refs, classification diagnostics, and facet counts into lightweight query-index and Project Web read models.
- [ ] 5.2 Implement the fixed portfolio preset registry and explicit filter composition with coherent filtered edges, source counts, visible counts, applied predicates, and completeness metadata.
- [ ] 5.3 Add read-only decision-context endpoints that return recorded alternatives, outcomes, rationale, consequences, closure or deferral reasons, reopen history, and supporting refs without backfilling missing context.
- [ ] 5.4 Add bounded ancestor and descendant read endpoints over canonical Idea Lineage Edges with incomplete-result diagnostics and continuation or refinement metadata.
- [ ] 5.5 Update topic index revision and event invalidation when canonical facets, decision membership, transitions, or lineage change while excluding browser-only state.
- [ ] 5.6 Add backend tests for every preset, composed filters, unknown classifications, independent state combinations, coherent edge projection, decision history, traversal bounds, lazy payload boundaries, and non-mutation.

## 6. Steering Application Service and Operator Routing

- [ ] 6.1 Implement one steering application service for `Explore this idea` and `Explore instead` with expected revision, expected state, idempotency key, reopening confirmation, Gate policy, and exact replacement ids.
- [ ] 6.2 Atomically record steering Decision Records, option membership, facet transitions, Research Inquiry or Research Task refs, provenance, and planned handoff or dispatch state.
- [ ] 6.3 Add GUI Backend and CLI steering surfaces that use the shared service and return accepted, conflict, Gate-required, dispatch-pending, and blocked results with durable refs.
- [ ] 6.4 Compose Project Operator instructions from exact Research Idea identity, latest Idea Realization refs, Decision Record, Research Inquiry, Research Task, and user prompt, then route them through the configured topic research actor adapter.
- [ ] 6.5 Record successful adapter delivery and preserve canonical decisions with pending or blocked retry state when delivery fails after commit.
- [ ] 6.6 Add integration tests for alongside exploration, replacement deferral, closed or deferred reopening, duplicate retries, stale revision conflicts, Gate pauses, transaction rollback, dispatch success, and post-commit dispatch failure.

## 7. Project Web Portfolio Experience

- [ ] 7.1 Extend TypeScript contracts, API clients, and observable view state with canonical facets, preset metadata, explicit filters, decision context, traversal responses, and steering action results.
- [ ] 7.2 Add shared portfolio presets and facet filters to Idea Graph and Idea Timeline with visible-versus-source counts, Needs Classification diagnostics, and restorable per-view state.
- [ ] 7.3 Render exploration, decision, evidence, visibility, archive, backend-selected, and UI-selected meaning independently in nodes, rows, hover previews, and idea details.
- [ ] 7.4 Add `Show descendants` and `Show ancestry` flows that compose with relation filters, preserve prior view state, and label incomplete traversal.
- [ ] 7.5 Add decision comparison and history views that show all recorded alternatives, outcomes, rationale, evidence refs, closure or deferral reasons, and reopen history.
- [ ] 7.6 Add confirmed `Explore this idea` and `Explore instead` dialogs with exact affected ideas, expected transitions, rationale, conflict review, Gate handling, and dispatch status.
- [ ] 7.7 Preserve lazy detail loading, revision-aware refresh, stable layout, collapsed graph controls, browser selection, and local filter responsiveness while adding the portfolio features.
- [ ] 7.8 Add TypeScript component, state, interaction, accessibility, and browser smoke tests for all presets, cross-view parity, independent facets, lineage flows, decision review, steering, conflicts, and lazy loading.

## 8. Contracts, Documentation, and Fixture Migration

- [ ] 8.1 Update `docs/ui/contracts/` and permissive Python schemas for portfolio facets, presets, filters, decision context, traversal, and steering request and response payloads.
- [ ] 8.2 Add shared Python and TypeScript fixtures that prove identical preset results, facet counts, independent combinations, decision option interpretation, and traversal completeness.
- [ ] 8.3 Update CLI, GUI, operator, and research workflow documentation with the new vocabulary, migration procedure, read-only versus mutating boundary, and steering examples.
- [ ] 8.4 Generate and review an explicit migration and repair plan for `isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model`, then apply it only after preview validation.
- [ ] 8.5 Verify the migrated flash-attention topic shows all proposed, unexplored, explored, selected, deferred, closed, and needs-classification ideas with canonical lineage and decision diagnostics.

## 9. End-to-end Validation

- [ ] 9.1 Run focused unit and integration suites for runtime storage, CLI, record acceptance, query indexing, GUI Backend, system-skill content, and Project Web.
- [ ] 9.2 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test` and resolve regressions within the change scope.
- [ ] 9.3 Build the latest Project Web bundle and run browser smoke tests against the flash-attention topic for initial load, presets, decision review, lineage traversal, and steering confirmation.
- [ ] 9.4 Run `openspec validate add-research-idea-portfolio-workflow --strict` and confirm every task and requirement has implementation or test evidence before completion.
