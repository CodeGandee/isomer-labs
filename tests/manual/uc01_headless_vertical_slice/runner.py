"""UC-01 manual acceptance harness runner."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Mapping

from isomer_labs.project.context import resolve_effective_topic_context
from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.models import (
    TOPIC_AGENT_TEAM_PROFILE_SCHEMA_VERSION,
    DomainAgentTeamTemplate,
    EffectiveTopicContext,
    SelectionRequest,
    TopicAgentTeamProfile,
    TopicAgentTeamProfileRegistration,
)
from isomer_labs.project import discover_project
from isomer_labs.teams.profile_bundles import materialize_topic_agent_team_profile_bundle
from isomer_labs.runtime.records import RuntimeLifecycleRecord
from isomer_labs.runtime.store import (
    WorkspaceRuntimeStore,
    initialize_workspace_runtime,
    open_workspace_runtime,
    prepare_topic_environment_readiness,
)
from isomer_labs.runtime.validation import validate_workspace_runtime
from isomer_labs.teams.profiles import parse_topic_agent_team_profile, validate_topic_agent_team_profile
from isomer_labs.teams.templates import (
    DEEPSCI_MINI_TEMPLATE_ID,
    find_domain_agent_team_template,
    validate_domain_agent_team_template,
)
from isomer_labs.core.toml_loader import load_toml
from isomer_labs.teams.instantiation import parse_topic_team_instantiation_packet
from isomer_labs.project.validation import build_project_state

from uc01_headless_vertical_slice.constants import (
    UC01_LIVE_GATE_ENV,
    UC01_PROFILE_ID,
    UC01_RESEARCH_TASK_ID,
    UC01_RESEARCH_TOPIC_ID,
    UC01_ROUTE_CLASSIFICATIONS,
    UC01_SEED_INQUIRY_ID,
)
from uc01_headless_vertical_slice.handoffs import write_handoff_round
from uc01_headless_vertical_slice.records import (
    artifact_record,
    artifact_specs,
    base_records,
    complete_record,
    evidence_specs,
    finding_specs,
    simple_record,
    view_specs,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURE_PROJECT = REPO_ROOT / "tests" / "fixtures" / "projects" / "uc01-headless-gb10"


@dataclass(frozen=True)
class UC01Result:
    ok: bool
    mutated: bool
    skipped: bool
    mode: str
    route_classification: str | None
    project_ref: str
    topic_ref: str
    topic_workspace_ref: str
    agent_team_instance_ref: str | None = None
    research_inquiry_refs: list[str] = field(default_factory=list)
    research_task_refs: list[str] = field(default_factory=list)
    run_refs: list[str] = field(default_factory=list)
    handoff_refs: list[str] = field(default_factory=list)
    artifact_refs: list[str] = field(default_factory=list)
    evidence_item_refs: list[str] = field(default_factory=list)
    finding_refs: list[str] = field(default_factory=list)
    gate_ref: str | None = None
    decision_record_ref: str | None = None
    view_manifest_refs: list[str] = field(default_factory=list)
    provenance_refs: list[str] = field(default_factory=list)
    adapter_payload_refs: list[str] = field(default_factory=list)
    adapter_command_run_refs: list[str] = field(default_factory=list)
    live_capability_report: dict[str, object] | None = None
    cleanup_status: str | None = None
    diagnostics: list[dict[str, object]] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "mutated": self.mutated,
            "skipped": self.skipped,
            "mode": self.mode,
            "route_classification": self.route_classification,
            "project_ref": self.project_ref,
            "topic_ref": self.topic_ref,
            "topic_workspace_ref": self.topic_workspace_ref,
            "agent_team_instance_ref": self.agent_team_instance_ref,
            "research_inquiry_refs": self.research_inquiry_refs,
            "research_task_refs": self.research_task_refs,
            "run_refs": self.run_refs,
            "handoff_refs": self.handoff_refs,
            "artifact_refs": self.artifact_refs,
            "evidence_item_refs": self.evidence_item_refs,
            "finding_refs": self.finding_refs,
            "gate_ref": self.gate_ref,
            "decision_record_ref": self.decision_record_ref,
            "view_manifest_refs": self.view_manifest_refs,
            "provenance_refs": self.provenance_refs,
            "adapter_payload_refs": self.adapter_payload_refs,
            "adapter_command_run_refs": self.adapter_command_run_refs,
            "live_capability_report": self.live_capability_report,
            "cleanup_status": self.cleanup_status,
            "diagnostics": self.diagnostics,
        }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the UC-01 headless vertical slice.")
    parser.add_argument(
        "--live-houmao",
        action="store_true",
        help=f"Request live Houmao mode. Requires {UC01_LIVE_GATE_ENV}=1 to mutate.",
    )
    args = parser.parse_args(argv)
    print(json.dumps(run_manual_validation(live_houmao=args.live_houmao), indent=2, sort_keys=True))
    return 0


def run_manual_validation(*, live_houmao: bool = False) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="isomer-uc01-") as tmp:
        root = Path(tmp) / "project"
        shutil.copytree(FIXTURE_PROJECT, root)
        _rewrite_fixture_team_repository_path(root)
        env = _validation_env()

        project_validation = _run_json(root, env, ["project", "--root", str(root), "validate"])
        _require(
            project_validation["status"] == 0 and project_validation["json"]["ok"],
            "fixture Project validation failed",
            project_validation,
        )
        context, context_diagnostics = resolve_fixture_context(root, env)
        _require(context is not None and not has_errors(context_diagnostics), "fixture context failed", [item.to_json() for item in context_diagnostics])
        assert context is not None

        simulated, simulated_diagnostics = run_uc01_headless(
            context,
            env=env,
            adapter_mode="simulated",
            actor_ref="operator-agent:manual-uc01",
            follow_up_selection=None,
            agent_team_instance_id=None,
        )
        _require(simulated.ok and not has_errors(simulated_diagnostics), "simulated UC-01 run failed", simulated.to_json())
        _require(
            simulated.route_classification == "uc07-measured-optimization",
            "simulated UC-01 selected an unexpected route classification",
            simulated.to_json(),
        )
        runtime_inspection, runtime_diagnostics = validate_workspace_runtime(context, env=env)
        _require(not has_errors(runtime_diagnostics), "runtime validation failed after simulated UC-01 run", [item.to_json() for item in runtime_diagnostics])
        summary, inspect_diagnostics = inspect_uc01_summary(context, env=env)
        _require(not has_errors(inspect_diagnostics) and summary["complete"], "UC-01 summary did not close", summary)
        live = _validate_live_mode(live_houmao, env)

        return {
            "ok": True,
            "fixture_project": str(FIXTURE_PROJECT),
            "topic": UC01_RESEARCH_TOPIC_ID,
            "project_validate_diagnostics": project_validation["json"]["diagnostics"],
            "simulated": {
                "mode": simulated.mode,
                "route_classification": simulated.route_classification,
                "agent_team_instance_ref": simulated.agent_team_instance_ref,
                "artifact_count": len(simulated.artifact_refs),
                "evidence_item_count": len(simulated.evidence_item_refs),
                "view_manifest_count": len(simulated.view_manifest_refs),
            },
            "runtime": {
                "counts": runtime_inspection.counts,
                "diagnostics": [diagnostic.to_json() for diagnostic in runtime_diagnostics],
            },
            "uc01_summary": summary,
            "live": live,
        }


def resolve_fixture_context(root: Path, env: Mapping[str, str]) -> tuple[EffectiveTopicContext | None, list[Diagnostic]]:
    project, diagnostics = discover_project(cwd=root, env=env, project_selector=str(root), manifest_selector=None)
    if project is None:
        return None, diagnostics
    state = build_project_state(project)
    diagnostics.extend(state.diagnostics)
    context, context_diagnostics = resolve_effective_topic_context(
        state,
        SelectionRequest(research_topic_id=UC01_RESEARCH_TOPIC_ID),
        cwd=root,
        env=env,
    )
    diagnostics.extend(context_diagnostics)
    return context, diagnostics


def run_uc01_headless(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    adapter_mode: str,
    actor_ref: str | None,
    follow_up_selection: str | None,
    agent_team_instance_id: str | None,
) -> tuple[UC01Result, list[Diagnostic]]:
    diagnostics = _fixture_diagnostics(context)
    live_capability_report = _live_capability_report(context, env) if adapter_mode == "live" else None
    route = follow_up_selection or "uc07-measured-optimization"
    if route not in UC01_ROUTE_CLASSIFICATIONS:
        diagnostics.append(
            Diagnostic(
                code="ISO081",
                severity="error",
                concept="UC-01 follow-up Gate",
                field="follow_up_selection",
                message=f"Unsupported UC-01 route classification: {route}.",
            )
        )
    if adapter_mode == "live" and env.get(UC01_LIVE_GATE_ENV) != "1":
        diagnostics.append(
            Diagnostic(
                code="ISO080",
                severity="warning",
                concept="UC-01 live validation",
                field=UC01_LIVE_GATE_ENV,
                message="Live Houmao UC-01 validation skipped because the live-validation gate is absent.",
            )
        )
        return (
            _empty_result(
                context,
                mode="live",
                skipped=True,
                diagnostics=diagnostics,
                live_capability_report=live_capability_report,
                cleanup_status="skipped",
            ),
            diagnostics,
        )
    if has_errors(diagnostics):
        return _empty_result(context, mode=adapter_mode, skipped=False, diagnostics=diagnostics), diagnostics

    init_result, init_diagnostics = initialize_workspace_runtime(context, env=env)
    diagnostics.extend(init_diagnostics)
    if init_result is None or has_errors(diagnostics):
        return _empty_result(context, mode=adapter_mode, skipped=False, diagnostics=diagnostics), diagnostics

    existing_store, existing_diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    diagnostics.extend(existing_diagnostics)
    if existing_store is None:
        return _empty_result(context, mode=adapter_mode, skipped=False, diagnostics=diagnostics), diagnostics
    try:
        existing_summary = summarize_uc01_records(existing_store)
        if bool(existing_summary.get("complete")):
            return (
                _result_from_summary(
                    context,
                    existing_store,
                    mode=adapter_mode,
                    mutated=False,
                    live_capability_report=live_capability_report,
                    cleanup_status="already-complete" if adapter_mode == "live" else None,
                ),
                diagnostics,
            )
    finally:
        existing_store.close()

    readiness_result, readiness_diagnostics = prepare_topic_environment_readiness(
        context,
        env=env,
        actor_ref=actor_ref,
    )
    diagnostics.extend(readiness_diagnostics)
    if readiness_result is None or readiness_result.readiness is None or readiness_result.readiness.status != "ready":
        return _empty_result(context, mode=adapter_mode, skipped=False, diagnostics=diagnostics), diagnostics

    profile, template, load_diagnostics = load_uc01_profile_and_template(context)
    diagnostics.extend(load_diagnostics)
    if profile is None or template is None or has_errors(diagnostics):
        return _empty_result(context, mode=adapter_mode, skipped=False, diagnostics=diagnostics), diagnostics

    store, open_diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    diagnostics.extend(open_diagnostics)
    if store is None:
        return _empty_result(context, mode=adapter_mode, skipped=False, diagnostics=diagnostics), diagnostics

    try:
        with store.connection:
            result = _write_uc01_records(
                context,
                store,
                profile=profile,
                template=template,
                adapter_mode=adapter_mode,
                actor_ref=actor_ref or "operator-agent:uc01",
                route_classification=route,
                agent_team_instance_id=agent_team_instance_id,
                live_capability_report=live_capability_report,
            )
    except ValueError as exc:
        diagnostics.append(
            Diagnostic(
                code="ISO080",
                severity="error",
                concept="UC-01 manual harness",
                message=str(exc),
            )
        )
        result = _empty_result(context, mode=adapter_mode, skipped=False, diagnostics=diagnostics)
    finally:
        store.close()
    return result, diagnostics


def inspect_uc01_summary(context: EffectiveTopicContext, *, env: Mapping[str, str]) -> tuple[dict[str, object], list[Diagnostic]]:
    store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if store is None:
        return {"exists": False, "complete": False}, diagnostics
    summary = summarize_uc01_records(store)
    store.close()
    return summary, diagnostics


def summarize_uc01_records(store: WorkspaceRuntimeStore) -> dict[str, object]:
    records = store.list_lifecycle_records()
    by_kind: dict[str, list[RuntimeLifecycleRecord]] = {}
    for record in records:
        if _is_uc01_record(record):
            by_kind.setdefault(record.record_kind, []).append(record)
    gate = _first(by_kind.get("gate", []))
    decision = _first(by_kind.get("decision_record", []))
    route = decision.transition_metadata.get("route_classification") if decision is not None else None
    team = next(
        (
            record
            for record in store.list_agent_team_instances()
            if record.research_topic_id == UC01_RESEARCH_TOPIC_ID and record.domain_agent_team_template_id == DEEPSCI_MINI_TEMPLATE_ID
        ),
        None,
    )
    handoffs = [
        record
        for record in store.list_handoffs()
        if record.research_topic_id == UC01_RESEARCH_TOPIC_ID and record.id.startswith("handoff-uc01-")
    ]
    adapter_payload_refs = [
        record.id
        for record in store.list_adapter_payload_refs()
        if record.research_topic_id == UC01_RESEARCH_TOPIC_ID and record.id.startswith("adapter-payload-uc01-")
    ]
    adapter_command_run_refs = [
        record.id
        for record in store.list_adapter_command_runs()
        if record.research_topic_id == UC01_RESEARCH_TOPIC_ID and record.id.startswith("adapter-command-uc01-")
    ]
    required = {
        "research_inquiry": UC01_SEED_INQUIRY_ID,
        "research_task": UC01_RESEARCH_TASK_ID,
        "gate": "gate-uc01-follow-up-inquiry",
        "decision_record": "decision-uc01-follow-up-inquiry",
    }
    missing = [
        f"{kind}:{record_id}"
        for kind, record_id in required.items()
        if all(record.id != record_id for record in by_kind.get(kind, []))
    ]
    for kind in ("artifact", "evidence_item", "finding", "view_manifest", "provenance_record"):
        if not by_kind.get(kind):
            missing.append(kind)
    return {
        "exists": bool(by_kind),
        "complete": not missing and gate is not None and gate.status == "resolved" and decision is not None,
        "route_classification": route,
        "missing": missing,
        "counts": {kind: len(items) for kind, items in sorted(by_kind.items())},
        "agent_team_instance_ref": team.id if team is not None else None,
        "research_inquiry_refs": [record.id for record in by_kind.get("research_inquiry", [])],
        "research_task_refs": [record.id for record in by_kind.get("research_task", [])],
        "run_refs": [record.id for record in by_kind.get("run", [])],
        "handoff_refs": [record.id for record in handoffs],
        "artifact_refs": [record.id for record in by_kind.get("artifact", [])],
        "evidence_item_refs": [record.id for record in by_kind.get("evidence_item", [])],
        "finding_refs": [record.id for record in by_kind.get("finding", [])],
        "gate_ref": gate.id if gate is not None else None,
        "decision_record_ref": decision.id if decision is not None else None,
        "view_manifest_refs": [record.id for record in by_kind.get("view_manifest", [])],
        "provenance_refs": [record.id for record in by_kind.get("provenance_record", [])],
        "adapter_payload_refs": adapter_payload_refs,
        "adapter_command_run_refs": adapter_command_run_refs,
    }


def validate_uc01_records(context: EffectiveTopicContext, store: WorkspaceRuntimeStore) -> list[Diagnostic]:
    summary = summarize_uc01_records(store)
    diagnostics: list[Diagnostic] = []
    if not summary["exists"]:
        return diagnostics
    for missing in _summary_list(summary, "missing"):
        diagnostics.append(
            Diagnostic(
                code="ISO081",
                severity="error",
                concept="UC-01 Runtime Research Records",
                path=store.db_path,
                message=f"UC-01 recording graph is missing required record: {missing}.",
            )
        )
    route = summary.get("route_classification")
    if route not in UC01_ROUTE_CLASSIFICATIONS:
        diagnostics.append(
            Diagnostic(
                code="ISO081",
                severity="error",
                concept="UC-01 follow-up Gate",
                path=store.db_path,
                message="UC-01 Decision Record has no supported route classification.",
            )
        )
    forbidden_kinds = {
        "baseline_measurement",
        "candidate_optimization",
        "speedup",
        "utilization",
        "correctness_result",
        "automatic_replay",
        "compute_budget_gate",
    }
    for record in store.list_lifecycle_records():
        marker = str(record.transition_metadata.get("uc07_record_kind", ""))
        if marker in forbidden_kinds:
            diagnostics.append(
                Diagnostic(
                    code="ISO081",
                    severity="error",
                    concept="UC-01 measurement boundary",
                    path=store.db_path,
                    field=record.id,
                    message="UC-01 must not create measured optimization records reserved for UC-07.",
                )
            )
    if context.research_topic.id == UC01_RESEARCH_TOPIC_ID and summary["exists"] and not summary["complete"]:
        diagnostics.append(
            Diagnostic(
                code="ISO081",
                severity="warning",
                concept="UC-01 Runtime Research Records",
                path=store.db_path,
                message="UC-01 records exist but the follow-up Gate is not fully closed.",
            )
        )
    return diagnostics


def load_uc01_profile_and_template(
    context: EffectiveTopicContext,
) -> tuple[TopicAgentTeamProfile | None, DomainAgentTeamTemplate | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    template_registration = find_domain_agent_team_template(DEEPSCI_MINI_TEMPLATE_ID, context.project)
    template = None
    if template_registration is not None:
        template_report = validate_domain_agent_team_template(context.project, template_registration, include_harness=False)
        diagnostics.extend(template_report.diagnostics)
        template = template_report.template
    packet_path = context.project.root / "fixtures" / "uc01" / "topic-team-instantiation-packet.toml"
    if packet_path.exists() and template is not None:
        raw_packet, packet_load_diagnostics = load_toml(packet_path, "Topic Team Instantiation Packet")
        diagnostics.extend(packet_load_diagnostics)
        if raw_packet is not None:
            packet, packet_parse_diagnostics = parse_topic_team_instantiation_packet(packet_path, raw_packet)
            diagnostics.extend(packet_parse_diagnostics)
            if packet is not None:
                materialization = materialize_topic_agent_team_profile_bundle(
                    context,
                    template,
                    packet,
                    write=True,
                    overwrite=True,
                )
                diagnostics.extend(materialization.diagnostics)
                if materialization.profile is not None:
                    _register_materialized_profile_for_manual_run(context, materialization.profile)
                return materialization.profile, template, diagnostics

    profile_id = context.topic_agent_team_profile_id or UC01_PROFILE_ID
    registration = context.project.manifest.first_topic_agent_team_profile(profile_id)
    if registration is None:
        diagnostics.append(
            Diagnostic(
                code="ISO020",
                severity="error",
                concept="Topic Agent Team Profile",
                field="topic_agent_team_profile_id",
                message=f"UC-01 requires a registered Topic Agent Team Profile: {profile_id}.",
            )
        )
        return None, None, diagnostics
    profile_path = context.project.root / registration.path_input
    raw, load_diagnostics = load_toml(profile_path, "Topic Agent Team Profile")
    diagnostics.extend(load_diagnostics)
    profile = None
    if raw is not None:
        profile, parse_diagnostics = parse_topic_agent_team_profile(profile_path, raw)
        diagnostics.extend(parse_diagnostics)
    template_registration = find_domain_agent_team_template(registration.domain_agent_team_template_id, context.project)
    if template_registration is None:
        diagnostics.append(
            Diagnostic(
                code="ISO016",
                severity="error",
                concept="Domain Agent Team Template",
                field="domain_agent_team_template_id",
                message=f"Unknown Domain Agent Team Template: {registration.domain_agent_team_template_id}.",
            )
        )
        return profile, None, diagnostics
    template_report = validate_domain_agent_team_template(context.project, template_registration, include_harness=False)
    diagnostics.extend(template_report.diagnostics)
    profile_report = validate_topic_agent_team_profile(profile, template_report.template, project=context.project, source_path=profile_path)
    diagnostics.extend(profile_report.diagnostics)
    return profile, template_report.template, diagnostics


def _register_materialized_profile_for_manual_run(
    context: EffectiveTopicContext,
    profile: TopicAgentTeamProfile,
) -> None:
    if context.project.manifest.first_topic_agent_team_profile(profile.id) is not None:
        return
    context.project.manifest.topic_agent_team_profiles.append(
        TopicAgentTeamProfileRegistration(
            id=profile.id,
            path_input=_project_relative_path(context.project.root, profile.source_path),
            domain_agent_team_template_id=profile.domain_agent_team_template_id,
            research_topic_id=profile.research_topic_id,
            schema_version=TOPIC_AGENT_TEAM_PROFILE_SCHEMA_VERSION,
            status="active",
            source_path=context.project.manifest_path,
        )
    )


def _project_relative_path(project_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(project_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def _write_uc01_records(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    *,
    profile: TopicAgentTeamProfile,
    template: DomainAgentTeamTemplate,
    adapter_mode: str,
    actor_ref: str,
    route_classification: str,
    agent_team_instance_id: str | None,
    live_capability_report: dict[str, object] | None,
) -> UC01Result:
    existing_team_id = agent_team_instance_id or "ati-uc01-gb10-deepsci-mini"
    if store.get_lifecycle_record("decision-uc01-follow-up-inquiry") is not None:
        return _result_from_summary(
            context,
            store,
            mode=adapter_mode,
            mutated=False,
            live_capability_report=live_capability_report,
            cleanup_status="already-complete" if adapter_mode == "live" else None,
        )
    creation = None
    team = store.get_agent_team_instance(existing_team_id)
    if team is None:
        creation, create_diagnostics = store.create_agent_team_instance(
            context,
            profile,
            template,
            requested_id=existing_team_id,
            env=os.environ,
        )
        if create_diagnostics:
            raise ValueError("; ".join(diagnostic.message for diagnostic in create_diagnostics))
        if creation is None:
            raise ValueError("UC-01 Agent Team Instance could not be created.")
        team = creation.agent_team_instance
    store.link_agent_team_instance_refs(team.id, status="running")
    summary = store.get_agent_team_instance_summary(team.id)
    if summary is None:
        raise ValueError("UC-01 Agent Team Instance summary could not be loaded after creation.")
    agents_by_role = {agent.agent_role_id: agent for agent in summary.agent_instances}
    for role_id in ("deepsci-mini-lead", "deepsci-mini-scout", "deepsci-mini-synth-reviewer"):
        if role_id not in agents_by_role:
            raise ValueError(f"UC-01 Agent Team Instance is missing role {role_id}.")

    artifact_refs: list[str] = []
    evidence_refs: list[str] = []
    finding_refs: list[str] = []
    view_refs: list[str] = []
    provenance_refs: list[str] = []
    adapter_payload_refs: list[str] = []
    adapter_command_refs: list[str] = []

    for record in base_records(context, actor_ref):
        store.upsert_lifecycle_record(record)
        provenance_refs.extend(record.provenance_refs)

    scout_refs = write_handoff_round(
        context,
        store,
        team_id=team.id,
        source_agent_id=agents_by_role["deepsci-mini-lead"].id,
        target_agent_id=agents_by_role["deepsci-mini-scout"].id,
        stage="scout",
        actor_ref=actor_ref,
    )
    synth_refs = write_handoff_round(
        context,
        store,
        team_id=team.id,
        source_agent_id=agents_by_role["deepsci-mini-lead"].id,
        target_agent_id=agents_by_role["deepsci-mini-synth-reviewer"].id,
        stage="synthesis-review",
        actor_ref=actor_ref,
    )
    adapter_payload_refs.extend([*scout_refs["payload_refs"], *synth_refs["payload_refs"]])
    adapter_command_refs.extend([*scout_refs["command_refs"], *synth_refs["command_refs"]])

    for artifact in artifact_specs(route_classification):
        record, provenance = artifact_record(context, artifact, actor_ref)
        store.upsert_lifecycle_record(provenance)
        store.upsert_lifecycle_record(record)
        artifact_refs.append(record.id)
        provenance_refs.append(provenance.id)
    for evidence in evidence_specs():
        record, provenance = simple_record(context, "evidence_item", str(evidence["id"]), "supported", evidence, actor_ref)
        store.upsert_lifecycle_record(provenance)
        store.upsert_lifecycle_record(record)
        evidence_refs.append(record.id)
        provenance_refs.append(provenance.id)
    for finding in finding_specs():
        record, provenance = simple_record(context, "finding", str(finding["id"]), "candidate", finding, actor_ref)
        store.upsert_lifecycle_record(provenance)
        store.upsert_lifecycle_record(record)
        finding_refs.append(record.id)
        provenance_refs.append(provenance.id)

    gate, gate_provenance = simple_record(
        context,
        "gate",
        "gate-uc01-follow-up-inquiry",
        "resolved",
        {
            "uc01": True,
            "governed_action": "select-follow-up-research-inquiry",
            "route_classification_candidates": list(UC01_ROUTE_CLASSIFICATIONS),
            "selected_route_classification": route_classification,
            "selected_research_inquiry_id": _selected_follow_up_inquiry_id(route_classification),
        },
        actor_ref,
    )
    decision, decision_provenance = simple_record(
        context,
        "decision_record",
        "decision-uc01-follow-up-inquiry",
        "resolved",
        {
            "uc01": True,
            "route_classification": route_classification,
            "selected_research_inquiry_id": _selected_follow_up_inquiry_id(route_classification),
            "rejected_alternatives": [item for item in UC01_ROUTE_CLASSIFICATIONS if item != route_classification],
            "supporting_evidence_item_refs": evidence_refs,
        },
        actor_ref,
    )
    selected_inquiry, selected_inquiry_provenance = simple_record(
        context,
        "research_inquiry",
        _selected_follow_up_inquiry_id(route_classification),
        "planned",
        {
            "uc01": True,
            "parent_research_inquiry_id": UC01_SEED_INQUIRY_ID,
            "route_classification": route_classification,
        },
        actor_ref,
    )
    for record in (gate_provenance, gate, decision_provenance, decision, selected_inquiry_provenance, selected_inquiry):
        store.upsert_lifecycle_record(record)
    provenance_refs.extend([gate_provenance.id, decision_provenance.id, selected_inquiry_provenance.id])

    for view in view_specs(artifact_refs, evidence_refs, finding_refs, route_classification):
        record, provenance = simple_record(context, "view_manifest", str(view["id"]), "ready", view, actor_ref)
        store.upsert_lifecycle_record(provenance)
        store.upsert_lifecycle_record(record)
        view_refs.append(record.id)
        provenance_refs.append(provenance.id)

    closeout = complete_record(context, UC01_RESEARCH_TASK_ID, actor_ref)
    store.upsert_lifecycle_record(closeout)
    store.link_agent_team_instance_refs(
        team.id,
        run_ids=["run-uc01-scout", "run-uc01-synthesis-review", "run-uc01-closeout"],
        handoff_ids=["handoff-uc01-scout", "handoff-uc01-synthesis-review"],
        status="stopped" if adapter_mode == "live" else "ready",
    )
    return UC01Result(
        ok=True,
        mutated=True,
        skipped=False,
        mode=adapter_mode,
        route_classification=route_classification,
        project_ref=str(context.project.root),
        topic_ref=context.research_topic.id,
        topic_workspace_ref=context.topic_workspace_id,
        agent_team_instance_ref=team.id,
        research_inquiry_refs=[UC01_SEED_INQUIRY_ID, _selected_follow_up_inquiry_id(route_classification)],
        research_task_refs=[UC01_RESEARCH_TASK_ID, "research-task-uc01-scout", "research-task-uc01-synthesis-review"],
        run_refs=["run-uc01-scout", "run-uc01-synthesis-review", "run-uc01-closeout"],
        handoff_refs=["handoff-uc01-scout", "handoff-uc01-synthesis-review"],
        artifact_refs=artifact_refs,
        evidence_item_refs=evidence_refs,
        finding_refs=finding_refs,
        gate_ref=gate.id,
        decision_record_ref=decision.id,
        view_manifest_refs=view_refs,
        provenance_refs=sorted(set(provenance_refs)),
        adapter_payload_refs=adapter_payload_refs,
        adapter_command_run_refs=adapter_command_refs,
        live_capability_report=live_capability_report,
        cleanup_status="stopped" if adapter_mode == "live" else None,
        diagnostics=[],
    )


def _validate_live_mode(requested: bool, env: Mapping[str, str]) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="isomer-uc01-live-") as tmp:
        root = Path(tmp) / "project"
        shutil.copytree(FIXTURE_PROJECT, root)
        _rewrite_fixture_team_repository_path(root)
        context, diagnostics = resolve_fixture_context(root, env)
        _require(context is not None and not has_errors(diagnostics), "live fixture context failed", [item.to_json() for item in diagnostics])
        assert context is not None
        result, run_diagnostics = run_uc01_headless(
            context,
            env=env,
            adapter_mode="live",
            actor_ref="operator-agent:manual-uc01",
            follow_up_selection=None,
            agent_team_instance_id=None,
        )
        if env.get(UC01_LIVE_GATE_ENV) != "1":
            _require(result.skipped and not result.mutated and not has_errors(run_diagnostics), "live mode did not skip cleanly", result.to_json())
            return {
                "requested": requested,
                "status": "skipped",
                "gate": UC01_LIVE_GATE_ENV,
                "diagnostics": [diagnostic.to_json() for diagnostic in run_diagnostics],
            }
        _require(result.ok and not has_errors(run_diagnostics), "live UC-01 run failed", result.to_json())
        return {
            "requested": True,
            "status": "completed",
            "mode": result.mode,
            "route_classification": result.route_classification,
            "cleanup_status": result.cleanup_status,
        }


def _selected_follow_up_inquiry_id(route_classification: str) -> str:
    if route_classification == "uc07-measured-optimization":
        return "gb10-flash-attention-4-measured-optimization"
    if route_classification == "more-scouting":
        return "gb10-flash-attention-4-additional-scouting"
    return "gb10-flash-attention-4-alternate-investigation"


def _fixture_diagnostics(context: EffectiveTopicContext) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if context.research_topic.id != UC01_RESEARCH_TOPIC_ID:
        diagnostics.append(
            Diagnostic(
                code="ISO080",
                severity="error",
                concept="UC-01 fixture Project",
                field="research_topic_id",
                message=f"UC-01 requires Research Topic {UC01_RESEARCH_TOPIC_ID}.",
            )
        )
    if context.domain_agent_team_template_id not in {None, DEEPSCI_MINI_TEMPLATE_ID}:
        diagnostics.append(
            Diagnostic(
                code="ISO080",
                severity="error",
                concept="UC-01 fixture Project",
                field="domain_agent_team_template_id",
                message="UC-01 requires the deepsci-mini Domain Agent Team Template.",
            )
        )
    return diagnostics


def _live_capability_report(context: EffectiveTopicContext, env: Mapping[str, str]) -> dict[str, object]:
    command_override = env.get("ISOMER_HOUMAO_COMMAND")
    command_name = command_override or "houmao-mgr"
    resolved_command = shutil.which(command_name)
    checkout_candidates = [
        str(context.project.root / "extern" / "orphan" / "houmao"),
        env.get("ISOMER_HOUMAO_CHECKOUT", ""),
        str(Path.home() / "workspace" / "code" / "houmao"),
    ]
    return {
        "gate": UC01_LIVE_GATE_ENV,
        "gate_present": env.get(UC01_LIVE_GATE_ENV) == "1",
        "houmao_command": command_name,
        "houmao_command_resolved": resolved_command,
        "checkout_path_candidates": [path for path in checkout_candidates if path],
        "read_only_checks": ["command-resolution", "checkout-path-candidates", "cleanup-plan"],
        "cleanup_plan": "record Agent Team Instance cleanup status and preserve partial Workspace Runtime state",
    }


def _empty_result(
    context: EffectiveTopicContext,
    *,
    mode: str,
    skipped: bool,
    diagnostics: list[Diagnostic],
    live_capability_report: dict[str, object] | None = None,
    cleanup_status: str | None = None,
) -> UC01Result:
    return UC01Result(
        ok=not has_errors(diagnostics),
        mutated=False,
        skipped=skipped,
        mode=mode,
        route_classification=None,
        project_ref=str(context.project.root),
        topic_ref=context.research_topic.id,
        topic_workspace_ref=context.topic_workspace_id,
        live_capability_report=live_capability_report,
        cleanup_status=cleanup_status,
        diagnostics=[diagnostic.to_json() for diagnostic in diagnostics],
    )


def _result_from_summary(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    *,
    mode: str,
    mutated: bool,
    live_capability_report: dict[str, object] | None = None,
    cleanup_status: str | None = None,
) -> UC01Result:
    summary = summarize_uc01_records(store)
    return UC01Result(
        ok=bool(summary.get("complete")),
        mutated=mutated,
        skipped=False,
        mode=mode,
        route_classification=_summary_str(summary, "route_classification"),
        project_ref=str(context.project.root),
        topic_ref=context.research_topic.id,
        topic_workspace_ref=context.topic_workspace_id,
        agent_team_instance_ref=_summary_str(summary, "agent_team_instance_ref"),
        research_inquiry_refs=_summary_list(summary, "research_inquiry_refs"),
        research_task_refs=_summary_list(summary, "research_task_refs"),
        run_refs=_summary_list(summary, "run_refs"),
        handoff_refs=_summary_list(summary, "handoff_refs"),
        artifact_refs=_summary_list(summary, "artifact_refs"),
        evidence_item_refs=_summary_list(summary, "evidence_item_refs"),
        finding_refs=_summary_list(summary, "finding_refs"),
        gate_ref=_summary_str(summary, "gate_ref"),
        decision_record_ref=_summary_str(summary, "decision_record_ref"),
        view_manifest_refs=_summary_list(summary, "view_manifest_refs"),
        provenance_refs=_summary_list(summary, "provenance_refs"),
        adapter_payload_refs=_summary_list(summary, "adapter_payload_refs"),
        adapter_command_run_refs=_summary_list(summary, "adapter_command_run_refs"),
        live_capability_report=live_capability_report,
        cleanup_status=cleanup_status,
    )


def _is_uc01_record(record: RuntimeLifecycleRecord) -> bool:
    if record.research_topic_id != UC01_RESEARCH_TOPIC_ID:
        return False
    return bool(record.transition_metadata.get("uc01")) or record.id.startswith(
        ("artifact-uc01-", "evidence-uc01-", "finding-uc01-", "view-manifest-uc01-")
    )


def _first(records: list[RuntimeLifecycleRecord]) -> RuntimeLifecycleRecord | None:
    return records[0] if records else None


def _summary_str(summary: dict[str, object], key: str) -> str | None:
    value = summary.get(key)
    return value if isinstance(value, str) else None


def _summary_list(summary: dict[str, object], key: str) -> list[str]:
    value = summary.get(key)
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _validation_env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT / "src") + os.pathsep + str(REPO_ROOT / "tests" / "manual") + os.pathsep + env.get("PYTHONPATH", "")
    return env


def _rewrite_fixture_team_repository_path(root: Path) -> None:
    manifest_path = root / ".isomer-labs" / "manifest.toml"
    manifest_text = manifest_path.read_text(encoding="utf-8")
    manifest_text = manifest_text.replace('path = "../../../.."', f'path = "{REPO_ROOT.as_posix()}"')
    manifest_path.write_text(manifest_text, encoding="utf-8")


def _run_json(root: Path, env: Mapping[str, str], args: list[str]) -> dict[str, Any]:
    command = [sys.executable, "-m", "isomer_labs", "--print-json", *args]
    completed = subprocess.run(command, cwd=root, env=env, text=True, capture_output=True, check=False)
    payload = None
    if completed.stdout.strip():
        payload = json.loads(completed.stdout)
    return {
        "status": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "json": payload,
    }


def _require(condition: bool, message: str, payload: object) -> None:
    if not condition:
        raise RuntimeError(f"{message}: {json.dumps(payload, indent=2, sort_keys=True)}")
