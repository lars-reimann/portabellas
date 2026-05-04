# DataFrame

## Constructor

### `__init__(data: FrameInitTypes | None = None, schema: SchemaDefinition | None = None, *, schema_overrides: SchemaDict | None = None, strict: bool = True, orient: Orientation | None = None, infer_schema_length: int | None = N_INFER_DEFAULT, nan_to_null: bool = False, height: int | None = None) -> None`
Two-dimensional data structure representing data as a table with rows and columns.

## Class Methods

### `deserialize(source: str | bytes | Path | IOBase, *, format: SerializationFormat = "binary") -> DataFrame`
Read a serialized DataFrame from a file.

## Properties

### `columns -> list[str]`
Get or set column names.

### `dtypes -> list[DataType]`
Get the column data types.

### `flags -> dict[str, dict[str, bool]]`
Get flags that are set on the columns of this DataFrame.

### `height -> int`
Get the number of rows.

### `plot -> DataFramePlot`
Create a plot namespace.

### `schema -> Schema`
Get an ordered mapping of column names to their data type.

### `shape -> tuple[int, int]`
Get the shape of the DataFrame.

### `style -> GT`
Create a Great Table for styling.

### `width -> int`
Get the number of columns.

## Dunder Methods

### `__add__(other: DataFrame | Series | int | float | bool | str) -> DataFrame`
Arithmetic addition.

### `__array__(dtype: npt.DTypeLike | None = None, copy: bool | None = None) -> np.ndarray[Any, Any]`
Return a NumPy ndarray with the given data type.

### `__arrow_c_stream__(requested_schema: object | None = None) -> object`
Export a DataFrame via the Arrow PyCapsule Interface.

### `__bool__() -> NoReturn`
Truth value is ambiguous.

### `__contains__(key: str) -> bool`
Check membership.

### `__copy__() -> DataFrame`
Return a copy.

### `__dataframe__(nan_as_null: bool = False, allow_copy: bool = True) -> PolarsDataFrame`
Convert to a dataframe object implementing the dataframe interchange protocol.

### `__deepcopy__(memo: None = None) -> DataFrame`
Return a deep copy.

### `__eq__(other: object) -> DataFrame`
Equality comparison.

### `__floordiv__(other: DataFrame | Series | int | float) -> DataFrame`
Floor division.

### `__ge__(other: Any) -> DataFrame`
Greater-than-or-equal comparison.

### `__getitem__(key: SingleIndexSelector | SingleColSelector | MultiColSelector | MultiIndexSelector | tuple[...]) -> DataFrame | Series | Any`
Get part of the DataFrame as a new DataFrame, Series, or scalar.

### `__gt__(other: Any) -> DataFrame`
Greater-than comparison.

### `__iter__() -> Iterator[Series]`
Iterate over columns.

### `__le__(other: Any) -> DataFrame`
Less-than-or-equal comparison.

### `__len__() -> int`
Return the number of rows.

### `__lt__(other: Any) -> DataFrame`
Less-than comparison.

### `__mod__(other: DataFrame | Series | int | float) -> DataFrame`
Modulo.

### `__mul__(other: DataFrame | Series | int | float) -> DataFrame`
Multiplication.

### `__ne__(other: object) -> DataFrame`
Inequality comparison.

### `__radd__(other: DataFrame | Series | int | float | bool | str) -> DataFrame`
Reflected addition.

### `__repr__() -> str`
Return string representation.

### `__reversed__() -> Iterator[Series]`
Reverse iterate over columns.

### `__rmul__(other: int | float) -> DataFrame`
Reflected multiplication.

### `__setitem__(key: str | Sequence[int] | Sequence[str] | tuple[Any, str | int], value: Any) -> None`
Modify DataFrame elements in place, using assignment syntax.

### `__sub__(other: DataFrame | Series | int | float) -> DataFrame`
Subtraction.

### `__truediv__(other: DataFrame | Series | int | float) -> DataFrame`
True division.

## Instance Methods (Alphabetical)

### `approx_n_unique() -> DataFrame`
Approximate count of unique values.

### `bottom_k(k: int, *, by: IntoExpr | Iterable[IntoExpr], reverse: bool | Sequence[bool] = False) -> DataFrame`
Return the `k` smallest rows.

