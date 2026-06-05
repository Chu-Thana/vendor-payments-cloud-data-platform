SELECT
    fiscal_year,
    department,
    total_vouchers_pending,
    total_vouchers_paid,
    record_count
FROM vendor_payments_analytics.mart_pending_by_department
ORDER BY total_vouchers_pending DESC
LIMIT 20;
