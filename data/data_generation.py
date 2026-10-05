import numpy as np
import pandas as pd
from pathlib import Path

# ============================================================
# INVENTORY PERFORMANCE ANALYSIS
# Synthetic Retail Dataset Generator
# ============================================================

# -----------------------------
# Configuration
# -----------------------------

SEED = 42
rng = np.random.default_rng(SEED)

OUTPUT_DIR = Path("inventory_performance_dataset")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

N_PRODUCTS = 5_000
N_STORES = 40

START_DATE = pd.Timestamp("2026-01-01")
END_DATE = pd.Timestamp("2026-09-30")

TARGET_SALES = 2_500_000
TARGET_PURCHASE_ORDERS = 125_000

# Inventory will be weekly.
SNAPSHOT_DATES = pd.date_range(
    START_DATE,
    END_DATE,
    freq="7D"
)

# ============================================================
# 1. PRODUCTS
# ============================================================

print("Generating products...")

categories = [
    "Electronics",
    "Home Appliances",
    "Furniture",
    "Kitchen",
    "Personal Care",
    "Sports",
    "Stationery",
    "Clothing",
    "Accessories"
]

category_probs = np.array([
    0.11,
    0.09,
    0.08,
    0.13,
    0.12,
    0.09,
    0.10,
    0.16,
    0.12
])

category_probs = category_probs / category_probs.sum()

product_category = rng.choice(
    categories,
    size=N_PRODUCTS,
    p=category_probs
)

brands_by_category = {
    "Electronics": [
        "NovaTech", "PixelPro", "Voltix", "SmartCore"
    ],
    "Home Appliances": [
        "HomePlus", "Arctic", "PrimeHome", "Voltix"
    ],
    "Furniture": [
        "UrbanWood", "CasaLine", "ModernNest", "OakHouse"
    ],
    "Kitchen": [
        "ChefMate", "KitchenPro", "CasaLine", "DailyHome"
    ],
    "Personal Care": [
        "PureLife", "CarePlus", "Glow", "DailyCare"
    ],
    "Sports": [
        "ActiveX", "Motion", "PeakFit", "Sportiva"
    ],
    "Stationery": [
        "WriteWell", "OfficePro", "StudyMate", "PaperLine"
    ],
    "Clothing": [
        "UrbanWear", "Mode", "StreetLine", "Everyday"
    ],
    "Accessories": [
        "UrbanWear", "StyleHub", "Everyday", "TrendX"
    ]
}

cost_ranges = {
    "Electronics": (40, 1200),
    "Home Appliances": (100, 2500),
    "Furniture": (150, 5000),
    "Kitchen": (20, 900),
    "Personal Care": (10, 500),
    "Sports": (20, 1000),
    "Stationery": (3, 150),
    "Clothing": (15, 700),
    "Accessories": (8, 600)
}

products = pd.DataFrame({
    "product_id": [
        f"P{i:05d}" for i in range(1, N_PRODUCTS + 1)
    ],
    "category": product_category
})

products["brand"] = [
    rng.choice(brands_by_category[category])
    for category in products["category"]
]

# Generate unit cost by category
unit_cost = np.zeros(N_PRODUCTS)

for category, (low, high) in cost_ranges.items():

    mask = products["category"].eq(category)

    unit_cost[mask] = np.exp(
        rng.uniform(
            np.log(low),
            np.log(high),
            mask.sum()
        )
    )

markup = rng.uniform(
    1.18,
    1.65,
    N_PRODUCTS
)

products["unit_cost"] = np.round(
    unit_cost,
    2
)

products["unit_price"] = np.round(
    unit_cost * markup,
    2
)

# Product launch dates
products["launch_date"] = pd.to_datetime(
    rng.choice(
        pd.date_range(
            "2025-01-01",
            "2026-08-31",
            freq="D"
        ),
        size=N_PRODUCTS
    )
)

# Product demand strength.
# This is the hidden underlying demand driver.
product_demand = rng.lognormal(
    mean=1.3,
    sigma=1.0,
    size=N_PRODUCTS
)

