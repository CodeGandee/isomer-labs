## 1. Skill Skeleton

- [x] 1.1 Create `skillset/research-paradigm/deepsci/isomer-deepsci-pipeline/` folder
- [x] 1.2 Add standard skill layout: `SKILL.md`, `agents/openai.yaml`, `commands/`, `references/`, `placeholder-bindings.md`
- [x] 1.3 Add provenance note in `references/` explaining relationship to DeepScientist loop protocol

## 2. Pipeline Pass Subcommand Pages

- [x] 2.1 Create `commands/empirical-pass.md` (scout → baseline → idea → experiment → analysis)
- [x] 2.2 Create `commands/hypothesis-pass.md` (idea → experiment → analysis)
- [x] 2.3 Create `commands/paper-pass.md` (analysis → paper-outline → write → review)
- [x] 2.4 Create `commands/revision-pass.md` (review → analysis → write)
- [x] 2.5 Create `commands/rebuttal-pass.md` (rebuttal → analysis → experiment → write)
- [x] 2.6 Create `commands/polish-pass.md` (write → figure-polish → nature-polishing → review)
- [x] 2.7 Create `commands/submission-pass.md` (review → nature-data → finalize)
- [x] 2.8 Create `commands/list-passes.md`
- [x] 2.9 Validate all recipes have no loops, known skills, and registered artifacts

## 3. Skill Execution Contract

- [x] 3.1 Author `SKILL.md` with frontmatter, overview, workflow, reference routing, user skill callbacks, worker output policy, and quality gates
- [x] 3.2 Define `pipeline-terminal-report` shape in `references/terminal-report-template.md`
- [x] 3.3 Add stage transition rules in `references/transition-rules.md`
- [x] 3.4 Define pipeline control-surface objects in `references/placeholders.md` and populate `placeholder-bindings.md`

## 4. Skill Router

- [x] 4.1 Rewrite `SKILL.md` as a router with a Subcommands table
- [x] 4.2 Ensure each pass page loads its embedded recipe, checks entry context, runs stages, applies transition rules, and produces the terminal report

## 5. Skill Manifest

- [x] 5.1 Create `agents/openai.yaml` with `name`, `description`, and `default_prompt`
- [x] 5.2 Ensure manifest display name matches folder name
- [x] 5.3 Register `research-paradigm/deepsci/isomer-deepsci-pipeline` in `skillset/manifest.toml` under `[groups.deepsci]`

## 6. Research-Paradigm Spec Update

- [x] 6.1 Update `openspec/specs/research-paradigm-skills/spec.md` to include `isomer-deepsci-pipeline` in the production DeepSci skill folder list
- [x] 6.2 Remove or archive the delta spec `openspec/changes/add-isomer-deepsci-pipeline/specs/research-paradigm-skills/spec.md` after sync

## 7. Validation

- [x] 7.1 Run `pixi run lint` and fix any style issues
- [x] 7.2 Run `pixi run typecheck` if Python helpers are added
- [x] 7.3 Run `pixi run test` to ensure no regressions
- [x] 7.4 Run `openspec validate change "add-isomer-deepsci-pipeline"` before archive
