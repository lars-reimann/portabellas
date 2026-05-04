# Expr

## Class

Expressions that can be used in various contexts.

## Class Methods

### `deserialize(source: str | Path | IOBase | bytes, *, format: SerializationFormat = "binary") -> Expr`
Read a serialized expression from a file.

### `from_json(value: str) -> Expr`
Read an expression from a JSON encoded string to construct an Expression.

## Properties (Namespace Accessors)

| Accessor | Return Type | Description |
|----------|-------------|-------------|
| `arr` | `ExprArrayNameSpace` | Create an object namespace of all array related methods. |
| `bin` | `ExprBinaryNameSpace` | Create an object namespace of all binary related methods. |
| `cat` | `ExprCatNameSpace` | Create an object namespace of all categorical related methods. |
| `dt` | `ExprDateTimeNameSpace` | Create an object namespace of all datetime related methods. |
| `ext` | `ExprExtensionNameSpace` | Create an object namespace of all extension type related expressions. |
| `list` | `ExprListNameSpace` | Create an object namespace of all list related methods. |
| `meta` | `ExprMetaNameSpace` | Create an object namespace of all meta related expression methods. |
| `name` | `ExprNameNameSpace` | Create an object namespace of all expressions that modify expression names. |
| `str` | `ExprStringNameSpace` | Create an object namespace of all string related methods. |
| `struct` | `ExprStructNameSpace` | Create an object namespace of all struct related methods. |

## Operators

`__add__`, `__sub__`, `__mul__`, `__truediv__`, `__floordiv__`, `__mod__`, `__pow__`, `__radd__`, `__rsub__`, `__rmul__`, `__rtruediv__`, `__rfloordiv__`, `__rmod__`, `__rpow__`, `__eq__`, `__ne__`, `__lt__`, `__le__`, `__gt__`, `__ge__`, `__and__`, `__or__`, `__xor__`, `__rand__`, `__ror__`, `__rxor__`, `__invert__` (not_), `__neg__`, `__pos__`, `__abs__` (abs), `__array_ufunc__` (numpy ufuncs).

## Instance Methods (Alphabetical)

### `abs() -> Expr`
Compute absolute values.

### `add(other: Any) -> Expr`
Method equivalent of addition operator `expr + other`.

### `agg_groups() -> Expr` *(deprecated)*
Get the group indexes of the group by operation.

### `alias(name: str) -> Expr`
Rename the expression.

### `all(*, ignore_nulls: bool = True) -> Expr`
Return whether all values in the column are `True`.

### `and_(*others: Any) -> Expr`
Method equivalent of bitwise "and" operator `expr & other & ...`.

### `any(*, ignore_nulls: bool = True) -> Expr`
Return whether any of the values in the column are `True`.

### `append(other: IntoExpr, *, upcast: bool = True) -> Expr`
Append expressions.

### `approx_n_unique() -> Expr`
Approximate count of unique values.

### `arccos() -> Expr`
Compute the element-wise value for the inverse cosine.

### `arccosh() -> Expr`
Compute the element-wise value for the inverse hyperbolic cosine.

### `arcsin() -> Expr`
Compute the element-wise value for the inverse sine.

### `arcsinh() -> Expr`
Compute the element-wise value for the inverse hyperbolic sine.

### `arctan() -> Expr`
Compute the element-wise value for the inverse tangent.

### `arctanh() -> Expr`
Compute the element-wise value for the inverse hyperbolic tangent.

### `arg_max() -> Expr`
Get the index of the maximal value.

### `arg_min() -> Expr`
Get the index of the minimal value.

### `arg_sort(*, descending: bool = False, nulls_last: bool = False) -> Expr`
Get the index values that would sort this column.

### `arg_true() -> Expr`
Return indices where expression evaluates `True`.

### `arg_unique() -> Expr`
Get index of first unique value.

### `backward_fill(limit: int | None = None) -> Expr`
Fill missing values with the next non-null value.

### `bitwise_and() -> Expr`
Perform an aggregation of bitwise ANDs.

