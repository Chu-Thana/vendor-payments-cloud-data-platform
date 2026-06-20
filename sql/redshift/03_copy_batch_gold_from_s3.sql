TRUNCATE TABLE landing.spending_by_fiscal_year;

COPY landing.spending_by_fiscal_year
FROM 's3://vendor-payments-data-platform-thana/data-platform/vendor-payments/gold/full/mart_spending_by_fiscal_year/'
IAM_ROLE default
FORMAT AS CSV
IGNOREHEADER 1
REGION 'ap-southeast-1';


TRUNCATE TABLE landing.spending_by_department;

COPY landing.spending_by_department
FROM 's3://vendor-payments-data-platform-thana/data-platform/vendor-payments/gold/full/mart_spending_by_department/'
IAM_ROLE default
FORMAT AS CSV
IGNOREHEADER 1
REGION 'ap-southeast-1';


TRUNCATE TABLE landing.spending_by_supplier_top_n;

COPY landing.spending_by_supplier_top_n
FROM 's3://vendor-payments-data-platform-thana/data-platform/vendor-payments/gold/full/mart_spending_by_supplier_top_n/'
IAM_ROLE default
FORMAT AS CSV
IGNOREHEADER 1
REGION 'ap-southeast-1';


TRUNCATE TABLE landing.fund_category_summary;

COPY landing.fund_category_summary
FROM 's3://vendor-payments-data-platform-thana/data-platform/vendor-payments/gold/full/mart_fund_category_summary/'
IAM_ROLE default
FORMAT AS CSV
IGNOREHEADER 1
REGION 'ap-southeast-1';


TRUNCATE TABLE landing.pending_by_department;

COPY landing.pending_by_department
FROM 's3://vendor-payments-data-platform-thana/data-platform/vendor-payments/gold/full/mart_pending_by_department/'
IAM_ROLE default
FORMAT AS CSV
IGNOREHEADER 1
REGION 'ap-southeast-1';