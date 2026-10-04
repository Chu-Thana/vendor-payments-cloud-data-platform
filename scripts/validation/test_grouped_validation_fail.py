from scripts.validation.compare_grouped_batch_metrics import (
    compare_grouped_batch_metrics,
)


athena_results = [
    {
        "group_type": "fiscal_year",
        "group_value": "2024",
        "group_row_count": "1",
        "source_record_count": "100",
        "total_vouchers_paid": "1000.00",
        "total_vouchers_pending": "200.00",
        "total_encumbrance_balance": "50.00",
    }
]

redshift_results = [
    {
        "group_type": "fiscal_year",
        "group_value": "2024",
        "group_row_count": "1",
        "source_record_count": "100",
        "total_vouchers_paid": "1000.02",
        "total_vouchers_pending": "200.00",
        "total_encumbrance_balance": "50.00",
    }
]

compare_grouped_batch_metrics(
    athena_results=athena_results,
    redshift_results=redshift_results,
)