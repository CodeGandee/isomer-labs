# Manuscript Cleanliness

Use this reference before moving any local process, code, execution, artifact, or operator detail into paper-facing prose.

## Sort Source Material

Classify each candidate detail before writing:

- `claim`: a result, mechanism, limitation, comparison, or contribution supported by durable evidence. This can appear in main text.
- `experiment setting`: benchmark, dataset split, evaluator, comparator, intervention, metric, ablation design, or controlled factor. This can appear in main text when it helps readers interpret evidence.
- `reproducibility detail`: exact command shape, dependency, configuration, resource limit, local serving setup, or artifact layout. This usually belongs in appendix or reproducibility material.
- `implementation detail`: code path, module boundary, algorithm step, configuration value, or dataflow fact. This can appear only when verified and relevant to the method or reproducibility.
- `artifact history`: local branch names, run restarts, bundle status, record ids, command ids, prompt state, or process notes. This does not belong in manuscript prose.
- `operator instruction`: what the user asked, accepted, rejected, or prioritized. This does not belong in manuscript prose; convert only the scientifically relevant constraint into neutral experiment wording.

## Clean Prose Rules

Manuscript text should describe the research, not the agent process. Remove user/operator wording, route-control wording, restart language, local path names, tool promotion, TODOs, bundle-management language, raw execution shorthand, and unsupported claims about code or artifacts.

## Good Transformations

Bad process note: "The latest route accepted a dual endpoint setup." Main-text form: "All methods are compared under the same evidence budget." Reproducibility form: "The appendix reports the serving configuration used for the evaluation."

Bad process note: "The draft was restarted after the user requested a new paper line." Manuscript form: omit it and keep the fact in route records only.

Bad caption: "Publication-grade figure refinement is recommended." Caption form: state what the figure shows, which claim it supports, and what pattern the reader should remember.

## Code-Grounded Facts

Implementation surfaces can support prose when verified from current code, configuration, logs, or durable outputs. Examples include entrypoints, module boundaries, dataflow stages, control loops, evaluator wiring, ablation switches, objective weights, decoding settings, dataset filters, and generated traces. If a detail is only present in comments, planning notes, stale draft text, or recollection, do not write it as fact.

## Artifact Availability

Artifact availability must be globally consistent across abstract, main text, appendix, reproducibility statements, and bundle metadata. If a path exists but was not exercised by the evidence package, call it implemented or available, not experimentally validated.
