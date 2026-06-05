"""Order and order item generator.

The module uses customer purchase propensity to build a chronological
transaction history and keeps order totals consistent with item-level lines.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd

from aurora_fashion_club.config.constants import ORDER_CHANNELS, ORDER_STATUS, PAYMENT_METHODS, SHIPPING_TYPES
from aurora_fashion_club.utils import make_ids


class OrderGenerator:
    """Generate orders and order items from customers and products."""

    def __init__(self, rng: np.random.Generator):
        self.rng = rng

    def generate(self, customers: pd.DataFrame, products: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        order_rows = []
        item_rows = []
        order_ids = make_ids("ORD", int(customers["number_of_orders"].sum()))

        order_idx = 0
        for _, cust in customers.iterrows():
            n_orders = int(cust["number_of_orders"])
            if n_orders <= 0:
                continue

            order_dates = self._customer_order_dates(cust["first_purchase_date"], cust["last_purchase_date"], n_orders)
            for order_date in order_dates:
                order_id = order_ids[order_idx]
                order_idx += 1
                n_items = int(self.rng.integers(1, 9))
                channel = self._choose_channel(cust)
                status = self._choose_status(cust)
                payment = self.rng.choice(PAYMENT_METHODS, p=[0.44, 0.22, 0.10, 0.16, 0.08])
                shipping = self.rng.choice(SHIPPING_TYPES, p=[0.62, 0.18, 0.20])
                delivery_days = int(max(1, self.rng.normal(4 if shipping == "Express" else 7 if shipping == "Standard" else 2, 1.8)))
                shipping_cost = float(np.round(0 if shipping == "Store Pickup" else self.rng.uniform(12, 38) if shipping == "Standard" else self.rng.uniform(18, 55), 2))

                items = self._build_items(order_id, cust, products, n_items)
                gross_amount = float(items["line_amount"].sum())
                discount_amount = float(items["discount_value"].sum())
                net_amount = round(gross_amount - discount_amount + shipping_cost, 2)
                return_flag = int((cust["returns_rate"] > 0.18 and self.rng.random() < 0.35) or (status == "Returned"))

                order_rows.append(
                    {
                        "order_id": order_id,
                        "customer_id": cust["customer_id"],
                        "order_date": pd.to_datetime(order_date).date(),
                        "channel": channel,
                        "order_status": status,
                        "gross_amount": round(gross_amount, 2),
                        "discount_amount": round(discount_amount, 2),
                        "net_amount": net_amount,
                        "payment_method": payment,
                        "shipping_type": shipping,
                        "shipping_cost": shipping_cost,
                        "delivery_days": delivery_days,
                        "return_flag": return_flag,
                    }
                )
                item_rows.extend(items.to_dict("records"))

        orders = pd.DataFrame(order_rows).sort_values(["customer_id", "order_date"]).reset_index(drop=True)
        order_items = pd.DataFrame(item_rows).sort_values(["order_id", "order_item_id"]).reset_index(drop=True)
        return orders, order_items

    def _customer_order_dates(self, first_purchase_date, last_purchase_date, n_orders):
        start = pd.Timestamp(first_purchase_date)
        end = pd.Timestamp(last_purchase_date)
        if end <= start:
            end = start + pd.Timedelta(days=max(30, n_orders * 15))
        offsets = np.sort(self.rng.integers(0, max((end - start).days, 1) + 1, n_orders))
        return start + pd.to_timedelta(offsets, unit="D")

    def _choose_channel(self, cust):
        p = cust["acquisition_channel"]
        if p == "Store":
            return self.rng.choice(ORDER_CHANNELS, p=[0.16, 0.12, 0.72])
        if p == "Paid Social":
            return self.rng.choice(ORDER_CHANNELS, p=[0.45, 0.40, 0.15])
        return self.rng.choice(ORDER_CHANNELS, p=[0.52, 0.34, 0.14])

    def _choose_status(self, cust):
        if cust["returns_rate"] > 0.22 and self.rng.random() < 0.20:
            return "Returned"
        if cust["churn_risk_score"] > 0.72 and self.rng.random() < 0.10:
            return "Cancelled"
        return "Completed"

    def _build_items(self, order_id, cust, products, n_items):
        preferred = products.copy()
        preferred = preferred.sample(frac=1, random_state=int(self.rng.integers(0, 1_000_000)))
        chosen = preferred.head(n_items).copy()

        qty = self.rng.integers(1, 3, size=n_items)
        base_discount = chosen["avg_discount_rate"].to_numpy()
        cust_discount = cust["discount_usage_rate"]
        discount_rate = np.clip(base_discount + cust_discount * self.rng.uniform(0.35, 0.85, n_items), 0.0, 0.55)
        unit_price = chosen["list_price"].to_numpy()
        discount_value = np.round(unit_price * qty * discount_rate, 2)
        line_amount = np.round(unit_price * qty, 2)

        items = pd.DataFrame(
            {
                "order_item_id": make_ids("OIT", n_items, width=10),
                "order_id": order_id,
                "product_id": chosen["product_id"].to_list(),
                "quantity": qty,
                "unit_price": np.round(unit_price, 2),
                "discount_value": discount_value,
                "line_amount": line_amount,
            }
        )
        return items
