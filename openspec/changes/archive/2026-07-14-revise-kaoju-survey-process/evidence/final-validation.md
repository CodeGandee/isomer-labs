# Final Validation Evidence

Captured on 2026-07-14 after implementing `revise-kaoju-survey-process`.

## Outcome

The fourteen-skill Kaoju package, ten survey intents, typed Project services, MyST-first paper graph, self-contained wiki/viewer, Service Request boundary, explicit Pixi execution policy, and state-DB-backed Artifact model pass their focused, integration, repository-wide, and OpenSpec checks. No unrelated pre-existing failures remain in the executed validation set.

## Commands and Results

| Check | Result |
| --- | --- |
| `pixi run lint` | Passed. Ruff reported no violations. |
| `pixi run typecheck` | Passed. MyPy reported no issues in 145 source files. |
| `pixi run test` | Passed: 569 unit tests. |
| `pixi run python -m pytest -q tests/integration/test_kaoju_artifact_services.py tests/integration/test_kaoju_code_trial.py tests/integration/test_kaoju_paper_wiki.py tests/integration/test_kaoju_record_lifecycle.py tests/integration/test_kaoju_survey_intents.py` | Passed: 13 integration tests. |
| `pixi run python scripts/validate_research_paradigm_skillset.py` | Passed with no diagnostics. |
| Focused Kaoju contracts, bindings, skills, survey semantics, packaging, installer, and validator unit suite | Passed: 100 tests. |
| Skill Creator `quick_validate.py` for `isomer-kaoju-trial` and `isomer-kaoju-export` | Both skills valid. |
| `git diff --check` | Passed. |
| `openspec validate revise-kaoju-survey-process --strict` | Passed: change is valid. |

## Requirement and Scenario Evidence

Every scenario under each requirement in the listed spec area is exercised by the cited behavior tests, checked package contracts, or architecture validator rules. The tests use installed package resources and temporary Project and Topic Workspace fixtures rather than relying on checkout-only paths.

| Spec Area | Scenario Evidence | Principal Implementation |
| --- | --- | --- |
| `kaoju-artifact-bindings` | `tests/unit/test_kaoju_artifact_bindings.py`, `tests/unit/test_kaoju_contracts.py`, `tests/unit/test_kaoju_survey_process.py`, `tests/integration/test_kaoju_artifact_services.py`, and `tests/integration/test_kaoju_record_lifecycle.py` cover registry completeness, profiles, content modes, scoped current state, legacy ambiguity, lineage, immutable and append-only behavior, managed paths, recovery, stale content, and reset preservation. | `contracts/bindings.v2.json`, `src/isomer_labs/kaoju/contracts.py`, `artifacts.py`, and the Workspace Runtime record/index changes. |
| `kaoju-cli-services` | `tests/integration/test_kaoju_artifact_services.py`, `test_kaoju_code_trial.py`, and `test_kaoju_paper_wiki.py`, plus repository-wide CLI, research-record, and legacy-template unit tests, cover typed JSON success and failure, repository atomicity, Runs, synchronous Service Requests, operation extension points, paper/wiki commands, and compatibility surfaces. | `src/isomer_labs/cli/commands/kaoju_project.py`, `kaoju_ext.py`, and `src/isomer_labs/kaoju/{artifacts,runs,repositories,service_requests,execution,paper,wiki}.py`. |
| `kaoju-code-execution` | `tests/unit/test_kaoju_survey_process.py` and `tests/integration/test_kaoju_code_trial.py` cover reference resolution posture, shallow acquisition, inaccessible and duplicate repositories, exact commit/file/line evidence, environment planning, reuse/add/create selection, exact lock identity, failed and repaired smoke attempts, ambient-environment rejection, approval Gates, durable wrappers, path and generated data, immutable trial attempts, retry classification, and capability-probe calibration. | Trial and pipeline guidance, the adapted topic environment service, `survey.py`, `repositories.py`, `service_requests.py`, and `execution.py`. |
| `kaoju-paper-production` | `tests/integration/test_kaoju_paper_wiki.py` covers accepted and blocked audits, MyST validation, typed displays, template export/apply, stale bases, invalid placeholders, orphan confirmation, derived Markdown, stable and revised TeX initialization, registered builds, compiler fallback, PDF inspection, publication Gate, and Artifact lineage. Architecture validation checks MyST-first guidance and legacy non-promotion. | `src/isomer_labs/kaoju/paper.py`, MyST profiles and bindings, `isomer-kaoju-write`, paper intent pages, and `ext kaoju paper`. |
| `kaoju-research-extension` | `tests/unit/test_kaoju_skill_assets.py`, `test_kaoju_contracts.py`, `test_validate_research_paradigm_skillset.py`, and package asset tests cover the exact fourteen skills, ten intent routes, compatibility procedures, grouped manager actions, trial/reproduction separation, owner routing, Run checkpoints, and DB-only prior-work discovery. | `contracts/survey-process.v2.json`, the thin pipeline router, trial/export skills, shared guidance, and manifest metadata. |
| `kaoju-survey-intents` | `tests/unit/test_kaoju_survey_process.py` and `tests/integration/test_kaoju_survey_intents.py` cover multiple and custom directions, feasibility annotations, human confirmation, independent reading-list scopes, priority/secondary targets, shortages, provenance, version deduplication, inspection/refinement/approval, local and online acquisition posture, blockers, exact paper and display locators, associated code, audit prerequisites, blocked checkpoints, and resume from the first incomplete stage. | Direction, reading-list, acquisition, examination, audit, and pipeline guidance plus semantic validators in `survey.py`. |
| `kaoju-wiki-export` | `tests/integration/test_kaoju_paper_wiki.py` covers state-DB selection, explicit subsets and defaults, Markdown plus JSON output, provenance relationships, idempotent updates, human-file preservation, stale targets, package-owned viewer deployment and refresh, unrecognized targets, local launch, port conflicts, network Gates, Run/log output, and absence of external wiki skill routing. | `src/isomer_labs/kaoju/wiki.py`, package viewer assets and schemas, `isomer-kaoju-export`, and `ext kaoju wiki`. |
| `packaged-system-skills` | `tests/unit/test_system_skill_assets.py`, `test_system_skill_installer.py`, `test_isomer_cli.py`, and `test_kaoju_skill_assets.py` cover package-contained paths, deterministic materialization, selectors, callbacks, discovery, installation, upgrade, and the declared intent surface. | Packaged `manifest.toml`, system-skill discovery metadata, entrypoint index, and the fourteen Kaoju skill resources. |
| `research-paradigm-skills` | `scripts/validate_research_paradigm_skillset.py` and `tests/unit/test_validate_research_paradigm_skillset.py` validate binding authority, generated binding summaries, DB-only discovery, content authority, Gates, Runs, Service Requests, execution requests, MyST-first writing, reset semantics, trial ownership, Houmao adapter isolation, and the prohibition on external wiki skill invocation. | Shared/workspace/producer skill refactors, generated registry summaries, the environment service fulfillment page, and checked architecture rules. |

## Compatibility Evidence

The repository-wide unit suite retains existing DeepSci behavior, `ext research records`, historical `ext research templates` inspection and repair, existing record lifecycle behavior, package installation, GUI-neutral record rendering, and callback discovery. Legacy LaTeX records remain readable and explicitly non-canonical; no automatic TeX-to-MyST promotion was added.
