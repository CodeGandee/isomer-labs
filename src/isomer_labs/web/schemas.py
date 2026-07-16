"""Request models for the local Project web API."""

from __future__ import annotations

from typing import Literal

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


class ResearchIdeaSteeringRequestModel(BaseModel):
    """Confirmed Project Web request for one canonical steering action."""

    action: Literal["explore", "explore_instead"]
    target_idea_id: str
    actor_ref: str
    idempotency_key: str
    expected_index_revision: str | None = None
    expected_states: dict[str, dict[str, str]] = Field(default_factory=dict)
    replaced_idea_ids: list[str] = Field(default_factory=list)
    replacement_dispositions: dict[str, Literal["deferred", "closed"]] = Field(default_factory=dict)
    replacement_closure_reasons: dict[str, str] = Field(default_factory=dict)
    rationale: str | None = None
    user_prompt: str | None = None
    reopen_confirmed: bool = False
    gate_policy: Literal["none", "reopen", "replace", "all"] = "none"
    gate_resolution_ref: str | None = None
    agent_team_instance_id: str | None = None
    source_agent_instance_id: str | None = None
    target_agent_instance_id: str | None = None
    dispatch: bool = True
