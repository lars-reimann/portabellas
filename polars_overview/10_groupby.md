# GroupBy Classes

## GroupBy

Eager group-by operations on a DataFrame.

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `__iter__` | `() -> Iterator[tuple[tuple[object, ...], DataFrame]]` | Iterate over groups. |
| `agg` | `(*aggs: IntoExpr | Iterable[IntoExpr], **named_aggs: IntoExpr) -> DataFrame` | Compute aggregated values. |
| `all` | `() -> DataFrame` | Get all values per group as a list. |
| `first` | `() -> DataFrame` | Get the first value per group. |
| `head` | `(n: int = 5) -> DataFrame` | Get the first `n` rows per group. |
| `iter` | `() -> Iterator[tuple[tuple[object, ...], DataFrame]]` | Iterate over groups. |
| `last` | `() -> DataFrame` | Get the last value per group. |
| `len` | `() -> DataFrame` | Return the number of rows per group. |
| `map_groups` | `(function: Callable[[DataFrame], DataFrame], *, return_dtype: SchemaDict | None = None) -> DataFrame` | Apply a function over each group. |
| `max` | `() -> DataFrame` | Get the max value per group. |
| `mean` | `() -> DataFrame` | Get the mean value per group. |
| `median` | `() -> DataFrame` | Get the median value per group. |
| `min` | `() -> DataFrame` | Get the min value per group. |
| `n_groups` | `() -> int` | Return the number of groups. |
| `quantile` | `(quantile: float, interpolation: QuantileMethod = "nearest") -> DataFrame` | Compute quantile per group. |
| `size` | `() -> DataFrame` | Return the number of rows per group. |
| `std` | `(ddof: int = 1) -> DataFrame` | Compute standard deviation per group. |
| `sum` | `() -> DataFrame` | Get the sum per group. |
| `tail` | `(n: int = 5) -> DataFrame` | Get the last `n` rows per group. |
| `var` | `(ddof: int = 1) -> DataFrame` | Compute variance per group. |

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `by` | `list[Expr]` | The expressions that define the grouping. |
| `name_list` | `list[str]` | The column names used for grouping. |

---

## LazyGroupBy

Lazy group-by operations on a LazyFrame.

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `agg` | `(*aggs: IntoExpr | Iterable[IntoExpr], **named_aggs: IntoExpr) -> LazyFrame` | Compute aggregated values. |
| `all` | `() -> LazyFrame` | Get all values per group as a list. |
| `first` | `() -> LazyFrame` | Get the first value per group. |
| `head` | `(n: int = 5) -> LazyFrame` | Get the first `n` rows per group. |
| `last` | `() -> LazyFrame` | Get the last value per group. |
| `len` | `() -> LazyFrame` | Return the number of rows per group. |
| `map_groups` | `(function: Callable[[DataFrame], DataFrame], *, return_dtype: SchemaDict | None = None) -> LazyFrame` | Apply a function over each group. |
| `max` | `() -> LazyFrame` | Get the max value per group. |
| `mean` | `() -> LazyFrame` | Get the mean value per group. |
| `median` | `() -> LazyFrame` | Get the median value per group. |
| `min` | `() -> LazyFrame` | Get the min value per group. |
| `quantile` | `(quantile: float, interpolation: QuantileMethod = "nearest") -> LazyFrame` | Compute quantile per group. |
| `size` | `() -> LazyFrame` | Return the number of rows per group. |
| `std` | `(ddof: int = 1) -> LazyFrame` | Compute standard deviation per group. |
| `sum` | `() -> LazyFrame` | Get the sum per group. |
| `tail` | `(n: int = 5) -> LazyFrame` | Get the last `n` rows per group. |
| `var` | `(ddof: int = 1) -> LazyFrame` | Compute variance per group. |

---

## DynamicGroupBy

Group-by based on a temporal/time-based window.

### Constructor

`DynamicGroupBy(frame: DataFrame, index_column: str, *, period: str | timedelta, offset: str | timedelta | None = None, label: LabelMethod = "left", include_boundaries: bool = False, closed: ClosedInterval = "left", group_key: str | None = None, start_by: StartBy = "window", check_sorted: bool = True)`

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `agg` | `(*aggs: IntoExpr | Iterable[IntoExpr], **named_aggs: IntoExpr) -> DataFrame` | Compute aggregated values. |
| `first` | `() -> DataFrame` | Get the first value per group. |
| `last` | `() -> DataFrame` | Get the last value per group. |
| `max` | `() -> DataFrame` | Get the max value per group. |
| `mean` | `() -> DataFrame` | Get the mean value per group. |
| `median` | `() -> DataFrame` | Get the median value per group. |
| `min` | `() -> DataFrame` | Get the min value per group. |
| `sum` | `() -> DataFrame` | Get the sum per group. |

---

## RollingGroupBy

Group-by based on a rolling/fixed-size window.

### Constructor

`RollingGroupBy(frame: DataFrame, index_column: str, *, period: str | timedelta, offset: str | timedelta | None = None, closed: ClosedInterval = "right", check_sorted: bool = True)`

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `agg` | `(*aggs: IntoExpr | Iterable[IntoExpr], **named_aggs: IntoExpr) -> DataFrame` | Compute aggregated values. |
| `first` | `() -> DataFrame` | Get the first value per group. |
| `last` | `() -> DataFrame` | Get the last value per group. |
| `max` | `() -> DataFrame` | Get the max value per group. |
| `mean` | `() -> DataFrame` | Get the mean value per group. |
| `median` | `() -> DataFrame` | Get the median value per group. |
| `min` | `() -> DataFrame` | Get the min value per group. |
| `quantile` | `(quantile: float, interpolation: QuantileMethod = "nearest") -> DataFrame` | Compute quantile per group. |
| `sum` | `() -> DataFrame` | Get the sum per group. |
