"""In-memory recent Project Web diagnostic buffer."""

from __future__ import annotations

from collections import deque
from datetime import UTC, datetime
from typing import Any, Mapping


class RecentErrorBuffer:
    """Bounded process-local diagnostic ring buffer."""

    def __init__(self, *, maxlen: int = 100) -> None:
        self._items: deque[dict[str, Any]] = deque(maxlen=maxlen)

    def record_payload(self, topic_id: str, source_view: str, payload: Mapping[str, Any]) -> None:
        diagnostics = payload.get("diagnostics")
        if isinstance(diagnostics, list):
            for diagnostic in diagnostics:
                if isinstance(diagnostic, Mapping):
                    self.record(topic_id, source_view, diagnostic)
        error = payload.get("error")
        if isinstance(error, Mapping):
            self.record(
                topic_id,
                source_view,
                {
                    "severity": "error",
                    "code": error.get("code"),
                    "message": error.get("message"),
                },
            )

    def record(self, topic_id: str, source_view: str, diagnostic: Mapping[str, Any]) -> None:
        severity = str(diagnostic.get("severity") or "info")
        if severity not in {"warning", "error"}:
            return
        self._items.append(
            {
                "occurred_at": datetime.now(UTC).isoformat(),
                "topic_id": topic_id,
                "source_view": source_view,
                "severity": severity,
                "code": diagnostic.get("code"),
                "message": diagnostic.get("message"),
                "idea_id": diagnostic.get("idea_id"),
                "record_id": diagnostic.get("record_id"),
                "details": {key: value for key, value in diagnostic.items() if key not in {"severity", "code", "message", "idea_id", "record_id"}},
            }
        )

    def query(self, *, topic_id: str | None = None, limit: int = 50) -> list[dict[str, Any]]:
        selected = [item for item in reversed(self._items) if topic_id is None or item.get("topic_id") == topic_id]
        return selected[:limit]
