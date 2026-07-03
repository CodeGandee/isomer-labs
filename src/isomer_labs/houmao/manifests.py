"""Houmao adapter JSON manifests and reconciliation helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import subprocess
from typing import Iterable, Mapping

from isomer_labs.core.diagnostics import Diagnostic
from isomer_labs.project import houmao_project_dir_for_root
from isomer_labs.runtime.models import utc_timestamp


HOUMAO_ADAPTER_ID = "houmao"
HOUMAO_EXECUTION_ADAPTER_REF = "execution-adapter:houmao"
HOUMAO_MANIFEST_SCHEMA_VERSION = "isomer-houmao-adapter-manifest.v1"
ADAPTER_MANIFEST_ROOT = "runtime/adapters/houmao"
ADAPTER_LINK_FILENAME = "adapter-link.json"
LAUNCH_MATERIAL_FILENAME = "launch-material-manifest.json"
ADAPTER_RUNTIME_FILENAME = "adapter-runtime-manifest.json"

SECRET_FIELD_RE = re.compile(
    r"(api[_-]?key|access[_-]?key|secret|token|password|credential|private[_-]?key)",
    re.IGNORECASE,
)


class ManifestValidationError(ValueError):
    """Raised when a Houmao adapter manifest cannot be trusted."""


class ManifestKind(str, Enum):
    ADAPTER_LINK = "adapter_link"
    LAUNCH_MATERIAL = "launch_material"
    ADAPTER_RUNTIME = "adapter_runtime"


class ReconciliationState(str, Enum):
    LINKED = "linked"
    LAUNCHED_BY_ISOMER = "launched_by_isomer"
    EXTERNAL_DETECTED = "external_detected"
    ADOPTED = "adopted"
    DRIFTED = "drifted"
    CONFLICTED = "conflicted"
    STALE = "stale"
    REJECTED = "rejected"


class MappingConfidence(str, Enum):
    EXACT = "exact"
    NAME_MATCH = "name_match"
    MANIFEST_MATCH = "manifest_match"
    MANUAL = "manual"
    UNMAPPED = "unmapped"
    CONFLICT = "conflict"


@dataclass(frozen=True)
class ManifestPaths:
    root: Path
    adapter_link: Path
    launch_material: Path
    adapter_runtime: Path

    def to_json(self) -> dict[str, object]:
        return {
            "root": str(self.root),
            "adapter_link": str(self.adapter_link),
            "launch_material": str(self.launch_material),
            "adapter_runtime": str(self.adapter_runtime),
        }


@dataclass(frozen=True)
class AgentBinding:
    agent_instance_id: str
    agent_role_id: str | None = None
    houmao_profile: str | None = None
    houmao_agent_name: str | None = None
    houmao_managed_agent_id: str | None = None
    mapping_confidence: str = MappingConfidence.UNMAPPED.value

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "agent_instance_id": self.agent_instance_id,
            "mapping_confidence": self.mapping_confidence,
        }
        for key, value in (
            ("agent_role_id", self.agent_role_id),
            ("houmao_profile", self.houmao_profile),
            ("houmao_agent_name", self.houmao_agent_name),
            ("houmao_managed_agent_id", self.houmao_managed_agent_id),
        ):
            if value is not None:
                data[key] = value
        return data


@dataclass(frozen=True)
class MaterialFileRef:
    path: str
    digest: str
    source: str
    editable_policy: str
    agent_instance_id: str | None = None
    kind: str | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "path": self.path,
            "digest": self.digest,
            "source": self.source,
            "editable_policy": self.editable_policy,
        }
        if self.agent_instance_id is not None:
            data["agent_instance_id"] = self.agent_instance_id
        if self.kind is not None:
            data["kind"] = self.kind
        return data


@dataclass(frozen=True)
class ReconciliationResult:
    state: str
    mapping_confidence: str
    manifest_digest_summary: dict[str, object]
    live_observation_summary: dict[str, object]
    diagnostics: list[Diagnostic] = field(default_factory=list)
    agent_bindings: list[dict[str, object]] = field(default_factory=list)
    material_drift: list[dict[str, object]] = field(default_factory=list)
    manifest_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        return {
            "state": self.state,
            "mapping_confidence": self.mapping_confidence,
            "manifest_digest_summary": self.manifest_digest_summary,
            "live_observation_summary": self.live_observation_summary,
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
            "agent_bindings": self.agent_bindings,
            "material_drift": self.material_drift,
            "manifest_refs": self.manifest_refs,
        }


def manifest_paths(topic_workspace_path: Path, agent_team_instance_id: str) -> ManifestPaths:
    root = topic_workspace_path / ADAPTER_MANIFEST_ROOT / agent_team_instance_id
    return ManifestPaths(
        root=root,
        adapter_link=root / ADAPTER_LINK_FILENAME,
        launch_material=root / LAUNCH_MATERIAL_FILENAME,
        adapter_runtime=root / ADAPTER_RUNTIME_FILENAME,
    )


def adapter_manifest_path_plan_surface(agent_team_instance_id: str, manifest_kind: str) -> str:
    return f"adapter_manifest:{HOUMAO_ADAPTER_ID}:{agent_team_instance_id}:{manifest_kind}"


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def canonical_json_digest(value: object) -> str:
    return f"sha256:{sha256(canonical_json_bytes(value)).hexdigest()}"


def file_digest(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def write_json_manifest(path: Path, manifest: Mapping[str, object], *, expected_kind: str) -> str:
    validate_manifest_payload(manifest, expected_kind=expected_kind)
    reject_secret_material(manifest)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return canonical_json_digest(manifest)


def load_json_manifest(path: Path, *, expected_kind: str) -> dict[str, object]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ManifestValidationError(f"Manifest does not exist: {path}.") from exc
    except json.JSONDecodeError as exc:
        raise ManifestValidationError(f"Manifest is not valid JSON: {path}.") from exc
    if not isinstance(raw, dict):
        raise ManifestValidationError(f"Manifest root must be a JSON object: {path}.")
    validate_manifest_payload(raw, expected_kind=expected_kind)
    reject_secret_material(raw)
    return raw


def validate_manifest_payload(manifest: Mapping[str, object], *, expected_kind: str) -> None:
    observed_kind = manifest.get("manifest_kind")
    if observed_kind != expected_kind:
        raise ManifestValidationError(f"Expected manifest kind {expected_kind}, found {observed_kind}.")
    schema_version = manifest.get("schema_version")
    if schema_version != HOUMAO_MANIFEST_SCHEMA_VERSION:
        raise ManifestValidationError(
            f"Expected manifest schema {HOUMAO_MANIFEST_SCHEMA_VERSION}, found {schema_version}."
        )
    adapter_id = manifest.get("adapter_id")
    if adapter_id != HOUMAO_ADAPTER_ID:
        raise ManifestValidationError(f"Expected adapter id {HOUMAO_ADAPTER_ID}, found {adapter_id}.")


def secret_paths(value: object, *, prefix: str = "$") -> list[str]:
    paths: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_text = str(key)
            child_prefix = f"{prefix}.{key_text}"
            if SECRET_FIELD_RE.search(key_text):
                paths.append(child_prefix)
            paths.extend(secret_paths(item, prefix=child_prefix))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            paths.extend(secret_paths(item, prefix=f"{prefix}[{index}]"))
    return paths


def reject_secret_material(value: object) -> None:
    paths = secret_paths(value)
    if paths:
        raise ManifestValidationError(
            "Manifest payload contains secret-like field(s): " + ", ".join(sorted(paths))
        )


def redact_payload(value: object) -> object:
    if isinstance(value, Mapping):
        redacted: dict[str, object] = {}
        for key, item in value.items():
            key_text = str(key)
            redacted[key_text] = "[REDACTED]" if SECRET_FIELD_RE.search(key_text) else redact_payload(item)
        return redacted
    if isinstance(value, list):
        return [redact_payload(item) for item in value]
    return value


def build_adapter_link_manifest(
    *,
    project_root: Path,
    research_topic_id: str,
    topic_workspace_id: str,
    topic_workspace_path: Path,
    agent_team_instance_id: str,
    topic_agent_team_profile_id: str,
    domain_agent_team_template_id: str,
    agent_bindings: list[AgentBinding],
    houmao_project_dir: Path | None,
    actor_ref: str | None,
    operator_provenance: Mapping[str, object] | None = None,
    created_at: str | None = None,
) -> dict[str, object]:
    timestamp = created_at or utc_timestamp()
    manifest: dict[str, object] = {
        "schema_version": HOUMAO_MANIFEST_SCHEMA_VERSION,
        "manifest_kind": ManifestKind.ADAPTER_LINK.value,
        "adapter_id": HOUMAO_ADAPTER_ID,
        "execution_adapter_ref": HOUMAO_EXECUTION_ADAPTER_REF,
        "created_at": timestamp,
        "updated_at": timestamp,
        "actor_ref": actor_ref,
        "project": {
            "root": str(project_root.resolve(strict=False)),
            "research_topic_id": research_topic_id,
            "topic_workspace_id": topic_workspace_id,
            "topic_workspace_path": str(topic_workspace_path.resolve(strict=False)),
        },
        "agent_team_instance": {
            "id": agent_team_instance_id,
            "topic_agent_team_profile_id": topic_agent_team_profile_id,
            "domain_agent_team_template_id": domain_agent_team_template_id,
        },
        "houmao": {
            "project_dir": str((houmao_project_dir or houmao_project_dir_for_root(project_root)).resolve(strict=False)),
        },
        "agent_bindings": [binding.to_json() for binding in agent_bindings],
        "provenance_refs": [
            f"provenance:houmao-adapter-link:{agent_team_instance_id}",
        ],
    }
    if operator_provenance:
        manifest["operator_provenance"] = dict(operator_provenance)
    return manifest


def build_launch_material_manifest(
    *,
    link_manifest: Mapping[str, object],
    material_files: list[MaterialFileRef],
    source: str,
    created_at: str | None = None,
) -> dict[str, object]:
    timestamp = created_at or utc_timestamp()
    return {
        "schema_version": HOUMAO_MANIFEST_SCHEMA_VERSION,
        "manifest_kind": ManifestKind.LAUNCH_MATERIAL.value,
        "adapter_id": HOUMAO_ADAPTER_ID,
        "created_at": timestamp,
        "updated_at": timestamp,
        "source": source,
        "link_manifest_digest": canonical_json_digest(link_manifest),
        "project": link_manifest.get("project", {}),
        "agent_team_instance": link_manifest.get("agent_team_instance", {}),
        "operator_provenance": link_manifest.get("operator_provenance", {}),
        "files": [item.to_json() for item in material_files],
        "provenance_refs": [
            f"provenance:houmao-launch-material:{_manifest_team_id(link_manifest)}",
        ],
    }


def build_adapter_runtime_manifest(
    *,
    link_manifest: Mapping[str, object],
    result: ReconciliationResult,
    source_mode: str,
    observed_at: str | None = None,
) -> dict[str, object]:
    timestamp = observed_at or utc_timestamp()
    return {
        "schema_version": HOUMAO_MANIFEST_SCHEMA_VERSION,
        "manifest_kind": ManifestKind.ADAPTER_RUNTIME.value,
        "adapter_id": HOUMAO_ADAPTER_ID,
        "created_at": timestamp,
        "updated_at": timestamp,
        "source_mode": source_mode,
        "project": link_manifest.get("project", {}),
        "agent_team_instance": link_manifest.get("agent_team_instance", {}),
        "reconciliation": result.to_json(),
        "houmao": result.live_observation_summary,
        "agent_bindings": result.agent_bindings,
        "provenance_refs": [
            f"provenance:houmao-adapter-runtime:{_manifest_team_id(link_manifest)}:{timestamp}",
        ],
    }


def reconcile_houmao_manifests(
    *,
    link_manifest: Mapping[str, object] | None,
    launch_material_manifest: Mapping[str, object] | None = None,
    runtime_manifest: Mapping[str, object] | None = None,
    live_state: Mapping[str, object] | None = None,
    material_base_dir: Path | None = None,
    adopt: bool = False,
) -> ReconciliationResult:
    diagnostics: list[Diagnostic] = []
    if link_manifest is None:
        diagnostics.append(
            Diagnostic(
                code="ISO060",
                severity="error",
                concept="Houmao adapter reconciliation",
                message="Adapter link manifest is required before reconciliation.",
            )
        )
        return ReconciliationResult(
            state=ReconciliationState.REJECTED.value,
            mapping_confidence=MappingConfidence.UNMAPPED.value,
            manifest_digest_summary={},
            live_observation_summary={},
            diagnostics=diagnostics,
        )

    manifest_digest_summary = _manifest_digest_summary(
        link_manifest=link_manifest,
        launch_material_manifest=launch_material_manifest,
        runtime_manifest=runtime_manifest,
    )
    material_drift = _material_drift(launch_material_manifest, material_base_dir)
    agent_bindings = _as_dict_list(link_manifest.get("agent_bindings"))
    live_summary = _live_summary(live_state)
    conflicts = _mapping_conflicts(agent_bindings, live_summary.get("agents", []))

    if material_drift:
        diagnostics.append(
            Diagnostic(
                code="ISO061",
                severity="warning",
                concept="Houmao adapter reconciliation",
                message="Referenced Houmao launch material has drifted.",
            )
        )
    if conflicts:
        diagnostics.append(
            Diagnostic(
                code="ISO062",
                severity="error",
                concept="Houmao adapter reconciliation",
                message="Agent Instance to Houmao managed-agent mapping is conflicted.",
            )
        )

    state = ReconciliationState.LINKED.value
    mapping_confidence = _mapping_confidence(agent_bindings, live_summary.get("agents", []))
    if conflicts:
        state = ReconciliationState.CONFLICTED.value
        mapping_confidence = MappingConfidence.CONFLICT.value
    elif material_drift:
        state = ReconciliationState.DRIFTED.value
    elif adopt:
        state = ReconciliationState.ADOPTED.value
        if mapping_confidence == MappingConfidence.UNMAPPED.value:
            mapping_confidence = MappingConfidence.MANUAL.value
    elif _runtime_source_mode(runtime_manifest) == "isomer_quick_launch":
        state = ReconciliationState.LAUNCHED_BY_ISOMER.value
    elif live_summary.get("agents"):
        state = ReconciliationState.EXTERNAL_DETECTED.value

    return ReconciliationResult(
        state=state,
        mapping_confidence=mapping_confidence,
        manifest_digest_summary=manifest_digest_summary,
        live_observation_summary=live_summary,
        diagnostics=diagnostics,
        agent_bindings=agent_bindings,
        material_drift=material_drift,
        manifest_refs=_manifest_refs(link_manifest, launch_material_manifest, runtime_manifest),
    )


def collect_houmao_read_only_state(
    *,
    houmao_project_dir: Path | None,
    houmao_mgr: str = "houmao-mgr",
) -> tuple[dict[str, object], list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    executable = shutil.which(houmao_mgr)
    if executable is None:
        diagnostics.append(
            Diagnostic(
                code="ISO063",
                severity="warning",
                concept="Houmao adapter reconciliation",
                field="houmao-mgr",
                message="houmao-mgr is not available; reconciliation will use manifest-only observations.",
            )
        )
        return {"available": False, "agents": [], "commands": []}, diagnostics

    commands: list[dict[str, object]] = []
    state: dict[str, object] = {"available": True, "agents": [], "commands": commands}
    command_specs: list[list[str]] = []
    if houmao_project_dir is not None:
        command_specs.append(
            [executable, "--print-json", "project", "--project-dir", str(houmao_project_dir), "status"]
        )
    command_specs.append([executable, "--print-json", "agents", "global", "list"])
    for args in command_specs:
        try:
            completed = subprocess.run(args, check=False, capture_output=True, text=True, timeout=20)
        except (OSError, subprocess.TimeoutExpired) as exc:
            diagnostics.append(
                Diagnostic(
                    code="ISO063",
                    severity="warning",
                    concept="Houmao adapter reconciliation",
                    message=f"Houmao read-only command failed before completion: {exc}.",
                )
            )
            continue
        command_payload = {
            "args": args,
            "returncode": completed.returncode,
            "stdout": _parse_json_or_text(completed.stdout),
            "stderr": completed.stderr.strip(),
        }
        redacted_command = redact_payload(command_payload)
        commands.append(redacted_command if isinstance(redacted_command, dict) else command_payload)
        if completed.returncode != 0:
            diagnostics.append(
                Diagnostic(
                    code="ISO063",
                    severity="warning",
                    concept="Houmao adapter reconciliation",
                    message="Houmao read-only command returned a non-zero status.",
                )
            )
    state["agents"] = _agents_from_command_payloads(commands)
    return state, diagnostics


def _parse_json_or_text(value: str) -> object:
    stripped = value.strip()
    if not stripped:
        return None
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        return stripped


def _agents_from_command_payloads(commands: list[dict[str, object]]) -> list[dict[str, object]]:
    agents: list[dict[str, object]] = []
    for command in commands:
        stdout = command.get("stdout")
        if isinstance(stdout, dict):
            for key in ("agents", "managed_agents", "records"):
                maybe_agents = stdout.get(key)
                if isinstance(maybe_agents, list):
                    agents.extend(item for item in maybe_agents if isinstance(item, dict))
        elif isinstance(stdout, list):
            agents.extend(item for item in stdout if isinstance(item, dict))
    return _deduplicate_agent_records(agents)


def _deduplicate_agent_records(agents: list[dict[str, object]]) -> list[dict[str, object]]:
    deduplicated: list[dict[str, object]] = []
    seen: set[str] = set()
    for agent in agents:
        key = str(
            agent.get("agent_id")
            or agent.get("managed_agent_id")
            or agent.get("agent_name")
            or agent.get("name")
            or canonical_json_digest(agent)
        )
        if key in seen:
            continue
        seen.add(key)
        deduplicated.append(agent)
    return deduplicated


def _manifest_digest_summary(
    *,
    link_manifest: Mapping[str, object],
    launch_material_manifest: Mapping[str, object] | None,
    runtime_manifest: Mapping[str, object] | None,
) -> dict[str, object]:
    summary: dict[str, object] = {
        "adapter_link": canonical_json_digest(link_manifest),
    }
    if launch_material_manifest is not None:
        summary["launch_material"] = canonical_json_digest(launch_material_manifest)
    if runtime_manifest is not None:
        summary["adapter_runtime"] = canonical_json_digest(runtime_manifest)
    return summary


def _material_drift(
    launch_material_manifest: Mapping[str, object] | None,
    material_base_dir: Path | None,
) -> list[dict[str, object]]:
    if launch_material_manifest is None:
        return []
    drift: list[dict[str, object]] = []
    for item in _as_dict_list(launch_material_manifest.get("files")):
        path_text = item.get("path")
        expected = item.get("digest")
        if not isinstance(path_text, str) or not isinstance(expected, str):
            continue
        path = Path(path_text)
        if not path.is_absolute() and material_base_dir is not None:
            path = material_base_dir / path
        if not path.exists():
            drift.append({"path": str(path), "expected": expected, "observed": None, "status": "missing"})
            continue
        observed = file_digest(path)
        if observed != expected:
            drift.append({"path": str(path), "expected": expected, "observed": observed, "status": "changed"})
    return drift


def _live_summary(live_state: Mapping[str, object] | None) -> dict[str, object]:
    if live_state is None:
        return {"available": False, "agents": []}
    redacted = redact_payload(dict(live_state))
    if not isinstance(redacted, dict):
        return {"available": False, "agents": []}
    agents = _as_dict_list(redacted.get("agents"))
    redacted["agents"] = agents
    redacted.setdefault("available", bool(agents))
    return redacted


def _mapping_conflicts(
    agent_bindings: list[dict[str, object]],
    live_agents: object,
) -> list[str]:
    conflicts: list[str] = []
    agent_instance_ids = _duplicates(
        str(binding.get("agent_instance_id")) for binding in agent_bindings if binding.get("agent_instance_id")
    )
    managed_ids = _duplicates(
        str(binding.get("houmao_managed_agent_id")) for binding in agent_bindings if binding.get("houmao_managed_agent_id")
    )
    live_managed_ids = _duplicates(
        str(agent.get("agent_id") or agent.get("managed_agent_id"))
        for agent in _as_dict_list(live_agents)
        if agent.get("agent_id") or agent.get("managed_agent_id")
    )
    conflicts.extend(f"duplicate agent_instance_id: {value}" for value in agent_instance_ids)
    conflicts.extend(f"duplicate bound houmao managed-agent id: {value}" for value in managed_ids)
    conflicts.extend(f"duplicate live houmao managed-agent id: {value}" for value in live_managed_ids)
    return conflicts


def _mapping_confidence(
    agent_bindings: list[dict[str, object]],
    live_agents: object,
) -> str:
    if not agent_bindings:
        return MappingConfidence.UNMAPPED.value
    if any(binding.get("mapping_confidence") == MappingConfidence.EXACT.value for binding in agent_bindings):
        return MappingConfidence.EXACT.value
    if any(binding.get("houmao_managed_agent_id") for binding in agent_bindings):
        return MappingConfidence.MANIFEST_MATCH.value
    live_names = {
        str(agent.get("agent_name") or agent.get("name"))
        for agent in _as_dict_list(live_agents)
        if agent.get("agent_name") or agent.get("name")
    }
    bound_names = {
        str(binding.get("houmao_agent_name"))
        for binding in agent_bindings
        if binding.get("houmao_agent_name")
    }
    if bound_names and bound_names <= live_names:
        return MappingConfidence.NAME_MATCH.value
    if all(binding.get("agent_instance_id") for binding in agent_bindings):
        return MappingConfidence.MANUAL.value
    return MappingConfidence.UNMAPPED.value


def _runtime_source_mode(runtime_manifest: Mapping[str, object] | None) -> str | None:
    if runtime_manifest is None:
        return None
    value = runtime_manifest.get("source_mode")
    return str(value) if isinstance(value, str) else None


def _manifest_refs(
    link_manifest: Mapping[str, object] | None,
    launch_material_manifest: Mapping[str, object] | None,
    runtime_manifest: Mapping[str, object] | None,
) -> list[str]:
    refs = []
    for name, manifest in (
        ("adapter_link", link_manifest),
        ("launch_material", launch_material_manifest),
        ("adapter_runtime", runtime_manifest),
    ):
        if manifest is not None:
            refs.append(f"{name}:{canonical_json_digest(manifest)}")
    return refs


def _manifest_team_id(manifest: Mapping[str, object]) -> str:
    team = manifest.get("agent_team_instance")
    if isinstance(team, Mapping):
        value = team.get("id")
        if isinstance(value, str):
            return value
    return "unknown"


def _duplicates(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def _as_dict_list(value: object) -> list[dict[str, object]]:
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, Mapping)]
