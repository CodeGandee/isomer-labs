-- Generated sqlite control-plane schema for the DeepResearch general-purpose research loop.
-- Authority: specs/state/state-overview.md. Rich payloads live as artifacts under runs/<quest-id>/;
-- columns hold refs + scalars. Timestamps are ISO-8601 strings supplied by the caller (harness),
-- never generated implicitly. quest_id is the loop_id used for idempotency.
--
-- Design notes:
--   * Framework-fixed lifecycle states use CHECK constraints (closed set, owned by the platform).
--   * The research `stage` is a soft reference into stage_catalog so DOMAINS CAN ADD STAGES without
--     editing this file (general-purpose extensibility).
--   * Domain-specific payloads (kernels, sequences, proofs, ...) are NOT modeled as columns; they are
--     artifacts + schema-light measurement rows, so the core schema stays domain-neutral.

PRAGMA foreign_keys = ON;

-- ──────────────────────────────────────────────────────────────────────────
-- Extensibility registries
-- ──────────────────────────────────────────────────────────────────────────

-- Canonical + domain-added stages. Seeded with the default research stages; a knowledge pack may
-- INSERT additional stages (e.g. 'wet-lab', 'formal-proof') without schema changes.
CREATE TABLE IF NOT EXISTS stage_catalog (
    stage        TEXT PRIMARY KEY,
    ordinal      INTEGER NOT NULL,            -- default sequencing hint; Orchestrator may override
    description  TEXT NOT NULL,
    is_builtin   INTEGER NOT NULL DEFAULT 1,  -- 0 for domain-added stages
    owning_role  TEXT                         -- default agent role that executes this stage
);

INSERT OR IGNORE INTO stage_catalog (stage, ordinal, description, is_builtin, owning_role) VALUES
    ('intake-audit', 5, 'audit + trust-rank pre-existing assets when a quest starts from them', 1, 'scout-ideator'),
    ('scope',     10, 'intake + framing of the objective',                 1, 'scout-ideator'),
    ('baseline',  20, 'establish/verify a trustworthy comparator + metric', 1, 'scout-ideator'),
    ('idea',      30, 'hypothesis generation + route selection',           1, 'scout-ideator'),
    ('optimize',  35, 'algorithm-first frontier mgmt: rank/promote/fuse candidates', 1, 'orchestrator'),
    ('experiment',40, 'design, implement, execute a bounded experiment',   1, 'experimenter'),
    ('analysis',  50, 'slice/ablate results, decompose errors',            1, 'analyst'),
    ('decision',  60, 'route judgment from durable evidence',              1, 'orchestrator'),
    ('outline',   65, 'paper outline: paper-view vs evidence-view, scoped claims, evaluation/analysis plan', 1, 'writer'),
    ('write',     70, 'synthesize evidence into a report/manuscript',      1, 'writer'),
    ('review',    80, 'skeptical audit of the draft',                      1, 'reviewer'),
    ('rebuttal',  85, 'map external-reviewer feedback -> experiments + manuscript deltas + response', 1, 'writer'),
    ('finalize',  90, 'closure + archival; complete|stop|park|publish-and-continue', 1, 'orchestrator');

-- Pluggable domain knowledge: extra skills, references, templates, validators, metric vocabularies.
CREATE TABLE IF NOT EXISTS knowledge_pack (
    pack_id     TEXT PRIMARY KEY,
    domain      TEXT NOT NULL,
    name        TEXT NOT NULL,
    kind        TEXT NOT NULL CHECK (kind IN ('skill','reference','template','validator','metric_vocab','runner','compiler')),
    ref         TEXT NOT NULL,                 -- path/uri to the pack artifact (e.g. a domain adapter)
    enabled     INTEGER NOT NULL DEFAULT 1,
    -- Deterministic adapter resolution: among enabled packs of the same (domain, kind), the one with
    -- the LOWEST priority is primary; others are fallbacks. Priorities must be unique per (domain,kind)
    -- (invariant adapter_priority_unique), so resolution never ties. Default platform: no packs enabled.
    priority    INTEGER NOT NULL DEFAULT 100,
    created_at  TEXT NOT NULL
);

