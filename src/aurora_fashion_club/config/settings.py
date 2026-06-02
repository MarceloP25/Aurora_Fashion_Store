from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import yaml


@dataclass(frozen=True)
class ProjectSettings:
    name: str
    seed: int
    base_currency: str


@dataclass(frozen=True)
class GenerationSettings:
    customers: int
    products: int
    orders: int
    order_items_max_per_order: int
    campaigns: int
    interactions: int
    support_tickets: int
    digital_events: int


@dataclass(frozen=True)
class PathSettings:
    data_root: Path
    bronze: Path
    silver: Path
    gold: Path
    exports: Path
    feature_store: Path


@dataclass(frozen=True)
class AppConfig:
    project: ProjectSettings
    generation: GenerationSettings
    paths: PathSettings


def _load_yaml(path: str | Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_config(path: str | Path = "config.yaml") -> AppConfig:
    raw = _load_yaml(path)

    project = ProjectSettings(**raw["project"])
    generation = GenerationSettings(**raw["generation"])
    paths_raw = raw["paths"]
    paths = PathSettings(
        data_root=Path(paths_raw["data_root"]),
        bronze=Path(paths_raw["bronze"]),
        silver=Path(paths_raw["silver"]),
        gold=Path(paths_raw["gold"]),
        exports=Path(paths_raw["exports"]),
        feature_store=Path(paths_raw["feature_store"]),
    )
    return AppConfig(project=project, generation=generation, paths=paths)
