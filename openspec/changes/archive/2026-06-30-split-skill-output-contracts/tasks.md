## 1. Shared Output Contract Convention

- [x] 1.1 Update non-research-paradigm skill output contract wording to define Essential Output as the default chat report and Complete Output as request-only detail.
- [x] 1.2 Add request-trigger wording for complete, verbose, audit, debug, full handoff, JSON, or full output.
- [x] 1.3 Ensure Essential Output sections focus on status, what happened, important paths or refs, readiness, blockers, and next action.
- [x] 1.4 Ensure Complete Output sections preserve handoff and audit detail grouped by purpose.

## 2. Major Operator Skills

- [x] 2.1 Revise `skillset/operator/isomer-admin-topic-team-specialize/SKILL.md` output contract into Essential Output and Complete Output.
- [x] 2.2 Revise `skillset/operator/isomer-admin-topic-workspace-mgr/SKILL.md` output contract into Essential Output and Complete Output.
- [x] 2.3 Revise `skillset/operator/isomer-admin-project-mgr/SKILL.md` output contract into Essential Output and Complete Output.
- [x] 2.4 Check remaining `skillset/operator/*` skills outside `research-paradigm/` and apply the split where an output contract exists.

## 3. Service Skills

- [x] 3.1 Revise `skillset/service/isomer-srv-topic-env-setup/SKILL.md` output contract into Essential Output and Complete Output.
- [x] 3.2 Revise `skillset/service/isomer-srv-agent-env-setup/SKILL.md` output contract into Essential Output and Complete Output.
- [x] 3.3 Revise package repository resolution output contracts so their default output stays concise while complete output carries reachability and source evidence.
- [x] 3.4 Check remaining `skillset/service/*` skills and apply the split where an output contract exists.

## 4. Misc and Creator Skills

- [x] 4.1 Revise `skillset/misc/isomer-misc-bounded-run-tips/SKILL.md` reporting contract into Essential Output and Complete Output.
- [x] 4.2 Revise `skillset/misc/isomer-misc-nvidia-tools` reference output contracts where needed.
- [x] 4.3 Check `skillset/misc/*` and `skillset/skill-creator` output/reporting sections outside `research-paradigm/` and apply the split where relevant.

## 5. Reference Pages and Wording

- [x] 5.1 Update reference pages that say `Report using Output Contract` so they respect Essential Output by default and Complete Output on request.
- [x] 5.2 Avoid duplicating large complete field lists in reference pages unless the page has a genuinely local output contract.
- [x] 5.3 Keep Markdown structured and concise, using grouped lists instead of long prose.

## 6. Specs and Validation

- [x] 6.1 Update mainline OpenSpec specs for the new `skill-output-contracts` capability and affected existing skill capabilities.
- [x] 6.2 Update `scripts/validate_skillsets.py` to require the essential/complete output convention and complete-on-request wording for relevant skills.
- [x] 6.3 Update `tests/unit/test_validate_skillsets.py` fixtures and add regression checks for missing Essential Output, missing Complete Output, and default-complete leakage.
- [x] 6.4 Run quick skill validation for affected skills.
- [x] 6.5 Run `pixi run python scripts/validate_skillsets.py --scope service`, `pixi run python scripts/validate_skillsets.py --scope operator`, and relevant unit tests.
- [x] 6.6 Run `openspec validate split-skill-output-contracts --strict` and fix any artifact issues.
