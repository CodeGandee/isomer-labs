"""Semantic payload checks and deterministic survey-process decisions."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Iterable, Literal, Mapping, Sequence


@dataclass(frozen=True)
class ContractDiagnostic:
    """One stable file-oriented semantic contract diagnostic."""

    code: str
    message: str
    location: str
    severity: Literal["error", "warning"] = "error"

    def to_json(self) -> dict[str, str]:
        return {
            "code": self.code,
            "message": self.message,
            "location": self.location,
            "severity": self.severity,
        }


def validate_structured_artifact(path: Path, semantic_id: str) -> tuple[dict[str, Any], list[ContractDiagnostic]]:
    """Load one structured Kaoju payload and validate its semantic invariants."""

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [ContractDiagnostic("kaoju_payload_unreadable", str(exc), "<file>")]
    if not isinstance(raw, dict):
        return {}, [ContractDiagnostic("kaoju_payload_invalid", "Payload must be a JSON object.", "<root>")]
    diagnostics: list[ContractDiagnostic] = []
    _require_string(raw, "title", diagnostics)
    _require_string(raw, "summary", diagnostics)
    if raw.get("artifact_family") != "kaoju":
        diagnostics.append(ContractDiagnostic("kaoju_family_invalid", "artifact_family must be 'kaoju'.", "artifact_family"))
    if raw.get("semantic_id") != semantic_id:
        diagnostics.append(ContractDiagnostic("kaoju_semantic_mismatch", f"semantic_id must be '{semantic_id}'.", "semantic_id"))
    if not isinstance(raw.get("sections"), dict):
        diagnostics.append(ContractDiagnostic("kaoju_sections_invalid", "sections must be an object.", "sections"))
        return raw, diagnostics
    validator = _SEMANTIC_VALIDATORS.get(semantic_id)
    if validator is not None:
        validator(raw, diagnostics)
    return raw, diagnostics


def direction_set_diagnostics(payload: Mapping[str, Any]) -> list[ContractDiagnostic]:
    diagnostics: list[ContractDiagnostic] = []
    _validate_direction_set(payload, diagnostics)
    return diagnostics


def reading_list_diagnostics(payload: Mapping[str, Any]) -> list[ContractDiagnostic]:
    diagnostics: list[ContractDiagnostic] = []
    _validate_reading_list(payload, diagnostics)
    return diagnostics


MATERIAL_TRIAL_FIELDS = (
    "source_commit",
    "environment_lock",
    "data_identity",
    "wrapper_semantics",
    "evaluator",
    "metrics",
    "resource_limits",
    "fidelity",
    "interpretation_policy",
)


def classify_trial_retry(
    prior_request: Mapping[str, Any],
    candidate_request: Mapping[str, Any],
    *,
    failure_class: str,
    attempts_completed: int,
    attempt_bound: int,
) -> dict[str, object]:
    """Classify retry authority without erasing a prior attempt."""

    if attempt_bound < 1:
        raise ValueError("Trial attempt bound must be positive.")
    changed = [field for field in MATERIAL_TRIAL_FIELDS if prior_request.get(field) != candidate_request.get(field)]
    if attempts_completed >= attempt_bound:
        return {"decision": "blocked", "reason": "attempt_bound_exhausted", "changed_fields": changed, "requires_gate": False}
    if changed:
        return {"decision": "revise_plan", "reason": "material_change", "changed_fields": changed, "requires_gate": True}
    if failure_class in {"timeout", "temporary_io", "service_unavailable", "preemption"}:
        return {"decision": "retry_identical", "reason": "transient_failure", "changed_fields": [], "requires_gate": False}
    return {"decision": "revise_plan", "reason": "non_transient_failure", "changed_fields": [], "requires_gate": True}


def choose_environment_strategy(
    requirements: Sequence[str],
    environments: Sequence[Mapping[str, Any]],
) -> dict[str, object]:
    """Apply the UC-09 reuse, add-to-existing, then create preference order."""

    required = {value.strip() for value in requirements if value.strip()}
    if not required:
        raise ValueError("At least one environment requirement is required.")
    normalized = sorted(environments, key=lambda item: (str(item.get("name")) != "default", str(item.get("name"))))
    for environment in normalized:
        installed = {str(value) for value in _sequence(environment.get("packages"))}
        if required <= installed and environment.get("usable", True):
            return {"strategy": "reuse", "environment": str(environment.get("name")), "constraints": {}, "reason": "existing environment satisfies every requirement"}
    for environment in normalized:
        if environment.get("usable", True) and environment.get("can_add", False):
            missing = sorted(required - {str(value) for value in _sequence(environment.get("packages"))})
            return {"strategy": "add", "environment": str(environment.get("name")), "constraints": {name: "*" for name in missing}, "reason": "compatible additions to preferred existing environment"}
    return {"strategy": "create", "environment": "kaoju-run", "constraints": {name: "*" for name in sorted(required)}, "reason": "no existing environment can be reused or safely extended"}


def _validate_direction_set(payload: Mapping[str, Any], diagnostics: list[ContractDiagnostic]) -> None:
    sections = _mapping(payload.get("sections"))
    proposals = _sequence(sections.get("proposals"))
    if not proposals:
        diagnostics.append(ContractDiagnostic("direction_proposals_missing", "At least one direction proposal is required.", "sections.proposals"))
        return
    proposal_ids: set[str] = set()
    required = ("id", "title", "research_question", "boundary", "source_classes", "coverage_date", "expected_depth", "deliverables", "empirical_feasibility")
    for index, candidate in enumerate(proposals):
        if not isinstance(candidate, dict):
            diagnostics.append(ContractDiagnostic("direction_invalid", "Direction proposal must be an object.", f"sections.proposals/{index}"))
            continue
        for field in required:
            value = candidate.get(field)
            if value is None or value == "" or value == []:
                diagnostics.append(ContractDiagnostic("direction_field_missing", f"Direction requires {field}.", f"sections.proposals/{index}/{field}"))
        direction_id = candidate.get("id")
        if isinstance(direction_id, str):
            if direction_id in proposal_ids:
                diagnostics.append(ContractDiagnostic("direction_id_duplicate", f"Duplicate direction id: {direction_id}", f"sections.proposals/{index}/id"))
            proposal_ids.add(direction_id)
        feasibility = candidate.get("empirical_feasibility")
        if feasibility not in {"available", "requires-environment-work", "requires-unavailable-hardware-or-service", "unknown"}:
            diagnostics.append(ContractDiagnostic("direction_feasibility_invalid", "Empirical feasibility must use the checked four-state vocabulary.", f"sections.proposals/{index}/empirical_feasibility"))
    selections = _sequence(sections.get("selections"))
    if not selections:
        diagnostics.append(ContractDiagnostic("direction_selection_missing", "At least one direction must be selected or custom-added.", "sections.selections"))
    unknown = sorted(str(value) for value in selections if str(value) not in proposal_ids)
    if unknown:
        diagnostics.append(ContractDiagnostic("direction_selection_unknown", f"Selections do not resolve to proposals: {', '.join(unknown)}", "sections.selections"))
    confirmation = _mapping(sections.get("confirmation"))
    if confirmation.get("status") != "accepted" or not confirmation.get("actor_ref"):
        diagnostics.append(ContractDiagnostic("direction_confirmation_missing", "Accepted direction state requires explicit actor confirmation.", "sections.confirmation"))
    if len(proposals) < 3:
        diagnostics.append(ContractDiagnostic("direction_default_short", "The default proposal set targets three directions; record why fewer were useful.", "sections.proposals", "warning"))


def _validate_reading_list(payload: Mapping[str, Any], diagnostics: list[ContractDiagnostic]) -> None:
    sections = _mapping(payload.get("sections"))
    direction_id = sections.get("direction_id")
    if not isinstance(direction_id, str) or not direction_id:
        diagnostics.append(ContractDiagnostic("reading_direction_missing", "A reading list requires exactly one direction_id.", "sections.direction_id"))
    items = _sequence(sections.get("items"))
    ids: set[str] = set()
    reachable = {"priority": 0, "secondary": 0}
    source_classes: set[str] = set()
    reachable_version_families: dict[str, int] = {}
    required = ("item_id", "title", "source_type", "urls", "summary", "relevance_rationale", "estimated_depth", "query_provenance", "status", "priority", "version_family")
    for index, candidate in enumerate(items):
        if not isinstance(candidate, dict):
            diagnostics.append(ContractDiagnostic("reading_item_invalid", "Reading-list item must be an object.", f"sections.items/{index}"))
            continue
        for field in required:
            value = candidate.get(field)
            if value is None or value == "" or value == []:
                diagnostics.append(ContractDiagnostic("reading_item_field_missing", f"Reading-list item requires {field}.", f"sections.items/{index}/{field}"))
        item_id = candidate.get("item_id")
        if isinstance(item_id, str):
            if item_id in ids:
                diagnostics.append(ContractDiagnostic("reading_item_duplicate", f"Duplicate item_id: {item_id}", f"sections.items/{index}/item_id"))
            ids.add(item_id)
        source_type = candidate.get("source_type")
        if isinstance(source_type, str):
            source_classes.add(source_type)
        priority = candidate.get("priority")
        if priority not in {"priority", "secondary"}:
            diagnostics.append(ContractDiagnostic("reading_priority_invalid", "priority must be priority or secondary.", f"sections.items/{index}/priority"))
        if candidate.get("status") in {"planned", "human-added"} and priority in reachable:
            reachable[str(priority)] += 1
            version_family = candidate.get("version_family")
            if isinstance(version_family, str):
                previous = reachable_version_families.get(version_family)
                if previous is not None:
                    diagnostics.append(ContractDiagnostic("reading_version_duplicate", f"Reachable items {previous} and {index} belong to the same version family; select one and mark the other duplicate or excluded.", f"sections.items/{index}/version_family"))
                else:
                    reachable_version_families[version_family] = index
        if candidate.get("status") == "blocked" and not candidate.get("blocker_reason"):
            diagnostics.append(ContractDiagnostic("reading_blocker_reason_missing", "Blocked items require a reason and recovery route.", f"sections.items/{index}/blocker_reason"))
        provenance = _mapping(candidate.get("query_provenance"))
        if not any(provenance.get(field) not in (None, "") for field in ("query", "seed")):
            diagnostics.append(ContractDiagnostic("reading_query_missing", "Query provenance requires the query text or seed.", f"sections.items/{index}/query_provenance"))
        if not any(provenance.get(field) not in (None, "") for field in ("provider", "access_method")):
            diagnostics.append(ContractDiagnostic("reading_provider_missing", "Query provenance requires the provider or access method.", f"sections.items/{index}/query_provenance"))
        for field in ("route", "searched_through"):
            if provenance.get(field) in (None, ""):
                diagnostics.append(ContractDiagnostic("reading_provenance_incomplete", f"Query provenance requires {field}.", f"sections.items/{index}/query_provenance/{field}"))
    for priority, target in (("priority", 3), ("secondary", 3)):
        if reachable[priority] < target:
            diagnostics.append(ContractDiagnostic("reading_target_short", f"Reachable {priority} items are below the default target of {target}; preserve a coverage warning.", "sections.items", "warning"))
    if not source_classes.intersection({"paper", "technical_report"}):
        diagnostics.append(ContractDiagnostic("reading_primary_work_missing", "Papers or technical reports must anchor related-work coverage.", "sections.items"))
    approval = _mapping(sections.get("approval"))
    if approval.get("status") == "approved" and not approval.get("actor_ref"):
        diagnostics.append(ContractDiagnostic("reading_approval_actor_missing", "Approved reading lists require an actor ref.", "sections.approval.actor_ref"))


def _validate_source_digest(payload: Mapping[str, Any], diagnostics: list[ContractDiagnostic]) -> None:
    sections = _mapping(payload.get("sections"))
    if not isinstance(sections.get("source_identity"), dict):
        diagnostics.append(ContractDiagnostic("source_identity_missing", "Source Digest requires a resolved source identity and version family.", "sections.source_identity"))
    findings = _sequence(sections.get("findings"))
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            continue
        if finding.get("source_class") == "repository":
            for field in ("repository_ref", "commit", "file", "line_start", "line_end"):
                if finding.get(field) in (None, ""):
                    diagnostics.append(ContractDiagnostic("code_locator_incomplete", f"Code finding requires {field}.", f"sections.findings/{index}/{field}"))
            commit = finding.get("commit")
            if not isinstance(commit, str) or len(commit) != 40 or any(character not in "0123456789abcdefABCDEF" for character in commit):
                diagnostics.append(ContractDiagnostic("code_commit_invalid", "Code finding requires a full immutable repository commit.", f"sections.findings/{index}/commit"))
        elif not finding.get("locator"):
            diagnostics.append(ContractDiagnostic("paper_locator_missing", "Paper or report findings require an exact page, section, figure, or table locator.", f"sections.findings/{index}/locator"))
        if not finding.get("source_statement") or not finding.get("interpretation"):
            diagnostics.append(ContractDiagnostic("finding_boundary_missing", "Keep the source statement distinct from interpretation.", f"sections.findings/{index}"))
    approval = _mapping(sections.get("approval"))
    if approval.get("status") not in {"pending", "approved", "rejected"}:
        diagnostics.append(ContractDiagnostic("source_digest_approval_missing", "Source Digest requires pending, approved, or rejected review state.", "sections.approval.status"))
    elif approval.get("status") in {"approved", "rejected"} and approval.get("actor_ref") in (None, ""):
        diagnostics.append(ContractDiagnostic("source_digest_approval_actor_missing", "A decided Source Digest review requires an actor ref.", "sections.approval.actor_ref"))


def _validate_env_plan(payload: Mapping[str, Any], diagnostics: list[ContractDiagnostic]) -> None:
    sections = _mapping(payload.get("sections"))
    for field in ("dependencies", "critical_path", "candidates", "authorization", "expected_smoke_outputs"):
        if sections.get(field) in (None, "", [], {}):
            diagnostics.append(ContractDiagnostic("env_plan_field_missing", f"Environment preparation plan requires {field}.", f"sections.{field}"))
    if "risks" not in sections or not isinstance(sections.get("risks"), list):
        diagnostics.append(ContractDiagnostic("env_plan_field_missing", "Environment preparation plan requires an explicit risks list.", "sections.risks"))
    critical_path = _mapping(sections.get("critical_path"))
    for field in ("source_ref", "repository_ref", "task_critical_path"):
        if critical_path.get(field) in (None, "", []):
            diagnostics.append(ContractDiagnostic("env_critical_path_incomplete", f"Environment critical path requires {field}.", f"sections.critical_path.{field}"))
    authorization = _mapping(sections.get("authorization"))
    if authorization.get("status") not in {"pending", "approved", "rejected"}:
        diagnostics.append(ContractDiagnostic("env_authorization_invalid", "Environment plan authorization must be pending, approved, or rejected.", "sections.authorization.status"))
    if authorization.get("status") in {"approved", "rejected"} and authorization.get("actor_ref") in (None, ""):
        diagnostics.append(ContractDiagnostic("env_authorization_actor_missing", "A decided environment plan requires an actor ref.", "sections.authorization.actor_ref"))


def _validate_trial_plan(payload: Mapping[str, Any], diagnostics: list[ContractDiagnostic]) -> None:
    sections = _mapping(payload.get("sections"))
    if sections.get("trial_id") in (None, ""):
        diagnostics.append(ContractDiagnostic("trial_plan_field_missing", "Trial plan requires trial_id.", "sections.trial_id"))
    for field in ("prerequisites", "wrapper", "evaluation", "authorization"):
        if sections.get(field) in (None, "", [], {}):
            diagnostics.append(ContractDiagnostic("trial_plan_field_missing", f"Trial plan requires {field}.", f"sections.{field}"))
    prerequisites = _mapping(sections.get("prerequisites"))
    for field in ("source_ref", "repository_ref", "source_commit", "data_strategy", "pixi_env_ref"):
        if prerequisites.get(field) in (None, "", []):
            diagnostics.append(ContractDiagnostic("trial_prerequisite_missing", f"Trial prerequisites require {field}.", f"sections.prerequisites.{field}"))
    if prerequisites.get("data_strategy") not in {"dataset_path", "random_data"}:
        diagnostics.append(ContractDiagnostic("trial_data_strategy_invalid", "data_strategy must be dataset_path or random_data.", "sections.prerequisites.data_strategy"))
    elif prerequisites.get("data_strategy") == "dataset_path" and prerequisites.get("dataset_path") in (None, ""):
        diagnostics.append(ContractDiagnostic("trial_dataset_path_missing", "dataset_path strategy requires an authorized dataset path.", "sections.prerequisites.dataset_path"))
    elif prerequisites.get("data_strategy") == "random_data" and prerequisites.get("generated_dataset_ref") in (None, ""):
        diagnostics.append(ContractDiagnostic("trial_generated_dataset_missing", "random_data strategy requires a generated-dataset ref.", "sections.prerequisites.generated_dataset_ref"))
    wrapper = _mapping(sections.get("wrapper"))
    for field in ("artifact_ref", "run_command", "fidelity"):
        if wrapper.get(field) in (None, "", []):
            diagnostics.append(ContractDiagnostic("trial_wrapper_missing", f"Trial wrapper requires {field}.", f"sections.wrapper.{field}"))
    evaluation = _mapping(sections.get("evaluation"))
    for field in ("evaluator", "metrics", "expected_outputs", "limitations"):
        if evaluation.get(field) in (None, "", []):
            diagnostics.append(ContractDiagnostic("trial_evaluation_missing", f"Trial evaluation requires {field}.", f"sections.evaluation.{field}"))
    authorization = _mapping(sections.get("authorization"))
    if not isinstance(authorization.get("attempt_bound"), int) or int(authorization.get("attempt_bound", 0)) < 1:
        diagnostics.append(ContractDiagnostic("trial_attempt_bound_invalid", "Trial authorization requires a positive attempt_bound.", "sections.authorization.attempt_bound"))
    if authorization.get("resource_limits") in (None, "", [], {}):
        diagnostics.append(ContractDiagnostic("trial_resource_limit_missing", "Trial authorization requires resource_limits.", "sections.authorization.resource_limits"))
    gate = _mapping(authorization.get("human_gate"))
    if gate.get("status") not in {"pending", "approved", "rejected"}:
        diagnostics.append(ContractDiagnostic("trial_gate_missing", "Trial plan requires a pending, approved, or rejected human Gate.", "sections.authorization.human_gate"))
    elif gate.get("status") in {"approved", "rejected"} and gate.get("actor_ref") in (None, ""):
        diagnostics.append(ContractDiagnostic("trial_gate_actor_missing", "A decided trial Gate requires an actor ref.", "sections.authorization.human_gate.actor_ref"))


def _validate_generated_dataset(payload: Mapping[str, Any], diagnostics: list[ContractDiagnostic]) -> None:
    sections = _mapping(payload.get("sections"))
    if sections.get("purpose") != "capability-probe":
        diagnostics.append(ContractDiagnostic("generated_dataset_purpose_invalid", "Random-data trial inputs must use purpose 'capability-probe'.", "sections.purpose"))
    if sections.get("verification_depth") not in {"execution-only", "behavior-observed"}:
        diagnostics.append(ContractDiagnostic("generated_dataset_depth_invalid", "Generated-data evidence cannot claim stronger than executed verification depth.", "sections.verification_depth"))
    for field in ("generator", "outputs", "checks", "limitations"):
        if sections.get(field) in (None, "", [], {}):
            diagnostics.append(ContractDiagnostic("generated_dataset_field_missing", f"Generated Dataset requires {field}.", f"sections.{field}"))


def _validate_associated_source_code(payload: Mapping[str, Any], diagnostics: list[ContractDiagnostic]) -> None:
    sections = _mapping(payload.get("sections"))
    for field in ("source", "repository", "relationship"):
        if sections.get(field) in (None, "", [], {}):
            diagnostics.append(ContractDiagnostic("associated_source_field_missing", f"Associated Source Code requires {field}.", f"sections.{field}"))
    repository = _mapping(sections.get("repository"))
    commit = repository.get("commit")
    if not isinstance(commit, str) or len(commit) != 40 or any(character not in "0123456789abcdefABCDEF" for character in commit):
        diagnostics.append(ContractDiagnostic("associated_source_commit_invalid", "Associated Source Code requires a full immutable repository commit.", "sections.repository.commit"))
    relationship = _mapping(sections.get("relationship"))
    if relationship.get("status") not in {"verified", "candidate", "rejected", "blocked"}:
        diagnostics.append(ContractDiagnostic("associated_source_status_invalid", "Relationship status must be verified, candidate, rejected, or blocked.", "sections.relationship.status"))


def _validate_artifact_library(payload: Mapping[str, Any], diagnostics: list[ContractDiagnostic]) -> None:
    materials = _sequence(_mapping(payload.get("sections")).get("materials"))
    if not materials:
        diagnostics.append(ContractDiagnostic("artifact_library_empty", "Artifact Library requires at least one registered material.", "sections.materials"))
    for index, material in enumerate(materials):
        if not isinstance(material, dict):
            diagnostics.append(ContractDiagnostic("artifact_library_entry_invalid", "Artifact Library entry must be an object.", f"sections.materials/{index}"))
            continue
        for field in ("material_id", "source_identity", "source_class", "content_ref", "status", "provenance_refs"):
            if material.get(field) in (None, "", [], {}):
                diagnostics.append(ContractDiagnostic("artifact_library_field_missing", f"Artifact Library entry requires {field}.", f"sections.materials/{index}/{field}"))


def _validate_env_gate_revision(payload: Mapping[str, Any], diagnostics: list[ContractDiagnostic]) -> None:
    sections = _mapping(payload.get("sections"))
    for field in ("before", "after", "decision"):
        if sections.get(field) in (None, "", [], {}):
            diagnostics.append(ContractDiagnostic("env_gate_field_missing", f"Environment Gate revision requires {field}.", f"sections.{field}"))


def _validate_pixi_env_ref(payload: Mapping[str, Any], diagnostics: list[ContractDiagnostic]) -> None:
    sections = _mapping(payload.get("sections"))
    for field in ("intent_constraints", "resolved_packages", "lock"):
        if sections.get(field) in (None, "", [], {}):
            diagnostics.append(ContractDiagnostic("pixi_env_field_missing", f"Pixi environment ref requires {field}.", f"sections.{field}"))
    lock = _mapping(sections.get("lock"))
    if lock.get("identity") in (None, "") or lock.get("status") not in {"resolved", "ready"}:
        diagnostics.append(ContractDiagnostic("pixi_lock_invalid", "Pixi environment ref requires a resolved lock identity.", "sections.lock"))


def _validate_smoke_result(payload: Mapping[str, Any], diagnostics: list[ContractDiagnostic]) -> None:
    sections = _mapping(payload.get("sections"))
    execution = _mapping(sections.get("execution"))
    observation = _mapping(sections.get("observation"))
    for field in ("command_request_ref", "run_ref", "script_ref", "pixi_env_ref"):
        if execution.get(field) in (None, ""):
            diagnostics.append(ContractDiagnostic("smoke_execution_field_missing", f"Smoke execution requires {field}.", f"sections.execution.{field}"))
    for field in ("status", "task_critical_check", "logs"):
        if observation.get(field) in (None, "", []):
            diagnostics.append(ContractDiagnostic("smoke_observation_field_missing", f"Smoke observation requires {field}.", f"sections.observation.{field}"))
    if observation.get("environment_ready") is True and (observation.get("status") != "passed" or observation.get("task_critical_check") != "passed"):
        diagnostics.append(ContractDiagnostic("smoke_readiness_invalid", "Environment readiness requires a passed task-critical smoke observation.", "sections.observation.environment_ready"))


def _validate_trial_run(payload: Mapping[str, Any], diagnostics: list[ContractDiagnostic]) -> None:
    sections = _mapping(payload.get("sections"))
    execution = _mapping(sections.get("execution"))
    results = _mapping(sections.get("results"))
    for field in ("command_request_ref", "source_commit", "pixi_env_ref", "environment_lock", "data_ref", "wrapper_ref", "logs", "outputs", "timing", "resources", "adaptations", "terminal_status"):
        if execution.get(field) in (None, "", [], {}):
            diagnostics.append(ContractDiagnostic("trial_run_field_missing", f"Method Trial Run requires {field}.", f"sections.execution.{field}"))
    if results.get("checks") in (None, "", [], {}) or results.get("metrics") in (None, "", [], {}):
        diagnostics.append(ContractDiagnostic("trial_run_results_missing", "Method Trial Run requires checks and metrics.", "sections.results"))


def _validate_trial_result(payload: Mapping[str, Any], diagnostics: list[ContractDiagnostic]) -> None:
    sections = _mapping(payload.get("sections"))
    execution = _mapping(sections.get("execution"))
    results = _mapping(sections.get("results"))
    verdict = _mapping(sections.get("verdict"))
    if execution.get("trial_run_ref") in (None, "") or execution.get("input_basis") in (None, ""):
        diagnostics.append(ContractDiagnostic("trial_result_execution_missing", "Method Trial Result requires trial_run_ref and input_basis.", "sections.execution"))
    if results.get("checks") in (None, "", [], {}) or results.get("metrics") in (None, "", [], {}):
        diagnostics.append(ContractDiagnostic("trial_result_values_missing", "Method Trial Result requires checks and metrics.", "sections.results"))
    for field in ("status", "depth", "fidelity", "adaptations"):
        if verdict.get(field) in (None, "", []):
            diagnostics.append(ContractDiagnostic("trial_result_verdict_missing", f"Method Trial Result verdict requires {field}.", f"sections.verdict.{field}"))
    if sections.get("limitations") in (None, "", []):
        diagnostics.append(ContractDiagnostic("trial_result_limitations_missing", "Method Trial Result requires explicit limitations.", "sections.limitations"))
    if execution.get("input_basis") in {"random_data", "generated_data"}:
        if execution.get("run_purpose") != "capability-probe":
            diagnostics.append(ContractDiagnostic("trial_result_purpose_invalid", "Generated-data trial results require run_purpose capability-probe.", "sections.execution.run_purpose"))
        if verdict.get("depth") not in {"execution-only", "behavior-observed", "executed"}:
            diagnostics.append(ContractDiagnostic("trial_result_depth_invalid", "Generated-data trial results cannot claim stronger than executed verification depth.", "sections.verdict.depth"))


_SEMANTIC_VALIDATORS = {
    "kaoju:direction-set": _validate_direction_set,
    "kaoju:reading-list": _validate_reading_list,
    "kaoju:source-digest": _validate_source_digest,
    "kaoju:env-prep-plan": _validate_env_plan,
    "kaoju:env-gate-revision": _validate_env_gate_revision,
    "kaoju:pixi-env-ref": _validate_pixi_env_ref,
    "kaoju:smoke-run-result": _validate_smoke_result,
    "kaoju:method-trial-plan": _validate_trial_plan,
    "kaoju:method-trial-run": _validate_trial_run,
    "kaoju:method-trial-result": _validate_trial_result,
    "kaoju:generated-dataset": _validate_generated_dataset,
    "kaoju:associated-source-code": _validate_associated_source_code,
    "kaoju:artifact-library": _validate_artifact_library,
}


def _require_string(payload: Mapping[str, Any], field: str, diagnostics: list[ContractDiagnostic]) -> None:
    if not isinstance(payload.get(field), str) or not str(payload.get(field)).strip():
        diagnostics.append(ContractDiagnostic("kaoju_display_field_missing", f"{field} must be a non-empty string.", field))


def _mapping(value: object) -> Mapping[str, Any]:
    return value if isinstance(value, dict) else {}


def _sequence(value: object) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return []


def diagnostic_errors(diagnostics: Iterable[ContractDiagnostic]) -> list[ContractDiagnostic]:
    return [diagnostic for diagnostic in diagnostics if diagnostic.severity == "error"]
