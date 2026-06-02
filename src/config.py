from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class ProjectConfig:
    seed: int = 42
    n_customers: int = 5_000
    n_products: int = 1_000
    n_campaigns: int = 180
    start_date: str = "2023-01-01"
    end_date: str = "2025-12-31"
    output_dir: Path = field(default_factory=lambda: Path("data"))

    # scale controls
    avg_orders_per_customer: float = 4.5
    avg_interactions_per_customer: float = 10.0
    avg_digital_events_per_customer: float = 18.0
    support_ticket_rate: float = 0.08

    def resolved_output_dir(self, project_root: Path | None = None) -> Path:
        if self.output_dir.is_absolute():
            return self.output_dir
        root = project_root or Path(__file__).resolve().parents[1]
        return (root / self.output_dir).resolve()
