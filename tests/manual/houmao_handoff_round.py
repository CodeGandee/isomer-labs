"""Manual Houmao handoff round validation.

By default this script uses the same local fake ``houmao-mgr`` command as the
manifest reconciliation manual check. Use ``--live-houmao`` only when a real
local Houmao checkout or command has already passed Houmao-side validation.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from houmao_manifest_reconciliation import (
    FIXTURE_PROJECT,
    PROFILE_ID,
    REPO_ROOT,
    TOPIC_ID,
    _bootstrap_runtime,
    _create_team_instance,
    _prepare_project,
    _require,
    _run_cli,
    _validation_env,
)


TEAM_ID = "ati-manual-handoff"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate one Houmao-backed Isomer handoff round.")
    parser.add_argument(
        "--live-houmao",
        action="store_true",
        help="Use the real houmao-mgr command. Requires ISOMER_MANUAL_LIVE_HOUMAO=1.",
    )
    args = parser.parse_args(argv)
    if args.live_houmao and os.environ.get("ISOMER_MANUAL_LIVE_HOUMAO") != "1":
        print(
            json.dumps(
                {
                    "ok": False,
                    "skipped": True,
                    "reason": "Real Houmao validation requires ISOMER_MANUAL_LIVE_HOUMAO=1.",
                    "houmao_checkout": _checkout_report(),
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 77

    with tempfile.TemporaryDirectory(prefix="isomer-houmao-handoff-") as tmp:
        root = Path(tmp) / "project"
        shutil.copytree(FIXTURE_PROJECT, root)
        _prepare_project(root)
        env = _validation_env(root, fake_houmao=not args.live_houmao)
        capability = _capability_report(env)
        if args.live_houmao and not capability["available"]:
            print(json.dumps({"ok": False, "skipped": True, "reason": "houmao-unavailable", "capability": capability}, indent=2, sort_keys=True))
            return 77
        handoff = _validate_handoff_round(root, env, live_houmao=args.live_houmao)
        print(
            json.dumps(
                {
                    "ok": True,
                    "mode": "live-houmao" if args.live_houmao else "manual-fake-houmao",
                    "capability": capability,
                    "handoff_round": handoff,
                    "houmao_checkout": _checkout_report(),
                },
                indent=2,
                sort_keys=True,
            )
        )
    return 0


def _capability_report(env: dict[str, str]) -> dict[str, Any]:
    command = shlex.split(env.get("ISOMER_HOUMAO_COMMAND") or "houmao-mgr")
    completed = subprocess.run(
        [*command, "--version"],
        cwd=REPO_ROOT,
        env=env,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return {
        "available": completed.returncode == 0,
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
        "checkout": _checkout_report(),
    }


def _checkout_report() -> dict[str, object]:
    candidates = [
        REPO_ROOT / "extern" / "orphan" / "houmao",
        Path(os.environ.get("ISOMER_HOUMAO_CHECKOUT", "")).expanduser(),
        Path("~/workspace/code/houmao").expanduser(),
    ]
    return {
        "candidates": [
            {"path": str(path), "exists": path.exists(), "is_symlink": path.is_symlink()}
            for path in candidates
            if str(path) != "."
        ],
        "write_policy": "do-not-write-or-commit-extern-orphan-houmao-from-isomer-tests",
    }


def _validate_handoff_round(root: Path, env: dict[str, str], *, live_houmao: bool) -> dict[str, object]:
    _bootstrap_runtime(root, env)
    _create_team_instance(root, env, TEAM_ID)
    launch = _run_cli(
        root,
        env,
        [
            "--print-json",
            "team-instances",
            "launch",
            TEAM_ID,
            "--topic",
            TOPIC_ID,
            "--adapter",
            "houmao",
        ],
    )
    _require(launch["status"] == 0, "quick launch command failed", launch)
    show = _run_cli(root, env, ["--print-json", "team-instances", "show", TEAM_ID, "--topic", TOPIC_ID])
    _require(show["status"] == 0, "team show failed after launch", show)
    source_agent, target_agent = _agent_pair(show["json"]["summary"]["agent_instances"])

    dispatch = _run_cli(
        root,
        env,
        [
            "--print-json",
            "handoffs",
            "dispatch",
            "--topic",
            TOPIC_ID,
            "--agent-team-instance",
            TEAM_ID,
            "--source-agent-instance",
            source_agent,
            "--target-agent-instance",
            target_agent,
            "--run",
            "run-manual-handoff",
            "--message",
            "Manual validation handoff.",
            "--expected-output",
            f"artifact:{TOPIC_ID}:manual-handoff",
        ],
    )
    _require(dispatch["status"] == 0, "handoff dispatch failed", dispatch)
    handoff_id = str(dispatch["json"]["dispatch"]["handoff_id"])

    observe = _run_cli(root, env, ["--print-json", "handoffs", "observe", handoff_id, "--topic", TOPIC_ID, "--source", "mail"])
    _require(observe["status"] == 0, "handoff observe failed", observe)
    signal_observation_id = str(observe["json"]["observation"]["signal_observation_id"])

    normalize = _run_cli(
        root,
        env,
        [
            "--print-json",
            "handoffs",
            "normalize",
            handoff_id,
            "--topic",
            TOPIC_ID,
            "--status",
            "accepted",
            "--signal-observation",
            signal_observation_id,
            "--output-artifact",
            f"artifact:{TOPIC_ID}:manual-handoff",
            "--rationale",
            "Manual validation accepted the candidate result.",
        ],
    )
    _require(normalize["status"] == 0, "handoff normalization failed", normalize)

    validate = _run_cli(root, env, ["--print-json", "runtime", "validate", "--topic", TOPIC_ID])
    _require(validate["status"] == 0, "runtime validation failed after handoff round", validate)

    stop = _run_cli(root, env, ["--print-json", "team-instances", "stop", TEAM_ID, "--topic", TOPIC_ID, "--adapter", "houmao"])
    if not live_houmao:
        _require(stop["status"] == 0, "fake Houmao cleanup failed", stop)

    return {
        "profile_id": PROFILE_ID,
        "agent_team_instance_id": TEAM_ID,
        "source_agent_instance_id": source_agent,
        "target_agent_instance_id": target_agent,
        "handoff_id": handoff_id,
        "signal_observation_id": signal_observation_id,
        "normalization_id": normalize["json"]["normalization"]["normalization_record_id"],
        "runtime_counts": validate["json"]["runtime"]["counts"],
        "cleanup": {
            "status": stop["status"],
            "payload": stop["json"],
        },
    }


def _agent_pair(agent_instances: list[dict[str, object]]) -> tuple[str, str]:
    source = next(
        str(agent["id"])
        for agent in agent_instances
        if "master" in str(agent.get("agent_role_id", ""))
    )
    target = next(
        str(agent["id"])
        for agent in agent_instances
        if "experimenter" in str(agent.get("agent_role_id", ""))
    )
    return source, target


if __name__ == "__main__":
    raise SystemExit(main())
