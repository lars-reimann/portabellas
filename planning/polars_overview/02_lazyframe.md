# LazyFrame

## Constructor

### `LazyFrame(data: FrameInitTypes | None = None, schema: SchemaDefinition | None = None, *, schema_overrides: SchemaDict | None = None, strict: bool = True, orient: Orientation | None = None, infer_schema_length: int | None = N_INFER_DEFAULT, nan_to_null: bool = False, height: int | None = None) -> None`
Representation of a Lazy computation graph/query against a DataFrame.

## Class Methods

### `deserialize(source: str | bytes | Path | IOBase, *, format: SerializationFormat = "binary") -> LazyFrame`
Read a logical plan from a file to construct a LazyFrame.

## Properties

### `columns -> list[str]`
Get the column names.

### `dtypes -> list[DataType]`
Get the column data types.

### `schema -> Schema`
Get an ordered mapping of column names to their data type.

### `width -> int`
Get the number of columns.

## Dunder Methods

### `__contains__(key: str) -> bool`
Check membership via schema.

### `__getitem__(item: slice) -> LazyFrame`
Support slice syntax, returning a new LazyFrame.

### `__copy__() -> LazyFrame`
Return a copy.

### `__deepcopy__(memo: None = None) -> LazyFrame`
Return a deep copy.

## Instance Methods (Alphabetical)

### `approx_n_unique() -> LazyFrame` *(deprecated)*
Approximate count of unique values.

### `bottom_k(k: int, *, by: IntoExpr | Iterable[IntoExpr], reverse: bool | Sequence[bool] = False) -> LazyFrame`
Return the `k` smallest rows.

### `cache() -> LazyFrame`
Cache the result once the execution of the physical plan hits this node.

### `cast(dtypes: Mapping[ColumnNameOrSelector | PolarsDataType, PolarsDataType | PythonDataType] | PolarsDataType | pl.DataTypeExpr | Schema, *, strict: bool = True) -> LazyFrame`
Cast LazyFrame column(s) to the specified dtype(s).

### `clear(n: int = 0) -> LazyFrame`
Create an empty copy of the current LazyFrame, with zero to 'n' rows.

### `clone() -> LazyFrame`
Create a copy of this LazyFrame.

### `collect(*, type_coercion: bool = True, predicate_pushdown: bool = True, projection_pushdown: bool = True, simplify_expression: bool = True, slice_pushdown: bool = True, comm_subplan_elim: bool = True, comm_subexpr_elim: bool = True, cluster_with_columns: bool = True, collapse_joins: bool = True, no_optimization: bool = False, engine: EngineType = "auto", background: bool = False, optimizations: QueryOptFlags = DEFAULT_QUERY_OPT_FLAGS) -> DataFrame | InProcessQuery`
Materialize this LazyFrame into a DataFrame.

### `collect_async(*, gevent: bool = False, engine: EngineType = "auto", optimizations: QueryOptFlags = DEFAULT_QUERY_OPT_FLAGS) -> Awaitable[DataFrame] | _GeventDataFrameResult[DataFrame]`
Collect DataFrame asynchronously in thread pool.

### `collect_batches(*, chunk_size: int | None = None, maintain_order: bool = True, lazy: bool = False, engine: EngineType = "auto", optimizations: QueryOptFlags = DEFAULT_QUERY_OPT_FLAGS) -> Iterator[DataFrame]` *(unstable)*
Evaluate the query in streaming mode and get a generator that returns chunks.

### `collect_schema() -> Schema`
Resolve the schema of this LazyFrame.

### `count() -> LazyFrame`
Return the number of non-null elements for each column.

### `describe(percentiles: Sequence[float] | float | None = (0.25, 0.50, 0.75), *, interpolation: QuantileMethod = "nearest") -> DataFrame`
Creates a summary of statistics for a LazyFrame, returning a DataFrame.

### `drop(*columns: ColumnNameOrSelector | Iterable[ColumnNameOrSelector], strict: bool = True) -> LazyFrame`
Remove columns from the DataFrame.

### `drop_nans(subset: ColumnNameOrSelector | Collection[ColumnNameOrSelector] | None = None) -> LazyFrame`
Drop all rows that contain one or more NaN values.

### `drop_nulls(subset: ColumnNameOrSelector | Collection[ColumnNameOrSelector] | None = None) -> LazyFrame`
Drop all rows that contain one or more null values.

### `explain(*, format: ExplainFormat = "plain", optimized: bool = True, ...) -> str`
Create a string representation of the query plan.

### `explode(columns: ColumnNameOrSelector | Iterable[ColumnNameOrSelector], *more_columns: ColumnNameOrSelector, empty_as_null: bool = True, keep_nulls: bool = True) -> LazyFrame`
Explode the DataFrame to long format by exploding the given columns.

