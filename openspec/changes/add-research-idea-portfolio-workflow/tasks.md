## 1. Domain and Runtime Schema

- [x] 1.1 Update the canonical domain-language document to define independent Research Idea exploration, decision, evidence, archive, and visibility facets, closure reasons, state transitions, and decision option membership.
- [x] 1.2 Add typed Research Idea facet vocabularies, transition records, decision-option records, operation correlation, and deprecated compatibility-status projection to runtime record models.
- [x] 1.3 Add an additive SQLite migration for Research Idea facet columns, state-transition rows, decision-option membership rows, idempotency records, constraints, and query indexes while preserving existing status data.
- [x] 1.4 Implement runtime store create, read, list, and atomic mutation methods for facets, transitions, decision options, and operation ids with topic-boundary and ref validation.
- [x] 1.5 Add unit tests for valid independent facet combinations, invalid vocabularies, closure reason requirements, topic isolation, transaction rollback, and compatibility-status projection.

## 2. CLI, Validation, and Legacy Migration

- [x] 2.1 Extend `ext research ideas upsert` with initial canonical facet arguments and deprecate direct status mutation without removing compatibility reads.
- [x] 2.2 Add deterministic Research Idea transition and decision-option maintenance commands that require actor, rationale or reason, expected state, and applicable durable refs.
- [x] 2.3 Extend Research Idea query commands with facet, archive, visibility, generation, and Decision Record filters and complete decision-context output.
- [x] 2.4 Add bounded ancestor and descendant traversal commands with relation-kind, depth, node, and edge limits plus explicit completeness metadata.
- [x] 2.5 Implement preview and apply legacy-status migration using the conservative mapping in `design.md`, preserved original values, migration provenance, and `unknown` diagnostics.
- [x] 2.6 Extend Research Idea validation to cover invalid facets, incomplete transitions, compatibility projection conflicts, missing decision options, stale refs, and ambiguous legacy classifications.
- [x] 2.7 Add CLI and runtime tests for JSON determinism, preview non-mutation, apply idempotency, partial historical decision context, traversal bounds, and migration rollback safety.

## 3. Recording Contracts and Producer Integration

- [x] 3.1 Extend structured idea-bearing payload and profile mappings to accept authored facets, transition context, decision option sets, closure reasons, exact Idea Realization paths, and producer-independent artifact-family mappings.
- [x] 3.2 Make record acceptance and promised canonical Research Idea effects one transaction, returning all created or updated idea, realization, lineage, decision, and transition refs.
- [x] 3.3 Reject partial canonical effects for profiles that promise idea recording while continuing to accept non-idea-bearing records without inferred ideas.
- [x] 3.4 Add recording tests for raw slates, candidate frontiers, Kaoju Direction Sets, exploration outputs, evidence assessments, selected hypotheses, rejected or deferred ledgers, reopening decisions, and atomic failure.

## 4. System-skill Guidance

- [x] 4.1 Promote or create one paradigm-neutral, independently installed Research Idea Recording reference with the new facet vocabulary, durable-concept test, transition commands, decision-option requirements, migration posture, and accepted-output verification checklist.
- [x] 4.2 Update idea-producing DeepSci skill workflows and placeholder bindings to record canonical facets, exact realizations, lineage, generations, considered option sets, and terminal result refs at acceptance time.
- [x] 4.3 Add a versioned idea-bearing Kaoju Direction Set payload and binding profile with per-proposal canonical `idea_id`, exact object path, generation, authored option outcome, disposition rationale, closure reason, atomic-effect declaration, and readable legacy-profile migration posture.
- [x] 4.4 Update `isomer-kaoju-frame`, `isomer-kaoju-pipeline`, and `choose-directions` so actor-confirmed Direction Set acceptance atomically records every proposal concept, the Direction Set Decision Record, proposal generation, exact realizations, option membership, justified transitions, and terminal result refs.
- [x] 4.5 Update `isomer-kaoju-shared`, `isomer-kaoju-discover`, `isomer-kaoju-compare`, `isomer-kaoju-audit`, `isomer-kaoju-synthesize`, and `isomer-kaoju-write` with profile-specific direction mappings, explicit exploration and evidence updates, concept-changing follow-up lineage, and guardrails that keep sources, methods, claims, repair routes, and paper structure out of the idea portfolio unless explicitly promoted.
- [x] 4.6 Verify a Kaoju-only system-skill installation resolves the paradigm-neutral recording contract without DeepSci, and update system-skill manifest, inspection, install, version, and extension-isolation tests as required.
- [x] 4.7 Audit remaining packaged research-paradigm skills and extensions that create, select, defer, close, reopen, support, or refute Research Ideas and route them through the shared recording contract.
- [x] 4.8 Add skill-content tests that reject overloaded status-only instructions, Markdown-only completion claims, copied divergent vocabularies, missing canonical write verification, Kaoju-to-DeepSci dependencies, and automatic idea creation for non-concept survey candidates.

## 5. Query Index and GUI Backend Read Models

