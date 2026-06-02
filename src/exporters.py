from __future__ import annotations

from pathlib import Path
import json
import sqlite3

import pandas as pd
from openpyxl import Workbook

from .utils import ensure_directory, to_json_serializable


TABLE_ORDER = [
    "customers", "products", "orders", "order_items",
    "campaigns", "interactions", "support_tickets", "digital_events"
]


def export_csv(bundle, out_dir: Path) -> None:
    csv_dir = ensure_directory(out_dir / "csv")
    for name in TABLE_ORDER:
        getattr(bundle, name).to_csv(csv_dir / f"{name}.csv", index=False)


def export_json(bundle, out_dir: Path) -> None:
    json_dir = ensure_directory(out_dir / "json")
    payload = {}
    for name in TABLE_ORDER:
        df = getattr(bundle, name)
        payload[name] = json.loads(df.to_json(orient="records", date_format="iso"))
    with open(json_dir / "aurora_fashion_club.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=to_json_serializable)


def export_xlsx(bundle, out_dir: Path) -> None:
    xlsx_dir = ensure_directory(out_dir / "xlsx")
    file_path = xlsx_dir / "aurora_fashion_club.xlsx"
    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        for name in TABLE_ORDER:
            getattr(bundle, name).to_excel(writer, sheet_name=name[:31], index=False)


def export_sqlite(bundle, out_dir: Path) -> None:
    sqlite_dir = ensure_directory(out_dir / "sqlite")
    db_path = sqlite_dir / "aurora_fashion_club.sqlite"
    conn = sqlite3.connect(db_path)
    try:
        for name in TABLE_ORDER:
            df = getattr(bundle, name)
            df.to_sql(name, conn, if_exists="replace", index=False)
        # add indexes
        cur = conn.cursor()
        cur.execute("CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_interactions_customer_id ON interactions(customer_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_interactions_campaign_id ON interactions(campaign_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_tickets_customer_id ON support_tickets(customer_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_events_customer_id ON digital_events(customer_id);")
        conn.commit()
    finally:
        conn.close()


def export_bronze_silver_gold(bundle, out_dir: Path) -> None:
    bronze = ensure_directory(out_dir / "bronze")
    silver = ensure_directory(out_dir / "silver")
    gold = ensure_directory(out_dir / "gold")

    # bronze: raw
    for name in TABLE_ORDER:
        getattr(bundle, name).to_csv(bronze / f"{name}.csv", index=False)

    # silver: cleaned, with internal segment removed from customers
    for name in TABLE_ORDER:
        df = getattr(bundle, name).copy()
        if "_synthetic_segment" in df.columns:
            df = df.drop(columns=["_synthetic_segment"])
        df.to_csv(silver / f"{name}.csv", index=False)

    # gold: business-ready tables
    customers = bundle.customers.copy()
    if "_synthetic_segment" in customers.columns:
        customers = customers.drop(columns=["_synthetic_segment"])
    gold_tables = {
        "customer_features": customers,
        "campaign_summary": bundle.campaigns,
        "product_catalog": bundle.products,
    }
    for name, df in gold_tables.items():
        df.to_csv(gold / f"{name}.csv", index=False)


def export_all(bundle, out_dir: Path) -> None:
    ensure_directory(out_dir)
    export_csv(bundle, out_dir)
    export_json(bundle, out_dir)
    export_xlsx(bundle, out_dir)
    export_sqlite(bundle, out_dir)
    export_bronze_silver_gold(bundle, out_dir)
