"""FastAPI app factory for the local Isomer Project web GUI."""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator, Awaitable, Callable
import re
import time
from pathlib import Path
from typing import Literal, Mapping

from fastapi import Body, FastAPI, Query, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.gzip import GZipMiddleware

from .read_model import ProjectWebReadModel
from .schemas import IndexCleanupRequest, IndexRebuildRequest

WebCacheMode = Literal["normal", "debug"]

NO_CACHE_HEADERS = {
    "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
    "Pragma": "no-cache",
    "Expires": "0",
}

HTML_CACHE_HEADERS = {
    "Cache-Control": "no-cache",
}

API_CACHE_HEADERS = {
    "Cache-Control": "no-cache",
}

IMMUTABLE_ASSET_HEADERS = {
    "Cache-Control": "public, max-age=31536000, immutable",
}

_HASHED_ASSET_RE = re.compile(r"^/assets/.+[-.][A-Za-z0-9_-]{8,}\.[A-Za-z0-9][A-Za-z0-9.]*$")


def create_app(project_root: Path | str, *, env: Mapping[str, str] | None = None, cache_mode: WebCacheMode = "normal") -> FastAPI:
    """Create a Project-scoped local web application."""

    if cache_mode not in {"normal", "debug"}:
        raise ValueError(f"Unsupported Project Web cache mode: {cache_mode}")
    resolved_root = Path(project_root).expanduser().resolve(strict=False)
    read_model = ProjectWebReadModel(resolved_root, env=env)
    static_dir = Path(__file__).parent / "static"
    assets_dir = static_dir / "assets"

    app = FastAPI(title="Isomer Project Web GUI", version="0.1.0")
    app.add_middleware(GZipMiddleware, minimum_size=1024)
    app.state.project_root = resolved_root
    app.state.read_model = read_model
    app.state.cache_mode = cache_mode

    @app.middleware("http")
    async def cache_and_timing_headers(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        started = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = max(0.0, (time.perf_counter() - started) * 1000)
        response.headers["Server-Timing"] = f"app;dur={elapsed_ms:.1f}"
        response.headers["X-Isomer-Web-Cache-Mode"] = cache_mode
        response.headers.update(_cache_headers_for_path(request.url.path, cache_mode=cache_mode))
        return response

    app.mount("/assets", StaticFiles(directory=assets_dir, check_dir=False), name="assets")

    @app.get("/api/health")
    def health() -> dict[str, object]:
        return {"ok": True, "project_root": str(resolved_root), "cache_mode": cache_mode}

    @app.get("/api/project")
    def project() -> JSONResponse:
        return _json(read_model.project_summary())

    @app.get("/api/topics")
    def topics() -> JSONResponse:
        return _json(read_model.topics())

    @app.get("/api/explorer/project")
    def project_explorer(expanded_topic_id: list[str] = Query(default=[])) -> JSONResponse:
        return _json(read_model.project_explorer(expanded_topic_ids=tuple(expanded_topic_id)))

    @app.get("/api/openable/{openable_item_id:path}")
    def openable_item_descriptor(openable_item_id: str) -> JSONResponse:
        return _json(read_model.openable_item_descriptor(openable_item_id))

    @app.get("/api/topics/{topic_id}")
    def topic(topic_id: str) -> JSONResponse:
        return _json(read_model.topic(topic_id))

    @app.get("/api/topics/{topic_id}/runtime")
    def runtime(topic_id: str) -> JSONResponse:
        return _json(read_model.runtime(topic_id))

    @app.get("/api/topics/{topic_id}/overview")
    def topic_overview(topic_id: str) -> JSONResponse:
        return _json(read_model.topic_overview(topic_id))

    @app.get("/api/topics/{topic_id}/overview/json")
    def topic_overview_json(topic_id: str) -> JSONResponse:
        return _json(read_model.topic_overview_supporting_json(topic_id))

    @app.get("/api/topics/{topic_id}/actors")
    def actors(topic_id: str) -> JSONResponse:
        payload = read_model.topic(topic_id)
        return _json(
            {
                "ok": payload.get("ok", False),
                "mutated": False,
                "topic_actors": payload.get("topic_actors", []),
                "manifest": payload.get("topic_workspace_manifest"),
                "diagnostics": payload.get("diagnostics", []),
            }
        )

    @app.get("/api/topics/{topic_id}/records")
    def records(
        topic_id: str,
        record_kind: str | None = None,
        status: str | None = None,
        profile: str | None = None,
        facet: str | None = None,
        limit: int | None = Query(default=100, ge=1, le=1000),
    ) -> JSONResponse:
        return _json(
            read_model.records(
                topic_id,
                record_kind=record_kind,
                status=status,
                profile=profile,
                facet=facet,
                limit=limit,
            )
        )

    @app.get("/api/topics/{topic_id}/records/export")
    def records_export(
        topic_id: str,
        view: str = Query(default="dashboard"),
    ) -> JSONResponse:
        return _json(read_model.records_export(topic_id, view=view))

    @app.get("/api/topics/{topic_id}/graphs/{graph_scope}")
    def topic_graph(
        topic_id: str,
        graph_scope: str,
        renderer: str = Query(default="auto"),
        status: str | None = None,
        relation_kind: str | None = None,
        producer: str | None = None,
        time_range: str | None = None,
        search: str | None = None,
        limit: int | None = Query(default=None, ge=1, le=5000),
        cursor: str | None = None,
        include_secondary: bool = False,
        seed_node_id: list[str] = Query(default=[]),
        hop_radius: int | None = Query(default=None, ge=0, le=8),
        direction: str = Query(default="both"),
        edge_mode: str = Query(default="induced"),
    ) -> JSONResponse:
        return _json(
            read_model.topic_graph(
                topic_id,
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
                seed_node_ids=seed_node_id,
                hop_radius=hop_radius,
                direction=direction,
                edge_mode=edge_mode,
            )
        )

    @app.get("/api/topics/{topic_id}/recent-errors")
    def recent_errors(
        topic_id: str,
        limit: int = Query(default=50, ge=1, le=200),
    ) -> JSONResponse:
        return _json(read_model.recent_errors(topic_id, limit=limit))

    @app.get("/api/events")
    def topic_events(
        topic_id: str,
        interval_seconds: float = Query(default=2.0, ge=1.0, le=60.0),
        once: bool = False,
    ) -> StreamingResponse:
        async def stream() -> AsyncIterator[str]:
            last_event_id = None
            while True:
                payload = read_model.topic_change_event(topic_id)
                event_id = str(payload.get("event_id") or f"{topic_id}:unknown")
                event_type = str(payload.get("event_type") or "topic.index.changed")
                if once or event_id != last_event_id:
                    yield _sse(event_type, event_id, payload)
                    last_event_id = event_id
                if once:
                    break
                await asyncio.sleep(interval_seconds)

        return StreamingResponse(stream(), media_type="text/event-stream", headers=NO_CACHE_HEADERS)

    @app.get("/api/topics/{topic_id}/records/index/validate")
    def index_validate(topic_id: str, record_id: str | None = None) -> JSONResponse:
        return _json(read_model.index_validate(topic_id, record_id=record_id))

    @app.post("/api/topics/{topic_id}/records/index/rebuild")
    def index_rebuild(
        topic_id: str,
        request: IndexRebuildRequest = Body(default_factory=IndexRebuildRequest),
    ) -> JSONResponse:
        return _json(
            read_model.index_rebuild(
                topic_id,
                record_id=request.record_id,
                include_operation_set_files=request.include_operation_set_files,
                dry_run=request.dry_run,
            )
        )

    @app.post("/api/topics/{topic_id}/records/index/cleanup")
    def index_cleanup(
        topic_id: str,
        request: IndexCleanupRequest = Body(default_factory=IndexCleanupRequest),
    ) -> JSONResponse:
        return _json(
            read_model.index_cleanup(
                topic_id,
                stale_derived=request.stale_derived,
                orphaned=request.orphaned,
                missing_files=request.missing_files,
                apply_cleanup=request.apply_cleanup,
            )
        )

    @app.get("/api/topics/{topic_id}/records/{record_id}")
    def record_detail(
        topic_id: str,
        record_id: str,
        include_payload: bool = False,
    ) -> JSONResponse:
        return _json(read_model.record_detail(topic_id, record_id, include_payload=include_payload))

    @app.get("/api/topics/{topic_id}/ideas/{idea_id}")
    def idea_detail(
        topic_id: str,
        idea_id: str,
        include_source_json: bool = False,
    ) -> JSONResponse:
        return _json(read_model.idea_detail(topic_id, idea_id, include_source_json=include_source_json))

    @app.get("/api/topics/{topic_id}/viewer/records/{record_id}")
    def record_viewer_descriptor(topic_id: str, record_id: str) -> JSONResponse:
        return _json(read_model.record_viewer_descriptor(topic_id, record_id))

    @app.get("/api/topics/{topic_id}/records/{record_id}/render")
    def record_render(
        topic_id: str,
        record_id: str,
        output_format: str = Query(default="markdown", alias="format"),
    ) -> JSONResponse:
        if output_format != "markdown":
            return _json(
                {
                    "ok": False,
                    "mutated": False,
                    "error": {
                        "code": "unsupported_render_format",
                        "message": "Only Markdown rendering is supported by the web API.",
                    },
                    "diagnostics": [],
                }
            )
        return _json(read_model.record_render(topic_id, record_id))

    @app.get("/api/topics/{topic_id}/records/{record_id}/lineage")
    def record_lineage(
        topic_id: str,
        record_id: str,
        direction: str = Query(default="both"),
    ) -> JSONResponse:
        return _json(read_model.record_lineage(topic_id, record_id, direction=direction))

    @app.get("/api/topics/{topic_id}/records/{record_id}/siblings")
    def record_siblings(topic_id: str, record_id: str) -> JSONResponse:
        return _json(read_model.record_siblings(topic_id, record_id))

    @app.get("/api/topics/{topic_id}/records/{record_id}/files")
    def record_files(topic_id: str, record_id: str) -> JSONResponse:
        return _json(read_model.record_files(topic_id, record_id))

    @app.get("/api/topics/{topic_id}/records/{record_id}/files/{file_id:path}/content")
    def record_file_content(topic_id: str, record_id: str, file_id: str) -> Response:
        payload = read_model.record_file_content(topic_id, record_id, file_id)
        path = payload.get("path")
        if not payload.get("ok") or not isinstance(path, Path):
            return JSONResponse(content=jsonable_encoder(payload), status_code=404)
        media_type = payload.get("media_type")
        return FileResponse(path, media_type=str(media_type) if media_type else None)

    @app.get("/api/topics/{topic_id}/records/{record_id}/facets")
    def record_facets(topic_id: str, record_id: str, facet: str | None = None) -> JSONResponse:
        return _json(read_model.record_facets(topic_id, record_id, facet=facet))

    @app.get("/")
    def index() -> FileResponse:
        return FileResponse(static_dir / "index.html")

    @app.get("/api/{path:path}")
    def unknown_api(path: str) -> JSONResponse:
        return JSONResponse(
            content={
                "ok": False,
                "mutated": False,
                "error": {"code": "api_route_not_found", "message": f"API route not found: /api/{path}"},
                "diagnostics": [],
            },
            status_code=404,
        )

    @app.get("/{path:path}")
    def frontend_fallback(path: str) -> FileResponse:
        return FileResponse(static_dir / "index.html")

    return app


def _json(payload: object) -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(payload))


def _cache_headers_for_path(path: str, *, cache_mode: WebCacheMode) -> dict[str, str]:
    if cache_mode == "debug":
        return dict(NO_CACHE_HEADERS)
    if path.startswith("/api/") or path == "/api":
        return dict(API_CACHE_HEADERS)
    if _is_hashed_asset_path(path):
        return dict(IMMUTABLE_ASSET_HEADERS)
    if path.startswith("/assets/"):
        return dict(HTML_CACHE_HEADERS)
    return dict(HTML_CACHE_HEADERS)


def _is_hashed_asset_path(path: str) -> bool:
    return bool(_HASHED_ASSET_RE.match(path))


def _sse(event_type: str, event_id: str, payload: object) -> str:
    encoded = json.dumps(jsonable_encoder(payload), sort_keys=True, separators=(",", ":"))
    return f"id: {event_id}\nevent: {event_type}\ndata: {encoded}\n\n"
