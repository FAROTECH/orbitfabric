from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, model_validator

from .errors import ReleaseResolutionError
from .models import AdapterSourceCoordinate, Sha256, StrictModel


class CatalogDigest(StrictModel):
    algorithm: Literal["sha256"]
    value: Sha256


class CatalogReleaseSourceRef(StrictModel):
    binding: str = Field(min_length=1)
    release_ref: str = Field(min_length=1)


class CatalogReleaseRecord(StrictModel):
    version: str = Field(min_length=1)
    release_descriptor_digest: CatalogDigest
    sources: list[CatalogReleaseSourceRef] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_source_refs(self) -> CatalogReleaseRecord:
        refs = [(source.binding, source.release_ref) for source in self.sources]
        if len(refs) != len(set(refs)):
            raise ValueError("Catalog release source references must be unique")
        return self


class CatalogAdapterRecord(StrictModel):
    source_coordinate: AdapterSourceCoordinate
    releases: list[CatalogReleaseRecord] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_release_versions(self) -> CatalogAdapterRecord:
        versions = [release.version for release in self.releases]
        if len(versions) != len(set(versions)):
            raise ValueError("Catalog release versions must be unique per adapter")
        return self


class CatalogSourceBinding(StrictModel):
    id: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    config: dict[str, Any] = Field(default_factory=dict)


class AdapterCatalog(StrictModel):
    kind: Literal["orbitfabric.adapter_catalog"]
    catalog_version: Literal["0.1-candidate"]
    adapters: list[CatalogAdapterRecord] = Field(min_length=1)
    source_bindings: list[CatalogSourceBinding] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_catalog_identity_and_bindings(self) -> AdapterCatalog:
        coordinates = [
            _coordinate_tuple(adapter.source_coordinate) for adapter in self.adapters
        ]
        if len(coordinates) != len(set(coordinates)):
            raise ValueError("Catalog Source Coordinates must be unique")

        binding_ids = [binding.id for binding in self.source_bindings]
        if len(binding_ids) != len(set(binding_ids)):
            raise ValueError("Catalog source binding ids must be unique")

        known_bindings = set(binding_ids)
        for adapter in self.adapters:
            for release in adapter.releases:
                for source in release.sources:
                    if source.binding not in known_bindings:
                        raise ValueError(
                            "Catalog release source binding reference is unresolved: "
                            f"{source.binding}"
                        )
        return self


class ExactCatalogReleaseSource(StrictModel):
    binding: CatalogSourceBinding
    release_ref: str = Field(min_length=1)


class ExactCatalogReleaseSelection(StrictModel):
    source_coordinate: AdapterSourceCoordinate
    release_version: str = Field(min_length=1)
    release_descriptor_digest: CatalogDigest
    sources: list[ExactCatalogReleaseSource] = Field(min_length=1)


def select_exact_release(
    catalog: AdapterCatalog,
    source_coordinate: AdapterSourceCoordinate,
    release_version: str,
) -> ExactCatalogReleaseSelection:
    adapters = [
        adapter
        for adapter in catalog.adapters
        if _coordinate_tuple(adapter.source_coordinate)
        == _coordinate_tuple(source_coordinate)
    ]
    if len(adapters) != 1:
        raise ReleaseResolutionError(
            "Expected one Catalog adapter for Source Coordinate "
            f"{source_coordinate.display()}, found {len(adapters)}"
        )

    releases = [
        release
        for release in adapters[0].releases
        if release.version == release_version
    ]
    if len(releases) != 1:
        raise ReleaseResolutionError(
            "Expected one exact Catalog release "
            f"{source_coordinate.display()}@{release_version}, found {len(releases)}"
        )

    release = releases[0]
    resolved_sources = [
        ExactCatalogReleaseSource(
            binding=_resolve_binding(catalog, source.binding),
            release_ref=source.release_ref,
        )
        for source in release.sources
    ]
    return ExactCatalogReleaseSelection(
        source_coordinate=adapters[0].source_coordinate,
        release_version=release.version,
        release_descriptor_digest=release.release_descriptor_digest,
        sources=resolved_sources,
    )


def select_exact_release_by_logical_key(
    catalog: AdapterCatalog,
    *,
    publisher: str,
    name: str,
    release_version: str,
) -> ExactCatalogReleaseSelection:
    adapters = [
        adapter
        for adapter in catalog.adapters
        if adapter.source_coordinate.publisher == publisher
        and adapter.source_coordinate.name == name
    ]
    if len(adapters) != 1:
        raise ReleaseResolutionError(
            "Expected one Catalog Source Coordinate for logical key "
            f"{publisher}/{name}, found {len(adapters)}"
        )
    return select_exact_release(
        catalog,
        adapters[0].source_coordinate,
        release_version,
    )


def _resolve_binding(
    catalog: AdapterCatalog,
    binding_id: str,
) -> CatalogSourceBinding:
    matches = [
        binding for binding in catalog.source_bindings if binding.id == binding_id
    ]
    if len(matches) != 1:
        raise ReleaseResolutionError(
            "Expected one Catalog source binding "
            f"{binding_id!r}, found {len(matches)}"
        )
    return matches[0]


def _coordinate_tuple(
    coordinate: AdapterSourceCoordinate,
) -> tuple[str, str, str]:
    return coordinate.authority, coordinate.publisher, coordinate.name
