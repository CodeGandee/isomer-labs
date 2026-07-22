# Default Mindset Questions

## Status

Revised and accepted on 2026-07-21. The inventory sizes, survey-relative posture, and exact question ids and wording are final for packaged seed JSON; topic-derived Mindset Sources may adapt the fixed inventory under the accepted generation rules.

## Decision

The first version packages compact seed JSON with 8 fixed questions for `paper.deep-dive`, 6 fixed questions for `paper.skimming`, and 8 fixed questions for `source-code.ingest`, plus one repeatable `additional-questions` collector in each seed. Every fixed and collector question has `additional_notes` set to `""`. The Kaoju topic-creation skill reads `topic.intent.overview` and may adapt, add, remove, or replace fixed questions and populate notes while preserving the stable key and collector. It may copy an unchanged seed when specialization adds no value. Every question is evaluated relative to the active survey rather than as an isolated source-summary prompt. Every Mindset Record snapshots the exact resulting Source question and notes, records an answer state, and cites exact evidence refs when available. An agent must use `unresolved` or `not_applicable` rather than infer an unsupported answer.

## Accepted Active Survey Context

“Survey topic” maps to the canonical Research Topic plus the current `KAOJU:SURVEY-CONTRACT`, including its accepted survey question, boundary, inclusion and exclusion rules, desired depth, and deliverable purpose. When present, the Mindset Record also uses the selected Direction Set or direction-scoped Reading List and the current Related-Work Catalog and Claim-Evidence Ledger refs.

## Accepted Question Lists

### `paper.deep-dive`

1. `survey-role`: How does this paper relate to the active survey question, accepted boundary, and selected direction, and what role could it play in the survey?
2. `survey-relevant-claims`: Which of the paper's claims directly answer, support, challenge, refine, or fall outside the active survey question?
3. `portfolio-novelty`: Relative to works already represented in the survey, what is genuinely new, duplicative, complementary, or contradictory?
4. `comparison-mechanism`: Which mechanisms, assumptions, definitions, and method components matter to the survey's comparison dimensions?
5. `survey-claim-evidence`: Which exact sections, equations, figures, tables, or appendices support or challenge the survey-relevant claims, and what is my interpretation rather than a source statement?
6. `evaluation-transferability`: Do the datasets, metrics, baselines, controls, and ablations test the claims under conditions that fit the survey's scope and intended comparisons?
7. `boundary-limitations`: Which limitations, failure modes, contradictions, missing implementation details, or reproducibility gaps restrict how this paper can be used in the survey?
8. `survey-update-and-gaps`: What updates to the survey taxonomy, comparison structure, Claim-Evidence Ledger, or reading path should I recommend, and which survey questions remain unresolved?

### `paper.skimming`

1. `survey-fit`: What exact work and version am I inspecting, and how does it fit the active survey question, boundary, and selected direction?
2. `topic-relevant-claim`: What survey-relevant problem and principal claim can I establish at the inspection depth actually achieved?
3. `portfolio-relation`: Does this work add a new contribution, duplicate known work, complement a current category, or challenge an existing survey claim?
4. `survey-evidence-signal`: What is the strongest visible evidence relevant to the survey, where is it located, and what evidence depth have I actually achieved?
5. `scope-and-credibility-risk`: Which assumptions, evaluation settings, missing comparisons, contradictions, or identity and access uncertainties limit its relevance to this survey?
6. `survey-triage`: What survey disposition should I recommend: deep dive, defer, or exclude from the current boundary, what gap would it fill, and what must be verified first?

### `source-code.ingest`

1. `survey-role-and-identity`: How does this exact repository revision relate to the active survey question, selected direction, and associated works, and what are its source, license, and access posture?
2. `survey-relevant-architecture`: Which entrypoints and modules implement the concepts, methods, data paths, or evaluators that matter to the survey?
3. `claim-code-map`: Which survey-relevant paper claims, equations, or algorithms map to exact files and symbols, and what remains unmatched?
4. `behavior-path`: How do inputs, preprocessing, method logic, evaluation, and outputs connect for the behavior relevant to the survey?
5. `comparison-sensitive-configuration`: Which defaults, flags, seeds, thresholds, dependencies, hardware, datasets, or services could change the survey's interpretation or comparison?
6. `survey-evidence-surfaces`: What do tests, examples, benchmarks, and existing logs establish about the survey-relevant claims without executing the repository?
7. `paper-code-divergence`: What is missing, stale, stubbed, inconsistent, or divergent from the associated paper or the role assigned to this source in the survey?
8. `survey-readiness-and-risks`: What further source inspection, environment preparation, bounded trial, or reproduction should I recommend for the survey, and what blockers, side effects, or resource risks qualify that recommendation?

## Repeatable Additional-Question Collector

Each packaged seed and topic-derived Mindset Source contains collector `additional-questions` with prompt: “Did the user explicitly assign any additional questions to this Mindset Record that the fixed Mindset Source questions do not cover?” Its answer expectation is: “Register only questions explicitly targeted to the Mindset Record. Save ordinary paper or source-code questions and findings in the applicable reading Artifacts. If no additional questions were explicitly assigned, record none.” Its packaged `additional_notes` is empty. The collector does not count toward the packaged 8/6/8 fixed inventories.

## Boundary

These are reflective questions, not Workflow Stages. They do not direct acquisition, execution, mutation, Gate satisfaction, or evidence acceptance. Existing Kaoju procedures retain authority over those actions. Applicable procedures must resolve the topic Mindset Source, snapshot it into a Mindset Record, and inject the Record through accepted preflight and handoff checkpoints so the executing agent answers the immutable Run inventory.
