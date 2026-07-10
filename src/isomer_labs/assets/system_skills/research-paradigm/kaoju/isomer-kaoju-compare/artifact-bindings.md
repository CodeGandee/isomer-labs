# Compare Artifact Bindings

Read `../isomer-kaoju-shared/references/artifact-semantics.md` for meaning. This page is the physical and API authority for the rows below.

| Semantic id | Storage item | Record kind | Semantic label | Neutral profile | Producer | Consumers | Payload role | Lineage policy | Revision policy | Query metadata |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `kaoju:theory-comparison` | Managed JSON snapshot | `artifact` | `topic.records.artifacts` | `isomer:research/record-format/profile/kaoju/comparison/theory-comparison/v1` | isomer-kaoju-compare | audit, synthesize | Source-grounded theoretical comparison | `derived_from` compared Source Digests and dimension references | Separate per comparison boundary | dimensions, claims, procedure, evidence refs |
| `kaoju:comparison-matrix` | Managed JSON snapshot | `artifact` | `topic.records.artifacts` | `isomer:research/record-format/profile/kaoju/comparison/comparison-matrix/v1` | isomer-kaoju-compare | audit, synthesize, user | Audited cross-candidate view | `derived_from` intent, contract, candidate evidence and Runs | Separate per contract; revise only current presentation-neutral corrections | candidates, metrics, procedure, non-comparability |
| `kaoju:comparison-run` | Managed JSON snapshot plus raw-output refs | `run` | `topic.records.runs` | `isomer:research/record-format/profile/kaoju/run/comparison-run/v1` | isomer-kaoju-compare | comparison matrix, audit | One candidate attempt under frozen contract | `derived_from` comparison intent, decision, code, data, evaluator, and environment | Never revise attempt fidelity; separate adapted and repaired Runs | metrics, procedure, terminal status, output files |

## Normal Create

```text
isomer-cli --print-json ext research records create --topic <topic> --record-kind <row-record-kind> --semantic-label <row-semantic-label> --semantic-id <row-semantic-id> --format-profile <row-neutral-profile> --skill isomer-kaoju-compare --producer 'isomer-kaoju-compare' --consumer '<row-consumers>' --payload-file <payload-file> --metadata-json '{"actor_metadata":"<resolved>","procedure":"<theory-comparison-or-comparative-pass>"}' --files-json '<applicable-output-refs>'
```

## Lifecycle

Validate and create payload-first; list exact family and semantic id with optional `--latest-only`; show canonical payload; update only lifecycle metadata. Create theory comparisons, matrices, Runs, and follow-up evidence as bounded descendants with exact parents; never revise one Run into a repaired or adapted Run. Render on demand, export explicitly, and archive with the generic record commands while keeping raw outputs referenced.
