from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

import boto3


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_FILE = (
    PROJECT_ROOT
    / "output"
    / "reports"
    / "redshift_execution_summary.json"
)

AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-1")
REDSHIFT_WORKGROUP = os.getenv(
    "REDSHIFT_WORKGROUP",
    "default-workgroup",
)
REDSHIFT_DATABASE = os.getenv(
    "REDSHIFT_DATABASE",
    "dev",
)

POLL_INTERVAL_SECONDS = 1
STATEMENT_TIMEOUT_SECONDS = 300


def wait_for_statement(
    client: Any,
    statement_id: str,
) -> dict[str, Any]:
    """Wait until a Redshift Data API statement finishes."""

    started_at = time.monotonic()

    while True:
        response = client.describe_statement(Id=statement_id)
        status = response["Status"]

        if status == "FINISHED":
            return response

        if status in {"FAILED", "ABORTED"}:
            error_message = response.get(
                "Error",
                "Unknown Redshift statement error",
            )
            raise RuntimeError(
                f"Redshift statement {status.lower()}: "
                f"{error_message}"
            )

        elapsed_seconds = time.monotonic() - started_at

        if elapsed_seconds > STATEMENT_TIMEOUT_SECONDS:
            raise TimeoutError(
                "Redshift statement exceeded "
                f"{STATEMENT_TIMEOUT_SECONDS} seconds."
            )

        time.sleep(POLL_INTERVAL_SECONDS)


def convert_value(field: dict[str, Any]) -> Any:
    """Convert a Redshift Data API field into a Python value."""

    if field.get("isNull"):
        return None

    for key in (
        "stringValue",
        "longValue",
        "doubleValue",
        "booleanValue",
        "blobValue",
    ):
        if key in field:
            return field[key]

    return None


def execute_query(
    client: Any,
    sql: str,
) -> list[dict[str, Any]]:
    """Execute SQL and return rows as dictionaries."""

    response = client.execute_statement(
        WorkgroupName=REDSHIFT_WORKGROUP,
        Database=REDSHIFT_DATABASE,
        Sql=sql,
    )

    statement_id = response["Id"]
    statement = wait_for_statement(
        client=client,
        statement_id=statement_id,
    )

    if not statement.get("HasResultSet"):
        return []

    result = client.get_statement_result(
        Id=statement_id,
    )

    column_names = [
        column["name"]
        for column in result["ColumnMetadata"]
    ]

    rows: list[dict[str, Any]] = []

    for record in result["Records"]:
        row = {
            column_name: convert_value(field)
            for column_name, field in zip(
                column_names,
                record,
                strict=True,
            )
        }
        rows.append(row)

    return rows


def validate_batch_metrics(
    landing_counts: list[dict[str, Any]],
    analytics_view_count: int,
) -> str:
    total_landing_rows = sum(
        int(row["row_count"])
        for row in landing_counts
    )

    tables_are_non_empty = all(
        int(row["row_count"]) > 0
        for row in landing_counts
    )

    return (
        "PASS"
        if len(landing_counts) == 5
        and total_landing_rows > 0
        and tables_are_non_empty
        and analytics_view_count == 5
        else "FAIL"
    )


def validate_streaming_metrics(
    landing_metrics: dict[str, Any],
    analytics_metrics: dict[str, Any],
    analytics_view_count: int,
) -> str:
    total_rows = int(landing_metrics["total_rows"])
    rows_with_event_id = int(
        landing_metrics["rows_with_event_id"]
    )
    distinct_event_ids = int(
        landing_metrics["distinct_event_ids"]
    )
    duplicate_event_ids = int(
        landing_metrics["duplicate_event_ids"]
    )
    missing_event_ids = int(
        landing_metrics["missing_event_ids"]
    )

    analytics_total_events = int(
        analytics_metrics["total_events"]
    )
    analytics_distinct_events = int(
        analytics_metrics["total_distinct_events"]
    )

    return (
        "PASS"
        if total_rows > 0
        and rows_with_event_id == total_rows
        and distinct_event_ids == total_rows
        and duplicate_event_ids == 0
        and missing_event_ids == 0
        and analytics_total_events == total_rows
        and analytics_distinct_events == distinct_event_ids
        and analytics_view_count == 4
        else "FAIL"
    )