### `cast(dtypes: Mapping[ColumnNameOrSelector | PolarsDataType, PolarsDataType | PythonDataType] | PolarsDataType | Schema, *, strict: bool = True) -> DataFrame`
Cast DataFrame column(s) to the specified dtype(s).

### `clear(n: int = 0) -> DataFrame`
Create an empty (n=0) or `n`-row null-filled (n>0) copy of the DataFrame.

### `clone() -> DataFrame`
Create a copy of this DataFrame.

### `collect_schema() -> Schema`
Get an ordered mapping of column names to their data type.

### `corr(*, label: str | None = None, **kwargs: Any) -> DataFrame`
Return pairwise Pearson product-moment correlation coefficients between columns.

### `count() -> DataFrame`
Return the number of non-null elements for each column.

### `describe(percentiles: Sequence[float] | float | None = (0.25, 0.50, 0.75), *, interpolation: QuantileMethod = "nearest") -> DataFrame`
Summary statistics for a DataFrame.

### `drop(*columns: ColumnNameOrSelector | Iterable[ColumnNameOrSelector], strict: bool = True) -> DataFrame`
Remove columns from the dataframe.

### `drop_in_place(name: str) -> Series`
Drop a single column in-place and return the dropped column.

### `drop_nans(subset: ColumnNameOrSelector | Collection[ColumnNameOrSelector] | None = None) -> DataFrame`
Drop all rows that contain one or more NaN values.

### `drop_nulls(subset: ColumnNameOrSelector | Collection[ColumnNameOrSelector] | None = None) -> DataFrame`
Drop all rows that contain one or more null values.

### `equals(other: DataFrame, *, null_equal: bool = True) -> bool`
Check whether the DataFrame is equal to another DataFrame.

### `estimated_size(unit: SizeUnit = "b") -> int | float`
Return an estimation of the total (heap) allocated size of the `DataFrame`.

### `explode(columns: ColumnNameOrSelector | Iterable[ColumnNameOrSelector], *more_columns: ColumnNameOrSelector, empty_as_null: bool = True, keep_nulls: bool = True) -> DataFrame`
Explode the dataframe to long format by exploding the given columns.

### `extend(other: DataFrame) -> DataFrame`
Extend the memory backed by this `DataFrame` with the values from `other`.

### `fill_nan(value: Expr | int | float | None) -> DataFrame`
Fill floating point NaN values by an Expression evaluation.

### `fill_null(value: Any | Expr | None = None, strategy: FillNullStrategy | None = None, limit: int | None = None, *, matches_supertype: bool = True) -> DataFrame`
Fill null values using the specified value or strategy.

### `filter(*predicates: IntoExprColumn | Iterable[IntoExprColumn] | bool | list[bool] | np.ndarray[Any, Any], **constraints: Any) -> DataFrame`
Filter rows, retaining those that match the given predicate expression(s).

### `fold(operation: Callable[[Series, Series], Series]) -> Series`
Apply a horizontal reduction on a DataFrame.

### `gather_every(n: int, offset: int = 0) -> DataFrame`
Take every nth row in the DataFrame and return as a new DataFrame.

### `get_column(name: str, *, default: Any | NoDefault = NO_DEFAULT) -> Series | Any`
Get a single column by name.

### `get_column_index(name: str) -> int`
Find the index of a column by name.

### `get_columns() -> list[Series]`
Get the DataFrame as a List of Series.

### `glimpse(*, max_items_per_column: int = 10, max_colname_length: int = 50, return_type: Literal["frame", "self", "string"] | None = None) -> str | DataFrame | None`
Return a dense preview of the DataFrame.

### `group_by(*by: IntoExpr | Iterable[IntoExpr], maintain_order: bool = False, **named_by: IntoExpr) -> GroupBy`
Start a group by operation.

### `group_by_dynamic(index_column: IntoExpr, *, every: str | timedelta, period: str | timedelta | None = None, offset: str | timedelta | None = None, include_boundaries: bool = False, closed: ClosedInterval = "left", label: Label = "left", group_by: IntoExpr | Iterable[IntoExpr] | None = None, start_by: StartBy = "window") -> DynamicGroupBy`
Group based on a time value (or index value of type Int32, Int64).

