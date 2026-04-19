# TODO — Functionality Not Yet Implemented

Sourced from `old_reference/`, tabular data preparation only.

---

## 1. `Table` (`containers/_table.py`)

- **Reference source**: `old_reference/src/safeds/data/tabular/containers/_table.py`
- **Reference tests**: `old_reference/tests/safeds/data/tabular/containers/_table/`

### Missing: Dunder methods

- `__eq__(self, other: object) -> bool` — ref test: `test_eq.py`
- `__hash__(self) -> int` — ref test: `test_hash.py`
- `__dataframe__(self, allow_copy: bool = True) -> DataFrame` — ref test: `test_dataframe.py`
- `_repr_html_(self) -> str` — ref test: `test_repr_html.py`

### Missing: Properties

- `column_count -> int` — ref test: `test_column_count.py`
- `column_names -> list[str]` — ref test: `test_column_names.py`
- `schema -> Schema` — ref test: `test_schema.py`

### Missing: Static factory methods

- `from_columns(columns: Column | list[Column]) -> Table` — ref test: `test_from_columns.py`
- `from_csv_file(path: str | Path, *, separator: str = ",") -> Table` — ref test: `test_from_csv_file.py`
- `from_dict(data: dict[str, list[Any]]) -> Table` — ref test: `test_from_dict.py`
- `from_json_file(path: str | Path) -> Table` — ref test: `test_from_json_file.py`
- `from_parquet_file(path: str | Path) -> Table` — ref test: `test_from_parquet_file.py`

### Missing: Column operations

- `add_columns(columns: Column | list[Column] | Table) -> Table` — ref test: `test_add_columns.py`
- `add_computed_column(name: str, computer: Callable[[Row], Cell]) -> Table` — ref test: `test_add_computed_column.py`
- `add_index_column(name: str, *, first_index: int = 0) -> Table` — ref test: `test_add_index_column.py`
- `get_column(name: str) -> Column` — ref test: `test_get_column.py`
- `get_column_type(name: str) -> DataType` — ref test: `test_get_column_type.py`
- `has_column(name: str) -> bool` — ref test: `test_has_column.py`
- `remove_columns(selector: str | list[str], *, ignore_unknown_names: bool = False) -> Table` — ref test: `test_remove_columns.py`
- `remove_columns_with_missing_values(*, missing_value_ratio_threshold: float = 0) -> Table` — ref test: `test_remove_columns_with_missing_values.py`
- `remove_non_numeric_columns() -> Table` — ref test: `test_remove_non_numeric_columns.py`
- `rename_column(old_name: str, new_name: str) -> Table` — ref test: `test_rename_column.py`
- `replace_column(old_name: str, new_columns: Column | list[Column] | Table) -> Table` — ref test: `test_replace_column.py`
- `select_columns(selector: str | list[str]) -> Table` — ref test: `test_select_columns.py`
- `transform_columns(selector: str | list[str], transformer: Callable[[Cell], Cell] | Callable[[Cell, Row], Cell]) -> Table` — ref test: `test_transform_columns.py`

### Missing: Row operations

- `count_rows_if(predicate: Callable[[Row], Cell[bool | None]], *, ignore_unknown: bool = True) -> int | None` — ref test: `test_count_rows_if.py`
- `filter_rows(predicate: Callable[[Row], Cell[bool | None]]) -> Table` — ref test: `test_filter_rows.py`
- `filter_rows_by_column(name: str, predicate: Callable[[Cell], Cell[bool | None]]) -> Table` — ref test: `test_filter_rows_by_column.py`
- `remove_duplicate_rows() -> Table` — ref test: `test_remove_duplicate_rows.py`
- `remove_rows(predicate: Callable[[Row], Cell[bool | None]]) -> Table` — ref test: `test_remove_rows.py`
- `remove_rows_by_column(name: str, predicate: Callable[[Cell], Cell[bool | None]]) -> Table` — ref test: `test_remove_rows_by_column.py`
- `remove_rows_with_missing_values(*, selector: str | list[str] | None = None) -> Table` — ref test: `test_remove_rows_with_missing_values.py`
- `remove_rows_with_outliers(*, selector: str | list[str] | None = None, z_score_threshold: float = 3) -> Table` — ref test: `test_remove_rows_with_outliers.py`
- `shuffle_rows(*, random_seed: int = 0) -> Table` — ref test: `test_shuffle_rows.py`
- `slice_rows(*, start: int = 0, length: int | None = None) -> Table` — ref test: `test_slice_rows.py`
- `sort_rows(key_selector: Callable[[Row], Cell], *, descending: bool = False) -> Table` — ref test: `test_sort_rows.py`
- `sort_rows_by_column(name: str, *, descending: bool = False) -> Table` — ref test: `test_sort_rows_by_column.py`
- `split_rows(percentage_in_first: float, *, shuffle: bool = True, random_seed: int = 0) -> tuple[Table, Table]` — ref test: `test_split_rows.py`

