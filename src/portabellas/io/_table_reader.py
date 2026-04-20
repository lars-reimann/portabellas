from __future__ import annotations

from typing import TYPE_CHECKING

import polars as pl
import polars.exceptions as pl_exceptions

from portabellas._validation import normalize_and_check_file_path

if TYPE_CHECKING:
    from pathlib import Path

    from portabellas import Table


class TableReader:
    """
    Read a table from various sources.

    This class cannot be instantiated directly. Access it via `Table.read` instead.

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

    @staticmethod
    def csv_file(path: str | Path, *, separator: str = ",") -> Table:
        """
        Read a table from a CSV file.

        Parameters
        ----------
        path:
            The path to the CSV file. If the file extension is omitted, it is assumed to be ".csv".
        separator:
            The separator between values in the CSV file.

        Returns
        -------
        table:
            The table read from the file.

        Raises
        ------
        FileExtensionError
            If the path has an extension that is not ".csv".
        FileNotFoundError
            If no file exists at the given path.

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
        from portabellas.containers._table import Table  # circular import

        path = normalize_and_check_file_path(path, ".csv", [".csv"], check_if_file_exists=True)

        return Table._from_polars_lazy_frame(pl.scan_csv(path, separator=separator, raise_if_empty=False))

    @staticmethod
    def json_file(path: str | Path) -> Table:
        """
        Read a table from a JSON file.

        Parameters
        ----------
        path:
            The path to the JSON file. If the file extension is omitted, it is assumed to be ".json".

        Returns
        -------
        table:
            The table read from the file.

        Raises
        ------
        FileExtensionError
            If the path has an extension that is not ".json".
        FileNotFoundError
            If no file exists at the given path.

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
        from portabellas.containers._table import Table  # circular import

        path = normalize_and_check_file_path(path, ".json", [".json"], check_if_file_exists=True)

        return Table._from_polars_data_frame(pl.read_json(path))

    @staticmethod
    def jsonl_file(path: str | Path) -> Table:
        """
        Read a table from a JSONL (JSON Lines) file.

        Each line in the file is a valid JSON object. This format is also known as NDJSON (Newline-Delimited JSON).

        Parameters
        ----------
        path:
            The path to the JSONL file. If the file extension is omitted, it is assumed to be ".jsonl".

        Returns
        -------
        table:
            The table read from the file.

        Raises
        ------
        FileExtensionError
            If the path has an extension that is not ".jsonl" or ".ndjson".
        FileNotFoundError
            If no file exists at the given path.

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
        from portabellas.containers._table import Table  # circular import
        from portabellas.exceptions import LazyComputationError

        path = normalize_and_check_file_path(path, ".jsonl", [".jsonl", ".ndjson"], check_if_file_exists=True)

        lazy_frame = pl.scan_ndjson(path)

        try:
            lazy_frame.collect_schema()
        except pl_exceptions.ComputeError as e:
            if "empty reader" in str(e):
                return Table._from_polars_data_frame(pl.DataFrame())
            raise LazyComputationError(str(e)) from None

        return Table._from_polars_lazy_frame(lazy_frame)

    @staticmethod
    def parquet_file(path: str | Path) -> Table:
        """
        Read a table from a Parquet file.

        Parameters
        ----------
        path:
            The path to the Parquet file. If the file extension is omitted, it is assumed to be ".parquet".

        Returns
        -------
        table:
            The table read from the file.

        Raises
        ------
        FileExtensionError
            If the path has an extension that is not ".parquet".
        FileNotFoundError
            If no file exists at the given path.

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
        from portabellas.containers._table import Table  # circular import

        path = normalize_and_check_file_path(path, ".parquet", [".parquet"], check_if_file_exists=True)

        return Table._from_polars_lazy_frame(pl.scan_parquet(path))
