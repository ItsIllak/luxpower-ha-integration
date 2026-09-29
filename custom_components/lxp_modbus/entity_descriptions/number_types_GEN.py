"""GEN-family number entity definitions."""

from ..constants.hold_registers import H_FORCED_DISCHARGE_SOC_LIMIT


NUMBER_TYPES = [
    {
        "name": "Forced Discharge SOC Limit",
        "register": H_FORCED_DISCHARGE_SOC_LIMIT,
        "register_type": "hold",
        "min": 0,
        "max": 100,
        "step": 1,
        "unit": "%",
        "multiplier": 1,
        "icon": "mdi:battery-20",
        "enabled": True,
        "visible": True,
        "master_only": True,
        "device_group": "Battery",
    },
]