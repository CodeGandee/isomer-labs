---
name: deepresearch-science-scipkg
description: Use when the experimenter or analyst on a natural-science, engineering, simulation, or HPC quest is selecting or verifying a scientific software package (PySCF, LAMMPS, OpenMM, GROMACS, MEEP, Scanpy, Astropy, Geant4, OpenFOAM, CP2K, ABINIT, etc.), running a solver, analyzing a dataset, sweeping parameters, validating convergence/units/schema, submitting SLURM/SSH/HPC jobs, or recording science evidence as Science Evidence Graph nodes (package_check, computational_run, dataset_analysis, parameter_sweep, validation_result, claim) and claim-type discipline (computed/parsed/digitized/hypothesis). Read-only methodology lookup; surfaces the science-scipkg methodology reference (169 per-package cards), changes no quest state.
---

# science-scipkg (read-only methodology lookup)

## Overview

A read-only methodology lookup for the **experimenter and analyst** on natural-science / HPC quests: it surfaces the `science-scipkg` methodology reference (169 per-package routing cards plus the Science Evidence Graph contract) so the agent can pick the right scientific package, check it exists, run it in the shell, and record durable science evidence on the canonical `$HARNESS record apply` surface. This skill carries that reference in-folder and surfaces it; it makes no state change.

## When to Use

Invoke when the task carries any science / HPC signal:
- natural science, engineering, simulation, scientific software, numerical solver, model fitting, dataset analysis, HPC, SLURM, or SSH.
- a scientific package name (PySCF, LAMMPS, OpenMM, GROMACS, MEEP, Scanpy, Astropy, Geant4, OpenFOAM, CP2K, ABINIT, or similar) — you need which package fits, how to check it, evidence-path conventions, or pitfalls.
- a request to verify an environment, run a solver, reproduce a computational result, analyze scientific data, validate units/convergence/schema, or make a scientific claim.
- organizing a science task into a handoff or autonomous startup brief.
- recording science evidence as typed graph nodes (`package_check`, `computational_run`, `dataset_analysis`, `parameter_sweep`, `validation_result`, `claim`).

**When NOT to use:** this is advisory craft, not an authoritative state surface — never use it to finalize, mutate results, confirm GPU, or change quest state. It is for the experimenter/analyst roles, not the orchestrator's decision/finalize path. Do not treat it as a solver installer or package manager. Do not invent an `artifact.science` or top-level `science` MCP namespace on Houmao — there is no such runtime; record on `$HARNESS record apply`. Respect quest isolation: scope all paths to `runs/<this-quest-id>/...` and never reuse another quest's evidence.

## Workflow

1. **Index the methodology reference.** Run:
   `$HARNESS --via skill:deepresearch-science-scipkg:<your-role> knowledge cards --query scipkg`
   (or `$HARNESS --via skill:deepresearch-science-scipkg:<your-role> knowledge query --kind reference`). The `--via skill:...:<role>` stamp is for traceability only; read-only, so it records no row.
2. **Read the contract first for any science/HPC quest.** Open [references/science-evidence-graph.md](references/science-evidence-graph.md) — the six node types, the Houmao node→record mapping, claim-type discipline, and the HPC-via-shell workflow. The condensed version is inlined below; the full contract (mapping table, field spec, examples, validation) is the references page.
3. **Classify the task:** package check, computational run, dataset analysis, parameter sweep, validation, claim, or startup brief.
4. **Route the package.** If a package/domain is involved, search the compact index first, then open only the relevant cards — these are surfaced through `$HARNESS knowledge cards`:
   - `package-index.min.json` — compact index of the 169 cards; search this when the package/domain is unclear.
   - `domain-index.md` — cards grouped by inferred scientific domain.
   - `packages/<package_id>.md` — per-package card: knowledge URL, source URL, package-check pattern, expected science nodes, evidence paths, pitfalls.
   Treat cards as knowledge pointers only — they do **not** prove the solver, Python module, executable, license server, dataset, GPU backend, or HPC module exists.
