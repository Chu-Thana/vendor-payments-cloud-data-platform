SELECT
  event_id,
  event_timestamp,
  event_type,
  fiscal_year,
  department_name,
  supplier_name,
  CAST(payment_amount AS DOUBLE) AS payment_amount
FROM vendor_payments_analytics.vendor_payments_streaming_events
LIMIT 10;


SELECT
  COUNT(*) AS total_streaming_events,
  COUNT(DISTINCT event_id) AS unique_event_ids
FROM vendor_payments_analytics.vendor_payments_streaming_events;


SELECT
  fiscal_year,
  COUNT(*) AS event_count,
  SUM(CAST(payment_amount AS DOUBLE)) AS total_payment_amount
FROM vendor_payments_analytics.vendor_payments_streaming_events
GROUP BY fiscal_year
ORDER BY fiscal_year;


SELECT
  department_name,
  COUNT(*) AS event_count,
  SUM(CAST(payment_amount AS DOUBLE)) AS total_payment_amount
FROM vendor_payments_analytics.vendor_payments_streaming_events
GROUP BY department_name
ORDER BY total_payment_amount DESC
LIMIT 10;