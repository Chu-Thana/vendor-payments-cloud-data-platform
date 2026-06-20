SELECT
    COUNT(*) AS fiscal_year_rows,
    SUM(event_count) AS total_events,
    SUM(distinct_event_count) AS total_distinct_events,
    SUM(total_payment_amount) AS total_payment_amount
FROM analytics.streaming_events_by_fiscal_year;


SELECT
    fiscal_year,
    event_count,
    distinct_event_count,
    total_payment_amount,
    unique_departments,
    unique_suppliers
FROM analytics.streaming_events_by_fiscal_year
ORDER BY fiscal_year;


SELECT
    fiscal_year,
    department,
    event_count,
    total_payment_amount,
    payment_rank
FROM analytics.streaming_events_by_department
WHERE payment_rank <= 5
ORDER BY fiscal_year, payment_rank;


SELECT
    supplier_name,
    event_count,
    total_payment_amount,
    fiscal_year_count,
    payment_rank
FROM analytics.streaming_events_by_supplier
WHERE payment_rank <= 10
ORDER BY payment_rank;