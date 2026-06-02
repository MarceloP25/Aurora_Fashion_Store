from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from .config import ProjectConfig
from .utils import clamp, safe_div, set_seed


GENDERS = ["F", "M", "O"]
REGIONS = ["Sudeste", "Sul", "Nordeste", "Norte", "Centro-Oeste"]
INCOME_BANDS = ["Até 3k", "3k-6k", "6k-10k", "10k-20k", "20k+"]
ACQ_CHANNELS = ["paid_social", "search", "influencer", "social_commerce", "organic", "store"]
LOYALTY_TIERS = ["bronze", "silver", "gold", "platinum"]
CUSTOMER_PREFS = ["dresses", "tops", "bottoms", "shoes", "accessories", "activewear", "menswear", "outerwear"]

PRODUCT_CATEGORIES = {
    "women": {
        "dresses": ["casual", "party", "workwear"],
        "tops": ["t-shirt", "blouse", "shirt", "knit"],
        "bottoms": ["jeans", "trousers", "skirts"],
        "shoes": ["sneakers", "heels", "flats"],
        "accessories": ["bags", "belts", "jewelry"],
        "activewear": ["leggings", "sports_bra", "hoodie"],
        "outerwear": ["jacket", "coat", "blazer"],
    },
    "men": {
        "menswear": ["t-shirt", "shirt", "trousers", "jeans", "sweatshirt", "jacket", "shoes", "accessories"]
    },
}

SEASONS = ["spring", "summer", "fall", "winter", "all_year"]
BRANDS = ["Aurora", "Aurora Studio", "Aurora Premium", "Nord", "Vela", "Muse", "Essence", "Nova"]
PAYMENT_METHODS = ["credit_card", "pix", "debit_card", "wallet", "installments"]
SHIPPING_TYPES = ["standard", "express", "pickup"]
ORDER_STATUSES = ["delivered", "returned", "cancelled"]
ORDER_CHANNELS = ["ecommerce", "app", "store"]
INTERACTION_CHANNELS = ["email", "push", "sms", "whatsapp", "remarketing", "in_app"]
INTERACTION_TYPES = ["campaign", "abandonment", "recommendation", "winback", "loyalty", "browse_reminder"]
ISSUE_TYPES = ["late_delivery", "wrong_item", "size_issue", "payment_issue", "exchange", "refund", "app_bug"]
SEVERITIES = ["low", "medium", "high", "critical"]
EVENT_TYPES = ["page_view", "product_view", "add_to_cart", "wishlist", "checkout_start", "purchase", "app_open", "campaign_click"]
DEVICES = ["mobile", "desktop", "tablet"]

SEGMENT_PROFILES = {
    "premium_loyal": {
        "income": ["10k-20k", "20k+"],
        "channels": ["organic", "search", "store"],
        "orders_lambda": 8.0,
        "discount": (0.05, 0.18),
        "returns": (0.00, 0.06),
        "app": (18, 55),
        "risk_bias": -0.35,
    },
    "promo_sensitive": {
        "income": ["Até 3k", "3k-6k"],
        "channels": ["paid_social", "influencer", "social_commerce"],
        "orders_lambda": 4.5,
        "discount": (0.18, 0.45),
        "returns": (0.03, 0.12),
        "app": (4, 22),
        "risk_bias": 0.25,
    },
    "digital_engaged": {
        "income": ["3k-6k", "6k-10k", "10k-20k"],
        "channels": ["search", "organic", "paid_social"],
        "orders_lambda": 6.0,
        "discount": (0.08, 0.28),
        "returns": (0.01, 0.08),
        "app": (20, 70),
        "risk_bias": -0.1,
    },
    "store_preferred": {
        "income": ["6k-10k", "10k-20k"],
        "channels": ["store", "organic"],
        "orders_lambda": 5.5,
        "discount": (0.06, 0.22),
        "returns": (0.02, 0.10),
        "app": (2, 12),
        "risk_bias": 0.05,
    },
    "new_acquired": {
        "income": ["Até 3k", "3k-6k", "6k-10k"],
        "channels": ["paid_social", "influencer", "search"],
        "orders_lambda": 2.0,
        "discount": (0.15, 0.40),
        "returns": (0.03, 0.14),
        "app": (1, 15),
        "risk_bias": 0.12,
    },
    "high_risk": {
        "income": ["Até 3k", "3k-6k"],
        "channels": ["paid_social", "social_commerce"],
        "orders_lambda": 1.8,
        "discount": (0.20, 0.50),
        "returns": (0.05, 0.18),
        "app": (0, 8),
        "risk_bias": 0.45,
    },
}


@dataclass
class SyntheticDataBundle:
    customers: pd.DataFrame
    products: pd.DataFrame
    orders: pd.DataFrame
    order_items: pd.DataFrame
    campaigns: pd.DataFrame
    interactions: pd.DataFrame
    support_tickets: pd.DataFrame
    digital_events: pd.DataFrame


def _random_dates(rng: np.random.Generator, n: int, start: pd.Timestamp, end: pd.Timestamp) -> pd.DatetimeIndex:
    span = (end - start).days
    offsets = rng.integers(0, span + 1, size=n)
    return pd.to_datetime(start + pd.to_timedelta(offsets, unit="D"))


