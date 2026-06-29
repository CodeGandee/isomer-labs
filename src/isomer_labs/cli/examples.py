"""Public CLI examples used by docs and invocation diagnostics."""

from __future__ import annotations


COMMAND_EXAMPLES: dict[str, tuple[str, ...]] = {
    "project": (
        "pixi run isomer-cli --print-json project validate",
        "pixi run isomer-cli --print-json project doctor",
        "pixi run isomer-cli --print-json project topics list",
    ),
    "project doctor": (
        "pixi run isomer-cli --print-json project doctor",
        "pixi run isomer-cli --print-json project doctor --topic my-topic",
    ),
    "project paths": (
        "pixi run isomer-cli --print-json project paths get topic.records.artifacts --topic my-topic",
        "pixi run isomer-cli --print-json project paths list --topic my-topic --agent alice",
        "pixi run isomer-cli --print-json project paths register custom.datasets.raw --topic my-topic --path data/raw --storage-profile topic_records_dir --create",
    ),
    "project paths get": (
        "pixi run isomer-cli --print-json project paths get topic.records.artifacts --topic my-topic",
        "pixi run isomer-cli --print-json project paths get topic.repos.main --topic my-topic --configured",
        "pixi run isomer-cli --print-json project paths get agent.private_artifacts --topic my-topic --agent alice",
    ),
    "project paths register": (
        "pixi run isomer-cli --print-json project paths register custom.datasets.raw --topic my-topic --path data/raw --storage-profile topic_records_dir --create",
        "pixi run isomer-cli --print-json project paths register topic.repos.inner_group.some_repo_name --topic my-topic --path repos/extern/inner_group/some_repo_name --storage-profile topic_repo --create",
    ),
    "project paths materialize-default": (
        "pixi run isomer-cli --print-json project paths materialize-default --topic my-topic --label topic.records.artifacts",
        "pixi run isomer-cli --print-json project paths materialize-default --topic my-topic --agent alice --label agent.private_artifacts",
    ),
    "project topics": (
        "pixi run isomer-cli --print-json project topics list",
        "pixi run isomer-cli project topics create my-topic --statement \"Investigate the concrete research question.\"",
        "pixi run isomer-cli --print-json project topics show my-topic",
    ),
    "project topics create": (
        "pixi run isomer-cli project topics create my-topic --statement \"Investigate the concrete research question.\"",
        "pixi run isomer-cli project topics create my-topic --statement \"Investigate the concrete research question.\" --workspace-dir topic-workspaces/my-topic --set-default",
    ),
    "project validate": (
        "pixi run isomer-cli --print-json project validate",
        "pixi run isomer-cli --print-json project --root tests/fixtures/projects/deepsci-profile-use-cases validate",
    ),
    "schemas": (
        "pixi run isomer-cli --print-json schemas list",
    ),
    "schemas list": (
        "pixi run isomer-cli --print-json schemas list",
    ),
}


def examples_for_command(command_path: str, *, limit: int = 3) -> tuple[str, ...]:
    """Return examples for the nearest known public command path."""

    parts = command_path.split()
    while parts:
        key = " ".join(parts)
        examples = COMMAND_EXAMPLES.get(key)
        if examples:
            return examples[:limit]
        parts = parts[:-1]
    return COMMAND_EXAMPLES["project"][:limit]
