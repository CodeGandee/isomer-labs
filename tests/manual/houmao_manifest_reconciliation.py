"""Manual Houmao manifest reconciliation validation.

This script is intentionally outside ``tests/unit`` because it drives full CLI
workflows and creates a temporary project. By default it uses a local fake
``houmao-mgr`` command with the same command shapes Isomer calls. That keeps the
validation repeatable while preserving the live-gated workflow boundary.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_PROJECT = REPO_ROOT / "tests" / "fixtures" / "projects" / "deepsci-profile-use-cases"
TOPIC_ID = "novel-biomarker"
PROFILE_ID = "uc-01-novel-biomarker"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Houmao manifest reconciliation workflows.")
    parser.add_argument(
        "--live-houmao",
        action="store_true",
        help="Use the real houmao-mgr command. Requires ISOMER_MANUAL_LIVE_HOUMAO=1.",
    )
    args = parser.parse_args(argv)
    if args.live_houmao and os.environ.get("ISOMER_MANUAL_LIVE_HOUMAO") != "1":
        raise RuntimeError("Real Houmao validation requires ISOMER_MANUAL_LIVE_HOUMAO=1.")
    with tempfile.TemporaryDirectory(prefix="isomer-houmao-manifest-") as tmp:
        root = Path(tmp) / "project"
        shutil.copytree(FIXTURE_PROJECT, root)
        _prepare_project(root)
        env = _validation_env(root, fake_houmao=not args.live_houmao)
        quick = _validate_quick_launch(root, env)
        direct = _validate_direct_houmao(root, env)
        print(
            json.dumps(
                {
                    "ok": True,
                    "mode": "live-houmao" if args.live_houmao else "manual-fake-houmao",
                    "quick_launch": quick,
                    "direct_houmao": direct,
                },
                indent=2,
                sort_keys=True,
            )
        )
    return 0


def _prepare_project(root: Path) -> None:
    (root / "pyproject.toml").write_text(
        textwrap.dedent(
            """
            [project]
            name = "isomer-houmao-manual"
            version = "0.0.0"

            [tool.pixi.workspace]
            channels = ["conda-forge"]
            platforms = ["linux-aarch64"]
            """
        ).lstrip(),
        encoding="utf-8",
    )
    (root / "pixi.lock").write_text("version: 1\n", encoding="utf-8")
    manifest_path = root / ".isomer-labs" / "manifest.toml"
    manifest_path.write_text(
        manifest_path.read_text(encoding="utf-8")
        + textwrap.dedent(
            """

            [[topic_pixi_environment_bindings]]
            research_topic_id = "novel-biomarker"
            pixi_environment = "default"
            purpose = "runtime"
            """
        ),
        encoding="utf-8",
    )


def _validation_env(root: Path, *, fake_houmao: bool) -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")
    env["HOME"] = str(root / "home")
    if fake_houmao:
        fake_bin = root / "fake-bin"
        fake_bin.mkdir(parents=True, exist_ok=True)
        fake_command = fake_bin / "houmao-mgr"
        fake_command.write_text(_fake_houmao_mgr_source(), encoding="utf-8")
        fake_command.chmod(0o755)
        env["PATH"] = str(fake_bin) + os.pathsep + env.get("PATH", "")
        env["ISOMER_HOUMAO_COMMAND"] = "houmao-mgr"
        env["HOUMAO_FAKE_STATE"] = str(root / ".fake-houmao-global-state.json")
    else:
        env.setdefault("ISOMER_HOUMAO_COMMAND", "houmao-mgr")
    return env


def _validate_quick_launch(root: Path, env: dict[str, str]) -> dict[str, object]:
    _bootstrap_runtime(root, env)
    _create_team_instance(root, env, "ati-manual-quick")
    launch = _run_cli(
        root,
        env,
        [
            "team-instances",
            "launch",
            "ati-manual-quick",
            "--topic",
            TOPIC_ID,
            "--adapter",
            "houmao",
            "--json",
        ],
    )
    _require(launch["status"] == 0, "quick launch command failed", launch)
    launch_payload = launch["json"]
    _require(launch_payload["launch"]["status"] == "launched", "quick launch did not launch", launch_payload)
    _require(
        launch_payload["launch"]["reconciliation"]["state"] == "launched_by_isomer",
        "quick launch did not record launched_by_isomer reconciliation",
        launch_payload,
    )
    reconcile = _run_cli(
        root,
        env,
        [
            "team-instances",
            "reconcile",
            "ati-manual-quick",
            "--topic",
            TOPIC_ID,
            "--json",
        ],
    )
    _require(reconcile["status"] == 0, "quick reconcile command failed", reconcile)
    _require(
        reconcile["json"]["reconciliation"]["state"] == "launched_by_isomer",
        "quick reconcile did not confirm launched_by_isomer",
        reconcile["json"],
    )
    return {
        "launch_state": launch_payload["launch"]["reconciliation"]["state"],
        "reconcile_state": reconcile["json"]["reconciliation"]["state"],
        "runtime_manifest_path": launch_payload["launch"]["runtime_manifest_path"],
    }


def _validate_direct_houmao(root: Path, env: dict[str, str]) -> dict[str, object]:
    _create_team_instance(root, env, "ati-manual-direct")
    link = _run_cli(
        root,
        env,
        [
            "team-instances",
            "adapter-link",
            "export",
            "ati-manual-direct",
            "--topic",
            TOPIC_ID,
            "--houmao-project-dir",
            "topic-workspaces/novel-biomarker/runtime/adapters/houmao/ati-manual-direct/houmao-project",
            "--json",
        ],
    )
    _require(link["status"] == 0, "adapter link export failed", link)
    link_manifest = link["json"]["manifest"]
    binding = _first_binding(link_manifest)
    houmao_project_dir = Path(str(link_manifest["houmao"]["project_dir"]))
    _run_houmao(env, ["--print-json", "project", "--project-dir", str(houmao_project_dir), "init"])
    _run_houmao(
        env,
        [
            "--print-json",
            "project",
            "--project-dir",
            str(houmao_project_dir),
            "agents",
            "launch",
            "--profile",
            str(binding["houmao_profile"]),
            "--name",
            str(binding["houmao_agent_name"]),
            "--workdir",
            str(root),
            "--headless",
        ],
    )
    reconcile = _run_cli(
        root,
        env,
        [
            "team-instances",
            "reconcile",
            "ati-manual-direct",
            "--topic",
            TOPIC_ID,
            "--json",
        ],
    )
    _require(reconcile["status"] == 0, "direct reconcile command failed", reconcile)
    _require(
        reconcile["json"]["reconciliation"]["state"] == "external_detected",
        "direct reconcile did not report external_detected",
        reconcile["json"],
    )
    adopt = _run_cli(
        root,
        env,
        [
            "team-instances",
            "adopt",
            "ati-manual-direct",
            "--topic",
            TOPIC_ID,
            "--yes",
            "--json",
        ],
    )
    _require(adopt["status"] == 0, "direct adopt command failed", adopt)
    _require(adopt["json"]["reconciliation"]["state"] == "adopted", "direct adopt did not adopt", adopt["json"])
    return {
        "reconcile_state": reconcile["json"]["reconciliation"]["state"],
        "adopt_state": adopt["json"]["reconciliation"]["state"],
        "runtime_manifest_path": adopt["json"]["runtime_manifest_path"],
    }


def _bootstrap_runtime(root: Path, env: dict[str, str]) -> None:
    for args in (
        ["runtime", "init", "--topic", TOPIC_ID, "--json"],
        ["runtime", "prepare", "--topic", TOPIC_ID, "--json"],
    ):
        result = _run_cli(root, env, args)
        _require(result["status"] == 0, "runtime bootstrap command failed", result)


def _create_team_instance(root: Path, env: dict[str, str], team_id: str) -> None:
    result = _run_cli(
        root,
        env,
        [
            "team-instances",
            "create",
            "--topic",
            TOPIC_ID,
            "--topic-agent-team-profile",
            PROFILE_ID,
            "--id",
            team_id,
            "--json",
        ],
    )
    _require(result["status"] == 0, f"Agent Team Instance creation failed: {team_id}", result)


def _run_cli(root: Path, env: dict[str, str], args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, "-m", "isomer_labs", *args],
        cwd=root,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    return {
        "status": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "json": _parse_json(completed.stdout),
        "args": args,
    }


def _run_houmao(env: dict[str, str], args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(
        ["houmao-mgr", *args],
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    result = {
        "status": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "json": _parse_json(completed.stdout),
        "args": args,
    }
    _require(completed.returncode == 0, "fake houmao command failed", result)
    return result


def _parse_json(value: str) -> object:
    stripped = value.strip()
    if not stripped:
        return None
    return json.loads(stripped)


def _first_binding(link_manifest: dict[str, Any]) -> dict[str, Any]:
    bindings = link_manifest.get("agent_bindings")
    _require(isinstance(bindings, list) and bindings, "link manifest has no agent bindings", link_manifest)
    first = bindings[0]
    _require(isinstance(first, dict), "first link manifest binding is invalid", link_manifest)
    return first


def _require(condition: bool, message: str, payload: object) -> None:
    if not condition:
        raise RuntimeError(message + "\n" + json.dumps(payload, indent=2, sort_keys=True))


def _fake_houmao_mgr_source() -> str:
    return textwrap.dedent(
        r'''
        #!/usr/bin/env python3
        from __future__ import annotations

        import json
        import os
        import sys
        from pathlib import Path

        args = sys.argv[1:]

        def option(name: str, default: str | None = None) -> str | None:
            if name in args:
                index = args.index(name)
                if index + 1 < len(args):
                    return args[index + 1]
            return default

        def load(path: Path) -> dict[str, object]:
            if not path.exists():
                return {"agents": {}, "profiles": {}, "specialists": {}}
            data = json.loads(path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {"agents": {}, "profiles": {}, "specialists": {}}

        def save(path: Path, data: dict[str, object]) -> None:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        def project_state_path() -> Path:
            project_dir = option("--project-dir")
            if project_dir is None:
                return Path(os.environ["HOUMAO_FAKE_STATE"])
            return Path(project_dir) / ".fake-houmao-state.json"

        def global_state_path() -> Path:
            return Path(os.environ["HOUMAO_FAKE_STATE"])

        def agent_records(state: dict[str, object]) -> list[dict[str, object]]:
            agents = state.setdefault("agents", {})
            if isinstance(agents, dict):
                return [item for item in agents.values() if isinstance(item, dict)]
            return []

        if "--version" in args:
            print("houmao-mgr 0.0.0-manual")
            raise SystemExit(0)

        state_path = project_state_path()
        state = load(state_path)
        global_state = load(global_state_path())

        payload: dict[str, object]
        if "system-skills" in args and "list" in args:
            payload = {"skills": []}
        elif "project" in args and "init" in args:
            state_path.parent.mkdir(parents=True, exist_ok=True)
            payload = {"project": {"status": "initialized", "project_dir": str(state_path.parent)}}
        elif "project" in args and "status" in args:
            payload = {"project": {"status": "ready", "project_dir": str(state_path.parent)}, "agents": agent_records(state)}
        elif "specialist" in args and "create" in args:
            specialists = state.setdefault("specialists", {})
            specialists[str(option("--name"))] = {"name": option("--name"), "tool": option("--tool")}
            payload = {"specialist": specialists[str(option("--name"))]}
        elif "profile" in args and "create" in args:
            profiles = state.setdefault("profiles", {})
            profiles[str(option("--name"))] = {
                "name": option("--name"),
                "agent_name": option("--agent-name"),
                "specialist": option("--specialist"),
            }
            payload = {"profile": profiles[str(option("--name"))]}
        elif "agents" in args and "launch" in args:
            name = str(option("--name") or option("--agent-name"))
            record = {
                "agent_id": "hm-" + name,
                "managed_agent_id": "hm-" + name,
                "agent_name": name,
                "name": name,
                "profile": option("--profile"),
                "state": "running",
            }
            state.setdefault("agents", {})[name] = record
            global_state.setdefault("agents", {})[name] = record
            payload = record
        elif "agents" in args and "list" in args:
            payload = {"agents": agent_records(global_state if "global" in args else state)}
        elif "agents" in args and "get" in args:
            name = str(option("--name"))
            agents = state.setdefault("agents", {})
            payload = agents.get(name, {"agent_id": "hm-" + name, "agent_name": name, "name": name})
        elif "agents" in args and "stop" in args:
            name = str(option("--name"))
            agents = state.setdefault("agents", {})
            record = agents.get(name, {"agent_id": "hm-" + name, "agent_name": name, "name": name})
            if isinstance(record, dict):
                record["state"] = "stopped"
                agents[name] = record
            payload = {"stopped": True, "agent_name": name}
        else:
            payload = {"ok": False, "args": args}
            print(json.dumps(payload, sort_keys=True))
            raise SystemExit(2)

        save(state_path, state)
        save(global_state_path(), global_state)
        print(json.dumps(payload, sort_keys=True))
        '''
    ).lstrip()


if __name__ == "__main__":
    raise SystemExit(main())