### Missing: Table operations

- `add_tables_as_columns(others: Table | list[Table]) -> Table` — ref test: `test_add_tables_as_columns.py`
- `add_tables_as_rows(others: Table | list[Table]) -> Table` — ref test: `test_add_tables_as_rows.py`
- `join(right_table: Table, left_names: str | list[str], right_names: str | list[str], *, mode: Literal["inner", "left", "right", "full"] = "inner") -> Table` — ref test: `test_join.py`

### Missing: Statistics

- `summarize_statistics() -> Table` — ref test: `test_summarize_statistics.py`

### Missing: Export

- `to_columns() -> list[Column]` — ref test: `test_to_columns.py`
- `to_csv_file(path: str | Path) -> None` — ref test: `test_to_csv_file.py`
- `to_dict() -> dict[str, list[Any]]` — ref test: `test_to_dict.py`
- `to_json_file(path: str | Path) -> None` — ref test: `test_to_json_file.py`
- `to_parquet_file(path: str | Path) -> None` — ref test: `test_to_parquet_file.py`

---

## 2. `Column` (`containers/_column.py`)

- **Reference source**: `old_reference/src/safeds/data/tabular/containers/_column.py`
- **Reference tests**: `old_reference/tests/safeds/data/tabular/containers/_column/`

### Missing: Dunder methods

- `__eq__(self, other: object) -> bool` — ref test: `test_eq.py`
- `__hash__(self) -> int` — ref test: `test_hash.py`
- `_repr_html_(self) -> str` — ref test: `test_repr_html.py`

### Missing: Value operations

- `get_distinct_values(self, *, ignore_missing_values: bool = True) -> Sequence[T | None]` — ref test: `test_get_distinct_values.py`

### Missing: Reductions (quantifiers)

- `all(self, predicate: Callable[[Cell[T]], Cell[bool | None]], *, ignore_unknown: bool = True) -> bool | None` — ref test: `test_all.py`
- `any(self, predicate: Callable[[Cell[T]], Cell[bool | None]], *, ignore_unknown: bool = True) -> bool | None` — ref test: `test_any.py`
- `count_if(self, predicate: Callable[[Cell[T]], Cell[bool | None]], *, ignore_unknown: bool = True) -> int | None` — ref test: `test_count_if.py`
- `none(self, predicate: Callable[[Cell[T]], Cell[bool | None]], *, ignore_unknown: bool = True) -> bool | None` — ref test: `test_none.py`

### Missing: Statistics

- `summarize_statistics(self) -> Table` — ref test: `test_summarize_statistics.py`
- `correlation_with(self, other: Column) -> float` — ref test: `test_correlation_with.py`
- `distinct_value_count(self, *, ignore_missing_values: bool = True) -> int` — ref test: `test_distinct_value_count.py`
- `idness(self) -> float` — ref test: `test_idness.py`
- `max(self) -> T | None` — ref test: `test_max.py`
- `mean(self) -> T` — ref test: `test_mean.py`
- `median(self) -> T` — ref test: `test_median.py`
- `min(self) -> T | None` — ref test: `test_min.py`
- `missing_value_count(self) -> int` — ref test: `test_missing_value_count.py`
- `missing_value_ratio(self) -> float` — ref test: `test_missing_value_ratio.py`
- `mode(self, *, ignore_missing_values: bool = True) -> Sequence[T | None]` — ref test: `test_mode.py`
- `stability(self) -> float` — ref test: `test_stability.py`
- `standard_deviation(self) -> float` — ref test: `test_standard_deviation.py`
- `variance(self) -> float` — ref test: `test_variance.py`

