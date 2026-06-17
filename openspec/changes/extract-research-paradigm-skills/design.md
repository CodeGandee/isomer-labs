## Context

DeepScientist provides a mature research-stage pipeline through source-controlled skill bundles under `extern/orphan/DeepScientist/src/skills/`. The repository already contains an analysis layer at `context/explore/deepscientist-skill-analysis/` that summarizes each active skill's state machine, durable outputs, and constraints. The existing `teams/deepsci-org/source/team-design.md` maps those skills to Houmao specialists, but it still names DeepScientist sources and assumes a DeepScientist-like research loop.

The target is a project skillset under `skillset/research-paradigm/` that future agents can load without needing DeepScientist quest state, artifact APIs, memory APIs, or runtime-specific command wrappers. The extracted skills should preserve the reusable research methods: scouting, baseline acceptance, ideation, optimization, experiments, analysis campaigns, writing, review, rebuttal, decision, finalization, figure work, and scientific computation discipline.

## Goals / Non-Goals

**Goals:**

- Create portable Codex-style skills under `skillset/research-paradigm/`.
- Preserve the DeepScientist research-stage logic while removing DeepScientist workspace specifics.
- Use established Isomer Labs domain concepts for research lifecycle, workspace, agent, artifact, evidence, and decision language.
- Define a shared vocabulary for durable Artifacts, Evidence Items, handoffs, Decision Records, Gates, and source provenance.
- Mark unsettled concrete paths, filenames, commands, runtime APIs, storage locations, and generated artifact layouts as `yet-to-be-determined` instead of inventing defaults.
- Keep each skill discoverable through minimal `name` and `description` frontmatter.
- Use progressive disclosure: concise `SKILL.md` files, with templates and longer playbooks under `references/`.
- Define generic research-agent role mappings that can replace the DeepScientist-specific role naming in `teams/deepsci-org`.
- Preserve license and provenance notices for copied or adapted material.

**Non-Goals:**

- Do not implement a new autonomous research runtime, daemon, harness, database, mailbox system, or scheduler.
- Do not port DeepScientist APIs such as `artifact.*`, `memory.*`, `bash_exec(...)`, or DeepXiv.
- Do not change the Python package, Pixi configuration, or test commands.
- Do not require the Nature/publication helpers in the first core agent path unless their source material is copied as optional companions.
- Do not create agent instances or credentials as part of the skill extraction.

## Decisions

### Use Codex skill folders as the target format

Each extracted skill will be a folder named `isomer-labs-research-<purpose>` containing a required `SKILL.md`. The `SKILL.md` frontmatter will contain only `name` and `description`, matching the skill creation guidance. Optional `references/`, `assets/`, `scripts/`, and `agents/openai.yaml` files may be added only when they directly support that skill.

Alternative considered: copy DeepScientist skill folders verbatim and rename them. This would be faster, but it would preserve runtime coupling and very large instruction bodies.

### Extract research operations, not runtime APIs

DeepScientist terms will be mapped to generic host concepts:

| DeepScientist source term | Isomer target concept |
| --- | --- |
| `quest` | Research Thread, Research Task, Run, or Isomer Workspace, depending on scope |
| quest root | Isomer Workspace or Workspace Runtime, only when the storage scope is known |
| `artifact.*` | Artifact, Evidence Item, Decision Record, Gate, Provenance Record, or host API, depending on operation |
| `memory.*` | prior durable context, Artifact, Finding, or Evidence Item |
| `bash_exec(...)` | host-provided execution tool, marked `yet-to-be-determined` until the command surface is selected |
| DeepXiv / `artifact.arxiv(...)` | paper search and paper-reading capability, marked `yet-to-be-determined` until provider selection |
| quest branch | Research Branch |
| quest worktree | isolated execution surface or Agent Workspace, marked `yet-to-be-determined` when the concrete filesystem layout is unsettled |
| `workspace_mode`, `continuation_policy`, and `auto_continue` | DeepScientist runtime scheduling and collaboration details. Do not port them as Isomer concepts; express retained behavior as Agent Team Instance advancement under Coordination Policy, paused waiting for Operator Agent instruction, Workflow Stage recommendations, Gates, and Decision Records. |

Alternative considered: introduce an Isomer-specific harness contract now. That would make the skills more executable for one runtime, but it would narrow the research paradigm before the agent architecture is settled.

### Do not port DeepScientist continuation policy

DeepScientist uses `continuation_policy` to decide whether its daemon schedules another turn, parks until a user message or resume, or monitors external progress. Isomer Labs should not expose that as a research-paradigm skill concept. The Operator Agent remains the human-facing control boundary, while delegated Agent Team Instances either continue their approved loop or pause and wait for Operator Agent instruction.

