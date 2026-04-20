from pathlib import Path

import pytest

from portabellas import Table
from portabellas.exceptions import FileExtensionError
from tests.helpers import resolve_resource_path


@pytest.mark.parametrize(
    ("resource_path", "expected"),
    [
        pytest.param("parquet/empty.parquet", Table({}), id="empty"),
        pytest.param("parquet/non-empty.parquet", Table({"A": [1], "B": [2]}), id="non-empty"),
        pytest.param("parquet/special-character.parquet", Table({"A": ["❔"], "B": [2]}), id="special character"),
        pytest.param("parquet/empty", Table({}), id="missing extension"),
    ],
)
class TestShouldCreateTableFromParquetFile:
    def test_path_as_string(self, resource_path: str, expected: Table) -> None:
        path = resolve_resource_path(resource_path)

        actual = Table.read.parquet_file(path)

        assert actual == expected

    def test_path_as_path_object(self, resource_path: str, expected: Table) -> None:
        path = Path(resolve_resource_path(resource_path))

        actual = Table.read.parquet_file(path)

        assert actual == expected


def test_should_raise_if_wrong_extension() -> None:
    path = resolve_resource_path("parquet/non-empty.parquet").replace(".parquet", ".txt")

    with pytest.raises(FileExtensionError):
        Table.read.parquet_file(path)


def test_should_raise_if_file_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        Table.read.parquet_file(resolve_resource_path("parquet/not-found.parquet"))
