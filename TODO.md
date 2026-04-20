# TODO — Functionality Not Yet Implemented

Sourced from `old_reference/`, tabular data preparation only. If something is not listed here, it's already done.

---

## 1. `Table` (`containers/_table.py`)

- **Reference source**: `old_reference/src/safeds/data/tabular/containers/_table.py`
- **Reference tests**: `old_reference/tests/safeds/data/tabular/containers/_table/`

### Missing: Dunder methods

(None — all implemented.)

### Missing: Properties

(None — all implemented.)

### Missing: Static factory methods

(None — from_columns and from_dict implemented; from_csv/from_json/from_parquet via `Table.read.*`.)

### Missing: Column operations

- `add_index_column(name: str, *, first_index: int = 0) -> Table` — ref test: `test_add_index_column.py`
- `remove_columns(selector: str | list[str], *, ignore_unknown_names: bool = False) -> Table` — ref test: `test_remove_columns.py`
- `remove_columns_with_missing_values(*, missing_value_ratio_threshold: float = 0) -> Table` — ref test: `test_remove_columns_with_missing_values.py`
- `remove_non_numeric_columns() -> Table` — ref test: `test_remove_non_numeric_columns.py`
- `rename_column(old_name: str, new_name: str) -> Table` — ref test: `test_rename_column.py`
- `replace_column(old_name: str, new_columns: Column | list[Column] | Table) -> Table` — ref test: `test_replace_column.py`
- `select_columns(selector: str | list[str]) -> Table` — ref test: `test_select_columns.py`
- `transform_columns(selector: str | list[str], mapper: Callable[[Cell], Cell] | Callable[[Cell, Row], Cell]) -> Table` — ref test: `test_transform_columns.py` (rename to `map_columns` when implementing)

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

(None — to_columns and to_dict implemented; to_csv/to_json/to_parquet via `table.write.*`.)

---

## 2. `Column` (`containers/_column.py`)

- **Reference source**: `old_reference/src/safeds/data/tabular/containers/_column.py`
- **Reference tests**: `old_reference/tests/safeds/data/tabular/containers/_column/`

### Missing: Dunder methods

(None — all implemented.)

### Missing: Value operations

- `get_distinct_values(self, *, ignore_missing_values: bool = True) -> Sequence[T | None]` — ref test: `test_get_distinct_values.py`

### Missing: Reductions (quantifiers)

(None — all, any, count_if, and none implemented.)

### Missing: Statistics

- `summarize_statistics(self) -> Table` — ref test: `test_summarize_statistics.py`
- `correlation_with(self, other: Column) -> float` — ref test: `test_correlation_with.py`
- `distinct_value_count(self, *, ignore_missing_values: bool = True) -> int` — ref test: `test_distinct_value_count.py`
- `idness(self) -> float` — ref test: `test_idness.py` (maybe...)
- `max(self) -> T | None` — ref test: `test_max.py`
- `mean(self) -> T` — ref test: `test_mean.py`
- `median(self) -> T` — ref test: `test_median.py`
- `min(self) -> T | None` — ref test: `test_min.py`
- `missing_value_count(self) -> int` — ref test: `test_missing_value_count.py` (maybe... - probably either this or missing_value_ratio)
- `missing_value_ratio(self) -> float` — ref test: `test_missing_value_ratio.py` (maybe... - probably either this or missing_value_count)
- `mode(self, *, ignore_missing_values: bool = True) -> Sequence[T | None]` — ref test: `test_mode.py`
- `stability(self) -> float` — ref test: `test_stability.py` (maybe...)
- `standard_deviation(self) -> float` — ref test: `test_standard_deviation.py`
- `variance(self) -> float` — ref test: `test_variance.py`

### Missing: Export

(None — to_list implemented.)

---

## 3. Plotters (`plotting/`)

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
- Potentially create interactive plots (e.g. with plotly?), instead of static matplotlib plots

### `ColumnPlotter`

- `box_plot(self, *, theme: Literal["dark", "light"] = "light") -> Image`
- `histogram(self, *, max_bin_count: int = 10, theme: Literal["dark", "light"] = "light") -> Image`
- `lag_plot(self, lag: int, *, theme: Literal["dark", "light"] = "light") -> Image`
- `violin_plot(self, *, theme: Literal["dark", "light"] = "light") -> Image`
- Potentially create interactive plots (e.g. with plotly?), instead of static matplotlib plots

---

## 4. Additional `DataType` variants

- `Decimal(precision: int, scale: int) -> DataType`
- `Array(inner: DataType, width: int) -> DataType`
- `List(inner: DataType) -> DataType`
- `Struct(fields: list[tuple[str, DataType]]) -> DataType`
- `Categorical() -> DataType`
- `Enum(categories: list[str]) -> DataType`
- `Object() -> DataType`
- `Unknown() -> DataType`

---

## 5. Missing validation functions (`_validation/`)

- **Reference source**: `old_reference/src/safeds/_validation/`

- `check_bounds(value, *, lower_bound, upper_bound, lower_bound_mode, upper_bound_mode) -> None` ✅
- `check_column_has_no_missing_values(column) -> None`
- `check_column_is_numeric(column) -> None` / `check_columns_are_numeric(columns) -> None`
- `check_schema(actual, expected) -> None`
- `convert_and_check_datetime_format(format) -> str` ✅ (lives in `_expr_string_operations.py`)
- `normalize_and_check_file_path(path, *, valid_extensions, default_extension) -> Path` ✅

---

## 6. Missing exception classes (`exceptions/`)

- **Reference source**: `old_reference/src/safeds/exceptions/_data.py`

- `NonNumericColumnError`
- `MissingValuesColumnError`
- `IllegalFormatError`
- `OutOfBoundsError` ✅
- `FileExtensionError` ✅
- `MissingValuesError` (used by `check_column_has_no_missing_values`)
- `ColumnTypeError` (used by `check_column_is_numeric`)
- `SchemaError` (used by `check_schema`)
- `FileExtensionError` (used by `normalize_and_check_file_path`)

---

## 7. Integration rules

- `old_reference/` is in `.gitignore` — use `rm` (not `git rm`) to delete files from it.
- Only delete old_reference files for items that are **fully integrated** (e.g., don't delete Row source if Row still has missing methods).
- No `__eq__`/`__hash__` on Row — explicitly excluded.
- No `_equals()` on Cell — explicitly excluded.
- No `__sizeof__` on Cell — explicitly excluded.
- No `_structural_hash` — use straightforward `hash()` that fulfills the hash contract.
- No transformers (imputers, scalers, encoders, discretizers) — out of scope.
- TODO.md lists only **missing** functionality — if something isn't listed, it's already done.
- Add exception classes and validation functions **as needed** (not once upfront).
