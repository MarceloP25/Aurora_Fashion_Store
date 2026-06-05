"""Central seed control for deterministic generation."""

from __future__ import annotations

from aurora_fashion_club.utils import set_seed


def build_rng(seed: int):
    """Return a NumPy random generator configured with the project seed."""
    return set_seed(seed)
