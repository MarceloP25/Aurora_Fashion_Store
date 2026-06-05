"""Customer base generator.

This module creates the behavioral backbone of the project and attaches the
main analytical labels used later for CRM, retention, churn, and LTV.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from aurora_fashion_club.config.constants import (
    ACQUISITION_CHANNELS,
    CATEGORY_PREFERENCES,
    GENDERS,
    INCOME_BANDS,
    LOYALTY_TIERS,
    REGIONS,
)
from aurora_fashion_club.utils import clamp, make_ids, weighted_choice


class CustomerGenerator:
    """Generate synthetic customer records with realistic business signals."""

    def __init__(self, n_customers: int, rng: np.random.Generator):
        self.n = n_customers
        self.rng = rng

    def generate(self) -> pd.DataFrame:
        customer_id = make_ids("CUST", self.n)
        profile = weighted_choice(
            self.rng,
            ["premium", "regular", "promo", "digital", "store", "new", "risk"],
            [0.08, 0.24, 0.16, 0.17, 0.15, 0.10, 0.10],
            self.n,
        )

        age = self._gen_age(profile)
        income_band = self._gen_income(profile)
        acquisition_channel = self._gen_acquisition(profile)
        loyalty_tier = self._gen_loyalty(profile)
        region = weighted_choice(self.rng, REGIONS, [0.50, 0.19, 0.17, 0.08, 0.06], self.n)
        gender = weighted_choice(self.rng, GENDERS, [0.52, 0.45, 0.03], self.n)
        category_preference = weighted_choice(self.rng, CATEGORY_PREFERENCES, [0.35, 0.18, 0.12, 0.15, 0.20], self.n)

        first_purchase_date = pd.Timestamp("2022-01-01") + pd.to_timedelta(self.rng.integers(0, 1500, self.n), unit="D")
        tenure_days = np.maximum((pd.Timestamp.today().normalize() - first_purchase_date).days, 1)
        number_of_orders = self._gen_orders(profile)
        recency = self._gen_recency(profile)
        last_purchase_date = pd.Timestamp.today().normalize() - pd.to_timedelta(recency, unit="D")
        last_purchase_date = np.maximum(last_purchase_date, first_purchase_date.values)

        average_ticket = self._gen_ticket(profile, income_band)
        total_spent = np.round(number_of_orders * average_ticket * self.rng.uniform(0.95, 1.15, self.n), 2)
        discount_usage_rate = np.round(clamp(self._gen_discount(profile), 0.02, 0.90), 2)
        returns_rate = np.round(clamp(self._gen_returns(profile), 0.00, 0.45), 2)
        app_sessions = np.maximum(self.rng.poisson(self._gen_sessions(profile)), 0)
        email_open_rate = np.round(clamp(self._gen_open_rate(profile), 0.03, 0.85), 2)
        email_click_rate = np.round(clamp(email_open_rate * self.rng.uniform(0.08, 0.35, self.n), 0.01, 0.45), 2)
        sms_response_rate = np.round(clamp(self._gen_sms(profile), 0.01, 0.35), 2)
        campaign_exposure_count = np.maximum(self.rng.poisson(self._gen_exposure(profile)), 0)
        campaign_conversion_rate = np.round(clamp(self._gen_conversion(profile), 0.01, 0.45), 2)
        days_since_last_purchase = recency
        churn_risk_score = np.round(clamp(self._gen_churn_risk(profile, recency, returns_rate, app_sessions), 0.01, 0.99), 3)
        churn_flag = (churn_risk_score >= 0.62).astype(int)
        estimated_ltv = np.round(total_spent * (1 + (1 - churn_risk_score)) * self.rng.uniform(0.9, 1.4, self.n), 2)

        df = pd.DataFrame(
            {
                "customer_id": customer_id,
                "gender": gender,
                "age": age,
                "region": region,
                "city": self._gen_city(region),
                "income_band": income_band,
                "acquisition_channel": acquisition_channel,
                "first_purchase_date": first_purchase_date.date,
                "last_purchase_date": pd.to_datetime(last_purchase_date).date,
                "number_of_orders": number_of_orders,
                "total_spent": total_spent,
                "average_ticket": np.round(average_ticket, 2),
                "discount_usage_rate": discount_usage_rate,
                "returns_rate": returns_rate,
                "app_sessions": app_sessions,
                "email_open_rate": email_open_rate,
                "email_click_rate": email_click_rate,
                "sms_response_rate": sms_response_rate,
                "loyalty_tier": loyalty_tier,
                "campaign_exposure_count": campaign_exposure_count,
                "campaign_conversion_rate": campaign_conversion_rate,
                "days_since_last_purchase": days_since_last_purchase,
                "category_preference": category_preference,
                "churn_flag": churn_flag,
                "churn_risk_score": churn_risk_score,
                "estimated_ltv": estimated_ltv,
            }
        )

        return df.sort_values("customer_id").reset_index(drop=True)

    def _gen_age(self, profile):
        base = {
            "premium": self.rng.normal(41, 8, self.n),
            "regular": self.rng.normal(35, 9, self.n),
            "promo": self.rng.normal(31, 8, self.n),
            "digital": self.rng.normal(29, 7, self.n),
            "store": self.rng.normal(44, 10, self.n),
            "new": self.rng.normal(26, 5, self.n),
            "risk": self.rng.normal(33, 9, self.n),
        }
        return np.round(clamp(np.array([base[p][i] for i, p in enumerate(profile)]), 18, 72)).astype(int)

    def _gen_income(self, profile):
        mapping = {
            "premium": [0.02, 0.08, 0.20, 0.35, 0.35],
            "regular": [0.10, 0.35, 0.30, 0.18, 0.07],
            "promo": [0.22, 0.40, 0.22, 0.10, 0.06],
            "digital": [0.12, 0.30, 0.28, 0.20, 0.10],
            "store": [0.08, 0.26, 0.32, 0.22, 0.12],
            "new": [0.18, 0.38, 0.24, 0.14, 0.06],
            "risk": [0.20, 0.40, 0.22, 0.12, 0.06],
        }
        return np.array([self.rng.choice(INCOME_BANDS, p=mapping[p]) for p in profile])

    def _gen_acquisition(self, profile):
        mapping = {
            "premium": [0.10, 0.22, 0.15, 0.18, 0.15, 0.20],
            "regular": [0.24, 0.14, 0.20, 0.12, 0.12, 0.18],
            "promo": [0.38, 0.20, 0.10, 0.08, 0.08, 0.16],
            "digital": [0.32, 0.18, 0.18, 0.12, 0.12, 0.08],
            "store": [0.08, 0.05, 0.08, 0.08, 0.06, 0.65],
            "new": [0.36, 0.22, 0.14, 0.08, 0.08, 0.12],
            "risk": [0.34, 0.16, 0.12, 0.08, 0.10, 0.20],
        }
        return np.array([self.rng.choice(ACQUISITION_CHANNELS, p=mapping[p]) for p in profile])

    def _gen_loyalty(self, profile):
        mapping = {
            "premium": [0.04, 0.16, 0.42, 0.38],
            "regular": [0.24, 0.42, 0.24, 0.10],
            "promo": [0.42, 0.33, 0.18, 0.07],
            "digital": [0.20, 0.38, 0.28, 0.14],
            "store": [0.18, 0.34, 0.28, 0.20],
            "new": [0.55, 0.28, 0.12, 0.05],
            "risk": [0.44, 0.30, 0.18, 0.08],
        }
        return np.array([self.rng.choice(LOYALTY_TIERS, p=mapping[p]) for p in profile])

    def _gen_orders(self, profile):
        lam = {
            "premium": 12, "regular": 7, "promo": 6, "digital": 8, "store": 7, "new": 2, "risk": 3,
        }
        return np.array([max(1, self.rng.poisson(lam[p])) for p in profile])

    def _gen_recency(self, profile):
        base = {
            "premium": self.rng.gamma(2.0, 18.0, self.n),
            "regular": self.rng.gamma(2.2, 25.0, self.n),
            "promo": self.rng.gamma(2.4, 30.0, self.n),
            "digital": self.rng.gamma(1.8, 20.0, self.n),
            "store": self.rng.gamma(2.0, 28.0, self.n),
            "new": self.rng.gamma(1.5, 12.0, self.n),
            "risk": self.rng.gamma(2.8, 40.0, self.n),
        }
        return np.round(clamp(np.array([base[p][i] for i, p in enumerate(profile)]), 0, 730)).astype(int)

    def _gen_ticket(self, profile, income_band):
        income_multiplier = {
            "Baixa": 0.85, "Média": 1.0, "Média-alta": 1.15, "Alta": 1.35, "Premium": 1.55
        }
        base = {
            "premium": 480, "regular": 260, "promo": 190, "digital": 220, "store": 240, "new": 160, "risk": 180,
        }
        ticket = np.array([base[p] * income_multiplier[i] for p, i in zip(profile, income_band)])
        return ticket * self.rng.uniform(0.8, 1.25, self.n)

    def _gen_discount(self, profile):
        return np.array([self.rng.beta(2, 7) if p == "premium" else self.rng.beta(4, 4) if p == "promo" else self.rng.beta(3, 6) for p in profile])

    def _gen_returns(self, profile):
        return np.array([self.rng.beta(2, 14) if p == "premium" else self.rng.beta(3, 10) if p in {"promo", "risk"} else self.rng.beta(2, 12) for p in profile])

    def _gen_sessions(self, profile):
        return np.array([18 if p == "digital" else 11 if p == "premium" else 6 if p == "regular" else 4 if p == "promo" else 3 for p in profile])

    def _gen_open_rate(self, profile):
        return np.array([0.58 if p == "premium" else 0.45 if p == "digital" else 0.35 if p == "regular" else 0.25 if p == "promo" else 0.22 for p in profile])

    def _gen_sms(self, profile):
        return np.array([0.26 if p == "promo" else 0.18 if p == "risk" else 0.12 for p in profile])

    def _gen_exposure(self, profile):
        return np.array([18 if p == "promo" else 12 if p == "digital" else 10 if p == "regular" else 8 for p in profile])

    def _gen_conversion(self, profile):
        return np.array([0.22 if p == "premium" else 0.18 if p == "digital" else 0.14 if p == "regular" else 0.10 if p == "promo" else 0.08 for p in profile])

    def _gen_churn_risk(self, profile, recency, returns_rate, app_sessions):
        profile_risk = np.array([0.18 if p == "premium" else 0.32 if p == "digital" else 0.38 if p == "regular" else 0.48 if p == "promo" else 0.62 if p == "risk" else 0.52 for p in profile])
        return profile_risk + (recency / 1000) + returns_rate * 0.8 - (app_sessions / 250) + self.rng.normal(0, 0.03, self.n)

    def _gen_city(self, region):
        cities = {
            "Sudeste": ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Vitória"],
            "Sul": ["Curitiba", "Porto Alegre", "Florianópolis"],
            "Nordeste": ["Recife", "Salvador", "Fortaleza", "Natal"],
            "Centro-Oeste": ["Brasília", "Goiânia", "Cuiabá"],
            "Norte": ["Manaus", "Belém", "Rio Branco"],
        }
        return np.array([self.rng.choice(cities[r]) for r in region])
