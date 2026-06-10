# Loop Overview: DeepResearch (general-purpose autonomous research platform)

## Source

- Reference system: **DeepScientist** (https://github.com/ResearAI/DeepScientist) — a local-first
  autonomous research studio: one quest = one git repo, persistent findings memory, hypothesis →
  experiment → analysis → write loop, with human takeover preserved throughout.
- This loop re-expresses DeepScientist's research loop as a Houmao `loop-pro` **tree-loop**, with
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

## Participants

Role → implementation is resolved per-deployment, but the default split is LLM-agents for reasoning
and deterministic harness tools for anything that must not be hallucinated.

LLM agents:

- **Orchestrator** *(LLM, tree-loop root)*: owns the research state machine — selects the next stage,
  tracks round/budget, applies acceptance and stop-loss rules, records every transition in the
  `decision` log, and arms the next durable self-wakeup. Replaces DeepScientist's `runtime_state.json`
  + `decision` / `intake-audit` stage skills. Owns iteration and termination.
- **Scout / Ideator** *(LLM)*: scope intake, baseline framing, hypothesis generation, route selection.
  Replaces DeepScientist `scout` + `idea`.
- **Experimenter** *(LLM, may run as K parallel instances)*: design, implement, and execute a bounded
  experiment inside an **isolated worktree** so parallel routes never clobber each other. Replaces
  DeepScientist `experiment`; the worktree model preserves DeepScientist's "branches express research
  structure / keep failed routes" principle.
- **Analyst** *(LLM)*: analysis campaigns — slice/ablate results, decompose errors, judge whether a
  result confirms / blocks / is inconclusive against a parent claim. Replaces `analysis-campaign`.
- **Writer** *(LLM)*: synthesize durable evidence into a report/manuscript artifact. Replaces `write`.
- **Reviewer** *(LLM)*: skeptical audit of a draft before finalize; rebuttal handling. Replaces
  `review` / `rebuttal`.

Harness tools (deterministic; no LLM; the trust boundary):

- **State store**: read/write the SQLite control plane (the only authority for loop bookkeeping).
- **Experiment runner**: execute an experiment's run contract and capture results/metrics honestly.
  *Domain-pluggable* — the default is a generic command-runner; domains override it.
- **Validator**: baseline gate, metric-completeness/comparability checks, manuscript coverage,
  claim↔evidence consistency. *Partly domain-pluggable.* Replaces DeepScientist `artifact.validate_*`.
- **Findings store**: persist/retrieve durable findings memory + reflexion notes (cross-round and
  cross-quest). Replaces DeepScientist `memory/{ideas,decisions,knowledge}` + reflexion store.
- **Git checkpoint**: commit durable artifacts into the quest worktree; manage branches/worktrees.
  Replaces DeepScientist `git.auto_checkpoint`.
- **Artifact compiler**: render reports/figures (e.g. LaTeX/markdown/plots). *Domain-pluggable.*
- **Idea refiner (Bayesian optimization)**: a deterministic harness command that reads the
  `search_space` + each experiment's `experiment_param` + the primary `measurement`, and proposes the
  next point to evaluate. Used when a quest declares a tunable search space; the proposal is recorded
  as a new idea/experiment (`experiment_param.proposed_by = 'bo'`). Replaces DeepScientist's
  Bayesian-optimization hypothesis refinement. The Orchestrator may instead refine ideas heuristically
  from findings memory when no search space is defined.
- **Literature / web search**: a generic harness command for arxiv + web retrieval; fetched sources
  land in the `reference` table (cached under `runs/<quest>/refs/`) and become `claim_evidence` of
  `source_kind = 'reference'`. Available to all quests. Replaces DeepScientist `artifact.arxiv` / deepxiv.

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
  DeepScientist's correctness-as-hard-gate rule.
- **Acceptance is objective-defined.** The quest's objective declares its own success/acceptance
  criteria; the platform does not assume a single universal metric.
- **Stop when** any of: acceptance criteria met; **convergence** (no new admissible findings for
  `convergence_patience` rounds); **budget** exhausted (round ceiling or cost/time); or an explicit
  **stop-loss** (novelty/evidence/reader-value collapse). A stop-loss that ends the quest on
  low-quality grounds requires **operator confirmation** (recorded as a gated `decision`).
- **Final output**: the best supported result/artifact plus the full evidence trail (ideas,
  experiments, measurements, analyses, decisions, findings) — auditable end to end.

## Workspace Expectations

- One quest = one **operator-owned git workspace** (mounted via `houmao-utils-workspace-mgr`,
  git flavor). Research branches → real git branches; parallel experiments → isolated **worktrees**,
  one mutable work root per Experimenter instance (no shared mutable roots).
- Shared read-only resources: the objective spec, baseline reference, and any enabled knowledge packs.
- Durable per-round run artifacts under `runs/<quest-id>/round-<n>/...`; SQLite holds refs + scalars.
- Findings memory persists across rounds and (optionally) across quests for reuse.

## Constraints

- Never report a result as supported unless it passed the applicable validity gate.
- Metrics/measurements must come from real execution; agents may not invent numbers.
- Findings/reflexion lessons must be grounded in recorded measurements, not speculation.
- Domain knowledge stays as queryable data/skills (knowledge packs), not hard-coded in agent prose.
- The Orchestrator is the single authority for stage transitions and termination.
- All durable bookkeeping goes through the State harness; agents never hand-edit SQLite or memory pages.

## Open Questions (to resolve in clarify-intent / ADRs)

- **Domain pluggability surface:** exact contract for overriding Experiment runner / Validator /
  Artifact compiler per domain (knowledge-pack manifest schema). RESOLVE before `execplan-harness`.
- **Single-agent vs role-specialized agents:** run one general worker re-prompted per stage, or
  distinct specialists (Scout/Experimenter/Analyst/Writer/Reviewer)? Affects agent bindings + cost.
- **Cross-quest findings visibility:** isolated per quest (DeepScientist default `independent`) vs a
  shared global findings store. Affects `finding_memory.scope` defaults.
- **Concurrency:** one active quest at a time (DeepScientist `max_concurrent_quests: 1`) vs multiple.
- **DeepScientist features without a direct Houmao counterpart — operator decisions (resolved):**
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
  - DeepScientist domain/publication helpers (paper-outline, paper-plot, figure-polish, nature-figure,
    nature-data, nature-polishing, nature-paper2ppt, science, mentor) → **integrated**: `outline` stage,
    harness extension commands (`render plot|polish|slides`, `manuscript polish|datastmt`, `knowledge query`),
    the `deepresearch-mentor` skill, and built-in optional `knowledge_pack`s (disabled by default to keep
    the core domain-neutral; see `execplan/packs/`).