### `bitwise_count_ones() -> Expr`
Evaluate the number of set bits.

### `bitwise_count_zeros() -> Expr`
Evaluate the number of unset bits.

### `bitwise_leading_ones() -> Expr`
Evaluate the number most-significant set bits before seeing an unset bit.

### `bitwise_leading_zeros() -> Expr`
Evaluate the number most-significant unset bits before seeing a set bit.

### `bitwise_or() -> Expr`
Perform an aggregation of bitwise ORs.

### `bitwise_trailing_ones() -> Expr`
Evaluate the number least-significant set bits before seeing an unset bit.

### `bitwise_trailing_zeros() -> Expr`
Evaluate the number least-significant unset bits before seeing a set bit.

### `bitwise_xor() -> Expr`
Perform an aggregation of bitwise XORs.

### `bottom_k(k: int | IntoExprColumn = 5) -> Expr`
Return the `k` smallest elements.

### `bottom_k_by(by: IntoExpr | Iterable[IntoExpr], k: int | IntoExprColumn = 5, *, reverse: bool | Sequence[bool] = False) -> Expr`
Return the elements corresponding to the `k` smallest elements of the `by` column(s).

### `cast(dtype: PolarsDataType | pl.DataTypeExpr | type[Any], *, strict: bool = True, wrap_numerical: bool = False) -> Expr`
Cast between data types.

### `cbrt() -> Expr`
Compute the cube root of the elements.

### `ceil() -> Expr`
Rounds up to the nearest integer value.

### `clip(lower_bound: NumericLiteral | TemporalLiteral | IntoExprColumn | None = None, upper_bound: NumericLiteral | TemporalLiteral | IntoExprColumn | None = None) -> Expr`
Set values outside the given boundaries to the boundary value.

### `cos() -> Expr`
Compute the element-wise value for the cosine.

### `cosh() -> Expr`
Compute the element-wise value for the hyperbolic cosine.

### `cot() -> Expr`
Compute the element-wise value for the cotangent.

### `count() -> Expr`
Return the number of non-null elements in the column.

### `cum_count(*, reverse: bool = False) -> Expr`
Return the cumulative count of the non-null values in the column.

### `cum_max(*, reverse: bool = False) -> Expr`
Get an array with the cumulative max computed at every element.

### `cum_min(*, reverse: bool = False) -> Expr`
Get an array with the cumulative min computed at every element.

### `cum_prod(*, reverse: bool = False) -> Expr`
Get an array with the cumulative product computed at every element.

### `cum_sum(*, reverse: bool = False) -> Expr`
Get an array with the cumulative sum computed at every element.

### `cumulative_eval(expr: Expr, *, min_samples: int = 1) -> Expr`
Run an expression over a sliding window that increases `1` slot every iteration.

### `cut(breaks: Sequence[float], *, labels: Sequence[str] | None = None, left_closed: bool = False, include_breaks: bool = False) -> Expr`
Bin continuous values into discrete categories.

### `degrees() -> Expr`
Convert from radians to degrees.

### `diff(n: int | IntoExpr = 1, null_behavior: NullBehavior = "ignore") -> Expr`
Calculate the first discrete difference between shifted items.

### `dot(other: Expr | str) -> Expr`
Compute the dot/inner product between two Expressions.

### `drop_nans() -> Expr`
Drop all floating point NaN values.

### `drop_nulls() -> Expr`
Drop all null values.

### `entropy(base: float = math.e, *, normalize: bool = True) -> Expr`
Computes the entropy.

### `eq(other: Any) -> Expr`
Method equivalent of equality operator `expr == other`.

### `eq_missing(other: Any) -> Expr`
Method equivalent of equality operator `expr == other` where `None == None`.

### `ewm_mean(*, com: float | None = None, span: float | None = None, half_life: float | None = None, alpha: float | None = None, adjust: bool = True, min_samples: int = 1, ignore_nulls: bool = False) -> Expr`
Compute exponentially-weighted moving average.

### `ewm_mean_by(by: str | IntoExpr, *, half_life: str | timedelta) -> Expr`
Compute time-based exponentially weighted moving average.

### `ewm_std(*, com: float | None = None, span: float | None = None, half_life: float | None = None, alpha: float | None = None, adjust: bool = True, bias: bool = False, min_samples: int = 1, ignore_nulls: bool = False) -> Expr`
Compute exponentially-weighted moving standard deviation.

### `ewm_var(*, com: float | None = None, span: float | None = None, half_life: float | None = None, alpha: float | None = None, adjust: bool = True, bias: bool = False, min_samples: int = 1, ignore_nulls: bool = False) -> Expr`
Compute exponentially-weighted moving variance.

### `exclude(columns: str | PolarsDataType | Collection[str | PolarsDataType], *more_columns: str | PolarsDataType) -> Expr`
Exclude columns from a multi-column expression.

### `exp() -> Expr`
Compute the exponential, element-wise.

### `explode(*, empty_as_null: bool = True, keep_nulls: bool = True) -> Expr`
Explode a list expression.

### `extend_constant(value: IntoExpr, n: int | IntoExprColumn) -> Expr`
Extremely fast method for extending the Series with 'n' copies of a value.

### `fill_nan(value: int | float | Expr | None) -> Expr`
Fill floating point NaN value with a fill value.

### `fill_null(value: Any | Expr | None = None, strategy: FillNullStrategy | None = None, limit: int | None = None) -> Expr`
Fill null values using the specified value or strategy.

### `filter(*predicates: IntoExprColumn | Iterable[IntoExprColumn], **constraints: Any) -> Expr`
Filter the expression based on one or more predicate expressions.

### `first(*, ignore_nulls: bool = False) -> Expr`
Get the first value.

### `floor() -> Expr`
Rounds down to the nearest integer value.

### `floordiv(other: Any) -> Expr`
Method equivalent of integer division operator `expr // other`.

### `flatten() -> Expr` *(deprecated — use Expr.list.explode)*
Flatten a list or string column.

### `forward_fill(limit: int | None = None) -> Expr`
Fill missing values with the last non-null value.

### `gather(indices: int | Sequence[int] | IntoExpr | Series | np.ndarray[Any, Any]) -> Expr`
Take values by index.

### `gather_every(n: int, offset: int = 0) -> Expr`
Take every nth value in the Series and return as a new Series.

### `ge(other: Any) -> Expr`
Method equivalent of "greater than or equal" operator `expr >= other`.

### `get(index: int | Expr, *, null_on_oob: bool = False) -> Expr`
Return a single value by index.

### `gt(other: Any) -> Expr`
Method equivalent of "greater than" operator `expr > other`.

### `has_nulls() -> Expr`
Check whether the expression contains one or more null values.

### `hash(seed: int = 0, seed_1: int | None = None, seed_2: int | None = None, seed_3: int | None = None) -> Expr`
Hash the elements in the selection.

### `head(n: int | Expr = 10) -> Expr`
Get the first `n` rows.

### `hist(bins: IntoExpr | None = None, *, bin_count: int | None = None, include_category: bool = False, include_breakpoint: bool = False) -> Expr`
Bin values into buckets and count their occurrences.

### `implode(*, maintain_order: bool = True) -> Expr`
Aggregate values into a list.

### `index_of(element: IntoExpr) -> Expr`
Get the index of the first occurrence of a value, or `None` if it's not found.

### `inspect(fmt: str = "{}") -> Expr`
Print the value that this expression evaluates to and pass on the value.

### `interpolate(method: InterpolationMethod = "linear") -> Expr`
Interpolate intermediate values.

### `interpolate_by(by: IntoExpr) -> Expr`
Fill null values using interpolation based on another column.

### `is_between(lower_bound: IntoExpr, upper_bound: IntoExpr, closed: ClosedInterval = "both") -> Expr`
Check if this expression is between the given lower and upper bounds.

