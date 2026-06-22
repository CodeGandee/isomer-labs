"""Stable identifier helpers for Workspace Runtime records."""

from __future__ import annotations

import re


def _path_plan_id(topic_workspace_id: str, surface: str) -> str:
    return f"path-plan-{_slug(topic_workspace_id)}-{_slug(surface)}"


def _provenance_ref(record_kind: str, record_id: str) -> str:
    return f"provenance:{record_kind}:{record_id}"


def _slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "-", value).strip("-") or "record"
