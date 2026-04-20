from pathlib import Path

import pytest

from portabellas._validation import normalize_and_check_file_path
from portabellas.exceptions import FileExtensionError


def test_should_add_canonical_extension_if_missing() -> None:
    result = normalize_and_check_file_path("data", ".csv", [".csv"])
    assert result == Path("data.csv")


def test_should_pass_if_extension_is_valid() -> None:
    result = normalize_and_check_file_path("data.csv", ".csv", [".csv"])
    assert result == Path("data.csv")


def test_should_raise_if_extension_is_invalid() -> None:
    with pytest.raises(FileExtensionError, match="Expected path with extension"):
        normalize_and_check_file_path("data.txt", ".csv", [".csv"])


def test_should_accept_path_object() -> None:
    result = normalize_and_check_file_path(Path("data"), ".json", [".json"])
    assert result == Path("data.json")


def test_should_raise_file_not_found_if_check_enabled(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="File not found"):
        normalize_and_check_file_path(
            tmp_path / "missing.csv",
            ".csv",
            [".csv"],
            check_if_file_exists=True,
        )


def test_should_not_raise_file_not_found_if_file_exists(tmp_path: Path) -> None:
    path = tmp_path / "exists.csv"
    path.write_text("test")

    result = normalize_and_check_file_path(path, ".csv", [".csv"], check_if_file_exists=True)
    assert result == path


def test_should_not_check_file_existence_by_default(tmp_path: Path) -> None:
    result = normalize_and_check_file_path(tmp_path / "missing.csv", ".csv", [".csv"])
    assert result == tmp_path / "missing.csv"


def test_should_support_multiple_valid_extensions() -> None:
    result = normalize_and_check_file_path("data.csv", ".csv", [".csv", ".tsv"])
    assert result == Path("data.csv")