### `fetch(n_rows: int = 500, **kwargs: Any) -> DataFrame` *(deprecated)*
Collect a small number of rows for debugging purposes.

### `fill_nan(value: int | float | Expr | None) -> LazyFrame`
Fill floating point NaN values.

### `fill_null(value: Any | Expr | None = None, strategy: FillNullStrategy | None = None, limit: int | None = None, *, matches_supertype: bool = True) -> LazyFrame`
Fill null values using the specified value or strategy.

### `filter(*predicates: IntoExprColumn | Iterable[IntoExprColumn] | bool | list[bool] | np.ndarray[Any, Any], **constraints: Any) -> LazyFrame`
Filter rows in the LazyFrame based on a predicate expression.

### `first() -> LazyFrame`
Get the first row of the DataFrame.

### `gather_every(n: int, offset: int = 0) -> LazyFrame`
Take every nth row in the LazyFrame and return as a new LazyFrame.

### `group_by(*by: IntoExpr | Iterable[IntoExpr], maintain_order: bool = False, **named_by: IntoExpr) -> LazyGroupBy`
Start a group by operation.

### `group_by_dynamic(index_column: IntoExpr, *, every: str | timedelta, period: str | timedelta | None = None, offset: str | timedelta | None = None, include_boundaries: bool = False, closed: ClosedInterval = "left", label: Label = "left", group_by: IntoExpr | Iterable[IntoExpr] | None = None, start_by: StartBy = "window") -> LazyGroupBy`
Group based on a time value (or index value of type Int32, Int64).

### `head(n: int = 5) -> LazyFrame`
Get the first `n` rows.

### `inspect(fmt: str = "{}") -> LazyFrame`
Inspect a node in the computation graph.

### `interpolate() -> LazyFrame`
Interpolate intermediate values.

### `join(other: LazyFrame, on: str | Expr | Sequence[str | Expr] | None = None, how: JoinStrategy = "inner", *, left_on: str | Expr | Sequence[str | Expr] | None = None, right_on: str | Expr | Sequence[str | Expr] | None = None, suffix: str = "_right", validate: JoinValidation = "m:m", nulls_equal: bool = False, coalesce: bool | None = None, maintain_order: MaintainOrderJoin | None = None, allow_parallel: bool = True, force_parallel: bool = False) -> LazyFrame`
Add a join operation to the Logical Plan.

### `join_asof(other: LazyFrame, *, left_on: str | None | Expr = None, right_on: str | None | Expr = None, on: str | None | Expr = None, by_left: str | Sequence[str] | None = None, by_right: str | Sequence[str] | None = None, by: str | Sequence[str] | None = None, strategy: AsofJoinStrategy = "backward", suffix: str = "_right", tolerance: str | int | float | timedelta | None = None, allow_parallel: bool = True, force_parallel: bool = False, coalesce: bool = True, allow_exact_matches: bool = True, check_sortedness: bool = True) -> LazyFrame`
Perform an asof join.

### `join_where(other: LazyFrame, *predicates: Expr | Iterable[Expr], suffix: str = "_right") -> LazyFrame` *(unstable)*
Perform a join based on one or multiple (in)equality predicates.

### `last() -> LazyFrame`
Get the last row of the DataFrame.

### `lazy() -> LazyFrame`
Return lazy representation, i.e. itself.

### `limit(n: int = 5) -> LazyFrame`
Get the first `n` rows.

### `map_batches(function: Callable[[DataFrame], DataFrame], *, predicate_pushdown: bool = False, projection_pushdown: bool = False, slice_pushdown: bool = False, no_optimizations: bool | None = None, schema: None | SchemaDict = None, validate_output_schema: bool = True, streamable: bool = False) -> LazyFrame`
Apply a custom function.

### `match_to_schema(schema: SchemaDict | Schema, *, missing_columns: Literal["insert", "raise"] | Mapping[str, Literal["insert", "raise"] | Expr] | Expr = "raise", missing_struct_fields: Literal["insert", "raise"] | Mapping[str, Literal["insert", "raise"]] = "raise", extra_columns: Literal["ignore", "raise"] = "raise", extra_struct_fields: Literal["ignore", "raise"] | Mapping[str, Literal["ignore", "raise"]] = "raise", integer_cast: Literal["upcast", "forbid"] | Mapping[str, Literal["upcast", "forbid"]] = "forbid", float_cast: Literal["upcast", "forbid"] | Mapping[str, Literal["upcast", "forbid"]] = "forbid") -> LazyFrame` *(unstable)*
Match or evolve the schema of a LazyFrame into a specific schema.

### `max() -> LazyFrame`
Aggregate the columns in the LazyFrame to their maximum value.

### `mean() -> LazyFrame`
Aggregate the columns in the LazyFrame to their mean value.

