"""Read-model helpers for the local Isomer Project web API."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
import os
from pathlib import Path
from typing import Any, Mapping

from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.models import EffectiveTopicContext, Project, ProjectState, SelectionRequest
from isomer_labs.project import discover_project
from isomer_labs.project.context import resolve_effective_topic_context
from isomer_labs.project.validation import build_project_state
from isomer_labs.records.index import (
    cleanup_query_index,
    query_index_export,
    query_index_facets,
    query_index_files,
    query_index_lineage,
    query_index_list,
    query_index_siblings,
    rebuild_query_index,
    validate_query_index,
)
from isomer_labs.records.store import ResearchRecordError, render_record, show_record
from isomer_labs.runtime.store import open_workspace_runtime
from isomer_labs.runtime.validation import inspect_workspace_runtime
from isomer_labs.workspace.actors import list_topic_actors
from isomer_labs.workspace.manifest import resolve_semantic_binding

from .contracts import (
    IdeaDetailResponseContract,
    RecordFilesResponseContract,
    RecordDetailResponseContract,
    RecordRenderResponseContract,
    RecordViewerDescriptorContract,
    TopicGraphResponseContract,
    TopicOverviewResponseContract,
    ensure_gui_payload,
)
from .graph import build_topic_graph_view
from .idea_detail import idea_detail_payload
from .project_explorer import openable_item_descriptor_payload, project_explorer_payload
from .recent_errors import RecentErrorBuffer

TOPIC_OVERVIEW_LABEL = "topic.intent.overview"
TOPIC_OVERVIEW_MAX_BYTES = 512 * 1024


def diagnostics_json(diagnostics: list[Diagnostic]) -> list[dict[str, object]]:
    return [diagnostic.to_json() for diagnostic in diagnostics]


def merge_diagnostics(payload: dict[str, Any], diagnostics: list[Diagnostic]) -> dict[str, Any]:
    existing = payload.get("diagnostics")
    merged: list[object] = []
    if isinstance(existing, list):
        merged.extend(existing)
    merged.extend(diagnostics_json(diagnostics))
    return {**payload, "diagnostics": merged}


@dataclass(frozen=True)
class ProjectWebReadModel:
    """Project-scoped read model used by FastAPI routes."""

    project_root: Path
    env: Mapping[str, str] | None = None
    _recent_errors: RecentErrorBuffer = field(default_factory=RecentErrorBuffer, init=False, repr=False, compare=False)

    @property
    def selected_env(self) -> Mapping[str, str]:
        return self.env if self.env is not None else os.environ

    def project_state(self) -> tuple[Project | None, ProjectState | None, list[Diagnostic]]:
        project, diagnostics = discover_project(
            cwd=self.project_root,
            env=self.selected_env,
            project_selector=str(self.project_root),
        )
        state = None
        if project is not None:
            state = build_project_state(project)
            diagnostics.extend(state.diagnostics)
        return project, state, diagnostics

    def topic_context(self, topic_id: str) -> tuple[EffectiveTopicContext | None, list[Diagnostic]]:
        project, state, diagnostics = self.project_state()
        if project is None or state is None:
            return None, diagnostics
        context, context_diagnostics = resolve_effective_topic_context(
            state,
            SelectionRequest(research_topic_id=topic_id),
            cwd=project.root,
            env=self.selected_env,
        )
        diagnostics.extend(context_diagnostics)
        return context, diagnostics

    def project_summary(self) -> dict[str, Any]:
        project, state, diagnostics = self.project_state()
        return {
            "ok": project is not None and not has_errors(diagnostics),
            "mutated": False,
            "project": project.to_json() if project is not None else None,
            "manifest": project.manifest.to_json() if project is not None else None,
            "topic_config_count": len(state.topic_configs) if state is not None else 0,
            "diagnostics": diagnostics_json(diagnostics),
        }

    def topics(self) -> dict[str, Any]:
        project, state, diagnostics = self.project_state()
        topics: list[dict[str, object]] = []
        if project is not None and state is not None:
            for topic in project.manifest.research_topics:
                topic_payload = topic.to_json()
                context, context_diagnostics = resolve_effective_topic_context(
                    state,
                    SelectionRequest(research_topic_id=topic.id),
                    cwd=project.root,
                    env=self.selected_env,
                )
                diagnostics.extend(context_diagnostics)
                if context is not None:
                    topic_payload["topic_workspace_path"] = str(context.topic_workspace_path)
                    topic_payload["topic_statement"] = (
                        context.research_topic_config.topic_statement
                        if context.research_topic_config is not None
                        else None
                    )
                topics.append(topic_payload)
        return {
            "ok": project is not None and not has_errors(diagnostics),
            "mutated": False,
            "topics": topics,
            "diagnostics": diagnostics_json(diagnostics),
        }

    def topic(self, topic_id: str) -> dict[str, Any]:
        context, diagnostics = self.topic_context(topic_id)
        payload: dict[str, Any] = {
            "ok": context is not None and not has_errors(diagnostics),
            "mutated": False,
            "context": context.to_json() if context is not None else None,
            "topic": context.research_topic.to_json() if context is not None else None,
            "topic_config": (
                context.research_topic_config.to_json()
                if context is not None and context.research_topic_config is not None
                else None
            ),
            "diagnostics": diagnostics_json(diagnostics),
        }
        if context is None:
            payload["topic_actors"] = []
            payload["topic_workspace_manifest"] = None
            return payload
        actors_payload, actor_diagnostics = list_topic_actors(context)
        diagnostics.extend(actor_diagnostics)
        payload["topic_actors"] = actors_payload.get("topic_actors", [])
        payload["topic_workspace_manifest"] = actors_payload.get("manifest")
        payload["ok"] = not has_errors(diagnostics)
        payload["diagnostics"] = diagnostics_json(diagnostics)
        return payload

    def runtime(self, topic_id: str) -> dict[str, Any]:
        context, diagnostics = self.topic_context(topic_id)
        inspection = None
        if context is not None:
            inspection, runtime_diagnostics = inspect_workspace_runtime(context, env=self.selected_env)
            diagnostics.extend(runtime_diagnostics)
        return {
            "ok": context is not None and not has_errors(diagnostics),
            "mutated": False,
            "runtime": inspection.to_json() if inspection is not None else None,
            "diagnostics": diagnostics_json(diagnostics),
        }

    def topic_overview(self, topic_id: str) -> dict[str, Any]:
        context, diagnostics = self.topic_context(topic_id)
        if context is None:
            return ensure_gui_payload({
                "ok": False,
                "mutated": False,
                "topic_id": topic_id,
                "topic_workspace_id": None,
                "overview": {
                    "semantic_label": TOPIC_OVERVIEW_LABEL,
                    "exists": False,
                    "content_markdown": None,
                },
                "topic_payload": None,
                "runtime_payload": None,
                "diagnostics": diagnostics_json(diagnostics),
            }, TopicOverviewResponseContract, contract_name="topic-overview")

        overview_result, overview_diagnostics = resolve_semantic_binding(
            context,
            TOPIC_OVERVIEW_LABEL,
            env=self.selected_env,
        )
        diagnostics.extend(overview_diagnostics)
        overview_payload: dict[str, Any] = {
            "semantic_label": TOPIC_OVERVIEW_LABEL,
            "exists": False,
            "content_markdown": None,
            "content_cap_bytes": TOPIC_OVERVIEW_MAX_BYTES,
        }
        if overview_result is not None:
            overview_payload.update(overview_result.to_json())
            overview_payload["content_markdown"] = None
            overview_payload["content_cap_bytes"] = TOPIC_OVERVIEW_MAX_BYTES
            overview_diagnostic = self._read_topic_overview_markdown(overview_result.path, overview_payload)
            if overview_diagnostic is not None:
                diagnostics.append(overview_diagnostic)

        topic_payload = self.topic(topic_id)
        runtime_payload = self.runtime(topic_id)
        merged_diagnostics = diagnostics_json(diagnostics)
        for payload in (topic_payload, runtime_payload):
            payload_diagnostics = payload.get("diagnostics")
            if isinstance(payload_diagnostics, list):
                merged_diagnostics.extend(payload_diagnostics)

        return ensure_gui_payload({
            "ok": not has_errors(diagnostics) and bool(topic_payload.get("ok", True)) and bool(runtime_payload.get("ok", True)),
            "mutated": False,
            "topic_id": context.research_topic.id,
            "topic_workspace_id": context.topic_workspace_id,
            "overview": overview_payload,
            "topic_payload": topic_payload,
            "runtime_payload": runtime_payload,
            "diagnostics": merged_diagnostics,
        }, TopicOverviewResponseContract, contract_name="topic-overview")

    def project_explorer(self, *, expanded_topic_ids: tuple[str, ...] = ()) -> dict[str, Any]:
        return project_explorer_payload(self, expanded_topic_ids=expanded_topic_ids)

    def openable_item_descriptor(self, openable_item_id: str) -> dict[str, Any]:
        return openable_item_descriptor_payload(self, openable_item_id)

    def records(
        self,
        topic_id: str,
        *,
        record_kind: str | None = None,
        status: str | None = None,
        profile: str | None = None,
        facet: str | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        return self._with_context(
            topic_id,
            lambda context: query_index_list(
                context,
                env=self.selected_env,
                record_kind=record_kind,
                status=status,
                profile=profile,
                facet=facet,
                limit=limit,
            ),
        )

    def records_export(self, topic_id: str, *, view: str) -> dict[str, Any]:
        return self._with_context(topic_id, lambda context: query_index_export(context, env=self.selected_env, view=view))

    def topic_graph(
        self,
        topic_id: str,
        *,
        graph_scope: str,
        renderer: str = "auto",
        status: str | None = None,
        relation_kind: str | None = None,
        producer: str | None = None,
        time_range: str | None = None,
        search: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
        include_secondary: bool = False,
    ) -> dict[str, Any]:
        payload = self._with_context(
            topic_id,
            lambda context: self._topic_graph_payload(
                context,
                graph_scope=graph_scope,
                renderer=renderer,
                status=status,
                relation_kind=relation_kind,
                producer=producer,
                time_range=time_range,
                search=search,
                limit=limit,
                cursor=cursor,
                include_secondary=include_secondary,
            ),
        )
        self._recent_errors.record_payload(topic_id, f"graph:{graph_scope}", payload)
        return payload

    def recent_errors(self, topic_id: str, *, limit: int = 50) -> dict[str, Any]:
        return {
            "ok": True,
            "mutated": False,
            "topic_id": topic_id,
            "errors": self._recent_errors.query(topic_id=topic_id, limit=limit),
            "diagnostics": [],
        }

    def record_detail(self, topic_id: str, record_id: str, *, include_payload: bool) -> dict[str, Any]:
        return self._with_context(
            topic_id,
            lambda context: self._record_detail_payload(
                context,
                record_id,
                include_payload=include_payload,
            ),
        )

    def idea_detail(self, topic_id: str, idea_id: str, *, include_source_json: bool = False) -> dict[str, Any]:
        return self._with_context(
            topic_id,
            lambda context: _ensure_contract_tuple(
                idea_detail_payload(
                    context,
                    idea_id,
                    env=self.selected_env,
                    include_source_json=include_source_json,
                ),
                IdeaDetailResponseContract,
                "idea-detail",
            ),
        )

    def record_render(self, topic_id: str, record_id: str) -> dict[str, Any]:
        return self._with_context(topic_id, lambda context: self._record_render_payload(context, record_id))

    def record_lineage(self, topic_id: str, record_id: str, *, direction: str) -> dict[str, Any]:
        return self._with_context(
            topic_id,
            lambda context: query_index_lineage(context, record_id, env=self.selected_env, direction=direction),
        )

    def record_siblings(self, topic_id: str, record_id: str) -> dict[str, Any]:
        return self._with_context(topic_id, lambda context: query_index_siblings(context, record_id, env=self.selected_env))

    def record_files(self, topic_id: str, record_id: str) -> dict[str, Any]:
        return self._with_context(topic_id, lambda context: self._record_files_payload(context, record_id))

    def record_facets(self, topic_id: str, record_id: str, *, facet: str | None) -> dict[str, Any]:
        return self._with_context(
            topic_id,
            lambda context: query_index_facets(context, record_id, env=self.selected_env, facet=facet),
        )

    def record_viewer_descriptor(self, topic_id: str, record_id: str) -> dict[str, Any]:
        return self._with_context(
            topic_id,
            lambda context: self._record_viewer_descriptor_payload(context, record_id),
        )

    def record_file_content(self, topic_id: str, record_id: str, file_id: str) -> dict[str, Any]:
        files_payload = self.record_files(topic_id, record_id)
        if not files_payload.get("ok"):
            return {
                **files_payload,
                "path": None,
                "error": files_payload.get("error")
                or {"code": "record_files_unavailable", "message": "Record file metadata is unavailable."},
            }
        files = files_payload.get("files")
        if not isinstance(files, list):
            files = []
        for item in files:
            if not isinstance(item, Mapping) or str(item.get("id")) != file_id:
                continue
            if not item.get("openable"):
                return {
                    "ok": False,
                    "mutated": False,
                    "topic_id": topic_id,
                    "record_id": record_id,
                    "file_id": file_id,
                    "path": None,
                    "media_type": item.get("media_type"),
                    "exists": bool(item.get("exists")),
                    "error": {
                        "code": "file_not_openable",
                        "message": f"File is not openable: {item.get('open_blocked_reason') or 'unknown'}",
                    },
                    "diagnostics": files_payload.get("diagnostics", []),
                }
            resolved_path = item.get("resolved_path")
            if not isinstance(resolved_path, str):
                return {
                    "ok": False,
                    "mutated": False,
                    "topic_id": topic_id,
                    "record_id": record_id,
                    "file_id": file_id,
                    "path": None,
                    "media_type": item.get("media_type"),
                    "exists": False,
                    "error": {"code": "file_path_unresolved", "message": "File path is not resolved."},
                    "diagnostics": files_payload.get("diagnostics", []),
                }
            return {
                "ok": True,
                "mutated": False,
                "topic_id": topic_id,
                "record_id": record_id,
                "file_id": file_id,
                "path": Path(resolved_path),
                "media_type": item.get("media_type"),
                "exists": True,
                "diagnostics": files_payload.get("diagnostics", []),
            }
        return {
            "ok": False,
            "mutated": False,
            "topic_id": topic_id,
            "record_id": record_id,
            "file_id": file_id,
            "path": None,
            "exists": False,
            "error": {"code": "file_not_found", "message": f"Record file is not indexed: {file_id}"},
            "diagnostics": files_payload.get("diagnostics", []),
        }

    def topic_change_event(self, topic_id: str) -> dict[str, Any]:
        return self._with_context(topic_id, lambda context: self._topic_change_event_payload(context))

    def index_validate(self, topic_id: str, *, record_id: str | None = None) -> dict[str, Any]:
        return self._with_context(
            topic_id,
            lambda context: validate_query_index(context, env=self.selected_env, record_id=record_id),
        )

    def index_rebuild(
        self,
        topic_id: str,
        *,
        record_id: str | None = None,
        include_operation_set_files: bool = False,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        return self._with_context(
            topic_id,
            lambda context: rebuild_query_index(
                context,
                env=self.selected_env,
                record_id=record_id,
                include_operation_set_files=include_operation_set_files,
                dry_run=dry_run,
            ),
        )

    def index_cleanup(
        self,
        topic_id: str,
        *,
        stale_derived: bool = False,
        orphaned: bool = False,
        missing_files: bool = False,
        apply_cleanup: bool = False,
    ) -> dict[str, Any]:
        return self._with_context(
            topic_id,
            lambda context: cleanup_query_index(
                context,
                env=self.selected_env,
                stale_derived=stale_derived,
                orphaned=orphaned,
                missing_files=missing_files,
                apply=apply_cleanup,
            ),
        )

    def _with_context(
        self,
        topic_id: str,
        callback: Any,
    ) -> dict[str, Any]:
        context, diagnostics = self.topic_context(topic_id)
        if context is None:
            return {
                "ok": False,
                "mutated": False,
                "diagnostics": diagnostics_json(diagnostics),
            }
        try:
            payload, call_diagnostics = callback(context)
        except ResearchRecordError as exc:
            return merge_diagnostics(exc.to_payload(), diagnostics)
        diagnostics.extend(call_diagnostics)
        return merge_diagnostics(dict(payload), diagnostics)

    def _read_topic_overview_markdown(self, path: Path, overview_payload: dict[str, Any]) -> Diagnostic | None:
        if not path.exists():
            overview_payload["exists"] = False
            return Diagnostic(
                code="topic_overview_missing",
                severity="warning",
                concept="Topic Overview",
                path=path,
                field=TOPIC_OVERVIEW_LABEL,
                message="Topic overview Markdown is missing.",
                hint=f"Create the `{TOPIC_OVERVIEW_LABEL}` file before expecting the overview tab to show Markdown.",
            )
        try:
            size = path.stat().st_size
            overview_payload["exists"] = True
            overview_payload["content_bytes"] = size
            if size > TOPIC_OVERVIEW_MAX_BYTES:
                return Diagnostic(
                    code="topic_overview_unreadable",
                    severity="warning",
                    concept="Topic Overview",
                    path=path,
                    field=TOPIC_OVERVIEW_LABEL,
                    message=f"Topic overview Markdown is larger than the {TOPIC_OVERVIEW_MAX_BYTES} byte read-model limit.",
                    hint="Shorten the topic overview or inspect it outside the GUI.",
                )
            overview_payload["content_markdown"] = path.read_text(encoding="utf-8")
            return None
        except (OSError, UnicodeError) as exc:
            overview_payload["content_markdown"] = None
            return Diagnostic(
                code="topic_overview_unreadable",
                severity="warning",
                concept="Topic Overview",
                path=path,
                field=TOPIC_OVERVIEW_LABEL,
                message=f"Topic overview Markdown cannot be read: {exc}",
            )

    def _topic_graph_payload(
        self,
        context: EffectiveTopicContext,
        *,
        graph_scope: str,
        renderer: str,
        status: str | None,
        relation_kind: str | None,
        producer: str | None,
        time_range: str | None,
        search: str | None,
        limit: int | None,
        cursor: str | None,
        include_secondary: bool,
    ) -> tuple[dict[str, Any], list[Diagnostic]]:
        export_payload, diagnostics = query_index_export(context, env=self.selected_env, view="graph")
        graph_payload = build_topic_graph_view(
            context,
            export_payload,
            graph_scope=graph_scope,
            renderer=renderer,
            status=status,
            relation_kind=relation_kind,
            producer=producer,
            time_range=time_range,
            search=search,
            limit=limit,
            cursor=cursor,
            include_secondary=include_secondary,
        )
        return ensure_gui_payload(graph_payload, TopicGraphResponseContract, contract_name="topic-graph"), diagnostics

    def _record_files_payload(
        self,
        context: EffectiveTopicContext,
        record_id: str,
    ) -> tuple[dict[str, Any], list[Diagnostic]]:
        payload, diagnostics = query_index_files(context, record_id, env=self.selected_env)
        payload = dict(payload)
        payload["topic_id"] = context.research_topic.id
        return ensure_gui_payload(payload, RecordFilesResponseContract, contract_name="record-files"), diagnostics

    def _record_detail_payload(
        self,
        context: EffectiveTopicContext,
        record_id: str,
        *,
        include_payload: bool,
    ) -> tuple[dict[str, Any], list[Diagnostic]]:
        payload, diagnostics = show_record(
            context,
            record_id,
            env=self.selected_env,
            include_payload=include_payload,
            include_validation_diagnostics=True,
            include_render_diagnostics=True,
        )
        files_payload, files_diagnostics = query_index_files(context, record_id, env=self.selected_env)
        diagnostics.extend(files_diagnostics)
        enriched, metadata_diagnostics = self._enrich_record_inspection_payload(context, record_id, payload, files_payload=files_payload)
        diagnostics.extend(metadata_diagnostics)
        return ensure_gui_payload(enriched, RecordDetailResponseContract, contract_name="record-detail"), diagnostics

    def _record_render_payload(
        self,
        context: EffectiveTopicContext,
        record_id: str,
    ) -> tuple[dict[str, Any], list[Diagnostic]]:
        payload, diagnostics = render_record(context, record_id, env=self.selected_env)
        detail_payload, detail_diagnostics = show_record(
            context,
            record_id,
            env=self.selected_env,
            include_payload=False,
            include_validation_diagnostics=False,
            include_render_diagnostics=False,
        )
        files_payload, files_diagnostics = query_index_files(context, record_id, env=self.selected_env)
        diagnostics.extend([*detail_diagnostics, *files_diagnostics])
        enriched_source = {**detail_payload, "record": payload.get("record") or detail_payload.get("record")}
        enriched_source, metadata_diagnostics = self._enrich_record_inspection_payload(context, record_id, enriched_source, files_payload=files_payload)
        diagnostics.extend(metadata_diagnostics)
        for key in ("topic_workspace_relative_path", "absolute_filepath", "direct_parent_idea", "record_inspection"):
            if key in enriched_source:
                payload[key] = enriched_source[key]
        return ensure_gui_payload(payload, RecordRenderResponseContract, contract_name="record-render"), diagnostics

    def _record_viewer_descriptor_payload(
        self,
        context: EffectiveTopicContext,
        record_id: str,
    ) -> tuple[dict[str, Any], list[Diagnostic]]:
        try:
            detail_payload, detail_diagnostics = show_record(
                context,
                record_id,
                env=self.selected_env,
                include_payload=False,
                include_validation_diagnostics=True,
                include_render_diagnostics=True,
            )
        except ResearchRecordError as exc:
            payload = exc.to_payload()
            payload.update(
                {
                    "mutated": False,
                    "topic_id": context.research_topic.id,
                    "record_id": record_id,
                    "viewer_kind": "unknown",
                    "exists": False,
                    "diagnostics": [],
                }
            )
            return ensure_gui_payload(payload, RecordViewerDescriptorContract, contract_name="record-viewer-descriptor"), []
        files_payload, files_diagnostics = query_index_files(context, record_id, env=self.selected_env)
        record_raw = detail_payload.get("record")
        record: Mapping[str, Any] = record_raw if isinstance(record_raw, Mapping) else {}
        structured_raw = detail_payload.get("structured_payload")
        structured: Mapping[str, Any] = structured_raw if isinstance(structured_raw, Mapping) else {}
        files_raw = files_payload.get("files")
        files: list[object] = list(files_raw) if isinstance(files_raw, list) else []
        viewer_kind, media_type = _viewer_kind(record, structured, files)
        primary_file = _primary_openable_file(files)
        title = _descriptor_title(record, structured, record_id)
        detail_diagnostic_payload = detail_payload.get("diagnostics")
        file_diagnostic_payload = files_payload.get("diagnostics")
        descriptor_diagnostics = [
            *(list(detail_diagnostic_payload) if isinstance(detail_diagnostic_payload, list) else []),
            *(list(file_diagnostic_payload) if isinstance(file_diagnostic_payload, list) else []),
        ]
        enriched_detail, metadata_diagnostics = self._enrich_record_inspection_payload(context, record_id, detail_payload, files_payload=files_payload)
        descriptor_diagnostics.extend(diagnostic.to_json() for diagnostic in metadata_diagnostics)
        record_url = f"/api/topics/{context.research_topic.id}/records/{record_id}"
        render_url = f"{record_url}/render"
        primary_content_url = render_url if viewer_kind == "markdown" else None
        if primary_file is not None:
            primary_content_url = f"{record_url}/files/{primary_file}/content"
        return ensure_gui_payload({
            "ok": bool(detail_payload.get("ok", True)),
            "mutated": False,
            "topic_id": context.research_topic.id,
            "record_id": record_id,
            "title": title,
            "viewer_kind": viewer_kind,
            "topic_workspace_relative_path": enriched_detail.get("topic_workspace_relative_path"),
            "absolute_filepath": enriched_detail.get("absolute_filepath"),
            "direct_parent_idea": enriched_detail.get("direct_parent_idea"),
            "record_inspection": enriched_detail.get("record_inspection"),
            "primary_content_url": primary_content_url,
            "detail_url": record_url,
            "render_url": render_url,
            "files_url": f"{record_url}/files",
            "facets_url": f"{record_url}/facets",
            "media_type": media_type,
            "exists": True,
            "diagnostics": descriptor_diagnostics,
        }, RecordViewerDescriptorContract, contract_name="record-viewer-descriptor"), [*detail_diagnostics, *files_diagnostics]

    def _enrich_record_inspection_payload(
        self,
        context: EffectiveTopicContext,
        record_id: str,
        payload: Mapping[str, Any],
        *,
        files_payload: Mapping[str, Any] | None = None,
    ) -> tuple[dict[str, Any], list[Diagnostic]]:
        enriched = dict(payload)
        record_raw = enriched.get("record")
        record: Mapping[str, Any] = record_raw if isinstance(record_raw, Mapping) else {}
        structured_raw = enriched.get("structured_payload")
        structured: Mapping[str, Any] = structured_raw if isinstance(structured_raw, Mapping) else {}
        files_raw = files_payload.get("files") if files_payload is not None else None
        files = [item for item in files_raw if isinstance(item, Mapping)] if isinstance(files_raw, list) else []
        path_metadata = _record_path_metadata(context, record, structured, files)
        parent_idea, diagnostics = _direct_parent_idea_metadata(context, self.selected_env, record_id)
        inspection = {
            "topic_workspace_relative_path": path_metadata.get("topic_workspace_relative_path"),
            "absolute_filepath": path_metadata.get("absolute_filepath"),
            "path_source": path_metadata.get("path_source"),
            "direct_parent_idea": parent_idea,
        }
        if path_metadata.get("topic_workspace_relative_path") is not None:
            enriched["topic_workspace_relative_path"] = path_metadata["topic_workspace_relative_path"]
        if path_metadata.get("absolute_filepath") is not None:
            enriched["absolute_filepath"] = path_metadata["absolute_filepath"]
        if parent_idea is not None:
            enriched["direct_parent_idea"] = parent_idea
        enriched["record_inspection"] = {key: value for key, value in inspection.items() if value is not None}
        return enriched, diagnostics

    def _topic_change_event_payload(self, context: EffectiveTopicContext) -> tuple[dict[str, Any], list[Diagnostic]]:
        export_payload, diagnostics = query_index_export(context, env=self.selected_env, view="graph")
        export_diagnostic_payload = export_payload.get("diagnostics")
        event_diagnostics = list(export_diagnostic_payload) if isinstance(export_diagnostic_payload, list) else []
        event = {
            "ok": bool(export_payload.get("ok", True)),
            "mutated": False,
            "event_id": f"{context.topic_workspace_id}:{export_payload.get('index_revision') or 'unknown'}",
            "event_type": "topic.index.changed",
            "topic_id": context.research_topic.id,
            "topic_workspace_id": context.topic_workspace_id,
            "index_revision": export_payload.get("index_revision"),
            "changed_record_ids": [],
            "changed_material_kinds": [],
            "graph_scopes": ["idea-lineage", "idea-timeline"],
            "diagnostics_count": len(event_diagnostics),
            "occurred_at": datetime.now(UTC).isoformat(),
            "diagnostics": event_diagnostics,
        }
        return event, diagnostics


def _ensure_contract_tuple(
    result: tuple[dict[str, Any], list[Diagnostic]],
    schema: type[Any],
    contract_name: str,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    payload, diagnostics = result
    return ensure_gui_payload(payload, schema, contract_name=contract_name), diagnostics

def _viewer_kind(record: Mapping[str, Any], structured: Mapping[str, Any], files: list[object]) -> tuple[str, str | None]:
    for item in files:
        if not isinstance(item, Mapping) or not item.get("openable"):
            continue
        if item.get("file_role") in {"structured_payload", "structured_payload_manifest"}:
            continue
        media_type = str(item.get("media_type") or "")
        path = str(item.get("path") or item.get("resolved_path") or "").lower()
        if media_type == "application/pdf" or path.endswith(".pdf"):
            return "pdf", media_type or "application/pdf"
        if media_type.startswith("image/") or path.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
            return "image", media_type or None
        if media_type in {"text/csv", "text/tab-separated-values"} or path.endswith((".csv", ".tsv")):
            return "table", media_type or None
        if media_type == "application/json" or path.endswith(".json"):
            return "json", media_type or "application/json"
    if structured:
        return "markdown", str(structured.get("payload_media_type") or "text/markdown")
    if record.get("content_path"):
        content_path = str(record.get("content_path"))
        if content_path.endswith(".json"):
            return "json", "application/json"
        if content_path.endswith(".pdf"):
            return "pdf", "application/pdf"
        return "markdown", "text/markdown"
    return "unknown", None


def _primary_openable_file(files: list[object]) -> str | None:
    item = _primary_openable_file_item(files)
    file_id = item.get("id") if item is not None else None
    if isinstance(file_id, str) and file_id:
        return file_id
    return None


def _primary_openable_file_item(files: list[object]) -> Mapping[str, Any] | None:
    for item in files:
        if not isinstance(item, Mapping) or not item.get("openable"):
            continue
        if item.get("file_role") in {"structured_payload", "structured_payload_manifest"}:
            continue
        return item
    return None


def _descriptor_title(record: Mapping[str, Any], structured: Mapping[str, Any], record_id: str) -> str:
    for value in (record.get("title"), structured.get("title"), record.get("id")):
        if isinstance(value, str) and value:
            return value
    metadata = record.get("transition_metadata")
    if isinstance(metadata, Mapping):
        for key in ("title", "placeholder", "profile"):
            value = metadata.get(key)
            if isinstance(value, str) and value:
                return value
    return record_id


def _record_path_metadata(
    context: EffectiveTopicContext,
    record: Mapping[str, Any],
    structured: Mapping[str, Any],
    files: list[Mapping[str, Any]],
) -> dict[str, str | None]:
    primary_file = _primary_openable_file_item(list(files))
    candidates: list[tuple[str, object]] = []
    if primary_file is not None:
        candidates.extend(
            [
                ("primary_file", primary_file.get("resolved_path")),
                ("primary_file", primary_file.get("path")),
            ]
        )
    candidates.extend(
        [
            ("structured_payload", structured.get("payload_file_path")),
            ("rendered_markdown", structured.get("rendered_markdown_path")),
            ("record_content", record.get("content_path")),
        ]
    )
    metadata = record.get("transition_metadata")
    if isinstance(metadata, Mapping):
        candidates.extend(
            [
                ("metadata_payload", metadata.get("payload_file_path")),
                ("metadata_rendered_markdown", metadata.get("rendered_markdown_path")),
                ("metadata_content", metadata.get("content_path")),
            ]
        )
    for source, value in candidates:
        if not isinstance(value, str) or not value.strip():
            continue
        path = _resolve_record_path(context, value)
        if path is None:
            continue
        absolute = path.resolve(strict=False)
        relative = _topic_workspace_relative_path(context, absolute)
        return {
            "topic_workspace_relative_path": relative,
            "absolute_filepath": str(absolute),
            "path_source": source,
        }
    return {"topic_workspace_relative_path": None, "absolute_filepath": None, "path_source": None}


def _resolve_record_path(context: EffectiveTopicContext, value: str) -> Path | None:
    path = Path(value)
    if path.is_absolute():
        return path
    topic_candidate = context.topic_workspace_path / path
    if topic_candidate.exists():
        return topic_candidate
    project_candidate = context.project.root / path
    if project_candidate.exists():
        return project_candidate
    if str(path).startswith(str(context.topic_workspace_id)):
        return context.project.root / path
    return topic_candidate


def _topic_workspace_relative_path(context: EffectiveTopicContext, path: Path) -> str | None:
    try:
        return str(path.resolve(strict=False).relative_to(context.topic_workspace_path.resolve(strict=False)))
    except ValueError:
        return None


def _direct_parent_idea_metadata(
    context: EffectiveTopicContext,
    env: Mapping[str, str],
    record_id: str,
) -> tuple[dict[str, object] | None, list[Diagnostic]]:
    store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if store is not None:
        try:
            realizations = store.list_research_idea_realizations(topic_workspace_id=context.topic_workspace_id, record_id=record_id)
            if realizations:
                realization = next((item for item in realizations if item.latest), realizations[0])
                idea = store.get_research_idea(realization.idea_id, topic_workspace_id=context.topic_workspace_id)
                payload: dict[str, object] = {
                    "idea_id": realization.idea_id,
                    "source": "canonical_realization",
                    "realization_id": realization.id,
                }
                if idea is not None:
                    payload.update(
                        {
                            "display_key": idea.display_key,
                            "title": idea.title,
                            "summary": idea.summary,
                            "status": idea.status,
                        }
                    )
                return {key: value for key, value in payload.items() if value is not None}, diagnostics
        finally:
            store.close()
    facets_payload, facet_diagnostics = query_index_facets(context, record_id, env=env, facet="ideas")
    diagnostics.extend(facet_diagnostics)
    ideas = facets_payload.get("ideas")
    if isinstance(ideas, list):
        for item in ideas:
            if not isinstance(item, Mapping):
                continue
            idea_id = item.get("idea_id")
            title = item.get("title")
            if isinstance(idea_id, str) and idea_id:
                return {
                    "idea_id": idea_id,
                    "title": title if isinstance(title, str) else None,
                    "summary": item.get("summary") if isinstance(item.get("summary"), str) else None,
                    "status": item.get("status") if isinstance(item.get("status"), str) else None,
                    "source": "query_index_ideas",
                }, diagnostics
    return None, diagnostics
