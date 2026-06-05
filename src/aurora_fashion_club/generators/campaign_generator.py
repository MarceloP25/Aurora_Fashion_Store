"""Campaign generator for CRM performance history."""

from __future__ import annotations

import numpy as np
import pandas as pd

from aurora_fashion_club.config.constants import CAMPAIGN_CHANNELS, CAMPAIGN_TYPES, OFFER_TYPES
from aurora_fashion_club.utils import make_ids, weighted_choice


class CampaignGenerator:
    """Create campaign metadata and basic performance metrics."""

    def __init__(self, n_campaigns: int, rng: np.random.Generator):
        self.n = n_campaigns
        self.rng = rng

    def generate(self) -> pd.DataFrame:
        campaign_id = make_ids("CMP", self.n)
        campaign_type = weighted_choice(self.rng, CAMPAIGN_TYPES, [0.20, 0.16, 0.18, 0.16, 0.18, 0.12], self.n)
        channel = weighted_choice(self.rng, CAMPAIGN_CHANNELS, [0.24, 0.16, 0.18, 0.12, 0.14, 0.16], self.n)
        offer_type = np.array([self.rng.choice(OFFER_TYPES) for _ in range(self.n)])
        target_segment = weighted_choice(self.rng, ["Premium", "Regular", "Promo", "New", "Inactive", "Digital"], [0.15, 0.24, 0.20, 0.14, 0.14, 0.13], self.n)
        send_date = pd.Timestamp("2023-01-01") + pd.to_timedelta(self.rng.integers(0, 900, self.n), unit="D")
        impressions = self.rng.integers(8000, 250000, self.n)

        open_rate = self._open_rate(campaign_type, channel, target_segment)
        click_rate = np.clip(open_rate * self.rng.uniform(0.08, 0.28, self.n), 0.005, 0.24)
        conv_rate = np.clip(click_rate * self.rng.uniform(0.08, 0.22, self.n), 0.001, 0.12)
        opens = np.round(impressions * open_rate).astype(int)
        clicks = np.round(impressions * click_rate).astype(int)
        conversions = np.round(impressions * conv_rate).astype(int)
        revenue_generated = np.round(conversions * self.rng.uniform(110, 380, self.n), 2)
        cost = np.round(impressions * self.rng.uniform(0.04, 0.21, self.n), 2)

        return pd.DataFrame(
            {
                "campaign_id": campaign_id,
                "campaign_name": [f"{t} - {s} - {i}" for i, (t, s) in enumerate(zip(campaign_type, target_segment), start=1)],
                "campaign_type": campaign_type,
                "target_segment": target_segment,
                "channel": channel,
                "send_date": send_date.date,
                "offer_type": offer_type,
                "cost": cost,
                "impressions": impressions,
                "opens": opens,
                "clicks": clicks,
                "conversions": conversions,
                "revenue_generated": revenue_generated,
            }
        ).sort_values("send_date").reset_index(drop=True)

    def _open_rate(self, campaign_type, channel, target_segment):
        base = []
        for ct, ch, seg in zip(campaign_type, channel, target_segment):
            value = 0.18
            value += 0.08 if ct in {"Retention", "Loyalty"} else 0
            value += 0.07 if ch in {"Email", "Push"} else 0
            value += 0.06 if seg == "Premium" else 0
            value -= 0.04 if seg == "Inactive" else 0
            base.append(value)
        return np.clip(np.array(base), 0.04, 0.65)
