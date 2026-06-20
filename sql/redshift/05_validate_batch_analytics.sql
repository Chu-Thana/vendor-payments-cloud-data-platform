SELECT
    fiscal_year,
    total_vouchers_paid,
    previous_year_vouchers_paid,
    year_over_year_change
FROM analytics.spending_by_fiscal_year
ORDER BY fiscal_year;


SELECT
    fiscal_year,
    department,
    total_vouchers_paid,
    spending_rank
FROM analytics.department_spending_ranked
WHERE spending_rank <= 5
ORDER BY fiscal_year, spending_rank;


SELECT
    supplier_name,
    total_vouchers_paid,
    spending_rank
FROM analytics.supplier_spending_ranked
WHERE spending_rank <= 10
ORDER BY spending_rank;