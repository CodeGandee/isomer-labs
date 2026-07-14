# Agent Task

## Objective

Implement the full Kaoju Survey Process user-facing workflow layer for the `2026-07-14-kaoju-survey-process-usecases` feature. The layer must expose the ten use cases (`uc-01` through `uc-10`) as durable, state-DB-backed workflows that an operator, researcher, or Topic Actor can invoke from a Project Operator Session. The implementation should reuse existing Kaoju stage skills (`isomer-kaoju-frame`, `isomer-kaoju-discover`, `isomer-kaoju-acquire`, `isomer-kaoju-examine`, `isomer-kaoju-audit`, `isomer-kaoju-synthesize`, `isomer-kaoju-write`) rather than re-implementing them, and must store metadata in the topic workspace state database with filesystem links for every durable artifact.

## Required Use Cases

- `uc-01`: Survey Direction From Topic — propose one or more bounded survey directions from a topic or research question, let the actor select or refine, and persist the chosen next-direction set.
- `uc-02`: Collect Online Info And Build In-Depth Reading List — for an accepted direction, collect online sources and compose a direction-owned reading list with 3 priority + 3 secondary items (best effort), plus metadata, saved for actor inspection.
- `uc-03`: Ingest Reading Item In Depth — read a selected reading item (paper, article, documentation) and produce structured survey records; download papers/repos to the topic artifact library when possible, fall back to online reading when access is blocked.
- `uc-04`: Write Paper From Digested Materials — from accepted audit/synthesis records, produce a content-first MyST paper draft through a two-stage structure-then-fill workflow.
- `uc-05`: Paper Template Manual Editing And Apply — extract the MyST paper template to a workspace directory for manual editing, then apply the revised template and regenerate the paper.
- `uc-06`: Create Paper PDF — generate a TeX template from the accepted MyST draft, produce the TeX paper, compile to PDF, and keep both templates as durable artifacts.
- `uc-07`: Export Survey Records To LLM Wiki And Deploy Viewer — export survey records into an LLM Wiki (human-viewable + machine-friendly metadata) and deploy the bundled web viewer; the viewer manifest points at the wiki so it can be restarted later.
- `uc-08`: Ingest Source Code By Link Or Name — check out and ingest a source-code repository by URL/name; focus on specific aspects the actor cares about; look up the repo online if only a name or paper reference is given.
- `uc-09`: Prepare Code Run Environment — inspect a repo, update the topic env gate (intent + derived), install dependencies with Pixi using a reuse-first strategy, and verify with a smoke-run script.
- `uc-10`: Run Source Code Trial — plan and execute a data-driven trial of the prepared source code using an existing dataset or generated data, and record the trial result.

## Design References

- [Feature Requirement](feature-requirement.md)
- [Use Cases](usecases/README.md)
- [Public Interfaces](design/public-interfaces.md)
- Existing Kaoju skill suite: `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/`
- Prior analysis of the Kaoju suite: `.imsight-arts/agent-skill-handling/analysis/kaoju-suite/`
- Example topic workspace: `isomer-content/topic-ws/predictive-memory-tiering-survey/`

## Implementation Instructions

### 1. State database and artifact layer

Before implementing individual use cases, ensure every workflow can:

- Query and mutate the topic workspace state database through `isomer-cli` state commands or the equivalent Isomer state API.
- Resolve semantic filesystem paths (`topic.repos.extern.*`, `topic.actors.workspace`, `agent.workspace`, `tmp/`, artifact library) via `isomer-cli project paths get` rather than hard-coding directory paths.
- Register durable artifacts with a `kaoju:*` semantic id, a metadata record in the state DB, and a filesystem link.
- Read back artifacts by querying the state DB instead of scanning directories.

### 2. Use case routing and public interface

Choose one public surface for the workflow layer and implement it consistently:

- Option A: a new top-level system skill, e.g. `isomer-kaoju-workflow` or `isomer-kaoju-surveyor`, with one subcommand per use case.
- Option B: new subcommands under the existing `isomer-kaoju-pipeline` skill.
- Option C: operator-level recipes in `isomer-op-entrypoint` that dispatch to the Kaoju stage skills.

