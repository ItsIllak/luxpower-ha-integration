"""Tests for family-specific number entity definitions."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from custom_components.lxp_modbus.constants.hold_registers import (
    H_FORCED_DISCHARGE_SOC_LIMIT,
    H_FORCED_DISCHARGE_SOC_LIMIT_AND_START_TIME,
)
from custom_components.lxp_modbus.entity_descriptions.number_types import (
    get_number_types,
)


def description_for(descriptions, name):
    """Return exactly one description by entity name."""
    matches = [
        description
        for description in descriptions
        if description.get("name") == name
    ]

    assert len(matches) == 1, (
        f"Expected one description named {name!r}, found {len(matches)}"
    )

    return matches[0]


def test_lxp_uses_packed_forced_discharge_soc_register():
    """LXP keeps the SOC limit in the low byte of register 83."""
    descriptions = get_number_types("LXP-5K")
    description = description_for(
        descriptions,
        "Forced Discharge SOC Limit",
    )

    assert description["register"] == (
        H_FORCED_DISCHARGE_SOC_LIMIT_AND_START_TIME
    )
    assert "extract" in description
    assert "compose" in description

    original = (14 << 8) | 80

    assert description["extract"](original) == 80
    assert description["compose"](original, 55) == ((14 << 8) | 55)


def test_gen_uses_raw_forced_discharge_soc_register():
    """GEN treats all of register 83 as the SOC-limit value."""
    descriptions = get_number_types("GEN-5K")
    description = description_for(
        descriptions,
        "Forced Discharge SOC Limit",
    )

    assert description["register"] == H_FORCED_DISCHARGE_SOC_LIMIT
    assert "extract" not in description
    assert "compose" not in description


def test_gen_variant_does_not_change_other_number_entities():
    """The GEN file changes only the intended number entity."""
    base = get_number_types(None)
    gen = get_number_types("GEN-5K")

    base_names = [item["name"] for item in base]
gen_names = [item["name"] for item in gen]

    assert gen_names == base_names


def test_unknown_model_uses_shared_packed_behaviour():
    """Unknown models use the safe existing packed-register behaviour."""
    descriptions = get_number_types("UNRECOGNISED-MODEL")
    description = description_for(
        descriptions,
        "Forced Discharge SOC Limit",
    )

    assert description["register"] == (
        H_FORCED_DISCHARGE_SOC_LIMIT_AND_START_TIME
    )
    assert "extract" in description
    assert "compose" in description

    original = (9 << 8) | 10

    assert description["extract"](original) == 10
    assert description["compose"](original, 55) == ((9 << 8) | 55)


def test_missing_model_uses_shared_packed_behaviour():
    """Missing model information uses the shared default."""
    descriptions = get_number_types(None)
    description = description_for(
        descriptions,
        "Forced Discharge SOC Limit",
    )

    assert description["register"] == (
        H_FORCED_DISCHARGE_SOC_LIMIT_AND_START_TIME
    )
    assert "extract" in description
    assert "compose" in description
