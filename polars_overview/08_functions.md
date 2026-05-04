# Top-Level Functions

## Aggregation Functions

### `all(*names: str) -> Expr`
Select all columns, or select all columns matching the given names.

### `all_horizontal(*exprs: IntoExpr) -> Expr`
Compute the bitwise AND horizontally across columns.

### `any(*names: str) -> Expr`
Select any column matching the given names.

### `any_horizontal(*exprs: IntoExpr) -> Expr`
Compute the bitwise OR horizontally across columns.

### `approx_n_unique(*columns: str | Expr) -> Expr`
Approximate count of unique values.

### `count(*columns: str | Expr) -> Expr`
Return the number of non-null values in the column.

### `max(*columns: str | Expr) -> Expr`
Get the maximum value.

### `max_horizontal(*exprs: IntoExpr) -> Expr`
Get the maximum value horizontally across columns.

### `mean(*columns: str | Expr) -> Expr`
Get the mean value.

### `mean_horizontal(*exprs: IntoExpr) -> Expr`
Compute the mean horizontally across columns.

### `median(*columns: str | Expr) -> Expr`
Get the median value.

### `min(*columns: str | Expr) -> Expr`
Get the minimum value.

### `min_horizontal(*exprs: IntoExpr) -> Expr`
Get the minimum value horizontally across columns.

### `n_unique(*columns: str | Expr) -> Expr`
Count unique values.

### `quantile(column: str | Expr, quantile: float | Expr, interpolation: QuantileMethod = "nearest") -> Expr`
Get quantile value.

### `std(column: str | Expr, ddof: int = 1) -> Expr`
Get standard deviation.

### `sum(*columns: str | Expr) -> Expr`
Get the sum value.

### `sum_horizontal(*exprs: IntoExpr) -> Expr`
Sum all values horizontally across columns.

### `var(column: str | Expr, ddof: int = 1) -> Expr`
Get variance.

## Column / Expression Constructors

### `col(*names: str | Iterable[str]) -> Expr`
Create an expression referring to a column by name.

### `element() -> Expr`
Create an expression referring to the element in an `eval` context.

### `field(name: str | list[str]) -> Expr`
Create an expression referring to a struct field.

### `first(*columns: str | Expr) -> Expr`
Get the first value, or select the first column.

### `last(*columns: str | Expr) -> Expr`
Get the last value, or select the last column.

### `len() -> Expr`
Return the number of rows.

### `lit(value: Any, *, dtype: PolarsDataType | None = None, allow_object: bool = False, *) -> Expr`
Create a literal expression.

### `nth(*indices: int | Sequence[int]) -> Expr`
Select columns by index.

## Arithmetic / Math Functions

### `arange(start: int | IntoExprColumn, end: int | IntoExprColumn, step: int = 1, *, dtype: PolarsDataType | None = None, eager: bool = False) -> Expr | Series`
Generate a range of integers.

### `arctan2(y: int | float | IntoExprColumn, x: int | float | IntoExprColumn) -> Expr`
Compute two-argument arctangent in radians.

### `arctan2d(y: int | float | IntoExprColumn, x: int | float | IntoExprColumn) -> Expr`
Compute two-argument arctangent in degrees.

### `int_range(start: int | IntoExprColumn, end: int | IntoExprColumn, step: int = 1, *, dtype: PolarsDataType | None = None, eager: bool = False) -> Expr | Series`
Generate a range of integers.

### `int_ranges(start: int | IntoExprColumn, end: int | IntoExprColumn, step: int | IntoExprColumn = 1, *, dtype: PolarsDataType | None = None, eager: bool = False) -> Expr | Series`
Generate a range of integers for each row.

### `linear_space(start: float | IntoExprColumn, end: float | IntoExprColumn, num: int | IntoExprColumn, *, eager: bool = False) -> Expr | Series`
Generate a sequence of evenly spaced numbers.

### `linear_spaces(start: float | IntoExprColumn, end: float | IntoExprColumn, num: int | IntoExprColumn, *, eager: bool = False) -> Expr | Series`
Generate a sequence of evenly spaced numbers for each row.

### `ones(n: int | IntoExprColumn, *, dtype: PolarsDataType | None = None, eager: bool = False) -> Expr | Series`
Create a Series of ones.

### `zeros(n: int | IntoExprColumn, *, dtype: PolarsDataType | None = None, eager: bool = False) -> Expr | Series`
Create a Series of zeros.

### `repeat(value: int | float | str | bool | date | datetime | timedelta | time | None, n: int | IntoExprColumn, *, dtype: PolarsDataType | None = None, eager: bool = False) -> Expr | Series`
Repeat a value `n` times.

## String Functions

### `concat_str(exprs: IntoExpr | Iterable[IntoExpr], separator: str = "", *, ignore_nulls: bool = False) -> Expr`
Horizontally concatenate columns into a string.

### `format(template: str, *exprs: IntoExpr) -> Expr`
Format expressions as a string using a template.

### `escape_regex(str: str) -> str`
Escape a regex pattern string.

## List / Array Functions

