from pathlib import Path

import pytest

from portabellas import Table
from portabellas.exceptions import FileExtensionError
from tests.helpers import resolve_resource_path


@pytest.mark.parametrize(
    ("resource_path", "expected"),
    [
        pytest.param("json/empty.json", Table({}), id="empty"),
        pytest.param("json/non-empty.json", Table({"A": [1], "B": [2]}), id="non-empty"),
        pytest.param("json/special-character.json", Table({"A": ["❔"], "B": [2]}), id="special character"),
        pytest.param("json/empty", Table({}), id="missing extension"),
    ],
)
class TestShouldCreateTableFromJsonFile:
    def test_path_as_string(self, resource_path: str, expected: Table) -> None:
        path = resolve_resource_path(resource_path)

        actual = Table.read.json_file(path)

        assert actual == expected

    def test_path_as_path_object(self, resource_path: str, expected: Table) -> None:
        path = Path(resolve_resource_path(resource_path))

        actual = Table.read.json_file(path)

        assert actual == expected


def test_should_raise_if_wrong_extension() -> None:
    path = resolve_resource_path("json/non-empty.json").replace(".json", ".txt")

    with pytest.raises(FileExtensionError):
        Table.read.json_file(path)


def test_should_raise_if_file_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        Table.read.json_file(resolve_resource_path("json/not-found.json"))