### `is_close(other: IntoExpr, *, abs_tol: float = 0.0, rel_tol: float = 1e-09, nans_equal: bool = False) -> Expr`
Check if this expression is close, i.e. almost equal, to the other expression.

### `is_duplicated() -> Expr`
Return a boolean mask indicating duplicated values.

### `is_finite() -> Expr`
Returns a boolean Series indicating which values are finite.

### `is_first_distinct() -> Expr`
Return a boolean mask indicating the first occurrence of each distinct value.

### `is_in(other: Expr | Collection[Any] | Series, *, nulls_equal: bool = False) -> Expr`
Check if elements of this expression are present in the other Series.

### `is_infinite() -> Expr`
Returns a boolean Series indicating which values are infinite.

### `is_last_distinct() -> Expr`
Return a boolean mask indicating the last occurrence of each distinct value.

### `is_nan() -> Expr`
Returns a boolean Series indicating which values are NaN.

### `is_not_nan() -> Expr`
Returns a boolean Series indicating which values are not NaN.

### `is_not_null() -> Expr`
Returns a boolean Series indicating which values are not null.

### `is_null() -> Expr`
Returns a boolean Series indicating which values are null.

### `is_unique() -> Expr`
Get mask of unique values.

### `item(*, allow_empty: bool = False) -> Expr`
Get the single value.

### `kurtosis(*, fisher: bool = True, bias: bool = True) -> Expr`
Compute the kurtosis (Fisher or Pearson) of a dataset.

### `last(*, ignore_nulls: bool = False) -> Expr`
Get the last value.

### `le(other: Any) -> Expr`
Method equivalent of "less than or equal" operator `expr <= other`.

### `len() -> Expr`
Return the number of elements in the column.

### `limit(n: int | Expr = 10) -> Expr`
Get the first `n` rows (alias for `Expr.head`).

### `log(base: float | IntoExpr = math.e) -> Expr`
Compute the logarithm to a given base.

### `log10() -> Expr`
Compute the base 10 logarithm of the input array, element-wise.

### `log1p() -> Expr`
Compute the natural logarithm of each element plus one.

### `lower_bound() -> Expr`
Calculate the lower bound.

### `lt(other: Any) -> Expr`
Method equivalent of "less than" operator `expr < other`.

### `map_batches(function: Callable[[Series], Series | Any], return_dtype: PolarsDataType | pl.DataTypeExpr | None = None, *, agg_list: bool = False, is_elementwise: bool = False, returns_scalar: bool = False) -> Expr`
Apply a custom python function to a whole Series or sequence of Series.

### `map_elements(function: Callable[[Any], Any], return_dtype: PolarsDataType | pl.DataTypeExpr | None = None, *, skip_nulls: bool = True, pass_name: bool = False, strategy: MapElementsStrategy = "thread_local", returns_scalar: bool = False) -> Expr`
Map a custom/user-defined function (UDF) to each element of a column.

### `max() -> Expr`
Get maximum value.

### `max_by(by: IntoExpr) -> Expr`
Get maximum value, ordered by another expression.

### `mean() -> Expr`
Get mean value.

### `median() -> Expr`
Get median value using linear interpolation.

### `min() -> Expr`
Get minimum value.

### `min_by(by: IntoExpr) -> Expr`
Get minimum value, ordered by another expression.

### `mode(*, maintain_order: bool = False) -> Expr`
Compute the most occurring value(s).

### `mod(other: Any) -> Expr`
Method equivalent of modulus operator `expr % other`.

### `mul(other: Any) -> Expr`
Method equivalent of multiplication operator `expr * other`.

### `nan_max() -> Expr`
Get maximum value, but propagate/poison encountered NaN values.

### `nan_min() -> Expr`
Get minimum value, but propagate/poison encountered NaN values.

### `ne(other: Any) -> Expr`
Method equivalent of inequality operator `expr != other`.

### `ne_missing(other: Any) -> Expr`
Method equivalent of equality operator `expr != other` where `None == None`.

### `neg() -> Expr`
Method equivalent of unary minus operator `-expr`.

