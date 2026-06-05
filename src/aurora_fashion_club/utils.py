"""Small reusable helpers for the synthetic data layer.

The goal here is to keep generators compact, deterministic, and readable.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import sqlite3

import numpy as np
import pandas as pd


def set_seed(seed: int) -> np.random.Generator:
    """Set NumPy's global seed and return a local generator."""
    np.random.seed(seed)
    return np.random.default_rng(seed)


def clamp(values, low, high):
    """Clamp scalar or array-like values into a bounded range."""
    return np.clip(values, low, high)


def make_ids(prefix: str, n: int, width: int = 7) -> list[str]:
    """Build stable string identifiers such as CUST0000001."""
    return [f"{prefix}{i:0{width}d}" for i in range(1, n + 1)]


def weighted_choice(rng: np.random.Generator, values: list, weights: list[float], size: int) -> np.ndarray:
    """Vectorized weighted sampling."""
    w = np.array(weights, dtype=float)
    w = w / w.sum()
    return rng.choice(values, size=size, p=w)


def sample_dates(
    rng: np.random.Generator,
    start: str,
    end: str,
    size: int,
) -> pd.DatetimeIndex:
    """Sample random timestamps between two dates."""
    start_ts = pd.Timestamp(start).value // 10**9
    end_ts = pd.Timestamp(end).value // 10**9
    random_ts = rng.integers(start_ts, end_ts, size=size)
    return pd.to_datetime(random_ts, unit="s")


def save_sqlite(tables: dict[str, pd.DataFrame], path: str | Path) -> None:
    """Persist a dictionary of DataFrames into a SQLite database."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        for name, df in tables.items():
            df.to_sql(name, conn, if_exists="replace", index=False)


def ensure_dir(path: str | Path) -> Path:
    """Create a directory if it does not exist and return it as Path."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p
