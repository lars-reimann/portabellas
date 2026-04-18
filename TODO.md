# TODO — Functionality Not Yet Implemented

Sourced from Safe-DS (`/home/lars/Repositories/Safe-DS/Library`), tabular data preparation only.
Already-implemented stubs and classes are noted where relevant.

---

## 1. `Table` (`containers/_table.py`)

### Already implemented

- `__init__(self, data: Mapping[str, Sequence[object]]) -> None`
- `__repr__(self) -> str`
- `__str__(self) -> str`
- `row_count -> int`
- `_data_frame -> pl.DataFrame`
- `_from_polars_data_frame(data: pl.DataFrame) -> Table`
- `_from_polars_lazy_frame(data: pl.LazyFrame) -> Table`
- `plot -> TablePlotter`
- `write -> TableWriter`
- `read: TableReader` (class attribute)

### Missing: Dunder methods

- `__eq__(self, other: object) -> bool`
- `__hash__(self) -> int`
- `__sizeof__(self) -> int`
- `__dataframe__(self, allow_copy: bool = True) -> DataFrame` — dataframe interchange protocol
- `_repr_html_(self) -> str` — IPython HTML representation

### Missing: Properties

- `column_count -> int`
- `column_names -> list[str]`
- `schema -> Schema`

### Missing: Static factory methods

- `from_columns(columns: Column | list[Column]) -> Table`
- `from_csv_file(path: str | Path, *, separator: str = ",") -> Table`
- `from_dict(data: dict[str, list[Any]]) -> Table`
- `from_json_file(path: str | Path) -> Table`
- `from_parquet_file(path: str | Path) -> Table`

### Missing: Column operations

- `add_columns(columns: Column | list[Column] | Table) -> Table`
- `add_computed_column(name: str, computer: Callable[[Row], Cell]) -> Table`
- `add_index_column(name: str, *, first_index: int = 0) -> Table`
- `get_column(name: str) -> Column`
- `get_column_type(name: str) -> DataType`
- `has_column(name: str) -> bool`
- `remove_columns(selector: str | list[str], *, ignore_unknown_names: bool = False) -> Table`
- `remove_columns_with_missing_values(*, missing_value_ratio_threshold: float = 0) -> Table`
- `remove_non_numeric_columns() -> Table`
- `rename_column(old_name: str, new_name: str) -> Table`
- `replace_column(old_name: str, new_columns: Column | list[Column] | Table) -> Table`
- `select_columns(selector: str | list[str]) -> Table`
- `transform_columns(selector: str | list[str], transformer: Callable[[Cell], Cell] | Callable[[Cell, Row], Cell]) -> Table`

### Missing: Row operations

- `count_rows_if(predicate: Callable[[Row], Cell[bool | None]], *, ignore_unknown: bool = True) -> int | None`
- `filter_rows(predicate: Callable[[Row], Cell[bool | None]]) -> Table`
- `filter_rows_by_column(name: str, predicate: Callable[[Cell], Cell[bool | None]]) -> Table`
- `remove_duplicate_rows() -> Table`
- `remove_rows(predicate: Callable[[Row], Cell[bool | None]]) -> Table`
- `remove_rows_by_column(name: str, predicate: Callable[[Cell], Cell[bool | None]]) -> Table`
- `remove_rows_with_missing_values(*, selector: str | list[str] | None = None) -> Table`
- `remove_rows_with_outliers(*, selector: str | list[str] | None = None, z_score_threshold: float = 3) -> Table`
- `shuffle_rows(*, random_seed: int = 0) -> Table`
- `slice_rows(*, start: int = 0, length: int | None = None) -> Table`
- `sort_rows(key_selector: Callable[[Row], Cell], *, descending: bool = False) -> Table`
- `sort_rows_by_column(name: str, *, descending: bool = False) -> Table`
- `split_rows(percentage_in_first: float, *, shuffle: bool = True, random_seed: int = 0) -> tuple[Table, Table]`

### Missing: Table operations