### Missing: Export

- `to_list(self) -> list[T]` — ref test: `test_to_list.py`

---

## 3. `Row` (`containers/_row/`)

- **Reference source**: `old_reference/src/safeds/data/tabular/containers/_row.py` (ABC), `old_reference/src/safeds/data/tabular/containers/_lazy_vectorized_row.py` (concrete)
- **Reference tests**: `old_reference/tests/safeds/data/tabular/containers/_lazy_vectorized_row/`

Empty stub. All methods and properties missing.

### Abstract interface (to be defined on `Row`)

- `__contains__(self, key: object, /) -> bool` — ref test: `test_contains.py`
- `__eq__(self, other: object) -> bool` — ref test: `test_eq.py`
- `__getitem__(self, name: str) -> Cell` — ref test: `test_getitem.py`
- `__hash__(self) -> int` — ref test: `test_hash.py`
- `__iter__(self) -> Iterator[str]` — ref test: `test_iter.py`
- `__len__(self) -> int` — ref test: `test_len.py`
- `column_count -> int` — ref test: `test_column_count.py`
- `column_names -> list[str]` — ref test: `test_column_names.py`
- `schema -> Schema` — ref test: `test_schema.py`
- `get_cell(self, name: str) -> Cell` — ref test: `test_get_cell.py`
- `get_column_type(self, name: str) -> DataType` — ref test: `test_get_column_type.py`
- `has_column(self, name: str) -> bool` — ref test: `test_has_column.py`

### Concrete `ExprRow` (lazy, builds Polars expressions)

- Delegates all operations to the underlying table
- `get_cell(name: str) -> ExprCell` — returns `ExprCell(pl.col(name))`

---

## 4. `Cell` (`containers/_cell/`)

- **Reference source**: `old_reference/src/safeds/data/tabular/containers/_cell.py` (ABC), `old_reference/src/safeds/data/tabular/containers/_lazy_cell.py` (concrete)
- **Reference tests**: `old_reference/tests/safeds/data/tabular/containers/_lazy_cell/`

### Type aliases (to be defined)

```python
_ConvertibleToIntCell = int | Cell | None
_ConvertibleToStringCell = str | Cell | None
```

### Missing: Static methods

- `date(year: _ConvertibleToIntCell, month: _ConvertibleToIntCell, day: _ConvertibleToIntCell) -> Cell[date | None]` — ref test: `test_date.py`
- `datetime(year: _ConvertibleToIntCell, month: _ConvertibleToIntCell, day: _ConvertibleToIntCell, hour: _ConvertibleToIntCell, minute: _ConvertibleToIntCell, second: _ConvertibleToIntCell, *, microsecond: _ConvertibleToIntCell = 0, time_zone: str | None = None) -> Cell[datetime | None]` — ref test: `test_datetime.py`
- `duration(*, weeks: _ConvertibleToIntCell = 0, days: _ConvertibleToIntCell = 0, hours: _ConvertibleToIntCell = 0, minutes: _ConvertibleToIntCell = 0, seconds: _ConvertibleToIntCell = 0, milliseconds: _ConvertibleToIntCell = 0, microseconds: _ConvertibleToIntCell = 0) -> Cell[timedelta | None]` — ref test: `test_duration.py`
- `time(hour: _ConvertibleToIntCell, minute: _ConvertibleToIntCell, second: _ConvertibleToIntCell, *, microsecond: _ConvertibleToIntCell = 0) -> Cell[time | None]` — ref test: `test_time.py`
- `first_not_none(cells: list[Cell[P]]) -> Cell[P | None]` — ref test: `test_first_not_none.py`

### Missing: Properties (namespaces)

- `dt -> DatetimeOperations`
- `dur -> DurationOperations`
- `math -> MathOperations`
- `str -> StringOperations`