def generate_customers(cfg: ProjectConfig, rng: np.random.Generator) -> pd.DataFrame:
    start = pd.Timestamp(cfg.start_date)
    end = pd.Timestamp(cfg.end_date)
    n = cfg.n_customers

    seg_names = np.array(list(SEGMENT_PROFILES.keys()))
    seg_probs = np.array([0.22, 0.18, 0.22, 0.14, 0.14, 0.10])
    segments = rng.choice(seg_names, size=n, p=seg_probs)

    gender = rng.choice(GENDERS, size=n, p=[0.58, 0.40, 0.02])
    region = rng.choice(REGIONS, size=n, p=[0.40, 0.20, 0.22, 0.08, 0.10])
    city_map = {
        "Sudeste": ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Campinas", "Vitória"],
        "Sul": ["Porto Alegre", "Curitiba", "Florianópolis", "Joinville"],
        "Nordeste": ["Salvador", "Recife", "Fortaleza", "Natal"],
        "Norte": ["Manaus", "Belém", "Porto Velho"],
        "Centro-Oeste": ["Brasília", "Goiânia", "Cuiabá"],
    }
    city = [rng.choice(city_map[r]) for r in region]

    age = np.clip(rng.normal(36, 11, n).round().astype(int), 18, 72)
    acquisition_channel = np.array([
        rng.choice(ACQ_CHANNELS if seg not in ("store_preferred",) else ["store", "organic"], p=[0.28, 0.22, 0.16, 0.16, 0.10, 0.08] if seg != "store_preferred" else [0.62, 0.38])
        for seg in segments
    ], dtype=object)

    income_band = np.array([
        rng.choice(SEGMENT_PROFILES[seg]["income"]) for seg in segments
    ], dtype=object)

    first_purchase_date = _random_dates(rng, n, start, end - pd.Timedelta(days=90))
    # older customers for loyal segments
    age_adjustment = np.where(
        np.isin(segments, ["premium_loyal", "digital_engaged", "store_preferred"]),
        rng.integers(30, 420, size=n),
        rng.integers(0, 240, size=n),
    )
    first_purchase_date = pd.Series(pd.to_datetime(first_purchase_date) - pd.to_timedelta(age_adjustment, unit="D"))
    first_purchase_date = first_purchase_date.clip(lower=start)

    last_purchase_date = []
    number_of_orders = []
    category_pref = []
    discount_usage_rate = []
    returns_rate = []
    app_sessions = []
    open_rate = []
    click_rate = []
    sms_rate = []
    tier = []
    camp_exposure = []
    camp_conv = []

    for seg in segments:
        prof = SEGMENT_PROFILES[seg]
        orders_n = max(1, int(rng.poisson(prof["orders_lambda"])))
        if seg == "high_risk":
            orders_n = max(1, int(rng.poisson(1.6)))
        if seg == "new_acquired":
            orders_n = max(1, int(rng.poisson(2.2)))
        number_of_orders.append(orders_n)

        # recency depends on segment
        recency_days = int(np.clip(rng.gamma(shape=2.1 if seg != "high_risk" else 3.8, scale=22 if seg != "high_risk" else 35), 0, 420))
        last_dt = end - pd.Timedelta(days=recency_days)
        last_dt = max(last_dt, pd.Timestamp(first_purchase_date[len(last_purchase_date)]))
        last_purchase_date.append(last_dt)

        category_pref.append(rng.choice(CUSTOMER_PREFS, p=np.array([0.18,0.17,0.14,0.13,0.12,0.08,0.10,0.08])))
        discount_usage_rate.append(np.clip(rng.normal(*prof["discount"]), 0, 0.75))
        returns_rate.append(np.clip(rng.normal(*prof["returns"]), 0, 0.35))
        app_sessions.append(int(np.clip(rng.normal(*prof["app"]), 0, None)))
        open_rate.append(np.clip(rng.beta(2.8, 4.0) + (0.07 if seg == "premium_loyal" else 0), 0, 1))
        click_rate.append(np.clip(open_rate[-1] * rng.uniform(0.18, 0.45), 0, 1))
        sms_rate.append(np.clip(rng.beta(1.8, 6.0) * (1.2 if seg in ("promo_sensitive", "high_risk") else 0.8), 0, 1))
        base_tier = "platinum" if seg == "premium_loyal" else "gold" if seg == "digital_engaged" else "silver" if seg in ("store_preferred",) else "bronze"
        tier.append(base_tier)
        camp_exposure.append(int(np.clip(rng.normal(25 if seg != "high_risk" else 18, 8), 3, 80)))
        camp_conv.append(np.clip(rng.normal(0.14 if seg == "premium_loyal" else 0.10 if seg == "digital_engaged" else 0.08 if seg == "store_preferred" else 0.06 if seg == "promo_sensitive" else 0.05, 0.03), 0, 1))

    customers = pd.DataFrame({
        "customer_id": [f"CUST-{i:07d}" for i in range(1, n + 1)],
        "_synthetic_segment": segments,
        "gender": gender,
        "age": age,
        "region": region,
        "city": city,
        "income_band": income_band,
        "acquisition_channel": acquisition_channel,
        "first_purchase_date": pd.to_datetime(first_purchase_date).dt.normalize(),
        "last_purchase_date": pd.to_datetime(last_purchase_date).normalize(),
        "number_of_orders": number_of_orders,
        "total_spent": 0.0,
        "average_ticket": 0.0,
        "discount_usage_rate": np.round(discount_usage_rate, 3),
        "returns_rate": np.round(returns_rate, 3),
        "app_sessions": app_sessions,
        "email_open_rate": np.round(open_rate, 3),
        "email_click_rate": np.round(click_rate, 3),
        "sms_response_rate": np.round(sms_rate, 3),
        "loyalty_tier": tier,
        "campaign_exposure_count": camp_exposure,
        "campaign_conversion_rate": np.round(camp_conv, 3),
        "days_since_last_purchase": (end - pd.to_datetime(last_purchase_date)).days,
        "category_preference": category_pref,
        "churn_flag": 0,
        "churn_risk_score": 0.0,
        "estimated_ltv": 0.0,
    })

    # balance small missingness and mild inconsistencies
    for col in ["city", "income_band", "email_click_rate", "sms_response_rate"]:
        mask = rng.random(n) < 0.01
        customers.loc[mask, col] = np.nan

    return customers


