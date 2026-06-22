CREATE TABLE IF NOT EXISTS participants (
  role_id TEXT PRIMARY KEY,
  role_kind TEXT NOT NULL,
  active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS handoffs (
  handoff_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  sender_role TEXT NOT NULL,
  receiver_role TEXT NOT NULL,
  workflow_stage TEXT NOT NULL,
  status TEXT NOT NULL,
  request_payload_ref TEXT,
  result_payload_ref TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS payloads (
  payload_id TEXT PRIMARY KEY,
  schema_id TEXT NOT NULL,
  payload_kind TEXT NOT NULL,
  handoff_id TEXT,
  payload_ref TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS decisions (
  decision_id TEXT PRIMARY KEY,
  gate_ref TEXT NOT NULL,
  decision_record_ref TEXT NOT NULL,
  selected_research_inquiry_ref TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS operator_intents (
  intent_id TEXT PRIMARY KEY,
  intent_kind TEXT NOT NULL,
  actor_ref TEXT NOT NULL,
  rationale TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
