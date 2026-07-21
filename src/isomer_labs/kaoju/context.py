"""Compact selected-context reporting for topic-scoped Kaoju services."""

from __future__ import annotations

from isomer_labs.models import EffectiveTopicContext


SELECTED_CONTEXT_SOURCE_FIELDS = (
    "project",
    "research_topic_id",
    "topic_workspace_id",
    "topic_workspace_path",
)


def selected_context_payload(context: EffectiveTopicContext) -> dict[str, object]:
    """Serialize only the Topic and Topic Workspace selection used by a Kaoju call."""

    return {
        "research_topic_id": context.research_topic.id,
        "topic_workspace_id": context.topic_workspace_id,
        "topic_workspace_path": str(context.topic_workspace_path.resolve(strict=False)),
        "sources": {
            field: context.sources[field]
            for field in SELECTED_CONTEXT_SOURCE_FIELDS
            if field in context.sources
        },
    }