### `not_() -> Expr`
Method equivalent of bitwise "not" operator `~expr`.

### `null_count() -> Expr`
Count null values.

### `n_unique() -> Expr`
Count unique values.

### `or_(*others: Any) -> Expr`
Method equivalent of bitwise "or" operator `expr | other | ...`.

### `over(partition_by: IntoExpr | Iterable[IntoExpr] | None = None, *more_exprs: IntoExpr, order_by: IntoExpr | Iterable[IntoExpr] | None = None, descending: bool = False, nulls_last: bool = False, mapping_strategy: WindowMappingStrategy = "group_to_rows") -> Expr`
Compute expressions over the given groups.

### `pct_change(n: int | IntoExprColumn = 1) -> Expr`
Computes percentage change between values.

### `peak_max() -> Expr`
Get a boolean mask of the local maximum peaks.

### `peak_min() -> Expr`
Get a boolean mask of the local minimum peaks.

### `pipe(function: Callable[Concatenate[Expr, P], T], *args: P.args, **kwargs: P.kwargs) -> T`
Offers a structured way to apply a sequence of user-defined functions (UDFs).

### `pow(exponent: IntoExprColumn | int | float) -> Expr`
Method equivalent of exponentiation operator `expr ** exponent`.

### `product() -> Expr`
Compute the product of an expression.

### `qcut(quantiles: Sequence[float] | int, *, labels: Sequence[str] | None = None, left_closed: bool = False, allow_duplicates: bool = False, include_breaks: bool = False) -> Expr`
Bin continuous values into discrete categories based on their quantiles.

### `quantile(quantile: float | list[float] | Expr, interpolation: QuantileMethod = "nearest") -> Expr`
Get quantile value.

### `radians() -> Expr`
Convert from degrees to radians.

### `rank(method: RankMethod = "average", *, descending: bool = False, seed: int | None = None) -> Expr`
Assign ranks to data, dealing with ties appropriately.

### `rechunk() -> Expr`
Create a single chunk of memory for this Series.

### `register_plugin(*, lib: str, symbol: str, args: list[IntoExpr] | None = None, kwargs: dict[Any, Any] | None = None, is_elementwise: bool = False, input_wildcard_expansion: bool = False, returns_scalar: bool = False, cast_to_supertypes: bool = False, pass_name_to_apply: bool = False, changes_length: bool = False) -> Expr`
Register a plugin function.

### `reinterpret(*, signed: bool | None = None, dtype: PolarsDataType | None = None) -> Expr`
Reinterpret the underlying bits as a signed/unsigned integer or float.

### `replace(old: IntoExpr | Sequence[Any] | Mapping[Any, Any], new: IntoExpr | Sequence[Any] | NoDefault = NO_DEFAULT, *, default: IntoExpr | NoDefault = NO_DEFAULT, return_dtype: PolarsDataType | None = None) -> Expr`
Replace the given values by different values of the same data type.

### `replace_strict(old: IntoExpr | Sequence[Any] | Mapping[Any, Any], new: IntoExpr | Sequence[Any] | NoDefault = NO_DEFAULT, *, default: IntoExpr | NoDefault = NO_DEFAULT, return_dtype: PolarsDataType | pl.DataTypeExpr | None = None) -> Expr`
Replace all values by different values.

### `repeat_by(by: pl.Series | Expr | str | int) -> Expr`
Repeat the elements in this Series as specified in the given expression.

### `reshape(dimensions: tuple[int, ...]) -> Expr`
Reshape this Expr to a flat column or an Array column.

### `reverse() -> Expr`
Reverse the selection.

### `rle() -> Expr`
Compress the column data using run-length encoding.

### `rle_id() -> Expr`
Get a distinct integer ID for each run of identical values.

### `rolling(index_column: IntoExprColumn, *, period: str | timedelta, offset: str | timedelta | None = None, closed: ClosedInterval = "right") -> Expr`
Create rolling groups based on a temporal or integer column.

