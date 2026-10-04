CREATE EXTERNAL TABLE IF NOT EXISTS vendor_payments_analytics.mart_spending_by_fiscal_year (
    fiscal_year INT,
    total_vouchers_paid DOUBLE,
    total_vouchers_pending DOUBLE,
    total_encumbrance_balance DOUBLE,
    total_pending_retainage DOUBLE,
    record_count BIGINT,
    negative_paid_records BIGINT,
    large_paid_1m_records BIGINT,
    missing_po_date_records BIGINT,
    unique_suppliers BIGINT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    'separatorChar' = ',',
    'quoteChar' = '\"',
    'escapeChar' = '\\'
)
STORED AS TEXTFILE
LOCATION 's3://vendor-payments-data-platform-thana/data-platform/vendor-payments/gold/full/mart_spending_by_fiscal_year/'
TBLPROPERTIES ('skip.header.line.count'='1');


CREATE EXTERNAL TABLE IF NOT EXISTS vendor_payments_analytics.mart_spending_by_department (
    fiscal_year INT,
    organization_group STRING,
    department STRING,
    total_vouchers_paid DOUBLE,
    total_vouchers_pending DOUBLE,
    total_encumbrance_balance DOUBLE,
    total_pending_retainage DOUBLE,
    record_count BIGINT,
    negative_paid_records BIGINT,
    large_paid_1m_records BIGINT,
    missing_po_date_records BIGINT,
    unique_suppliers BIGINT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    'separatorChar' = ',',
    'quoteChar' = '\"',
    'escapeChar' = '\\'
)
STORED AS TEXTFILE
LOCATION 's3://vendor-payments-data-platform-thana/data-platform/vendor-payments/gold/full/mart_spending_by_department/'
TBLPROPERTIES ('skip.header.line.count'='1');


CREATE EXTERNAL TABLE IF NOT EXISTS vendor_payments_analytics.mart_spending_by_supplier_top_n (
    supplier_name STRING,
    total_vouchers_paid DOUBLE,
    total_vouchers_pending DOUBLE,
    total_encumbrance_balance DOUBLE,
    total_pending_retainage DOUBLE,
    record_count BIGINT,
    negative_paid_records BIGINT,
    large_paid_1m_records BIGINT,
    missing_po_date_records BIGINT,
    unique_suppliers BIGINT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    'separatorChar' = ',',
    'quoteChar' = '\"',
    'escapeChar' = '\\'
)
STORED AS TEXTFILE
LOCATION 's3://vendor-payments-data-platform-thana/data-platform/vendor-payments/gold/full/mart_spending_by_supplier_top_n/'
TBLPROPERTIES ('skip.header.line.count'='1');


CREATE EXTERNAL TABLE IF NOT EXISTS vendor_payments_analytics.mart_pending_by_department (
    fiscal_year INT,
    department STRING,
    total_vouchers_paid DOUBLE,
    total_vouchers_pending DOUBLE,
    total_encumbrance_balance DOUBLE,
    total_pending_retainage DOUBLE,
    record_count BIGINT,
    negative_paid_records BIGINT,
    large_paid_1m_records BIGINT,
    missing_po_date_records BIGINT,
    unique_suppliers BIGINT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    'separatorChar' = ',',
    'quoteChar' = '\"',
    'escapeChar' = '\\'
)
STORED AS TEXTFILE
LOCATION 's3://vendor-payments-data-platform-thana/data-platform/vendor-payments/gold/full/mart_pending_by_department/'
TBLPROPERTIES ('skip.header.line.count'='1');


CREATE EXTERNAL TABLE IF NOT EXISTS vendor_payments_analytics.mart_fund_category_summary (
    fiscal_year INT,
    fund_type STRING,
    fund_category STRING,
    total_vouchers_paid DOUBLE,
    total_vouchers_pending DOUBLE,
    total_encumbrance_balance DOUBLE,
    total_pending_retainage DOUBLE,
    record_count BIGINT,
    negative_paid_records BIGINT,
    large_paid_1m_records BIGINT,
    missing_po_date_records BIGINT,
    unique_suppliers BIGINT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    'separatorChar' = ',',
    'quoteChar' = '\"',
    'escapeChar' = '\\'
)
STORED AS TEXTFILE
LOCATION 's3://vendor-payments-data-platform-thana/data-platform/vendor-payments/gold/full/mart_fund_category_summary/'
TBLPROPERTIES ('skip.header.line.count'='1');