from __future__ import annotations

from orbitfabric.gen.runtime.naming import to_camel_case, to_pascal_case


def test_pascal_case_from_model_ids() -> None:
    assert to_pascal_case("payload.start_acquisition") == "PayloadStartAcquisition"
    assert to_pascal_case("payload.radiation_histogram") == "PayloadRadiationHistogram"
    assert to_pascal_case("eps.battery_warning") == "EpsBatteryWarning"
    assert to_pascal_case("SAFE") == "Safe"


def test_pascal_case_prefixes_numeric_leading_parts() -> None:
    assert to_pascal_case("3u.demo") == "N3uDemo"


def test_pascal_case_fallback_for_empty_symbol() -> None:
    assert to_pascal_case("...") == "Unnamed"


def test_camel_case_from_model_ids() -> None:
    assert to_camel_case("payload.start_acquisition") == "payloadStartAcquisition"
    assert to_camel_case("3u.demo") == "n3uDemo"
