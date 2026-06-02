from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


def set_seed(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def clamp(series_or_value, lower=None, upper=None):
    if isinstance(series_or_value, pd.Series):
        return series_or_value.clip(lower=lower, upper=upper)
    value = series_or_value
    if lower is not None:
        value = max(lower, value)
    if upper is not None:
        value = min(upper, value)
    return value


def safe_div(numerator, denominator, default=0.0):
    with np.errstate(divide="ignore", invalid="ignore"):
        result = np.where(denominator == 0, default, numerator / denominator)
    return result


def date_range_days(start: str, end: str) -> int:
    return (pd.Timestamp(end) - pd.Timestamp(start)).days + 1


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def to_json_serializable(obj: Any) -> Any:
    if is_dataclass(obj):
        return asdict(obj)
    if isinstance(obj, (pd.Timestamp, datetime)):
        return obj.isoformat()
    if isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    if isinstance(obj, (np.floating, np.float32, np.float64)):
        return float(obj)
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


def chunked(iterable, size: int):
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch
