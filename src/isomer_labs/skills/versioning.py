"""Version metadata helpers for packaged and projected Isomer skills."""

from __future__ import annotations

from dataclasses import dataclass
from importlib.resources.abc import Traversable
from typing import Literal

from packaging.version import InvalidVersion, Version
import yaml  # type: ignore[import-untyped]


SkillVersionMetadataStatus = Literal["valid", "unversioned", "malformed_version"]


@dataclass(frozen=True)
class SkillVersionObservation:
    """Parsed `agents/openai.yaml` release metadata for one skill directory."""

    status: SkillVersionMetadataStatus
    raw_version: str | None
    normalized_version: str | None
    message: str | None = None

    @property
    def version(self) -> Version | None:
        if self.normalized_version is None:
            return None
        return Version(self.normalized_version)

    def to_json(self) -> dict[str, object]:
        return {
            "status": self.status,
            "raw_version": self.raw_version,
            "normalized_version": self.normalized_version,
            "message": self.message,
        }


def inspect_skill_version(skill_root: Traversable) -> SkillVersionObservation:
    """Read one skill's Isomer-owned release version from `agents/openai.yaml`."""

    manifest = skill_root.joinpath("agents", "openai.yaml")
    if not manifest.is_file():
        return SkillVersionObservation("unversioned", None, None, "agents/openai.yaml is missing")
    try:
        loaded = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return SkillVersionObservation("malformed_version", None, None, f"Cannot parse agents/openai.yaml: {exc}")
    if not isinstance(loaded, dict):
        return SkillVersionObservation("malformed_version", None, None, "agents/openai.yaml must be a YAML mapping")
    metadata = loaded.get("metadata")
    if not isinstance(metadata, dict):
        return SkillVersionObservation("unversioned", None, None, "metadata.version is missing")
    raw_version = metadata.get("version")
    if not isinstance(raw_version, str) or not raw_version:
        return SkillVersionObservation("unversioned", None, None, "metadata.version is missing")
    try:
        parsed = Version(raw_version)
    except InvalidVersion:
        return SkillVersionObservation(
            "malformed_version",
            raw_version,
            None,
            f"metadata.version is not a valid PEP 440 version: {raw_version!r}",
        )
    return SkillVersionObservation("valid", raw_version, str(parsed))


def require_skill_version(skill_root: Traversable) -> str:
    """Return a valid raw skill version or raise a deterministic error."""

    observation = inspect_skill_version(skill_root)
    if observation.status != "valid" or observation.raw_version is None:
        raise ValueError(observation.message or "Skill version metadata is unavailable")
    return observation.raw_version
