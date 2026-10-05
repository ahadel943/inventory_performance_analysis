-- ===============================================================
-- ===================== USING PSQL cli tool =====================
-- ===============================================================

-- first, switch connection to inventory_performance database
\c inventory_performance;

-- ===============================================================
-- ======================= CSVs DATA LOAD ========================
-- ===============================================================

-- products data
\copy raw_data.products (product_id, category, brand, unit_cost, unit_price, launch_date, demand_class, reorder_point, target_stock)
from 'FILE_PATH\\products.csv'
with (format csv, header true);

-- stores data
\copy raw_data.stores (store_id, region, city, store_type, demand_multiplier)
from 'FILE_PATH\\stores.csv'
with (format csv, header true);

-- sales data
\copy raw_data.sales (sale_id, sale_date, store_id, product_id, unit_price, quantity)
from 'FILE_PATH\\sales.csv'
with (format csv, header true);

-- inventory_snapshots data
\copy raw_data.inventory_snapshots (snapshot_date, store_id, product_id, stock_on_hand, stock_reserved)
from 'FILE_PATH\\inventory_snapshots.csv'
with (format csv, header true);

-- purchase_orders data
\copy raw_data.purchase_orders (po_id, product_id, store_id, order_date, quantity_ordered, expected_date, received_date, quantity_received)
from 'E:\DataAnalysis\_Projects\proj_18\source_data\purchase_orders.csv'
with (format csv, header true);