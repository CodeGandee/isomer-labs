"""Stable identifier helpers for Workspace Runtime records."""

from __future__ import annotations

import re
import uuid


def _path_plan_id(topic_workspace_id: str, surface: str) -> str:
    return f"path-plan-{_slug(topic_workspace_id)}-{_slug(surface)}"


def _provenance_ref(record_kind: str, record_id: str) -> str:
    return f"provenance:{record_kind}:{record_id}"


def _slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "-", value).strip("-") or "record"


def _agent_instance_id(topic_workspace_id: str, team_id: str, role_id: str) -> str:
    """Return a globally unique Agent Instance id.

    The id embeds the owning Topic Workspace, Agent Team Instance, and Agent
    Role for readability, and appends a short random suffix so that ids are
    unique across the whole Project.
    """
    short_uuid = uuid.uuid4().hex[:8]
    return f"agent-{_slug(topic_workspace_id)}-{_slug(team_id)}-{_slug(role_id)}-{short_uuid}"
