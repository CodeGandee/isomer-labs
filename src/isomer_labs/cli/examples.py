"""Public CLI examples used by docs and invocation diagnostics."""

from __future__ import annotations


COMMAND_EXAMPLES: dict[str, tuple[str, ...]] = {
    "project": (
        "isomer-cli --print-json project validate",
        "isomer-cli --print-json project topics list",
        "isomer-cli --print-json project context show",
    ),
    "doctor": (
        "isomer-cli --print-json doctor",
        "isomer-cli --print-json doctor --with-topic my-topic",
    ),
    "project paths": (
        "isomer-cli --print-json project paths get topic.records.artifacts --topic my-topic",
        "isomer-cli --print-json project paths list --topic my-topic --agent alice",
        "isomer-cli --print-json project paths default topic.repos.sources.method --topic my-topic",
    ),
    "project paths get": (
        "isomer-cli --print-json project paths get topic.records.artifacts --topic my-topic",
        "isomer-cli --print-json project paths get topic.repos.main --topic my-topic --configured",
        "isomer-cli --print-json project paths get agent.output_root --topic my-topic --agent alice",
    ),
    "project outputs policy": (
        "isomer-cli --print-json project outputs policy --topic my-topic --agent alice",
        "isomer-cli --print-json project outputs policy --topic my-topic --topic-actor operator",
    ),
    "project paths register": (
        "isomer-cli --print-json project paths register custom.datasets.raw --topic my-topic --path data/raw --storage-profile topic_records_dir --create",
        "isomer-cli --print-json project paths register topic.repos.inner_group.some_repo_name --topic my-topic --path repos/extern/inner_group/some_repo_name --storage-profile topic_repo --create",
    ),
    "project paths materialize-default": (
        "isomer-cli --print-json project paths materialize-default --topic my-topic --label topic.records.artifacts",
        "isomer-cli --print-json project paths materialize-default --topic my-topic --agent alice --label agent.private_artifacts",
    ),
    "project repos": (
        "isomer-cli --print-json project repos register sources.method --topic my-topic --path repos/extern/sources/method",
        "isomer-cli --print-json project repos create tools.benchmarks --topic my-topic",
    ),
    "project repos register": (
        "isomer-cli --print-json project repos register sources.method --topic my-topic --path repos/extern/sources/method",
    ),
    "project topics": (
        "isomer-cli --print-json project topics list",
        "isomer-cli project topics create my-topic --statement \"Investigate the concrete research question.\"",
        "isomer-cli --print-json project topics show my-topic",
    ),
    "project topics create": (
        "isomer-cli project topics create my-topic --statement \"Investigate the concrete research question.\"",
        "isomer-cli project topics create my-topic --statement \"Investigate the concrete research question.\" --workspace-dir topic-workspaces/my-topic --set-default",
    ),
    "project validate": (
        "isomer-cli --print-json project validate",
        "isomer-cli --print-json project --root /path/to/project validate",
    ),
    "schemas": (
        "isomer-cli --print-json schemas list",
    ),
    "schemas list": (
        "isomer-cli --print-json schemas list",
    ),
    "ext research templates": (
        "isomer-cli --print-json ext research templates list",
        "isomer-cli --print-json ext research templates show --name main",
        "isomer-cli --print-json ext kaoju paper template list --topic my-topic",
    ),
    "ext kaoju paper template": (
        "isomer-cli --print-json ext kaoju paper template list --topic my-topic",
        "isomer-cli --print-json ext kaoju paper template show --topic my-topic --name main",
        "isomer-cli --print-json ext kaoju paper template export --topic my-topic --name main --actor agent:writer",
    ),
    "ext research records": (
        "isomer-cli --print-json ext research records list --topic my-topic",
        "isomer-cli --print-json ext research records show <record-id> --topic my-topic",
        "isomer-cli --print-json ext research records create --topic my-topic --record-kind artifact",
    ),
    "ext research ideas": (
        "isomer-cli --print-json ext research ideas list --topic my-topic",
        "isomer-cli --print-json ext research ideas graph --topic my-topic",
        "isomer-cli --print-json ext research ideas validate --topic my-topic",
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