### `hash_rows(seed: int = 0, seed_1: int | None = None, seed_2: int | None = None, seed_3: int | None = None) -> Series`
Hash and combine the rows in this DataFrame.

### `head(n: int = 5) -> DataFrame`
Get the first `n` rows.

### `hstack(columns: list[Series] | DataFrame, *, in_place: bool = False) -> DataFrame`
Return a new DataFrame grown horizontally by stacking multiple Series to it.

### `insert_column(index: int, column: IntoExprColumn) -> DataFrame`
Insert a Series (or expression) at a certain column index.

### `interpolate() -> DataFrame`
Interpolate intermediate values.

### `is_duplicated() -> Series`
Get a mask of all duplicated rows in this DataFrame.

### `is_empty() -> bool`
Returns `True` if the DataFrame contains no rows.

### `is_unique() -> Series`
Get a mask of all unique rows in this DataFrame.

### `item(row: int | None = None, column: int | str | None = None) -> Any`
Return the DataFrame as a scalar, or return the element at the given row/column.

### `iter_columns() -> Iterator[Series]`
Returns an iterator over the columns of this DataFrame.

### `iter_rows(*, named: bool = False, buffer_size: int = 512) -> Iterator[tuple[Any, ...]] | Iterator[dict[str, Any]]`
Returns an iterator over the DataFrame of rows of python-native values.

### `iter_slices(n_rows: int = 10_000) -> Iterator[DataFrame]`
Returns a non-copying iterator of slices over the underlying DataFrame.

### `join(other: DataFrame, on: str | Expr | Sequence[str | Expr] | None = None, how: JoinStrategy = "inner", *, left_on: str | Expr | Sequence[str | Expr] | None = None, right_on: str | Expr | Sequence[str | Expr] | None = None, suffix: str = "_right", validate: JoinValidation = "m:m", nulls_equal: bool = False, coalesce: bool | None = None, maintain_order: MaintainOrderJoin | None = None) -> DataFrame`
Join in SQL-like fashion.

### `join_asof(other: DataFrame, *, left_on: str | None | Expr = None, right_on: str | None | Expr = None, on: str | None | Expr = None, by_left: str | Sequence[str] | None = None, by_right: str | Sequence[str] | None = None, by: str | Sequence[str] | None = None, strategy: AsofJoinStrategy = "backward", suffix: str = "_right", tolerance: str | int | float | timedelta | None = None, allow_parallel: bool = True, force_parallel: bool = False, coalesce: bool = True, allow_exact_matches: bool = True, check_sortedness: bool = True) -> DataFrame`
Perform an asof join.

### `join_where(other: DataFrame, *predicates: Expr | Iterable[Expr], suffix: str = "_right") -> DataFrame`
Perform a join based on one or multiple (in)equality predicates.

### `lazy() -> LazyFrame`
Start a lazy query from this point.

### `limit(n: int = 5) -> DataFrame`
Get the first `n` rows.

### `map_columns(column_names: str | Sequence[str] | pl.Selector, function: Callable[Concatenate[Series, P], Series], *args: P.args, **kwargs: P.kwargs) -> DataFrame`
Apply eager functions to columns of a DataFrame.

### `map_rows(function: Callable[[tuple[Any, ...]], Any], return_dtype: PolarsDataType | None = None, *, inference_size: int = 256) -> DataFrame`
Apply a custom/user-defined function (UDF) over the rows of the DataFrame.

### `match_to_schema(schema: SchemaDict | Schema, *, missing_columns: Literal["insert", "raise"] | Mapping[str, Literal["insert", "raise"] | Expr] = "raise", missing_struct_fields: Literal["insert", "raise"] | Mapping[str, Literal["insert", "raise"]] = "raise", extra_columns: Literal["ignore", "raise"] = "raise", extra_struct_fields: Literal["ignore", "raise"] | Mapping[str, Literal["ignore", "raise"]] = "raise", integer_cast: Literal["upcast", "forbid"] | Mapping[str, Literal["upcast", "forbid"]] = "forbid", float_cast: Literal["upcast", "forbid"] | Mapping[str, Literal["upcast", "forbid"]] = "forbid") -> DataFrame`
Match or evolve the schema of a LazyFrame into a specific schema.

### `max() -> DataFrame`
Aggregate the columns of this DataFrame to their maximum value.

