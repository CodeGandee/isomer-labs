# Research Recording Contracts Design Choices

## Artifact Terminology

**Decision:** Keep **Artifact** as the canonical domain term. Use `artifact_id`, `artifact_ref`, or "Artifact reference" only when another record points to an Artifact.

## Rationale

The established domain language defines **Artifact** as a durable file or file-backed output produced or used during research work. The workspace engine data model also uses `artifact` as the record family. Introducing `ArtifactRef` as a first-class record family would create a second domain term for the same concept and would blur the distinction between a durable Artifact and a pointer to it.

## Consequences

- Research Recording Contracts name **Artifact** as the durable record family.
- Evidence Items, Decision Records, View Manifests, and other records may still carry Artifact references.
- Implementation names can use `artifact_id` or `artifact_ref` for fields, but user-facing docs and domain language should not introduce **Artifact Ref** as a separate concept.

## Finding Scope

**Decision:** Scope **Findings** primarily to **Research Inquiry** when an applicable inquiry exists. Use Research Topic or Topic Workspace scope only when the platform has not yet created a more specific Research Inquiry.

## Rationale

The established engine data model sketches `finding` with `research_inquiry_id`, and the domain model treats Research Inquiry as the question or line of inquiry under a Research Topic. Findings are reusable insights, but they usually answer or steer a question, so Research Inquiry is the right primary owner.

## Consequences

- Finding records should include a Research Inquiry reference when available.
- Topic-level and Topic Workspace-level Finding queries remain supported through scope refs, tags, and indexes.
- Topic-scoped Findings can exist before inquiry decomposition, but they should be linkable to a Research Inquiry later.

## Gate Resolution and Decision Records

**Decision:** A Gate resolution creates or links a **Decision Record** only when the user made a meaningful choice. A `cancelled` or `superseded` Gate can close without a Decision Record, but it must still have a **Provenance Record**.

## Rationale

The established domain language says a Decision Record may resolve a Gate and that a Decision Record records a meaningful choice. Treating every Gate closure as a Decision Record would create low-value records for cancellation or supersession, while omitting Decision Records for claim-shaping Gate choices would weaken auditability.

## Consequences

- `resolved` Gates that select a research route, waive a baseline, strengthen a claim, publish, archive, or approve another meaningful action should create or link a Decision Record.
- `cancelled` and `superseded` Gates need status, actor, timestamp, consequence summary, and Provenance Record refs, but not necessarily a Decision Record.
- Gate history remains auditable without overloading Decision Record as a generic lifecycle log.

## Research Claim Status and Evidence Relations

**Decision:** Use `open`, `supported`, `refuted`, and `withdrawn` as the Research Claim statuses. Treat support, contradiction, context, refutation support, and withdrawal rationale as Evidence Item or claim-evidence-link relations.

## Rationale

The established domain language says a Research Claim can be open, supported, refuted, or withdrawn, and that Evidence Items can support, contradict, or contextualize a claim. Keeping contradiction and context on the evidence relation supports mixed evidence without forcing the Research Claim into a single ambiguous status.

## Consequences

- A Research Claim with unresolved contradictory Evidence Items should remain `open` until a Decision Record or updated Evidence Item resolves the contradiction.
- Evidence Items and claim-evidence links carry relation meaning such as support, contradiction, context, refutation, or withdrawal rationale.
- GUI and validation can still display "contradicted evidence" or "contextual evidence" without adding `contradicted` or `contextualized` as Research Claim statuses.
