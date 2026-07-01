## 1. Inventory

- [x] 1.1 Inventory writing-related placeholders in `isomer-rsch-paper-outline-v2`, `isomer-rsch-write-v2`, `isomer-rsch-review-v2`, `isomer-rsch-rebuttal-v2`, `isomer-rsch-finalize-v2`, `isomer-rsch-paper-plot-v2`, `isomer-rsch-figure-polish-v2`, and Nature companion v2 skills.
- [x] 1.2 Compare each writing-related binding row with the paper-writing artifact mapping in `context/plans/refactor-isomer-rsch-skills/required-storage-support.md`.
- [x] 1.3 Identify any `migrate/placeholders.md` kind values that conflict with the required durable storage role.

## 2. Core Paper Skill Bindings

- [x] 2.1 Update `isomer-rsch-paper-outline-v2/placeholder-bindings.md` so paper outline, selected outline, paper view, evidence view, section writing plan, and outline validation placeholders use paper-line profiles and explicit semantic labels.
- [x] 2.2 Update `isomer-rsch-write-v2/placeholder-bindings.md` so paper contract, paper outline, writing plan, source-material ledger, citation ledger, display plan, draft sections, manuscript validation, bundle checkpoint, and route decision placeholders use paper-line profiles and explicit semantic labels.
- [x] 2.3 Update `isomer-rsch-review-v2/placeholder-bindings.md` so review report, revision log, evidence TODO, paper experiment matrix update, and route decision placeholders link to review profiles, paper matrix views, task records, and decisions as appropriate.
- [x] 2.4 Update `isomer-rsch-rebuttal-v2/placeholder-bindings.md` so reviewer matrix, action plan, reviewer-linked TODO, evidence update, text delta, response letter, and revision handoff placeholders use rebuttal profiles, task records, evidence records, and package-like artifact profiles as appropriate.
- [x] 2.5 Update `isomer-rsch-finalize-v2/placeholder-bindings.md` so finalize context, claim ledger, limitations, final summary, resume packet, closure decision, blocker, and continuity placeholders read paper bundle, evidence ledger, claim map, validation, and review/rebuttal state through precise profiles.

## 3. Companion Skill Bindings

- [x] 3.1 Update `isomer-rsch-paper-plot-v2/placeholder-bindings.md` so first-pass figure, plot inspection, source data, and figure-polish handoff placeholders link to figure and paper experiment matrix profiles where relevant.
- [x] 3.2 Update `isomer-rsch-figure-polish-v2/placeholder-bindings.md` so final figure export, render review, provenance, style contract, and downstream paper surface placeholders use figure export, figure catalog, evidence, and provenance profiles.
- [x] 3.3 Update Nature companion v2 binding pages only for placeholders that produce paper-writing artifacts, such as polished manuscript text, data availability statements, presentation packages, Nature figures, bibliography-adjacent outputs, or submission-facing evidence.

## 4. Registry and Guidance Adjustments

- [x] 4.1 Adjust `migrate/placeholders.md` files only when a placeholder is missing or its kind conflicts with the durable binding role.
- [x] 4.2 Update shared v2 references or local binding rules if agents need one concise rule that paper-line binding profiles come from the required storage-support mapping.
- [x] 4.3 Avoid adding paper-specific top-level semantic labels and ensure all updated rows use existing generic semantic labels.

## 5. Validation

- [x] 5.1 Run `pixi run validate-research-skills` and fix placeholder binding coverage, extra placeholder rows, stale references, or self-containment issues.
- [x] 5.2 Run `pixi run docs-validate` if implementation changes shared planning or documentation files.
- [x] 5.3 Review `git diff --check` and inspect the updated binding rows for correct `--semantic-label`, `--profile`, `--placeholder`, `--skill`, producer, consumer, and metadata usage.
