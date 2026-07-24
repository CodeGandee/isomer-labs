"""Local-only CLI commands for canonical literature observations and projections."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import click

from isomer_labs.cli.options import (
    common_options as _common_options,
    topic_selection_options as _topic_selection_options,
)
from isomer_labs.records.literature import (
    list_literature_observations,
    query_literature_citations,
    query_literature_papers,
    rebuild_literature_index,
    record_literature_observation,
    show_literature_observation,
    validate_literature_index,
)


def register_literature_commands(research_group: click.Group, *, with_context: Any) -> None:
    """Register provider-neutral local data commands under ``ext research``."""

    @research_group.group(
        name="literature",
        help="Validate, record, index, and query Isomer-owned local literature data; performs no provider or network I/O.",
    )
    def literature_group() -> None:
        pass

    @literature_group.command(
        name="record",
        help="Record one normalized logical literature action from a local payload file; performs no provider I/O.",
    )
    @_common_options
    @_topic_selection_options
    @click.option(
        "--payload-file",
        type=click.Path(path_type=Path, dir_okay=False),
        required=True,
        help="Provider-neutral isomer-literature-provider-observation.v1 JSON file.",
    )
    @click.pass_context
    def record_command(ctx: click.Context, payload_file: Path, **kwargs: Any) -> int:
        values = {**kwargs, "payload_file": payload_file}
        return with_context(
            ctx,
            values,
            lambda context, _request: record_literature_observation(
                context,
                payload_file,
                env=os.environ,
                cwd=Path.cwd(),
            ),
            build_request=False,
        )

    @literature_group.group(
        name="observations",
        help="Inspect canonical local literature observations; performs no provider I/O.",
    )
    def observations_group() -> None:
        pass

    @observations_group.command(
        name="list",
        help="List canonical local literature observations with validation and projection posture.",
    )
    @_common_options
    @_topic_selection_options
    @click.option("--limit", type=int, default=None, help="Maximum observations to return; defaults to 100.")
    @click.pass_context
    def observations_list_command(ctx: click.Context, limit: int | None, **kwargs: Any) -> int:
        return with_context(
            ctx,
            kwargs,
            lambda context, _request: list_literature_observations(context, env=os.environ, limit=limit),
            build_request=False,
        )

    @observations_group.command(
        name="show",
        help="Show one canonical local literature observation with validation and projection posture.",
    )
    @_common_options
    @_topic_selection_options
    @click.argument("observation_id")
    @click.pass_context
    def observations_show_command(ctx: click.Context, observation_id: str, **kwargs: Any) -> int:
        return with_context(
            ctx,
            kwargs,
            lambda context, _request: show_literature_observation(
                context,
                observation_id,
                env=os.environ,
            ),
            build_request=False,
        )

    @literature_group.group(
        name="papers",
        help="Query derived normalized paper occurrences in the local literature index; performs no provider I/O.",
    )
    def papers_group() -> None:
        pass

    @papers_group.command(
        name="query",
        help="Query local paper occurrences by a provider-neutral selector; this command does not search a provider.",
    )
    @_common_options
    @_topic_selection_options
    @click.option("--doi", default=None, help="Normalized or URL-form DOI selector.")
    @click.option("--arxiv-id", "--arxiv", "arxiv_id", default=None, help="arXiv identifier selector.")
    @click.option(
        "--provider-qualified-id",
        "--provider-id",
        "provider_id",
        default=None,
        help="Provider-qualified selector in PROVIDER:ID form.",
    )
    @click.option("--title", default=None, help="Exact case-insensitive normalized title selector.")
    @click.option("--year", type=int, default=None, help="Publication year selector.")
    @click.option("--observation-ref", default=None, help="Canonical source observation id selector.")
    @click.option("--limit", type=int, default=None, help="Maximum occurrences to return; defaults to 100.")
    @click.pass_context
    def papers_query_command(ctx: click.Context, **kwargs: Any) -> int:
        values = dict(kwargs)
        return with_context(
            ctx,
            values,
            lambda context, _request: query_literature_papers(
                context,
                env=os.environ,
                doi=values.get("doi"),
                arxiv_id=values.get("arxiv_id"),
                provider_id=values.get("provider_id"),
                title=values.get("title"),
                year=values.get("year"),
                observation_ref=values.get("observation_ref"),
                limit=values.get("limit"),
            ),
            build_request=False,
        )

    @literature_group.group(
        name="citations",
        help="Query provider-reported citation edges in the local literature index; performs no provider I/O.",
    )
    def citations_group() -> None:
        pass

    @citations_group.command(
        name="query",
        help="Query local provider-reported citation edges; this command does not fetch citations or references.",
    )
    @_common_options
    @_topic_selection_options
    @click.option("--paper-key", default=None, help="Normalized paper key at either citation endpoint.")
    @click.option("--observation-ref", default=None, help="Canonical source observation id selector.")
    @click.option(
        "--direction",
        type=click.Choice(("forward", "backward")),
        default=None,
        help="Route direction relative to the action target.",
    )
    @click.option("--limit", type=int, default=None, help="Maximum edges to return; defaults to 100.")
    @click.pass_context
    def citations_query_command(ctx: click.Context, **kwargs: Any) -> int:
        values = dict(kwargs)
        return with_context(
            ctx,
            values,
            lambda context, _request: query_literature_citations(
                context,
                env=os.environ,
                paper_key=values.get("paper_key"),
                observation_ref=values.get("observation_ref"),
                direction=values.get("direction"),
                limit=values.get("limit"),
            ),
            build_request=False,
        )

    @literature_group.group(
        name="index",
        help="Manage the independently versioned local literature query projection; performs no provider I/O.",
    )
    def index_group() -> None:
        pass

    @index_group.command(
        name="rebuild",
        help="Explicitly replace only derived isomer-literature-query-index.v1 rows from canonical observations.",
    )
    @_common_options
    @_topic_selection_options
    @click.pass_context
    def index_rebuild_command(ctx: click.Context, **kwargs: Any) -> int:
        return with_context(
            ctx,
            kwargs,
            lambda context, _request: rebuild_literature_index(context, env=os.environ),
            build_request=False,
        )

    @index_group.command(
        name="validate",
        help="Validate the local literature projection without creating, migrating, repairing, or rebuilding it.",
    )
    @_common_options
    @_topic_selection_options
    @click.pass_context
    def index_validate_command(ctx: click.Context, **kwargs: Any) -> int:
        return with_context(
            ctx,
            kwargs,
            lambda context, _request: validate_literature_index(context, env=os.environ),
            build_request=False,
        )
