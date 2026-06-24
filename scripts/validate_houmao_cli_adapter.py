#!/usr/bin/env python3
"""Live-gated validation for the Houmao CLI adapter."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys


def isomer_project_command(project: Path, *args: str) -> list[str]:
    return ["pixi", "run", "isomer-cli", "project", "--root", str(project), *args]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, help="Project root to validate.")
    parser.add_argument("--topic", required=True, help="Research Topic id.")
    parser.add_argument("--profile", required=True, help="Topic Agent Team Profile id.")
    parser.add_argument("--instance-id", default="ati-houmao-live-validation", help="Agent Team Instance id to create or reuse.")
    parser.add_argument("--houmao-command", default=None, help="Optional ISOMER_HOUMAO_COMMAND override.")
    parser.add_argument("--yes-live", action="store_true", help="Actually run commands that can launch and stop Houmao agents.")
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve(strict=False)
    commands = [
        isomer_project_command(project, "runtime", "init", "--topic", args.topic, "--json"),
        isomer_project_command(project, "runtime", "prepare", "--topic", args.topic, "--json"),
        isomer_project_command(
            project,
            "team-instances",
            "create",
            "--topic",
            args.topic,
            "--topic-agent-team-profile",
            args.profile,
            "--id",
            args.instance_id,
            "--json",
        ),
        isomer_project_command(
            project,
            "team-instances",
            "launch-material",
            "prepare",
            args.instance_id,
            "--topic",
            args.topic,
            "--adapter",
            "houmao",
            "--json",
        ),
        isomer_project_command(
            project,
            "team-instances",
            "launch",
            args.instance_id,
            "--topic",
            args.topic,
            "--adapter",
            "houmao",
            "--json",
        ),
        isomer_project_command(
            project,
            "team-instances",
            "inspect-live",
            args.instance_id,
            "--topic",
            args.topic,
            "--adapter",
            "houmao",
            "--json",
        ),
        isomer_project_command(
            project,
            "team-instances",
            "stop",
            args.instance_id,
            "--topic",
            args.topic,
            "--adapter",
            "houmao",
            "--json",
        ),
        isomer_project_command(
            project,
            "team-instances",
            "reconcile",
            args.instance_id,
            "--topic",
            args.topic,
            "--json",
        ),
    ]

    if not args.yes_live:
        print("Dry run only. Re-run with --yes-live to launch and stop Houmao agents.")
        for command in commands:
            print("$ " + " ".join(command))
        return 0

    env = dict(os.environ)
    if args.houmao_command is not None:
        env["ISOMER_HOUMAO_COMMAND"] = args.houmao_command
    for command in commands:
        completed = subprocess.run(command, cwd=project, env=env, text=True, check=False)
        if completed.returncode != 0:
            print(f"Command failed with exit code {completed.returncode}: {' '.join(command)}", file=sys.stderr)
            return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