-- ──────────────────────────────────────────────────────────────────────────
-- Quest (= run = loop_id) : top-level config + state-machine cursor
-- ──────────────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS quest (
    quest_id            TEXT PRIMARY KEY,        -- also the loop_id for handoff idempotency
    plan_revision       INTEGER NOT NULL DEFAULT 1,
    title               TEXT NOT NULL,
    domain              TEXT NOT NULL DEFAULT 'general',
    objective_ref       TEXT NOT NULL,           -- artifact: brief/goal spec
    acceptance_ref      TEXT,                    -- artifact: objective-defined success criteria
    workspace_ref       TEXT NOT NULL,           -- operator-owned git workspace root
    -- budget / stop policy
    max_rounds          INTEGER NOT NULL DEFAULT 24,
    convergence_patience INTEGER NOT NULL DEFAULT 3,  -- rounds with no new admissible finding ⇒ converged
    cost_budget         REAL,                    -- optional, units defined by deployment
    baseline_gate       TEXT NOT NULL DEFAULT 'pending'
                          CHECK (baseline_gate IN ('pending','passed','waived','blocked')),
    -- lifecycle (framework-fixed)
    run_state           TEXT NOT NULL DEFAULT 'not_started'
                          CHECK (run_state IN ('not_started','running','paused','recovering',
                                               'waiting_user','parked','stopped','completed')),
    execution_mode      TEXT NOT NULL DEFAULT 'auto' CHECK (execution_mode IN ('auto','manual')),
    -- cursor
    round_index         INTEGER NOT NULL DEFAULT 0,
    current_stage       TEXT REFERENCES stage_catalog(stage),
    active_branch_id    TEXT,                    -- → branch.branch_id
    active_idea_id      TEXT,                    -- → idea.idea_id
    -- result pointer
    best_result_ref     TEXT,                    -- → result.result_id of best supported result
    stop_reason         TEXT,
    created_at          TEXT NOT NULL,
    updated_at          TEXT NOT NULL
);

-- One row per round; tracks the per-round stage micro-state and expected/received handoffs.
CREATE TABLE IF NOT EXISTS round (
    quest_id         TEXT NOT NULL REFERENCES quest(quest_id),
    round_index      INTEGER NOT NULL,
    stage            TEXT NOT NULL REFERENCES stage_catalog(stage),
    branch_id        TEXT,
    expected_handoffs INTEGER NOT NULL DEFAULT 0,  -- e.g. K parallel experimenters
    received_handoffs INTEGER NOT NULL DEFAULT 0,
    status           TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open','closed')),
    summary_ref      TEXT,                          -- rendered round summary artifact
    created_at       TEXT NOT NULL,
    updated_at       TEXT NOT NULL,
    PRIMARY KEY (quest_id, round_index)
);

CREATE TABLE IF NOT EXISTS participant (
    quest_id    TEXT NOT NULL REFERENCES quest(quest_id),
    instance_id TEXT NOT NULL,
    role        TEXT NOT NULL,
    tool        TEXT,                            -- Houmao tool binding: claude|codex|gemini
    last_seen   TEXT,
    PRIMARY KEY (quest_id, instance_id)
);

-- ──────────────────────────────────────────────────────────────────────────
-- Research structure: branches (worktrees) → ideas → experiments → results → analyses
-- ──────────────────────────────────────────────────────────────────────────

-- Research routes. Failed routes are PARKED/ABANDONED, never deleted (preserve-failed-routes).
CREATE TABLE IF NOT EXISTS branch (
    branch_id    TEXT PRIMARY KEY,
    quest_id     TEXT NOT NULL REFERENCES quest(quest_id),
    parent_branch_id TEXT REFERENCES branch(branch_id),
    git_branch   TEXT NOT NULL,
    worktree_ref TEXT,                            -- isolated work root; null if not materialized
    status       TEXT NOT NULL DEFAULT 'active'
                  CHECK (status IN ('active','parked','abandoned','merged')),
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL
);

