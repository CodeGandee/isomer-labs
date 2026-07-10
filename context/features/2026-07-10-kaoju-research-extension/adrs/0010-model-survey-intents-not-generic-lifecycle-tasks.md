# Model Survey Intents, Not Generic Lifecycle Tasks

Status: accepted

Kaoju use cases shall represent user-visible survey goals. Generic research mechanics such as framing a question, discovering and acquiring sources, tracing a paper claim into code, pulling a newer repository revision, or resuming stale work are stage behavior inside a survey workflow rather than standalone Kaoju use cases.

## Considered Options

- Keep one use case for every public skill or pipeline stage. This was rejected because it makes internal mechanics look like independent survey goals and duplicates the end-to-end scenarios that already invoke those stages.
- Keep generic repository, environment, and refresh scenarios as Kaoju use cases. This was rejected because those behaviors belong to shared project, workspace, source-control, and execution infrastructure unless a concrete survey intent requires them.
- Preserve separate planning and execution use cases for the same empirical comparison. This was rejected because the user's goal is one actual-run comparison; the mandatory intent document and proceed checkpoint are phases within that use case.

## Consequences

- Broad field surveying owns source discovery, inclusion decisions, version-family resolution, and bounded material acquisition needed to produce its Related-Work Catalog and Field Summary.
- Testing a paper method owns both faithful intended-data reproduction and generated-data capability probes. Faithful and repaired Runs remain separate evidence within that use case.
- Comparing methods with actual Runs owns the Comparison Intent Document, clarification or proceed checkpoint, candidate preparation, controlled execution, fairness checks, and empirical Comparison Matrix.
- Audit and synthesis remains a standalone survey use case because reviewing and closing a survey evidence package is itself a user-visible survey goal.
- Claim tracing, source acquisition, environment preparation, refresh, and lineage handling remain reusable skill-stage contracts. Their direct invocability does not require separate use cases.
- A source or repository update becomes Kaoju use-case behavior only when it changes the evidence needed by an active survey goal. Routine update and checkout work routes to its generic owner.
- The consolidated use-case index is renumbered around survey intents. Removed identifiers are not retained as empty compatibility entries because the feature is still in draft design.