### `max_horizontal() -> Series`
Get the maximum value horizontally across columns.

### `mean() -> DataFrame`
Aggregate the columns of this DataFrame to their mean value.

### `mean_horizontal(*, ignore_nulls: bool = True) -> Series`
Take the mean of all values horizontally across columns.

### `melt(id_vars: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None = None, value_vars: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None = None, variable_name: str | None = None, value_name: str | None = None) -> DataFrame` *(deprecated)*
Unpivot a DataFrame from wide to long format.

### `median() -> DataFrame`
Aggregate the columns of this DataFrame to their median value.

### `merge_sorted(other: DataFrame, key: str, *, maintain_order: bool = False) -> DataFrame`
Take two sorted DataFrames and merge them by the sorted key.

### `min() -> DataFrame`
Aggregate the columns of this DataFrame to their minimum value.

### `min_horizontal() -> Series`
Get the minimum value horizontally across columns.

### `n_chunks(strategy: Literal["first", "all"] = "first") -> int | list[int]`
Get number of chunks used by the ChunkedArrays of this DataFrame.

### `n_unique(subset: str | Expr | Sequence[str | Expr] | None = None) -> int`
Return the number of unique rows, or the number of unique row-subsets.

### `null_count() -> DataFrame`
Create a new DataFrame that shows the null counts per column.

### `partition_by(by: ColumnNameOrSelector | Sequence[ColumnNameOrSelector], *more_by: ColumnNameOrSelector, maintain_order: bool = True, include_key: bool = True, as_dict: bool = False) -> list[DataFrame] | dict[tuple[Any, ...], DataFrame]`
Group by the given columns and return the groups as separate dataframes.

### `pipe(function: Callable[Concatenate[DataFrame, P], T], *args: P.args, **kwargs: P.kwargs) -> T`
Offers a structured way to apply a sequence of user-defined functions (UDFs).

### `pivot(on: ColumnNameOrSelector | Sequence[ColumnNameOrSelector], on_columns: Sequence[Any] | pl.Series | pl.DataFrame | None = None, *, index: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None = None, values: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None = None, aggregate_function: PivotAgg | Expr | None = None, maintain_order: bool = True, sort_columns: bool = False, separator: str = "_", column_naming: Literal["auto", "combine"] = "auto") -> DataFrame`
Create a spreadsheet-style pivot table as a DataFrame.

### `product() -> DataFrame`
Aggregate the columns of this DataFrame to their product values.

### `quantile(quantile: float, interpolation: QuantileMethod = "nearest") -> DataFrame`
Aggregate the columns of this DataFrame to their quantile value.

### `rechunk() -> DataFrame`
Rechunk the data in this DataFrame to a contiguous allocation.

### `remove(*predicates: IntoExprColumn | Iterable[IntoExprColumn] | bool | list[bool] | np.ndarray[Any, Any], **constraints: Any) -> DataFrame`
Remove rows, dropping those that match the given predicate expression(s).

### `rename(mapping: Mapping[str, str] | Callable[[str], str], *, strict: bool = True) -> DataFrame`
Rename column names.

### `replace_column(index: int, column: Series) -> DataFrame`
Replace a column at an index location.

### `reverse() -> DataFrame`
Reverse the DataFrame.

### `rolling(index_column: IntoExpr, *, period: str | timedelta, offset: str | timedelta | None = None, closed: ClosedInterval = "right", group_by: IntoExpr | Iterable[IntoExpr] | None = None) -> RollingGroupBy`
Create rolling groups based on a temporal or integer column.

### `row(index: int | None = None, *, by_predicate: Expr | None = None, named: bool = False) -> tuple[Any, ...] | dict[str, Any]`
Get the values of a single row, either by index or by predicate.

### `rows(*, named: bool = False) -> list[tuple[Any, ...]] | list[dict[str, Any]]`
Returns all data in the DataFrame as a list of rows of python-native values.

### `rows_by_key(key: ColumnNameOrSelector | Sequence[ColumnNameOrSelector], *, named: bool = False, include_key: bool = False, unique: bool = False) -> dict[Any, Any]`
Returns all data as a dictionary of python-native values keyed by some column.

### `sample(n: int | Series | None = None, *, fraction: float | Series | None = None, with_replacement: bool = False, shuffle: bool = False, seed: int | None = None) -> DataFrame`
Sample from this DataFrame.