products["demand_class"] = pd.qcut(
    product_demand,
    q=[0, 0.20, 0.50, 0.80, 1.00],
    labels=[
        "Low",
        "Medium",
        "High",
        "Very High"
    ]
).astype(str)

# Reorder point and target stock.
products["reorder_point"] = np.maximum(
    5,
    np.round(
        product_demand *
        rng.uniform(2.5, 7.0, N_PRODUCTS)
    )
).astype(int)

products["target_stock"] = np.maximum(
    products["reorder_point"] + 1,
    np.round(
        products["reorder_point"] *
        rng.uniform(1.4, 2.6, N_PRODUCTS)
    )
).astype(int)

# ------------------------------------------------------------
# Intentional product data-quality problems
# ------------------------------------------------------------

# Missing brand ~1%
missing_brand_idx = rng.choice(
    N_PRODUCTS,
    size=50,
    replace=False
)

products.loc[
    missing_brand_idx,
    "brand"
] = pd.NA

# Missing category ~0.5%
remaining_idx = np.setdiff1d(
    np.arange(N_PRODUCTS),
    missing_brand_idx
)

missing_category_idx = rng.choice(
    remaining_idx,
    size=25,
    replace=False
)

products.loc[
    missing_category_idx,
    "category"
] = pd.NA

products.to_csv(
    OUTPUT_DIR / "products.csv",
    index=False
)

print(f"products: {len(products):,} rows")


# ============================================================
# 2. STORES
# ============================================================

print("Generating stores...")

regions = {
    "Cairo": [
        "Cairo"
    ],
    "Giza": [
        "Giza"
    ],
    "Alexandria": [
        "Alexandria"
    ],
    "Delta": [
        "Mansoura",
        "Tanta",
        "Zagazig",
        "Damanhur"
    ],
    "Upper Egypt": [
        "Minya",
        "Assiut",
        "Sohag"
    ],
    "Canal": [
        "Ismailia",
        "Suez",
        "Port Said"
    ]
}

region_names = list(regions.keys())

stores = pd.DataFrame({
    "store_id": [
        f"S{i:03d}" for i in range(1, N_STORES + 1)
    ],
    "region": rng.choice(
        region_names,
        N_STORES,
        p=[
            0.25,
            0.15,
            0.15,
            0.20,
            0.15,
            0.10
        ]
    )
})

stores["city"] = [
    rng.choice(regions[region])
    for region in stores["region"]
]

stores["store_type"] = rng.choice(
    [
        "Large",
        "Medium",
        "Small"
    ],
    N_STORES,
    p=[
        0.25,
        0.50,
        0.25
    ]
)

store_multiplier_map = {
    "Large": 1.70,
    "Medium": 1.00,
    "Small": 0.55
}

stores["demand_multiplier"] = (
    stores["store_type"]
    .map(store_multiplier_map)
    .astype(float)
)

# Some stores are naturally stronger/weaker.
special_stores = rng.choice(
    N_STORES,
    size=6,
    replace=False
)

stores.loc[
    special_stores[:3],
    "demand_multiplier"
] *= 1.35

stores.loc[
    special_stores[3:],
    "demand_multiplier"
] *= 0.70

stores["demand_multiplier"] = np.round(
    stores["demand_multiplier"],
    2
)

# Missing store type
missing_store_type_idx = rng.choice(
    N_STORES,
    size=2,
    replace=False
)

stores.loc[
    missing_store_type_idx,
    "store_type"
] = pd.NA

stores.to_csv(
    OUTPUT_DIR / "stores.csv",
    index=False
)

print(f"stores: {len(stores):,} rows")


# ============================================================
# 3. SALES
# ============================================================

print("Generating sales...")

product_ids = products["product_id"].to_numpy()
store_ids = stores["store_id"].to_numpy()

