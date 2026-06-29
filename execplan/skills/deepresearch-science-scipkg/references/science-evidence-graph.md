# Science Evidence Graph (contract)

> Detail page for the `deepresearch-science-scipkg` skill. The
> `references/package-index.min.json`, `references/domain-index.md`, and
> `references/packages/<package_id>.md` pointers below are the **runtime
> knowledge reference** surfaced through
> `$HARNESS --via skill:deepresearch-science-scipkg:<your-role> knowledge cards --query scipkg`
> (or `knowledge query --kind reference`) — they are data the harness serves, not
> files shipped inside this skill. The claim-type, package-check, HPC, and
> brief-template content from the other reference pages is inlined in the parent
> `SKILL.md`.

The source runtime recorded
science evidence through an `artifact.science(...)` MCP tool that maintained an
append-only "Science Evidence Graph" of typed nodes. Houmao has **no
`artifact.science` runtime**; record science evidence on the existing `$HARNESS`
record surface (`record apply`) instead. This file preserves the full node-type
contract, claim-type discipline, and HPC-via-shell workflow so an agent can
operate it on Houmao.

---

## Houmao mapping header (node type → `$HARNESS` record surface)

Record science evidence with `$HARNESS record apply --json '{...}'` against the
Houmao quest records, scoped to `runs/<quest-id>/...`. Map the source
`artifact.science(node_type=...)` nodes onto Houmao records as follows:

| Source `science.*` node | Houmao record (`record apply`) | Notes |
| --- | --- | --- |
| `science.computational_run` | `experiment` / `result` | A solver run / numerical computation / model fit. Use `experiment` for the run record and `result` for its measured outputs. |
| `science.dataset_analysis` | `analysis` (+ `result`) | Analysis of existing data; record the analysis and any derived results. |
| `science.parameter_sweep` | `experiment` (campaign) / multiple `result` | A swept campaign: one experiment record with per-point `result`/`measurement` rows. |
| `science.validation_result` | `measurement` / `analysis` (validation) | Convergence / units / schema / control / tolerance checks recorded separately from raw run status. |
| `science.claim` | `claim` | Carries the claim-type discipline below; link to its supporting records. |
| `science.package_check` | **no direct Houmao equivalent — advisory** | There is no first-class environment-check record. Record the package check as part of the experiment/setup evidence (e.g. an `experiment` setup note or an artifact at `validation/environment/<pkg>_doctor.json`) and reference it from downstream records. Treat the node-type discipline below as advisory craft. |

Notes that hold across the mapping:

- The Houmao **DB stays canonical**; these node-type rules are advisory craft, not
  an authoritative state surface. Do not invent an `artifact.science` namespace or
  a top-level `science` MCP namespace on Houmao.
- Where the source text says `bash_exec(...)`, use a normal shell
  (Houmao `Bash`/terminal). Where it says `artifact.science(...)`, use
  `$HARNESS record apply`. Where it says `artifact.interact(...)`, use the normal
  Houmao user-facing milestone/blocker channel.
- Node ids are stable logical ids (append-only). On Houmao,
  prefer one logical record per logical node id and append updates/new records
  rather than mutating evidence in place.

---

## One-sentence summary

Use the shell to do the real scientific work, use the package cards
(`references/packages/`, `references/package-index.min.json`,
`references/domain-index.md`) to choose the right package/reference path, and
record the durable Science Evidence Graph on the Houmao record surface.

## Match signals

Use this contract when the task includes any of these signals:

- natural science, engineering, simulation, scientific software, numerical
  solver, HPC, SLURM, SSH, model fitting, or dataset analysis
- package names such as PySCF, LAMMPS, OpenMM, GROMACS, MEEP, Scanpy, Astropy,
  Geant4, OpenFOAM, CP2K, ABINIT, or similar scientific packages
- requests to verify an environment, run a solver, reproduce a computational
  result, analyze scientific data, validate units/convergence/schema, or make a
  scientific claim
- organizing a science task into a handoff or autonomous startup brief

## Control surface

- Real execution: always the shell (`bash_exec(...)`).
- Evidence records: `$HARNESS record apply` (used
  `artifact.science(...)`).
- User-visible milestones or blockers: the normal Houmao user-facing channel
  (used `artifact.interact(...)`).
