from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import boto3

from scripts.athena.run_athena_query import (
    execute_query_file,
    get_query_results,
)
from scripts.validation.compare_grouped_batch_metrics import (
    compare_grouped_batch_metrics,
)
from scripts.warehouse.run_redshift_sql import (
    execute_sql_file,
    get_statement_results,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

AWS_REGION = os.getenv(
    "AWS_REGION",
    "ap-southeast-1",
)

ATHENA_VALIDATE_BATCH_GROUPED_SQL = (
    PROJECT_ROOT
    / "sql"
    / "athena"
    / "14_validate_batch_grouped.sql"
)

REDSHIFT_VALIDATE_BATCH_GROUPED_SQL = (
    PROJECT_ROOT
    / "sql"
    / "redshift"
    / "12_validate_batch_grouped_metrics.sql"
)


def normalize_grouped_results(
    results: list[dict[str, str | None]],
    source_name: str,
) -> list[dict[str, str]]:
    if not results:
        raise ValueError(
            f"{source_name} grouped validation returned no rows."
        )

    required_columns = {
        "group_type",
        "group_value",
        "group_row_count",
        "source_record_count",
        "total_vouchers_paid",
        "total_vouchers_pending",
        "total_encumbrance_balance",
    }

    normalized_results: list[dict[str, str]] = []

    for result in results:
        missing_columns = (
            required_columns - result.keys()
        )

        if missing_columns:
            raise ValueError(
                f"{source_name} grouped validation "
                f"is missing columns: "
                f"{sorted(missing_columns)}"
            )

        normalized_row: dict[str, str] = {}

        for column in required_columns:
            value = result[column]

            if value is None:
                raise ValueError(
                    f"{source_name} grouped validation "
                    f"returned NULL for {column}."
                )

            normalized_row[column] = value

        normalized_results.append(
            normalized_row
        )

    return normalized_results


def run_validation() -> None:
    athena_client: Any = boto3.client(
        "athena",
        region_name=AWS_REGION,
    )

    redshift_client: Any = boto3.client(
        "redshift-data",
        region_name=AWS_REGION,
    )

    print(
        "Reading Batch Athena grouped metrics..."
    )

    athena_query_id = execute_query_file(
        client=athena_client,
        sql_file=ATHENA_VALIDATE_BATCH_GROUPED_SQL,
    )

    athena_metrics = normalize_grouped_results(
        get_query_results(
            client=athena_client,
            query_execution_id=athena_query_id,
        ),
        source_name="Athena",
    )

    print(
        "Reading Batch Redshift grouped metrics..."
    )

    redshift_statement_id = execute_sql_file(
        client=redshift_client,
        sql_file=REDSHIFT_VALIDATE_BATCH_GROUPED_SQL,
    )

    redshift_metrics = normalize_grouped_results(
        get_statement_results(
            client=redshift_client,
            statement_id=redshift_statement_id,
        ),
        source_name="Redshift",
    )

    print(
        f"Athena grouped row count: "
        f"{len(athena_metrics)}"
    )

    print(
        f"Redshift grouped row count: "
        f"{len(redshift_metrics)}"
    )

    compare_grouped_batch_metrics(
        athena_results=athena_metrics,
        redshift_results=redshift_metrics,
    )


def main() -> None:
    if not os.getenv("ATHENA_OUTPUT_LOCATION"):
        raise ValueError(
            "ATHENA_OUTPUT_LOCATION is not set."
        )

    run_validation()


if __name__ == "__main__":
    main()