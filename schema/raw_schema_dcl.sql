/*
	============================================================================
    	USING psql COMMAND LINE TOOL FOR THE INITIAL SETUP AND FOR DATA LOAD
	============================================================================
*/

-- create project database
create database inventory_performance;

-- switch connection to inventory_performance
\c inventory_performance;

-- create raw data schema
create schema raw_data;

-- CRAETE RAW SCHEMA TABLE

-- products table
create table raw_data.products (
	product_id varchar,
	category varchar,
	brand varchar,
	unit_cost numeric(10, 2),
	unit_price numeric(10, 2),
	launch_date date,
	demand_class varchar,
	reorder_point integer,
	target_stock integer
);

-- stores table
create table raw_data.stores (
	store_id varchar,
	region varchar,
	city varchar,
	store_type varchar,
	demand_multiplier numeric(10, 2)
);

-- sales table
create table raw_data.sales (
	sale_id varchar,
	sale_date date,
	store_id varchar,
	product_id varchar,
	unit_price numeric(10, 2),
	quantity integer 
);

-- inventory_snapshots table 
create table raw_data.inventory_snapshots (
	snapshot_date date,
	store_id varchar,
	product_id varchar,
	stock_on_hand integer,
	stock_reserved integer
);

-- purchase_orders table
create table raw_data.purchase_orders (
	po_id varchar,
	product_id varchar,
	store_id varchar,
	order_date date,
	quantity_ordered integer,
	expected_date date,
	received_date date,
	quantity_received integer
);




















