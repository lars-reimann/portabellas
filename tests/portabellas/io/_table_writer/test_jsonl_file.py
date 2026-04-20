from pathlib import Path

import pytest

from portabellas import Table
from portabellas.exceptions import FileExtensionError


@pytest.mark.parametrize(
    "table",
    [
        pytest.param(Table({}), id="empty"),
        pytest.param(Table({"col1": [0, 1], "col2": ["a", "b"]}), id="with data"),
    ],
)
class TestShouldCreateJsonlFile:
    def test_path_as_string(self, table: Table, tmp_path: Path) -> None:
        path_as_string = str(tmp_path / "table.jsonl")

        table.write.jsonl_file(path_as_string)
        restored = Table.read.jsonl_file(path_as_string)
        assert restored == table

    def test_path_as_path_object(self, table: Table, tmp_path: Path) -> None:
        path_as_path_object = tmp_path / "table.jsonl"

        table.write.jsonl_file(path_as_path_object)
        restored = Table.read.jsonl_file(path_as_path_object)
        assert restored == table


def test_should_add_missing_extension(tmp_path: Path) -> None:
    write_path = tmp_path / "table"
    read_path = tmp_path / "table.jsonl"

    table = Table({})
    table.write.jsonl_file(write_path)
    restored = Table.read.jsonl_file(read_path)
    assert restored == table


def test_should_accept_ndjson_extension(tmp_path: Path) -> None:
    path = tmp_path / "table.ndjson"

    table = Table({"a": [1]})
    table.write.jsonl_file(path)
    restored = Table.read.jsonl_file(path)
    assert restored == table


def test_should_raise_if_wrong_file_extension(tmp_path: Path) -> None:
    with pytest.raises(FileExtensionError):
        Table({}).write.jsonl_file(tmp_path / "table.txt")


def test_should_create_parent_directories(tmp_path: Path) -> None:
    path = tmp_path / "subdir" / "table.jsonl"

    Table({"a": [1]}).write.jsonl_file(path)
    assert path.is_file()
