"""Digital event generator for app and web engagement."""

from __future__ import annotations

import numpy as np
import pandas as pd

from aurora_fashion_club.config.constants import DEVICE_TYPES, EVENT_TYPES
from aurora_fashion_club.utils import make_ids


class DigitalEventGenerator:
    """Generate clickstream-style events driven by customer engagement."""

    def __init__(self, n_events: int, rng: np.random.Generator):
        self.n = n_events
        self.rng = rng

    def generate(self, customers: pd.DataFrame) -> pd.DataFrame:
        weights = self._customer_weights(customers)
        sampled_customers = self.rng.choice(customers["customer_id"].to_numpy(), size=self.n, replace=True, p=weights)
        cust_lookup = customers.set_index("customer_id")

        event_type = []
        device_type = []
        session_duration = np.zeros(self.n)
        page_views = np.zeros(self.n, dtype=int)
        add_to_cart_flag = np.zeros(self.n, dtype=int)
        checkout_start_flag = np.zeros(self.n, dtype=int)
        purchase_flag = np.zeros(self.n, dtype=int)
        event_date = []

        for i, cid in enumerate(sampled_customers):
            cust = cust_lookup.loc[cid]
            base = 1 + cust["app_sessions"] / 12
            event_type.append(self._event_type(cust))
            device_type.append(self.rng.choice(DEVICE_TYPES, p=[0.78 if cust["acquisition_channel"] != "Store" else 0.55, 0.18, 0.04 if cust["acquisition_channel"] != "Store" else 0.13]))
            session_duration[i] = float(np.clip(self.rng.normal(4 + base, 2.8), 0.2, 48))
            page_views[i] = int(max(1, self.rng.poisson(2 + base)))
            add_to_cart_flag[i] = int(self.rng.random() < np.clip(0.08 + cust["campaign_conversion_rate"] * 0.8, 0.02, 0.72))
            checkout_start_flag[i] = int(add_to_cart_flag[i] and self.rng.random() < 0.55)
            purchase_flag[i] = int(checkout_start_flag[i] and self.rng.random() < np.clip(0.18 + cust["campaign_conversion_rate"], 0.04, 0.78))
            event_date.append(pd.Timestamp(cust["last_purchase_date"]) - pd.Timedelta(days=int(self.rng.integers(0, 120))))

        return pd.DataFrame(
            {
                "event_id": make_ids("EVT", self.n),
                "customer_id": sampled_customers,
                "event_date": pd.to_datetime(event_date).date,
                "event_type": event_type,
                "device_type": device_type,
                "session_duration": np.round(session_duration, 2),
                "page_views": page_views,
                "add_to_cart_flag": add_to_cart_flag,
                "checkout_start_flag": checkout_start_flag,
                "purchase_flag": purchase_flag,
            }
        ).sort_values("event_date").reset_index(drop=True)

    def _customer_weights(self, customers):
        base = customers["app_sessions"].to_numpy() + customers["campaign_exposure_count"].to_numpy() * 0.3 + 1
        return base / base.sum()

    def _event_type(self, cust):
        if cust["app_sessions"] > 12:
            return self.rng.choice(EVENT_TYPES, p=[0.18, 0.18, 0.12, 0.08, 0.06, 0.06, 0.20, 0.12])
        return self.rng.choice(EVENT_TYPES, p=[0.22, 0.18, 0.08, 0.04, 0.06, 0.04, 0.28, 0.10])