### `concat_arr(*exprs: IntoExpr) -> Expr`
Concatenate arrays horizontally.

### `concat_list(exprs: IntoExpr | Iterable[IntoExpr]) -> Expr`
Concatenate lists horizontally into a list.

### `implode(*columns: str | Expr) -> Expr`
Aggregate values into a list.

## Conditional / Logical Functions

### `coalesce(*exprs: IntoExpr | Iterable[IntoExpr]) -> Expr`
Return the first non-null value for each row.

### `when(condition: Expr) -> When`
Start a when-then-else expression.

### `exclude(columns: str | PolarsDataType | Collection[str | PolarsDataType], *more_columns: str | PolarsDataType) -> Expr`
Exclude columns from selection.

### `select(*exprs: IntoExpr | Iterable[IntoExpr]) -> Expr`
Select columns from the DataFrame (in expression context).

## Cumulative Functions

### `cum_count(*exprs: IntoExpr | Iterable[IntoExpr], *, reverse: bool = False) -> Expr`
Return the cumulative count.

### `cum_fold(acc: IntoExpr, function: Callable[[Series, Series], Series], exprs: IntoExpr | Iterable[IntoExpr], *, include_init: bool = False) -> Expr`
Cumulatively fold horizontally across columns.

### `cum_reduce(function: Callable[[Series, Series], Series], exprs: IntoExpr | Iterable[IntoExpr]) -> Expr`
Cumulatively reduce horizontally across columns.

### `cum_sum(*exprs: IntoExpr | Iterable[IntoExpr], *, reverse: bool = False) -> Expr`
Return the cumulative sum.

### `cum_sum_horizontal(*exprs: IntoExpr | Iterable[IntoExpr]) -> Expr`
Cumulative sum across columns horizontally.

## Temporal Functions

### `date(*, year: Expr | int | None = None, month: Expr | int | None = None, day: Expr | int | None = None) -> Expr`
Create a Date expression.

### `date_range(start: date | datetime | str | Expr, end: date | datetime | str | Expr, interval: str | timedelta = "1d", *, eager: bool = False, closed: ClosedInterval = "both") -> Expr | Series`
Generate a date range.

### `date_ranges(start: date | datetime | str | Expr, end: date | datetime | str | Expr, interval: str | timedelta = "1d", *, eager: bool = False, closed: ClosedInterval = "both") -> Expr | Series`
Generate a date range for each row.

### `datetime(*, year: Expr | int | None = None, month: Expr | int | None = None, day: Expr | int | None = None, hour: Expr | int | None = None, minute: Expr | int | None = None, second: Expr | int | None = None, microsecond: Expr | int | None = None, time_unit: TimeUnit | None = None, time_zone: str | None = None, ambiguous: Ambiguous | Expr = "raise") -> Expr`
Create a Datetime expression.

### `datetime_range(start: date | datetime | str | Expr, end: date | datetime | str | Expr, interval: str | timedelta = "1d", *, eager: bool = False, closed: ClosedInterval = "both", time_unit: TimeUnit | None = None, time_zone: str | None = None) -> Expr | Series`
Generate a datetime range.

### `datetime_ranges(start: date | datetime | str | Expr, end: date | datetime | str | Expr, interval: str | timedelta = "1d", *, eager: bool = False, closed: ClosedInterval = "both", time_unit: TimeUnit | None = None, time_zone: str | None = None) -> Expr | Series`
Generate a datetime range for each row.

### `duration(*, weeks: Expr | int | None = None, days: Expr | int | None = None, hours: Expr | int | None = None, minutes: Expr | int | None = None, seconds: Expr | int | None = None, milliseconds: Expr | int | None = None, microseconds: Expr | int | None = None, nanoseconds: Expr | int | None = None, time_unit: TimeUnit = "us") -> Expr`
Create a Duration expression.

### `time(*, hour: Expr | int | None = None, minute: Expr | int | None = None, second: Expr | int | None = None, microsecond: Expr | int | None = None, nanosecond: Expr | int | None = None) -> Expr`
Create a Time expression.

### `time_range(start: time | str | Expr, end: time | str | Expr, interval: str | timedelta = "1h", *, eager: bool = False, closed: ClosedInterval = "both") -> Expr | Series`
Generate a time range.

### `time_ranges(start: time | str | Expr, end: time | str | Expr, interval: str | timedelta = "1h", *, eager: bool = False, closed: ClosedInterval = "both") -> Expr | Series`
Generate a time range for each row.

## Sorting / Ranking / Indexing Functions

### `arg_sort_by(exprs: IntoExpr | Iterable[IntoExpr], *more_exprs: IntoExpr, descending: bool | Sequence[bool] = False, nulls_last: bool | Sequence[bool] = False, multithreaded: bool = True, maintain_order: bool = False) -> Expr`
Return the row indices that would sort the given columns.

### `arg_where(condition: Expr | Series) -> Expr | Series`
Return indices where `condition` is `True`.

### `row_index(name: str = "row_index", offset: int = 0) -> Expr`
Add a row index column.

## Business Day Functions