### `select(*exprs: IntoExpr | Iterable[IntoExpr], **named_exprs: IntoExpr) -> DataFrame`
Select columns from this DataFrame.

### `select_seq(*exprs: IntoExpr | Iterable[IntoExpr], **named_exprs: IntoExpr) -> DataFrame`
Select columns from this DataFrame.

### `serialize(file: IOBase | str | Path | None = None, *, format: SerializationFormat = "binary") -> bytes | str | None`
Serialize this DataFrame to a file or string in JSON format.

### `set_sorted(column: str, *, descending: bool = False, nulls_last: bool = False) -> DataFrame`
Flag a column as sorted.

### `shift(n: int = 1, *, fill_value: IntoExpr | None = None) -> DataFrame`
Shift values by the given number of indices.

### `show(limit: int | None = 5, *, ascii_tables: bool | None = None, decimal_separator: str | None = None, thousands_separator: str | bool | None = None, float_precision: int | None = None, fmt_float: FloatFmt | None = None, fmt_str_lengths: int | None = None, fmt_table_cell_list_len: int | None = None, tbl_cell_alignment: Alignment | None = None, tbl_cell_numeric_alignment: Alignment | None = None, tbl_cols: int | None = None, tbl_column_data_type_inline: bool | None = None, tbl_dataframe_shape_below: bool | None = None, tbl_formatting: TableFormatNames | None = None, tbl_hide_column_data_types: bool | None = None, tbl_hide_column_names: bool | None = None, tbl_hide_dtype_separator: bool | None = None, tbl_hide_dataframe_shape: bool | None = None, tbl_width_chars: int | None = None, trim_decimal_zeros: bool | None = True) -> None`
Show the first `n` rows.

### `shrink_to_fit(*, in_place: bool = False) -> DataFrame`
Shrink DataFrame memory usage.

### `slice(offset: int, length: int | None = None) -> DataFrame`
Get a slice of this DataFrame.

### `sort(by: IntoExpr | Iterable[IntoExpr], *more_by: IntoExpr, descending: bool | Sequence[bool] = False, nulls_last: bool | Sequence[bool] = False, multithreaded: bool = True, maintain_order: bool = False) -> DataFrame`
Sort the dataframe by the given columns.

### `sql(query: str, *, table_name: str = "self") -> DataFrame`
Execute a SQL query against the DataFrame.

### `std(ddof: int = 1) -> DataFrame`
Aggregate the columns of this DataFrame to their standard deviation value.

### `sum() -> DataFrame`
Aggregate the columns of this DataFrame to their sum value.

### `sum_horizontal(*, ignore_nulls: bool = True) -> Series`
Sum all values horizontally across columns.

### `tail(n: int = 5) -> DataFrame`
Get the last `n` rows.

### `to_arrow(*, compat_level: CompatLevel | None = None) -> pa.Table`
Collect the underlying arrow arrays in an Arrow Table.

### `to_dict(*, as_series: bool = True) -> dict[str, Series] | dict[str, list[Any]]`
Convert DataFrame to a dictionary mapping column name to values.

### `to_dummies(columns: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None = None, *, separator: str = "_", drop_first: bool = False, drop_nulls: bool = False) -> DataFrame`
Convert categorical variables into dummy/indicator variables.

### `to_dicts() -> list[dict[str, Any]]`
Convert every row to a dictionary of Python-native values.

### `to_init_repr(n: int = 1000) -> str`
Convert DataFrame to instantiable string representation.

### `to_jax(return_type: JaxExportType = "array", *, device: jax.Device | str | None = None, label: str | Expr | Sequence[str | Expr] | None = None, features: str | Expr | Sequence[str | Expr] | None = None, dtype: PolarsDataType | None = None, order: IndexOrder = "fortran") -> jax.Array | dict[str, jax.Array]`
Convert DataFrame to a Jax Array, or dict of Jax Arrays.

### `to_numpy(*, order: IndexOrder = "fortran", writable: bool = False, allow_copy: bool = True, structured: bool = False, use_pyarrow: bool | None = None) -> np.ndarray[Any, Any]`
Convert this DataFrame to a NumPy ndarray.

