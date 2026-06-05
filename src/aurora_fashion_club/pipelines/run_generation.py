"""Stage 1 orchestration: synthetic data generation.

This pipeline builds the raw synthetic dataset and persists it in three
delivery forms:
- CSV files in the bronze layer and export folder;
- JSON records for interoperability;
- SQLite for relational querying.
"""

from __future__ import annotations

from aurora_fashion_club.config.settings import load_config
from aurora_fashion_club.config.seeds import build_rng
from aurora_fashion_club.exports.export_data import export_bronze, export_csv, export_json, export_sqlite
from aurora_fashion_club.generators.campaign_generator import CampaignGenerator
from aurora_fashion_club.generators.customer_generator import CustomerGenerator
from aurora_fashion_club.generators.digital_event_generator import DigitalEventGenerator
from aurora_fashion_club.generators.interaction_generator import InteractionGenerator
from aurora_fashion_club.generators.order_generator import OrderGenerator
from aurora_fashion_club.generators.product_generator import ProductGenerator
from aurora_fashion_club.generators.support_generator import SupportTicketGenerator
from aurora_fashion_club.utils import ensure_dir


def main() -> dict[str, object]:
    """Generate the complete stage-1 dataset and persist all raw outputs."""
    config = load_config()
    rng = build_rng(config.project.seed)

    bronze = ensure_dir(config.paths.bronze)
    exports = ensure_dir(config.paths.exports)

    customers = CustomerGenerator(config.generation.customers, rng).generate()
    products = ProductGenerator(config.generation.products, rng).generate()
    campaigns = CampaignGenerator(config.generation.campaigns, rng).generate()
    orders, order_items = OrderGenerator(rng).generate(customers, products)
    interactions = InteractionGenerator(config.generation.interactions, rng).generate(customers, campaigns)
    support_tickets = SupportTicketGenerator(config.generation.support_tickets, rng).generate(customers)
    digital_events = DigitalEventGenerator(config.generation.digital_events, rng).generate(customers)

    tables = {
        "customers": customers,
        "products": products,
        "orders": orders,
        "order_items": order_items,
        "campaigns": campaigns,
        "interactions": interactions,
        "support_tickets": support_tickets,
        "digital_events": digital_events,
    }

    export_csv(tables, exports / "csv")
    export_bronze(tables, bronze)
    export_json(tables, exports / "json")
    export_sqlite(tables, exports / "sqlite" / "aurora_fashion_club.db")

    print("[generation] raw tables written successfully")
    for name, df in tables.items():
        print(f" - {name}: {len(df):,} rows")

    return tables


if __name__ == "__main__":
    main()