# Category-level seasonal/demand effect
seasonality_by_category = {
    "Electronics": 1.10,
    "Home Appliances": 1.05,
    "Furniture": 0.95,
    "Kitchen": 1.00,
    "Personal Care": 1.00,
    "Sports": 1.08,
    "Stationery": 1.18,
    "Clothing": 1.12,
    "Accessories": 1.08
}

category_factor = np.array([
    seasonality_by_category.get(
        category,
        0.90
    )
    if pd.notna(category)
    else 0.90
    for category in products["category"]
])

product_weights = (
    product_demand *
    category_factor
)

product_weights = (
    product_weights /
    product_weights.sum()
)

store_weights = (
    stores["demand_multiplier"]
    .fillna(0.90)
    .to_numpy()
)

store_weights = (
    store_weights /
    store_weights.sum()
)

date_range = pd.date_range(
    START_DATE,
    END_DATE,
    freq="D"
)

monthly_factor = {
    1: 0.92,
    2: 0.95,
    3: 1.00,
    4: 0.98,
    5: 1.02,
    6: 1.05,
    7: 1.00,
    8: 1.10,
    9: 1.12
}

date_weights = np.array([
    monthly_factor[date.month]
    for date in date_range
])

date_weights /= date_weights.sum()

# Generate product/store/date selections
sale_product_idx = rng.choice(
    N_PRODUCTS,
    size=TARGET_SALES,
    p=product_weights
)

sale_store_idx = rng.choice(
    N_STORES,
    size=TARGET_SALES,
    p=store_weights
)

sale_dates = rng.choice(
    date_range.to_numpy(),
    size=TARGET_SALES,
    p=date_weights
)

# Quantity distribution
random_values = rng.random(
    TARGET_SALES
)

quantity = np.where(
    random_values < 0.68,
    1,
    np.where(
        random_values < 0.90,
        rng.integers(
            2,
            4,
            TARGET_SALES
        ),
        rng.integers(
            4,
            11,
            TARGET_SALES
        )
    )
)

sales = pd.DataFrame({
    "sale_id": [
        f"SALE{i:08d}"
        for i in range(1, TARGET_SALES + 1)
    ],
    "sale_date": pd.to_datetime(sale_dates),
    "store_id": store_ids[sale_store_idx],
    "product_id": product_ids[sale_product_idx]
})

sales["unit_price"] = np.round(
    products["unit_price"]
    .to_numpy()[sale_product_idx]
    *
    rng.uniform(
        0.96,
        1.04,
        TARGET_SALES
    ),
    2
)

sales["quantity"] = quantity.astype(
    np.int16
)

# ------------------------------------------------------------
# Sales data-quality issues
# ------------------------------------------------------------

# Missing price ~0.4%
missing_price_n = int(
    TARGET_SALES * 0.004
)

missing_price_idx = rng.choice(
    TARGET_SALES,
    size=missing_price_n,
    replace=False
)

sales.loc[
    missing_price_idx,
    "unit_price"
] = np.nan

# Invalid quantities ~0.1%
invalid_quantity_n = int(
    TARGET_SALES * 0.001
)

invalid_quantity_idx = rng.choice(
    TARGET_SALES,
    size=invalid_quantity_n,
    replace=False
)

half = invalid_quantity_n // 2

sales.loc[
    invalid_quantity_idx[:half],
    "quantity"
] = 0

sales.loc[
    invalid_quantity_idx[half:],
    "quantity"
] = -1

# Orphan product references ~0.15%
orphan_sales_n = int(
    TARGET_SALES * 0.0015
)

orphan_sales_idx = rng.choice(
    TARGET_SALES,
    size=orphan_sales_n,
    replace=False
)

sales.loc[
    orphan_sales_idx,
    "product_id"
] = [
    f"INVALID_P{i:05d}"
    for i in range(orphan_sales_n)
]

# Duplicate transactions ~0.7%
duplicate_n = int(
    TARGET_SALES * 0.007
)

duplicate_source_idx = rng.choice(
    sales.index,
    size=duplicate_n,
    replace=False
)