-- Pre-existing assets audited at quest entry (intake-audit stage). Trust-ranked; a trusted asset may
-- be ADOPTED into a state row (e.g. an existing baseline -> baseline_gate, existing results -> result).
CREATE TABLE IF NOT EXISTS intake_asset (
    asset_id     TEXT PRIMARY KEY,
    quest_id     TEXT NOT NULL REFERENCES quest(quest_id),
    kind         TEXT NOT NULL CHECK (kind IN ('baseline','result','draft','dataset','code','paper','other')),
    source_ref   TEXT NOT NULL,                  -- path/uri of the pre-existing asset
    trust        TEXT NOT NULL DEFAULT 'suspect' CHECK (trust IN ('trusted','suspect','untrusted','rejected')),
    adopt_as     TEXT,                            -- id/token of the state row it was adopted into (null if not adopted)
    notes        TEXT,
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS idea (
    idea_id        TEXT PRIMARY KEY,
    quest_id       TEXT NOT NULL REFERENCES quest(quest_id),
    branch_id      TEXT REFERENCES branch(branch_id),
    parent_idea_id TEXT REFERENCES idea(idea_id),
    round_index    INTEGER,
    statement      TEXT NOT NULL,                 -- the hypothesis / direction, short form
    route          TEXT,                          -- chosen route label
    artifact_ref   TEXT,                          -- full idea memo
    status         TEXT NOT NULL DEFAULT 'proposed'
                    CHECK (status IN ('proposed','selected','rejected','exhausted')),
    created_at     TEXT NOT NULL,
    updated_at     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS experiment (
    experiment_id  TEXT PRIMARY KEY,
    quest_id       TEXT NOT NULL REFERENCES quest(quest_id),
    idea_id        TEXT REFERENCES idea(idea_id),
    branch_id      TEXT REFERENCES branch(branch_id),
    round_index    INTEGER,
    run_contract_ref TEXT NOT NULL,               -- locked run spec artifact
    is_baseline    INTEGER NOT NULL DEFAULT 0,
    status         TEXT NOT NULL DEFAULT 'designed'
                    CHECK (status IN ('designed','running','done','failed','aborted')),
    log_ref        TEXT,
    created_at     TEXT NOT NULL,
    updated_at     TEXT NOT NULL
);

-- Tunable dimensions for an objective (the search space the BO refiner optimizes over).
-- Domain-neutral: each dimension is named + typed; bounds/choices held as text, parsed by the refiner.
CREATE TABLE IF NOT EXISTS search_space (
    space_id     TEXT NOT NULL,                  -- a quest may define more than one space
    quest_id     TEXT NOT NULL REFERENCES quest(quest_id),
    dim_name     TEXT NOT NULL,
    dim_kind     TEXT NOT NULL CHECK (dim_kind IN ('real','int','categorical','bool')),
    low          REAL,                            -- real/int bounds
    high         REAL,
    choices      TEXT,                            -- json array for categorical
    log_scale    INTEGER NOT NULL DEFAULT 0,
    created_at   TEXT NOT NULL,
    PRIMARY KEY (quest_id, space_id, dim_name)
);

-- The concrete point (parameter assignment) an experiment evaluated. BO reads these + the primary
-- measurement to propose the next point; the proposal is recorded as a new idea/experiment.
CREATE TABLE IF NOT EXISTS experiment_param (
    experiment_id TEXT NOT NULL REFERENCES experiment(experiment_id),
    space_id      TEXT,
    dim_name      TEXT NOT NULL,
    value_num     REAL,
    value_text    TEXT,
    proposed_by   TEXT NOT NULL DEFAULT 'agent' CHECK (proposed_by IN ('agent','bo','operator','seed')),
    created_at    TEXT NOT NULL,
    PRIMARY KEY (experiment_id, dim_name)
);

-- A result is one validated outcome of an experiment (an experiment may yield several).
CREATE TABLE IF NOT EXISTS result (
    result_id      TEXT PRIMARY KEY,
    quest_id       TEXT NOT NULL REFERENCES quest(quest_id),
    experiment_id  TEXT NOT NULL REFERENCES experiment(experiment_id),
    round_index    INTEGER,
    validity       TEXT NOT NULL DEFAULT 'unchecked'
                    CHECK (validity IN ('unchecked','valid','invalid','incomparable')),
    artifact_ref   TEXT NOT NULL,                 -- runs/<quest>/round-<n>/result.json
    created_at     TEXT NOT NULL
);

-- Schema-light, domain-neutral metric capture. Any domain records measurements here by name.
CREATE TABLE IF NOT EXISTS measurement (
    measurement_id TEXT PRIMARY KEY,
    result_id      TEXT NOT NULL REFERENCES result(result_id),
    metric_name    TEXT NOT NULL,                 -- domain-defined (validated against metric_vocab pack)
    value_num      REAL,
    value_text     TEXT,
    unit           TEXT,
    is_primary     INTEGER NOT NULL DEFAULT 0,    -- the objective's headline metric
    artifact_ref   TEXT,
    created_at     TEXT NOT NULL
);

-- Optimization frontier for algorithm-first quests (the `optimize` stage, orchestrator-owned).
-- Ranks candidate routes by their primary objective; tracks the incumbent and promotion/fusion.
CREATE TABLE IF NOT EXISTS frontier_entry (
    entry_id      TEXT PRIMARY KEY,
    quest_id      TEXT NOT NULL REFERENCES quest(quest_id),
    candidate_kind TEXT NOT NULL CHECK (candidate_kind IN ('branch','experiment','result')),
    candidate_ref TEXT NOT NULL,                  -- id of the branch/experiment/result this entry ranks
    round_index   INTEGER,
    score         REAL,                           -- primary objective value (BO objective sense applies)
    rank          INTEGER,                        -- 1 = best; nullable for unranked candidates
    status        TEXT NOT NULL DEFAULT 'candidate'
                   CHECK (status IN ('candidate','incumbent','promoted','parked','dropped','fused')),
    created_at    TEXT NOT NULL,
    updated_at    TEXT NOT NULL,
    UNIQUE (quest_id, candidate_ref)
);

CREATE TABLE IF NOT EXISTS analysis (
    analysis_id    TEXT PRIMARY KEY,
    quest_id       TEXT NOT NULL REFERENCES quest(quest_id),
    result_id      TEXT REFERENCES result(result_id),
    round_index    INTEGER,
    parent_claim   TEXT,                          -- the claim this slice tests
    finding        TEXT,
    verdict        TEXT NOT NULL DEFAULT 'inconclusive'
                    CHECK (verdict IN ('confirms','blocks','inconclusive')),
    artifact_ref   TEXT,
    created_at     TEXT NOT NULL
);

-- ──────────────────────────────────────────────────────────────────────────
-- Evidence + claims (findings memory core) and the decision/route log
-- ──────────────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS claim (
    claim_id     TEXT PRIMARY KEY,
    quest_id     TEXT NOT NULL REFERENCES quest(quest_id),
    statement    TEXT NOT NULL,
    status       TEXT NOT NULL DEFAULT 'open'
                  CHECK (status IN ('open','supported','refuted','withdrawn')),
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL
);

-- Claim ↔ evidence map. source_kind keeps it general (a result, an analysis, a citation, ...).
CREATE TABLE IF NOT EXISTS claim_evidence (
    claim_id      TEXT NOT NULL REFERENCES claim(claim_id),
    source_kind   TEXT NOT NULL CHECK (source_kind IN ('result','analysis','measurement','reference','external')),
    source_ref    TEXT NOT NULL,                  -- id or uri of the evidence
    relation      TEXT NOT NULL DEFAULT 'supports' CHECK (relation IN ('supports','contradicts','contextualizes')),
    -- A 'contradicts' link may be acknowledged and later resolved/rebutted. Only UNRESOLVED
    -- contradictions block a claim from becoming 'supported'.
    resolved      INTEGER NOT NULL DEFAULT 0,     -- 0=open, 1=resolved/rebutted
    resolution_ref TEXT,                          -- artifact/decision explaining the rebuttal
    resolved_at   TEXT,
    created_at    TEXT NOT NULL,
    PRIMARY KEY (claim_id, source_kind, source_ref)
);

-- Every state-machine transition / route judgment (replaces DeepScientist runtime_state + decision).
CREATE TABLE IF NOT EXISTS decision (
    decision_id   TEXT PRIMARY KEY,
    quest_id      TEXT NOT NULL REFERENCES quest(quest_id),
    round_index   INTEGER,
    from_stage    TEXT REFERENCES stage_catalog(stage),
    to_stage      TEXT REFERENCES stage_catalog(stage),
    route         TEXT NOT NULL,                  -- continue|branch|reset|stop|finalize|...
    rationale_ref TEXT,
    requires_user_confirm INTEGER NOT NULL DEFAULT 0,
    confirmed     INTEGER NOT NULL DEFAULT 0,     -- 0 until operator confirms a gated decision
    created_at    TEXT NOT NULL
);

-- Finalize outcomes (richer than complete/stop): append one row per finalize event.
--   complete | stop                          -> run_state completed|stopped (terminal)
--   park (park_and_continue_later)           -> run_state parked; reopen_conditions required
--   publish_and_continue (from new incumbent)-> run_state stays running; next_incumbent_ref required
CREATE TABLE IF NOT EXISTS finalize_outcome (
    outcome_id        TEXT PRIMARY KEY,
    quest_id          TEXT NOT NULL REFERENCES quest(quest_id),
    outcome           TEXT NOT NULL CHECK (outcome IN ('complete','stop','park','publish_and_continue')),
    published_ref     TEXT,                        -- the published result/report artifact (publish_and_continue)
    next_incumbent_ref TEXT,                       -- branch/result to continue from (publish_and_continue)
    reopen_conditions TEXT,                         -- when/why to resume (park)
    created_at        TEXT NOT NULL
);

-- Durable, reusable findings + reflexion. scope='global' enables cross-quest reuse.
CREATE TABLE IF NOT EXISTS finding_memory (
    memory_id     TEXT PRIMARY KEY,
    quest_id      TEXT REFERENCES quest(quest_id),  -- null allowed for global-only entries
    scope         TEXT NOT NULL DEFAULT 'quest' CHECK (scope IN ('quest','global')),
    kind          TEXT NOT NULL CHECK (kind IN ('idea','decision','knowledge','lesson','reference')),
    summary       TEXT NOT NULL,
    artifact_ref  TEXT,
    grounded_by   TEXT,                            -- ref to the measurement/result it is grounded in
    created_at    TEXT NOT NULL,
    updated_at    TEXT NOT NULL
);

-- External knowledge fetched by the web/arxiv harness (literature, citations, sources).
CREATE TABLE IF NOT EXISTS reference (
    reference_id TEXT PRIMARY KEY,
    quest_id     TEXT REFERENCES quest(quest_id),  -- null for globally cached sources
    source       TEXT NOT NULL CHECK (source IN ('arxiv','web','doi','manual')),
    cite_key     TEXT,                            -- bibtex key when applicable
    title        TEXT,
    uri          TEXT NOT NULL,
    artifact_ref TEXT,                             -- cached fetched content under runs/<quest>/refs/
    fetched_at   TEXT NOT NULL,
    created_at   TEXT NOT NULL
);

-- Generic artifact index (figures, drafts, reports, bundles).
CREATE TABLE IF NOT EXISTS artifact (
    artifact_id  TEXT PRIMARY KEY,
    quest_id     TEXT NOT NULL REFERENCES quest(quest_id),
    round_index  INTEGER,
    kind         TEXT NOT NULL,                   -- report|figure|draft|bundle|log|other
    ref          TEXT NOT NULL,                   -- path under runs/<quest>/...
    created_at   TEXT NOT NULL
);

-- ──────────────────────────────────────────────────────────────────────────
-- Continuation + comms ledgers (self-mail wakeup + handoff idempotency)
-- ──────────────────────────────────────────────────────────────────────────

-- Durable backbone of the self-mail wakeup spine. recover/ resume rebuild intent from here.
CREATE TABLE IF NOT EXISTS self_wakeup (
    wakeup_id     TEXT PRIMARY KEY,
    quest_id      TEXT NOT NULL REFERENCES quest(quest_id),
    -- Continuation lane groups wakeups of one self-driven thread. The initial tree-loop uses a single
    -- lane 'main' (one orchestrator-owned thread), but the model supports multiple lanes later with
    -- no schema change: invariants enforce one open wakeup PER LANE, and (as an initial policy only)
    -- one active lane per quest.
    continuation_lane TEXT NOT NULL DEFAULT 'main',
    handoff_id    TEXT NOT NULL,                  -- stable id; resends reuse it
    next_stage    TEXT REFERENCES stage_catalog(stage),
    reason        TEXT NOT NULL,                  -- wake-up reason / next-step intent
    next_action   TEXT,                           -- exact first action on resume
    message_ref   TEXT,                           -- opaque mailbox ref of the self-mail
    status        TEXT NOT NULL DEFAULT 'armed'
                  CHECK (status IN ('armed','delivered','consumed','superseded','failed')),
    deliver_after TEXT,                           -- optional ISO time hint
    created_at    TEXT NOT NULL,
    updated_at    TEXT NOT NULL
);

-- Logical handoff ledger for idempotency/dedup (loop_id = quest_id, stable handoff_id).
-- Resends reuse handoff_id; receivers dedup; supervisor resends only when downstream is unobservable.
CREATE TABLE IF NOT EXISTS handoff (
    handoff_id    TEXT NOT NULL,
    quest_id      TEXT NOT NULL REFERENCES quest(quest_id),
    round_index   INTEGER,
    schema_id     TEXT NOT NULL,                  -- message/template type
    from_role     TEXT,
    to_role       TEXT,
    status        TEXT NOT NULL DEFAULT 'pending'
                  CHECK (status IN ('pending','sent','acked','result_received','processed','failed')),
    attempt_count INTEGER NOT NULL DEFAULT 0,
    max_attempts  INTEGER NOT NULL DEFAULT 5,
    receipt_due_at TEXT,
    result_due_at  TEXT,
    created_at    TEXT NOT NULL,
    updated_at    TEXT NOT NULL,
    PRIMARY KEY (quest_id, handoff_id)
);

-- Physical message log; references the logical handoff.
CREATE TABLE IF NOT EXISTS mail_log (
    payload_id   TEXT PRIMARY KEY,
    quest_id     TEXT NOT NULL REFERENCES quest(quest_id),
    handoff_id   TEXT,
    round_index  INTEGER,
    schema_id    TEXT NOT NULL,
    direction    TEXT NOT NULL CHECK (direction IN ('out','in')),
    sender       TEXT,
    recipient    TEXT,
    message_ref  TEXT,                            -- opaque mailbox ref
    status       TEXT NOT NULL DEFAULT 'sent'
                  CHECK (status IN ('sent','received','processed','failed')),
    created_at   TEXT NOT NULL
);

-- Operator control-plane events (pause/resume/stop/override/takeover).
CREATE TABLE IF NOT EXISTS operator_intent_event (
    event_id    TEXT PRIMARY KEY,
    quest_id    TEXT NOT NULL REFERENCES quest(quest_id),
    kind        TEXT NOT NULL CHECK (kind IN ('pause','resume','stop','override','recover','set-mode','takeover','handback','confirm')),
    detail      TEXT,
    created_at  TEXT NOT NULL
);

-- Append-only durable quirks (framework + system pitfalls); replaces DeepScientist quirks files.
CREATE TABLE IF NOT EXISTS quirk (
    quirk_id    TEXT PRIMARY KEY,
    layer       TEXT NOT NULL CHECK (layer IN ('framework','system')),
    surface     TEXT NOT NULL,
    symptom     TEXT NOT NULL,
    workaround  TEXT,
    status      TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open','mitigated','resolved')),
    created_at  TEXT NOT NULL
);

-- ──────────────────────────────────────────────────────────────────────────
-- Indexes
-- ──────────────────────────────────────────────────────────────────────────

CREATE INDEX IF NOT EXISTS idx_round_quest      ON round(quest_id, status);
CREATE INDEX IF NOT EXISTS idx_idea_quest        ON idea(quest_id, status);
CREATE INDEX IF NOT EXISTS idx_experiment_quest  ON experiment(quest_id, round_index, status);
CREATE INDEX IF NOT EXISTS idx_result_quest      ON result(quest_id, validity);
CREATE INDEX IF NOT EXISTS idx_measurement_result ON measurement(result_id, metric_name);
CREATE INDEX IF NOT EXISTS idx_analysis_quest    ON analysis(quest_id, verdict);
CREATE INDEX IF NOT EXISTS idx_claimev_claim     ON claim_evidence(claim_id);
CREATE INDEX IF NOT EXISTS idx_decision_quest    ON decision(quest_id, round_index);
CREATE INDEX IF NOT EXISTS idx_findmem_scope     ON finding_memory(scope, kind);
CREATE INDEX IF NOT EXISTS idx_wakeup_open       ON self_wakeup(quest_id, continuation_lane, status);
CREATE INDEX IF NOT EXISTS idx_handoff_status    ON handoff(quest_id, status);
CREATE INDEX IF NOT EXISTS idx_mail_quest        ON mail_log(quest_id, handoff_id, status);
CREATE INDEX IF NOT EXISTS idx_branch_quest      ON branch(quest_id, status);
CREATE INDEX IF NOT EXISTS idx_param_experiment  ON experiment_param(experiment_id);
CREATE INDEX IF NOT EXISTS idx_reference_quest   ON reference(quest_id, source);
CREATE INDEX IF NOT EXISTS idx_intake_quest      ON intake_asset(quest_id, trust);
CREATE INDEX IF NOT EXISTS idx_frontier_quest    ON frontier_entry(quest_id, status, rank);
CREATE INDEX IF NOT EXISTS idx_finalize_quest    ON finalize_outcome(quest_id, outcome);
