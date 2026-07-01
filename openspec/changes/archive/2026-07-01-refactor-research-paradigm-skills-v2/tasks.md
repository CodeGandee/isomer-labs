## 1. Preserve Current Skills as V1

- [x] 1.1 Create `skillset/research-paradigm/v1/` and move every current flat `skillset/research-paradigm/isomer-rsch-*` folder into it.
- [x] 1.2 Rename every moved folder from `isomer-rsch-<purpose>` to `isomer-rsch-<purpose>-v1`.
- [x] 1.3 Update each v1 `SKILL.md` frontmatter `name:` to match the `-v1` folder name.
- [x] 1.4 Update each v1 `agents/openai.yaml` display name and default prompt to use the matching `-v1` skill name.
- [x] 1.5 Update v1 internal cross-skill references where they name moved skills so preserved v1 material points to `-v1` names.

## 2. Create V2 Shared Placeholder Contract

- [x] 2.1 Create `skillset/research-paradigm/v2/isomer-rsch-shared-v2/` with valid `SKILL.md` frontmatter and manifest.
- [x] 2.2 Write `isomer-rsch-shared-v2/SKILL.md` around the core loop `Frame -> Comparator -> Hypothesis -> Experiment -> Analysis -> Decision -> Finalize`.
- [x] 2.3 Add `isomer-rsch-shared-v2/references/semantic-placeholders.md` with the `[[rsch-object:<id>]]` syntax and explicit "not storage-bound yet" rule.
- [x] 2.4 Define initial placeholder semantics for research frame, comparator contract, selected hypothesis, optimization frontier, experiment contract, experiment result, analysis finding, science validity note, route decision, and final summary.

## 3. Create V2 Core Method Skills

- [x] 3.1 Create v2 folders, `SKILL.md`, and manifests for `isomer-rsch-scout-v2`, `isomer-rsch-baseline-v2`, and `isomer-rsch-idea-v2`.
- [x] 3.2 Create v2 folders, `SKILL.md`, and manifests for `isomer-rsch-optimize-v2`, `isomer-rsch-experiment-v2`, and `isomer-rsch-analysis-v2`.
- [x] 3.3 Create v2 folders, `SKILL.md`, and manifests for `isomer-rsch-decision-v2`, `isomer-rsch-finalize-v2`, and `isomer-rsch-science-v2`.
- [x] 3.4 Ensure every v2 skill uses the concise sections: purpose, when to use, workflow, semantic inputs, semantic outputs, guardrails, and source lineage when needed.
- [x] 3.5 Ensure every v2 skill declares semantic inputs and outputs only through registered `[[rsch-object:<id>]]` placeholders.
- [x] 3.6 Remove active v2 instructions that require Artifacts, Evidence Items, Runs, Gates, Decision Records, Provenance Records, concrete paths, storage labels, runtime rows, scheduler fields, or execution adapters.

## 4. Update Documentation and Provenance

- [x] 4.1 Rewrite `skillset/research-paradigm/README.md` to explain the v1 preserved generation, v2 active core generation, v2 placeholder contract, and paper-skill deferral.
- [x] 4.2 Update `skillset/research-paradigm/PROVENANCE.md` to state that v1 preserves the existing DeepScientist-derived skills and v2 distills the core process from `context/explore/deepscientist-skill-analysis/`.
- [x] 4.3 Update `skillset/README.md` or role-map documentation that mentions research-paradigm skill names so active core references use `-v2` where appropriate and preserved paper skills use `-v1`.
- [x] 4.4 Update any topic-team fixtures or template material that must keep invoking research skills so the intended generation is explicit.

## 5. Update Validation

- [x] 5.1 Update `scripts/validate_research_paradigm_skillset.py` to accept the `v1/` and `v2/` generation layout and reject active flat root `isomer-rsch-*` skill folders.
- [x] 5.2 Add validation for generation-suffixed folder names, `SKILL.md` frontmatter names, manifest display names, and manifest default prompts.
- [x] 5.3 Add validation that every v2 `[[rsch-object:<id>]]` placeholder is registered in `v2/isomer-rsch-shared-v2/references/semantic-placeholders.md`.
- [x] 5.4 Add validation that active v2 guidance does not require storage-binding terms outside allowed provenance, migration, or rejected-storage-binding zones.
- [x] 5.5 Update `skillset/research-paradigm/validation.toml` allow zones for v1 preservation and v2 placeholder/storage-binding checks.
- [x] 5.6 Update `tests/unit/test_validate_research_paradigm_skillset.py` for the generationed layout, registered placeholder checks, unregistered placeholder failures, and v2 storage-binding failures.

## 6. Verify

- [x] 6.1 Run `pixi run validate-research-skills`.
- [x] 6.2 Run `pixi run python -m unittest tests.unit.test_validate_research_paradigm_skillset`.
- [x] 6.3 Run `openspec validate refactor-research-paradigm-skills-v2 --strict`.
- [x] 6.4 Inspect `skillset/research-paradigm/v2/` with `rg` to confirm active v2 guidance uses semantic placeholders and does not contain storage-bound instructions.
