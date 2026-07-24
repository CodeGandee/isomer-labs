"""Checked immutable writing-template defaults packaged with the Kaoju write owner."""

from __future__ import annotations

from dataclasses import dataclass
from importlib.resources import files
import json
from pathlib import Path
from typing import Mapping

from isomer_labs.kaoju.artifacts import KaojuServiceError
from isomer_labs.kaoju.template_support import DEFAULT_TEMPLATE_NAME, TemplateKindSpec, resolve_template_kind, template_tree_digest
from isomer_labs.kaoju.template_validation import validate_authored_metadata


PACKAGED_TEMPLATE_SCHEMA_VERSION = "isomer-kaoju-packaged-templates.v1"
PACKAGED_TEMPLATE_RESOURCE = (
    "assets/system_skills/research-paradigm/kaoju/isomer-ext-kaoju-entrypoint/subskills/"
    "isomer-kaoju-write/assets/defaults/templates"
)
PACKAGED_TEMPLATE_MANIFEST = "manifest.json"


@dataclass(frozen=True)
class PackagedTemplate:
    """One validated immutable role-local packaged template."""

    template_kind: TemplateKindSpec
    name: str
    identity: str
    resource_version: str
    tree_digest: str
    authored_metadata: dict[str, object]
    root: Path

    def to_json(self) -> dict[str, object]:
        return {
            "template_kind": self.template_kind.kind,
            "name": self.name,
            "packaged_identity": self.identity,
            "packaged_resource_version": self.resource_version,
            "tree_digest": self.tree_digest,
            "authored_metadata": self.authored_metadata,
        }


def packaged_template_root() -> Path:
    """Return the protected write owner's packaged-template root."""

    return Path(str(files("isomer_labs").joinpath(PACKAGED_TEMPLATE_RESOURCE)))


def load_packaged_template(kind: str | TemplateKindSpec) -> PackagedTemplate:
    """Load and validate exactly one declared role-local ``main`` template."""

    selected_kind = resolve_template_kind(kind)
    root = packaged_template_root()
    manifest_path = root / PACKAGED_TEMPLATE_MANIFEST
    try:
        raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise KaojuServiceError(
            "packaged_template_manifest_invalid",
            f"Kaoju packaged-template manifest is missing or unreadable: {exc}",
        ) from exc
    if not isinstance(raw, dict) or raw.get("schema_version") != PACKAGED_TEMPLATE_SCHEMA_VERSION:
        raise KaojuServiceError(
            "packaged_template_manifest_invalid",
            "Kaoju packaged-template manifest has an unsupported schema version.",
        )
    resource_version = raw.get("resource_version")
    inventory = raw.get("templates")
    if not isinstance(resource_version, str) or not resource_version or not isinstance(inventory, dict):
        raise KaojuServiceError(
            "packaged_template_manifest_invalid",
            "Kaoju packaged-template manifest must declare a resource version and template inventory.",
        )
    if set(inventory) != {"content", "latex"}:
        raise KaojuServiceError(
            "packaged_template_inventory_invalid",
            "Kaoju packaged-template inventory must contain exactly content/main and latex/main.",
        )
    item = inventory.get(selected_kind.kind)
    if not isinstance(item, dict):
        raise KaojuServiceError(
            "packaged_template_inventory_invalid",
            f"Kaoju packaged-template inventory has no {selected_kind.kind}/main entry.",
        )
    name = item.get("name")
    relative_root = item.get("root")
    recorded_digest = item.get("tree_digest")
    authored = item.get("authored_metadata")
    if name != DEFAULT_TEMPLATE_NAME or relative_root != f"{selected_kind.kind}/{DEFAULT_TEMPLATE_NAME}":
        raise KaojuServiceError(
            "packaged_template_identity_invalid",
            f"Kaoju packaged {selected_kind.kind} default must be named main at {selected_kind.kind}/main.",
        )
    if not isinstance(recorded_digest, str) or not isinstance(authored, dict):
        raise KaojuServiceError(
            "packaged_template_manifest_invalid",
            f"Kaoju packaged {selected_kind.kind}/main has incomplete digest or authored metadata.",
        )
    template_root = (root / relative_root).resolve(strict=False)
    try:
        template_root.relative_to(root.resolve(strict=False))
    except ValueError as exc:
        raise KaojuServiceError(
            "packaged_template_path_invalid",
            f"Kaoju packaged {selected_kind.kind}/main escapes its protected resource root.",
        ) from exc
    observed_digest = template_tree_digest(template_root)
    if observed_digest != recorded_digest:
        raise KaojuServiceError(
            "packaged_template_digest_mismatch",
            f"Kaoju packaged {selected_kind.kind}/main digest is {observed_digest}, expected {recorded_digest}.",
        )
    validated = validate_authored_metadata(authored, root=template_root, template_kind=selected_kind)
    if "entrypoint" not in validated or "use_guidance" not in validated:
        raise KaojuServiceError(
            "packaged_template_metadata_invalid",
            f"Kaoju packaged {selected_kind.kind}/main requires an entrypoint and use guidance.",
        )
    if selected_kind.kind == "content" and Path(str(validated["entrypoint"])).suffix.casefold() not in {".md", ".myst"}:
        raise KaojuServiceError(
            "packaged_template_metadata_invalid",
            "Kaoju packaged content/main entrypoint must be a MyST-oriented .md or .myst file.",
        )
    identity = f"isomer-kaoju-packaged-template:{resource_version}:{selected_kind.kind}:{DEFAULT_TEMPLATE_NAME}"
    return PackagedTemplate(
        template_kind=selected_kind,
        name=DEFAULT_TEMPLATE_NAME,
        identity=identity,
        resource_version=resource_version,
        tree_digest=observed_digest,
        authored_metadata=validated,
        root=template_root,
    )


def validate_packaged_templates() -> list[dict[str, object]]:
    """Return stable diagnostics for the complete packaged-template inventory."""

    diagnostics: list[dict[str, object]] = []
    for kind in ("content", "latex"):
        try:
            load_packaged_template(kind)
        except KaojuServiceError as exc:
            diagnostics.append(
                {
                    "severity": "error",
                    "code": exc.code,
                    "message": str(exc),
                    "path": str(packaged_template_root()),
                    "template_kind": kind,
                }
            )
    return diagnostics


def packaged_template_identity(value: Mapping[str, object]) -> bool:
    """Return whether metadata names one checked packaged-template identity."""

    identity = value.get("packaged_identity")
    version = value.get("packaged_resource_version")
    return isinstance(identity, str) and identity.startswith("isomer-kaoju-packaged-template:") and isinstance(version, str) and bool(version)