sales_duplicates = sales.loc[
    duplicate_source_idx
].copy()

sales = pd.concat(
    [
        sales,
        sales_duplicates
    ],
    ignore_index=True
)

# Shuffle
sales = sales.sample(
    frac=1,
    random_state=SEED
).reset_index(drop=True)

sales.to_csv(
    OUTPUT_DIR / "sales.csv",
    index=False
)

print(f"sales: {len(sales):,} rows")


# ============================================================
# 4. PURCHASE ORDERS
# ============================================================

print("Generating purchase orders...")

po_product_idx = rng.choice(
    N_PRODUCTS,
    TARGET_PURCHASE_ORDERS,
    p=product_weights
)

po_store_idx = rng.choice(
    N_STORES,
    TARGET_PURCHASE_ORDERS,
    p=store_weights
)

po_order_dates = pd.to_datetime(
    rng.choice(
        date_range.to_numpy(),
        TARGET_PURCHASE_ORDERS
    )
)

quantity_ordered = np.maximum(
    5,
    np.round(
        product_demand[po_product_idx] *
        rng.uniform(
            2.5,
            8.0,
            TARGET_PURCHASE_ORDERS
        )
    )
).astype(int)

purchase_orders = pd.DataFrame({
    "po_id": [
        f"PO{i:07d}"
        for i in range(
            1,
            TARGET_PURCHASE_ORDERS + 1
        )
    ],
    "product_id": product_ids[po_product_idx],
    "store_id": store_ids[po_store_idx],
    "order_date": po_order_dates,
    "quantity_ordered": quantity_ordered
})

# Expected lead time
lead_days = rng.integers(
    3,
    22,
    TARGET_PURCHASE_ORDERS
)

purchase_orders["expected_date"] = (
    purchase_orders["order_date"]
    +
    pd.to_timedelta(
        lead_days,
        unit="D"
    )
)

# PO states
po_state = rng.choice(
    [
        "Normal",
        "Late",
        "Partial",
        "Open"
    ],
    TARGET_PURCHASE_ORDERS,
    p=[
        0.72,
        0.13,
        0.08,
        0.07
    ]
)

received_date = pd.Series(
    pd.NaT,
    index=purchase_orders.index,
    dtype="datetime64[ns]"
)

quantity_received = np.zeros(
    TARGET_PURCHASE_ORDERS,
    dtype=np.int32
)

normal_mask = po_state == "Normal"
late_mask = po_state == "Late"
partial_mask = po_state == "Partial"
open_mask = po_state == "Open"

# Normal
normal_delay = rng.integers(
    -2,
    3,
    normal_mask.sum()
)

received_date.loc[normal_mask] = (
    purchase_orders.loc[
        normal_mask,
        "expected_date"
    ].to_numpy()
    +
    pd.to_timedelta(
        normal_delay,
        unit="D"
    )
)

quantity_received[normal_mask] = (
    purchase_orders.loc[
        normal_mask,
        "quantity_ordered"
    ].to_numpy()
)

# Late
late_delay = rng.integers(
    3,
    16,
    late_mask.sum()
)

received_date.loc[late_mask] = (
    purchase_orders.loc[
        late_mask,
        "expected_date"
    ].to_numpy()
    +
    pd.to_timedelta(
        late_delay,
        unit="D"
    )
)

quantity_received[late_mask] = (
    purchase_orders.loc[
        late_mask,
        "quantity_ordered"
    ].to_numpy()
)

# Partial
partial_delay = rng.integers(
    0,
    12,
    partial_mask.sum()
)

received_date.loc[partial_mask] = (
    purchase_orders.loc[
        partial_mask,
        "expected_date"
    ].to_numpy()
    +
    pd.to_timedelta(
        partial_delay,
        unit="D"
    )
)

partial_ratio = rng.uniform(
    0.35,
    0.85,
    partial_mask.sum()
)

quantity_received[partial_mask] = np.floor(
    purchase_orders.loc[
        partial_mask,
        "quantity_ordered"
    ].to_numpy()
    *
    partial_ratio
).astype(int)

