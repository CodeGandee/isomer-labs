"""Manual acceptance check for Project-root Kaoju template context pinning."""

from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import textwrap
from typing import Any
from unittest.mock import patch

from isomer_labs import cli


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def _run(root: Path, *arguments: str) -> tuple[int, dict[str, Any]]:
    stdout = io.StringIO()
    with (
        contextlib.chdir(root),
        patch.dict(os.environ, {"HOME": str(root), "PATH": os.environ.get("PATH", "")}, clear=True),
        contextlib.redirect_stdout(stdout),
    ):
        status = cli.main(["--print-json", *arguments])
    return status, json.loads(stdout.getvalue())


def _require(condition: bool, message: str, payload: object | None = None) -> None:
    if not condition:
        detail = f"\n{json.dumps(payload, indent=2, sort_keys=True)}" if payload is not None else ""
        raise RuntimeError(f"{message}{detail}")


def _prepare_project(root: Path) -> None:
    _write(
        root / ".isomer-labs/manifest.toml",
        """
        schema_version = "isomer-project-manifest.v1"
        [defaults]
        research_topic_id = "alpha"
        topic_workspace_id = "alpha"
        [[research_topics]]
        id = "alpha"
        config_path = ".isomer-labs/research-topics/alpha.toml"
        topic_workspace_id = "alpha"
        status = "active"
        [[research_topics]]
        id = "beta"
        config_path = ".isomer-labs/research-topics/beta.toml"
        topic_workspace_id = "beta"
        status = "active"
        [[topic_workspaces]]
        id = "alpha"
        research_topic_id = "alpha"
        path = "topic-workspaces/alpha"
        status = "active"
        [[topic_workspaces]]
        id = "beta"
        research_topic_id = "beta"
        path = "topic-workspaces/beta"
        status = "active"
        """,
    )
    for topic in ("alpha", "beta"):
        _write(
            root / f".isomer-labs/research-topics/{topic}.toml",
            f"""
            schema_version = "isomer-research-topic-config.v1"
            research_topic_id = "{topic}"
            topic_statement = "{topic.title()} survey"
            """,
        )
        _write(root / f"topic-workspaces/{topic}/isomer-topic-workspace-summary.md", f"# {topic.title()}\n")
    for topic in ("alpha", "beta"):
        status, payload = _run(root, "project", "--root", str(root), "runtime", "init", "--topic", topic)
        _require(status == 0, f"runtime init failed for {topic}", payload)


def _prepare_beta_template(root: Path) -> tuple[Path, Path]:
    tree = root / "prepared/beta-latex-main"
    _write(
        tree / "template.tex",
        r"""
        \documentclass{article}
        \begin{document}
        % ISOMER_BODY
        \end{document}
        """,
    )
    metadata = root / "prepared/beta-latex-metadata.json"
    _write(
        metadata,
        json.dumps(
            {
                "entrypoint": "template.tex",
                "extensions": {
                    "latex": {
                        "composition_mode": "marker",
                        "marker": "% ISOMER_BODY",
                        "build_profile": "pdflatex",
                        "source_provenance": "manual-acceptance:beta-main",
                        "license_posture": "test-only",
                    }
                },
            }
        )
        + "\n",
    )
    return tree, metadata


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="isomer-kaoju-context-") as temporary:
        root = Path(temporary)
        _prepare_project(root)

        status, location = _run(root, "project", "self", "location")
        _require(status == 0 and location["location"]["workspace_kind"] == "project_root", "Project-root ambient classification failed", location)

        status, alignment = _run(root, "project", "self", "check", "--scope", "topic", "--topic", "beta")
        _require(status == 0 and alignment["alignment"]["verdict"] == "explicit_override", "Explicit beta alignment failed", alignment)
        _require(alignment["alignment"]["selected_target"]["research_topic_id"] == "beta", "Alignment did not pin beta", alignment)

        status, default_list = _run(root, "ext", "kaoju", "paper", "template", "list", "--kind", "latex", "--project", str(root))
        _require(status == 0 and default_list["selected_context"]["research_topic_id"] == "alpha", "Omitted selector did not report alpha default", default_list)
        _require(default_list["selected_context"]["sources"]["research_topic_id"] == "Project Manifest default", "Default selection source was not visible", default_list)

        tree, metadata = _prepare_beta_template(root)
        status, created = _run(
            root,
            "ext",
            "kaoju",
            "paper",
            "template",
            "create",
            "--topic",
            "beta",
            "--kind",
            "latex",
            "--name",
            "main",
            "--from",
            str(tree),
            "--metadata-file",
            str(metadata),
            "--actor",
            "agent:manual-check",
            "--project",
            str(root),
        )
        _require(status == 0 and created["selected_context"]["research_topic_id"] == "beta", "Beta template create failed", created)

        status, missing_default = _run(root, "ext", "kaoju", "paper", "template", "show", "--kind", "latex", "--name", "main", "--project", str(root))
        _require(status == 1 and missing_default["error"]["code"] == "template_not_found", "Default lookup searched or selected beta", missing_default)
        _require(missing_default["selected_context"]["research_topic_id"] == "alpha", "Missing-template failure lost selected context", missing_default)

        status, exported = _run(
            root,
            "ext",
            "kaoju",
            "paper",
            "template",
            "export",
            "--topic",
            "beta",
            "--kind",
            "latex",
            "--name",
            "main",
            "--actor",
            "agent:manual-check",
            "--project",
            str(root),
        )
        expected = root / "topic-workspaces/beta/intent/derived/writing-templates/latex/main"
        _require(status == 0 and exported["selected_context"]["research_topic_id"] == "beta", "Beta export lost pinned context", exported)
        _require(exported["target"] == str(expected), "Export did not use beta writing-template exchange surface", exported)
        _require((expected / ".isomer-template-export.json").is_file(), "Export observation metadata is missing", exported)
        _require("/actors/" not in exported["target"] and "/agents/" not in exported["target"], "Export used a worker workspace", exported)
        _require(not (root / "topic-workspaces/alpha/intent/derived/writing-templates/latex/main").exists(), "Export leaked into the default topic")

        print("PASS: Project-root preflight pinned beta and exported to topic-workspaces/beta/intent/derived/writing-templates/latex/main")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
