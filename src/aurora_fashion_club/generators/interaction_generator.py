"""CRM interaction generator linked to campaigns and customer traits."""

from __future__ import annotations

import numpy as np
import pandas as pd

from aurora_fashion_club.config.constants import INTERACTION_TYPES, MESSAGE_THEMES
from aurora_fashion_club.utils import make_ids


class InteractionGenerator:
    """Generate customer-level interactions derived from campaign pressure."""

    def __init__(self, n_interactions: int, rng: np.random.Generator):
        self.n = n_interactions
        self.rng = rng

    def generate(self, customers: pd.DataFrame, campaigns: pd.DataFrame) -> pd.DataFrame:
        customer_pool = customers["customer_id"].to_numpy()
        campaign_pool = campaigns["campaign_id"].to_numpy()

        sampled_customers = self.rng.choice(customer_pool, size=self.n, replace=True)
        sampled_campaigns = self.rng.choice(campaign_pool, size=self.n, replace=True)

        cust_lookup = customers.set_index("customer_id")
        camp_lookup = campaigns.set_index("campaign_id")

        interaction_type = []
        response_flag = []
        conversion_flag = []
        channel = []
        interaction_date = []
        message_theme = []

        for cid, cmp_id in zip(sampled_customers, sampled_campaigns):
            cust = cust_lookup.loc[cid]
            camp = camp_lookup.loc[cmp_id]
            prob_response = float(np.clip(cust["email_open_rate"] * 0.55 + cust["campaign_conversion_rate"] * 0.8, 0.03, 0.92))
            prob_conversion = float(np.clip(prob_response * 0.45 + camp["conversions"] / max(camp["impressions"], 1) * 1.2, 0.01, 0.55))
            response = int(self.rng.random() < prob_response)
            conversion = int(response and self.rng.random() < prob_conversion)
            response_flag.append(response)
            conversion_flag.append(conversion)
            channel.append(camp["channel"])
            interaction_type.append(self.rng.choice(INTERACTION_TYPES, p=[0.38, 0.22, 0.10, 0.18, 0.12] if response else [0.05, 0.05, 0.05, 0.02, 0.83]))
            interaction_date.append(pd.Timestamp(camp["send_date"]) + pd.Timedelta(days=int(self.rng.integers(0, 5 if response else 10))))
            message_theme.append(self.rng.choice(MESSAGE_THEMES))

        return pd.DataFrame(
            {
                "interaction_id": make_ids("INT", self.n),
                "customer_id": sampled_customers,
                "interaction_date": pd.to_datetime(interaction_date).date,
                "channel": channel,
                "interaction_type": interaction_type,
                "response_flag": response_flag,
                "conversion_flag": conversion_flag,
                "campaign_id": sampled_campaigns,
                "message_theme": message_theme,
            }
        ).sort_values("interaction_date").reset_index(drop=True)