### `rolling_kurtosis(window_size: int, *, fisher: bool = True, bias: bool = True, min_samples: int | None = None, center: bool = False) -> Expr`
Compute a rolling kurtosis.

### `rolling_map(function: Callable[[Series], Any], window_size: int, weights: list[float] | None = None, *, min_samples: int | None = None, center: bool = False) -> Expr`
Compute a custom rolling window function.

### `rolling_max(window_size: int, weights: list[float] | None = None, *, min_samples: int | None = None, center: bool = False) -> Expr`
Apply a rolling max (moving max) over the values in this array.

### `rolling_max_by(by: IntoExpr, window_size: timedelta | str, *, min_samples: int = 1, closed: ClosedInterval = "right") -> Expr`
Apply a rolling max based on another column.

### `rolling_mean(window_size: int, weights: list[float] | None = None, *, min_samples: int | None = None, center: bool = False) -> Expr`
Apply a rolling mean (moving mean) over the values in this array.

### `rolling_mean_by(by: IntoExpr, window_size: timedelta | str, *, min_samples: int = 1, closed: ClosedInterval = "right") -> Expr`
Apply a rolling mean based on another column.

### `rolling_median(window_size: int, weights: list[float] | None = None, *, min_samples: int | None = None, center: bool = False) -> Expr`
Compute a rolling median.

### `rolling_median_by(by: IntoExpr, window_size: timedelta | str, *, min_samples: int = 1, closed: ClosedInterval = "right") -> Expr`
Compute a rolling median based on another column.

### `rolling_min(window_size: int, weights: list[float] | None = None, *, min_samples: int | None = None, center: bool = False) -> Expr`
Apply a rolling min (moving min) over the values in this array.

### `rolling_min_by(by: IntoExpr, window_size: timedelta | str, *, min_samples: int = 1, closed: ClosedInterval = "right") -> Expr`
Apply a rolling min based on another column.

### `rolling_quantile(quantile: float, interpolation: QuantileMethod = "nearest", window_size: int = 2, weights: list[float] | None = None, *, min_samples: int | None = None, center: bool = False) -> Expr`
Compute a rolling quantile.

### `rolling_quantile_by(by: IntoExpr, window_size: timedelta | str, *, quantile: float, interpolation: QuantileMethod = "nearest", min_samples: int = 1, closed: ClosedInterval = "right") -> Expr`
Compute a rolling quantile based on another column.

### `rolling_rank(window_size: int, method: RankMethod = "average", *, seed: int | None = None, min_samples: int | None = None, center: bool = False) -> Expr`
Compute a rolling rank.

### `rolling_rank_by(by: IntoExpr, window_size: timedelta | str, method: RankMethod = "average", *, seed: int | None = None, min_samples: int = 1, closed: ClosedInterval = "right") -> Expr`
Compute a rolling rank based on another column.

### `rolling_skew(window_size: int, *, bias: bool = True, min_samples: int | None = None, center: bool = False) -> Expr`
Compute a rolling skew.

### `rolling_std(window_size: int, weights: list[float] | None = None, *, min_samples: int | None = None, center: bool = False, ddof: int = 1) -> Expr`
Compute a rolling standard deviation.

### `rolling_std_by(by: IntoExpr, window_size: timedelta | str, *, min_samples: int = 1, closed: ClosedInterval = "right", ddof: int = 1) -> Expr`
Compute a rolling standard deviation based on another column.

### `rolling_sum(window_size: int, weights: list[float] | None = None, *, min_samples: int | None = None, center: bool = False) -> Expr`
Apply a rolling sum (moving sum) over the values in this array.

### `rolling_sum_by(by: IntoExpr, window_size: timedelta | str, *, min_samples: int = 1, closed: ClosedInterval = "right") -> Expr`
Apply a rolling sum based on another column.

### `rolling_var(window_size: int, weights: list[float] | None = None, *, min_samples: int | None = None, center: bool = False, ddof: int = 1) -> Expr`
Compute a rolling variance.

