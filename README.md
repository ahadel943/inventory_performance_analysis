# **Inventory Performance Analysis**

## **Project Overview**
This project analyzes inventory performance across a multi-store retail business to understand how inventory levels, sales demand, stock availability, and replenishment activity interact across products and stores.

The analysis uses product, store, sales, inventory snapshot, and purchase order data to evaluate overall inventory health and identify patterns of stockouts, excess inventory, slow-moving products, and replenishment risks. The project follows a SQL-based analytical workflow in PostgreSQL, starting from raw operational data through data quality validation and preparation of an analytical data layer before conducting the business analysis.

## **Business Problem**
Retail businesses need to maintain enough inventory to meet customer demand without tying up excessive capital in slow-moving or unnecessary stock. Poor inventory performance can appear in different forms: products may frequently run out of stock despite strong demand, while other products may remain overstocked with limited sales activity. These issues can also vary significantly across stores and may be influenced by replenishment patterns and purchase order performance.

Without a clear view of these patterns, it can be difficult to determine which products and stores require replenishment attention, which carry excess inventory, and where inventory inefficiencies are concentrated.

## **Project Goal**
The goal of this project is to evaluate inventory performance across products and stores, identify the main patterns behind stock inefficiency, and determine where the business should prioritize replenishment or inventory reduction.

The analysis will focus on inventory availability, stockouts, excess and slow-moving inventory, demand patterns, inventory turnover, and replenishment activity, with the aim of translating these findings into actionable inventory management priorities.

## **Business Problem**
**NO SUMMARY YET**

## **Dataset Description**
The project uses five datasets representing the core operational activities of a retail inventory system. Together, they provide information about products, stores, sales transactions, inventory levels, and replenishment through purchase orders.

### **1.Products**
| Column | Description |
| ------ | ----------- |
| `product_id` | Unique identifier for each product. |
| `category` | Product category. |
| `brand` | Product brand. |
| `unit_cost` | Cost incurred by the business for one unit of the product. |
| `unit_price` | Selling price of one unit. |
| `launch_date` | Date when the product was introduced. |
| `demand_class` | Demand classification of the product. |
| `reorder_point` | Inventory level at which replenishment should be considered. |
| `target_stock` | Target inventory level maintained for the product. |
- **Grain:** One row per product.

### **2.Stores**
| Column | Description |
| ------ | ----------- |
| `store_id` | Unique identifier for each store. |
| `region` | Geographic region of the store. |
| `city` | City where the store is located. |
| `store_type` | Store classification based on its size/type. |
| `demand_multiplier` | Relative demand factor representing differences in store-level sales volume. |
- **Grain:** One row per store.

### **3.Sales**
| Column | Description |
| ------ | ----------- |
| `sale_id` | Unique identifier for each sales transaction. |
| `sale_date` | Date when the sale occurred. |
| `store_id` | Identifier of the store where the sale occurred. |
| `product_id` | Identifier of the product sold. |
| `unit_price` | Selling price per unit at the time of the transaction. |
| `quantity` | Number of units sold in the transaction. |
- **Grain:** One row per sales transaction.

### **4. Inventory Snapshots**
| Column | Description |
| ------ | ----------- |
| `snapshot_date` | Date on which the inventory level was recorded. |
| `store_id` | Identifier of the store holding the inventory. |
| `product_id` | Identifier of the product being tracked. |
| `stock_on_hand` | Physical inventory quantity recorded at the store. |
| `stock_reserved` | Portion of the on-hand inventory reserved for existing orders or other commitments. |
- **Grain:** One row per product-store combination at each inventory snapshot date.

### **5. Purchase Orders**
| Column | Description |
| ------ | ----------- |
| `po_id` | Unique identifier for the purchase order. |
| `product_id` | Identifier of the product being ordered. |
| `store_id` | Identifier of the store requesting the inventory. |
| `order_date` | Date when the purchase order was placed. |
| `quantity_ordered` | Quantity requested in the purchase order. |
| `expected_date` | Expected date for receiving the order. |
| `received_date` | Actual date when the order was received. |
| `quantity_received` | Quantity actually received from the purchase order. |
- **Grain:** One row per purchase order.

### **Dataset Summary**
| Column | Ros | Role in Analysis |
| ------ | ----------- | -------- |
| `products` | **5,000** | Product attributes, pricing, cost, and inventory targets |
| `stores` | **40** | Store and geographic attributes |
| `sales` | **2,517,500** | Customer demand and sales velocity |
| `inventory_snapshots` | **7,800,000** | Inventory levels and stock availability over time |
| `purchase_orders` | **125,625** | Replenishment activity and receiving performance |
