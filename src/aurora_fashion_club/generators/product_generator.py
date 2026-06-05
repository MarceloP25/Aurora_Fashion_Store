"""Product catalog generator for fashion retail."""

from __future__ import annotations

import numpy as np
import pandas as pd

from aurora_fashion_club.config.constants import BRANDS, PRODUCT_CATEGORIES, SEASONS
from aurora_fashion_club.utils import make_ids, weighted_choice


class ProductGenerator:
    """Generate a compact but realistic product catalog."""

    def __init__(self, n_products: int, rng: np.random.Generator):
        self.n = n_products
        self.rng = rng

    def generate(self) -> pd.DataFrame:
        product_id = make_ids("PROD", self.n)
        category = weighted_choice(self.rng, list(PRODUCT_CATEGORIES.keys()), [0.30, 0.20, 0.18, 0.17, 0.15], self.n)
        subcategory = np.array([self.rng.choice(PRODUCT_CATEGORIES[c]) for c in category])
        gender_target = weighted_choice(self.rng, ["F", "M", "Unisex"], [0.56, 0.32, 0.12], self.n)
        season = weighted_choice(self.rng, SEASONS, [0.35, 0.30, 0.22, 0.13], self.n)
        brand = weighted_choice(self.rng, BRANDS, [0.28, 0.15, 0.14, 0.16, 0.14, 0.13], self.n)

        base_price = np.array([self._price_band(c, s) for c, s in zip(category, subcategory)])
        list_price = np.round(base_price * self.rng.uniform(0.88, 1.18, self.n), 2)
        avg_discount_rate = np.round(np.where(category == "Premium", self.rng.uniform(0.03, 0.12, self.n), self.rng.uniform(0.08, 0.35, self.n)), 2)
        margin_rate = np.round(np.where(category == "Premium", self.rng.uniform(0.48, 0.68, self.n), self.rng.uniform(0.25, 0.52, self.n)), 2)
        launch_date = pd.Timestamp("2021-01-01") + pd.to_timedelta(self.rng.integers(0, 1800, self.n), unit="D")
        is_bestseller = (self.rng.random(self.n) < np.where(category == "Premium", 0.18, 0.32)).astype(int)
        return_rate = np.round(np.where(category == "Accessories", self.rng.uniform(0.03, 0.10, self.n), self.rng.uniform(0.06, 0.22, self.n)), 2)

        return pd.DataFrame(
            {
                "product_id": product_id,
                "product_name": [f"{b} {c} {i}" for i, (b, c) in enumerate(zip(brand, subcategory), start=1)],
                "category": category,
                "subcategory": subcategory,
                "gender_target": gender_target,
                "season": season,
                "brand": brand,
                "list_price": list_price,
                "avg_discount_rate": avg_discount_rate,
                "margin_rate": margin_rate,
                "launch_date": launch_date.date,
                "is_bestseller": is_bestseller,
                "return_rate": return_rate,
            }
        ).sort_values("product_id").reset_index(drop=True)

    def _price_band(self, category: str, subcategory: str) -> float:
        lookup = {
            "Casual": 120,
            "Workwear": 220,
            "Premium": 680,
            "Athleisure": 180,
            "Accessories": 95,
        }
        if subcategory in {"Suits", "Leather", "Tailoring", "Coats"}:
            return lookup["Premium"]
        return lookup[category]
