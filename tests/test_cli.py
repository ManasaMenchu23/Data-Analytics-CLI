from pathlib import Path

from typer.testing import CliRunner

from app import app

runner = CliRunner()


def _sample_csv() -> Path:
    return Path(__file__).resolve().parent / "data" / "sample.csv"


def test_info_command_prints_shape():
    csv_path = _sample_csv()
    result = runner.invoke(app, ["info", str(csv_path)])
    assert result.exit_code == 0
    assert "Rows:" in result.stdout


def test_nulls_command_runs():
    csv_path = _sample_csv()
    result = runner.invoke(app, ["nulls", str(csv_path)])
    assert result.exit_code == 0


def test_sort_unknown_column_exits_with_error():
    csv_path = _sample_csv()
    result = runner.invoke(app, ["sort", str(csv_path), "unknown_column"])
    assert result.exit_code !=0 