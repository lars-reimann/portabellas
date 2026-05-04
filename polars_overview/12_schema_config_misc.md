# Schema, Config, and Miscellaneous

## Schema

### `Schema`
A mapping from column names to data types. Inherits from `OrderedDict[str, PolarsDataType]`.

#### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `from_dict` | `(data: dict[str, PolarsDataType]) -> Schema` | Create from a dictionary. |
| `from_names_and_dtypes` | `(names: Sequence[str], dtypes: Sequence[PolarsDataType]) -> Schema` | Create from parallel sequences. |
| `to_python` | `() -> dict[str, type]` | Convert to Python types. |
| `len` | `() -> int` | Get the number of columns. |
| `names` | `() -> list[str]` | Get the column names. |
| `dtypes` | `() -> list[PolarsDataType]` | Get the data types. |
| `equals` | `(other: Schema, *, check_dtypes: bool = True, check_names: bool = True, check_order: bool = True) -> bool` | Check equality. |

---

## Config

### `Config`
Configuration options for Polars behavior. Accessed via `pl.Config`.

#### Methods (Selection)

| Method | Signature | Description |
|--------|-----------|-------------|
| `set_ascii_tables` | `(active: bool = True) -> type[Config]` | Use ASCII for table display. |
| `set_auto_structify` | `(active: bool = True) -> type[Config]` | Auto-structify multi-output expressions. |
| `set_fmt_str_lengths` | `(n: int) -> type[Config]` | Set string display length. |
| `set_float_fmt` | `(fmt: str) -> type[Config]` | Set float display format. |
| `set_float_precision` | `(n: int) -> type[Config]` | Set float precision. |
| `set_thousands_separator` | `(sep: str | None) -> type[Config]` | Set thousands separator. |
| `set_streaming_chunk_size` | `(chunk_size: int) -> type[Config]` | Set chunk size for streaming. |
| `set_tbl_cell_alignment` | `(alignment: str) -> type[Config]` | Set table cell alignment. |
| `set_tbl_cols` | `(n: int) -> type[Config]` | Set number of columns to display. |
| `set_tbl_column_data_type` | `(value: str) -> type[Config]` | Set column data type display. |
| `set_tbl_dataframe_shape_below` | `(active: bool = True) -> type[Config]` | Show shape below the table. |
| `set_tbl_formatting` | `(format: str) -> type[Config]` | Set table formatting. |
| `set_tbl_hide_column_data_types` | `(active: bool = True) -> type[Config]` | Hide column data types. |
| `set_tbl_hide_column_names` | `(active: bool = True) -> type[Config]` | Hide column names. |
| `set_tbl_hide_dataframe_shape` | `(active: bool = True) -> type[Config]` | Hide dataframe shape. |
| `set_tbl_rows` | `(n: int) -> type[Config]` | Set number of rows to display. |
| `set_tbl_row_sizing` | `(value: str) -> type[Config]` | Set row sizing strategy. |
| `set_verbose` | `(active: bool = True) -> type[Config]` | Enable verbose logging. |
| `load_from_env` | `() -> None` | Load config from environment variables. |
| `save_to_env` | `(scope: str = "global") -> None` | Save config to environment variables. |

---

## SQLContext

### `SQLContext(*, frames: dict[str, DataFrame | LazyFrame] | None = None, register_globals: bool = False, search_path: str | Sequence[str] | None = None)`

Execute SQL queries against DataFrames.

#### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `execute` | `(query: str) -> LazyFrame` | Execute a SQL query. |
| `get_tables` | `() -> list[str]` | Get registered table names. |
| `register` | `(name: str, frame: DataFrame | LazyFrame | None = None) -> SQLContext | None` | Register a DataFrame as a table. |
| `register_many` | `(frames: dict[str, DataFrame | LazyFrame] | None = None, **named_frames: DataFrame | LazyFrame) -> SQLContext` | Register multiple DataFrames. |
| `unregister` | `(names: str | Sequence[str]) -> SQLContext` | Unregister tables. |
| `update` | `(other: SQLContext) -> SQLContext` | Update with tables from another context. |
| `tables` | `() -> list[str]` | List registered table names. |