# Open POs
quantity_received[open_mask] = 0

purchase_orders["received_date"] = received_date

purchase_orders["quantity_received"] = (
    quantity_received
)

# ------------------------------------------------------------
# PO quality/business issues
# ------------------------------------------------------------

# Over-received POs ~1.5% of received POs
received_idx = purchase_orders.index[
    purchase_orders["received_date"].notna()
]

over_received_n = int(
    len(received_idx) * 0.015
)

over_received_idx = rng.choice(
    received_idx,
    size=over_received_n,
    replace=False
)

purchase_orders.loc[
    over_received_idx,
    "quantity_received"
] = (
    purchase_orders.loc[
        over_received_idx,
        "quantity_ordered"
    ].to_numpy()
    +
    rng.integers(
        1,
        15,
        over_received_n
    )
)

# Invalid expected date:
# expected_date < order_date
bad_expected_n = int(
    TARGET_PURCHASE_ORDERS * 0.0015
)

bad_expected_idx = rng.choice(
    TARGET_PURCHASE_ORDERS,
    size=bad_expected_n,
    replace=False
)

purchase_orders.loc[
    bad_expected_idx,
    "expected_date"
] = (
    purchase_orders.loc[
        bad_expected_idx,
        "order_date"
    ].to_numpy()
    -
    pd.to_timedelta(
        rng.integers(
            1,
            5,
            bad_expected_n
        ),
        unit="D"
    )
)

# Invalid received date:
# received_date < order_date
valid_received_idx = purchase_orders.index[
    purchase_orders["received_date"].notna()
]

bad_received_n = int(
    TARGET_PURCHASE_ORDERS * 0.001
)

bad_received_idx = rng.choice(
    valid_received_idx,
    size=bad_received_n,
    replace=False
)

purchase_orders.loc[
    bad_received_idx,
    "received_date"
] = (
    purchase_orders.loc[
        bad_received_idx,
        "order_date"
    ].to_numpy()
    -
    pd.to_timedelta(
        rng.integers(
            1,
            4,
            bad_received_n
        ),
        unit="D"
    )
)

# Duplicate PO records ~0.5%
po_duplicate_n = int(
    TARGET_PURCHASE_ORDERS * 0.005
)

po_duplicate_idx = rng.choice(
    purchase_orders.index,
    size=po_duplicate_n,
    replace=False
)

po_duplicates = purchase_orders.loc[
    po_duplicate_idx
].copy()

purchase_orders = pd.concat(
    [
        purchase_orders,
        po_duplicates
    ],
    ignore_index=True
)

purchase_orders = purchase_orders.sample(
    frac=1,
    random_state=SEED
).reset_index(drop=True)

purchase_orders.to_csv(
    OUTPUT_DIR / "purchase_orders.csv",
    index=False
)

print(
    f"purchase_orders: "
    f"{len(purchase_orders):,} rows"
)


# ============================================================
# 5. INVENTORY SNAPSHOTS
# ============================================================

print("Generating inventory snapshots...")
print(
    "This is the largest table. "
    "It will be written in chunks."
)

# We intentionally generate weekly:
#
# 5,000 products
# × 40 stores
# × ~40 weeks
#
# ≈ 8 million rows

N_WEEKS = len(SNAPSHOT_DATES)

# Store demand multipliers
store_demand = (
    stores["demand_multiplier"]
    .fillna(0.90)
    .to_numpy()
)

# Product/store inventory behavior.
#
# inventory_factor < 1
#     → understock tendency
#
# inventory_factor > 1
#     → overstock tendency

inventory_factor = rng.lognormal(
    mean=0.0,
    sigma=0.45,
    size=(N_PRODUCTS, N_STORES)
)

# ------------------------------------------------------------
# Explicit business scenarios
# ------------------------------------------------------------

# High-demand products
high_demand_products = np.argsort(
    product_demand
)[-500:]

understock_products = rng.choice(
    high_demand_products,
    size=120,
    replace=False
)