### Missing: Other

- `_equals(self, other: object) -> bool` — ref test: `test_equals.py`

---

## 5. `Schema` (`typing/_schema.py`)

- **Reference source**: `old_reference/src/safeds/data/tabular/typing/_schema.py`
- **Reference tests**: `old_reference/tests/safeds/data/tabular/typing/_schema/`

Empty stub. All methods and properties missing.

- `__init__(self, schema: Mapping[str, DataType]) -> None`
- `_from_polars_schema(schema: pl.Schema) -> Schema`
- `__contains__(self, key: object, /) -> bool` — ref test: `test_contains.py`
- `__eq__(self, other: object) -> bool` — ref test: `test_eq.py`
- `__getitem__(self, key: str, /) -> DataType` — ref test: `test_get_item.py`
- `__hash__(self) -> int` — ref test: `test_hash.py`
- `__iter__(self) -> Iterator[str]` — ref test: `test_iter.py`
- `__len__(self) -> int` — ref test: `test_len.py`
- `__repr__(self) -> str` — ref test: `test_repr.py`
- `__str__(self) -> str` — ref test: `test_str.py`
- `_repr_markdown_(self) -> str` — ref test: `test_repr_markdown.py`
- `column_count -> int` — ref test: `test_column_count.py`
- `column_names -> list[str]` — ref test: `test_column_names.py`
- `get_column_type(self, name: str) -> DataType` — ref test: `test_get_column_type.py`
- `has_column(self, name: str) -> bool` — ref test: `test_has_column.py`
- `to_dict(self) -> dict[str, DataType]` — ref test: `test_to_dict.py`

---

## 6. `StringOperations` (`query/_string_operations/`)

- **Reference source**: `old_reference/src/safeds/data/tabular/query/_string_operations.py` (ABC), `old_reference/src/safeds/data/tabular/query/_lazy_string_operations.py` (concrete)
- **Reference tests**: `old_reference/tests/safeds/data/tabular/query/_lazy_string_operations/`

Empty stub. All methods missing.

- `contains(self, substring: _ConvertibleToStringCell) -> Cell[bool | None]` — ref test: `test_contains.py`
- `ends_with(self, suffix: _ConvertibleToStringCell) -> Cell[bool | None]` — ref test: `test_ends_with.py`
- `index_of(self, substring: _ConvertibleToStringCell) -> Cell[int | None]` — ref test: `test_index_of.py`
- `length(self, *, optimize_for_ascii: bool = False) -> Cell[int | None]` — ref test: `test_length.py`
- `pad_end(self, length: int, *, character: str = " ") -> Cell[str | None]` — ref test: `test_pad_end.py`
- `pad_start(self, length: int, *, character: str = " ") -> Cell[str | None]` — ref test: `test_pad_start.py`
- `remove_prefix(self, prefix: _ConvertibleToStringCell) -> Cell[str | None]` — ref test: `test_remove_prefix.py`
- `remove_suffix(self, suffix: _ConvertibleToStringCell) -> Cell[str | None]` — ref test: `test_remove_suffix.py`
- `repeat(self, count: _ConvertibleToIntCell) -> Cell[str | None]` — ref test: `test_repeat.py`
- `replace_all(self, old: _ConvertibleToStringCell, new: _ConvertibleToStringCell) -> Cell[str | None]` — ref test: `test_replace_all.py`
- `reverse(self) -> Cell[str | None]` — ref test: `test_reverse.py`
- `slice(self, *, start: _ConvertibleToIntCell = 0, length: _ConvertibleToIntCell = None) -> Cell[str | None]` — ref test: `test_slice.py`
- `starts_with(self, prefix: _ConvertibleToStringCell) -> Cell[bool | None]` — ref test: `test_starts_with.py`
- `strip(self, *, characters: _ConvertibleToStringCell = None) -> Cell[str | None]` — ref test: `test_strip.py`
- `strip_end(self, *, characters: _ConvertibleToStringCell = None) -> Cell[str | None]` — ref test: `test_strip_end.py`
- `strip_start(self, *, characters: _ConvertibleToStringCell = None) -> Cell[str | None]` — ref test: `test_strip_start.py`
- `to_date(self, *, format: str | None = "iso") -> Cell[date | None]` — ref test: `test_to_date.py`
- `to_datetime(self, *, format: str | None = "iso") -> Cell[datetime | None]` — ref test: `test_to_datetime.py`
- `to_float(self) -> Cell[float | None]` — ref test: `test_to_float.py`
- `to_int(self, *, base: _ConvertibleToIntCell = 10) -> Cell[int | None]` — ref test: `test_to_int.py`
- `to_lowercase(self) -> Cell[str | None]` — ref test: `test_to_lowercase.py`
- `to_time(self, *, format: str | None = "iso") -> Cell[time | None]` — ref test: `test_to_time.py`
- `to_uppercase(self) -> Cell[str | None]` — ref test: `test_to_uppercase.py`

