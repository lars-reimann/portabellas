from pathlib import Path

import pytest

from portabellas import Table
from portabellas.exceptions import FileExtensionError
from tests.helpers import resolve_resource_path


@pytest.mark.parametrize(
    ("resource_path", "expected"),
    [
        pytest.param("csv/empty.csv", Table({}), id="empty"),
        pytest.param("csv/non-empty.csv", Table({"A": [1], "B": [2]}), id="non-empty"),
        pytest.param("csv/special-character.csv", Table({"A": ["❔"], "B": [2]}), id="special character"),
        pytest.param("csv/empty", Table({}), id="missing extension"),
    ],
)
class TestShouldCreateTableFromCsvFile:
    def test_path_as_string(self, resource_path: str, expected: Table) -> None:
        path = resolve_resource_path(resource_path)

        actual = Table.read.csv_file(path)

        assert actual == expected

    def test_path_as_path_object(self, resource_path: str, expected: Table) -> None:
        path = Path(resolve_resource_path(resource_path))

        actual = Table.read.csv_file(path)

        assert actual == expected


def test_should_read_csv_with_custom_separator() -> None:
    path = resolve_resource_path("csv/non-empty.csv")

    actual = Table.read.csv_file(path, separator=",")

    assert actual == Table({"A": [1], "B": [2]})


def test_should_raise_if_wrong_extension() -> None:
    path = resolve_resource_path("csv/non-empty.csv").replace(".csv", ".txt")

    with pytest.raises(FileExtensionError):
        Table.read.csv_file(path)


def test_should_raise_if_file_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        Table.read.csv_file(resolve_resource_path("csv/not-found.csv"))