### `rolling_var_by(by: IntoExpr, window_size: timedelta | str, *, min_samples: int = 1, closed: ClosedInterval = "right", ddof: int = 1) -> Expr`
Compute a rolling variance based on another column.

### `round(decimals: int = 0, mode: RoundMode = "half_to_even") -> Expr`
Round underlying floating point data by `decimals` digits.

### `round_sig_figs(digits: int) -> Expr`
Round to a number of significant figures.

### `sample(n: int | IntoExprColumn | None = None, *, fraction: float | IntoExprColumn | None = None, with_replacement: bool = False, shuffle: bool = False, seed: int | None = None) -> Expr`
Sample from this expression.

### `search_sorted(element: IntoExpr | np.ndarray[Any, Any], side: SearchSortedSide = "any", *, descending: bool = False) -> Expr`
Find indices where elements should be inserted to maintain order.

### `set_sorted(*, descending: bool = False, nulls_last: bool = False) -> Expr`
Flags the expression as 'sorted'.

### `shift(n: int | IntoExprColumn = 1, *, fill_value: IntoExpr | None = None) -> Expr`
Shift values by the given number of indices.

### `shrink_dtype() -> Expr`
Shrink numeric columns to the minimal required datatype.

### `shuffle(seed: int | None = None) -> Expr`
Shuffle the contents of this expression.

### `sign() -> Expr`
Compute the element-wise sign function on numeric types.

### `sin() -> Expr`
Compute the element-wise value for the sine.

### `sinh() -> Expr`
Compute the element-wise value for the hyperbolic sine.

### `skew(*, bias: bool = True) -> Expr`
Compute the sample skewness of a data set.

### `slice(offset: int | Expr, length: int | Expr | None = None) -> Expr`
Get a slice of this expression.

### `sort(*, descending: bool = False, nulls_last: bool = False) -> Expr`
Sort this column.

### `sort_by(by: IntoExpr | Iterable[IntoExpr], *more_by: IntoExpr, descending: bool | Sequence[bool] = False, nulls_last: bool | Sequence[bool] = False, multithreaded: bool = True, maintain_order: bool = False) -> Expr`
Sort this column by the ordering of other columns.

### `sqrt() -> Expr`
Compute the square root of the elements.

### `std(ddof: int = 1) -> Expr`
Get standard deviation.

### `sub(other: Any) -> Expr`
Method equivalent of subtraction operator `expr - other`.

### `sum() -> Expr`
Get sum value.

### `tail(n: int | Expr = 10) -> Expr`
Get the last `n` rows.

### `tan() -> Expr`
Compute the element-wise value for the tangent.

### `tanh() -> Expr`
Compute the element-wise value for the hyperbolic tangent.

### `to_physical() -> Expr`
Cast to physical representation of the logical dtype.

### `top_k(k: int | IntoExprColumn = 5) -> Expr`
Return the `k` largest elements.

### `top_k_by(by: IntoExpr | Iterable[IntoExpr], k: int | IntoExprColumn = 5, *, reverse: bool | Sequence[bool] = False) -> Expr`
Return the elements corresponding to the `k` largest elements of the `by` column(s).

### `truediv(other: Any) -> Expr`
Method equivalent of float division operator `expr / other`.

### `truncate(decimals: int = 0) -> Expr`
Truncate numeric data toward zero to `decimals` number of decimal places.

### `unique(*, maintain_order: bool = False) -> Expr`
Get unique values of this expression.

### `unique_counts() -> Expr`
Return a count of the unique values in the order of appearance.

### `upper_bound() -> Expr`
Calculate the upper bound.

### `value_counts(*, sort: bool = False, parallel: bool = False, name: str | None = None, normalize: bool = False) -> Expr`
Count the occurrence of unique values.

### `var(ddof: int = 1) -> Expr`
Get variance.

### `where(predicate: Expr) -> Expr` *(deprecated — use filter)*
Filter a single column.

### `xor(other: Any) -> Expr`
Method equivalent of bitwise exclusive-or operator `expr ^ other`.