---

## StringCache

### `StringCache`
Context manager for using a global string cache for categorical values.

#### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `__enter__` | `() -> StringCache` | Enter the context. |
| `__exit__` | `(*args: Any) -> None` | Exit the context. |

#### Usage

```python
with pl.StringCache():
    # Categorical values created here share the same global cache
    df1 = pl.DataFrame({"cat": pl.Series(["a", "b", "c"], dtype=pl.Categorical)})
    df2 = pl.DataFrame({"cat": pl.Series(["b", "c", "d"], dtype=pl.Categorical)})
```

---

## Selectors

### `selectors`
Column selection helpers (accessed via `pl.selectors` or `cs`).

#### Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `all` | `() -> Selector` | Select all columns. |
| `binary` | `() -> Selector` | Select Binary columns. |
| `boolean` | `() -> Selector` | Select Boolean columns. |
| `by_name` | `(*names: str | Sequence[str], require_all: bool = True) -> Selector` | Select by column name. |
| `by_dtype` | `(*dtypes: PolarsDataType | Collection[PolarsDataType]) -> Selector` | Select by data type. |
| `categorical` | `() -> Selector` | Select Categorical columns. |
| `contains` | `(substring: str) -> Selector` | Select columns containing a substring. |
| `date` | `() -> Selector` | Select Date columns. |
| `datetime` | `(*time_units: TimeUnit | None, time_zones: str | Sequence[str] | None = None) -> Selector` | Select Datetime columns. |
| `decimal` | `() -> Selector` | Select Decimal columns. |
| `duration` | `(*time_units: TimeUnit | None) -> Selector` | Select Duration columns. |
| `ends_with` | `(*suffixes: str) -> Selector` | Select columns ending with suffixes. |
| `exclude` | `(*selectors: Selector | str | PolarsDataType | Collection[PolarsDataType]) -> Selector` | Exclude columns. |
| `first` | `() -> Selector` | Select the first column. |
| `float` | `() -> Selector` | Select Float columns. |
| `integer` | `() -> Selector` | Select Integer columns. |
| `last` | `() -> Selector` | Select the last column. |
| `matches` | `(pattern: str) -> Selector` | Select columns matching a regex. |
| `numeric` | `() -> Selector` | Select numeric columns. |
| `signed_integer` | `() -> Selector` | Select signed integer columns. |
| `starts_with` | `(*prefixes: str) -> Selector` | Select columns starting with prefixes. |
| `string` | `(*, include_categorical: bool = False) -> Selector` | Select String columns. |
| `struct` | `() -> Selector` | Select Struct columns. |
| `temporal` | `() -> Selector` | Select temporal columns. |
| `time` | `() -> Selector` | Select Time columns. |
| `unsigned_integer` | `() -> Selector` | Select unsigned integer columns. |

Selectors support set operations: `|` (union), `&` (intersection), `~` (complement).

---

## CompatLevel

### `CompatLevel`
Compatibility level for serialization formats.

#### Values

| Value | Description |
|-------|-------------|
| `newest` | Use the newest features. |
| `oldest` | Use the oldest compatible features. |

#### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `from_version` | `(version: int) -> CompatLevel` | Create from a version number. |

---

## QueryOptFlags

### `QueryOptFlags(*, type_coercion: bool = True, predicate_pushdown: bool = True, projection_pushdown: bool = True, simplify_expression: bool = True, slice_pushdown: bool = True, comm_subplan_elim: bool = True, comm_subexpr_elim: bool = True, cluster_with_key: bool = True, collapse_joins: bool = True, streaming: bool = False, _eager: bool = False)`

Flags to control query optimization.

---

## GPUEngine

### `GPUEngine(*, engine: str | None = None, raise_on_fail: bool = True, config: dict[str, Any] | None = None)`

Configuration for GPU-accelerated query execution.

---

## Exceptions