def build_batch_metrics(
    client: Any,
) -> dict[str, Any]:
    """Collect Batch landing and analytics metrics."""

    landing_counts = execute_query(
        client,
        """
        SELECT
            'fund_category_summary' AS table_name,
            COUNT(*) AS row_count
        FROM landing.fund_category_summary

        UNION ALL

        SELECT
            'pending_by_department',
            COUNT(*)
        FROM landing.pending_by_department

        UNION ALL

        SELECT
            'spending_by_department',
            COUNT(*)
        FROM landing.spending_by_department

        UNION ALL

        SELECT
            'spending_by_fiscal_year',
            COUNT(*)
        FROM landing.spending_by_fiscal_year

        UNION ALL

        SELECT
            'spending_by_supplier_top_n',
            COUNT(*)
        FROM landing.spending_by_supplier_top_n

        ORDER BY table_name;
        """,
    )

    analytics_view_count = execute_query(
        client,
        """
        SELECT COUNT(*) AS view_count
        FROM information_schema.views
        WHERE table_schema = 'analytics'
          AND table_name IN (
              'spending_by_fiscal_year',
              'department_spending_ranked',
              'supplier_spending_ranked',
              'fund_category_spending_ranked',
              'pending_by_department_ranked'
          );
        """,
    )[0]["view_count"]

    total_landing_rows = sum(
        int(row["row_count"])
        for row in landing_counts
    )

    validation_status = validate_batch_metrics(
        landing_counts=landing_counts,
        analytics_view_count=analytics_view_count,
    )

    return {
        "landing_table_count": len(landing_counts),
        "landing_total_rows": total_landing_rows,
        "landing_tables": landing_counts,
        "analytics_view_count": analytics_view_count,
        "validation_status": validation_status,
    }


def build_streaming_metrics(
    client: Any,
) -> dict[str, Any]:
    """Collect Streaming landing and analytics metrics."""

    landing_metrics = execute_query(
        client,
        """
        SELECT
            COUNT(*) AS total_rows,
            COUNT(event_id) AS rows_with_event_id,
            COUNT(DISTINCT event_id) AS distinct_event_ids,
            COUNT(*) - COUNT(DISTINCT event_id)
                AS duplicate_event_ids,
            SUM(
                CASE
                    WHEN event_id IS NULL
                      OR TRIM(event_id) = ''
                    THEN 1
                    ELSE 0
                END
            ) AS missing_event_ids
        FROM landing.vendor_payments_streaming_events;
        """,
    )[0]

    analytics_metrics = execute_query(
        client,
        """
        SELECT
            COUNT(*) AS fiscal_year_rows,
            SUM(event_count) AS total_events,
            SUM(distinct_event_count)
                AS total_distinct_events,
            SUM(total_payment_amount)
                AS total_payment_amount
        FROM analytics.streaming_events_by_fiscal_year;
        """,
    )[0]

    analytics_view_count = execute_query(
        client,
        """
        SELECT COUNT(*) AS view_count
        FROM information_schema.views
        WHERE table_schema = 'analytics'
          AND table_name IN (
              'vendor_payments_streaming_events',
              'streaming_events_by_fiscal_year',
              'streaming_events_by_department',
              'streaming_events_by_supplier'
          );
        """,
    )[0]["view_count"]

    validation_status = validate_streaming_metrics(
        landing_metrics=landing_metrics,
        analytics_metrics=analytics_metrics,
        analytics_view_count=analytics_view_count,
    )

    return {
        "landing_table_count": 1,
        "landing_metrics": landing_metrics,
        "analytics_view_count": analytics_view_count,
        "analytics_metrics": analytics_metrics,
        "validation_status": validation_status,
    }


def normalize_for_json(value: Any) -> Any:
    """Convert values into JSON-compatible types."""

    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, dict):
        return {
            key: normalize_for_json(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            normalize_for_json(item)
            for item in value
        ]

    return value


def main() -> None:
    started_at = datetime.now(timezone.utc)
    started_monotonic = time.monotonic()

    client = boto3.client(
        "redshift-data",
        region_name=AWS_REGION,
    )

    batch_metrics = build_batch_metrics(client)
    streaming_metrics = build_streaming_metrics(client)

    completed_at = datetime.now(timezone.utc)
    runtime_seconds = round(
        time.monotonic() - started_monotonic,
        2,
    )

    overall_status = (
        "PASS"
        if batch_metrics["validation_status"] == "PASS"
        and streaming_metrics["validation_status"] == "PASS"
        else "FAIL"
    )

    summary = {
        "project": "Vendor Payments Cloud Data Platform",
        "component": "Amazon Redshift Serverless",
        "pipeline_version": "1.0.0",
        "generated_at": completed_at.isoformat(),
        "execution": {
            "started_at": started_at.isoformat(),
            "completed_at": completed_at.isoformat(),
            "runtime_seconds": runtime_seconds,
            "status": overall_status,
        },
        "redshift": {
            "region": AWS_REGION,
            "workgroup": REDSHIFT_WORKGROUP,
            "database": REDSHIFT_DATABASE,
            "architecture": {
                "landing_schema": "landing",
                "analytics_schema": "analytics",
            },
        },
        "batch": batch_metrics,
        "streaming": streaming_metrics,
        "validation": {
            "status": overall_status,
        },
    }

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            normalize_for_json(summary),
            file,
            indent=2,
        )

    print(
        "Redshift execution summary generated successfully."
    )
    print(f"Output: {OUTPUT_FILE}")
    print(f"Status: {overall_status}")
    print(f"Runtime: {runtime_seconds} seconds")


if __name__ == "__main__":
    main()