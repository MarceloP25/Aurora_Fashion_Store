"""Fixed domain lists used by the synthetic generators."""

GENDERS = ["F", "M", "U"]
REGIONS = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
INCOME_BANDS = ["Baixa", "Média", "Média-alta", "Alta", "Premium"]
ACQUISITION_CHANNELS = ["Paid Social", "Influencer", "Organic Search", "Email", "Referral", "Store"]
LOYALTY_TIERS = ["Bronze", "Silver", "Gold", "Platinum"]
CATEGORY_PREFERENCES = ["Casual", "Workwear", "Premium", "Athleisure", "Accessories"]
PRODUCT_CATEGORIES = {
    "Casual": ["T-shirts", "Jeans", "Dresses", "Skirts"],
    "Workwear": ["Blazers", "Shirts", "Trousers", "Suits"],
    "Premium": ["Coats", "Leather", "Silk", "Tailoring"],
    "Athleisure": ["Leggings", "Sneakers", "Hoodies", "Tops"],
    "Accessories": ["Bags", "Belts", "Jewelry", "Scarves"],
}
SEASONS = ["SS", "FW", "Basics", "Capsule"]
BRANDS = ["Aurora", "Linea", "North", "Studio", "Avenue", "Edition"]
ORDER_CHANNELS = ["E-commerce", "App", "Store"]
ORDER_STATUS = ["Completed", "Cancelled", "Returned"]
PAYMENT_METHODS = ["Credit Card", "Pix", "Debit Card", "Installments", "Wallet"]
SHIPPING_TYPES = ["Standard", "Express", "Store Pickup"]
CAMPAIGN_TYPES = ["Retention", "Reactivation", "Upsell", "Cross-sell", "Acquisition", "Loyalty"]
CAMPAIGN_CHANNELS = ["Email", "SMS", "Push", "WhatsApp", "Remarketing", "In-app"]
OFFER_TYPES = ["Discount", "Free Shipping", "Exclusive Access", "Bundle", "Cashback", "Early Release"]
INTERACTION_TYPES = ["Open", "Click", "Reply", "Conversion", "Unsubscribe"]
MESSAGE_THEMES = ["New Collection", "Sale", "VIP Benefit", "Reactivation", "Cross-sell", "Seasonal Drop"]
ISSUE_TYPES = ["Late Delivery", "Return Issue", "Payment", "Product Quality", "Login", "App Bug"]
SEVERITIES = ["Low", "Medium", "High", "Critical"]
DEVICE_TYPES = ["Mobile", "Desktop", "Tablet"]
EVENT_TYPES = ["page_view", "product_view", "add_to_cart", "wishlist", "checkout_start", "purchase", "app_open", "campaign_click"]
