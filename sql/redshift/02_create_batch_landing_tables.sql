DROP TABLE IF EXISTS landing.spending_by_fiscal_year;

CREATE TABLE landing.spending_by_fiscal_year (
    fiscal_year                 INTEGER,
    total_vouchers_paid         DECIMAL(20, 2),
    total_vouchers_pending      DECIMAL(20, 2),
    total_encumbrance_balance   DECIMAL(20, 2),
    total_pending_retainage     DECIMAL(20, 2),
    record_count                BIGINT,
    unique_suppliers            BIGINT,
    negative_paid_records       BIGINT,
    large_paid_1m_records       BIGINT,
    missing_po_date_records     BIGINT
);


DROP TABLE IF EXISTS landing.spending_by_department;

CREATE TABLE landing.spending_by_department (
    fiscal_year                 INTEGER,
    organization_group          VARCHAR(256),
    department                  VARCHAR(256),
    total_vouchers_paid         DECIMAL(20, 2),
    total_vouchers_pending      DECIMAL(20, 2),
    total_encumbrance_balance   DECIMAL(20, 2),
    total_pending_retainage     DECIMAL(20, 2),
    record_count                BIGINT,
    unique_suppliers            BIGINT,
    negative_paid_records       BIGINT,
    large_paid_1m_records       BIGINT,
    missing_po_date_records     BIGINT
);


DROP TABLE IF EXISTS landing.spending_by_supplier_top_n;

CREATE TABLE landing.spending_by_supplier_top_n (
    supplier_name               VARCHAR(512),
    total_vouchers_paid         DECIMAL(20, 2),
    total_vouchers_pending      DECIMAL(20, 2),
    total_encumbrance_balance   DECIMAL(20, 2),
    total_pending_retainage     DECIMAL(20, 2),
    record_count                BIGINT,
    unique_suppliers            BIGINT,
    negative_paid_records       BIGINT,
    large_paid_1m_records       BIGINT,
    missing_po_date_records     BIGINT
);


DROP TABLE IF EXISTS landing.fund_category_summary;

CREATE TABLE landing.fund_category_summary (
    fiscal_year                 INTEGER,
    fund_type                   VARCHAR(256),
    fund_category               VARCHAR(256),
    total_vouchers_paid         DECIMAL(20, 2),
    total_vouchers_pending      DECIMAL(20, 2),
    total_encumbrance_balance   DECIMAL(20, 2),
    total_pending_retainage     DECIMAL(20, 2),
    record_count                BIGINT,
    unique_suppliers            BIGINT,
    negative_paid_records       BIGINT,
    large_paid_1m_records       BIGINT,
    missing_po_date_records     BIGINT
);


DROP TABLE IF EXISTS landing.pending_by_department;

CREATE TABLE landing.pending_by_department (
    fiscal_year                 INTEGER,
    department                  VARCHAR(256),
    total_vouchers_paid         DECIMAL(20, 2),
    total_vouchers_pending      DECIMAL(20, 2),
    total_encumbrance_balance   DECIMAL(20, 2),
    total_pending_retainage     DECIMAL(20, 2),
    record_count                BIGINT,
    unique_suppliers            BIGINT,
    negative_paid_records       BIGINT,
    large_paid_1m_records       BIGINT,
    missing_po_date_records     BIGINT
);