### `median() -> LazyFrame`
Aggregate the columns in the LazyFrame to their median value.

### `melt(id_vars: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None = None, value_vars: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None = None, variable_name: str | None = None, value_name: str | None = None, *, streamable: bool = True) -> LazyFrame` *(deprecated)*
Unpivot a DataFrame from wide to long format.

### `merge_sorted(other: LazyFrame, key: str, *, maintain_order: bool = False) -> LazyFrame`
Take two sorted DataFrames and merge them by the sorted key.

### `min() -> LazyFrame`
Aggregate the columns in the LazyFrame to their minimum value.

### `null_count() -> LazyFrame`
Aggregate the columns in the LazyFrame as the sum of their null value count.

### `pipe(function: Callable[Concatenate[LazyFrame, P], T], *args: P.args, **kwargs: P.kwargs) -> T`
Offers a structured way to apply a sequence of user-defined functions (UDFs).

### `pipe_with_schema(function: Callable[[LazyFrame, Schema], LazyFrame]) -> LazyFrame` *(unstable)*
Allows to alter the lazy frame during the plan stage with the resolved schema.

### `pivot(on: ColumnNameOrSelector | Sequence[ColumnNameOrSelector], on_columns: Sequence[Any] | pl.Series | pl.DataFrame, *, index: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None = None, values: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None = None, aggregate_function: PivotAgg | Expr | None = None, maintain_order: bool = False, separator: str = "_", column_naming: Literal["auto", "combine"] = "auto") -> LazyFrame`
Create a spreadsheet-style pivot table as a DataFrame.

### `profile(*, type_coercion: bool = True, predicate_pushdown: bool = True, projection_pushdown: bool = True, simplify_expression: bool = True, no_optimization: bool = False, slice_pushdown: bool = True, comm_subplan_elim: bool = True, comm_subexpr_elim: bool = True, cluster_with_columns: bool = True, collapse_joins: bool = True, show_plot: bool = False, truncate_nodes: int = 0, figsize: tuple[int, int] = (18, 8), engine: EngineType = "auto", optimizations: QueryOptFlags = DEFAULT_QUERY_OPT_FLAGS) -> tuple[DataFrame, DataFrame]`
Profile a LazyFrame.

### `quantile(quantile: float | Expr, interpolation: QuantileMethod = "nearest") -> LazyFrame`
Aggregate the columns in the LazyFrame to their quantile value.

### `remove(*predicates: IntoExprColumn | Iterable[IntoExprColumn] | bool | list[bool] | np.ndarray[Any, Any], **constraints: Any) -> LazyFrame`
Remove rows, dropping those that match the given predicate expression(s).

### `rename(mapping: Mapping[str, str] | Callable[[str], str], *, strict: bool = True) -> LazyFrame`
Rename column names.

### `reverse() -> LazyFrame`
Reverse the DataFrame.

### `rolling(index_column: IntoExpr, *, period: str | timedelta, offset: str | timedelta | None = None, closed: ClosedInterval = "right", group_by: IntoExpr | Iterable[IntoExpr] | None = None) -> LazyGroupBy`
Create rolling groups based on a temporal or integer column.

### `select(*exprs: IntoExpr | Iterable[IntoExpr], **named_exprs: IntoExpr) -> LazyFrame`
Select columns from this LazyFrame.

### `select_seq(*exprs: IntoExpr | Iterable[IntoExpr], **named_exprs: IntoExpr) -> LazyFrame`
Select columns from this LazyFrame.

### `serialize(file: IOBase | str | Path | None = None, *, format: SerializationFormat = "binary") -> bytes | str | None`
Serialize the logical plan of this LazyFrame to a file or string in JSON format.

### `set_sorted(column: str | list[str], *more_columns: str, descending: bool | list[bool] = False, nulls_last: bool | list[bool] = False) -> LazyFrame`
Flag a column as sorted.

### `shift(n: int | IntoExprColumn = 1, *, fill_value: IntoExpr | None = None) -> LazyFrame`
Shift values by the given number of indices.

### `show(limit: int | None = 5, *, ...) -> None`
Show the first `n` rows.

### `show_graph(*, optimized: bool = True, show: bool = True, output_path: str | Path | None = None, raw_output: bool = False, figsize: tuple[float, float] = (16.0, 12.0), ..., optimizations: QueryOptFlags = DEFAULT_QUERY_OPT_FLAGS) -> str | None`
Show a plot of the query plan.

### `sink_batches(function: Callable[[DataFrame], bool | None], *, chunk_size: int | None = None, maintain_order: bool = True, lazy: bool = False, engine: EngineType = "auto", optimizations: QueryOptFlags = DEFAULT_QUERY_OPT_FLAGS) -> pl.LazyFrame | None` *(unstable)*
Evaluate the query and call a user-defined function for every ready batch.