Document the chosen surface in `design/public-interfaces.md`. Each command must accept a `--topic <topic>` argument and, where applicable, a `--direction`, `--reading-item`, `--paper`, or `--repo` argument.

### 3. Per-use-case implementation notes

#### uc-01 — Survey Direction From Topic

- Accept a topic or research question.
- Use `isomer-kaoju-frame` or equivalent framing logic to propose 3–5 concrete survey directions.
- Present directions to the actor with A/B/C/D choices; allow multi-select or free-form refinement.
- Persist the selected/refined direction set as `kaoju:next-direction-set` in the state DB.

#### uc-02 — Collect Online Info And Build In-Depth Reading List

- Accept a direction id (from `kaoju:next-direction-set`).
- Use `isomer-kaoju-discover` to collect candidate sources, recording query provenance.
- Compose one direction-owned reading list artifact (`kaoju:reading-list`) with metadata per item: name, URL, source type, one-paragraph summary, priority (primary/secondary), and locator.
- Default target is 3 primary + 3 secondary items; fewer is a warning, not a blocker.
- Answer the actor question: "For `<direction>`, what are you going to read?"

#### uc-03 — Ingest Reading Item In Depth

- Accept a reading item id from `kaoju:reading-list`.
- If the item has an associated paper or repo, acquire it to the topic artifact library using `isomer-kaoju-acquire` or `isomer-kaoju-examine`.
- For papers and source code, prefer local download/checkout (`git clone --depth 1` for repos); if blocked by provider restrictions, read online and record the access blocker.
- Index acquired files in the state DB to avoid repeated download.
- Produce: `kaoju:source-digest`, `kaoju:claim-evidence-ledger` entries, and any contradictions or limitations.

#### uc-04 — Write Paper From Digested Materials

- Require an accepted audit report (`kaoju:audit-report`) and synthesis records (`kaoju:field-summary`, `kaoju:related-work-catalog`, `kaoju:claim-status-table`).
- First produce a MyST paper structure with placeholders (`kaoju:paper-myst-template`).
- Then fill the structure to produce the MyST paper draft (`kaoju:paper-myst-draft`).
- Content first; formatting is deferred to Markdown/LaTeX derivation.

#### uc-05 — Paper Template Manual Editing And Apply

- On "get me the md template", extract `kaoju:paper-myst-template` to a user-given directory or a system-defined topic workspace directory, write a manifest, and record the extraction in the state DB.
- On "apply the template" or "update the paper with new template", read back the manually edited template, update the durable `kaoju:paper-myst-template` artifact, and regenerate the MyST paper draft.

#### uc-06 — Create Paper PDF

- From the accepted MyST draft, generate a TeX template (`kaoju:paper-tex-template`) and keep it as a durable artifact.
- Generate the TeX paper (`kaoju:paper-tex-draft`).
- Compile to PDF and record the output path.
- Conversion from MyST to Markdown must be scriptable; conversion from MyST to LaTeX may be initialized by a script but must be completed by direct file inspection and editing where the script is insufficient.

#### uc-07 — Export Survey Records To LLM Wiki And Deploy Viewer

- Accept a target path from the user.
- Export survey records into an LLM Wiki format: human-viewable Markdown cross-linked pages plus machine-friendly metadata (JSON/YAML).
- Keep the implementation self-contained inside Isomer Labs; do not route to the external `imsight-llm-wiki` skill.
- On "deploy a viewer", copy/deploy the bundled web viewer to the user-given path, write a viewer manifest that points at the wiki, and record it in the state DB.
- On "start the viewer", read the manifest and start the viewer on a port.

#### uc-08 — Ingest Source Code By Link Or Name

