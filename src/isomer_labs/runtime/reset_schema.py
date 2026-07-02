"""Reset checkpoint schema helpers for Workspace Runtime persistence."""

from __future__ import annotations

import sqlite3


def create_reset_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS topic_reset_checkpoints (
            id TEXT PRIMARY KEY,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            status TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            payload_digest TEXT NOT NULL,
            checkpoint_digest TEXT NOT NULL,
            actor_ref TEXT,
            source_record_id TEXT,
            rendered_markdown_path TEXT,
            rendered_markdown_digest TEXT,
            diagnostics_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_topic_reset_checkpoints_topic
            ON topic_reset_checkpoints (research_topic_id, topic_workspace_id);
        CREATE INDEX IF NOT EXISTS idx_topic_reset_checkpoints_status
            ON topic_reset_checkpoints (status, updated_at);

        CREATE TABLE IF NOT EXISTS topic_reset_plans (
            id TEXT PRIMARY KEY,
            checkpoint_id TEXT NOT NULL,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            status TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            payload_digest TEXT NOT NULL,
            checkpoint_digest TEXT NOT NULL,
            precondition_digest TEXT NOT NULL,
            actor_ref TEXT,
            rendered_markdown_path TEXT,
            rendered_markdown_digest TEXT,
            diagnostics_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_topic_reset_plans_checkpoint
            ON topic_reset_plans (checkpoint_id, created_at);
        CREATE INDEX IF NOT EXISTS idx_topic_reset_plans_topic
            ON topic_reset_plans (research_topic_id, topic_workspace_id);
        CREATE INDEX IF NOT EXISTS idx_topic_reset_plans_status
            ON topic_reset_plans (status, updated_at);

        CREATE TABLE IF NOT EXISTS topic_reset_plan_actions (
            id TEXT PRIMARY KEY,
            plan_id TEXT NOT NULL,
            action TEXT NOT NULL,
            target_kind TEXT NOT NULL,
            target_ref TEXT,
            target_path TEXT,
            semantic_label TEXT,
            source_kind TEXT,
            status TEXT NOT NULL,
            details_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_topic_reset_plan_actions_plan
            ON topic_reset_plan_actions (plan_id, action, target_kind);
        CREATE INDEX IF NOT EXISTS idx_topic_reset_plan_actions_target
            ON topic_reset_plan_actions (target_kind, target_ref);

        CREATE TABLE IF NOT EXISTS topic_reset_outcomes (
            id TEXT PRIMARY KEY,
            checkpoint_id TEXT NOT NULL,
            plan_id TEXT NOT NULL,
            research_topic_id TEXT NOT NULL,
            topic_workspace_id TEXT NOT NULL,
            status TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            payload_digest TEXT NOT NULL,
            applied_actions_json TEXT NOT NULL,
            skipped_actions_json TEXT NOT NULL,
            failed_actions_json TEXT NOT NULL,
            diagnostics_json TEXT NOT NULL,
            actor_ref TEXT,
            started_at TEXT NOT NULL,
            finished_at TEXT NOT NULL,
            rendered_markdown_path TEXT,
            rendered_markdown_digest TEXT,
            provenance_refs_json TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_topic_reset_outcomes_plan
            ON topic_reset_outcomes (plan_id, finished_at);
        CREATE INDEX IF NOT EXISTS idx_topic_reset_outcomes_topic
            ON topic_reset_outcomes (research_topic_id, topic_workspace_id);
        """
    )
