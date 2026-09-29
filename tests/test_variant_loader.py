"""Tests for inverter-family detection and optional variant loading."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from custom_components.lxp_modbus.utils import inverter_family_prefix
from custom_components.lxp_modbus.variant_loader import (
    load_variant_module,
    merge_named_definitions,
)


def test_gen_model_maps_to_gen_family():
    """GEN model prefixes select the GEN variant."""
    assert inverter_family_prefix("GEN-5K") == "GEN"


def test_lxp_model_maps_to_lxp_family():
    """LXP model prefixes select the LXP variant."""
    assert inverter_family_prefix("LXP-12K") == "LXP"


def test_family_detection_is_case_insensitive():
    """Model-family detection ignores case and surrounding whitespace."""
    assert inverter_family_prefix(" lxp-5k ") == "LXP"
    assert inverter_family_prefix(" gen-5k ") == "GEN"


def test_unknown_model_maps_to_unknown_family():
    """Unrecognised models use the shared definitions only."""
    assert inverter_family_prefix("SOMETHING-ELSE") == "UNKNOWN"


def test_missing_model_maps_to_unknown_family():
    """Missing model data is safe."""
    assert inverter_family_prefix(None) == "UNKNOWN"
    assert inverter_family_prefix("") == "UNKNOWN"


def test_unknown_family_has_no_variant_module():
    """UNKNOWN does not attempt to load a variant file."""
    module = load_variant_module(
        "custom_components.lxp_modbus.entity_descriptions.number_types",
        "UNKNOWN",
    )

    assert module is None


def test_missing_variant_file_is_ignored():
    """A family without a variant file falls back to shared definitions."""
    module = load_variant_module(
        "custom_components.lxp_modbus.entity_descriptions.number_types",
        "LXP",
    )

    # This assumes number_types_LXP.py does not exist yet.
    assert module is None


def test_existing_gen_variant_file_is_loaded():
    """The GEN number-type variant is discovered by filename."""
    module = load_variant_module(
        "custom_components.lxp_modbus.entity_descriptions.number_types",
        "GEN",
    )

    assert module is not None
    assert hasattr(module, "NUMBER_TYPES")


def test_merge_replaces_matching_definition():
    """A variant entry with the same name replaces the base entry."""
    base = [
        {"name": "Shared", "value": "base"},
        {"name": "Unchanged", "value": "base"},
    ]
    variant = [
        {"name": "Shared", "value": "variant"},
    ]

    result = merge_named_definitions(base, variant)

    assert result == [
        {"name": "Shared", "value": "variant"},
        {"name": "Unchanged", "value": "base"},
    ]


def test_merge_appends_new_definition():
    """A variant entry with a new name is appended."""
    base = [
        {"name": "Shared", "value": "base"},
    ]
    variant = [
        {"name": "Additional", "value": "variant"},
    ]

    result = merge_named_definitions(base, variant)

    assert result == [
        {"name": "Shared", "value": "base"},
        {"name": "Additional", "value": "variant"},
    ]