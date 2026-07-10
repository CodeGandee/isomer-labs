# External Owner Routing

## Ownership Boundary

Kaoju decides what survey evidence is needed and consumes returned refs. It does not replace the owners that govern platform state or execution.

| Need | Route |
| --- | --- |
| Topic Workspace topology, repository registration, managed dataset links, or Project state | Applicable operator or Topic Workspace owner skill. |
| Topic or Agent Workspace environment mutation | Applicable environment setup service skill. |
| Literature, repository, dataset, model, or artifact access | Resolved provider binding under its access and provenance contract. |
| Builds, tests, first-hand Runs, and raw outputs | Existing execution adapter; apply bounded-run guidance for resource-heavy work. |
| Credentials, private data, licenses, cost, or accelerators | Existing Gate owner before action. |
| Durable Artifacts, Evidence Items, Research Claims, Findings, Decision Records, Runs, and Provenance Records | Existing research-recording API or approved file-backed Artifact route. |

## Handoff Contract

State the requested operation, immutable inputs, destination purpose, resource boundary, Gate refs, and expected returned refs. On return, validate identity and status before using the result as evidence.

Owner absence, rejected authorization, access failure, or insufficient resources is a blocker. Record the attempted route and resume condition rather than teaching a bypass.
