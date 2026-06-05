"""Lightweight multi-format exporters for the bronze and delivery layers."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from aurora_fashion_club.utils import ensure_dir, save_sqlite


def export_csv(tables: dict[str, pd.DataFrame], csv_dir: str | Path) -> None:
    """Write one CSV per entity."""
    csv_dir = ensure_dir(csv_dir)
    for name, df in tables.items():
        df.to_csv(csv_dir / f"{name}.csv", index=False)


def export_bronze(tables: dict[str, pd.DataFrame], bronze_dir: str | Path) -> None:
    """Persist raw tables as the bronze reference layer.

    In stage 1, bronze is intentionally identical to the raw CSV output.
    """
    export_csv(tables, bronze_dir)


def export_json(tables: dict[str, pd.DataFrame], json_dir: str | Path) -> None:
    """Export tables to JSON records, one file per entity."""
    json_dir = ensure_dir(json_dir)
    for name, df in tables.items():
        df.to_json(json_dir / f"{name}.json", orient="records", date_format="iso")


def export_sqlite(tables: dict[str, pd.DataFrame], db_path: str | Path) -> None:
    """Store all tables inside a single SQLite database."""
    save_sqlite(tables, db_path)


def export_xlsx(tables: dict[str, pd.DataFrame], xlsx_path: str | Path) -> None:
    """Write a compact Excel workbook with one sheet per table."""
    xlsx_path = Path(xlsx_path)
    xlsx_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        for name, df in tables.items():
            df.to_excel(writer, sheet_name=name[:31], index=False)
