from pathlib import Path

import pytest

from portabellas import Table
from portabellas.exceptions import FileExtensionError
from tests.helpers import resolve_resource_path


@pytest.mark.parametrize(
    ("resource_path", "expected"),
    [
        pytest.param("jsonl/empty.jsonl", Table({}), id="empty"),
        pytest.param("jsonl/non-empty.jsonl", Table({"A": [1], "B": [2]}), id="non-empty"),
        pytest.param("jsonl/special-character.jsonl", Table({"A": ["❔"], "B": [2]}), id="special character"),
        pytest.param("jsonl/empty", Table({}), id="missing extension"),
        pytest.param("jsonl/non-empty.ndjson", Table({"A": [1], "B": [2]}), id="ndjson extension"),
    ],
)
class TestShouldCreateTableFromJsonlFile:
    def test_path_as_string(self, resource_path: str, expected: Table) -> None:
        path = resolve_resource_path(resource_path)

        actual = Table.read.jsonl_file(path)

        assert actual == expected

    def test_path_as_path_object(self, resource_path: str, expected: Table) -> None:
        path = Path(resolve_resource_path(resource_path))

        actual = Table.read.jsonl_file(path)

        assert actual == expected


def test_should_raise_if_wrong_extension() -> None:
    path = resolve_resource_path("jsonl/non-empty.jsonl").replace(".jsonl", ".txt")

    with pytest.raises(FileExtensionError):
        Table.read.jsonl_file(path)


def test_should_raise_if_file_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        Table.read.jsonl_file(resolve_resource_path("jsonl/not-found.jsonl"))