| Exception | Description |
|-----------|-------------|
| `PolarsError` | Base exception for Polars errors. |
| `ColumnNotFoundError` | Column does not exist. |
| `ComputeError` | Error during computation. |
| `DuplicateError` | Duplicate column/label. |
| `InvalidOperationError` | Invalid operation for the given data type. |
| `NoDataError` | No data available. |
| `OutOfBoundsError` | Index out of bounds. |
| `SchemaError` | Schema mismatch. |
| `ShapeError` | Shape mismatch. |
| `StringCacheMismatchError` | String cache mismatch between categoricals. |
| `StructFieldNotFoundError` | Struct field not found. |
| `UnmappedSubtreeError` | Unmapped subtree during conversion. |
| `CategoricalRemappingWarning` | Warning when categorical remapping occurs. |
| `PerformanceWarning` | Warning about performance issues. |
| `ChronoFormatWarning` | Warning about chrono format parsing. |
| `PolarsWarning` | Base warning for Polars. |
| `PolarsPanicError` | Internal panic (bug in Polars). |

---

## Meta Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `get_index_type` | `() -> PolarsDataType` | Get the index data type. |
| `thread_pool_size` | `() -> int` | Get the Polars thread pool size. |
| `set_float_fmt` | `(fmt: str) -> None` | Set float formatting. |
| `set_fmt_str_lengths` | `(n: int) -> None` | Set string display length. |
| `set_thousands_separator` | `(sep: str | None) -> None` | Set thousands separator. |
| `show_versions` | `() -> None` | Print version information. |
| `get_float_fmt` | `() -> str` | Get the current float format. |

---

## Convert Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `from_arrow` | `(a: ArrowArray | ArrowTable | ArrowChunked | Sequence[ArrowArray], *, schema: SchemaDict | None = None, rechunk: bool = True) -> DataFrame | Series` | Convert from Arrow. |
| `from_dataframe` | `(df: Any, *, allow_zero_copy: bool = False, rechunk: bool = True) -> DataFrame` | Convert from a DataFrame interchange object. |
| `from_dict` | `(data: dict[str, Sequence[object] | Series | Expr], *, schema: SchemaDict | Schema | None = None, schema_overrides: SchemaDict | None = None, strict: bool = True, nan_to_null: bool = False) -> DataFrame` | Create from a dictionary. |
| `from_dicts` | `(data: Sequence[dict[str, Any]], *, schema: SchemaDict | Schema | None = None, schema_overrides: SchemaDict | None = None, strict: bool = True, infer_schema_length: int | None = 50) -> DataFrame` | Create from a sequence of dicts. |
| `from_records` | `(data: Sequence[Sequence[Any]] | numpy.ndarray[Any, Any], *, schema: SchemaDict | Schema | None = None, schema_overrides: SchemaDict | None = None, orient: Orientation | None = None, infer_schema_length: int | None = 50) -> DataFrame` | Create from records. |
| `from_pandas` | `(data: pandas.DataFrame | pandas.Series | pandas.Index, *, schema: SchemaDict | None = None, schema_overrides: SchemaDict | None = None, rechunk: bool = True, nan_to_null: bool = True, include_index: bool = False) -> DataFrame | Series` | Convert from pandas. |
| `from_raw` | `(raw: RawFrame, *, schema: Schema | None = None) -> DataFrame` | Create from a raw frame. |
| `from_numpy` | `(data: numpy.ndarray[Any, Any], *, schema: SchemaDict | Schema | None = None, schema_overrides: SchemaDict | None = None, orient: Orientation | None = None) -> DataFrame` | Create from a NumPy array. |

---

## Catalog

### `DatabaseCatalog`
Catalog for managing database connections and table registrations.

---

## API Namespace Registration

Polars allows registering custom namespaces on `Series`, `DataFrame`, and `LazyFrame`.

### `register_series_namespace(name: str) -> Callable[[type], type]`
Decorator to register a custom Series namespace.

### `register_dataframe_namespace(name: str) -> Callable[[type], type]`
Decorator to register a custom DataFrame namespace.

### `register_lazyframe_namespace(name: str) -> Callable[[type], type]`
Decorator to register a custom LazyFrame namespace.