- `add_tables_as_columns(others: Table | list[Table]) -> Table`
- `add_tables_as_rows(others: Table | list[Table]) -> Table`
- `join(right_table: Table, left_names: str | list[str], right_names: str | list[str], *, mode: Literal["inner", "left", "right", "full"] = "inner") -> Table`

### Missing: Statistics

- `summarize_statistics() -> Table`

### Missing: Export

- `to_columns() -> list[Column]`
- `to_csv_file(path: str | Path) -> None`
- `to_dict() -> dict[str, list[Any]]`
- `to_json_file(path: str | Path) -> None`
- `to_parquet_file(path: str | Path) -> None`

---

## 2. `Column` (`containers/_column.py`)

### Already implemented

- `__init__(self, name: str, data: Sequence[T], *, type: DataType | None = None) -> None`
- `__contains__(self, value: object) -> bool`
- `__getitem__(self, index: int) -> T`
- `__getitem__(self, index: slice) -> Column[T]`
- `__iter__(self) -> Iterator[T]`
- `__len__(self) -> int`
- `__repr__(self) -> str`
- `__str__(self) -> str`
- `name -> str`
- `row_count -> int`
- `type -> DataType`
- `_series -> pl.Series`
- `_from_polars_series(data: pl.Series) -> Column`
- `_from_polars_lazy_frame(name: str, data: pl.LazyFrame) -> Column`
- `get_value(self, index: int) -> T`
- `plot -> ColumnPlotter`

### Missing: Dunder methods

- `__eq__(self, other: object) -> bool`
- `__hash__(self) -> int`
- `__sizeof__(self) -> int`
- `_repr_html_(self) -> str`

### Missing: Value operations

- `get_distinct_values(self, *, ignore_missing_values: bool = True) -> Sequence[T | None]`

### Missing: Reductions (quantifiers)

- `all(self, predicate: Callable[[Cell[T]], Cell[bool | None]], *, ignore_unknown: bool = True) -> bool | None`
- `any(self, predicate: Callable[[Cell[T]], Cell[bool | None]], *, ignore_unknown: bool = True) -> bool | None`
- `count_if(self, predicate: Callable[[Cell[T]], Cell[bool | None]], *, ignore_unknown: bool = True) -> int | None`
- `none(self, predicate: Callable[[Cell[T]], Cell[bool | None]], *, ignore_unknown: bool = True) -> bool | None`

### Missing: Transformations

- `rename(self, new_name: str) -> Column[T]`
- `transform(self, transformer: Callable[[Cell[T]], Cell[R]]) -> Column[R]`

### Missing: Statistics

- `summarize_statistics(self) -> Table`
- `correlation_with(self, other: Column) -> float`
- `distinct_value_count(self, *, ignore_missing_values: bool = True) -> int`
- `idness(self) -> float`
- `max(self) -> T | None`
- `mean(self) -> T`
- `median(self) -> T`
- `min(self) -> T | None`
- `missing_value_count(self) -> int`
- `missing_value_ratio(self) -> float`
- `mode(self, *, ignore_missing_values: bool = True) -> Sequence[T | None]`
- `stability(self) -> float`
- `standard_deviation(self) -> float`
- `variance(self) -> float`

### Missing: Export

- `to_list(self) -> list[T]`

---

## 3. `Row` (`containers/_row/`)

Empty stub. All methods and properties missing.

### Abstract interface (to be defined on `Row`)

- `__contains__(self, key: object, /) -> bool`
- `__eq__(self, other: object) -> bool`
- `__getitem__(self, name: str) -> Cell`
- `__hash__(self) -> int`
- `__iter__(self) -> Iterator[str]`
- `__len__(self) -> int`
- `__sizeof__(self) -> int`
- `column_count -> int`
- `column_names -> list[str]`
- `schema -> Schema`
- `get_cell(self, name: str) -> Cell`
- `get_column_type(self, name: str) -> DataType`
- `has_column(self, name: str) -> bool`

### Concrete `ExprRow` (lazy, builds Polars expressions)

