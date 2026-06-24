# Loop Overview: DeepResearch (general-purpose autonomous research platform)

## Source

- Reference system: a local-first
  autonomous research studio: one quest = one git repo, persistent findings memory, hypothesis →
  experiment → analysis → write loop, with human takeover preserved throughout.
- This loop re-expresses a prior research loop as a Houmao `loop-pro` **tree-loop**, with
  stage logic in generated skills and durable state in loop SQLite + an operator-owned git workspace.
- Closest in-repo precedent: `KernelAgent/` (a Houmao tree-loop with an Orchestrator that owns round
  iteration / termination, LLM reasoning agents, deterministic harness tools, a reflexion store, and
  isolated per-worker worktrees). DeepResearch is the **domain-agnostic generalization** of that shape.

## Objective

- Provide a **general-purpose** autonomous research loop that takes a research objective (a paper, a
  repository, a dataset, or a natural-language goal) and drives it through repeated rounds of
  scoping → hypothesis → experiment → analysis → synthesis until an acceptance condition or a
  stop-loss is reached.
- Be **domain-neutral by default**: no built-in assumptions about ML, GPUs, biology, etc. Domain
  knowledge (extra stages, validators, references, templates, metrics) is added later as pluggable
  **knowledge packs** and **domain harness commands**, not hard-coded here.
- **Accumulate, never lose**: failed routes are preserved as branches/worktrees and as durable
  findings memory, so later rounds build on prior evidence instead of repeating it.
- **Survive interruption**: the loop continues across CLI/provider hiccups and gateway restarts via
  the durable **self-mail wakeup** mechanism backed by a self-wakeup ledger in SQLite.
- **Keep humans in the loop**: an operator can inspect, redirect, pause/resume, take over, and hand
  control back at any round; high-risk routes (e.g. low-quality stop) require explicit confirmation.
  Use of physical resources is gated too: experiments may run only on **operator-confirmed GPUs**
  (`gpu confirm`; enforced apply-time by the `experiment_requires_gpu_confirmation` invariant).

## Participants

Role → implementation is resolved per-deployment, but the default split is LLM-agents for reasoning
and deterministic harness tools for anything that must not be hallucinated.

LLM agents:

- **Orchestrator** *(LLM, tree-loop root)*: owns the research state machine — selects the next stage,
  tracks round/budget, applies acceptance and stop-loss rules, records every transition in the
  `decision` log, and arms the next durable self-wakeup. Replaces `runtime_state.json`
  + `decision` / `intake-audit` stage skills. Owns iteration and termination.
- **Scout / Ideator** *(LLM)*: scope intake, baseline framing, hypothesis generation, route selection.
  Replaces the prior `scout` + `idea`.
- **Experimenter** *(LLM, may run as K parallel instances)*: design, implement, and execute a bounded
  experiment inside an **isolated worktree** so parallel routes never clobber each other. Replaces
  the prior `experiment` stage; the worktree model preserves "branches express research
  structure / keep failed routes" principle.
- **Analyst** *(LLM)*: analysis campaigns — slice/ablate results, decompose errors, judge whether a
  result confirms / blocks / is inconclusive against a parent claim. Replaces `analysis-campaign`.
- **Writer** *(LLM)*: synthesize durable evidence into a **publication-grade manuscript** — figures
  rendered from recorded measurements, a bibliography + related work, an ablation that isolates the
  operative mechanism, a compiled LaTeX/PDF paper, a **Chinese edition** (`paper-zh.pdf`), and a
  submission bundle (evidence ledger + claim↔evidence map + checklist). Replaces `write`.
- **Reviewer** *(LLM)*: skeptical audit of a draft before finalize; rebuttal handling. Replaces
  `review` / `rebuttal`.

Harness tools (deterministic; no LLM; the trust boundary):

- **State store**: read/write the SQLite control plane (the only authority for loop bookkeeping).
- **Experiment runner**: execute an experiment's run contract and capture results/metrics honestly.
  *Domain-pluggable* — the default is a generic command-runner; domains override it.
- **Validator + research-quality binding gates**: metric-completeness/comparability checks plus the
  typed binding gates — idea selection, baseline contract, campaign coverage, analysis bridge, paper
  spine, manuscript coverage, review verdict — each shaped as *typed record → validator-computed flag →
  hard handoff/finalize guard*, surfaced by `gate status` and routed deterministically; `methodology
  check` resolves each `methodology_used[].applied_as` to the stage's validated record (methodology is
  binding, not advisory). *Partly domain-pluggable.* Replaces the prior `artifact.validate_*`. See
  `execplan/docs/binding-gates.md` for the per-gate record/validator/guard map.