- [x] 5.1 Project every topic-scoped canonical Research Idea regardless of producer extension or artifact family, together with facets, decision summaries, transition refs, classification diagnostics, and facet counts, into lightweight query-index and Project Web read models.
- [x] 5.2 Implement the fixed portfolio preset registry and explicit filter composition with coherent filtered edges, source counts, visible counts, applied predicates, and completeness metadata.
- [x] 5.3 Add read-only decision-context endpoints that return recorded alternatives, outcomes, rationale, consequences, closure or deferral reasons, reopen history, and supporting refs without backfilling missing context.
- [x] 5.4 Add bounded ancestor and descendant read endpoints over canonical Idea Lineage Edges with incomplete-result diagnostics and continuation or refinement metadata.
- [x] 5.5 Update topic index revision and event invalidation when canonical facets, decision membership, transitions, or lineage change while excluding browser-only state.
- [x] 5.6 Add backend tests for every preset, composed filters, unknown classifications, independent state combinations, coherent edge projection, decision history, traversal bounds, lazy payload boundaries, non-mutation, Kaoju-only topics, mixed DeepSci and Kaoju topics, and unprojected legacy Direction Set diagnostics.

## 6. Steering Application Service and Operator Routing

- [x] 6.1 Implement one steering application service for `Explore this idea` and `Explore instead` with expected revision, expected state, idempotency key, reopening confirmation, Gate policy, and exact replacement ids.
- [x] 6.2 Atomically record steering Decision Records, option membership, facet transitions, Research Inquiry or Research Task refs, provenance, and planned handoff or dispatch state.
- [x] 6.3 Add GUI Backend and CLI steering surfaces that use the shared service and return accepted, conflict, Gate-required, dispatch-pending, and blocked results with durable refs.
- [x] 6.4 Compose Project Operator instructions from exact Research Idea identity, latest Idea Realization refs, Decision Record, Research Inquiry, Research Task, and user prompt, then route them through the configured topic research actor adapter.
- [x] 6.5 Record successful adapter delivery and preserve canonical decisions with pending or blocked retry state when delivery fails after commit.
- [x] 6.6 Add integration tests for alongside exploration, replacement deferral, closed or deferred reopening, duplicate retries, stale revision conflicts, Gate pauses, transaction rollback, dispatch success, and post-commit dispatch failure.

## 7. Project Web Portfolio Experience

- [x] 7.1 Extend TypeScript contracts, API clients, and observable view state with canonical facets, preset metadata, explicit filters, decision context, traversal responses, and steering action results.
- [x] 7.2 Add shared portfolio presets and facet filters to Idea Graph and Idea Timeline with visible-versus-source counts, Needs Classification diagnostics, and restorable per-view state.
- [x] 7.3 Render exploration, decision, evidence, visibility, archive, backend-selected, and UI-selected meaning independently in nodes, rows, hover previews, and idea details.
- [x] 7.4 Add `Show descendants` and `Show ancestry` flows that compose with relation filters, preserve prior view state, and label incomplete traversal.
- [x] 7.5 Add decision comparison and history views that show all recorded alternatives, outcomes, rationale, evidence refs, closure or deferral reasons, and reopen history.
- [x] 7.6 Add confirmed `Explore this idea` and `Explore instead` dialogs with exact affected ideas, expected transitions, rationale, conflict review, Gate handling, and dispatch status.
- [x] 7.7 Preserve lazy detail loading, revision-aware refresh, stable layout, collapsed graph controls, browser selection, and local filter responsiveness while adding the portfolio features.
- [x] 7.8 Add TypeScript component, state, interaction, accessibility, and browser smoke tests for all presets, cross-view parity, independent facets, lineage flows, decision review, steering, conflicts, lazy loading, Kaoju-only portfolios, and mixed-paradigm portfolios without Kaoju-specific graph parsing.

## 8. Contracts, Documentation, and Fixture Migration

- [x] 8.1 Update `docs/ui/contracts/` and permissive Python schemas for portfolio facets, presets, filters, decision context, traversal, and steering request and response payloads.
- [x] 8.2 Add shared Python and TypeScript fixtures that prove identical preset results, facet counts, independent combinations, decision option interpretation, traversal completeness, and cross-paradigm union semantics for Kaoju-only and mixed DeepSci and Kaoju topics.
- [x] 8.3 Update CLI, GUI, operator, and research workflow documentation with the new vocabulary, migration procedure, read-only versus mutating boundary, and steering examples.
- [x] 8.4 Add preview and apply migration for legacy Kaoju Direction Sets that creates one idea per durable proposal, preserves direction ids as aliases, records directly justified selection outcomes, diagnoses unknown dispositions and rationale, and never invents lineage.
- [x] 8.5 Generate and review an explicit migration and repair plan for `isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model`, then apply it only after preview validation.
- [x] 8.6 Verify the migrated flash-attention topic shows all proposed, unexplored, explored, selected, deferred, closed, and needs-classification ideas with canonical lineage and decision diagnostics.
- [x] 8.7 Create or migrate representative Kaoju-only and mixed DeepSci and Kaoju topic fixtures, then verify every survey direction appears in Idea Graph and Idea Timeline with correct presets, exact realization detail, decision context, lineage, and steering eligibility.

## 9. End-to-end Validation

- [x] 9.1 Run focused unit and integration suites for runtime storage, CLI, record acceptance, query indexing, GUI Backend, system-skill content, and Project Web.
- [x] 9.2 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test` and resolve regressions within the change scope.
- [x] 9.3 Build the latest Project Web bundle and run browser smoke tests against the flash-attention topic plus Kaoju-only and mixed-paradigm fixtures for initial load, complete direction visibility, presets, decision review, lineage traversal, exact realization detail, and steering confirmation.
- [x] 9.4 Run `openspec validate add-research-idea-portfolio-workflow --strict` and confirm every task and requirement has implementation or test evidence before completion.
