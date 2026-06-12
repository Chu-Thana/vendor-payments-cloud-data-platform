import pytest

from scripts.streaming import upload_streaming_to_s3


def test_streaming_build_upload_plan_contains_expected_zones():
    upload_plan = upload_streaming_to_s3.build_upload_plan()

    s3_keys = [s3_key for _, s3_key in upload_plan]

    assert any("/streaming/staging/" in key for key in s3_keys)
    assert any("/streaming/curated/" in key for key in s3_keys)
    assert any("/streaming/reports/" in key for key in s3_keys)


def test_streaming_build_upload_plan_contains_expected_files():
    upload_plan = upload_streaming_to_s3.build_upload_plan()

    local_files = [local_path.name for local_path, _ in upload_plan]

    assert "vendor_payments_streaming_staging.jsonl" in local_files
    assert "vendor_payments_streaming_events.csv" in local_files
    assert "streaming_summary_report.json" in local_files
    assert "airflow_orchestration_summary.json" in local_files


def test_streaming_upload_plan_uses_vendor_payments_prefix():
    upload_plan = upload_streaming_to_s3.build_upload_plan()

    s3_keys = [s3_key for _, s3_key in upload_plan]

    assert all("data-platform/vendor-payments" in key for key in s3_keys)


def test_validate_streaming_upload_plan_raises_error_for_missing_file(tmp_path):
    missing_file = tmp_path / "missing_streaming_output.jsonl"
    upload_plan = [
        (
            missing_file,
            "data-platform/vendor-payments/streaming/staging/missing_streaming_output.jsonl",
        )
    ]

    with pytest.raises(FileNotFoundError):
        upload_streaming_to_s3.validate_upload_plan(upload_plan)


def test_validate_streaming_upload_plan_passes_for_existing_file(tmp_path):
    existing_file = tmp_path / "streaming_summary_report.json"
    existing_file.write_text("{}", encoding="utf-8")

    upload_plan = [
        (
            existing_file,
            "data-platform/vendor-payments/streaming/reports/streaming_summary_report.json",
        )
    ]

    upload_streaming_to_s3.validate_upload_plan(upload_plan)