- **Findings store**: persist/retrieve durable findings memory + reflexion notes, **cross-round but
  per-quest only** (quest-isolated — a quest never reads another quest's findings). Replaces the prior
  `memory/{ideas,decisions,knowledge}` + reflexion store.
- **Git checkpoint**: commit durable artifacts into the quest worktree; manage branches/worktrees.
  Replaces the prior `git.auto_checkpoint`.
- **Artifact compiler**: render reports/figures (e.g. LaTeX/markdown/plots). *Domain-pluggable.*
- **Idea-level BO (`bo` — DeepScientist-inspired LLM-reviewer surrogate + UCB-like acquisition, not full
  statistical Bayesian optimization)**: chooses which candidate research move to try next. `bo candidates`
  gathers quest-local candidates (open `research_opportunity` rows, the latest `idea_select`, quest-local
  `frontier_entry`); the independent **BO-reviewer** role (the LLM Reviewer — launched as its own tree-loop
  participant, dispatched for the `bo-review` stage; configurable; default backend `codex`, effort `max`,
  in `agents/bo-reviewer.toml`) scores each into a `bo_review` valuation vector
  (utility/quality/novelty/exploration_value/uncertainty/feasibility/cost/risk, 0–100); `bo select` runs the
  deterministic UCB-like acquisition (`exploitation + beta*exploration − penalty`) and records a
  `bo_decision`. `bo suggest` is the high-level entry point. Everything is quest-local and ADVISORY (never a
  gate; reviews are a surrogate valuation, not proof). When no idea-level candidate exists but a
  `search_space` does, `bo suggest` falls back to a clearly-labelled midpoint/default heuristic (not real
  BO). The Orchestrator may record a selected candidate as a new idea/experiment
  (`experiment_param.proposed_by = 'bo'`), or refine ideas heuristically from findings memory.
- **Literature / web search**: a generic harness command for arxiv + web retrieval; fetched sources
  land in the `reference` table (cached under `runs/<quest>/refs/`) and become `claim_evidence` of
  `source_kind = 'reference'`. References are **quest-owned** — each quest fetches and caches its own
  sources; no cross-quest reference reuse. Replaces the prior `artifact.arxiv` / deepxiv.

## Operating Model

- **Round structure (per round, Orchestrator-driven):** the Orchestrator reads durable state, selects
  the next stage from the stage catalog, dispatches the owning agent via a gateway-queued prompt,
  receives the result by mail, records it through the State/Findings harness, then **decides the next
  route** and arms the next self-wakeup. One bounded turn per wake; no in-chat waiting/polling.
- **Default stage sequence** (extensible via `stage_catalog`):
  `[intake-audit] → scope → baseline → idea → (optimize) → experiment → analysis → decision → write →
  review → finalize`, with `decision` reachable from any stage to re-route (continue / branch / reset /
  stop / finalize). `intake-audit` is an optional entry path for quests starting from existing assets;
  `optimize` is the orchestrator-internal algorithm-first frontier loop; `finalize` resolves to
  complete / stop / park / publish-and-continue.

  > **Pre-launch research-contract expansion (active).** *Before* `quest.create`, the operator's minimal
  > Objective/Acceptance is expanded into a deeper, domain-neutral scientific done-bar (falsifiable claim,
  > mechanism, baseline/ablation, alternative ruled out, scope, scholarly positioning, traceability), which
  > the operator **approves / edits / trims** (skill `deepresearch-research-contract`; rubric in
  > `execplan/docs/research-contract.md`). The approved contract is recorded as a `research-contract`
  > artifact and the move to `running` is **hard-gated** on it.
  >
  > **Claude effort selection (active, Claude-conditional).** When any participant uses `tool='claude'`, the
  > operator must also choose a Claude effort/reasoning level before launch (Standard/High/Max-if-supported/
  > role-specific/custom). It is applied as a launch-time override (`agents launch --reasoning-level`), NOT
  > persisted onto the shared profiles (quest-independence: the template stays pristine); it is recorded as a
  > `kind='effort-selection'` artifact, and **hard-gated** at `not_started → running`. See
  > `execplan/docs/claude-effort.md`. The full move-to-running gate set is now: **clarification +
  > research-contract + GPU + effort-selection** (`records.py` `_clarification_gate` / `_contract_gate` /
  > `_effort_gate` / `_gpu_launch_gate`).
- **Continuation = durable self-mail wakeup.** At the end of every round the Orchestrator writes state
  and sends a `[self-wakeup]` self-mail recording the next stage + intent; the mail-notifier wakes the
  loop. Live gateway reminders are NOT used for the spine (they die on gateway restart). Every wakeup
  is mirrored in the `self_wakeup` table so `recover` can rebuild intent after any interruption.
- **Idempotency / dedup.** Every dispatch carries a stable `loop_id` (= quest_id) + `handoff_id`.
  Resends reuse the same `handoff_id`; the `handoff` ledger lets receivers dedup and lets a supervisor
  resend only when downstream work cannot be observed (relay/edge-loop pattern).
- **Parallel fan-out** is optional and confined to the `experiment`/`analysis` stages: K Experimenter
  instances on K isolated worktrees, results collected by the Orchestrator (tree-loop reply-to-root).
- **Bookkeeping lives in SQLite + run artifacts only** — never in agent managed-memory pages. Memory
  pages hold operator-facing readable context only.

## Termination / Acceptance

- **Validity gates are hard.** A result cannot advance to synthesis unless the baseline gate is
  satisfied (or explicitly waived) and metric completeness/comparability passes. Generalizes
  correctness-as-hard-gate rule.
- **Acceptance is objective-defined.** The quest's objective declares its own success/acceptance
  criteria; the platform does not assume a single universal metric.

  > **Deep done-bar + scholarship (active gates).** Acceptance is a *deep* done-bar, not a single shallow
  > threshold the loop can clear without understanding — set at launch via the research-contract expansion
  > (`execplan/docs/research-contract.md`) and hard-gated at `not_started → running`. Correspondingly, a
  > `complete` finalize is **hard-gated** on genuine scholarly positioning (real Related Work + claim-linked
  > citations, not internal provenance) — the scholarship bar in `execplan/docs/publication-quality.md`,
  > checked by `lit audit` and `records.py::_finalize_scholarship_gate`.
- **Stop when** any of: acceptance criteria met; **convergence** (no new admissible findings for
  `convergence_patience` rounds); **budget** exhausted (round ceiling or cost/time); or an explicit
  **stop-loss** (novelty/evidence/reader-value collapse). A stop-loss that ends the quest on
  low-quality grounds requires **operator confirmation** (recorded as a gated `decision`).
- **Final output**: a publication-grade, **bilingual** deliverable (compiled `paper.pdf` + `paper-zh.pdf`
  with figures, bibliography, and submission bundle) for the best supported result, plus the full
  evidence trail (ideas, experiments, measurements, analyses, decisions, findings) — auditable end to end.

## Workspace Expectations

- **One quest = one self-contained folder** `runs/<quest-id>/`. Everything the quest produces lives
  inside it: the objective (`objective/`), baseline (`baseline/`), the **code repo** (`repo/`, =
  `quest.workspace_ref`), per-agent worktrees (`workspaces/`), per-round artifacts (`round-<n>/`),
  report/figures/refs/findings, and rendered mail. The repo is a git workspace (mounted via
  `houmao-utils-workspace-mgr`, git flavor): research branches → real git branches; parallel experiments
  → isolated **worktrees**, one mutable work root per Experimenter instance (no shared mutable roots).
- **Per-quest, not shared**: the objective spec and baseline are canonical under `runs/<quest-id>/`
  (read-only to agents). `shared/` is OPTIONAL staging/templates only — never the canonical source.
- The only **shared state** is the control plane: the single SQLite DB `runs/state.sqlite` (one active
  quest at a time) and the `.houmao/mailbox` messaging infra. Knowledge packs live under `execplan/packs/`.
  This is platform INFRASTRUCTURE, not a cross-quest data pool.
- **TOTAL QUEST ISOLATION**: a new quest never re-uses, refers to, or inspects ANY artifact of another
  quest — not another quest's `runs/<q>/` files, not `outputs/`, and not its DB rows. Findings
  and references are quest-owned (invariants `finding_quest_owned` + `reference_quest_owned`); every quest
  collects its data fresh. Agents read only their own quest's `runs/<this-quest>/` + their worktree.
- `outputs/` is an unused legacy location; every quest's materials live under `runs/<quest-id>/`.
- Findings memory persists across rounds within a quest, but never across quests.

## Constraints

- Never report a result as supported unless it passed the applicable validity gate.
- Metrics/measurements must come from real execution; agents may not invent numbers.
- Findings/reflexion lessons must be grounded in recorded measurements, not speculation.
- Domain knowledge stays as queryable data/skills (knowledge packs), not hard-coded in agent prose.
- The Orchestrator is the single authority for stage transitions and termination.
- All durable bookkeeping goes through the State harness; agents never hand-edit SQLite or memory pages.

## Open Questions

**Resolved during implementation:**

- **Domain pluggability surface** → RESOLVED: knowledge packs declare a `pack.toml` with `backs`
  (the harness command they serve) + `kind` (compiler/template/reference/…); among enabled packs of one
  (domain, kind) the lowest unique priority is primary (`adapter_priority_unique` invariant).
- **Single-agent vs role-specialized agents** → RESOLVED: **role-specialized** — six default-live participants
  (Orchestrator + Scout/Ideator, Experimenter ×≤8, Analyst, Writer, Reviewer), one per binding, plus an
  optional codex-tooled BO-reviewer (idea-level surrogate; stub fallback when not launched).
- **Concurrency** → RESOLVED: **one active quest at a time**, enforced by the `single_active_quest`
  invariant (quests share one control-plane DB, distinguished by `quest_id`).

**Still open:**

- **Prior-system features without a direct Houmao counterpart — operator decisions (resolved):**
  - **Cross-quest findings visibility → RESOLVED: total quest isolation.** Findings (and references) are
    quest-owned; no shared/global store. Enforced by schema (`quest_id` required, `scope` enum `['quest']`)
    + invariants `finding_quest_owned`/`reference_quest_owned`. A new quest never reuses/inspects another
    quest's findings, references, or artifacts.
  - Operator interface → **Houmao-native**: observe via `houmao-agent-inspect`/loop `status`; control
    via operator-via-mail recorded in `operator_intent_event`. No web UI/TUI built.
  - Multi-runner → **Houmao tools only** (`claude`/`codex`/`gemini`), chosen per role via
    `participant.tool`. Kimi/OpenCode dropped unless Houmao adds them.
  - Hypothesis refinement → **implement the BO refiner harness now** (see Participants).
  - Literature/arxiv → **implement the web/arxiv harness now** (see Participants).
  - Chat connectors → **skipped** for now (operator-via-mail replaces them).
  - Research Map / Canvas visualization → **skipped** for now (SQLite state is queryable; a renderer
    can be added later).
  - BenchStore → **subsumed** by `result` + `measurement`. Quirks files → **implemented** as `quirk`.
  - intake-audit → **implemented** as a first-class entry stage (+ `intake_asset`).
  - optimize → **implemented** as a first-class orchestrator-internal stage (+ `frontier_entry`).
  - manuscript-language + academic-outline validation → **implemented** as harness commands
    (`manuscript validate`, `outline validate`).
  - finalize → **enriched**: complete / stop / park_and_continue_later / publish_and_continue_from_new_incumbent
    (+ `finalize_outcome`).
  - rebuttal → **implemented** as a first-class Writer stage (+ route enum).
  - the domain/publication helper packs (paper-outline, paper-plot, figure-polish, nature-figure,
    nature-data, nature-polishing, nature-paper2ppt, science, mentor) → **integrated**: `outline` stage,
    harness extension commands (`render plot|polish|slides`, `manuscript polish|datastmt`, `knowledge query`),
    the `deepresearch-mentor` skill, and built-in `knowledge_pack`s under `execplan/packs/`.
  - **Publication path turned ON.** A new **`paper-latex`** compiler pack (backs `render report`) renders
    the Markdown manuscript → LaTeX article → compiled PDF (XeLaTeX/TinyTeX; auto-detects CJK via `ctexart`
    for the Chinese edition). The publication packs (paper-latex, paper-plot, figure-polish, and the
    nature-* figure/slides/data/polishing packs) are **enabled by default** so output quality matches the
    the reference counterparts; only `mentor-standards` stays disabled. Plus harness
    commands `lit bib` (references → `.bib`) and `manuscript bundle` (evidence ledger + claim↔evidence map
    + submission checklist, which tracks the EN + ZH PDFs and orphan claims).
