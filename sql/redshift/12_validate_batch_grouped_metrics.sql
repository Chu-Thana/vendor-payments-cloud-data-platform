SELECT
    'fiscal_year' AS group_type,
    CAST(fiscal_year AS VARCHAR) AS group_value,
    COUNT(*) AS group_row_count,
    SUM(record_count) AS source_record_count,
    SUM(total_vouchers_paid) AS total_vouchers_paid,
    SUM(total_vouchers_pending) AS total_vouchers_pending,
    SUM(total_encumbrance_balance) AS total_encumbrance_balance
FROM landing.spending_by_fiscal_year
GROUP BY fiscal_year

UNION ALL

SELECT
    'department' AS group_type,
    department AS group_value,
    COUNT(*) AS group_row_count,
    SUM(record_count) AS source_record_count,
    SUM(total_vouchers_paid) AS total_vouchers_paid,
    SUM(total_vouchers_pending) AS total_vouchers_pending,
    SUM(total_encumbrance_balance) AS total_encumbrance_balance
FROM landing.spending_by_department
GROUP BY department

UNION ALL

SELECT
    'fund_category' AS group_type,
    fund_category AS group_value,
    COUNT(*) AS group_row_count,
    SUM(record_count) AS source_record_count,
    SUM(total_vouchers_paid) AS total_vouchers_paid,
    SUM(total_vouchers_pending) AS total_vouchers_pending,
    SUM(total_encumbrance_balance) AS total_encumbrance_balance
FROM landing.fund_category_summary
GROUP BY fund_category

ORDER BY
    group_type,
    group_value;