# Evidence Contract

## Required Dimensions

Record each applicable dimension independently:

| Dimension | Values or content |
| --- | --- |
| `verification_depth` | `discovered`, `metadata-checked`, `abstract-inspected`, `fulltext-inspected`, `source-inspected`, `executed`, or `compared` |
| `evidence_verdict` | `supports`, `partially-supports`, `contradicts`, `inconclusive`, `not-applicable`, or `blocked` |
| `run_purpose` | `reproduction`, `capability-probe`, `comparison`, `diagnostic`, or `repair-validation` |
| `execution_fidelity` | `upstream-faithful`, `adapted`, `reimplemented`, `repaired`, or `generated-input` |
| `input_basis` | Intended dataset, registered dataset id and fingerprint, generated dataset Artifact ref, or other exact input ref |
| `locator` | Exact source location or Run and raw-output ref |

Not every Evidence Item has every field. Source observations need source identity, locator, depth, and verdict; Runs also need purpose, fidelity, input basis, environment, and outputs.

## Depth Rules

Depth records what the agent actually checked, not what the material appears to contain. Discovery metadata cannot inherit full-text depth, code inspection cannot inherit execution depth, and a single-method Run cannot inherit comparative depth.

`compared` requires measurements from eligible candidates under an accepted Comparison Contract. A theory comparison remains source-inspected even when its matrix is complete.

## Evidence Acceptance

A provider response, search result, repository page, or command output is raw provenance. Promote it to an Evidence Item only after identity and relevance checks, then link the Evidence Item to each Research Claim it supports or challenges.

Preserve `not stated`, `not applicable`, `unclear`, `disputed`, and `not-comparable` rather than converting absence or incompatibility into a score.

## Generated Data

A Generated Dataset Artifact records its generator, schema, size, seeds, assumptions, checks, and limitations. Runs on that Artifact use `run_purpose: capability-probe`, `execution_fidelity: generated-input`, and no stronger than `verification_depth: executed`.
