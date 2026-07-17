"""Click registration for Operation Set Acceptance commands."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Callable

import click

from isomer_labs.cli.options import common_options, topic_selection_options
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.records.operation_sets import (
    apply_operation_set_acceptance,
    inspect_operation_set,
    plan_operation_set_acceptance,
    verify_operation_set_acceptance,
)


ContextRunner = Callable[..., int]


def register_research_operation_set_commands(
    research_group: click.Group,
    *,
    with_context: ContextRunner,
) -> None:
    """Register receipt-backed operation-set inspection, acceptance, and verification."""

    @research_group.group(
        name="operation-sets",
        help="Inspect, accept, and verify worker operation-set research outputs.",
    )
    def operation_sets_group() -> None:
        pass

    @operation_sets_group.command(
        name="inspect",
        help="Inventory an operation set and compare its explicit acceptance manifest.",
    )
    @common_options
    @topic_selection_options
    @_worker_options
    @click.option(
        "--manifest-path",
        type=click.Path(path_type=Path),
        default=None,
        help="Optional acceptance manifest to compare inside the reserved control directory.",
    )
    @click.option(
        "--write-scaffold",
        is_flag=True,
        help="Write one visibly incomplete manifest scaffold; never overwrites an existing manifest.",
    )
    @click.argument("operation_set_path", type=click.Path(path_type=Path))
    @click.pass_context
    def inspect_command(
        ctx: click.Context,
        operation_set_path: Path,
        agent_name: str | None = None,
        topic_actor_name: str | None = None,
        manifest_path: Path | None = None,
        write_scaffold: bool = False,
        **kwargs: Any,
    ) -> int:
        return with_context(
            ctx,
            dict(kwargs),
            lambda context, _request: inspect_operation_set(
                context,
                operation_set_path,
                env=os.environ,
                cwd=Path.cwd(),
                agent_name=agent_name,
                topic_actor_name=topic_actor_name,
                manifest_path=manifest_path,
                write_scaffold=write_scaffold,
            ),
            build_request=False,
        )

    @operation_sets_group.command(
        name="accept",
        help="Preview a complete acceptance plan; add --apply to mutate records and receipts.",
    )
    @common_options
    @topic_selection_options
    @_worker_options
    @click.option(
        "--apply",
        "apply_changes",
        is_flag=True,
        help="Apply the preflighted plan as a resumable receipt-backed saga.",
    )
    @click.argument("manifest_path", type=click.Path(path_type=Path))
    @click.pass_context
    def accept_command(
        ctx: click.Context,
        manifest_path: Path,
        agent_name: str | None = None,
        topic_actor_name: str | None = None,
        apply_changes: bool = False,
        **kwargs: Any,
    ) -> int:
        def accept(context: EffectiveTopicContext, _request: object) -> tuple[dict[str, Any], list[Any]]:
            callback = apply_operation_set_acceptance if apply_changes else plan_operation_set_acceptance
            return callback(
                context,
                manifest_path,
                env=os.environ,
                cwd=Path.cwd(),
                agent_name=agent_name,
                topic_actor_name=topic_actor_name,
            )

        return with_context(ctx, dict(kwargs), accept, build_request=False)

    @operation_sets_group.command(
        name="verify",
        help="Verify a receipt or the latest receipt for an operation-set id without repair.",
    )
    @common_options
    @topic_selection_options
    @click.argument("receipt_or_operation_set_id")
    @click.pass_context
    def verify_command(
        ctx: click.Context,
        receipt_or_operation_set_id: str,
        **kwargs: Any,
    ) -> int:
        return with_context(
            ctx,
            dict(kwargs),
            lambda context, _request: verify_operation_set_acceptance(
                context,
                receipt_or_operation_set_id,
                env=os.environ,
            ),
            build_request=False,
        )


def _worker_options(command: Any) -> Any:
    command = click.option(
        "--topic-actor",
        "topic_actor_name",
        default=None,
        help="Topic Actor whose resolved output policy owns the operation set.",
    )(command)
    command = click.option(
        "--agent",
        "agent_name",
        default=None,
        help="Agent whose resolved output policy owns the operation set.",
    )(command)
    return command