---

## 7. `DatetimeOperations` (`query/_datetime_operations/`)

- **Reference source**: `old_reference/src/safeds/data/tabular/query/_datetime_operations.py` (ABC), `old_reference/src/safeds/data/tabular/query/_lazy_datetime_operations.py` (concrete)
- **Reference tests**: `old_reference/tests/safeds/data/tabular/query/_lazy_datetime_operations/`

Empty stub. All methods missing.

### Extract component

- `century(self) -> Cell[int | None]` — ref test: `test_century.py`
- `date(self) -> Cell[date | None]` — ref test: `test_date.py`
- `day(self) -> Cell[int | None]` — ref test: `test_day.py`
- `day_of_week(self) -> Cell[int | None]` — ref test: `test_day_of_week.py`
- `day_of_year(self) -> Cell[int | None]` — ref test: `test_day_of_year.py`
- `hour(self) -> Cell[int | None]` — ref test: `test_hour.py`
- `microsecond(self) -> Cell[int | None]` — ref test: `test_microsecond.py`
- `millennium(self) -> Cell[int | None]` — ref test: `test_millennium.py`
- `millisecond(self) -> Cell[int | None]` — ref test: `test_millisecond.py`
- `minute(self) -> Cell[int | None]` — ref test: `test_minute.py`
- `month(self) -> Cell[int | None]` — ref test: `test_month.py`
- `quarter(self) -> Cell[int | None]` — ref test: `test_quarter.py`
- `second(self) -> Cell[int | None]` — ref test: `test_second.py`
- `time(self) -> Cell[time | None]` — ref test: `test_time.py`
- `week(self) -> Cell[int | None]` — ref test: `test_week.py`
- `year(self) -> Cell[int | None]` — ref test: `test_year.py`

### Other

- `is_in_leap_year(self) -> Cell[bool | None]` — ref test: `test_is_in_leap_year.py`
- `replace(self, *, year: _ConvertibleToIntCell = None, month: _ConvertibleToIntCell = None, day: _ConvertibleToIntCell = None, hour: _ConvertibleToIntCell = None, minute: _ConvertibleToIntCell = None, second: _ConvertibleToIntCell = None, microsecond: _ConvertibleToIntCell = None) -> Cell` — ref test: `test_replace.py`
- `to_string(self, *, format: str = "iso") -> Cell[str | None]` — ref test: `test_to_string.py`
- `unix_timestamp(self, *, unit: Literal["s", "ms", "us"] = "s") -> Cell[int | None]` — ref test: `test_unix_timestamp.py`

---

## 8. `DurationOperations` (`query/_duration_operations/`)

- **Reference source**: `old_reference/src/safeds/data/tabular/query/_duration_operations.py` (ABC), `old_reference/src/safeds/data/tabular/query/_lazy_duration_operations.py` (concrete)
- **Reference tests**: `old_reference/tests/safeds/data/tabular/query/_lazy_duration_operations/`

Empty stub. All methods missing.