understock_stores = rng.integers(
    0,
    N_STORES,
    size=120
)

for product_idx, store_idx in zip(
    understock_products,
    understock_stores
):
    inventory_factor[
        product_idx,
        store_idx
    ] *= rng.uniform(
        0.25,
        0.55
    )

# Low-demand products
low_demand_products = np.argsort(
    product_demand
)[:1_200]

overstock_products = rng.choice(
    low_demand_products,
    size=180,
    replace=False
)

overstock_stores = rng.integers(
    0,
    N_STORES,
    size=180
)

for product_idx, store_idx in zip(
    overstock_products,
    overstock_stores
):
    inventory_factor[
        product_idx,
        store_idx
    ] *= rng.uniform(
        2.5,
        5.0
    )

# ------------------------------------------------------------
# Generate one week at a time
# ------------------------------------------------------------

inventory_file = (
    OUTPUT_DIR /
    "inventory_snapshots.csv"
)

# Remove previous file if it exists
if inventory_file.exists():
    inventory_file.unlink()

first_chunk = True

for week_number, snapshot_date in enumerate(
    SNAPSHOT_DATES,
    start=1
):

    # Every product × every store
    product_grid = np.repeat(
        np.arange(N_PRODUCTS),
        N_STORES
    )

    store_grid = np.tile(
        np.arange(N_STORES),
        N_PRODUCTS
    )

    n_rows = len(product_grid)

    # Base demand
    base_demand = (
        product_demand[product_grid]
        *
        store_demand[store_grid]
    )

    # Inventory policy
    target_stock = (
        products["target_stock"]
        .to_numpy()[product_grid]
    )

    policy = (
        target_stock
        *
        inventory_factor[
            product_grid,
            store_grid
        ]
    )

    # Weekly random variation
    noise = rng.lognormal(
        mean=0.0,
        sigma=0.40,
        size=n_rows
    )

    stock = (
        policy *
        noise
    )

    # Seasonal effect
    month = snapshot_date.month

    seasonal_factor = monthly_factor.get(
        month,
        1.0
    )

    stock = (
        stock /
        max(
            0.45,
            seasonal_factor
        )
    )

    # --------------------------------------------------------
    # Natural stockouts
    # --------------------------------------------------------

    stockout_probability = np.clip(
        0.015
        +
        (
            base_demand /
            np.quantile(
                base_demand,
                0.90
            )
        ) * 0.03
        +
        (
            1 /
            np.maximum(
                inventory_factor[
                    product_grid,
                    store_grid
                ],
                0.25
            )
        ) * 0.01,
        0.01,
        0.12
    )

    stockout_mask = (
        rng.random(n_rows)
        <
        stockout_probability
    )

    stock[stockout_mask] = 0

    # Products not yet launched should have no stock
    launch_dates = (
        products["launch_date"]
        .to_numpy()
        .astype("datetime64[ns]")
    )

    not_launched = (
        np.datetime64(snapshot_date)
        <
        launch_dates[product_grid]
    )

    stock[not_launched] = 0

    stock = np.maximum(
        0,
        np.rint(stock)
    ).astype(np.int32)

    # Reserved stock
    reserved_ratio = rng.beta(
        1.4,
        8.0,
        n_rows
    )

    stock_reserved = np.floor(
        stock *
        reserved_ratio
    ).astype(np.int32)

    inventory_chunk = pd.DataFrame({
        "snapshot_date": snapshot_date,
        "store_id": store_ids[store_grid],
        "product_id": product_ids[product_grid],
        "stock_on_hand": stock,
        "stock_reserved": stock_reserved
    })

    # --------------------------------------------------------
    # Inventory data-quality issues
    # --------------------------------------------------------

    # Negative stock ~0.04%
    negative_n = max(
        1,
        int(n_rows * 0.0004)
    )

    negative_idx = rng.choice(
        n_rows,
        size=negative_n,
        replace=False
    )

    inventory_chunk.loc[
        negative_idx,
        "stock_on_hand"
    ] = -rng.integers(
        1,
        8,
        negative_n
    )

    # Reserved stock > stock on hand ~0.05%
    positive_rows = np.flatnonzero(
        inventory_chunk[
            "stock_on_hand"
        ].to_numpy() > 0
    )

    if len(positive_rows) > 0:

        reserved_error_n = max(
            1,
            int(len(positive_rows) * 0.0005)
        )

        reserved_error_idx = rng.choice(
            positive_rows,
            size=reserved_error_n,
            replace=False
        )

        inventory_chunk.loc[
            reserved_error_idx,
            "stock_reserved"
        ] = (
            inventory_chunk.loc[
                reserved_error_idx,
                "stock_on_hand"
            ].to_numpy()
            +
            rng.integers(
                1,
                10,
                reserved_error_n
            )
        )

    # Orphan product references ~0.1%
    orphan_n = max(
        1,
        int(n_rows * 0.001)
    )

    orphan_idx = rng.choice(
        n_rows,
        size=orphan_n,
        replace=False
    )

    inventory_chunk.loc[
        orphan_idx,
        "product_id"
    ] = [
        f"INVALID_P{i:05d}"
        for i in range(orphan_n)
    ]

    # --------------------------------------------------------
    # Write this week's chunk
    # --------------------------------------------------------

    inventory_chunk.to_csv(
        inventory_file,
        mode="w" if first_chunk else "a",
        header=first_chunk,
        index=False
    )

    first_chunk = False

    print(
        f"Week {week_number:02d}/{N_WEEKS} "
        f"completed"
    )