def generate_products(cfg: ProjectConfig, rng: np.random.Generator) -> pd.DataFrame:
    n = cfg.n_products
    categories = []
    subcategories = []
    gender_target = []
    season = []
    brand = []
    list_price = []
    avg_discount_rate = []
    margin_rate = []
    launch_date = []
    bestseller = []
    return_rate = []
    product_name = []

    all_rows = []
    for gender_key, cats in PRODUCT_CATEGORIES.items():
        for cat, subs in cats.items():
            for sub in subs:
                all_rows.append((gender_key, cat, sub))
    all_rows = all_rows * (n // len(all_rows) + 1)
    rng.shuffle(all_rows)
    all_rows = all_rows[:n]

    for i, (gkey, cat, sub) in enumerate(all_rows, start=1):
        gender_target.append("female" if gkey == "women" else "male")
        categories.append(cat)
        subcategories.append(sub)
        s = rng.choice(SEASONS, p=[0.22, 0.23, 0.24, 0.17, 0.14])
        season.append(s)
        brand_choice = rng.choice(BRANDS, p=[0.18, 0.15, 0.18, 0.12, 0.12, 0.11, 0.08, 0.06])
        brand.append(brand_choice)
        base_price = {
            "dresses": 219,
            "tops": 89,
            "bottoms": 149,
            "shoes": 259,
            "accessories": 79,
            "activewear": 129,
            "outerwear": 299,
            "menswear": 139,
        }[cat]
        premium_mult = 1.4 if brand_choice in ("Aurora Premium", "Aurora Studio") else 1.0
        price = np.clip(rng.normal(base_price * premium_mult, base_price * 0.28), 39, 1299)
        list_price.append(round(float(price), 2))
        disc = np.clip(rng.normal(0.15 if premium_mult == 1.0 else 0.08, 0.08), 0.0, 0.45)
        avg_discount_rate.append(round(float(disc), 3))
        margin = np.clip(rng.normal(0.42 if premium_mult == 1.4 else 0.33, 0.09), 0.12, 0.68)
        margin_rate.append(round(float(margin), 3))
        launch = pd.Timestamp(cfg.start_date) - pd.Timedelta(days=int(rng.integers(0, 1100)))
        launch_date.append(launch.normalize())
        is_best = int(rng.random() < (0.18 if cat in ("tops", "dresses", "menswear") else 0.11))
        bestseller.append(is_best)
        rr = np.clip(rng.normal(0.06 if is_best else 0.11, 0.03), 0.01, 0.30)
        return_rate.append(round(float(rr), 3))
        product_name.append(f"{brand_choice} {cat.title()} {sub.title()} {i:04d}")

    return pd.DataFrame({
        "product_id": [f"PROD-{i:07d}" for i in range(1, n + 1)],
        "product_name": product_name,
        "category": categories,
        "subcategory": subcategories,
        "gender_target": gender_target,
        "season": season,
        "brand": brand,
        "list_price": list_price,
        "avg_discount_rate": avg_discount_rate,
        "margin_rate": margin_rate,
        "launch_date": launch_date,
        "is_bestseller": bestseller,
        "return_rate": return_rate,
    })


def _customer_order_profile(customers: pd.DataFrame):
    seg = customers["_synthetic_segment"].to_numpy()
    income = customers["income_band"].fillna("3k-6k").to_numpy()
    return seg, income


def generate_orders_and_items(cfg: ProjectConfig, rng: np.random.Generator, customers: pd.DataFrame, products: pd.DataFrame):
    start = pd.Timestamp(cfg.start_date)
    end = pd.Timestamp(cfg.end_date)

    cust_segments = customers["_synthetic_segment"].to_numpy()
    customer_ids = customers["customer_id"].to_numpy()

    product_lookup = products.set_index("product_id")
    product_ids = products["product_id"].to_numpy()

    orders_rows = []
    items_rows = []

    order_counter = 1
    item_counter = 1

    for idx, cust_id in enumerate(customer_ids):
        seg = cust_segments[idx]
        prof = SEGMENT_PROFILES[seg]
        n_orders = max(1, int(rng.poisson(prof["orders_lambda"])))
        if seg == "high_risk":
            n_orders = max(1, int(rng.poisson(1.5)))
        if seg == "new_acquired":
            n_orders = max(1, int(rng.poisson(2.0)))

        first_dt = pd.Timestamp(customers.loc[idx, "first_purchase_date"])
        last_dt = pd.Timestamp(customers.loc[idx, "last_purchase_date"])
        if last_dt < first_dt:
            last_dt = first_dt + pd.Timedelta(days=int(rng.integers(0, 30)))
        if last_dt > end:
            last_dt = end

        if n_orders == 1:
            order_dates = [last_dt]
        else:
            span_days = max(1, (last_dt - first_dt).days)
            offs = np.sort(rng.integers(0, span_days + 1, size=n_orders))
            order_dates = [first_dt + pd.Timedelta(days=int(o)) for o in offs]
            order_dates[-1] = last_dt

        customer_discount = float(customers.loc[idx, "discount_usage_rate"])
        customer_returns = float(customers.loc[idx, "returns_rate"])
        customer_channel = customers.loc[idx, "acquisition_channel"] if pd.notna(customers.loc[idx, "acquisition_channel"]) else rng.choice(ACQ_CHANNELS)
        customer_income = customers.loc[idx, "income_band"] if pd.notna(customers.loc[idx, "income_band"]) else "3k-6k"

        for od in order_dates:
            channel = rng.choice(ORDER_CHANNELS, p=[0.42, 0.34, 0.24])
            if customer_channel == "store":
                channel = rng.choice(ORDER_CHANNELS, p=[0.22, 0.10, 0.68])
            status = rng.choice(ORDER_STATUSES, p=[0.82, 0.10, 0.08]) if customer_returns < 0.12 else rng.choice(ORDER_STATUSES, p=[0.72, 0.20, 0.08])
            shipping_type = rng.choice(SHIPPING_TYPES, p=[0.62, 0.18, 0.20]) if channel != "store" else "pickup"
            payment_method = rng.choice(PAYMENT_METHODS, p=[0.56, 0.12, 0.12, 0.05, 0.15])
            n_items = int(rng.integers(1, 9))
            if seg == "premium_loyal":
                n_items = int(rng.integers(1, 6))
            if seg == "high_risk":
                n_items = int(rng.integers(1, 5))

            chosen_products = rng.choice(product_ids, size=n_items, replace=False if n_items <= len(product_ids) else True)
            quantities = rng.integers(1, 3, size=n_items)
            line_amounts = []
            item_discounts = []
            gross_line_amounts = []

            for pid, qty in zip(chosen_products, quantities):
                prod = product_lookup.loc[pid]
                unit_price = float(prod["list_price"]) * float(rng.uniform(0.92, 1.05))
                unit_price = round(unit_price, 2)
                gross_line = round(unit_price * qty, 2)
                disc_rate = np.clip(
                    rng.normal(
                        loc=float(prod["avg_discount_rate"]) + (0.10 if customer_discount > 0.25 else 0.0),
                        scale=0.06,
                    ),
                    0.0,
                    0.55,
                )
                if seg == "premium_loyal":
                    disc_rate = np.clip(disc_rate * 0.55, 0.0, 0.30)
                discount_value = round(gross_line * disc_rate, 2)
                line_amount = round(gross_line - discount_value, 2)
                line_amounts.append(line_amount)
                item_discounts.append(discount_value)
                gross_line_amounts.append(gross_line)
                items_rows.append({
                    "order_item_id": f"OITEM-{item_counter:09d}",
                    "order_id": f"ORD-{order_counter:09d}",
                    "product_id": pid,
                    "quantity": int(qty),
                    "unit_price": unit_price,
                    "discount_value": discount_value,
                    "line_amount": line_amount,
                })
                item_counter += 1

            gross_amount = round(float(np.sum(gross_line_amounts)), 2)
            discount_amount = round(float(np.sum(item_discounts)), 2)
            net_amount = round(float(np.sum(line_amounts)), 2)
            shipping_cost = round(float(np.clip(rng.normal(18 if shipping_type == "express" else 12 if shipping_type == "standard" else 0, 5), 0, 48)), 2)
            delivery_days = int(np.clip(rng.normal(3 if shipping_type == "express" else 6 if shipping_type == "standard" else 0, 2), 0, 14))
            if channel == "store":
                delivery_days = 0
                shipping_cost = 0.0
            return_flag = int(status == "returned" or (customer_returns > 0.14 and rng.random() < 0.18))
            orders_rows.append({
                "order_id": f"ORD-{order_counter:09d}",
                "customer_id": cust_id,
                "order_date": pd.Timestamp(od).normalize(),
                "channel": channel,
                "order_status": status,
                "gross_amount": gross_amount,
                "discount_amount": discount_amount,
                "net_amount": net_amount,
                "payment_method": payment_method,
                "shipping_type": shipping_type,
                "shipping_cost": shipping_cost,
                "delivery_days": delivery_days,
                "return_flag": return_flag,
            })
            order_counter += 1

    orders = pd.DataFrame(orders_rows)
    order_items = pd.DataFrame(items_rows)

    return orders, order_items


def generate_campaigns(cfg: ProjectConfig, rng: np.random.Generator) -> pd.DataFrame:
    n = cfg.n_campaigns
    start = pd.Timestamp(cfg.start_date)
    end = pd.Timestamp(cfg.end_date)
    send_date = _random_dates(rng, n, start, end)

    campaign_types = np.array(["retention", "reactivation", "upsell", "cross_sell", "conversion", "loyalty"])
    target_segments = np.array(["premium_loyal", "promo_sensitive", "digital_engaged", "store_preferred", "new_acquired", "high_risk"])
    offer_types = np.array(["discount", "free_shipping", "exclusive_access", "bundle", "cashback", "early_access"])

    rows = []
    for i in range(n):
        ctype = rng.choice(campaign_types, p=[0.20, 0.16, 0.16, 0.16, 0.18, 0.14])
        seg = rng.choice(target_segments)
        channel = rng.choice(INTERACTION_CHANNELS[:6], p=[0.36, 0.20, 0.12, 0.10, 0.10, 0.12])
        if seg == "premium_loyal":
            offer = rng.choice(["exclusive_access", "early_access", "bundle", "free_shipping"], p=[0.4, 0.2, 0.2, 0.2])
        elif seg == "promo_sensitive":
            offer = rng.choice(["discount", "cashback", "free_shipping", "bundle"], p=[0.52, 0.18, 0.18, 0.12])
        else:
            offer = rng.choice(offer_types)
        impressions = int(np.clip(rng.normal(150_000 if seg != "premium_loyal" else 70_000, 55_000), 20_000, 450_000))
        open_rate = np.clip(rng.normal(0.21 if seg == "premium_loyal" else 0.17 if seg == "digital_engaged" else 0.15, 0.05), 0.03, 0.55)
        click_rate = np.clip(open_rate * rng.uniform(0.12, 0.35), 0.01, 0.20)
        conversions = int(np.clip(impressions * click_rate * rng.uniform(0.03, 0.12), 50, impressions * 0.04))
        opens = int(impressions * open_rate)
        clicks = int(impressions * click_rate)
        cost = round(float(np.clip(rng.normal(6500 if seg != "premium_loyal" else 3500, 1700), 900, 22000)), 2)
        revenue = round(float(conversions * rng.normal(165, 60)), 2)
        rows.append({
            "campaign_id": f"CAMP-{i+1:06d}",
            "campaign_name": f"{ctype.title()} {seg.replace('_', ' ').title()} {i+1:03d}",
            "campaign_type": ctype,
            "target_segment": seg,
            "channel": channel,
            "send_date": pd.Timestamp(send_date[i]).normalize(),
            "offer_type": offer,
            "cost": cost,
            "impressions": impressions,
            "opens": opens,
            "clicks": clicks,
            "conversions": conversions,
            "revenue_generated": revenue,
        })
    return pd.DataFrame(rows)


def generate_interactions(cfg: ProjectConfig, rng: np.random.Generator, customers: pd.DataFrame, campaigns: pd.DataFrame) -> pd.DataFrame:
    customer_ids = customers["customer_id"].to_numpy()
    segments = customers["_synthetic_segment"].to_numpy()

    rows = []
    interaction_id = 1

    for idx, cust_id in enumerate(customer_ids):
        seg = segments[idx]
        base_n = int(np.clip(rng.poisson(cfg.avg_interactions_per_customer * (1.4 if seg in ("digital_engaged", "premium_loyal") else 0.85 if seg == "high_risk" else 1.0)), 1, 45))
        exposed_campaigns = campaigns.sample(n=min(base_n, len(campaigns)), replace=len(campaigns) < base_n, random_state=int(rng.integers(0, 1_000_000)))
        for _, camp in exposed_campaigns.iterrows():
            response_prob = 0.45 if seg == "premium_loyal" and camp["offer_type"] in ("exclusive_access", "early_access") else 0.22 if seg == "promo_sensitive" and camp["offer_type"] == "discount" else 0.18 if seg == "digital_engaged" else 0.11 if seg == "store_preferred" else 0.08 if seg == "high_risk" else 0.14
            response_prob = np.clip(response_prob + (0.04 if camp["channel"] in ("email", "push") else 0) - (0.04 if seg == "high_risk" else 0), 0.01, 0.75)
            response_flag = int(rng.random() < response_prob)
            conversion_prob = response_prob * (0.35 if camp["campaign_type"] == "retention" else 0.42 if camp["campaign_type"] in ("reactivation", "conversion") else 0.28)
            conversion_flag = int(response_flag and rng.random() < conversion_prob)
            interaction_dt = pd.Timestamp(camp["send_date"]) + pd.Timedelta(days=int(rng.integers(0, 4)))
            rows.append({
                "interaction_id": f"INT-{interaction_id:09d}",
                "customer_id": cust_id,
                "interaction_date": interaction_dt.normalize(),
                "channel": camp["channel"],
                "interaction_type": camp["campaign_type"],
                "response_flag": response_flag,
                "conversion_flag": conversion_flag,
                "campaign_id": camp["campaign_id"],
                "message_theme": camp["offer_type"],
            })
            interaction_id += 1
    return pd.DataFrame(rows)


def generate_support_tickets(cfg: ProjectConfig, rng: np.random.Generator, customers: pd.DataFrame) -> pd.DataFrame:
    rows = []
    ticket_id = 1
    segments = customers["_synthetic_segment"].to_numpy()

    for idx, cust_id in enumerate(customers["customer_id"].to_numpy()):
        seg = segments[idx]
        rate = cfg.support_ticket_rate * (1.5 if seg == "high_risk" else 1.2 if seg == "promo_sensitive" else 0.75 if seg == "premium_loyal" else 1.0)
        n_tickets = int(rng.poisson(rate * 6))
        for _ in range(n_tickets):
            open_dt = pd.Timestamp(cfg.start_date) + pd.Timedelta(days=int(rng.integers(0, (pd.Timestamp(cfg.end_date) - pd.Timestamp(cfg.start_date)).days + 1)))
            sev = rng.choice(SEVERITIES, p=[0.42, 0.31, 0.18, 0.09])
            issue = rng.choice(ISSUE_TYPES)
            base_hours = {"low": 8, "medium": 18, "high": 38, "critical": 72}[sev]
            resolution = max(0.5, float(np.clip(rng.normal(base_hours, base_hours * 0.45), 0.5, 180)))
            satisfaction = float(np.clip(rng.normal(4.4 if seg == "premium_loyal" else 3.9, 0.8) - (0.8 if sev in ("high", "critical") else 0), 1.0, 5.0))
            reopened = int(rng.random() < (0.05 if sev == "low" else 0.09 if sev == "medium" else 0.15 if sev == "high" else 0.23))
            close_dt = open_dt + pd.Timedelta(hours=resolution)
            rows.append({
                "ticket_id": f"TICK-{ticket_id:09d}",
                "customer_id": cust_id,
                "open_date": open_dt.normalize(),
                "close_date": close_dt.normalize(),
                "issue_type": issue,
                "severity": sev,
                "resolution_time_hours": round(resolution, 2),
                "satisfaction_score": round(satisfaction, 2),
                "reopened_flag": reopened,
            })
            ticket_id += 1
    return pd.DataFrame(rows)


def generate_digital_events(cfg: ProjectConfig, rng: np.random.Generator, customers: pd.DataFrame, campaigns: pd.DataFrame) -> pd.DataFrame:
    rows = []
    event_id = 1
    segments = customers["_synthetic_segment"].to_numpy()
    customer_ids = customers["customer_id"].to_numpy()

    campaign_dates = campaigns["send_date"].to_numpy()
    for idx, cust_id in enumerate(customer_ids):
        seg = segments[idx]
        n_events = int(np.clip(rng.poisson(cfg.avg_digital_events_per_customer * (2.0 if seg in ("digital_engaged", "premium_loyal") else 0.55 if seg == "high_risk" else 1.0)), 2, 120))
        device_probs = [0.78, 0.18, 0.04] if seg != "store_preferred" else [0.46, 0.45, 0.09]
        for _ in range(n_events):
            event_dt = pd.Timestamp(cfg.start_date) + pd.Timedelta(days=int(rng.integers(0, (pd.Timestamp(cfg.end_date) - pd.Timestamp(cfg.start_date)).days + 1)))
            etype = rng.choice(EVENT_TYPES, p=[0.30, 0.22, 0.16, 0.08, 0.08, 0.04, 0.10, 0.02])
            if seg == "premium_loyal":
                etype = rng.choice(EVENT_TYPES, p=[0.22, 0.20, 0.14, 0.08, 0.08, 0.04, 0.14, 0.10])
            device = rng.choice(DEVICES, p=device_probs)
            session = float(np.clip(rng.normal(7.5 if seg in ("digital_engaged", "premium_loyal") else 4.8, 2.8), 0.2, 35))
            page_views = int(np.clip(rng.normal(8 if seg != "high_risk" else 4, 4), 1, 40))
            add_flag = int(etype in ("add_to_cart", "checkout_start", "purchase") or (rng.random() < (0.22 if seg in ("digital_engaged", "premium_loyal") else 0.12)))
            checkout_flag = int(etype in ("checkout_start", "purchase") or (add_flag and rng.random() < 0.38))
            purchase_flag = int(etype == "purchase" or (checkout_flag and rng.random() < (0.52 if seg == "premium_loyal" else 0.25)))
            rows.append({
                "event_id": f"EVT-{event_id:011d}",
                "customer_id": cust_id,
                "event_date": pd.Timestamp(event_dt).normalize(),
                "event_type": etype,
                "device_type": device,
                "session_duration": round(session, 2),
                "page_views": page_views,
                "add_to_cart_flag": add_flag,
                "checkout_start_flag": checkout_flag,
                "purchase_flag": purchase_flag,
            })
            event_id += 1
    return pd.DataFrame(rows)


def build_features(customers: pd.DataFrame, orders: pd.DataFrame, order_items: pd.DataFrame, interactions: pd.DataFrame, support_tickets: pd.DataFrame, digital_events: pd.DataFrame, campaigns: pd.DataFrame, products: pd.DataFrame, cfg: ProjectConfig) -> pd.DataFrame:
    customers = customers.copy()
    orders = orders.copy()
    order_items = order_items.copy()
    interactions = interactions.copy()
    support_tickets = support_tickets.copy()
    digital_events = digital_events.copy()

    # transactional aggregates
    order_agg = orders.groupby("customer_id").agg(
        order_count=("order_id", "count"),
        first_order_date=("order_date", "min"),
        last_order_date=("order_date", "max"),
        gross_revenue=("gross_amount", "sum"),
        discount_total=("discount_amount", "sum"),
        net_revenue=("net_amount", "sum"),
        avg_order_value=("net_amount", "mean"),
        return_orders=("return_flag", "sum"),
        avg_delivery_days=("delivery_days", "mean"),
        avg_shipping_cost=("shipping_cost", "mean"),
    ).reset_index()

    item_agg = order_items.merge(orders[["order_id", "customer_id"]], on="order_id", how="left").groupby("customer_id").agg(
        item_count=("order_item_id", "count"),
        avg_unit_price=("unit_price", "mean"),
        avg_line_amount=("line_amount", "mean"),
        total_quantity=("quantity", "sum"),
    ).reset_index()

    interaction_agg = interactions.groupby("customer_id").agg(
        interaction_count=("interaction_id", "count"),
        response_count=("response_flag", "sum"),
        conversion_count=("conversion_flag", "sum"),
    ).reset_index()

    ticket_agg = support_tickets.groupby("customer_id").agg(
        ticket_count=("ticket_id", "count"),
        avg_resolution_time_hours=("resolution_time_hours", "mean"),
        avg_satisfaction=("satisfaction_score", "mean"),
        reopened_count=("reopened_flag", "sum"),
    ).reset_index()

    digital_agg = digital_events.groupby("customer_id").agg(
        digital_events_count=("event_id", "count"),
        app_open_count=("event_type", lambda s: int((s == "app_open").sum())),
        add_to_cart_count=("add_to_cart_flag", "sum"),
        checkout_start_count=("checkout_start_flag", "sum"),
        purchase_event_count=("purchase_flag", "sum"),
        avg_session_duration=("session_duration", "mean"),
        avg_page_views=("page_views", "mean"),
    ).reset_index()

    customers = customers.merge(order_agg, on="customer_id", how="left")
    customers = customers.merge(item_agg, on="customer_id", how="left")
    customers = customers.merge(interaction_agg, on="customer_id", how="left")
    customers = customers.merge(ticket_agg, on="customer_id", how="left")
    customers = customers.merge(digital_agg, on="customer_id", how="left")

    for col in ["order_count", "item_count", "interaction_count", "ticket_count", "digital_events_count", "response_count", "conversion_count", "app_open_count", "add_to_cart_count", "checkout_start_count", "purchase_event_count", "reopened_count", "return_orders", "total_quantity"]:
        customers[col] = customers[col].fillna(0).astype(int)

    for col in ["gross_revenue", "discount_total", "net_revenue", "avg_order_value", "avg_unit_price", "avg_line_amount", "avg_delivery_days", "avg_shipping_cost", "avg_resolution_time_hours", "avg_satisfaction", "avg_session_duration", "avg_page_views"]:
        if col in customers.columns:
            customers[col] = customers[col].astype(float)

    end = pd.Timestamp(cfg.end_date)
    customers["days_since_last_purchase"] = (end - pd.to_datetime(customers["last_order_date"]).fillna(end)).dt.days
    customers["days_since_last_purchase"] = customers["days_since_last_purchase"].fillna((end - pd.to_datetime(customers["last_purchase_date"])).dt.days)
    customers["days_since_last_purchase"] = customers["days_since_last_purchase"].clip(lower=0).astype(int)

    customers["repeat_purchase_rate"] = safe_div(customers["order_count"] - 1, customers["order_count"].replace(0, np.nan), default=0.0)
    customers["response_rate"] = safe_div(customers["response_count"], customers["interaction_count"].replace(0, np.nan), default=0.0)
    customers["conversion_rate_from_interactions"] = safe_div(customers["conversion_count"], customers["interaction_count"].replace(0, np.nan), default=0.0)
    customers["digital_engagement_index"] = (
        0.35 * safe_div(customers["digital_events_count"], customers["digital_events_count"].replace(0, np.nan), default=0.0)
        + 0.25 * safe_div(customers["app_open_count"], customers["digital_events_count"].replace(0, np.nan), default=0.0)
        + 0.20 * safe_div(customers["add_to_cart_count"], customers["digital_events_count"].replace(0, np.nan), default=0.0)
        + 0.20 * safe_div(customers["avg_session_duration"].fillna(0), 20.0, default=0.0)
    )

    customers["campaign_fatigue_index"] = np.clip(
        (customers["campaign_exposure_count"] / 50.0)
        - customers["campaign_conversion_rate"].fillna(0)
        + customers["days_since_last_purchase"] / 365.0 * 0.12,
        0,
        1.5,
    )

    # derived churn score
    norm_days = customers["days_since_last_purchase"] / max(1, customers["days_since_last_purchase"].max())
    norm_return = customers["returns_rate"].fillna(0)
    norm_discount = customers["discount_usage_rate"].fillna(0)
    norm_digital = np.clip(customers["digital_engagement_index"].fillna(0), 0, 1.5) / 1.5
    norm_inter = np.clip(customers["response_rate"].fillna(0), 0, 1)

    churn_risk = (
        0.34 * norm_days
        + 0.18 * (1 - np.clip(customers["repeat_purchase_rate"], 0, 1))
        + 0.12 * norm_return
        + 0.10 * norm_discount
        + 0.08 * (1 - norm_digital)
        + 0.08 * (1 - norm_inter)
        + 0.10 * np.clip(customers["campaign_fatigue_index"] / 1.5, 0, 1)
    )
    churn_risk += np.where(customers["_synthetic_segment"].isin(["high_risk", "promo_sensitive"]), 0.06, 0)
    churn_risk += np.where(customers["_synthetic_segment"].eq("premium_loyal"), -0.06, 0)
    churn_risk = np.clip(churn_risk + np.random.default_rng(cfg.seed).normal(0, 0.035, len(customers)), 0, 1)
    customers["churn_risk_score"] = np.round(churn_risk, 4)
    customers["churn_flag"] = (customers["churn_risk_score"] >= 0.56).astype(int)

    customers["estimated_ltv"] = np.round(
        np.maximum(customers["net_revenue"].fillna(0), customers["gross_revenue"].fillna(0) * 0.82)
        * (1 + customers["repeat_purchase_rate"].fillna(0) * 0.75)
        * (1 - customers["churn_risk_score"] * 0.35)
        + customers["digital_engagement_index"].fillna(0) * 280,
        2,
    )

    # final clean-up
    customers["average_ticket"] = np.round(safe_div(customers["net_revenue"].fillna(0), customers["order_count"].replace(0, np.nan), default=0.0), 2)
    customers["total_spent"] = customers["net_revenue"].fillna(0).round(2)

    customers["days_since_last_purchase"] = customers["days_since_last_purchase"].astype(int)

    # bring to requested schema columns + helpful metrics
    final_cols = [
        "customer_id", "gender", "age", "region", "city", "income_band", "acquisition_channel",
        "first_purchase_date", "last_purchase_date", "number_of_orders", "total_spent",
        "average_ticket", "discount_usage_rate", "returns_rate", "app_sessions",
        "email_open_rate", "email_click_rate", "sms_response_rate", "loyalty_tier",
        "campaign_exposure_count", "campaign_conversion_rate", "days_since_last_purchase",
        "category_preference", "churn_flag", "churn_risk_score", "estimated_ltv",
        # enrichments
        "order_count", "first_order_date", "last_order_date", "gross_revenue", "discount_total",
        "net_revenue", "avg_order_value", "item_count", "total_quantity", "interaction_count",
        "response_count", "conversion_count", "ticket_count", "avg_satisfaction", "avg_resolution_time_hours",
        "digital_events_count", "app_open_count", "add_to_cart_count", "checkout_start_count", "purchase_event_count",
        "avg_session_duration", "avg_page_views", "repeat_purchase_rate", "response_rate",
        "conversion_rate_from_interactions", "digital_engagement_index", "campaign_fatigue_index",
    ]
    for c in final_cols:
        if c not in customers.columns:
            customers[c] = np.nan

    customers = customers[final_cols + (["_synthetic_segment"] if "_synthetic_segment" in customers.columns else [])]

    # parse dates
    for c in ["first_purchase_date", "last_purchase_date", "first_order_date", "last_order_date"]:
        if c in customers.columns:
            customers[c] = pd.to_datetime(customers[c]).dt.normalize()

    return customers


def generate_all(cfg: ProjectConfig) -> SyntheticDataBundle:
    rng = set_seed(cfg.seed)
    customers = generate_customers(cfg, rng)
    products = generate_products(cfg, rng)
    orders, order_items = generate_orders_and_items(cfg, rng, customers, products)
    campaigns = generate_campaigns(cfg, rng)
    interactions = generate_interactions(cfg, rng, customers, campaigns)
    support_tickets = generate_support_tickets(cfg, rng, customers)
    digital_events = generate_digital_events(cfg, rng, customers, campaigns)

    customers = build_features(customers, orders, order_items, interactions, support_tickets, digital_events, campaigns, products, cfg)
    return SyntheticDataBundle(customers, products, orders, order_items, campaigns, interactions, support_tickets, digital_events)