- Delegates all operations to the underlying table
- `get_cell(name: str) -> ExprCell` — returns `ExprCell(pl.col(name))`

---

## 4. `Cell` (`containers/_cell/`)

Empty stub. All methods and properties missing.

### Type aliases (to be defined)

```python
_ConvertibleToCell = int | float | Decimal | date | time | datetime | timedelta | bool | str | bytes | Cell | None
_ConvertibleToBooleanCell = bool | Cell | None
_ConvertibleToIntCell = int | Cell | None
_ConvertibleToStringCell = str | Cell | None
```

### Missing: Static methods

- `constant(value: _PythonLiteral | None, *, type: DataType | None = None) -> Cell`
- `date(year: _ConvertibleToIntCell, month: _ConvertibleToIntCell, day: _ConvertibleToIntCell) -> Cell[date | None]`
- `datetime(year: _ConvertibleToIntCell, month: _ConvertibleToIntCell, day: _ConvertibleToIntCell, hour: _ConvertibleToIntCell, minute: _ConvertibleToIntCell, second: _ConvertibleToIntCell, *, microsecond: _ConvertibleToIntCell = 0, time_zone: str | None = None) -> Cell[datetime | None]`
- `duration(*, weeks: _ConvertibleToIntCell = 0, days: _ConvertibleToIntCell = 0, hours: _ConvertibleToIntCell = 0, minutes: _ConvertibleToIntCell = 0, seconds: _ConvertibleToIntCell = 0, milliseconds: _ConvertibleToIntCell = 0, microseconds: _ConvertibleToIntCell = 0) -> Cell[timedelta | None]`
- `time(hour: _ConvertibleToIntCell, minute: _ConvertibleToIntCell, second: _ConvertibleToIntCell, *, microsecond: _ConvertibleToIntCell = 0) -> Cell[time | None]`
- `first_not_none(cells: list[Cell[P]]) -> Cell[P | None]`

### Missing: Properties (namespaces)

- `dt -> DatetimeOperations`
- `dur -> DurationOperations`
- `math -> MathOperations`
- `str -> StringOperations`

### Missing: Boolean operations

- `not_(self) -> Cell[bool | None]`
- `and_(self, other: _ConvertibleToBooleanCell) -> Cell[bool | None]`
- `or_(self, other: _ConvertibleToBooleanCell) -> Cell[bool | None]`
- `xor(self, other: _ConvertibleToBooleanCell) -> Cell[bool | None]`

### Missing: Numeric operations

- `neg(self) -> Cell`
- `add(self, other: _ConvertibleToCell) -> Cell`
- `div(self, other: _ConvertibleToCell) -> Cell`
- `mod(self, other: _ConvertibleToCell) -> Cell`
- `mul(self, other: _ConvertibleToCell) -> Cell`
- `pow(self, other: _ConvertibleToCell) -> Cell`
- `sub(self, other: _ConvertibleToCell) -> Cell`

### Missing: Comparison operations

- `eq(self, other: _ConvertibleToCell, *, propagate_missing_values: bool = True) -> Cell[bool | None]`
- `neq(self, other: _ConvertibleToCell, *, propagate_missing_values: bool = True) -> Cell[bool | None]`
- `ge(self, other: _ConvertibleToCell) -> Cell[bool | None]`
- `gt(self, other: _ConvertibleToCell) -> Cell[bool | None]`
- `le(self, other: _ConvertibleToCell) -> Cell[bool | None]`
- `lt(self, other: _ConvertibleToCell) -> Cell[bool | None]`

### Missing: Other

- `cast(self, type: DataType) -> Cell`

### Missing: Dunder methods