### `to_pandas(*, use_pyarrow_extension_array: bool = False, **kwargs: Any) -> pd.DataFrame`
Convert this DataFrame to a pandas DataFrame.

### `to_series(index: int = 0) -> Series`
Select column as Series at index location.

### `to_struct(name: str = "") -> Series`
Convert a `DataFrame` to a `Series` of type `Struct`.

### `to_torch(return_type: TorchExportType = "tensor", *, label: str | Expr | Sequence[str | Expr] | None = None, features: str | Expr | Sequence[str | Expr] | None = None, dtype: PolarsDataType | None = None) -> torch.Tensor | dict[str, torch.Tensor] | PolarsDataset`
Convert DataFrame to a PyTorch Tensor, Dataset, or dict of Tensors.

### `top_k(k: int, *, by: IntoExpr | Iterable[IntoExpr], reverse: bool | Sequence[bool] = False) -> DataFrame`
Return the `k` largest rows.

### `transpose(*, include_header: bool = False, header_name: str = "column", column_names: str | Iterable[str] | None = None) -> DataFrame`
Transpose a DataFrame over the diagonal.

### `unique(subset: IntoExpr | Collection[IntoExpr] | None = None, *, keep: UniqueKeepStrategy = "any", maintain_order: bool = False) -> DataFrame`
Drop duplicate rows from this DataFrame.

### `unnest(columns: ColumnNameOrSelector | Collection[ColumnNameOrSelector] | None = None, *more_columns: ColumnNameOrSelector, separator: str | None = None) -> DataFrame`
Decompose struct columns into separate columns for each of their fields.

### `unpivot(on: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None = None, *, index: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None = None, variable_name: str | None = None, value_name: str | None = None) -> DataFrame`
Unpivot a DataFrame from wide to long format.

### `unstack(*, step: int, how: UnstackDirection = "vertical", columns: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None = None, fill_values: list[Any] | None = None) -> DataFrame`
Unstack a long table to a wide form without doing an aggregation.

### `update(other: DataFrame, on: str | Sequence[str] | None = None, how: Literal["left", "inner", "full"] = "left", *, left_on: str | Sequence[str] | None = None, right_on: str | Sequence[str] | None = None, include_nulls: bool = False, maintain_order: MaintainOrderJoin | None = "left") -> DataFrame`
Update the values in this `DataFrame` with the values in `other`.

### `upsample(time_column: str, *, every: str | timedelta, group_by: str | Sequence[str] | None = None, maintain_order: bool = False) -> DataFrame`
Upsample a DataFrame at a regular frequency.

### `var(ddof: int = 1) -> DataFrame`
Aggregate the columns of this DataFrame to their variance value.

### `vstack(other: DataFrame, *, in_place: bool = False) -> DataFrame`
Grow this DataFrame vertically by stacking a DataFrame to it.

### `with_columns(*exprs: IntoExpr | Iterable[IntoExpr], **named_exprs: IntoExpr) -> DataFrame`
Add columns to this DataFrame.

### `with_columns_seq(*exprs: IntoExpr | Iterable[IntoExpr], **named_exprs: IntoExpr) -> DataFrame`
Add columns to this DataFrame.

### `with_row_count(name: str = "row_nr", offset: int = 0) -> DataFrame` *(deprecated)*
Add a column at index 0 that counts the rows.

### `with_row_index(name: str = "index", offset: int = 0) -> DataFrame`
Add a row index as the first column in the DataFrame.

### `write_avro(file: str | Path | IO[bytes], compression: AvroCompression = "uncompressed", name: str = "") -> None`
Write to Apache Avro file.

### `write_clipboard(*, separator: str = "\t", **kwargs: Any) -> None`
Copy `DataFrame` in csv format to the system clipboard with `write_csv`.

### `write_csv(file: str | Path | IO[str] | IO[bytes] | None = None, *, include_bom: bool = False, compression: Literal["uncompressed", "gzip", "zstd"] = "uncompressed", compression_level: int | None = None, check_extension: bool = True, include_header: bool = True, separator: str = ",", line_terminator: str = "\n", quote_char: str = '"', batch_size: int = 1024, datetime_format: str | None = None, date_format: str | None = None, time_format: str | None = None, float_scientific: bool | None = None, float_precision: int | None = None, decimal_comma: bool = False, null_value: str | None = None, quote_style: CsvQuoteStyle | None = None, storage_options: StorageOptionsDict | None = None, credential_provider: CredentialProviderFunction | Literal["auto"] | None = "auto", retries: int | None = None) -> str | None`
Write to comma-separated values (CSV) file.

