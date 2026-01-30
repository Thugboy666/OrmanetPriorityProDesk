from __future__ import annotations

import math
from typing import Any


def normalize_porto_franco(value: Any) -> str:
    if value is None:
        return "none"
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return "none"

    if math.isnan(numeric) or numeric <= 0:
        return "none"
    if numeric <= 300:
        return "300"
    if numeric <= 500:
        return "500"
    return "500"
