SELECT
    fiscal_year,
    total_vouchers_paid,
    total_vouchers_pending,
    record_count,
    unique_suppliers
FROM vendor_payments_analytics.mart_spending_by_fiscal_year
ORDER BY fiscal_year;
