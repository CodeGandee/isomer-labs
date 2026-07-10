# Survey Artifacts

## Core Artifacts

| Artifact | Minimum contents |
| --- | --- |
| Survey Contract | Question, boundary, source classes, coverage date, inclusion rules, desired depth, resources, Gates, and stop conditions. |
| Related-Work Catalog | Stable work id, work family, material identities, type, relevance, inclusion state, discovery route, exact refs, depth, and limitations. |
| Field Summary | Evidence-backed themes, chronology, taxonomy, representative works, implementation links, disagreements, gaps, and coverage limits. |
| Source Digest | Source Identity, exact inspected locators, claims, method details, implementation mapping, contradictions, depth, and evidence refs. |
| Source Access Blocker | Requested identity, attempted locators, failure evidence, effect on claims, and bounded recovery route. |
| Claim-Evidence Ledger | Research Claim ids, supporting and challenging Evidence Items, achieved depth, verdict, and unresolved gaps. |
| Comparison Intent Document | Candidate identities, reuse evidence, preparation route, inputs, evaluator, metrics, fairness rules, resources, Gates, and unresolved decisions. |
| Comparison Matrix | Dimensions or metrics, candidate cells, exact evidence or Run refs, variability, adaptations, and non-comparability reasons. |
| Topic Dataset Manifest | Dataset identity, name, description, external and managed locators, access, license, observed metadata, fingerprint or staleness policy, and provenance. |
| Audit Report | Checked scope, defects, severity, affected claims, accepted evidence, repair routes, and readiness decision. |
| Claim Status Table | Final claim, status, depth, verdict, accepted evidence refs, contradictions, and limitations. |
| Kaoju Dossier | Survey boundary, catalog and comparison views, findings, failures, limitations, unresolved questions, and exact output refs. |

## Delta Rule

Curated intake and direction expansion produce Survey Deltas rather than rewriting history invisibly. A delta states its base Artifact ref, added or changed entries, excluded or blocked items, affected claims, audit decision, and derived output refs.

## Storage Rule

These names are semantic contracts. Resolve their exact ids through `artifact-semantics.md`, then use the producer's `artifact-bindings.md` for persistence. Accepted structured state is canonical managed JSON; Markdown, CSV, matrices, and dossiers are derived renders or explicit exports. Follow `artifact-recording.md` for payload, lineage, worker-output, and large-material rules.
