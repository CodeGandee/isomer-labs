# Require a Comparison Intent Before Empirical Runs

Status: accepted

Before Kaoju compares methods A, B, C, or another candidate set through actual Runs, it shall create a durable Comparison Intent Document as part of the survey artifacts. The document translates the user's goal and Kaoju's field-informed judgment into a reviewable preparation plan, then waits for the user to clarify or proceed before acquisition, reproduction, reimplementation, environment mutation, or comparison Runs begin.

## Considered Options

- Start with the obvious benchmark and refine the protocol after seeing results. This was rejected because early choices about data, metrics, environments, and candidate adaptations can make later numbers unfair or unusable.
- Keep the plan only in the conversation. This was rejected because the survey needs a durable record of why candidates, metrics, dependencies, and reproduction work were chosen.
- Reproduce every candidate from scratch before planning the comparison. This was rejected because accepted prior evidence may be reusable, while some candidates may be blocked or not comparable before any expensive work starts.

## Consequences

- The Comparison Intent Document separates the user's requested outcome, Kaoju's proposed field-specific judgments, accepted prior evidence, unresolved questions, and preparation blockers.
- Each candidate receives a readiness entry covering source identity, implementation authority, run path, required code, datasets, models, environment, hardware, evaluator, existing reproduction evidence, staleness, and whether reuse, reproduction, repair, reimplementation, or a blocker is proposed.
- Prior reproductions may be reused only when their source revision, input and dataset contract, evaluator, metric definition, environment, hardware relevance, and lineage remain compatible with the planned comparison. Reuse and staleness decisions cite exact evidence refs.
- Reimplementation is never an implicit substitute for an unavailable implementation. It requires a separate proposal and Artifact identity, and its Runs cannot be labeled upstream-faithful reproduction.
- Kaoju proposes comparison dimensions, metrics, quality constraints, repetitions, statistics, tolerances, and fairness rules from the survey domain and source evidence. It records the rationale and marks unsupported details as unresolved rather than inventing commands or protocol facts.
- Creating the document may inspect the request, accepted survey artifacts, prior Runs, and already available source material, and may perform bounded non-mutating source discovery when field context is missing. New material acquisition, large downloads, environment mutation, reproduction, reimplementation, and comparison Runs wait for the user's proceed decision and any required Gates.
- After presenting the plan, Kaoju asks: `Do you want to clarify for more detail, or proceed?` Clarification follows UC-08's structured interaction and updates the document. Proceeding records the decision, freezes an executable Comparison Contract, and begins the accepted preparation route.
- If later acquisition or reproduction evidence invalidates the accepted plan, Kaoju versions the Comparison Intent Document and presents the material change before starting the affected comparison Runs.
