from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


def test_required_project_directories_exist():
    required_dirs = [
        ROOT_DIR / "airflow",
        ROOT_DIR / "api",
        ROOT_DIR / "assets",
        ROOT_DIR / "configs",
        ROOT_DIR / "data" / "sample",
        ROOT_DIR / "dbt",
        ROOT_DIR / "scripts" / "batch",
        ROOT_DIR / "scripts" / "warehouse",
    ]

    for dir_path in required_dirs:
        assert dir_path.exists(), f"Missing required directory: {dir_path}"


def test_required_project_files_exist():
    required_files = [
        ROOT_DIR / "README.md",
        ROOT_DIR / "requirements.txt",
        ROOT_DIR / ".env.example",
        ROOT_DIR / "data" / "sample" / "superstore_cleaned.csv",
        ROOT_DIR / "data" / "sample" / "superstore_cleaned.parquet",
        ROOT_DIR / "scripts" / "batch" / "convert_to_parquet.py",
        ROOT_DIR / "scripts" / "batch" / "upload_csv_to_s3.py",
        ROOT_DIR / "scripts" / "batch" / "upload_to_s3.py",
    ]

    for file_path in required_files:
        assert file_path.exists(), f"Missing required file: {file_path}"


def test_architecture_assets_exist():
    required_assets = [
        ROOT_DIR / "assets" / "00_cloud-data-platform-architecture.png",
        ROOT_DIR / "assets" / "01_s3_data_lake_structure.png",
        ROOT_DIR / "assets" / "02_athena_query_performance.png",
        ROOT_DIR / "assets" / "03_redshift_query_performance.png",
    ]

    for asset_path in required_assets:
        assert asset_path.exists(), f"Missing required asset: {asset_path}"