- Boolean: `__invert__`, `__and__`, `__rand__`, `__or__`, `__ror__`, `__xor__`, `__rxor__`
- Comparison: `__eq__`, `__ge__`, `__gt__`, `__le__`, `__lt__`, `__ne__`
- Numeric: `__abs__`, `__ceil__`, `__floor__`, `__neg__`, `__pos__`, `__add__`, `__radd__`, `__floordiv__`, `__rfloordiv__`, `__mod__`, `__rmod__`, `__mul__`, `__rmul__`, `__pow__`, `__rpow__`, `__sub__`, `__rsub__`, `__truediv__`, `__rtruediv__`
- Other: `__hash__`, `__repr__`, `__sizeof__`, `__str__`

### Concrete `ExprCell` (lazy, builds Polars expressions)

All the above methods need `ExprCell` implementations that build `pl.Expr` lazily.

---

## 5. `Schema` (`typing/_schema.py`)

Empty stub. All methods and properties missing.

### Missing

- `__init__(self, schema: Mapping[str, DataType]) -> None`
- `_from_polars_schema(schema: pl.Schema) -> Schema`
- `__contains__(self, key: object, /) -> bool`
- `__eq__(self, other: object) -> bool`
- `__getitem__(self, key: str, /) -> DataType`
- `__hash__(self) -> int`
- `__iter__(self) -> Iterator[str]`
- `__len__(self) -> int`
- `__repr__(self) -> str`
- `__sizeof__(self) -> int`
- `__str__(self) -> str`
- `_repr_markdown_(self) -> str`
- `column_count -> int`
- `column_names -> list[str]`
- `get_column_type(self, name: str) -> DataType`
- `has_column(self, name: str) -> bool`
- `to_dict(self) -> dict[str, DataType]`

---

## 6. `StringOperations` (`query/_string_operations/`)

Empty stub. All methods missing.

- `contains(self, substring: _ConvertibleToStringCell) -> Cell[bool | None]`
- `ends_with(self, suffix: _ConvertibleToStringCell) -> Cell[bool | None]`
- `index_of(self, substring: _ConvertibleToStringCell) -> Cell[int | None]`
- `length(self, *, optimize_for_ascii: bool = False) -> Cell[int | None]`
- `pad_end(self, length: int, *, character: str = " ") -> Cell[str | None]`
- `pad_start(self, length: int, *, character: str = " ") -> Cell[str | None]`
- `remove_prefix(self, prefix: _ConvertibleToStringCell) -> Cell[str | None]`
- `remove_suffix(self, suffix: _ConvertibleToStringCell) -> Cell[str | None]`
- `repeat(self, count: _ConvertibleToIntCell) -> Cell[str | None]`
- `replace_all(self, old: _ConvertibleToStringCell, new: _ConvertibleToStringCell) -> Cell[str | None]`
- `reverse(self) -> Cell[str | None]`
- `slice(self, *, start: _ConvertibleToIntCell = 0, length: _ConvertibleToIntCell = None) -> Cell[str | None]`
- `starts_with(self, prefix: _ConvertibleToStringCell) -> Cell[bool | None]`
- `strip(self, *, characters: _ConvertibleToStringCell = None) -> Cell[str | None]`
- `strip_end(self, *, characters: _ConvertibleToStringCell = None) -> Cell[str | None]`
- `strip_start(self, *, characters: _ConvertibleToStringCell = None) -> Cell[str | None]`
- `to_date(self, *, format: str | None = "iso") -> Cell[date | None]`
- `to_datetime(self, *, format: str | None = "iso") -> Cell[datetime | None]`
- `to_float(self) -> Cell[float | None]`
- `to_int(self, *, base: _ConvertibleToIntCell = 10) -> Cell[int | None]`
- `to_lowercase(self) -> Cell[str | None]`
- `to_time(self, *, format: str | None = "iso") -> Cell[time | None]`
- `to_uppercase(self) -> Cell[str | None]`

---

## 7. `DatetimeOperations` (`query/_datetime_operations/`)

Empty stub. All methods missing.

### Extract component

