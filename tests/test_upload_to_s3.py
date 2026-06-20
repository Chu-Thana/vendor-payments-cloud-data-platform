from pathlib import Path

from scripts.batch import upload_to_s3


def create_gold_sample_files(
    gold_sample_dir: Path,
) -> None:
    gold_sample_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    gold_files = [
        "mart_spending_by_fiscal_year.csv",
        "mart_spending_by_department.csv",
        "mart_spending_by_supplier_top_n.csv",
        "mart_fund_category_summary.csv",
        "mart_pending_by_department.csv",
    ]

    for file_name in gold_files:
        (gold_sample_dir / file_name).write_text(
            "sample_header\nsample_value\n",
            encoding="utf-8",
        )


def test_build_upload_plan_contains_expected_zones(
    tmp_path: Path,
    monkeypatch,
) -> None:
    gold_sample_dir = tmp_path / "gold_sample"
    create_gold_sample_files(gold_sample_dir)

    monkeypatch.setattr(
        upload_to_s3,
        "GOLD_SAMPLE_DIR",
        gold_sample_dir,
    )

    upload_plan = upload_to_s3.build_upload_plan()

    s3_keys = [
        s3_key
        for _, s3_key in upload_plan
    ]

    assert any(
        "/raw/sample/" in key
        for key in s3_keys
    )
    assert any(
        "/silver/sample/" in key
        for key in s3_keys
    )
    assert any(
        "/gold/sample/" in key
        for key in s3_keys
    )


def test_build_upload_plan_contains_vendor_payments_files(
    tmp_path: Path,
    monkeypatch,
) -> None:
    gold_sample_dir = tmp_path / "gold_sample"
    create_gold_sample_files(gold_sample_dir)

    monkeypatch.setattr(
        upload_to_s3,
        "GOLD_SAMPLE_DIR",
        gold_sample_dir,
    )

    upload_plan = upload_to_s3.build_upload_plan()

    local_files = [
        local_path.name
        for local_path, _ in upload_plan
    ]

    assert "vendor_payments_sample.csv" in local_files
    assert "vendor_payments_silver_sample.csv" in local_files
    assert "mart_spending_by_fiscal_year.csv" in local_files


def test_validate_upload_plan_raises_error_for_missing_file(tmp_path):
    missing_file = tmp_path / "missing.csv"
    upload_plan = [(missing_file, "data-platform/vendor-payments/raw/sample/missing.csv")]

    try:
        upload_to_s3.validate_upload_plan(upload_plan)
    except FileNotFoundError as error:
        assert "Missing required files" in str(error)
        assert "missing.csv" in str(error)
    else:
        raise AssertionError("Expected FileNotFoundError for missing file")


def test_validate_upload_plan_passes_for_existing_file(tmp_path):
    existing_file = tmp_path / "existing.csv"
    existing_file.write_text("id,amount\n1,100\n", encoding="utf-8")

    upload_plan = [(existing_file, "data-platform/vendor-payments/raw/sample/existing.csv")]

    upload_to_s3.validate_upload_plan(upload_plan)


def test_all_s3_keys_start_with_vendor_payments_prefix():
    upload_plan = upload_to_s3.build_upload_plan()

    for _, s3_key in upload_plan:
        assert s3_key.startswith("data-platform/vendor-payments/")
        assert isinstance(s3_key, str)
        assert s3_key