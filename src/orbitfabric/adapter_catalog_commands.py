from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Any

import typer

from orbitfabric.adapter_manager import AdapterCatalog, AdapterManagerError, select_exact_release
from orbitfabric.adapter_manager.models import AdapterSourceCoordinate

catalog_app = typer.Typer(
    help="Inspect and select exact adapter releases from a local Adapter Catalog.",
    no_args_is_help=True,
)


def _json_echo(payload: Any) -> None:
    if hasattr(payload, "model_dump"):
        payload = payload.model_dump(mode="json")
    typer.echo(json.dumps(payload, indent=2, sort_keys=True))


def _fail(exc: Exception) -> None:
    typer.echo(f"Adapter Catalog error: {exc}", err=True)
    raise typer.Exit(code=1) from exc


def _load_catalog(path: Path) -> AdapterCatalog:
    try:
        return AdapterCatalog.model_validate_json(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError(f"Invalid Adapter Catalog {path}: {exc}") from exc


def _parse_source_coordinate(value: str) -> AdapterSourceCoordinate:
    authority, authority_separator, logical = value.partition(":")
    publisher, publisher_separator, name = logical.partition("/")
    if (
        not authority_separator
        or not publisher_separator
        or not authority.strip()
        or not publisher.strip()
        or not name.strip()
    ):
        raise ValueError("Source Coordinate must use AUTHORITY:PUBLISHER/NAME syntax")
    return AdapterSourceCoordinate(
        authority=authority.strip(),
        publisher=publisher.strip(),
        name=name.strip(),
    )


@catalog_app.command("validate")
def validate_catalog(
    catalog_path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Local Adapter Catalog JSON file.",
        ),
    ],
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Write the conformant Core Catalog model as JSON."),
    ] = False,
) -> None:
    """Validate one local Adapter Catalog with the Core-owned model."""
    try:
        catalog = _load_catalog(catalog_path)
    except ValueError as exc:
        _fail(exc)
        return

    if json_output:
        _json_echo(catalog)
        return

    release_count = sum(len(adapter.releases) for adapter in catalog.adapters)
    typer.echo(f"Adapter Catalog: {catalog_path}")
    typer.echo(f"Version: {catalog.catalog_version}")
    typer.echo(f"Adapters: {len(catalog.adapters)}")
    typer.echo(f"Releases: {release_count}")
    typer.echo(f"Source bindings: {len(catalog.source_bindings)}")
    typer.echo("Result: CONFORMANT")


@catalog_app.command("list")
def list_catalog(
    catalog_path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Local Adapter Catalog JSON file.",
        ),
    ],
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Write Core Catalog adapter records as JSON."),
    ] = False,
) -> None:
    """List exact releases recorded in one local Adapter Catalog."""
    try:
        catalog = _load_catalog(catalog_path)
    except ValueError as exc:
        _fail(exc)
        return

    if json_output:
        _json_echo([adapter.model_dump(mode="json") for adapter in catalog.adapters])
        return

    for adapter in catalog.adapters:
        for release in adapter.releases:
            typer.echo(f"{adapter.source_coordinate.display()}@{release.version}")


@catalog_app.command("select")
def select_catalog_release(
    catalog_path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Local Adapter Catalog JSON file.",
        ),
    ],
    source_coordinate: Annotated[
        str,
        typer.Argument(help="Exact Source Coordinate as AUTHORITY:PUBLISHER/NAME."),
    ],
    release_version: Annotated[
        str,
        typer.Option("--version", help="Exact release version string."),
    ],
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Write the exact Core Catalog selection as JSON."),
    ] = False,
) -> None:
    """Select one exact release by full Source Coordinate and exact version."""
    try:
        catalog = _load_catalog(catalog_path)
        coordinate = _parse_source_coordinate(source_coordinate)
        selection = select_exact_release(catalog, coordinate, release_version)
    except (AdapterManagerError, ValueError) as exc:
        _fail(exc)
        return

    if json_output:
        _json_echo(selection)
        return

    typer.echo(
        "Selected: "
        f"{selection.source_coordinate.display()}@{selection.release_version}"
    )
    typer.echo(
        "Release Descriptor: "
        f"{selection.release_descriptor_digest.algorithm}:"
        f"{selection.release_descriptor_digest.value}"
    )
    typer.echo("Sources:")
    for source in selection.sources:
        typer.echo(
            f"  {source.binding.id}  "
            f"provider={source.binding.provider}  "
            f"release_ref={source.release_ref}"
        )


__all__ = ["catalog_app"]
