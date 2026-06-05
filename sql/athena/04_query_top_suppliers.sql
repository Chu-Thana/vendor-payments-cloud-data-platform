SELECT
    supplier_name,
    total_vouchers_paid,
    total_vouchers_pending,
    record_count,
    large_paid_1m_records
FROM vendor_payments_analytics.mart_spending_by_supplier_top_n
ORDER BY total_vouchers_paid DESC
LIMIT 20;
