# Validation, Config & Utils

Sources:
- `src/portabellas/_validation/` — validation functions
- `src/portabellas/_config/` — configuration
- `src/portabellas/_utils/` — utility functions

These are internal modules but listed for completeness.

---

## Validation Functions

`check_bounds(name: str, actual: float | None, *, lower_bound: float | None = None, lower_bound_mode: str = "closed", upper_bound: float | None = None, upper_bound_mode: str = "closed") -> None` — Check whether a value is within the expected range and raise an error if it is not.

`check_column_has_no_missing_values(column: Column, *, other_columns: list[Column] | None = None, operation: str = "do an operation") -> None` — Check whether columns have no missing values, and raise an error if any do.

`check_column_is_numeric(column: Column, *, other_columns: list[Column] | None = None, operation: str = "do a numeric operation") -> None` — Check whether columns are numeric, and raise an error if any are not.

`check_columns_are_numeric(table_or_schema: Table | Schema, selector: str | list[str], *, operation: str = "do a numeric operation") -> None` — Check whether the specified columns are numeric, and raise an error if any are not.

`check_columns_dont_exist(table_or_schema: Table | Schema, new_names: str | list[str], *, old_name: str | None = None) -> None` — Check whether the specified new column names do not exist yet and are unique, and raise an error if they do.

`check_columns_exist(table_or_schema: Table | Schema, selector: str | list[str]) -> None` — Check whether the specified columns exist, and raise an error if they do not.

`check_and_convert_datetime_format(format_: str, *, type_: Literal["datetime", "date", "time"], used_for_parsing: bool) -> str` — Validate and convert a portabellas datetime format string to a Polars strftime/strptime format string.

`check_indices[T](sequence: Sequence[T], indices: int | list[int], *, allow_negative: bool = True) -> None` — Check if indices are valid for the provided sequence.

`check_row_counts_are_equal(data: Sequence[Column | Table] | Mapping[str, Sequence[Any]], *, ignore_entries_without_rows: bool = False) -> None` — Check whether all columns or tables have the same row count and raise an error if they do not.

`check_schema(expected: Table | Schema, actual: Table | Schema) -> None` — Check whether two schemas match, and raise an error if they do not.

`check_time_zone(time_zone: str | None) -> None` — Check if the time zone is valid.

`normalize_and_check_file_path(path: str | Path, canonical_file_extension: str, valid_file_extensions: list[str], *, check_if_file_exists: bool = False) -> Path` — Normalize a path and check its validity.

---

## Config

`get_polars_config() -> pl.Config` — Return a `pl.Config` with `float_precision=5`, `tbl_cell_numeric_alignment="RIGHT"`, `tbl_formatting="ASCII_FULL_CONDENSED"`, `tbl_hide_dataframe_shape=True`.

---

## Utils

`compute_duplicates[T](values: list[T], *, forbidden_values: set[T] | None = None) -> list[T]` — Compute the duplicates in a list of values.

`safely_collect_lazy_frame(frame: pl.LazyFrame) -> pl.DataFrame` — Collect a LazyFrame into a DataFrame and raise a custom error if something goes wrong.

`safely_collect_lazy_frame_schema(frame: pl.LazyFrame) -> pl.Schema` — Collect the schema of a LazyFrame and raise a custom error if something goes wrong.

`get_similar_strings(given_string: str, valid_strings: Iterable[str]) -> list[str]` — Find up to 3 close matches for `given_string` in `valid_strings` using `difflib.get_close_matches`.
