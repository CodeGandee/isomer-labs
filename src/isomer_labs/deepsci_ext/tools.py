"""DeepScientist compatibility tool registry and mock service."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import re
import sys
from typing import Any, Mapping
import uuid

from isomer_labs.core.diagnostics import Diagnostic
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.runtime.records import utc_timestamp
from isomer_labs.runtime.store import open_workspace_runtime
from isomer_labs.deepsci_ext.store import DeepSciCompatStore, StoredBashSession, StoredMemoryCard

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

MEMORY_KINDS = ("papers", "ideas", "decisions", "episodes", "knowledge", "templates")
BASH_MODES = ("detach", "await", "create", "read", "kill", "list", "history")


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


def dumps_raw_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True)


def load_input_json(value: str | None) -> dict[str, Any]:
    raw = ""
    if value == "-":
        raw = sys.stdin.read()
    elif value is not None:
        raw = value
    elif not sys.stdin.isatty():
        raw = sys.stdin.read()
    if not raw.strip():
        return {}
    loaded = json.loads(raw)
    if not isinstance(loaded, dict):
        raise ValueError("DeepScientist compatibility input JSON must be an object.")
    return loaded


def unsupported_tool_payload(tool_name: str) -> dict[str, Any]:
    return {
        "ok": False,
        "tool_name": tool_name,
        "error": {
            "code": "unsupported_tool",
            "message": f"Unsupported DeepScientist compatibility tool: {tool_name}",
            "tool_name": tool_name,
        },
    }


class DeepSciCompatError(Exception):
    """Deterministic compatibility-layer error."""

    def __init__(self, message: str, *, code: str = "deepsci_compat_error", payload: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.payload = payload or {}

    def to_payload(self, *, tool_name: str | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "ok": False,
            "error": {
                "code": self.code,
                "message": self.message,
            },
        }
        if tool_name is not None:
            payload["tool_name"] = tool_name
            payload["error"]["tool_name"] = tool_name
        payload.update(self.payload)
        return payload


def call_tool(
    context: EffectiveTopicContext,
    tool_name: str,
    arguments: dict[str, Any],
    *,
    env: Mapping[str, str],
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """Call a supported DeepScientist compatibility mock."""

    tool_parts = split_tool_name(tool_name)
    if tool_parts is None:
        raise DeepSciCompatError(
            f"Unsupported DeepScientist compatibility tool: {tool_name}",
            code="unsupported_tool",
        )
    runtime_store, diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    if runtime_store is None:
        return {
            "ok": False,
            "tool_name": tool_name,
            "error": {
                "code": "workspace_runtime_missing",
                "message": "Workspace Runtime must be initialized before DeepScientist compatibility calls can store state.",
            },
            "diagnostics": [diagnostic.to_json() for diagnostic in diagnostics],
        }, diagnostics
    store = DeepSciCompatStore(runtime_store)
    try:
        with store.connection:
            store.ensure_schema()
        namespace, name = tool_parts
        service = DeepSciCompatService(context, store)
        if namespace == "memory":
            return service.call_memory(name, arguments), diagnostics
        if namespace == "artifact":
            return service.call_artifact(name, arguments), diagnostics
        if namespace == "bash_exec":
            return service.call_bash_exec(name, arguments), diagnostics
        raise DeepSciCompatError(f"Unsupported DeepScientist compatibility namespace: {namespace}", code="unsupported_namespace")
    finally:
        store.close()


class DeepSciCompatService:
    """Tool-family mocks that preserve DeepScientist-visible shapes."""

    def __init__(self, context: EffectiveTopicContext, store: DeepSciCompatStore) -> None:
        self.context = context
        self.store = store

    def call_memory(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name not in MEMORY_TOOLS:
            raise DeepSciCompatError(f"Unsupported memory tool: {name}", code="unsupported_tool")
        if name == "write":
            return self.memory_write(arguments)
        if name == "read":
            return self.memory_read(arguments)
        if name == "search":
            return self.memory_search(arguments)
        if name == "list_recent":
            return self.memory_list_recent(arguments)
        if name == "promote_to_global":
            return self.memory_promote_to_global(arguments)
        raise DeepSciCompatError(f"Unsupported memory tool: {name}", code="unsupported_tool")

    def memory_write(self, arguments: dict[str, Any]) -> dict[str, Any]:
        kind = str(arguments.get("kind") or "knowledge").strip()
        if kind not in MEMORY_KINDS:
            raise DeepSciCompatError(f"Unknown memory kind: {kind}", code="invalid_memory_kind")
        title = str(arguments.get("title") or "Untitled").strip() or "Untitled"
        scope = _normalize_scope(arguments.get("scope"), allow_both=False)
        raw_metadata = arguments.get("metadata")
        metadata = dict(raw_metadata) if isinstance(raw_metadata, dict) else {}
        body = str(arguments.get("markdown") if arguments.get("markdown") is not None else arguments.get("body") or "")
        tags = normalize_tags(arguments.get("tags"))
        now = utc_timestamp()
        card_id = str(metadata.get("id") or f"{kind[:-1] if kind.endswith('s') else kind}-{uuid.uuid4().hex[:12]}")
        metadata.update(
            {
                "id": card_id,
                "type": kind,
                "kind": kind[:-1] if kind.endswith("s") else kind,
                "title": title,
                "quest_id": self.context.topic_workspace_id if scope == "quest" else None,
                "tags": tags,
                "scope": scope,
                "updated_at": now,
            }
        )
        metadata.setdefault("created_at", now)
        path_slug = slugify(title) or card_id
        path = f"sqlite://deepsci_compat_memory_cards/{scope}/{kind}/{path_slug}-{card_id}.md"
        document_id = f"memory::{kind}/{path_slug}-{card_id}.md"
        card = self.store.insert_memory_card(
            self.context,
            card_id=card_id,
            scope=scope,
            kind=kind,
            title=title,
            body=body,
            path=path,
            document_id=document_id,
            metadata=metadata,
            tags=tags,
            created_at=str(metadata.get("created_at") or now),
            updated_at=now,
            writable=scope == "quest",
            shared=scope == "global",
            source_quest_id=self.context.topic_workspace_id if scope == "quest" else None,
        )
        return card_payload(card)

    def memory_read(self, arguments: dict[str, Any]) -> dict[str, Any]:
        card_id = _optional_string(arguments.get("card_id"))
        path = _optional_string(arguments.get("path"))
        card = self.store.get_memory_card(card_id=card_id, path=path)
        if card is None:
            return {
                "ok": False,
                "error": "Memory card not found",
                "card_id": card_id,
                "path": path,
            }
        return card_payload(card)

    def memory_search(self, arguments: dict[str, Any]) -> dict[str, Any]:
        query = str(arguments.get("query") or "")
        scope = _normalize_scope(arguments.get("scope"), allow_both=True)
        kind = _optional_string(arguments.get("kind"))
        limit = _positive_limit(arguments.get("limit"), default=10, maximum=500)
        cards = self.store.list_memory_cards(self.context, scopes=_scopes_for_search(scope), kind=kind)
        query_lower = query.lower()
        matches = [
            card
            for card in cards
            if not query_lower
            or query_lower in card.title.lower()
            or query_lower in card.body.lower()
            or query_lower in str(card.metadata).lower()
        ][:limit]
        return {
            "ok": True,
            "count": len(matches),
            "items": [card_item_payload(card) for card in matches],
        }

    def memory_list_recent(self, arguments: dict[str, Any]) -> dict[str, Any]:
        scope = _normalize_scope(arguments.get("scope"), allow_both=True)
        kind = _optional_string(arguments.get("kind"))
        limit = _positive_limit(arguments.get("limit"), default=10, maximum=500)
        cards = self.store.list_memory_cards(self.context, scopes=_scopes_for_search(scope), kind=kind)
        selected = cards[:limit]
        return {
            "ok": True,
            "count": len(selected),
            "items": [card_item_payload(card) for card in selected],
        }

    def memory_promote_to_global(self, arguments: dict[str, Any]) -> dict[str, Any]:
        card_id = _optional_string(arguments.get("card_id"))
        path = _optional_string(arguments.get("path"))
        card = self.store.get_memory_card(card_id=card_id, path=path)
        if card is None:
            return {
                "ok": False,
                "error": "Memory card not found",
                "card_id": card_id,
                "path": path,
            }
        now = utc_timestamp()
        metadata = dict(card.metadata)
        metadata["scope"] = "global"
        metadata["updated_at"] = now
        metadata["promoted_from"] = {"scope": card.scope, "path": card.path}
        promoted = self.store.update_memory_scope(card_id=card.id, scope="global", metadata=metadata, updated_at=now)
        if promoted is None:
            raise DeepSciCompatError("Memory promotion failed.", code="memory_promotion_failed")
        return card_payload(promoted)

    def call_artifact(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name not in ARTIFACT_TOOLS:
            raise DeepSciCompatError(f"Unsupported artifact tool: {name}", code="unsupported_tool")
        if name == "get_quest_state":
            response = self.artifact_get_quest_state(arguments)
        elif name == "read_quest_documents":
            response = self.artifact_read_quest_documents(arguments)
        elif name == "record":
            response = self.artifact_record(arguments)
        else:
            response = self.artifact_generic(name, arguments)
        call_id = f"artifact-call-{uuid.uuid4().hex[:12]}"
        self.store.record_artifact_call(
            self.context,
            call_id=call_id,
            tool_name=f"artifact.{name}",
            request=dict(arguments),
            response=response,
            mocked=True,
        )
        return response

    def artifact_get_quest_state(self, arguments: dict[str, Any]) -> dict[str, Any]:
        detail = str(arguments.get("detail") or "summary").strip().lower() or "summary"
        if detail not in {"summary", "full"}:
            raise DeepSciCompatError("get_quest_state detail must be `summary` or `full`.", code="invalid_detail")
        state: dict[str, Any] = {
            "quest_id": self.context.topic_workspace_id,
            "title": (
                self.context.research_topic_config.topic_statement
                if self.context.research_topic_config is not None
                else None
            )
            or self.context.research_topic.id,
            "active_anchor": "mock",
            "continuation_policy": "manual",
            "continuation_anchor": None,
            "continuation_reason": None,
            "baseline_gate": None,
            "active_baseline_id": None,
            "active_baseline_variant_id": None,
            "active_run_id": self.context.lifecycle_refs.get("run_id"),
            "active_idea_id": None,
            "active_analysis_campaign_id": None,
            "active_idea_line_ref": None,
            "active_paper_line_ref": None,
            "current_workspace_branch": None,
            "current_workspace_root": str(self.context.topic_workspace_path),
            "research_head_branch": None,
            "research_head_worktree_root": None,
            "workspace_mode": "isomer-topic-workspace",
            "runtime_status": "mocked",
            "display_status": "mocked",
            "waiting_interaction_id": None,
            "pending_user_message_count": 0,
            "next_pending_slice_id": None,
            "paper_contract_health": None,
        }
        if detail == "full":
            state.update(
                {
                    "startup_contract": None,
                    "requested_baseline_ref": None,
                    "confirmed_baseline_ref": None,
                    "counts": {},
                    "paths": {"topic_workspace": str(self.context.topic_workspace_path)},
                    "active_interactions": [],
                    "recent_reply_threads": [],
                    "recent_artifacts": [],
                    "recent_runs": [],
                    "idea_lines": [],
                    "paper_lines": [],
                }
            )
        return {
            "ok": True,
            "mocked": True,
            "detail": detail,
            "quest_state": state,
        }

    def artifact_read_quest_documents(self, arguments: dict[str, Any]) -> dict[str, Any]:
        mode = str(arguments.get("mode") or "excerpt").strip().lower() or "excerpt"
        if mode not in {"excerpt", "full"}:
            raise DeepSciCompatError("read_quest_documents mode must be `excerpt` or `full`.", code="invalid_mode")
        max_lines = _positive_limit(arguments.get("max_lines"), default=12, maximum=500)
        raw_names = arguments.get("names")
        names = [str(item).strip().lower() for item in raw_names if str(item).strip()] if isinstance(raw_names, list) else []
        if not names:
            names = ["brief", "plan", "status", "summary", "active_user_requirements"]
        document_paths = {
            "brief": self.context.topic_workspace_path / "brief.md",
            "plan": self.context.topic_workspace_path / "plan.md",
            "status": self.context.topic_workspace_path / "status.md",
            "summary": self.context.topic_workspace_path / "SUMMARY.md",
            "active_user_requirements": self.context.topic_workspace_path / "active_user_requirements.md",
        }
        items: list[dict[str, Any]] = []
        for name in names:
            path = document_paths.get(name)
            if path is None:
                continue
            content = _read_document_content(path, mode=mode, max_lines=max_lines)
            items.append(
                {
                    "name": name,
                    "path": str(path),
                    "exists": path.exists(),
                    "content": content,
                }
            )
        return {
            "ok": True,
            "mocked": True,
            "mode": mode,
            "count": len(items),
            "items": items,
        }

    def artifact_record(self, arguments: dict[str, Any]) -> dict[str, Any]:
        payload = arguments.get("payload")
        record_payload = dict(payload) if isinstance(payload, dict) else {}
        artifact_id = str(record_payload.get("artifact_id") or f"compat-artifact-{uuid.uuid4().hex[:12]}")
        artifact_kind = _optional_string(record_payload.get("kind"))
        self.store.record_artifact_record(
            self.context,
            artifact_id=artifact_id,
            artifact_kind=artifact_kind,
            payload=record_payload,
        )
        return {
            "ok": True,
            "mocked": True,
            "status": "mocked",
            "artifact_id": artifact_id,
            "recorded": artifact_kind,
            "record": record_payload,
            "workspace_root": str(self.context.topic_workspace_path),
            "artifact_path": None,
            "checkpoint": None,
            "baseline_registry_entry": None,
            "suppressed": False,
        }

    def artifact_generic(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        return {
            "ok": True,
            "mocked": True,
            "tool_name": name,
            "status": "mocked",
            "request": dict(arguments),
            "message": "Isomer DeepScientist compatibility mock recorded the call without executing external behavior.",
        }

    def call_bash_exec(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name != "bash_exec":
            raise DeepSciCompatError(f"Unsupported bash_exec tool: {name}", code="unsupported_tool")
        mode = str(arguments.get("mode") or "detach").strip().lower() or "detach"
        if mode == "create":
            mode = "await"
        if mode not in BASH_MODES:
            raise DeepSciCompatError("Mode must be one of `detach`, `await`, `create`, `read`, `kill`, `list`, or `history`.", code="invalid_bash_mode")
        if mode in {"list", "history"}:
            return self.bash_list_or_history(mode, arguments)
        if mode == "read":
            return self.bash_read(arguments)
        if mode == "kill":
            return self.bash_kill(arguments)
        command = _normalize_command(arguments.get("command"))
        bash_id = _optional_string(arguments.get("id"))
        if mode == "await" and not command and bash_id:
            session = self._resolve_bash_session(bash_id)
            completed = self._complete_session(session)
            return bash_session_payload(completed)
        if not command:
            raise DeepSciCompatError("command is required for `detach` and `await`.", code="missing_command")
        status = "running" if mode == "detach" else "completed"
        session = self._create_session(arguments, command=command, status=status)
        return bash_session_payload(session)

    def bash_list_or_history(self, mode: str, arguments: dict[str, Any]) -> dict[str, Any]:
        limit = _positive_limit(arguments.get("limit"), default=20, maximum=500)
        status = _optional_string(arguments.get("status"))
        kind = _optional_string(arguments.get("kind"))
        items = [bash_session_payload(item) for item in self.store.list_bash_sessions(self.context, status=status, kind=kind, limit=limit)]
        history_lines = [format_history_line(item) for item in items]
        if mode == "history":
            return {
                "ok": True,
                "mocked": True,
                "count": len(items),
                "lines": history_lines,
                "items": items,
            }
        counts = dict(Counter(str(item.get("status") or "unknown") for item in items))
        return {
            "ok": True,
            "mocked": True,
            "count": len(items),
            "items": items,
            "status_counts": counts,
            "summary": {"count": len(items), "status_counts": counts},
            "history_lines": history_lines,
        }

    def bash_read(self, arguments: dict[str, Any]) -> dict[str, Any]:
        session = self._resolve_bash_session(_optional_string(arguments.get("id")))
        payload = bash_session_payload(session)
        payload.update(self._bash_log_window(session, arguments))
        return payload

    def bash_kill(self, arguments: dict[str, Any]) -> dict[str, Any]:
        session = self._resolve_bash_session(_optional_string(arguments.get("id")))
        stopped = self.store.mark_bash_session_stopped(
            bash_id=session.bash_id,
            reason=_optional_string(arguments.get("reason")),
        )
        if stopped is None:
            raise DeepSciCompatError("Bash session not found.", code="bash_session_not_found")
        return bash_session_payload(stopped)

    def _create_session(self, arguments: dict[str, Any], *, command: str, status: str) -> StoredBashSession:
        now = utc_timestamp()
        bash_id = _optional_string(arguments.get("id")) or f"bash-{uuid.uuid4().hex[:12]}"
        cwd = str(self.context.topic_workspace_path)
        workdir = _optional_string(arguments.get("workdir"))
        log_path = f"sqlite://deepsci_compat_bash_log_entries/{bash_id}"
        finished_at = now if status == "completed" else None
        exit_code = 0 if status == "completed" else None
        metadata: dict[str, Any] = {
            "mocked": True,
            "env": arguments.get("env") if isinstance(arguments.get("env"), dict) else {},
            "timeout_seconds": arguments.get("timeout_seconds"),
            "wait_timeout_seconds": arguments.get("wait_timeout_seconds"),
        }
        session = StoredBashSession(
            bash_id=bash_id,
            command=command,
            status=status,
            kind=_optional_string(arguments.get("kind")),
            comment=arguments.get("comment"),
            label=_optional_string(arguments.get("label")) or None,
            workdir=workdir,
            cwd=cwd,
            log_path=log_path,
            started_at=now,
            finished_at=finished_at,
            exit_code=exit_code,
            stop_reason=None,
            last_progress=None,
            last_progress_at=None,
            last_output_at=now,
            last_output_seq=1,
            metadata=metadata,
        )
        stored = self.store.upsert_bash_session(self.context, session=session)
        self.store.add_bash_log_entry(
            bash_id=stored.bash_id,
            text=f"[isomer mock] Command was not executed: {command}",
            created_at=now,
        )
        return stored

    def _complete_session(self, session: StoredBashSession) -> StoredBashSession:
        completed = StoredBashSession(
            **{
                **session.__dict__,
                "status": "completed",
                "finished_at": utc_timestamp(),
                "exit_code": 0,
            }
        )
        return self.store.upsert_bash_session(self.context, session=completed)

    def _resolve_bash_session(self, bash_id: str | None) -> StoredBashSession:
        session = self.store.get_bash_session(bash_id) if bash_id else self.store.latest_bash_session()
        if session is None:
            raise DeepSciCompatError("Bash session not found.", code="bash_session_not_found")
        return session

    def _bash_log_window(self, session: StoredBashSession, arguments: dict[str, Any]) -> dict[str, Any]:
        tail = arguments.get("tail") if arguments.get("tail") is not None else arguments.get("tail_limit")
        line_limit = _positive_limit(tail, default=200, maximum=1000)
        entries = self.store.bash_log_entries(bash_id=session.bash_id, order="asc")
        lines = [str(row["text"]) for row in entries]
        start_value = arguments.get("start")
        if start_value is not None:
            try:
                start = max(0, int(start_value))
            except (TypeError, ValueError):
                start = 0
            window = lines[start : start + line_limit]
            window_start = start
        elif tail is not None:
            window = lines[-line_limit:]
            window_start = max(0, len(lines) - len(window))
        else:
            window = lines[:]
            window_start = 0
        return {
            "log": "\n".join(window),
            "log_lines": window,
            "log_line_count": len(lines),
            "log_windowed": len(window) != len(lines) or window_start != 0,
            "line_limit": line_limit,
            "log_window_start": window_start,
            "log_window_end": window_start + len(window),
            "tail": [
                {
                    "seq": int(row["sequence"]),
                    "stream": str(row["stream"]),
                    "text": str(row["text"]),
                    "created_at": str(row["created_at"]),
                }
                for row in entries[-line_limit:]
            ],
            "latest_seq": int(entries[-1]["sequence"]) if entries else 0,
        }


def card_payload(card: StoredMemoryCard) -> dict[str, Any]:
    return {
        "id": card.id,
        "title": card.title,
        "type": card.kind,
        "scope": card.scope,
        "path": card.path,
        "metadata": card.metadata,
        "body": card.body,
        "updated_at": card.updated_at,
        "excerpt": excerpt(card.body),
    }


def card_item_payload(card: StoredMemoryCard) -> dict[str, Any]:
    item = {
        "id": card.id,
        "title": card.title,
        "type": card.kind,
        "path": card.path,
        "document_id": card.document_id,
        "excerpt": excerpt(card.body),
        "updated_at": card.updated_at,
        "writable": card.writable,
        "scope": card.scope,
        "shared": card.shared,
    }
    if card.source_quest_id is not None:
        item["source_quest_id"] = card.source_quest_id
    return item


def bash_session_payload(session: StoredBashSession) -> dict[str, Any]:
    return {
        "ok": True,
        "mocked": True,
        "id": session.bash_id,
        "bash_id": session.bash_id,
        "log_path": session.log_path,
        "status": session.status,
        "kind": session.kind,
        "comment": session.comment,
        "label": session.label,
        "command": session.command,
        "workdir": session.workdir,
        "cwd": session.cwd,
        "started_at": session.started_at,
        "finished_at": session.finished_at,
        "exit_code": session.exit_code,
        "stop_reason": session.stop_reason,
        "last_progress": session.last_progress,
        "last_progress_at": session.last_progress_at,
        "last_output_at": session.last_output_at,
        "last_output_seq": session.last_output_seq,
        "run_age_seconds": 0,
        "status_age_seconds": 0,
        "silent_seconds": 0,
        "progress_age_seconds": None,
        "latest_signal_at": None,
        "signal_age_seconds": None,
        "watchdog_after_seconds": None,
        "watchdog_overdue": False,
    }


def format_history_line(item: dict[str, Any]) -> str:
    return f"{item.get('bash_id')} {item.get('status')} {item.get('command')}"


def normalize_tags(value: object) -> list[str]:
    if value is None:
        return []
    raw_items: list[object]
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return []
        raw_items = [part.strip() for part in stripped.split(",")]
    elif isinstance(value, list):
        raw_items = list(value)
    else:
        raw_items = [value]
    tags: list[str] = []
    seen: set[str] = set()
    for item in raw_items:
        text = str(item or "").strip()
        if not text or text in seen:
            continue
        seen.add(text)
        tags.append(text)
    return tags


def excerpt(text: str) -> str:
    stripped = str(text or "").strip()
    if not stripped:
        return ""
    return stripped.splitlines()[0]


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return normalized[:80]


def _normalize_scope(value: object, *, allow_both: bool) -> str:
    normalized = str(value or "quest").strip().lower() or "quest"
    allowed = {"quest", "global", "both"} if allow_both else {"quest", "global"}
    if normalized not in allowed:
        allowed_text = ", ".join(f"`{item}`" for item in sorted(allowed))
        raise DeepSciCompatError(f"Scope must be one of {allowed_text}.", code="invalid_scope")
    return normalized


def _scopes_for_search(scope: str) -> tuple[str, ...]:
    return ("quest", "global") if scope == "both" else (scope,)


def _optional_string(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _positive_limit(value: object, *, default: int, maximum: int) -> int:
    try:
        return max(1, min(int(str(value)), maximum))
    except (TypeError, ValueError):
        return default


def _normalize_command(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return " ".join(str(item) for item in value)
    return str(value)


def _read_document_content(path: Path, *, mode: str, max_lines: int) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8").strip()
    if mode == "full":
        return text or None
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    content = "\n".join(lines[:max_lines]).strip()
    return content or None
