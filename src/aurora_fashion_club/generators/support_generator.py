"""Support ticket generator for experience and churn signals."""

from __future__ import annotations

import numpy as np
import pandas as pd

from aurora_fashion_club.config.constants import ISSUE_TYPES, SEVERITIES
from aurora_fashion_club.utils import make_ids


class SupportTicketGenerator:
    """Generate service tickets based on customer friction indicators."""

    def __init__(self, n_tickets: int, rng: np.random.Generator):
        self.n = n_tickets
        self.rng = rng

    def generate(self, customers: pd.DataFrame) -> pd.DataFrame:
        sampled_customers = self.rng.choice(
            customers["customer_id"].to_numpy(),
            size=self.n,
            replace=True,
            p=self._customer_weights(customers),
        )
        cust_lookup = customers.set_index("customer_id")

        open_dates, close_dates, issue_type, severity = [], [], [], []
        resolution_time_hours, satisfaction_score, reopened_flag = [], [], []

        for cid in sampled_customers:
            cust = cust_lookup.loc[cid]
            open_date = pd.Timestamp(cust["last_purchase_date"]) + pd.Timedelta(days=int(self.rng.integers(1, 55)))
            sev = self._severity(cust)
            res_hours = float(np.clip(self.rng.normal(10 if sev == "Low" else 24 if sev == "Medium" else 42 if sev == "High" else 64, 9), 1, 120))
            close_date = open_date + pd.Timedelta(hours=res_hours)
            sat = float(np.clip(5 - (res_hours / 24) - (0.8 if sev in {"High", "Critical"} else 0), 1, 5))
            reopened = int(self.rng.random() < (0.08 if sat > 3.7 else 0.22 if sat > 2.6 else 0.38))

            open_dates.append(open_date.date())
            close_dates.append(close_date.date())
            issue_type.append(self.rng.choice(ISSUE_TYPES))
            severity.append(sev)
            resolution_time_hours.append(round(res_hours, 2))
            satisfaction_score.append(round(sat, 2))
            reopened_flag.append(reopened)

        return pd.DataFrame(
            {
                "ticket_id": make_ids("TCK", self.n),
                "customer_id": sampled_customers,
                "open_date": open_dates,
                "close_date": close_dates,
                "issue_type": issue_type,
                "severity": severity,
                "resolution_time_hours": resolution_time_hours,
                "satisfaction_score": satisfaction_score,
                "reopened_flag": reopened_flag,
            }
        ).sort_values("open_date").reset_index(drop=True)

    def _customer_weights(self, customers):
        raw = customers["returns_rate"].to_numpy() + customers["churn_risk_score"].to_numpy() * 0.8 + 0.02
        raw = raw / raw.sum()
        return raw

    def _severity(self, cust):
        if cust["loyalty_tier"] == "Platinum":
            return self.rng.choice(SEVERITIES, p=[0.58, 0.28, 0.10, 0.04])
        if cust["churn_risk_score"] > 0.7:
            return self.rng.choice(SEVERITIES, p=[0.18, 0.30, 0.32, 0.20])
        return self.rng.choice(SEVERITIES, p=[0.42, 0.34, 0.16, 0.08])
