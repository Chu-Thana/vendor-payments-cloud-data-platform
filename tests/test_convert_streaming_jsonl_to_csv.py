import csv
import json

import pytest

from scripts.streaming.convert_streaming_jsonl_to_csv import (
    convert_jsonl_to_csv,
    flatten_record,
    infer_fieldnames,
    read_jsonl_records,
)


def test_flatten_record_flattens_nested_dictionary():
    record = {
        "event_id": "evt_001",
        "payment": {
            "fiscal_year": 2026,
            "amount": 1000.5,
        },
    }

    flattened = flatten_record(record)

    assert flattened["event_id"] == "evt_001"
    assert flattened["payment_fiscal_year"] == 2026
    assert flattened["payment_amount"] == 1000.5


def test_infer_fieldnames_returns_sorted_columns():
    records = [
        {"event_id": "evt_001", "amount": 100},
        {"event_id": "evt_002", "supplier_name": "ABC"},
    ]

    fieldnames = infer_fieldnames(records)

    assert fieldnames == ["amount", "event_id", "supplier_name"]


def test_read_jsonl_records_reads_and_flattens_records(tmp_path):
    input_file = tmp_path / "events.jsonl"
    records = [
        {
            "event_id": "evt_001",
            "payment": {
                "amount": 100,
            },
        },
        {
            "event_id": "evt_002",
            "payment": {
                "amount": 200,
            },
        },
    ]

    input_file.write_text(
        "\n".join(json.dumps(record) for record in records),
        encoding="utf-8",
    )

    parsed_records = read_jsonl_records(input_file)

    assert len(parsed_records) == 2
    assert parsed_records[0]["event_id"] == "evt_001"
    assert parsed_records[0]["payment_amount"] == 100


def test_read_jsonl_records_raises_error_for_invalid_json(tmp_path):
    input_file = tmp_path / "invalid.jsonl"
    input_file.write_text('{"event_id": "evt_001"}\n{invalid-json}', encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON"):
        read_jsonl_records(input_file)


def test_convert_jsonl_to_csv_creates_curated_csv(tmp_path):
    input_file = tmp_path / "events.jsonl"
    output_file = tmp_path / "vendor_payments_streaming_events.csv"

    records = [
        {
            "event_id": "evt_001",
            "payment": {
                "fiscal_year": 2026,
                "amount": 1000.5,
            },
        },
        {
            "event_id": "evt_002",
            "payment": {
                "fiscal_year": 2026,
                "amount": 2500.75,
            },
        },
    ]

    input_file.write_text(
        "\n".join(json.dumps(record) for record in records),
        encoding="utf-8",
    )

    created_file = convert_jsonl_to_csv(input_file, output_file)

    assert created_file.exists()

    with created_file.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    assert len(rows) == 2
    assert rows[0]["event_id"] == "evt_001"
    assert rows[0]["payment_fiscal_year"] == "2026"
    assert rows[0]["payment_amount"] == "1000.5"