### `business_day_count(start: date | datetime | Expr, end: date | datetime | Expr, week_mask: Sequence[bool] = (True, True, True, True, True), holidays: Sequence[date] | None = None) -> Expr`
Count the number of business days between start and end.

## Correlation / Covariance Functions

### `corr(a: IntoExpr, b: IntoExpr, *, ddof: int = 1, propagate_nans: bool = False) -> Expr`
Compute the Pearson correlation.

### `cov(a: IntoExpr, b: IntoExpr, *, ddof: int = 1) -> Expr`
Compute the covariance.

### `rolling_corr(x: str | Expr, y: str | Expr, window_size: int, *, min_samples: int | None = None, ddof: int = 1) -> Expr`
Compute rolling Pearson correlation.

### `rolling_cov(x: str | Expr, y: str | Expr, window_size: int, *, min_samples: int | None = None, ddof: int = 1) -> Expr`
Compute rolling covariance.

## Fold / Reduce Functions

### `fold(acc: IntoExpr, function: Callable[[Series, Series], Series], exprs: IntoExpr | Iterable[IntoExpr], *, include_init: bool = False) -> Expr`
Fold horizontally across columns.

### `reduce(function: Callable[[Series, Series], Series], exprs: IntoExpr | Iterable[IntoExpr]) -> Expr`
Reduce horizontally across columns.

## Epoch / Conversion Functions

### `from_epoch(column: str | Expr, time_unit: EpochTimeUnit = "us") -> Expr`
Convert from epoch to Date/Datetime.

### `dtype_of(*columns: str | Expr) -> Expr`
Get the data type of the expression.

### `self_dtype() -> Expr`
Get the data type of the current expression context.

## Grouping / Merging Functions

### `groups(column: str | Expr) -> Expr`
Return the group indices.

### `merge_sorted(l_df: LazyFrame | DataFrame, r_df: LazyFrame | DataFrame, key: str) -> LazyFrame | DataFrame`
Merge two sorted DataFrames.

## Head / Tail Functions

### `head(n: int = 10) -> Expr`
Get the first `n` rows.

### `tail(n: int = 10) -> Expr`
Get the last `n` rows.

## Collection Functions

### `collect_all(*lfys: LazyFrame, *, type_coercion: bool = True, predicate_pushdown: bool = True, projection_pushdown: bool = True, simplify_expression: bool = True, no_optimization: bool = False, slice_pushdown: bool = True, comm_subplan_elim: bool = True, comm_subexpr_elim: bool = True, cluster_with_key: bool = True, collapse_joins: bool = True, _eager: bool = False) -> list[DataFrame]`
Collect multiple LazyFrames in parallel.

### `collect_all_async(lfys: Sequence[LazyFrame], *, type_coercion: bool = True, predicate_pushdown: bool = True, projection_pushdown: bool = True, simplify_expression: bool = True, no_optimization: bool = False, slice_pushdown: bool = True, comm_subplan_elim: bool = True, comm_subexpr_elim: bool = True, cluster_with_key: bool = True, collapse_joins: bool = True) -> Coroutine[Any, Any, list[DataFrame]]`
Collect multiple LazyFrames asynchronously.

### `defer(function: Callable[..., Any], *args: Any, schema: Callable[[list[Schema]], Schema] | Schema | None = None, **kwargs: Any) -> LazyFrame`
Defer a function call to be executed later.

## Concat Functions

### `concat(items: Sequence[DataFrame | LazyFrame | Series | Expr], *, rechunk: bool = True, how: ConcatMethod = "vertical", parallel: bool = True) -> DataFrame | LazyFrame | Series | Expr`
Combine multiple DataFrames/Series.

### `union(*exprs: IntoExpr | Iterable[IntoExpr]) -> Expr`
Compute the set union of list columns.

## Struct Functions

### `struct(*exprs: IntoExpr | Iterable[IntoExpr], *, eager: bool = False, schema: SchemaDict | None = None) -> Expr | Series`
Create a struct expression.

### `struct_with_fields(expr: IntoExpr, *fields: IntoExpr) -> Expr`
Add or replace fields of a struct.

## SQL Functions

### `sql_expr(sql: str) -> Expr`
Parse a SQL expression into a Polars expression.

## Misc Functions

### `align_frames(*frames: DataFrame | LazyFrame, on: str | Expr | Sequence[str] | Sequence[Expr] | Sequence[str | Expr], select: str | Expr | Sequence[str | Expr] | None = None, descending: bool | Sequence[bool] = False) -> list[DataFrame]`
Align frames on a common key.

### `explain_all(*lfys: LazyFrame) -> str`
Explain the query plan for multiple LazyFrames.

### `map_batches(function: Callable[[Sequence[Series]], Series], return_dtype: PolarsDataType | None = None, *, agg_list: bool = False) -> Expr`
Apply a custom function to entire batches.

### `map_groups(function: Callable[[Sequence[Series]], Series | Any], return_dtype: PolarsDataType | None = None, *, returns_scalar: bool = True) -> Expr`
Apply a custom function to groups.

### `set_random_seed(seed: int) -> None`
Set the random seed for reproducible results.
