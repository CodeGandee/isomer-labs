-- Generated SQLite state contract for deepsci-org loop-local bookkeeping.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS plan_metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS run_control (
    run_id TEXT PRIMARY KEY,
    run_state TEXT NOT NULL CHECK (run_state IN ('not_started', 'running', 'paused', 'recovering', 'parked', 'stopped', 'completed')),
    execution_mode TEXT NOT NULL CHECK (execution_mode IN ('manual', 'auto')),
    control_mode TEXT NOT NULL CHECK (control_mode IN ('manual', 'automatic')),
    domain_agent_team_template_ref TEXT NOT NULL,
    topic_agent_team_profile_id TEXT NOT NULL,
    agent_team_instance_id TEXT NOT NULL,
    research_topic_id TEXT NOT NULL,
    topic_workspace_ref TEXT NOT NULL,
    workspace_runtime_ref TEXT NOT NULL,
    active_gate_ref TEXT,
    parking_packet_id TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS participants (
    role_id TEXT PRIMARY KEY,
    role_kind TEXT NOT NULL,
    required INTEGER NOT NULL CHECK (required IN (0, 1)),
    scalable INTEGER NOT NULL CHECK (scalable IN (0, 1)),
    agent_profile_ref TEXT NOT NULL,
    capability_binding_ref TEXT NOT NULL,
    skill_projection_ref TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS handoffs (
    handoff_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES run_control(run_id),
    sender_role TEXT NOT NULL,
    receiver_role TEXT NOT NULL REFERENCES participants(role_id),
    workflow_stage TEXT NOT NULL,
    research_task_id TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('requested', 'in_progress', 'completed', 'blocked', 'needs_gate', 'partial', 'failed', 'normalized')),
    result_target_role TEXT NOT NULL,
    expected_outputs_json TEXT NOT NULL,
    artifact_refs_json TEXT NOT NULL DEFAULT '[]',
    evidence_item_refs_json TEXT NOT NULL DEFAULT '[]',
    research_claim_refs_json TEXT NOT NULL DEFAULT '[]',
    gate_recommendations_json TEXT NOT NULL DEFAULT '[]',
    recommended_next_stage TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mail_payloads (
    payload_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    schema_id TEXT NOT NULL,
    schema_version TEXT NOT NULL,
    handoff_id TEXT,
    sender_role TEXT,
    receiver_role TEXT,
    payload_path TEXT,
    rendered_path TEXT,
    houmao_mail_ref TEXT,
    processing_status TEXT NOT NULL CHECK (processing_status IN ('created', 'rendered', 'sent', 'received', 'processed', 'archived', 'failed')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS operator_intent_events (
    event_id TEXT PRIMARY KEY,
    run_id TEXT,
    event_kind TEXT NOT NULL CHECK (event_kind IN ('pause', 'resume', 'stop', 'mode_switch', 'redirect', 'gate_outcome', 'recover', 'manual_step', 'override')),
    actor_ref TEXT NOT NULL,
    reason TEXT NOT NULL,
    payload_ref TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS parking_packets (
    parking_packet_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    reason TEXT NOT NULL,
    blocker_refs_json TEXT NOT NULL DEFAULT '[]',
    last_stable_refs_json TEXT NOT NULL DEFAULT '[]',
    next_safe_operator_action TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_handoffs_run_status ON handoffs(run_id, status);
CREATE INDEX IF NOT EXISTS idx_handoffs_receiver_status ON handoffs(receiver_role, status);
CREATE INDEX IF NOT EXISTS idx_mail_payloads_schema_status ON mail_payloads(schema_id, processing_status);
CREATE INDEX IF NOT EXISTS idx_operator_intent_run_kind ON operator_intent_events(run_id, event_kind);
