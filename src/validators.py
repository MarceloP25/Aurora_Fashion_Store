from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import pandas as pd


@dataclass
class ValidationResult:
    passed: bool
    errors: List[str]
    warnings: List[str]


def validate_referential_integrity(bundle) -> ValidationResult:
    errors: List[str] = []
    warnings: List[str] = []

    customers = bundle.customers
    products = bundle.products
    orders = bundle.orders
    order_items = bundle.order_items
    campaigns = bundle.campaigns
    interactions = bundle.interactions
    support_tickets = bundle.support_tickets
    digital_events = bundle.digital_events

    if orders["customer_id"].isin(customers["customer_id"]).all() is False:
        errors.append("Orders contain invalid customer_id values.")
    if order_items["order_id"].isin(orders["order_id"]).all() is False:
        errors.append("Order items contain invalid order_id values.")
    if order_items["product_id"].isin(products["product_id"]).all() is False:
        errors.append("Order items contain invalid product_id values.")
    if interactions["customer_id"].isin(customers["customer_id"]).all() is False:
        errors.append("Interactions contain invalid customer_id values.")
    if interactions["campaign_id"].isin(campaigns["campaign_id"]).all() is False:
        errors.append("Interactions contain invalid campaign_id values.")
    if support_tickets["customer_id"].isin(customers["customer_id"]).all() is False:
        errors.append("Support tickets contain invalid customer_id values.")
    if digital_events["customer_id"].isin(customers["customer_id"]).all() is False:
        errors.append("Digital events contain invalid customer_id values.")

    # soft checks
    for name, df, cols in [
        ("customers", customers, ["customer_id"]),
        ("products", products, ["product_id"]),
        ("orders", orders, ["order_id"]),
        ("order_items", order_items, ["order_item_id"]),
        ("campaigns", campaigns, ["campaign_id"]),
        ("interactions", interactions, ["interaction_id"]),
        ("support_tickets", support_tickets, ["ticket_id"]),
        ("digital_events", digital_events, ["event_id"]),
    ]:
        dup = df.duplicated(subset=cols).sum()
        if dup:
            warnings.append(f"{name} has {dup} duplicate primary key rows.")

    # temporal sanity
    invalid_order_dates = (orders["customer_id"].map(customers.set_index("customer_id")["first_purchase_date"]) > orders["order_date"]).sum()
    if invalid_order_dates:
        warnings.append(f"{invalid_order_dates} orders occur before customer's first purchase date.")

    if (orders["gross_amount"] + 1e-6 < orders["net_amount"]).sum() > 0:
        warnings.append("Some orders have net amount greater than gross amount, verify discounts.")

    if (order_items["line_amount"] < 0).any():
        errors.append("Order items contain negative line amounts.")

    # brand style warnings
    if customers["churn_flag"].mean() < 0.05:
        warnings.append("Churn rate is very low; consider tightening the churn threshold.")
    if customers["churn_flag"].mean() > 0.6:
        warnings.append("Churn rate is very high; consider relaxing the churn threshold.")

    passed = len(errors) == 0
    return ValidationResult(passed=passed, errors=errors, warnings=warnings)