5. **Check the package before any computed work.** Use the shell (Houmao `Bash`/terminal) for import, executable, version, environment-module, and small smoke-test checks. Save the result to a durable file (usually `validation/environment/<pkg>_doctor.json`). See [Package check](#package-check) below.
6. **Do the real work in the shell.** Solver commands, scripts, SSH, `sbatch`/`squeue`, log reads, and data analysis all run in the shell. For HPC follow [HPC via the shell](#hpc-via-the-shell).
7. **Record science evidence on the Houmao record surface.** Map each source `science.*` node onto a `$HARNESS record apply` record per [the node mapping](#node-types-and-houmao-mapping). Record runs/analyses/sweeps with concrete input/log/output/evidence paths; record validation separately from raw run status; record a `claim` only after evidence supports it, with a `claim_type`.
8. **Surface user-visible milestones/blockers** through the normal Houmao user-facing channel — but never as the only scientific evidence.
9. **Return** the method to the calling task and continue. The DB stays canonical; this craft is advisory.

If the task does not map cleanly to these steps, use your native planning tool to build a plan from the commands, node types, and constraints in this skill, then execute it.

## Node types and Houmao mapping

There is **no `artifact.science` runtime** on Houmao. Record science evidence with `$HARNESS record apply --json '{...}'` against the quest records, scoped to `runs/<quest-id>/...`. Map the source node types as follows (full table, notes, and field spec in [references/science-evidence-graph.md](references/science-evidence-graph.md)):

| Source `science.*` node | Houmao record (`record apply`) |
| --- | --- |
| `science.computational_run` | `experiment` (the run) / `result` (its outputs) — solver run, numerical computation, model fit |
| `science.dataset_analysis` | `analysis` (+ `result`) — analysis of existing data |
| `science.parameter_sweep` | `experiment` (campaign) / multiple `result` — swept campaign with per-point rows |
| `science.validation_result` | `measurement` / `analysis` — convergence/units/schema/control/tolerance checks, recorded separately from run status |
| `science.claim` | `claim` — carries claim-type discipline; link supporting records |
| `science.package_check` | **advisory, no first-class record** — attach to experiment/setup evidence (e.g. `validation/environment/<pkg>_doctor.json`) and reference from downstream records |

The v1 node types are: `package_check`, `computational_run`, `dataset_analysis`, `parameter_sweep`, `validation_result`, `claim`. Prefer `computational_run` over a simulation-only term when the work is solver execution, numerical computation, model fitting, or engineering computation. Node ids are stable logical ids: create one once, then **append updates** rather than mutating in place (append-only graph). Status values: `planned`, `ready`, `queued`, `running`, `success`, `failed`, `blocked`, `warning`, `passed`, `active`, `superseded`.

Where source text says `bash_exec(...)`, use the shell; where it says `artifact.science(...)`, use `$HARNESS record apply`; where it says `artifact.interact(...)`, use the normal Houmao user-facing milestone/blocker channel.

## Claim discipline

Every `claim` needs a `claim_type`:

- **`computed`** — produced by real execution in the current quest. Must link to a run/analysis/sweep node and to output/log/evidence paths or related node ids; add validation when convergence/correctness/units/schema matter.
- **`parsed`** — read from supplied or existing data. Must link the input data path and the parser/script path or command log; add schema/count checks when relevant.
- **`digitized`** — extracted from a paper figure, image, PDF plot, or OCR. Must link the source figure/image/PDF path and the digitization method/script, with an uncertainty note. **Never relabel digitized evidence as computed** unless the computation was actually rerun.
- **`hypothesis`** — plausible but not yet verified. Must give rationale and the intended validation path, with no phrasing implying the result already happened.

**Upgrade path:** to turn a `hypothesis` into `computed`, run the needed package check and computation, record the run/validation nodes, then append a new computed claim or supersede the old one. If computed evidence does not exist yet, record a `hypothesis`, a blocker, or a validation need instead.

## Package check

Package knowledge and solver installation are separate. Before any computed result:

1. Check import or executable existence.
2. Capture version and important backend details.
3. Run a minimal smoke test when the package supports it.
4. Save the check to a durable file, usually under `validation/environment/`.
5. Record a `package_check` (advisory node type; attach to experiment/setup evidence on Houmao).

**Python pattern:** run a short shell script that writes JSON, e.g.:

```bash
python - <<'PY'
import json, pathlib
result = {"package_id": "pyscf", "import": "failed", "version": None, "smoke": "not_run"}
try:
    import pyscf
    result["import"] = "passed"
    result["version"] = getattr(pyscf, "__version__", None)
    result["smoke"] = "passed"
except Exception as exc:
    result["error"] = repr(exc)
pathlib.Path("validation/environment").mkdir(parents=True, exist_ok=True)
pathlib.Path("validation/environment/pyscf_doctor.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
PY
```

**CLI solver pattern:** check executable path, version output, module/environment state if on HPC, and a minimal dry run or example input if available.

**Interpretation:** `passed` = the current environment can run at least the smoke path; `failed` = the package was attempted and did not work; `blocked` = could not check because credentials, data, modules, license, network, or user confirmation are missing. Record failed/blocked checks too when they explain a blocker, with `status="failed"` or `status="blocked"` and the log path.

## HPC via the shell

The runtime embeds no HPC scheduler. Operate HPC through the shell like any other terminal action:

1. Verify remote access or local scheduler availability.
2. Write a small job script or command file in the workspace.
3. Submit through the shell, e.g. `ssh cluster sbatch job.sh`.
4. Capture job id, queue state, and log paths.
5. Record a science node with `status="queued"` or `status="running"` and scheduler facts in `metadata` (`{"scheduler": "slurm", "job_id": "..."}`).
6. Monitor with low-frequency reads: `squeue` / `sacct`, `tail`/`sed -n` on logs, file-existence and output-JSON checks.
7. On completion, record a success/failed update and a validation node.

Cautions: do not claim a queued job has produced results; do not infer global completion from a truncated log window; do not poll rapidly for multi-hour jobs; treat missing modules/licenses/allocations as a blocker and record the failed/blocked package check.

## Startup-brief usage

For natural-science / engineering startup sessions, decide whether the task suits autonomous work:

- Ordinary bounded tasks (one package check, one local calculation, one dataset inspection, one result explanation) usually route to interactive/Copilot mode.
- Long simulation campaigns, HPC campaigns, paper reproduction, or idea-driven research route to autonomous mode only when compute, data, privacy, network, and success criteria are clear enough.
- Use the brief shape below as startup **context**; do not require the main agent to materialize a `goal.md` file. Include expected packages, the package-check requirement, expected science node types, HPC expectation, and whether solver installation is unknown.

```markdown
# Science Task Brief: <title>
## Objective            — what scientific/engineering result to produce
## What To Compute Or Analyze — concrete calculations, simulations, analyses, reproductions, optimizations
## Setup And Constraints — physical params, package prefs, datasets, hardware, SSH/HPC, privacy, units, budget, runtime
## Success Criteria      — quantitative convergence, correctness, reproducibility, comparison, validation
## Deliverables          — scripts, logs, outputs, figures, tables, reports, data files
## Evidence Recording Plan — expected package_check, computational_run, dataset_analysis, parameter_sweep, validation_result, claim nodes
```

For performance optimization of scientific code, a brief additionally fixes: package, language, hot-path target with unchanged scientific semantics, editable scope, performance metric + aggregation rule, correctness constraints (numeric invariants/tolerances, forbidden weakenings), representative train/test workloads, deterministic build commands, and thread/seed/MPI/launcher/input-file constraints.

## Task readiness (validation)

A science task is ready to report when all hold:
- package availability is checked or explicitly blocked;
- each run or analysis has concrete input/log/output/evidence paths when applicable;
- validation status is recorded separately from raw execution status when correctness matters;
- claims are typed as `computed`, `parsed`, `digitized`, or `hypothesis`;
- evidence nodes are linked so the graph can be reconstructed.

## Common Mistakes

- **Treating package cards as proof.** A card never proves the solver, module, executable, license, dataset, GPU backend, or HPC module exists — always shell-check first.
- **Mislabeling evidence.** Calling a result `computed` from a plot redraw, paper-figure reading, or guess. Use `digitized`/`parsed`/`hypothesis` and only upgrade to `computed` after a real rerun.
- **Weakening science to pass.** Loosening tolerances, filters, physical models, convergence criteria, or validation merely to make a run pass.
- **Blind HPC submission.** Submitting remote/HPC jobs without a log path and status-reading plan; claiming a queued job has results; inferring completion from a truncated log; rapid-polling multi-hour jobs.
- **Chat-only evidence.** Creating science evidence only in the user-facing channel — record durable nodes.
- **Mutating the graph.** Re-recording the same `node_id` or editing evidence in place — the graph is append-only; create once, then append updates.
- **Inventing a namespace.** Do not create an `artifact.science` or top-level `science` MCP namespace, or migrate any FermiLink runner/HPC-profile-manager/CLI/backend/UI into the runtime — real execution stays in the shell; record on `$HARNESS record apply`.
- **Overriding task evidence with card metadata.** Task-specific evidence wins over package-card metadata.
- **Crossing the boundary.** Never finalize, mutate results, confirm GPU, or change quest state from this read-only lookup; never reuse another quest's evidence (quest isolation).

## Rationalizations to reject

| Rationalization | Reality |
| --- | --- |
| "The card says PySCF is available, so I can skip the import check." | Cards are pointers, not proof. Shell-check import/executable/version before any computed work. |
| "I redrew the paper's figure, so the value is computed." | That is `digitized`. `computed` requires a real run in this quest with linked run/evidence nodes. |
| "The run barely failed convergence; I'll loosen the tolerance so it passes." | Never weaken tolerances/models/criteria to pass. Record the failure/validation truthfully. |
| "The job is queued, I'll record the expected result now." | A queued job has no results. Record `status="queued"` only; record outputs after completion. |
| "I'll just note the result in chat." | Chat is not durable scientific evidence. Record a node on the record surface. |
| "There's an `artifact.science` tool in the source examples, I'll call it." | No such runtime on Houmao. Map fields onto `$HARNESS record apply`. |
| "This card is for another quest's package, I'll reuse its evidence." | Quest isolation is absolute. Scope to `runs/<this-quest-id>/...` and collect fresh. |

## Audit / boundaries

- `--via skill:deepresearch-science-scipkg:<role>` is passed for traceability; read-only, so it records no row.
- This skill makes no state change; it surfaces a read-only methodology reference. The DB stays canonical and this craft is advisory, never an authoritative state surface.
- Never finalize, mutate results, confirm GPU, or change quest state from here.

## Package catalog provenance

The catalog is generated from FermiLink's skilled-scipkg channel and stored as native routing material (commit `93f089a333a43089fb1a08a73c37d05fd6683214`). Cards preserve package ids, descriptions, tags, knowledge URLs, source-archive URLs, and upstream project URLs; they do not vendor package source trees and do not install runtimes. If deeper package knowledge is downloaded during a quest, preserve the source URL and license context in the quest evidence; do not paste large knowledge-base text into reports without attribution. Do not use FermiLink as a runtime dependency.
