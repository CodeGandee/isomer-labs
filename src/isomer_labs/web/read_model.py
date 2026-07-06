"""Read-model helpers for the local Isomer Project web API."""

from __future__ import annotations

from dataclasses import dataclass
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
    rebuild_query_index,
    validate_query_index,
)
from isomer_labs.records.store import ResearchRecordError, render_record, show_record
from isomer_labs.runtime.validation import inspect_workspace_runtime
from isomer_labs.workspace.actors import list_topic_actors


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

    def record_detail(self, topic_id: str, record_id: str, *, include_payload: bool) -> dict[str, Any]:
        return self._with_context(
            topic_id,
            lambda context: show_record(
                context,
                record_id,
                env=self.selected_env,
                include_payload=include_payload,
                include_validation_diagnostics=True,
                include_render_diagnostics=True,
            ),
        )

    def record_render(self, topic_id: str, record_id: str) -> dict[str, Any]:
        return self._with_context(topic_id, lambda context: render_record(context, record_id, env=self.selected_env))

    def record_lineage(self, topic_id: str, record_id: str, *, direction: str) -> dict[str, Any]:
        return self._with_context(
            topic_id,
            lambda context: query_index_lineage(context, record_id, env=self.selected_env, direction=direction),
        )

    def record_files(self, topic_id: str, record_id: str) -> dict[str, Any]:
        return self._with_context(topic_id, lambda context: query_index_files(context, record_id, env=self.selected_env))

    def record_facets(self, topic_id: str, record_id: str, *, facet: str | None) -> dict[str, Any]:
        return self._with_context(
            topic_id,
            lambda context: query_index_facets(context, record_id, env=self.selected_env, facet=facet),
        )

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
