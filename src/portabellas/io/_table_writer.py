from __future__ import annotations

from typing import TYPE_CHECKING

from portabellas._validation import normalize_and_check_file_path

if TYPE_CHECKING:
    from pathlib import Path

    from portabellas import Table


class TableWriter:
    """
    Write a table to various targets.

    This class cannot be instantiated directly. Access it via `table.write` instead.

    Examples
    --------
    >>> from portabellas import Table
    >>> import tempfile
    >>> from pathlib import Path
    >>> table = Table({"a": [1, 2], "b": [3, 4]})
    >>> with tempfile.TemporaryDirectory() as tmp:
    ...     table.write.csv_file(Path(tmp) / "test.csv")
    ...     restored = Table.read.csv_file(Path(tmp) / "test.csv")
    ...     restored == table
    True
    """

    def __init__(self, table: Table) -> None:
        self._table = table

    def csv_file(self, path: str | Path) -> None:
        """
        Write the table to a CSV file.

        If the file and/or the parent directories do not exist, they will be created. If the file exists already, it
        will be overwritten.

        Parameters
        ----------
        path:
            The path to the CSV file. If the file extension is omitted, it is assumed to be ".csv".

        Raises
        ------
        FileExtensionError
            If the path has an extension that is not ".csv".

        Examples
        --------
        >>> from portabellas import Table
        >>> import tempfile
        >>> from pathlib import Path
        >>> table = Table({"a": [1, 2], "b": [3, 4]})
        >>> with tempfile.TemporaryDirectory() as tmp:
        ...     table.write.csv_file(Path(tmp) / "test.csv")
        ...     restored = Table.read.csv_file(Path(tmp) / "test.csv")
        ...     restored == table
        True
        """
        path = normalize_and_check_file_path(path, ".csv", [".csv"])
        path.parent.mkdir(parents=True, exist_ok=True)

        self._table._lazy_frame.sink_csv(path)

    def json_file(self, path: str | Path) -> None:
        """
        Write the table to a JSON file.

        If the file and/or the parent directories do not exist, they will be created. If the file exists already, it
        will be overwritten.

        **Note:** This operation must fully load the data into memory, which can be expensive.

        Parameters
        ----------
        path:
            The path to the JSON file. If the file extension is omitted, it is assumed to be ".json".

        Raises
        ------
        FileExtensionError
            If the path has an extension that is not ".json".

        Examples
        --------
        >>> from portabellas import Table
        >>> import tempfile
        >>> from pathlib import Path
        >>> table = Table({"a": [1, 2], "b": [3, 4]})
        >>> with tempfile.TemporaryDirectory() as tmp:
        ...     table.write.json_file(Path(tmp) / "test.json")
        ...     restored = Table.read.json_file(Path(tmp) / "test.json")
        ...     restored == table
        True
        """
        path = normalize_and_check_file_path(path, ".json", [".json"])
        path.parent.mkdir(parents=True, exist_ok=True)

        self._table._data_frame.write_json(path)

    def jsonl_file(self, path: str | Path) -> None:
        """
        Write the table to a JSONL (JSON Lines) file.

        Each line in the file will be a valid JSON object. This format is also known as NDJSON (Newline-Delimited
        JSON).

        If the file and/or the parent directories do not exist, they will be created. If the file exists already, it
        will be overwritten.

        Parameters
        ----------
        path:
            The path to the JSONL file. If the file extension is omitted, it is assumed to be ".jsonl".

        Raises
        ------
        FileExtensionError
            If the path has an extension that is not ".jsonl" or ".ndjson".

        Examples
        --------
        >>> from portabellas import Table
        >>> import tempfile
        >>> from pathlib import Path
        >>> table = Table({"a": [1, 2], "b": [3, 4]})
        >>> with tempfile.TemporaryDirectory() as tmp:
        ...     table.write.jsonl_file(Path(tmp) / "test.jsonl")
        ...     restored = Table.read.jsonl_file(Path(tmp) / "test.jsonl")
        ...     restored == table
        True
        """
        path = normalize_and_check_file_path(path, ".jsonl", [".jsonl", ".ndjson"])
        path.parent.mkdir(parents=True, exist_ok=True)

        self._table._lazy_frame.sink_ndjson(path)

    def parquet_file(self, path: str | Path) -> None:
        """
        Write the table to a Parquet file.

        If the file and/or the parent directories do not exist, they will be created. If the file exists already, it
        will be overwritten.

        Parameters
        ----------
        path:
            The path to the Parquet file. If the file extension is omitted, it is assumed to be ".parquet".

        Raises
        ------
        FileExtensionError
            If the path has an extension that is not ".parquet".

        Examples
        --------
        >>> from portabellas import Table
        >>> import tempfile
        >>> from pathlib import Path
        >>> table = Table({"a": [1, 2], "b": [3, 4]})
        >>> with tempfile.TemporaryDirectory() as tmp:
        ...     table.write.parquet_file(Path(tmp) / "test.parquet")
        ...     restored = Table.read.parquet_file(Path(tmp) / "test.parquet")
        ...     restored == table
        True
        """
        path = normalize_and_check_file_path(path, ".parquet", [".parquet"])
        path.parent.mkdir(parents=True, exist_ok=True)

        self._table._lazy_frame.sink_parquet(path)
