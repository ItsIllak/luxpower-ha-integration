"""Load optional family-specific register and entity definitions."""

import importlib
import logging

_LOGGER = logging.getLogger(__name__)


def load_variant_module(base_module_name: str, family: str):
    """Load an optional module such as number_types_GEN.

    Missing variant modules are expected and return None. Import errors inside
    an existing variant module are not hidden.
    """
    if not family or family == "UNKNOWN":
        return None

    variant_name = f"{base_module_name}_{family}"

    try:
        return importlib.import_module(variant_name)
    except ModuleNotFoundError as err:
        if err.name == variant_name:
            return None
        raise


def merge_named_definitions(
    base_definitions: list[dict],
    variant_definitions: list[dict],
    key: str = "name",
) -> list[dict]:
    """Replace same-named base entries and append new variant entries."""
    merged = list(base_definitions)
    positions = {
        item[key]: index
        for index, item in enumerate(merged)
        if key in item
    }

    for variant in variant_definitions:
        name = variant.get(key)

        if name in positions:
            merged[positions[name]] = variant
        else:
            merged.append(variant)

    return merged