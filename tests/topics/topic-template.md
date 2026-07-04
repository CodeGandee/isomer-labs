# Research Topic: `<topic-title>`

Briefly state the research problem as a question or investigation intent. Name the target system, phenomenon, dataset, method, or domain clearly enough that topic materialization and Topic Team Specialization can preserve the intended scope.

> Example: How can we predict `<target-outcome>` for `<target-system>` using `<evidence-or-method>` while respecting `<key-constraint>`?

## Abstract

Summarize the proposed research in one short paragraph: what the topic studies, why it matters, how the work will proceed, and what kind of result should count as useful.

> Example: This research studies `<topic>` because `<motivation>`. It will use `<method>` over `<evidence-source>` to produce `<expected-output>`, with success judged by `<validation-signal>`.

## Introduction and Background

Explain the practical or scientific context for the topic. Include the important domain terms, current situation, and why this problem is worth investigating now.

> Example: `<domain>` currently depends on `<current-practice>`, but `<limitation>` makes it difficult to `<desired-action>`. Recent work on `<prior-work-area>` suggests a path, but `<remaining-gap>` remains unresolved.

## Research Objective

State the unresolved problem, missing evidence, weak explanation, performance gap, or design uncertainty that motivates the topic, then express the objective as a concrete question or intended result. Keep this section stable unless the user explicitly revises the topic.

> Example:
>
> - Primary objective: `<objective>`
> - Supporting objective 1: `<objective>`
> - Supporting objective 2: `<objective>`
> - Supporting objective 3: `<objective>`

## Literature and Prior Work

List the bodies of work, papers, repositories, benchmarks, datasets, systems, or standards that should anchor the investigation. Use this section to show where the topic sits relative to existing knowledge.

> Example:
>
> - `<paper-or-repo>` for `<reason-it-matters>`.
> - `<benchmark-or-dataset>` for `<comparison-or-validation-role>`.
> - `<standard-or-doc>` for `<required-context>`.

## Methodology and Research Design

Describe the planned approach, evidence sources, tools, experimental or analytical design, comparison targets, validation method, and expected analysis path. Include materialization placeholders when the topic depends on host facts, external repositories, datasets, credentials, or environment discovery.

> Example: Materialize `<placeholder>` from `<evidence-source>`, collect `<inputs>`, run `<analysis-or-experiment>`, compare against `<baseline-or-criterion>`, and validate with `<validation-method>`.

## Expected Outcomes

Describe the expected outputs and why they matter. Outputs may include a model, benchmark result, implementation, ranked decision, explanation, dataset, report, View Manifest, Decision Record, or follow-up Research Inquiry.

> Example:
>
> - `<artifact-or-record>` that shows `<main-result>`.
> - `<evidence-item>` that supports `<claim>`.
> - `<follow-up-inquiry>` for `<remaining-question>`.

## Additional Requirements

Use this section for topic-specific preferences and constraints that do not fit the proposal sections above. Preferences capture what the user wants this research to include when feasible; constraints define the should, should not, must, and must not boundaries for valid work.

> Example: This topic should prioritize `<user-priority>`, avoid `<non-goal>`, and keep `<materialization-dependent-fact>` unresolved until evidence binds it.

### Preferences

List topic-specific preferences: things the user wants to have in this research when they are feasible and consistent with the objective.

> Example:
>
> - Prefer concrete research objectives over broad topic labels (if the topic is still broad, narrow it before specialization).
> - Prefer evidence-backed claims over plausible but unsupported explanations (if evidence is missing, record the gap or blocker).
> - Prefer explicit placeholders for host, dataset, repository, model, credential, or environment facts (if a value must be discovered during materialization, do not hard-code it in the topic).
> - Prefer outputs that can be inspected and resumed through Isomer records (if output is temporary or local-only, promote the accepted result to a durable record).

### Constraints

List hard or strong boundaries for the research. Each item should use `should`, `should not`, `must`, or `must not` so later agents can distinguish required behavior from preferences.

> Example:
>
> - The topic must state a concrete research problem or question.
> - The research objective must identify the research gap or uncertainty that motivates the work.
> - The methodology must describe how evidence will be produced, selected, or analyzed.
> - Materialization-dependent facts must remain placeholders until evidence resolves them.
> - The topic must not require timeline or budget sections.
> - The topic should name expected outputs and why they matter.
> - The topic should preserve enough prior-work context for later agents to understand why the question is worth asking.

## Related Links

List relevant source repositories, papers, documentation, datasets, benchmarks, standards, or other references.

> Example:
>
> - `<link-title>`: `<url>`