- Accept a URL, repo name, or paper reference.
- If only a name/paper is given, search online for an associated repository; report a blocker if not found or inaccessible.
- Clone/checkout the repo with `git clone --depth 1` into the topic workspace artifact library and index it in the state DB.
- Read the local source code, focusing on the aspects the actor specified, and add the result to the surveyed artifacts (`kaoju:source-digest`, `kaoju:associated-source-code`).

#### uc-09 — Prepare Code Run Environment

- Ensure the source code exists in the topic workspace (route to uc-08 if needed).
- Inspect dependency files (`pixi.toml`, `pyproject.toml`, `requirements.txt`, `setup.py`, `environment.yml`, `Cargo.toml`, `package.json`, README install instructions, import statements).
- Update the topic env gate: `topic.intent.env_requirements` and `topic.env.derived_gate`.
- Select Pixi environment strategy in this order:
  1. Reuse an existing satisfying Pixi environment.
  2. Add packages to an existing environment (prefer `default`) without breaking it, using `"*"` or compatible version constraints rather than exact repo versions.
  3. Create a new dedicated Pixi environment.
- Install dependencies, create a smoke-run script that exercises the task-critical code path, run it, and record the result.

#### uc-10 — Run Source Code Trial

- Require a prepared environment from uc-09.
- Accept a dataset path or request generated data.
- Plan the trial, run the code on the data, and record the result as `kaoju:code-trial-result`.
- Capture logs, metrics, and any reproducibility notes.

### 4. Cross-cutting requirements

- Every claim-bearing procedure must invoke `isomer-kaoju-audit` before synthesis or paper writing.
- Online collection must record query provenance and source identity in durable records.
- All durable outputs must be registered in the state DB with metadata and filesystem links.
- Workflows must be resumable: an interrupted use case can be resumed from the last completed durable artifact.

## Verification

- Run `pixi run lint` and `pixi run typecheck` on any new Python code under `src/isomer_labs/`.
- Run `pixi run test` if unit tests are added for state DB helpers, env-gate logic, or use-case routers.
- Manual end-to-end check on `isomer-content/topic-ws/predictive-memory-tiering-survey/` or a fresh topic workspace:
  1. `uc-01`: propose directions from the topic.
  2. `uc-02`: build a reading list for a chosen direction.
  3. `uc-03`: ingest one reading item.
  4. `uc-08`: ingest a source-code repo.
  5. `uc-09`: prepare the code-run environment.
  6. `uc-10`: run the source-code trial.
  7. Audit and synthesize, then `uc-04` write a MyST paper draft.
  8. `uc-05` manually edit and apply the template.
  9. `uc-06` generate the PDF.
  10. `uc-07` export to LLM Wiki and deploy the viewer.
- Verify that every durable artifact can be looked up in the state DB and that its filesystem link resolves.

## Required Evidence

Evidence packs should be written to `tmp/kaoju-survey-process-evidence/` and should not be committed unless explicitly requested.

Each evidence pack should include:

- `input/`: the user prompts, topic id, and any starting references used during the run.
- `output/`: state DB query dumps, durable artifact manifests, sample generated files (paper draft, reading list, wiki export), and screenshots or logs from the viewer and PDF compilation.
- `README.md`: what was implemented, which use cases were exercised, how to inspect the state DB entries, and any blockers encountered.

## Out Of Scope

- Re-implementing the underlying Kaoju stage skills (frame, discover, acquire, examine, audit, synthesize, write).
- Replacing the existing `isomer-kaoju-pipeline` public procedures.
- Defining a new storage backend or artifact format; use existing `kaoju:*` semantic ids.
- Covering DeepSci hypothesis-driven research workflows.
- Low-level web search provider implementation details.
- LaTeX engine internals and citation style packages.
- Houmao agent team launch and runtime topology.

## Open Questions

- Which public surface should own these use cases: a new top-level skill, `isomer-kaoju-pipeline` subcommands, or operator recipes?
- Should the workflow be exposed as CLI commands, agent-skill invocations, or both?
- Should direction proposal be fully automated, clarification-driven, or both?
- How should the agent handle missing or partial state DB schema for new `kaoju:*` artifact types?