# ============================================================
# 6. GENERATION SUMMARY
# ============================================================

summary = f"""
INVENTORY PERFORMANCE ANALYSIS
Synthetic Dataset Generation Summary
=====================================

Seed:
{SEED}

Analysis period:
{START_DATE.date()} to {END_DATE.date()}

Snapshot frequency:
Weekly

Tables:

products
--------
Rows: {len(products):,}

stores
------
Rows: {len(stores):,}

sales
-----
Rows: {len(sales):,}

purchase_orders
---------------
Rows: {len(purchase_orders):,}

inventory_snapshots
-------------------
Rows: {N_PRODUCTS * N_STORES * N_WEEKS:,}

Intentional data-quality issues
--------------------------------

Products:
- Missing brand ~1%
- Missing category ~0.5%

Stores:
- Missing store_type in a small number of stores

Sales:
- Missing unit_price ~0.4%
- Duplicate transactions ~0.7%
- Orphan product references ~0.15%
- Invalid quantities ~0.1%

Purchase Orders:
- Late receipts ~13%
- Partial receipts ~8%
- Open POs ~7%
- Over-receiving ~1.5% of received POs
- Invalid expected dates ~0.15%
- Invalid received dates ~0.10%
- Duplicate POs ~0.5%

Inventory:
- Negative stock ~0.04%
- Reserved stock > on-hand stock ~0.05%
- Orphan product references ~0.1%

Business conditions:
- High-demand / understocked product-store combinations
- Low-demand / overstocked product-store combinations
- Natural stockouts
- Seasonal demand variation
- Store demand differences
- Product demand concentration
- Different product demand classes
- Late and partial replenishment
- Open purchase orders
- Product launch dates

Important:
The generator does not hard-code the final analytical conclusions.
The SQL analysis should discover the actual inventory patterns.
"""

with open(
    OUTPUT_DIR / "generation_summary.txt",
    "w",
    encoding="utf-8"
) as file:
    file.write(
        summary.strip()
    )

print("\n" + "=" * 60)
print("DATA GENERATION COMPLETED")
print("=" * 60)
print(f"Output folder: {OUTPUT_DIR.resolve()}")
print()
print("Files:")
print("- products.csv")
print("- stores.csv")
print("- sales.csv")
print("- purchase_orders.csv")
print("- inventory_snapshots.csv")
print("- generation_summary.txt")