CREATE OR REPLACE VIEW analytics.spending_by_fiscal_year AS
SELECT
    fiscal_year,
    total_vouchers_paid,
    total_vouchers_pending,
    total_encumbrance_balance,
    total_pending_retainage,
    record_count,
    unique_suppliers,
    negative_paid_records,
    large_paid_1m_records,
    missing_po_date_records,
    LAG(total_vouchers_paid) OVER (
        ORDER BY fiscal_year
    ) AS previous_year_vouchers_paid,
    total_vouchers_paid
        - LAG(total_vouchers_paid) OVER (
            ORDER BY fiscal_year
        ) AS year_over_year_change
FROM landing.spending_by_fiscal_year;


CREATE OR REPLACE VIEW analytics.department_spending_ranked AS
SELECT
    fiscal_year,
    organization_group,
    department,
    total_vouchers_paid,
    total_vouchers_pending,
    total_encumbrance_balance,
    total_pending_retainage,
    record_count,
    unique_suppliers,
    RANK() OVER (
        PARTITION BY fiscal_year
        ORDER BY total_vouchers_paid DESC
    ) AS spending_rank
FROM landing.spending_by_department;


CREATE OR REPLACE VIEW analytics.supplier_spending_ranked AS
SELECT
    supplier_name,
    total_vouchers_paid,
    total_vouchers_pending,
    total_encumbrance_balance,
    total_pending_retainage,
    record_count,
    RANK() OVER (
        ORDER BY total_vouchers_paid DESC
    ) AS spending_rank
FROM landing.spending_by_supplier_top_n;


CREATE OR REPLACE VIEW analytics.fund_category_spending_ranked AS
SELECT
    fiscal_year,
    fund_type,
    fund_category,
    total_vouchers_paid,
    total_vouchers_pending,
    total_encumbrance_balance,
    total_pending_retainage,
    record_count,
    unique_suppliers,
    RANK() OVER (
        PARTITION BY fiscal_year
        ORDER BY total_vouchers_paid DESC
    ) AS spending_rank
FROM landing.fund_category_summary;


CREATE OR REPLACE VIEW analytics.pending_by_department_ranked AS
SELECT
    fiscal_year,
    department,
    total_vouchers_paid,
    total_vouchers_pending,
    total_encumbrance_balance,
    total_pending_retainage,
    record_count,
    unique_suppliers,
    RANK() OVER (
        PARTITION BY fiscal_year
        ORDER BY total_vouchers_pending DESC
    ) AS pending_rank
FROM landing.pending_by_department;