Extracted skills should therefore recommend the next Workflow Stage, Gate, or Decision Record. They should not instruct an implementation to set `continuation_policy`, schedule `auto_continue` turns, or switch the Operator Agent between autonomous and manual modes. Concrete Agent Team Instance lifecycle states, scheduler behavior, and pause-state schemas remain `yet-to-be-determined:schema` or `yet-to-be-determined:policy` until accepted by Isomer platform design.

Alternative considered: map DeepScientist `continuation_policy` to an Isomer auto-continuation policy. This would preserve source-runtime behavior too directly and would blur the boundary between research-method skills and platform scheduling.

### Prefer explicit TBD markers over guessed surfaces

When a DeepScientist source skill names a concrete path, file, command, API, registry, runner home, workspace directory, or generated artifact layout that has no settled Isomer equivalent, the extracted skill will write `yet-to-be-determined` and name what decision is missing. This makes unresolved platform design visible for later iterations.

Alternative considered: pick provisional paths such as `artifacts/`, `experiments/`, `paper/`, `memory/`, or `runs/` to keep the skills executable. That would hide design gaps and could conflict with Isomer's Project Manifest, Isomer Workspace, Workspace Runtime, and Artifact model.

### Create one shared research skill

`isomer-labs-research-shared` will define common truth-source order, artifact vocabulary, handoff expectations, claim/evidence boundaries, and validation discipline. Stage skills will reference the shared skill instead of repeating common rules.

Alternative considered: duplicate the shared contract into every skill. That would make each skill standalone, but it would make later corrections expensive and inconsistent.

### Keep core research skills separate from publication extensions

The core set will cover intake, scout, baseline, idea, optimize, experiment, analysis, decision, finalize, write, review, rebuttal, paper-outline, paper-plot, figure-polish, and science. Nature-specific helpers can be ported as optional publication extensions after the core set, because they carry additional templates, upstream license notices, and journal-specific assumptions.

Alternative considered: port all active DeepScientist skills in one pass. That maximizes completeness, but it increases review cost and can blur generic research behavior with journal-specific production workflows.

### Map agents to skills outside the skills

Skills will not encode a single team topology. Team documents will define generic agents such as `research-lead`, `research-scout`, `research-designer`, `research-executor`, `research-writer`, and `research-reviewer`, then list which skills each role should install.

Alternative considered: one agent per extracted skill. That mirrors the full DeepScientist pipeline, but it creates more operational overhead than the current generic-team goal requires.

## Risks / Trade-offs

- DeepScientist-specific language may leak into generic skills -> Review generated skill text with targeted searches for `quest`, `artifact.`, `memory.`, `bash_exec`, `DeepScientist`, `DeepXiv`, and workspace-specific paths.
- DeepScientist scheduling language may leak into generic skills -> Review generated skill text for `workspace_mode`, `continuation_policy`, `auto_continue`, and `wait_for_user_or_resume`; remaining matches must be provenance, explicit mapping, or rejection notes.
- Isomer paths and files may be guessed too early -> Require `yet-to-be-determined` markers wherever the Isomer path, filename, command, API, or storage surface is not settled by existing domain concepts or ADRs.
- Extracted skills may become too shallow after removing runtime APIs -> Preserve the analyzed state machines, durable outputs, gate criteria, and pitfalls from `context/explore/deepscientist-skill-analysis/`.
- Large skills may load too much context -> Move long playbooks, templates, and examples into one-level `references/` files.
- License obligations may be missed for copied material -> Copy or summarize source material deliberately, and preserve Apache 2.0 plus upstream MIT notices where applicable.
- Agent mappings may overfit the current Houmao design -> Keep mappings as team documentation, not as hard requirements inside the skills.
- Validation may only check files exist, not skill quality -> Include both structural checks and content checks for neutral terminology, required requirements, and forward-test prompts where feasible.

## Migration Plan

1. Create `skillset/research-paradigm/` and the core skill folders.
2. Add `isomer-labs-research-shared` first so subsequent skills can reference a common contract.
3. Extract core stage skills from the analysis summaries and source skill bodies into concise `SKILL.md` files.
4. Move longer templates and playbooks into `references/` files when needed.
5. Add or update team documentation to map generic research agents to installed skills.
6. Run structural and content validation.
7. Leave DeepScientist source files unchanged.

Rollback is simple because this change is additive: remove the new `skillset/research-paradigm/` subtree and revert any team documentation edits.

## Implementation Defaults

- Leave Nature-specific helpers for a follow-up publication-extension change unless implementation discovers they are needed to satisfy an existing core skill requirement.
- Defer `agents/openai.yaml` generation until the extracted `SKILL.md` files stabilize.
- Update `teams/deepsci-org` around the six-agent generic map: `research-lead`, `research-scout`, `research-designer`, `research-executor`, `research-writer`, and `research-reviewer`.
- Use Isomer Labs concepts from `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md` as the canonical language baseline.
- Use `yet-to-be-determined` for unsettled concrete paths, filenames, command surfaces, runtime APIs, storage roots, and artifact layouts.
