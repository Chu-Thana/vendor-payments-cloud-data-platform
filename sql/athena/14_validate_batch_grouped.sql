SELECT
    'fiscal_year' AS group_type,
    CAST(fiscal_year AS VARCHAR) AS group_value,
    COUNT(*) AS group_row_count,
    SUM(record_count) AS source_record_count,
    SUM(
        CAST(total_vouchers_paid AS DECIMAL(20, 2))
    ) AS total_vouchers_paid,
    SUM(
        CAST(total_vouchers_pending AS DECIMAL(20, 2))
    ) AS total_vouchers_pending,
    SUM(
        CAST(total_encumbrance_balance AS DECIMAL(20, 2))
    ) AS total_encumbrance_balance
FROM vendor_payments_analytics.mart_spending_by_fiscal_year
GROUP BY fiscal_year

UNION ALL

SELECT
    'department' AS group_type,
    department AS group_value,
    COUNT(*) AS group_row_count,
    SUM(record_count) AS source_record_count,
    SUM(
        CAST(total_vouchers_paid AS DECIMAL(20, 2))
    ) AS total_vouchers_paid,
    SUM(
        CAST(total_vouchers_pending AS DECIMAL(20, 2))
    ) AS total_vouchers_pending,
    SUM(
        CAST(total_encumbrance_balance AS DECIMAL(20, 2))
    ) AS total_encumbrance_balance
FROM vendor_payments_analytics.mart_spending_by_department
GROUP BY department

UNION ALL

SELECT
    'fund_category' AS group_type,
    fund_category AS group_value,
    COUNT(*) AS group_row_count,
    SUM(record_count) AS source_record_count,
    SUM(
        CAST(total_vouchers_paid AS DECIMAL(20, 2))
    ) AS total_vouchers_paid,
    SUM(
        CAST(total_vouchers_pending AS DECIMAL(20, 2))
    ) AS total_vouchers_pending,
    SUM(
        CAST(total_encumbrance_balance AS DECIMAL(20, 2))
    ) AS total_encumbrance_balance
FROM vendor_payments_analytics.mart_fund_category_summary
GROUP BY fund_category

ORDER BY
    group_type,
    group_value;