- `abs(self) -> Cell[timedelta | None]` — ref test: `test_abs.py`
- `full_weeks(self) -> Cell[int | None]` — ref test: `test_full_weeks.py`
- `full_days(self) -> Cell[int | None]` — ref test: `test_full_days.py`
- `full_hours(self) -> Cell[int | None]` — ref test: `test_full_hours.py`
- `full_minutes(self) -> Cell[int | None]` — ref test: `test_full_minutes.py`
- `full_seconds(self) -> Cell[int | None]` — ref test: `test_full_seconds.py`
- `full_milliseconds(self) -> Cell[int | None]` — ref test: `test_full_milliseconds.py`
- `full_microseconds(self) -> Cell[int | None]` — ref test: `test_full_microseconds.py`
- `to_string(self, *, format: Literal["iso", "pretty"] = "iso") -> Cell[str | None]` — ref test: `test_to_string.py`

---

## 9. `MathOperations` (`query/_math_operations/`)

- **Reference source**: `old_reference/src/safeds/data/tabular/query/_math_operations.py` (ABC), `old_reference/src/safeds/data/tabular/query/_lazy_math_operations.py` (concrete)
- **Reference tests**: `old_reference/tests/safeds/data/tabular/query/_lazy_math_operations/`

Empty stub. All methods missing.

- `abs(self) -> Cell` — ref test: `test_abs.py`
- `acos(self) -> Cell` — ref test: `test_acos.py`
- `acosh(self) -> Cell` — ref test: `test_acosh.py`
- `asin(self) -> Cell` — ref test: `test_asin.py`
- `asinh(self) -> Cell` — ref test: `test_asinh.py`
- `atan(self) -> Cell` — ref test: `test_atan.py`
- `atanh(self) -> Cell` — ref test: `test_atanh.py`
- `cbrt(self) -> Cell` — ref test: `test_cbrt.py`
- `ceil(self) -> Cell` — ref test: `test_ceil.py`
- `cos(self) -> Cell` — ref test: `test_cos.py`
- `cosh(self) -> Cell` — ref test: `test_cosh.py`
- `degrees_to_radians(self) -> Cell` — ref test: `test_degrees_to_radians.py`
- `exp(self) -> Cell` — ref test: `test_exp.py`
- `floor(self) -> Cell` — ref test: `test_floor.py`
- `ln(self) -> Cell` — ref test: `test_ln.py`
- `log(self, base: float) -> Cell` — ref test: `test_log.py`
- `log10(self) -> Cell` — ref test: `test_log10.py`
- `radians_to_degrees(self) -> Cell` — ref test: `test_radians_to_degrees.py`
- `round_to_decimal_places(self, decimal_places: int) -> Cell` — ref test: `test_round_to_decimal_places.py`
- `round_to_significant_figures(self, significant_figures: int) -> Cell` — ref test: `test_round_to_significant_figures.py`
- `sign(self) -> Cell` — ref test: `test_sign.py`
- `sin(self) -> Cell` — ref test: `test_sin.py`
- `sinh(self) -> Cell` — ref test: `test_sinh.py`
- `sqrt(self) -> Cell` — ref test: `test_sqrt.py`
- `tan(self) -> Cell` — ref test: `test_tan.py`
- `tanh(self) -> Cell` — ref test: `test_tanh.py`

---

## 10. IO — `TableReader` (`io/_table_reader.py`)

- **Reference source**: `old_reference/src/safeds/data/tabular/containers/_table.py` (IO was on Table directly: `from_csv_file`, `from_json_file`, `from_parquet_file`)
- **Reference tests**: `old_reference/tests/safeds/data/tabular/containers/_table/` (test_from_csv_file.py, test_from_json_file.py, test_from_parquet_file.py)

Empty stub. All methods missing.

- `csv_file(path: str | Path, *, separator: str = ",") -> Table`
- `json_file(path: str | Path) -> Table`
- `parquet_file(path: str | Path) -> Table`

---

## 11. IO — `TableWriter` (`io/_table_writer.py`)

- **Reference source**: `old_reference/src/safeds/data/tabular/containers/_table.py` (IO was on Table directly: `to_csv_file`, `to_json_file`, `to_parquet_file`)
- **Reference tests**: `old_reference/tests/safeds/data/tabular/containers/_table/` (test_to_csv_file.py, test_to_json_file.py, test_to_parquet_file.py)

