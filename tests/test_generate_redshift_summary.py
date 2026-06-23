from __future__ import annotations

from decimal import Decimal

import pytest

from scripts.warehouse.generate_redshift_summary import (
    normalize_for_json,
    validate_batch_metrics,
    validate_streaming_metrics,
    validate_summary_metadata,
)


def test_validate_batch_metrics_passes() -> None:
    landing_counts = [
        {"table_name": "table_1", "row_count": 20},
        {"table_name": "table_2", "row_count": 1121},
        {"table_name": "table_3", "row_count": 100},
        {"table_name": "table_4", "row_count": 1061},
        {"table_name": "table_5", "row_count": 642},
    ]

    result = validate_batch_metrics(
        landing_counts=landing_counts,
        analytics_view_count=5,
    )

    assert result == "PASS"


def test_validate_batch_metrics_fails_when_table_is_empty() -> None:
    landing_counts = [
        {"table_name": "table_1", "row_count": 20},
        {"table_name": "table_2", "row_count": 1121},
        {"table_name": "table_3", "row_count": 0},
        {"table_name": "table_4", "row_count": 1061},
        {"table_name": "table_5", "row_count": 642},
    ]

    result = validate_batch_metrics(
        landing_counts=landing_counts,
        analytics_view_count=5,
    )

    assert result == "FAIL"


def test_validate_streaming_metrics_passes() -> None:
    landing_metrics = {
        "total_rows": 100000,
        "rows_with_event_id": 100000,
        "distinct_event_ids": 100000,
        "duplicate_event_ids": 0,
        "missing_event_ids": 0,
    }

    analytics_metrics = {
        "total_events": 100000,
        "total_distinct_events": 100000,
    }

    result = validate_streaming_metrics(
        landing_metrics=landing_metrics,
        analytics_metrics=analytics_metrics,
        analytics_view_count=4,
    )

    assert result == "PASS"


def test_validate_streaming_metrics_fails_when_duplicates_exist() -> None:
    landing_metrics = {
        "total_rows": 100000,
        "rows_with_event_id": 100000,
        "distinct_event_ids": 99999,
        "duplicate_event_ids": 1,
        "missing_event_ids": 0,
    }

    analytics_metrics = {
        "total_events": 100000,
        "total_distinct_events": 99999,
    }

    result = validate_streaming_metrics(
        landing_metrics=landing_metrics,
        analytics_metrics=analytics_metrics,
        analytics_view_count=4,
    )

    assert result == "FAIL"


def test_normalize_for_json_converts_decimal() -> None:
    value = {
        "total_payment_amount": Decimal("150580975432.60"),
    }

    result = normalize_for_json(value)

    assert result == {
        "total_payment_amount": 150580975432.60,
    }


def build_valid_summary() -> dict[str, object]:
    return {
        "project": "Vendor Payments Cloud Data Platform",
        "component": "Amazon Redshift Serverless",
        "pipeline_version": "1.0.0",
        "generated_at": "2026-06-22T17:11:10+00:00",
        "execution": {
            "started_at": "2026-06-22T17:07:45+00:00",
            "completed_at": "2026-06-22T17:11:10+00:00",
            "runtime_seconds": 188.58,
            "status": "PASS",
        },
        "redshift": {
            "region": "ap-southeast-1",
            "workgroup": "default-workgroup",
            "database": "dev",
            "architecture": {
                "landing_schema": "landing",
                "analytics_schema": "analytics",
            },
        },
        "batch": {
            "landing_table_count": 5,
            "analytics_view_count": 5,
            "validation_status": "PASS",
        },
        "streaming": {
            "landing_table_count": 1,
            "analytics_view_count": 4,
            "validation_status": "PASS",
        },
        "validation": {
            "status": "PASS",
        },
        "artifact": {
            "path": (
                "output/reports/"
                "redshift_execution_summary.json"
            ),
            "format": "json",
        },
    }


def test_validate_summary_metadata_passes() -> None:
    summary = build_valid_summary()

    validate_summary_metadata(summary)


def test_validate_summary_metadata_fails_when_section_missing() -> None:
    summary = build_valid_summary()
    summary.pop("artifact")

    with pytest.raises(
        ValueError,
        match="missing required sections: artifact",
    ):
        validate_summary_metadata(summary)


def test_validate_summary_metadata_fails_for_execution_status() -> None:
    summary = build_valid_summary()
    execution = summary["execution"]

    assert isinstance(execution, dict)
    execution["status"] = "UNKNOWN"

    with pytest.raises(
        ValueError,
        match="invalid execution status",
    ):
        validate_summary_metadata(summary)


def test_validate_summary_metadata_fails_for_validation_status() -> None:
    summary = build_valid_summary()
    validation = summary["validation"]

    assert isinstance(validation, dict)
    validation["status"] = "UNKNOWN"

    with pytest.raises(
        ValueError,
        match="invalid validation status",
    ):
        validate_summary_metadata(summary)
