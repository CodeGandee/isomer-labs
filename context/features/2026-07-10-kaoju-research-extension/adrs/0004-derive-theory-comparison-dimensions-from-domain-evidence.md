# Derive Theory-Comparison Dimensions from Domain Evidence

Status: accepted

When a user asks Kaoju to compare named works in theory, Kaoju shall derive the interesting comparison dimensions from the survey domain, the selected works, and, when necessary, bounded discovery of survey, taxonomy, or reference papers. The resulting source-grounded Theory Comparison Artifact becomes part of the survey artifacts but does not require Runs or receive empirical `compared` verification depth.

## Considered Options

- Apply one fixed comparison checklist to every field. This was rejected because useful dimensions differ across domains and a universal grid would produce shallow or inapplicable cells.
- Require the user to provide every comparison dimension. This was rejected because discovering the field's meaningful distinctions is part of the requested Kaoju analysis.
- Treat every comparison request as an empirical benchmark study. This was rejected because it changes the user's intent, incurs unnecessary execution cost, and conflates source analysis with first-hand measurement.

## Consequences

- A Theory Comparison Contract records the named target works, comparison question, `comparison_mode: theory`, evidence boundary, and stopping criteria.
- Kaoju records a Comparison Dimension Set with a definition, rationale, applicability rule, and source refs for each dimension. Dimensions may cover problem formulation, assumptions, mechanism, representation, formal guarantees, complexity, intended setting, limitations, or other domain-specific concerns, but this list is not a mandatory template.
- If the selected works and existing survey artifacts do not justify a useful dimension set, Kaoju may discover additional reference works. Those works justify or challenge dimensions but do not silently become comparison targets.
- Each matrix cell links to exact source evidence and may state `not stated`, `not applicable`, `unclear`, or `disputed` rather than filling gaps by inference.
- Theory-comparison cells retain their achieved source verification depth of `reported`, `located`, or `inspected`. Verification depth `compared` remains reserved for controlled first-hand comparative evidence.
- The Theory Comparison Artifact includes the dimension rationale, evidence-linked matrix, narrative trade-off analysis, disagreements, limitations, and empirical follow-up questions, and is linked from the Related-Work Catalog, Field Summary, or Kaoju Dossier as applicable.