Has `__init__` only. All write methods missing.

- `csv_file(self, path: str | Path) -> None`
- `json_file(self, path: str | Path) -> None`
- `parquet_file(self, path: str | Path) -> None`

---

## 12. Plotters (`plotting/`)

- **Reference source**: `old_reference/src/safeds/data/tabular/plotting/_table_plotter.py`, `old_reference/src/safeds/data/tabular/plotting/_column_plotter.py`
- **Reference tests**: None (plotting had no separate test files in the old reference)

Stubs exist with `__init__` only. All plot methods missing.

### `TablePlotter`

- `box_plots(self, *, theme: Literal["dark", "light"] = "light") -> Image`
- `histograms(self, *, max_bin_count: int = 10, theme: Literal["dark", "light"] = "light") -> Image`
- `violin_plots(self, *, theme: Literal["dark", "light"] = "light") -> Image`
- `line_plot(self, x_name: str, y_names: list[str], *, show_confidence_interval: bool = True, theme: Literal["dark", "light"] = "light") -> Image`
- `histogram_2d(self, x_name: str, y_name: str, *, x_max_bin_count: int = 10, y_max_bin_count: int = 10, theme: Literal["dark", "light"] = "light") -> Image`
- `moving_average_plot(self, x_name: str, y_name: str, window_size: int, *, theme: Literal["dark", "light"] = "light") -> Image`
- `scatter_plot(self, x_name: str, y_names: list[str], *, theme: Literal["dark", "light"] = "light") -> Image`
- `correlation_heatmap(self, *, theme: Literal["dark", "light"] = "light") -> Image`

### `ColumnPlotter`

- `box_plot(self, *, theme: Literal["dark", "light"] = "light") -> Image`
- `histogram(self, *, max_bin_count: int = 10, theme: Literal["dark", "light"] = "light") -> Image`
- `lag_plot(self, lag: int, *, theme: Literal["dark", "light"] = "light") -> Image`
- `violin_plot(self, *, theme: Literal["dark", "light"] = "light") -> Image`

---

## 13. Additional `DataType` variants

- **Reference source**: `old_reference/src/safeds/data/tabular/typing/_column_type.py`
- **Reference tests**: `old_reference/tests/safeds/data/tabular/typing/_polars_column_type/`

- `Decimal(precision: int, scale: int) -> DataType`
- `Array(inner: DataType, width: int) -> DataType`
- `List(inner: DataType) -> DataType`
- `Struct(fields: list[tuple[str, DataType]]) -> DataType`
- `Categorical() -> DataType`
- `Enum(categories: list[str]) -> DataType`
- `Object() -> DataType`
- `Unknown() -> DataType`

---

## 14. Missing validation functions (`_validation/`)

- **Reference source**: `old_reference/src/safeds/_validation/`

- `check_bounds(value, *, lower_bound, upper_bound, lower_bound_mode, upper_bound_mode) -> None`
- `check_column_has_no_missing_values(column) -> None`
- `check_column_is_numeric(column) -> None` / `check_columns_are_numeric(columns) -> None`
- `check_columns_dont_exist(names, old_names) -> None`
- `check_columns_exist(names, old_names) -> None`
- `check_schema(actual, expected) -> None`
- `convert_and_check_datetime_format(format) -> str`
- `normalize_and_check_file_path(path, *, valid_extensions, default_extension) -> Path`

---

## 15. Missing exception classes (`exceptions/`)

- **Reference source**: `old_reference/src/safeds/exceptions/_data.py`

- `NonNumericColumnError`
- `MissingValuesColumnError`
- `IllegalFormatError`
- `OutOfBoundsError` (used by `check_bounds`)
- `MissingValuesError` (used by `check_column_has_no_missing_values`)
- `ColumnTypeError` (used by `check_column_is_numeric`)
- `DuplicateColumnError` (used by `check_columns_dont_exist`)
- `ColumnNotFoundError` (used by `check_columns_exist`)
- `SchemaError` (used by `check_schema`)
- `FileExtensionError` (used by `normalize_and_check_file_path`)