- Package knowledge: this skill's references and package cards.
- Do not migrate any FermiLink runner, HPC profile manager, CLI workflow,
  backend, or UI into the runtime. The package cards are routing references; real
  execution stays in the shell.

## Progressive disclosure

Read only the references needed for the active task:

- `references/package-index.min.json`: compact index of the 169 package cards;
  search this first when a package/domain is unclear.
- `references/domain-index.md`: human-readable grouping by inferred scientific
  domain.
- `references/packages/<package_id>.md`: package-specific routing card with
  knowledge URL, source URL, package-check pattern, expected science nodes,
  evidence paths, and pitfalls.
- `references/package-check-playbook.md`: package availability checks before
  treating a solver as usable.
- `references/artifact-science-tool.md`: the original `artifact.science(...)`
  contract and examples (runtime; on Houmao read it as the field
  spec and map fields onto `record apply`).
- `references/hpc-via-bash-exec.md`: SSH, scheduler, queue, and remote-log
  discipline through the shell.
- `references/claim-type-discipline.md`: computed / parsed / digitized /
  hypothesis claim discipline.
- `references/science-task-brief-template.md`: startup brief shape; use as
  context, not as a required `goal.md` file.

## Workflow

1. Classify the task: package check, computational run, dataset analysis,
   parameter sweep, validation, claim, or startup brief.
2. If a package/domain is involved, search `references/package-index.min.json`
   and open only the relevant `references/packages/<package_id>.md` cards.
3. Treat package cards as knowledge pointers only. They do not prove the solver,
   Python module, executable, license server, dataset, GPU backend, or HPC
   module exists.
4. Before computed work, use the shell for import, executable, version,
   environment-module, and small smoke-test checks when relevant.
5. Record package checks as a `package_check` (advisory node type; on Houmao,
   attach to the experiment/setup evidence — see the mapping header).
6. Run solver commands, scripts, SSH, sbatch/squeue, log reads, and data
   analysis through the shell.
7. Record scientific execution as `computational_run`, `dataset_analysis`, or
   `parameter_sweep` (Houmao: `experiment`/`result`/`analysis`) with concrete
   input, log, output, and evidence paths.
8. Validate convergence, units, schema, controls, tolerances, seeds, or
   physical/statistical invariants, then record a `validation_result` (Houmao:
   `measurement`/`analysis`).
9. Record a `claim` only after evidence paths or related science nodes support
   it.
10. Use the user-facing channel for decisions or milestones that the user should
    see, but never as the only scientific evidence.

Science node ids are stable logical ids, not mutable file slots. Create a new
node id once. If status, evidence, or interpretation changes later, append an
update so the graph remains append-only. If a package check fails or is blocked
and that fact affects the route, record it as a `package_check` with
`status="failed"` or `status="blocked"` and point to the log or diagnostic file.

## Science node types

Use only these v1 node types unless the runtime contract changes:

- `science.package_check`
- `science.computational_run`
- `science.dataset_analysis`
- `science.parameter_sweep`
- `science.validation_result`
- `science.claim`

Prefer `science.computational_run` over a narrower simulation-only term when the
work is solver execution, numerical computation, model fitting, or engineering
computation.

### Node field spec (from `references/artifact-science-tool.md`)

Each node carries a common field set; the canonical example and the full field
list live in `references/artifact-science-tool.md`. Core fields:

- `node_type`, `node_id` (stable), `title`, `summary`, `status`
- `domain`, `package_id`, `task_type`
- `key_results` (list of `{label, value, unit}`)
- `input_paths`, `log_paths`, `output_paths`, `evidence_paths`
- `parent_node_ids`, `related_node_ids`
- `metadata` (e.g. scheduler facts: `{"scheduler": "slurm", "job_id": "..."}`)
- `claim_type` (claims only), `trust` (claims)

Status values: `planned`, `ready`, `queued`, `running`, `success`, `failed`,
`blocked`, `warning`, `passed`, `active`, `superseded`.

Required evidence rules:

- a passed `package_check` needs environment-check evidence; failed/blocked
  checks that determine the route should also be recorded with diagnostic
  evidence.
- a successful `computational_run` needs at least one input, log, output, or
  evidence path.
- a `validation_result` must reference a run, analysis, or sweep through
  `related_node_ids` or `parent_node_ids`.