### `sink_csv(path: str | Path | IO[bytes] | IO[str] | PartitionBy, *, include_bom: bool = False, compression: Literal["uncompressed", "gzip", "zstd"] = "uncompressed", ..., maintain_order: bool = True, ...) -> LazyFrame | None`
Evaluate the query in streaming mode and write to a CSV file.

### `sink_delta(target: str | Path | deltalake.DeltaTable, *, mode: Literal["error", "append", "overwrite", "ignore", "merge"] = "error", ...) -> deltalake.table.TableMerger | None` *(unstable)*
Sink DataFrame as delta table.

### `sink_iceberg(target: str | pyiceberg.table.Table, *, mode: Literal["append", "overwrite"], ...) -> pl.DataFrame` *(unstable)*
Sink a LazyFrame to an Iceberg table.

### `sink_ipc(path: str | Path | IO[bytes] | PartitionBy, *, compression: IpcCompression | None = "uncompressed", ..., maintain_order: bool = True, ...) -> LazyFrame | None`
Evaluate the query in streaming mode and write to an IPC file.

### `sink_ndjson(path: str | Path | IO[bytes] | IO[str] | PartitionBy, *, compression: Literal["uncompressed", "gzip", "zstd"] = "uncompressed", ..., maintain_order: bool = True, ...) -> LazyFrame | None`
Evaluate the query in streaming mode and write to an NDJSON file.

### `sink_parquet(path: str | Path | IO[bytes] | PartitionBy, *, compression: str = "zstd", ..., maintain_order: bool = True, ..., metadata: ParquetMetadata | None = None, ...) -> LazyFrame | None`
Evaluate the query in streaming mode and write to a Parquet file.

### `slice(offset: int, length: int | None = None) -> LazyFrame`
Get a slice of this DataFrame.

### `sort(by: IntoExpr | Iterable[IntoExpr], *more_by: IntoExpr, descending: bool | Sequence[bool] = False, nulls_last: bool | Sequence[bool] = False, maintain_order: bool = False, multithreaded: bool = True) -> LazyFrame`
Sort the LazyFrame by the given columns.

### `sql(query: str, *, table_name: str = "self") -> LazyFrame` *(unstable)*
Execute a SQL query against the LazyFrame.

### `std(ddof: int = 1) -> LazyFrame`
Aggregate the columns in the LazyFrame to their standard deviation value.

### `sum() -> LazyFrame`
Aggregate the columns in the LazyFrame to their sum value.

### `tail(n: int = 5) -> LazyFrame`
Get the last `n` rows.

### `top_k(k: int, *, by: IntoExpr | Iterable[IntoExpr], reverse: bool | Sequence[bool] = False) -> LazyFrame`
Return the `k` largest rows.

### `unique(subset: IntoExpr | Collection[IntoExpr] | None = None, *, keep: UniqueKeepStrategy = "any", maintain_order: bool = False) -> LazyFrame`
Drop duplicate rows from this LazyFrame.

### `unnest(columns: ColumnNameOrSelector | Collection[ColumnNameOrSelector] | None = None, *more_columns: ColumnNameOrSelector, separator: str | None = None) -> LazyFrame`
Decompose struct columns into separate columns for each of their fields.

### `unpivot(on: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None = None, *, index: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None = None, variable_name: str | None = None, value_name: str | None = None, streamable: bool = True) -> LazyFrame`
Unpivot a DataFrame from wide to long format.

### `update(other: LazyFrame, on: str | Sequence[str] | None = None, how: Literal["left", "inner", "full"] = "left", *, left_on: str | Sequence[str] | None = None, right_on: str | Sequence[str] | None = None, include_nulls: bool = False, maintain_order: MaintainOrderJoin | None = "left") -> LazyFrame` *(unstable)*
Update the values in this `LazyFrame` with the values in `other`.

### `var(ddof: int = 1) -> LazyFrame`
Aggregate the columns in the LazyFrame to their variance value.

### `with_columns(*exprs: IntoExpr | Iterable[IntoExpr], **named_exprs: IntoExpr) -> LazyFrame`
Add columns to this LazyFrame.

### `with_columns_seq(*exprs: IntoExpr | Iterable[IntoExpr], **named_exprs: IntoExpr) -> LazyFrame`
Add columns to this LazyFrame.

### `with_context(other: Self | list[Self]) -> LazyFrame` *(deprecated)*
Add an external context to the computation graph.

### `with_row_count(name: str = "row_nr", offset: int = 0) -> LazyFrame` *(deprecated)*
Add a column at index 0 that counts the rows.

### `with_row_index(name: str = "index", offset: int = 0) -> LazyFrame`
Add a row index as the first column in the LazyFrame.