### `write_database(table_name: str, connection: ConnectionOrCursor | str, *, if_table_exists: DbWriteMode = "fail", engine: DbWriteEngine | None = None, engine_options: dict[str, Any] | None = None) -> int`
Write the data in a Polars DataFrame to a database.

### `write_delta(target: str | Path | deltalake.DeltaTable, *, mode: Literal["error", "append", "overwrite", "ignore", "merge"] = "error", overwrite_schema: bool | None = None, storage_options: StorageOptionsDict | None = None, credential_provider: CredentialProviderFunction | Literal["auto"] | None = "auto", delta_write_options: dict[str, Any] | None = None, delta_merge_options: dict[str, Any] | None = None) -> deltalake.table.TableMerger | None`
Write DataFrame as delta table.

### `write_excel(workbook: str | Workbook | IO[bytes] | Path | None = None, worksheet: str | Worksheet | None = None, *, position: tuple[int, int] | str = "A1", table_style: str | dict[str, Any] | None = None, table_name: str | None = None, column_formats: ColumnFormatDict | None = None, dtype_formats: dict[OneOrMoreDataTypes, str] | None = None, conditional_formats: ConditionalFormatDict | None = None, header_format: dict[str, Any] | None = None, column_totals: ColumnTotalsDefinition | None = None, column_widths: ColumnWidthsDefinition | None = None, row_totals: RowTotalsDefinition | None = None, row_heights: dict[int | tuple[int, ...], int] | int | None = None, sparklines: dict[str, Sequence[str] | dict[str, Any]] | None = None, formulas: dict[str, str | dict[str, str]] | None = None, float_precision: int = 3, include_header: bool = True, autofilter: bool = True, autofit: bool = False, hidden_columns: Sequence[str] | SelectorType | None = None, hide_gridlines: bool = False, sheet_zoom: int | None = None, freeze_panes: str | tuple[int, int] | tuple[str, int, int] | tuple[int, int, int, int] | None = None, use_zip64: bool = False) -> Workbook`
Write frame data to a table in an Excel workbook/worksheet.

### `write_iceberg(target: str | pyiceberg.table.Table, mode: Literal["append", "overwrite"]) -> None`
Write DataFrame to an Iceberg table.

### `write_ipc(file: str | Path | IO[bytes] | None, *, compression: IpcCompression = "uncompressed", compat_level: CompatLevel | None = None, record_batch_size: int | None = None, storage_options: StorageOptionsDict | None = None, credential_provider: CredentialProviderFunction | Literal["auto"] | None = "auto", retries: int | None = None) -> BytesIO | None`
Write to Arrow IPC binary stream or Feather file.

### `write_ipc_stream(file: str | Path | IO[bytes] | None, *, compression: IpcCompression = "uncompressed", compat_level: CompatLevel | None = None) -> BytesIO | None`
Write to Arrow IPC record batch stream.

### `write_json(file: IOBase | str | Path | None = None) -> str | None`
Serialize to JSON representation.

### `write_ndjson(file: str | Path | IO[bytes] | IO[str] | None = None, *, compression: Literal["uncompressed", "gzip", "zstd"] = "uncompressed", compression_level: int | None = None, check_extension: bool = True) -> str | None`
Serialize to newline delimited JSON representation.

### `write_parquet(file: str | Path | IO[bytes], *, compression: ParquetCompression = "zstd", compression_level: int | None = None, statistics: bool | str | dict[str, bool] = True, row_group_size: int | None = None, data_page_size: int | None = None, use_pyarrow: bool = False, pyarrow_options: dict[str, Any] | None = None, partition_by: str | Sequence[str] | None = None, partition_chunk_size_bytes: int = 4_294_967_296, storage_options: StorageOptionsDict | None = None, credential_provider: CredentialProviderFunction | Literal["auto"] | None = "auto", retries: int | None = None, metadata: ParquetMetadata | None = None, arrow_schema: ArrowSchemaExportable | None = None, mkdir: bool = False) -> None`
Write to Apache Parquet file.
