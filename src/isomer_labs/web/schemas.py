"""Request models for the local Project web API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class IndexRebuildRequest(BaseModel):
    """Request body for explicit query-index rebuilds."""

    record_id: str | None = None
    include_operation_set_files: bool = False
    dry_run: bool = False


class IndexCleanupRequest(BaseModel):
    """Request body for explicit query-index cleanup."""

    stale_derived: bool = False
    orphaned: bool = False
    missing_files: bool = False
    apply_cleanup: bool = Field(default=False, alias="apply")

    model_config = {"populate_by_name": True}
