"""Canonical Service Request lifecycle and synchronous dispatch."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping, Sequence
import uuid

from isomer_labs.kaoju.artifacts import KaojuServiceError
from isomer_labs.kaoju.execution import ExecutionAdapterCommandRequest, command_environment, execute_command_request, uses_explicit_pixi_environment
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.records.store import ResearchRecordRequest, create_record, show_record, update_record


SERVICE_DISPATCH_FORMS = {"tool_native_subagent", "launched_service_agent"}
SERVICE_REQUEST_TERMINAL = {"complete", "failed", "blocked", "cancelled"}


class KaojuServiceRequestService:
    """Persist operational support intent separately from Research Tasks and Runs."""

    def __init__(self, context: EffectiveTopicContext, *, env: Mapping[str, str], cwd: Path) -> None:
        self.context = context
        self.env = env
        self.cwd = cwd

    def create(
        self,
        *,
        task: str,
        scope_kind: str,
        scope_ref: str,
        expected_output_refs: Sequence[str],
        authorization: str,
        dispatch_form: str,
        completion_observations: Sequence[str],
        command_request: dict[str, object] | None,
        research_task_ref: str | None,
        run_ref: str | None,
        actor_ref: str,
        request_id: str | None = None,
    ) -> dict[str, object]:
        if dispatch_form not in SERVICE_DISPATCH_FORMS:
            raise KaojuServiceError("service_dispatch_form_invalid", f"Unsupported Service Dispatch Form: {dispatch_form}")
        if not task.strip() or not scope_kind.strip() or not scope_ref.strip() or not authorization.strip() or not actor_ref.strip():
            raise KaojuServiceError("service_request_invalid", "Service Request task, scope, authorization, and actor are required.")
        if command_request is not None:
            _validate_command_request(command_request)
        selected_id = request_id or f"service-request-{uuid.uuid4().hex[:12]}"
        metadata: dict[str, object] = {
            "schema_version": "isomer-service-request.v1",
            "supported_scope": {"kind": scope_kind, "ref": scope_ref},
            "task": task,
            "expected_output_refs": list(expected_output_refs),
            "authorization": authorization,
            "service_dispatch_form": dispatch_form,
            "completion_observation_rules": list(completion_observations),
            "research_task_ref": research_task_ref,
            "run_ref": run_ref,
            "command_request": command_request,
            "requester_actor_ref": actor_ref,
            "service_actor_ref": None,
            "support_artifact_refs": [],
            "dispatch_observations": [],
        }
        lifecycle_refs = {key: value for key, value in (("research_task_id", research_task_ref), ("run_id", run_ref)) if value is not None}
        payload, _ = create_record(
            self.context,
            ResearchRecordRequest(
                record_kind="service_request",
                record_id=selected_id,
                status="planned",
                lifecycle_refs=lifecycle_refs,
                metadata=metadata,
            ),
            env=self.env,
            cwd=self.cwd,
        )
        if payload.get("ok") is False:
            raise KaojuServiceError("service_request_create_failed", "Service Request creation failed.")
        return {**payload, "operation": "service-requests.create", "service_request_ref": selected_id, "affected_refs": [selected_id]}

    def dispatch(
        self,
        request_id: str,
        *,
        service_actor_ref: str,
        timeout_seconds: float,
        no_wait: bool = False,
    ) -> dict[str, object]:
        if no_wait:
            raise KaojuServiceError("service_request_no_wait_unsupported", "The first release supports synchronous Service Request dispatch only.", ("Remove --no-wait and retry.",))
        record = self._record(request_id)
        if str(record["status"]) in SERVICE_REQUEST_TERMINAL:
            raise KaojuServiceError("service_request_terminal", f"Service Request {request_id} is already terminal.")
        metadata = _metadata(record)
        self._update(request_id, status="running", metadata={"service_actor_ref": service_actor_ref, "dispatch_started": True})
        raw_command = metadata.get("command_request")
        observation: dict[str, object]
        if isinstance(raw_command, dict):
            _validate_command_request(raw_command)
            request = ExecutionAdapterCommandRequest.create(
                extension_point=str(raw_command["extension_point"]),
                argv=_strings(raw_command["argv"]),
                cwd=_command_cwd(raw_command, self.context.topic_workspace_path),
                timeout_seconds=timeout_seconds,
                recording_refs=(request_id, *_strings(metadata.get("expected_output_refs"))),
            )
            observation = execute_command_request(request, env=command_environment(self.env))
        else:
            observation = {
                "status": "blocked",
                "request": {"id": f"command-request-{uuid.uuid4().hex[:12]}", "schema_version": "isomer-execution-adapter-command-request.v1", "extension_point": "service_dispatch", "recording_refs": [request_id]},
                "recovery": "Attach a provider-neutral command request or complete the support task through an authorized Service Agent, then dispatch synchronously.",
            }
        terminal = "complete" if observation["status"] == "succeeded" else "blocked" if observation["status"] in {"blocked", "timed_out"} else "failed"
        support_ref = self._record_support_artifact(request_id, observation, service_actor_ref=service_actor_ref, terminal_status=terminal)
        updated = self._update(
            request_id,
            status=terminal,
            metadata={
                "dispatch_observations": [observation],
                "support_artifact_refs": [support_ref],
                "terminal_status": terminal,
                "completion_observed": terminal == "complete",
            },
        )
        command_request = observation.get("request")
        command_request_ref = command_request.get("id") if isinstance(command_request, dict) else None
        return {
            **updated,
            "ok": terminal == "complete",
            "mutated": True,
            "operation": "service-requests.dispatch",
            "service_request_ref": request_id,
            "support_artifact_ref": support_ref,
            "command_request_ref": command_request_ref,
            "terminal_status": terminal,
            "observation": observation,
            "affected_refs": [request_id, support_ref, *([str(command_request_ref)] if command_request_ref else [])],
            "recovery_actions": [str(observation.get("recovery"))] if observation.get("recovery") else [],
        }

    def status(self, request_id: str) -> dict[str, object]:
        payload, _ = show_record(self.context, request_id, env=self.env, include_body=False)
        if payload.get("ok") is False:
            raise KaojuServiceError("service_request_not_found", f"Service Request not found: {request_id}")
        return {**payload, "operation": "service-requests.status", "service_request_ref": request_id}

    def _record(self, request_id: str) -> dict[str, object]:
        payload, _ = show_record(self.context, request_id, env=self.env)
        record = payload.get("record")
        if not isinstance(record, dict) or record.get("record_kind") != "service_request":
            raise KaojuServiceError("service_request_not_found", f"Service Request not found: {request_id}")
        return record

    def _update(self, request_id: str, *, status: str, metadata: dict[str, object]) -> dict[str, object]:
        payload, _ = update_record(
            self.context,
            request_id,
            ResearchRecordRequest(record_kind="service_request", status=status, metadata=metadata),
            env=self.env,
            cwd=self.cwd,
        )
        if payload.get("ok") is False:
            raise KaojuServiceError("service_request_update_failed", f"Service Request update failed: {request_id}")
        return payload

    def _record_support_artifact(
        self,
        request_id: str,
        observation: dict[str, object],
        *,
        service_actor_ref: str,
        terminal_status: str,
    ) -> str:
        support_ref = f"support-artifact-{request_id}-{uuid.uuid4().hex[:8]}"
        body = json.dumps(
            {
                "schema_version": "isomer-service-support-artifact.v1",
                "service_request_ref": request_id,
                "service_actor_ref": service_actor_ref,
                "terminal_status": terminal_status,
                "observation": observation,
            },
            indent=2,
            sort_keys=True,
        ) + "\n"
        payload, _ = create_record(
            self.context,
            ResearchRecordRequest(
                record_kind="artifact",
                record_id=support_ref,
                status="ready" if terminal_status == "complete" else terminal_status,
                body=body,
                content_name="service-support.json",
                metadata={"artifact_type": "service-support", "service_request_ref": request_id, "producer": "service-team", "actor_ref": service_actor_ref},
                parents=[{"record_id": request_id, "lineage_kind": "derived_from", "parent_role": "service_request"}],
            ),
            env=self.env,
            cwd=self.cwd,
        )
        if payload.get("ok") is False:
            raise KaojuServiceError("service_support_artifact_failed", f"Support Artifact creation failed for {request_id}.")
        return support_ref


def _metadata(record: dict[str, object]) -> dict[str, object]:
    value = record.get("transition_metadata")
    if not isinstance(value, dict):
        raise KaojuServiceError("service_request_corrupt", "Service Request transition metadata is invalid.")
    return value


def _validate_command_request(value: dict[str, object]) -> None:
    extension_point = value.get("extension_point")
    argv = value.get("argv")
    if not isinstance(extension_point, str) or not isinstance(argv, list) or not argv or any(not isinstance(item, str) or not item for item in argv):
        raise KaojuServiceError("command_request_invalid", "Command request requires an extension_point and non-empty string argv array.")
    if extension_point in {"smoke_run", "code_trial"} and not uses_explicit_pixi_environment(argv):
        raise KaojuServiceError("command_request_ambient_environment", f"{extension_point} requires a named Pixi environment in the command request.", ("Use pixi run --environment <name> ... and retry.",))


def _command_cwd(value: dict[str, object], default: Path) -> Path:
    raw = value.get("cwd")
    selected = Path(str(raw)).expanduser() if isinstance(raw, str) and raw else default
    return selected.resolve(strict=False)


def _strings(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]
