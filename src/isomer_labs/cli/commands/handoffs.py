"""Click registration and handlers for handoff commands."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import click

from isomer_labs.cli.handlers.team_instance_support import (
    _agent_team_summary_or_diagnostic,
    _unsupported_adapter_diagnostic,
)
from isomer_labs.cli.handlers.shared import _context_for_options, _emit
from isomer_labs.cli.options import (
    CliOptions,
    common_options as _common_options,
    merge_options as _merge_options,
    topic_selection_options as _topic_selection_options,
    value as _value,
)
from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.houmao.adapter import HoumaoAdapterFacade
from isomer_labs.houmao.manifests import HOUMAO_ADAPTER_ID
from isomer_labs.runtime.models import HandoffRecord
from isomer_labs.runtime.store import open_workspace_runtime


def register_handoff_commands(app: click.Group) -> None:
    @app.group(name="handoffs", help="Manual handoff dispatch, observation, and normalization commands.")
    def handoffs_group() -> None:
        pass

    @handoffs_group.command(name="dispatch", help="Dispatch a manual handoff through an Execution Adapter.")
    @_common_options
    @_topic_selection_options
    @click.option("--adapter", default="houmao", type=click.Choice(("houmao",)), help="Execution Adapter.")
    @click.option("--source-agent-instance", default=None, help="Source Agent Instance id.")
    @click.option("--target-agent-instance", default=None, help="Target Agent Instance id.")
    @click.option("--message", default=None, help="Dispatch message text.")
    @click.option("--message-file", default=None, help="Path to dispatch message text.")
    @click.option("--expected-output", "expected_output_refs", multiple=True, help="Expected output ref.")
    @click.option("--completion-watcher-contract", "completion_watcher_contract_refs", multiple=True, help="Completion Watcher Contract ref.")
    @click.option("--actor", "actor_ref", default=None, help="Actor ref for dispatch provenance.")
    @click.pass_context
    def handoffs_dispatch_command(
        ctx: click.Context,
        project: str | None = None,
        manifest: str | None = None,
        output_format: str | None = None,
        json_output: bool = False,
        research_topic_id: str | None = None,
        topic_workspace_id: str | None = None,
        research_inquiry_id: str | None = None,
        research_task_id: str | None = None,
        run_id: str | None = None,
        agent_team_instance_id: str | None = None,
        agent_instance_id: str | None = None,
        topic_agent_team_profile_id: str | None = None,
        adapter: str = "houmao",
        source_agent_instance: str | None = None,
        target_agent_instance: str | None = None,
        message: str | None = None,
        message_file: str | None = None,
        expected_output_refs: tuple[str, ...] = (),
        completion_watcher_contract_refs: tuple[str, ...] = (),
        actor_ref: str | None = None,
    ) -> int:
        options = _merge_options(
            ctx,
            project=project,
            manifest=manifest,
            output_format=output_format,
            json_output=json_output,
            research_topic_id=research_topic_id,
            topic_workspace_id=topic_workspace_id,
            research_inquiry_id=research_inquiry_id,
            research_task_id=research_task_id,
            run_id=run_id,
            agent_team_instance_id=agent_team_instance_id,
            agent_instance_id=agent_instance_id,
            topic_agent_team_profile_id=topic_agent_team_profile_id,
        )
        return _cmd_handoffs_dispatch(
            options,
            adapter=adapter,
            source_agent_instance_id=source_agent_instance,
            target_agent_instance_id=target_agent_instance or agent_instance_id,
            message=message,
            message_file=message_file,
            expected_output_refs=list(expected_output_refs),
            completion_watcher_contract_refs=list(completion_watcher_contract_refs),
            actor_ref=actor_ref,
        )

    @handoffs_group.command(name="observe", help="Record a non-authoritative Signal Observation for a handoff.")
    @_common_options
    @_topic_selection_options
    @click.argument("handoff_id")
    @click.option("--adapter", default="houmao", type=click.Choice(("houmao",)), help="Execution Adapter.")
    @click.option("--source", "observation_source", default="mail", type=click.Choice(("mail", "gateway", "file", "inspection")), help="Observation source.")
    @click.option("--payload-json", default=None, help="File observation payload path.")
    @click.option("--summary", "summary_text", default=None, help="Operator-facing observation summary.")
    @click.option("--actor", "actor_ref", default=None, help="Actor ref for observation provenance.")
    @click.pass_context
    def handoffs_observe_command(
        ctx: click.Context,
        handoff_id: str,
        project: str | None = None,
        manifest: str | None = None,
        output_format: str | None = None,
        json_output: bool = False,
        research_topic_id: str | None = None,
        topic_workspace_id: str | None = None,
        research_inquiry_id: str | None = None,
        research_task_id: str | None = None,
        run_id: str | None = None,
        agent_team_instance_id: str | None = None,
        agent_instance_id: str | None = None,
        topic_agent_team_profile_id: str | None = None,
        adapter: str = "houmao",
        observation_source: str = "mail",
        payload_json: str | None = None,
        summary_text: str | None = None,
        actor_ref: str | None = None,
    ) -> int:
        options = _merge_options(
            ctx,
            project=project,
            manifest=manifest,
            output_format=output_format,
            json_output=json_output,
            research_topic_id=research_topic_id,
            topic_workspace_id=topic_workspace_id,
            research_inquiry_id=research_inquiry_id,
            research_task_id=research_task_id,
            run_id=run_id,
            agent_team_instance_id=agent_team_instance_id,
            agent_instance_id=agent_instance_id,
            topic_agent_team_profile_id=topic_agent_team_profile_id,
        )
        return _cmd_handoffs_observe(
            options,
            handoff_id=handoff_id,
            adapter=adapter,
            observation_source=observation_source,
            payload_json=payload_json,
            summary_text=summary_text,
            actor_ref=actor_ref,
        )

    @handoffs_group.command(name="normalize", help="Accept, reject, or route repair for a handoff result.")
    @_common_options
    @_topic_selection_options
    @click.argument("handoff_id")
    @click.option("--adapter", default="houmao", type=click.Choice(("houmao",)), help="Execution Adapter.")
    @click.option("--status", "normalization_status", required=True, type=click.Choice(("accepted", "rejected", "blocked", "superseded", "repair_routed", "follow_up")), help="Normalization outcome.")
    @click.option("--rationale", default=None, help="Normalization rationale.")
    @click.option("--signal-observation", "signal_observation_ids", multiple=True, help="Reviewed Signal Observation id.")
    @click.option("--output-artifact", "output_artifact_refs", multiple=True, help="Accepted or retained output Artifact ref.")
    @click.option("--corrective-ref", "corrective_refs", multiple=True, help="Corrective Service Request or follow-up handoff ref.")
    @click.option("--actor", "actor_ref", default=None, help="Actor ref for normalization provenance.")
    @click.pass_context
    def handoffs_normalize_command(
        ctx: click.Context,
        handoff_id: str,
        project: str | None = None,
        manifest: str | None = None,
        output_format: str | None = None,
        json_output: bool = False,
        research_topic_id: str | None = None,
        topic_workspace_id: str | None = None,
        research_inquiry_id: str | None = None,
        research_task_id: str | None = None,
        run_id: str | None = None,
        agent_team_instance_id: str | None = None,
        agent_instance_id: str | None = None,
        topic_agent_team_profile_id: str | None = None,
        adapter: str = "houmao",
        normalization_status: str = "",
        rationale: str | None = None,
        signal_observation_ids: tuple[str, ...] = (),
        output_artifact_refs: tuple[str, ...] = (),
        corrective_refs: tuple[str, ...] = (),
        actor_ref: str | None = None,
    ) -> int:
        options = _merge_options(
            ctx,
            project=project,
            manifest=manifest,
            output_format=output_format,
            json_output=json_output,
            research_topic_id=research_topic_id,
            topic_workspace_id=topic_workspace_id,
            research_inquiry_id=research_inquiry_id,
            research_task_id=research_task_id,
            run_id=run_id,
            agent_team_instance_id=agent_team_instance_id,
            agent_instance_id=agent_instance_id,
            topic_agent_team_profile_id=topic_agent_team_profile_id,
        )
        return _cmd_handoffs_normalize(
            options,
            handoff_id=handoff_id,
            adapter=adapter,
            normalization_status=normalization_status,
            rationale=rationale,
            signal_observation_ids=list(signal_observation_ids),
            output_artifact_refs=list(output_artifact_refs),
            corrective_refs=list(corrective_refs),
            actor_ref=actor_ref,
        )


def _cmd_handoffs_dispatch(
    options: CliOptions,
    *,
    adapter: str,
    source_agent_instance_id: str | None,
    target_agent_instance_id: str | None,
    message: str | None,
    message_file: str | None,
    expected_output_refs: list[str],
    completion_watcher_contract_refs: list[str],
    actor_ref: str | None,
) -> int:
    command_name = "handoffs dispatch"
    context, diagnostics = _context_for_options(options)
    payload = {"ok": False, "mutated": False, "execution_adapter": adapter, "dispatch": None}
    if context is None:
        return _emit(command_name, options, payload, diagnostics, [])
    if adapter != HOUMAO_ADAPTER_ID:
        diagnostics.append(_unsupported_adapter_diagnostic(adapter))
        return _emit(command_name, options, payload, diagnostics, [])
    team_id = _value(options, "agent_team_instance_id")
    if team_id is None:
        diagnostics.append(_handoff_diagnostic("Agent Team Instance is required for handoff dispatch.", field="agent_team_instance_id"))
        return _emit(command_name, options, payload, diagnostics, [])
    if target_agent_instance_id is None:
        diagnostics.append(_handoff_diagnostic("Target Agent Instance is required for handoff dispatch.", field="target_agent_instance_id"))
        return _emit(command_name, options, payload, diagnostics, [])
    text, message_diagnostics = _dispatch_message(context.project.root, message=message, message_file=message_file)
    diagnostics.extend(message_diagnostics)
    if has_errors(diagnostics):
        return _emit(command_name, options, payload, diagnostics, [])
    store, runtime_diagnostics = open_workspace_runtime(context, env=os.environ, read_only=False)
    diagnostics.extend(runtime_diagnostics)
    if store is None:
        return _emit(command_name, options, payload, diagnostics, [])
    summary = _agent_team_summary_or_diagnostic(store, context, team_id, diagnostics)
    if summary is None:
        store.close()
        return _emit(command_name, options, payload, diagnostics, [])
    source_id = source_agent_instance_id or _default_source_agent(summary)
    if source_id is None:
        diagnostics.append(_handoff_diagnostic("Source Agent Instance is required for handoff dispatch.", field="source_agent_instance_id"))
        store.close()
        return _emit(command_name, options, payload, diagnostics, [])
    facade = HoumaoAdapterFacade(env=os.environ)
    with store.connection:
        result = facade.dispatch_handoff(
            context=context,
            store=store,
            summary=summary,
            source_agent_instance_id=source_id,
            target_agent_instance_id=target_agent_instance_id,
            message=text,
            run_id=_value(options, "run_id"),
            research_task_id=_value(options, "research_task_id"),
            expected_output_refs=expected_output_refs,
            completion_watcher_contract_refs=completion_watcher_contract_refs,
            actor_ref=actor_ref,
        )
    diagnostics.extend(result.diagnostics)
    store.close()
    payload.update({"ok": not has_errors(diagnostics), "mutated": result.dispatch_record_id is not None, "dispatch": result.to_json()})
    lines = [
        f"Handoff dispatch status: {result.status}",
        f"Handoff: {result.handoff_id}",
        f"Run: {result.run_id}",
    ]
    return _emit(command_name, options, payload, diagnostics, lines)


def _cmd_handoffs_observe(
    options: CliOptions,
    *,
    handoff_id: str,
    adapter: str,
    observation_source: str,
    payload_json: str | None,
    summary_text: str | None,
    actor_ref: str | None,
) -> int:
    command_name = "handoffs observe"
    context, diagnostics = _context_for_options(options)
    payload = {"ok": False, "mutated": False, "execution_adapter": adapter, "observation": None}
    if context is None:
        return _emit(command_name, options, payload, diagnostics, [])
    if adapter != HOUMAO_ADAPTER_ID:
        diagnostics.append(_unsupported_adapter_diagnostic(adapter))
        return _emit(command_name, options, payload, diagnostics, [])
    store, runtime_diagnostics = open_workspace_runtime(context, env=os.environ, read_only=False)
    diagnostics.extend(runtime_diagnostics)
    if store is None:
        return _emit(command_name, options, payload, diagnostics, [])
    handoff = _handoff_or_diagnostic(store.list_handoffs(), handoff_id, diagnostics)
    summary = _summary_for_handoff(store, context, options, handoff, diagnostics)
    if handoff is None or summary is None:
        store.close()
        return _emit(command_name, options, payload, diagnostics, [])
    payload_path = _optional_project_path(context.project.root, payload_json)
    facade = HoumaoAdapterFacade(env=os.environ)
    with store.connection:
        result = facade.observe_handoff(
            context=context,
            store=store,
            summary=summary,
            handoff=handoff,
            observation_source=observation_source,
            observation_payload_path=payload_path,
            summary_text=summary_text,
            actor_ref=actor_ref,
        )
    diagnostics.extend(result.diagnostics)
    store.close()
    payload.update({"ok": not has_errors(diagnostics), "mutated": result.signal_observation_id is not None, "observation": result.to_json()})
    lines = [
        f"Handoff observation status: {result.status}",
        f"Handoff: {result.handoff_id}",
        f"Signal Observation: {result.signal_observation_id}",
        "Completion authority: no",
    ]
    return _emit(command_name, options, payload, diagnostics, lines)


def _cmd_handoffs_normalize(
    options: CliOptions,
    *,
    handoff_id: str,
    adapter: str,
    normalization_status: str,
    rationale: str | None,
    signal_observation_ids: list[str],
    output_artifact_refs: list[str],
    corrective_refs: list[str],
    actor_ref: str | None,
) -> int:
    command_name = "handoffs normalize"
    context, diagnostics = _context_for_options(options)
    payload = {"ok": False, "mutated": False, "execution_adapter": adapter, "normalization": None}
    if context is None:
        return _emit(command_name, options, payload, diagnostics, [])
    if adapter != HOUMAO_ADAPTER_ID:
        diagnostics.append(_unsupported_adapter_diagnostic(adapter))
        return _emit(command_name, options, payload, diagnostics, [])
    store, runtime_diagnostics = open_workspace_runtime(context, env=os.environ, read_only=False)
    diagnostics.extend(runtime_diagnostics)
    if store is None:
        return _emit(command_name, options, payload, diagnostics, [])
    handoff = _handoff_or_diagnostic(store.list_handoffs(), handoff_id, diagnostics)
    if handoff is None:
        store.close()
        return _emit(command_name, options, payload, diagnostics, [])
    facade = HoumaoAdapterFacade(env=os.environ)
    with store.connection:
        result = facade.normalize_handoff(
            context=context,
            store=store,
            handoff=handoff,
            status=normalization_status,
            rationale=rationale or f"Handoff {normalization_status} by Operator Agent.",
            signal_observation_ids=signal_observation_ids,
            output_artifact_refs=output_artifact_refs,
            corrective_refs=corrective_refs,
            actor_ref=actor_ref,
        )
    diagnostics.extend(result.diagnostics)
    store.close()
    payload.update({"ok": not has_errors(diagnostics), "mutated": result.normalization_record_id is not None, "normalization": result.to_json()})
    lines = [
        f"Handoff normalization status: {result.status}",
        f"Handoff: {result.handoff_id}",
        f"Normalization: {result.normalization_record_id}",
    ]
    return _emit(command_name, options, payload, diagnostics, lines)


def _handoff_diagnostic(message: str, *, field: str | None = None) -> Diagnostic:
    return Diagnostic(code="ISO080", severity="error", concept="Handoff", field=field, message=message)


def _dispatch_message(project_root: Path, *, message: str | None, message_file: str | None) -> tuple[str, list[Diagnostic]]:
    if message_file is None:
        return message or "Manual handoff dispatched by the Operator Agent.", []
    path = _optional_project_path(project_root, message_file)
    if path is None:
        return message or "", [_handoff_diagnostic("Message file path is required.", field="message_file")]
    try:
        return path.read_text(encoding="utf-8"), []
    except OSError as exc:
        return "", [Diagnostic(code="ISO080", severity="error", concept="Handoff", path=path, field="message_file", message=f"Message file could not be read: {exc}.")]


def _optional_project_path(project_root: Path, value: str | None) -> Path | None:
    if value is None:
        return None
    path = Path(value)
    if path.is_absolute():
        return path.expanduser().resolve(strict=False)
    return (project_root / path).expanduser().resolve(strict=False)


def _default_source_agent(summary: object) -> str | None:
    agents = getattr(summary, "agent_instances", [])
    for agent in agents:
        role = str(getattr(agent, "agent_role_id", ""))
        if "master" in role or "operator" in role:
            return str(agent.id)
    return str(agents[0].id) if agents else None


def _handoff_or_diagnostic(handoffs: list[HandoffRecord], handoff_id: str, diagnostics: list[Diagnostic]) -> HandoffRecord | None:
    for handoff in handoffs:
        if handoff.id == handoff_id:
            return handoff
    diagnostics.append(_handoff_diagnostic(f"Unknown handoff: {handoff_id}.", field="handoff_id"))
    return None


def _summary_for_handoff(
    store: Any,
    context: Any,
    options: CliOptions,
    handoff: HandoffRecord | None,
    diagnostics: list[Diagnostic],
) -> object | None:
    if handoff is None:
        return None
    team_id = _value(options, "agent_team_instance_id") or handoff.agent_team_instance_id
    if team_id is None:
        diagnostics.append(_handoff_diagnostic("Agent Team Instance is required for handoff observation.", field="agent_team_instance_id"))
        return None
    return _agent_team_summary_or_diagnostic(store, context, team_id, diagnostics)
