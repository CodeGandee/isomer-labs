"""Project initialization for the Milestone 1 CLI."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from isomer_labs.workspace.surfaces import (
    CONTENT_ROOT_GITIGNORE_TEXT,
    CONTENT_ROOT_README_TEXT,
    content_path_defaults_for_init,
    content_root_path as default_content_root_path,
    topic_workspace_base_path as default_topic_workspace_base_path,
)
from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.houmao.adapter import HoumaoCommandCatalog, HoumaoCommandResult, HoumaoCommandRunner
from isomer_labs.core.path_utils import is_within
from isomer_labs.project import config_dir_for_root, manifest_path_for_root
from isomer_labs.project import (
    houmao_overlay_dir_for_root,
    houmao_project_dir_for_root,
    root_houmao_overlay_dir_for_root,
)
@dataclass(frozen=True)
class ProjectInitializationResult:
    project_root: Path
    project_manifest_path: Path
    content_root_path: Path
    topic_workspace_base_path: Path
    houmao_project_dir: Path
    houmao_overlay_dir: Path
    houmao_bootstrap_result: HoumaoCommandResult | None
    diagnostics: list[Diagnostic]

    @property
    def ok(self) -> bool:
        return not has_errors(self.diagnostics)


def initialize_project(
    project_root: Path,
    *,
    content_dir: str | None = None,
    env: Mapping[str, str] | None = None,
) -> ProjectInitializationResult:
    diagnostics: list[Diagnostic] = []
    root = project_root.resolve(strict=False)
    manifest_path = manifest_path_for_root(root)
    config_dir = config_dir_for_root(root)
    path_defaults = content_path_defaults_for_init(root, content_dir)
    content_root = default_content_root_path(root, path_defaults)
    topic_workspace_base = default_topic_workspace_base_path(root, path_defaults)
    houmao_project_dir = houmao_project_dir_for_root(root)
    houmao_overlay_dir = houmao_overlay_dir_for_root(root)
    root_houmao_overlay_dir = root_houmao_overlay_dir_for_root(root)

    if manifest_path.exists():
        return ProjectInitializationResult(
            project_root=root,
            project_manifest_path=manifest_path,
            content_root_path=content_root,
            topic_workspace_base_path=topic_workspace_base,
            houmao_project_dir=houmao_project_dir,
            houmao_overlay_dir=houmao_overlay_dir,
            houmao_bootstrap_result=None,
            diagnostics=[
                Diagnostic(
                    code="ISO003",
                    severity="error",
                    concept="Project Manifest",
                    path=manifest_path,
                    message="Project Manifest already exists; init refuses to overwrite it. Review removable Project-managed material with `isomer-cli project cleanup --part bootstrap --dry-run` before reinitializing.",
                )
            ],
        )

    diagnostics.extend(
        _validate_content_root(root, content_root, topic_workspace_base, config_dir, root_houmao_overlay_dir)
    )
    if has_errors(diagnostics):
        return ProjectInitializationResult(
            project_root=root,
            project_manifest_path=manifest_path,
            content_root_path=content_root,
            topic_workspace_base_path=topic_workspace_base,
            houmao_project_dir=houmao_project_dir,
            houmao_overlay_dir=houmao_overlay_dir,
            houmao_bootstrap_result=None,
            diagnostics=diagnostics,
        )

    config_dir.mkdir(parents=True, exist_ok=True)
    houmao_result = bootstrap_houmao_project(root, env=env)
    diagnostics.extend(houmao_result.diagnostics)
    if houmao_result.succeeded and not houmao_overlay_dir.exists():
        diagnostics.append(
            Diagnostic(
                code="ISO003",
                severity="error",
                concept="Houmao Project",
                path=houmao_overlay_dir,
                message="Houmao Project bootstrap completed without creating the Isomer-managed .isomer-labs/.houmao overlay.",
            )
        )
    if has_errors(diagnostics):
        return ProjectInitializationResult(
            project_root=root,
            project_manifest_path=manifest_path,
            content_root_path=content_root,
            topic_workspace_base_path=topic_workspace_base,
            houmao_project_dir=houmao_project_dir,
            houmao_overlay_dir=houmao_overlay_dir,
            houmao_bootstrap_result=houmao_result,
            diagnostics=diagnostics,
        )

    content_root.mkdir(parents=True, exist_ok=True)
    (content_root / "README.md").write_text(CONTENT_ROOT_README_TEXT, encoding="utf-8")
    (content_root / ".gitignore").write_text(CONTENT_ROOT_GITIGNORE_TEXT, encoding="utf-8")
    manifest_path.write_text(_manifest_text(path_defaults), encoding="utf-8")
    return ProjectInitializationResult(
        project_root=root,
        project_manifest_path=manifest_path,
        content_root_path=content_root,
        topic_workspace_base_path=topic_workspace_base,
        houmao_project_dir=houmao_project_dir,
        houmao_overlay_dir=houmao_overlay_dir,
        houmao_bootstrap_result=houmao_result,
        diagnostics=diagnostics,
    )


def bootstrap_houmao_project(project_root: Path, *, env: Mapping[str, str] | None = None) -> HoumaoCommandResult:
    root = project_root.resolve(strict=False)
    runner = HoumaoCommandRunner(root, env=env)
    return runner.run(HoumaoCommandCatalog().project_init(houmao_project_dir_for_root(root)))


def _validate_content_root(
    project_root: Path,
    content_root: Path,
    topic_workspace_base: Path,
    config_dir: Path,
    root_houmao_overlay_dir: Path,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if not is_within(content_root, project_root):
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="Project generated content root",
                path=content_root,
                field="content_dir",
                message="Project generated content root resolves outside the Project root.",
            )
        )
    if is_within(content_root, config_dir) or is_within(topic_workspace_base, config_dir):
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="Project generated content root",
                path=content_root,
                field="content_dir",
                message="Project generated content root must not live inside the Project Config Directory.",
            )
        )
    if is_within(content_root, root_houmao_overlay_dir) or is_within(topic_workspace_base, root_houmao_overlay_dir):
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="Project generated content root",
                path=content_root,
                field="content_dir",
                message="Project generated content root must not collide with root .houmao external Houmao state.",
            )
        )
    return diagnostics


def _manifest_text(path_defaults: Mapping[str, object]) -> str:
    content_root_input = _toml_string(str(path_defaults["isomer_content_root"]))
    topic_workspace_base_input = _toml_string(str(path_defaults["topic_workspace_base_dir"]))
    return (
        'schema_version = "isomer-project-manifest.v1"\n'
        "\n"
        "[paths]\n"
        f'isomer_content_root = "{content_root_input}"\n'
        f'topic_workspace_base_dir = "{topic_workspace_base_input}"\n'
    )


def _toml_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')
