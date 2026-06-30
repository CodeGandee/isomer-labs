"""DeepScientist source-discovered compatibility tool registry."""

from __future__ import annotations

MEMORY_TOOLS = (
    "write",
    "read",
    "search",
    "list_recent",
    "promote_to_global",
)

ARTIFACT_TOOLS = (
    "record",
    "science",
    "checkpoint",
    "git",
    "prepare_branch",
    "activate_branch",
    "submit_idea",
    "list_research_branches",
    "resolve_runtime_refs",
    "get_paper_contract",
    "get_paper_contract_health",
    "validate_manuscript_coverage",
    "validate_academic_outline",
    "validate_manuscript_language",
    "compile_outline_to_writing_plan",
    "get_quest_state",
    "get_global_status",
    "get_research_map_status",
    "get_benchstore_catalog",
    "get_start_setup_context",
    "get_method_scoreboard",
    "get_optimization_frontier",
    "read_quest_documents",
    "get_conversation_context",
    "get_analysis_campaign",
    "record_main_experiment",
    "create_analysis_campaign",
    "submit_paper_outline",
    "list_paper_outlines",
    "submit_paper_bundle",
    "record_analysis_slice",
    "publish_baseline",
    "attach_baseline",
    "confirm_baseline",
    "overwrite_baseline",
    "waive_baseline",
    "arxiv",
    "refresh_summary",
    "render_git_graph",
    "interact",
    "complete_quest",
)

BASH_EXEC_TOOLS = ("bash_exec",)

SUPPORTED_TOOLS = (
    *(f"memory.{name}" for name in MEMORY_TOOLS),
    *(f"artifact.{name}" for name in ARTIFACT_TOOLS),
    *(f"bash_exec.{name}" for name in BASH_EXEC_TOOLS),
)

TOOL_ARGUMENT_KEYS: dict[str, tuple[str, ...]] = {
    "memory.write": (
        "kind",
        "title",
        "body",
        "markdown",
        "scope",
        "tags",
        "metadata",
        "comment",
    ),
    "memory.read": ("card_id", "path", "scope", "comment"),
    "memory.search": ("query", "scope", "limit", "kind", "comment"),
    "memory.list_recent": ("scope", "limit", "kind", "comment"),
    "memory.promote_to_global": ("card_id", "path", "comment"),
    "artifact.get_quest_state": ("detail", "comment"),
    "artifact.read_quest_documents": ("names", "mode", "max_lines", "comment"),
    "artifact.record": ("payload", "comment"),
    "bash_exec.bash_exec": (
        "command",
        "mode",
        "id",
        "reason",
        "workdir",
        "env",
        "export_log",
        "export_log_to",
        "timeout_seconds",
        "wait_timeout_seconds",
        "status",
        "kind",
        "agent_ids",
        "agent_instance_ids",
        "chat_session_id",
        "limit",
        "start",
        "tail",
        "tail_limit",
        "before_seq",
        "after_seq",
        "order",
        "include_log",
        "wait",
        "force",
        "comment",
    ),
}


def split_tool_name(tool_name: str) -> tuple[str, str] | None:
    """Return namespace/tool parts for a recognized compatibility name."""

    normalized = str(tool_name or "").strip()
    if "." not in normalized:
        return None
    namespace, name = normalized.split(".", 1)
    if normalized not in SUPPORTED_TOOLS:
        return None
    return namespace, name


def tool_listing(namespace: str | None = None) -> dict[str, object]:
    """Return the supported tool names in a deterministic source-shaped listing."""

    selected = str(namespace or "").strip() or None
    groups: dict[str, tuple[str, ...]] = {
        "memory": MEMORY_TOOLS,
        "artifact": ARTIFACT_TOOLS,
        "bash_exec": BASH_EXEC_TOOLS,
    }
    if selected is not None:
        return {
            "ok": selected in groups,
            "namespace": selected,
            "tools": list(groups.get(selected, ())),
        }
    return {
        "ok": True,
        "namespaces": {
            name: list(tools)
            for name, tools in groups.items()
        },
        "tools": list(SUPPORTED_TOOLS),
    }