- `century(self) -> Cell[int | None]`
- `date(self) -> Cell[date | None]`
- `day(self) -> Cell[int | None]`
- `day_of_week(self) -> Cell[int | None]`
- `day_of_year(self) -> Cell[int | None]`
- `hour(self) -> Cell[int | None]`
- `microsecond(self) -> Cell[int | None]`
- `millennium(self) -> Cell[int | None]`
- `millisecond(self) -> Cell[int | None]`
- `minute(self) -> Cell[int | None]`
- `month(self) -> Cell[int | None]`
- `quarter(self) -> Cell[int | None]`
- `second(self) -> Cell[int | None]`
- `time(self) -> Cell[time | None]`
- `week(self) -> Cell[int | None]`
- `year(self) -> Cell[int | None]`

### Other

- `is_in_leap_year(self) -> Cell[bool | None]`
- `replace(self, *, year: _ConvertibleToIntCell = None, month: _ConvertibleToIntCell = None, day: _ConvertibleToIntCell = None, hour: _ConvertibleToIntCell = None, minute: _ConvertibleToIntCell = None, second: _ConvertibleToIntCell = None, microsecond: _ConvertibleToIntCell = None) -> Cell`
- `to_string(self, *, format: str = "iso") -> Cell[str | None]`
- `unix_timestamp(self, *, unit: Literal["s", "ms", "us"] = "s") -> Cell[int | None]`

---

## 8. `DurationOperations` (`query/_duration_operations/`)

Empty stub. All methods missing.

- `abs(self) -> Cell[timedelta | None]`
- `full_weeks(self) -> Cell[int | None]`
- `full_days(self) -> Cell[int | None]`
- `full_hours(self) -> Cell[int | None]`
- `full_minutes(self) -> Cell[int | None]`
- `full_seconds(self) -> Cell[int | None]`
- `full_milliseconds(self) -> Cell[int | None]`
- `full_microseconds(self) -> Cell[int | None]`
- `to_string(self, *, format: Literal["iso", "pretty"] = "iso") -> Cell[str | None]`

---

## 9. `MathOperations` (`query/_math_operations/`)

Empty stub. All methods missing.

- `abs(self) -> Cell`
- `acos(self) -> Cell`
- `acosh(self) -> Cell`
- `asin(self) -> Cell`
- `asinh(self) -> Cell`
- `atan(self) -> Cell`
- `atanh(self) -> Cell`
- `cbrt(self) -> Cell`
- `ceil(self) -> Cell`
- `cos(self) -> Cell`
- `cosh(self) -> Cell`
- `degrees_to_radians(self) -> Cell`
- `exp(self) -> Cell`
- `floor(self) -> Cell`
- `ln(self) -> Cell`
- `log(self, base: float) -> Cell`
- `log10(self) -> Cell`
- `radians_to_degrees(self) -> Cell`
- `round_to_decimal_places(self, decimal_places: int) -> Cell`
- `round_to_significant_figures(self, significant_figures: int) -> Cell`
- `sign(self) -> Cell`
- `sin(self) -> Cell`
- `sinh(self) -> Cell`
- `sqrt(self) -> Cell`
- `tan(self) -> Cell`
- `tanh(self) -> Cell`

---

## 10. IO — `TableReader` (`io/_table_reader.py`)

Empty stub. All methods missing.

- `csv_file(path: str | Path, *, separator: str = ",") -> Table`
- `json_file(path: str | Path) -> Table`
- `parquet_file(path: str | Path) -> Table`

---

## 11. IO — `TableWriter` (`io/_table_writer.py`)

Has `__init__` only. All write methods missing.

- `csv_file(self, path: str | Path) -> None`
- `json_file(self, path: str | Path) -> None`
- `parquet_file(self, path: str | Path) -> None`

---

## 12. Plotters (`plotting/`)

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

Noted as missing in `_data_type.py` TODOs:

- `Decimal(precision: int, scale: int) -> DataType`
- `Array(inner: DataType, width: int) -> DataType`
- `List(inner: DataType) -> DataType`
- `Struct(fields: list[tuple[str, DataType]]) -> DataType`
- `Categorical() -> DataType`
- `Enum(categories: list[str]) -> DataType`
- `Object() -> DataType`
- `Unknown() -> DataType`