- a `claim` needs `claim_type`; a `computed` claim needs evidence paths or
  related computed/validation nodes.

## Claim discipline

Every `claim` needs `claim_type` (full discipline in
`references/claim-type-discipline.md`):

- `computed`: produced by real execution in the current quest. Must link to a
  run/analysis/sweep node and to output/log/evidence paths or related node ids;
  add validation when convergence/correctness/units/schema matter.
- `parsed`: read from supplied or existing data. Must link the input data path
  and the parser/script path or command log; add schema/count checks when
  relevant.
- `digitized`: extracted from a paper figure, image, PDF plot, or OCR. Must link
  the source figure/image/PDF path and the digitization method/script, with an
  uncertainty note. Never relabel digitized evidence as computed unless the
  computation was actually rerun.
- `hypothesis`: plausible but not yet verified. Must give rationale and the
  intended validation path, with no phrasing implying the result already
  happened.

Upgrade path: to turn a `hypothesis` into `computed`, run the needed package
check and computation, record the run/validation nodes, then append a new
computed claim or supersede the old one. If computed evidence does not exist yet,
record a `hypothesis`, a blocker, or a validation need instead.

## HPC via the shell

The runtime does not embed an HPC scheduler. Operate HPC through the shell like
any other terminal action (full detail in `references/hpc-via-bash-exec.md`):

1. Verify remote access or local scheduler availability.
2. Write a small job script or command file in the workspace.
3. Submit through the shell, e.g. `ssh cluster sbatch job.sh`.
4. Capture job id, queue state, and log paths.
5. Record a science node with `status="queued"` or `status="running"` and
   scheduler facts in `metadata` (`{"scheduler": "slurm", "job_id": "..."}`).
6. Monitor with low-frequency reads: `squeue` / `sacct`, `tail`/`sed -n` on logs,
   file-existence and output-JSON checks.
7. On completion, record a success/failed update and a validation node.

Cautions: do not claim a queued job has produced results; do not infer global
completion from a truncated log window; do not poll rapidly for multi-hour jobs;
treat missing modules/licenses/allocations as a blocker and record the
failed/blocked package check.

## Startup-brief usage

For natural-science or engineering startup sessions, decide whether the task is
actually suited to autonomous work:

- Ordinary bounded tasks (one package check, one local calculation, one dataset
  inspection, one result explanation) usually route to interactive/Copilot mode.
- Long simulation campaigns, HPC campaigns, paper reproduction, or idea-driven
  research can route to autonomous mode only when compute, data, privacy,
  network, and success criteria are clear enough.
- Use the brief shape from `references/science-task-brief-template.md` as startup
  context; do not require the main agent to materialize a `goal.md` file.
- Include expected packages, the package-check requirement, expected science node
  types, HPC expectation, and whether solver installation is unknown.

## Package catalog provenance

The package catalog is generated from FermiLink's skilled-scipkg channel and
stored as native routing material (commit
`93f089a333a43089fb1a08a73c37d05fd6683214`). The cards preserve package ids,
descriptions, tags, knowledge URLs, source archive URLs, and upstream project
URLs. They do not vendor package source trees and do not install runtimes. If
deeper package knowledge must be downloaded during a quest, preserve the source
URL and license context in the quest evidence; do not paste large knowledge-base
text into reports without attribution.

## AVOID / pitfalls

- Do not treat this contract as a solver installation or package manager.
- Do not call a result `computed` from a plot redraw, paper figure reading, or
  guess.
- Do not weaken tolerances, filters, physical models, convergence criteria, or
  validation checks merely to make a run pass.
- Do not submit remote/HPC jobs without a log path and status-reading plan.
- Do not create science evidence only in chat.
- Do not let package-card metadata override task-specific evidence.
- Do not use FermiLink as a runtime dependency; use the native package cards as
  routing references and keep real execution in the shell.

## Validation (task readiness)

A science task is ready to report when these are true:

- package availability is checked or explicitly blocked
- each run or analysis has concrete input/log/output/evidence paths when
  applicable
- validation status is recorded separately from raw execution status when
  correctness matters
- claims are typed as computed, parsed, digitized, or hypothesis
- evidence nodes are linked so the graph can be reconstructed
