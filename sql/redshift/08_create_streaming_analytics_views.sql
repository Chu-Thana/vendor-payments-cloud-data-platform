CREATE OR REPLACE VIEW analytics.vendor_payments_streaming_events AS
SELECT
    event_id,
    CAST(event_timestamp AS TIMESTAMP) AS event_timestamp,
    event_type,
    CAST(fiscal_year AS INTEGER) AS fiscal_year,
    department,
    supplier_name,
    CAST(payment_amount AS DECIMAL(20, 2)) AS payment_amount,
    payment_status,
    dedup_status,
    business_composite_key,
    source_row_hash,
    source_system,
    CAST(ingested_at AS TIMESTAMP) AS ingested_at
FROM landing.vendor_payments_streaming_events;


CREATE OR REPLACE VIEW analytics.streaming_events_by_fiscal_year AS
SELECT
    fiscal_year,
    COUNT(*) AS event_count,
    COUNT(DISTINCT event_id) AS distinct_event_count,
    SUM(payment_amount) AS total_payment_amount,
    COUNT(DISTINCT department) AS unique_departments,
    COUNT(DISTINCT supplier_name) AS unique_suppliers
FROM analytics.vendor_payments_streaming_events
GROUP BY fiscal_year;


CREATE OR REPLACE VIEW analytics.streaming_events_by_department AS
SELECT
    fiscal_year,
    department,
    COUNT(*) AS event_count,
    SUM(payment_amount) AS total_payment_amount,
    COUNT(DISTINCT supplier_name) AS unique_suppliers,
    RANK() OVER (
        PARTITION BY fiscal_year
        ORDER BY SUM(payment_amount) DESC
    ) AS payment_rank
FROM analytics.vendor_payments_streaming_events
GROUP BY
    fiscal_year,
    department;


CREATE OR REPLACE VIEW analytics.streaming_events_by_supplier AS
SELECT
    supplier_name,
    COUNT(*) AS event_count,
    SUM(payment_amount) AS total_payment_amount,
    COUNT(DISTINCT fiscal_year) AS fiscal_year_count,
    RANK() OVER (
        ORDER BY SUM(payment_amount) DESC
    ) AS payment_rank
FROM analytics.vendor_payments_streaming_events
GROUP BY supplier_name;