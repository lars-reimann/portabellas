# Series

## Constructor

### `__init__(name: str | ArrayLike | None = None, values: ArrayLike | None = None, dtype: PolarsDataType | None = None, *, strict: bool = True, nan_to_null: bool = False) -> None`
A Series represents a single column in a Polars DataFrame.

## Properties

### `bin -> BinaryNameSpace`
Create an object namespace of all binary related methods.

### `cat -> CatNameSpace`
Create an object namespace of all categorical related methods.

### `dt -> DateTimeNameSpace`
Create an object namespace of all datetime related methods.

### `list -> ListNameSpace`
Create an object namespace of all list related methods.

### `arr -> ArrayNameSpace`
Create an object namespace of all array related methods.

### `str -> StringNameSpace`
Create an object namespace of all string related methods.

### `struct -> StructNameSpace`
Create an object namespace of all struct related methods.

### `ext -> ExtensionNameSpace`
Create an object namespace of all extension type related methods.

### `plot -> SeriesPlot`
Create a plot namespace.

### `dtype -> DataType`
Get the data type of this Series.

### `flags -> dict[str, bool]`
Get flags that are set on the Series.

### `name -> str`
Get the name of this Series.

### `shape -> tuple[int]`
Shape of this Series.

## Dunder Methods

### `__abs__() -> Series`
Compute absolute values.

### `__add__(other: Any) -> Series | DataFrame | Expr`
Arithmetic addition operator.

### `__and__(other: Any) -> Expr | Series`
Bitwise AND operator.

### `__array__(dtype: npt.DTypeLike | None = None, copy: bool | None = None) -> np.ndarray[Any, Any]`
Return a NumPy ndarray with the given data type.

### `__array_ufunc__(ufunc: np.ufunc, method: str, *inputs: Any, **kwargs: Any) -> Series`
Numpy universal functions.

### `__arrow_c_stream__(requested_schema: object | None = None) -> object`
Export a Series via the Arrow PyCapsule Interface.

### `__bool__() -> NoReturn`
The truth value of a Series is ambiguous.

### `__contains__(item: Any) -> bool`
Check if item is in the Series.

### `__copy__() -> Self`
Return a clone of the Series.

### `__deepcopy__(memo: None = None) -> Self`
Return a clone of the Series.

### `__eq__(other: object) -> Series | Expr`
Equality comparison operator.

### `__floordiv__(other: Any) -> Series | Expr`
Floor division operator.

### `__ge__(other: Any) -> Series | Expr`
Greater-than-or-equal comparison operator.

### `__getitem__(key: SingleIndexSelector | MultiIndexSelector) -> Any | Series`
Get part of the Series as a new Series or scalar.

### `__gt__(other: Any) -> Series | Expr`
Greater-than comparison operator.

### `__invert__() -> Series`
Invert (not) operator.

### `__iter__() -> Generator[Any]`
Iterate over the elements of the Series.

### `__le__(other: Any) -> Series | Expr`
Less-than-or-equal comparison operator.

### `__len__() -> int`
Return the length of the Series.

### `__lt__(other: Any) -> Series | Expr`
Less-than comparison operator.

### `__matmul__(other: Any) -> float | Series | None`
Matrix multiplication operator.

### `__mod__(other: Any) -> Series | Expr`
Modulo operator.

### `__mul__(other: Any) -> Series | DataFrame | Expr`
Multiplication operator.

### `__ne__(other: object) -> Series | Expr`
Inequality comparison operator.

### `__neg__() -> Series`
Negation operator.

### `__or__(other: Any) -> Expr | Series`
Bitwise OR operator.

### `__pos__() -> Series`
Unary plus operator.

### `__pow__(exponent: int | float | Series) -> Series`
Exponentiation operator.

### `__radd__(other: Any) -> Series`
Reflected addition operator.

### `__rmod__(other: Any) -> Series`
Reflected modulo operator.

### `__rmul__(other: Any) -> Series`
Reflected multiplication operator.

### `__rpow__(other: Any) -> Series`
Reflected exponentiation operator.

### `__rsub__(other: Any) -> Series`
Reflected subtraction operator.

### `__rtruediv__(other: Any) -> Series`
Reflected true division operator.

### `__setitem__(key: int | Series | np.ndarray[Any, Any] | Sequence[object] | tuple[object], value: Any) -> None`
Set Series values in-place using a single index, boolean mask, or index array.

### `__sub__(other: Any) -> Series | Expr`
Subtraction operator.

### `__truediv__(other: Any) -> Series | Expr`
True division operator.

### `__xor__(other: Any) -> Expr | Series`
Bitwise XOR operator.

## Instance Methods (Alphabetical)

### `abs() -> Series`
Compute absolute values.

### `alias(name: str) -> Series`
Rename the series.

### `all(*, ignore_nulls: bool = True) -> bool | None`
Return whether all values in the column are `True`.

### `any(*, ignore_nulls: bool = True) -> bool | None`
Return whether any of the values in the column are `True`.

### `append(other: Series) -> Self`
Append a Series to this one.

### `approx_n_unique() -> PythonLiteral | None`
Approximate count of unique values.

### `arccos() -> Series`
Compute the element-wise value for the inverse cosine.

### `arccosh() -> Series`
Compute the element-wise value for the inverse hyperbolic cosine.

### `arcsin() -> Series`
Compute the element-wise value for the inverse sine.

### `arcsinh() -> Series`
Compute the element-wise value for the inverse hyperbolic sine.

### `arctan() -> Series`
Compute the element-wise value for the inverse tangent.

### `arctanh() -> Series`
Compute the element-wise value for the inverse hyperbolic tangent.

### `arg_max() -> int | None`
Get the index of the maximal value.

### `arg_min() -> int | None`
Get the index of the minimal value.

### `arg_sort(*, descending: bool = False, nulls_last: bool = False) -> Series`
Get the index values that would sort this Series.

### `arg_true() -> Series`
Get index values where Boolean Series evaluate True.

### `arg_unique() -> Series`
Get unique index as Series.

### `backward_fill(limit: int | None = None) -> Series`
Fill missing values with the next non-null value.

### `bitwise_and() -> PythonLiteral | None`
Perform an aggregation of bitwise ANDs.

### `bitwise_count_ones() -> Self`
Evaluate the number of set bits.

### `bitwise_count_zeros() -> Self`
Evaluate the number of unset bits.

### `bitwise_leading_ones() -> Self`
Evaluate the number most-significant set bits before seeing an unset bit.

### `bitwise_leading_zeros() -> Self`
Evaluate the number most-significant unset bits before seeing a set bit.

### `bitwise_or() -> PythonLiteral | None`
Perform an aggregation of bitwise ORs.

### `bitwise_trailing_ones() -> Self`
Evaluate the number least-significant set bits before seeing an unset bit.

### `bitwise_trailing_zeros() -> Self`
Evaluate the number least-significant unset bits before seeing a set bit.

### `bitwise_xor() -> PythonLiteral | None`
Perform an aggregation of bitwise XORs.

### `bottom_k(k: int = 5) -> Series`
Return the `k` smallest elements.

### `bottom_k_by(by: IntoExpr | Iterable[IntoExpr], k: int = 5, *, reverse: bool | Sequence[bool] = False) -> Series`
Return the `k` smallest elements of the `by` column.

### `cast(dtype: type[int | float | str | bool] | PolarsDataType, *, strict: bool = True, wrap_numerical: bool = False) -> Self`
Cast between data types.

### `cbrt() -> Series`
Compute the cube root of the elements.

### `ceil() -> Series`
Rounds up to the nearest integer value.

### `chunk_lengths() -> list[int]`
Get the length of each individual chunk.

### `clear(n: int = 0) -> Series`
Create an empty copy of the current Series, with zero to 'n' elements.

### `clip(lower_bound: NumericLiteral | TemporalLiteral | IntoExprColumn | None = None, upper_bound: NumericLiteral | TemporalLiteral | IntoExprColumn | None = None) -> Series`
Set values outside the given boundaries to the boundary value.

### `clone() -> Self`
Create a copy of this Series.

### `cos() -> Series`
Compute the element-wise value for the cosine.

### `cosh() -> Series`
Compute the element-wise value for the hyperbolic cosine.

### `cot() -> Series`
Compute the element-wise value for the cotangent.

### `cum_count(*, reverse: bool = False) -> Self`
Return the cumulative count of the non-null values in the column.

### `cum_max(*, reverse: bool = False) -> Series`
Get an array with the cumulative max computed at every element.

### `cum_min(*, reverse: bool = False) -> Series`
Get an array with the cumulative min computed at every element.

### `cum_prod(*, reverse: bool = False) -> Series`
Get an array with the cumulative product computed at every element.

### `cum_sum(*, reverse: bool = False) -> Series`
Get an array with the cumulative sum computed at every element.

### `cumulative_eval(expr: Expr, *, min_samples: int = 1, parallel: bool = False) -> Series`
Run an expression over a sliding window that increases `1` slot every iteration.

### `cut(breaks: Sequence[float], *, labels: Sequence[str] | None = None, left_closed: bool = False, include_breaks: bool = False) -> Series`
Bin continuous values into discrete categories.

### `describe(percentiles: Sequence[float] | float | None = (0.25, 0.50, 0.75), interpolation: QuantileMethod = "nearest") -> DataFrame`
Quick summary statistics of a Series.

### `diff(n: int = 1, null_behavior: NullBehavior = "ignore") -> Series`
Calculate the first discrete difference between shifted items.

### `drop_nans() -> Series`
Drop all floating point NaN values.

### `drop_nulls() -> Series`
Drop all null values.

### `dot(other: Series | ArrayLike) -> int | float | None`
Compute the dot/inner product between two Series.

### `entropy(base: float = math.e, *, normalize: bool = True) -> float | None`
Computes the entropy.

### `eq(other: Any) -> Series | Expr`
Method equivalent of operator expression `series == other`.

### `eq_missing(other: Any) -> Series | Expr`
Method equivalent of equality operator `series == other` where `None == None`.

### `equals(other: Series, *, check_dtypes: bool = False, check_names: bool = False, null_equal: bool = True) -> bool`
Check whether the Series is equal to another Series.

### `estimated_size(unit: SizeUnit = "b") -> int | float`
Return an estimation of the total (heap) allocated size of the Series.

### `ewm_mean(*, com: float | None = None, span: float | None = None, half_life: float | None = None, alpha: float | None = None, adjust: bool = True, min_samples: int = 1, ignore_nulls: bool = False) -> Series`
Compute exponentially-weighted moving average.

### `ewm_mean_by(by: IntoExpr, *, half_life: str | timedelta) -> Series`
Compute time-based exponentially weighted moving average.

### `ewm_std(*, com: float | None = None, span: float | None = None, half_life: float | None = None, alpha: float | None = None, adjust: bool = True, bias: bool = False, min_samples: int = 1, ignore_nulls: bool = False) -> Series`
Compute exponentially-weighted moving standard deviation.

### `ewm_var(*, com: float | None = None, span: float | None = None, half_life: float | None = None, alpha: float | None = None, adjust: bool = True, bias: bool = False, min_samples: int = 1, ignore_nulls: bool = False) -> Series`
Compute exponentially-weighted moving variance.

### `exp() -> Series`
Compute the exponential, element-wise.

### `extend(other: Series) -> Self`
Extend the memory backed by this Series with the values from another.

### `extend_constant(value: IntoExpr, n: int | IntoExprColumn) -> Series`
Extremely fast method for extending the Series with 'n' copies of a value.

### `fill_nan(value: int | float | Expr | None) -> Series`
Fill floating point NaN value with a fill value.

### `fill_null(value: Any | Expr | None = None, strategy: FillNullStrategy | None = None, limit: int | None = None) -> Series`
Fill null values using the specified value or strategy.

### `filter(predicate: Series | Iterable[bool]) -> Self`
Filter elements by a boolean mask.

### `first(*, ignore_nulls: bool = False) -> PythonLiteral | None`
Get the first element of the Series.

### `floor() -> Series`
Rounds down to the nearest integer value.

### `forward_fill(limit: int | None = None) -> Series`
Fill missing values with the last non-null value.

### `gather(indices: int | list[int] | Expr | Series | np.ndarray[Any, Any]) -> Series`
Take values by index.

### `gather_every(n: int, offset: int = 0) -> Series`
Take every nth value in the Series and return as new Series.

### `get_chunks() -> list[Series]`
Get the chunks of this Series as a list of Series.

### `has_nulls() -> bool`
Check whether the Series contains one or more null values.

### `has_validity() -> bool`
Check whether the Series contains one or more null values.

### `hash(seed: int = 0, seed_1: int | None = None, seed_2: int | None = None, seed_3: int | None = None) -> Series`
Hash the Series.

### `head(n: int = 10) -> Series`
Get the first `n` elements.

### `hist(bins: list[float] | None = None, *, bin_count: int | None = None, include_category: bool = True, include_breakpoint: bool = True) -> DataFrame`
Bin values into buckets and count their occurrences.

### `implode() -> Self`
Aggregate values into a list.

### `index_of(element: IntoExpr) -> int | None`
Get the index of the first occurrence of a value, or `None` if it's not found.

### `interpolate(method: InterpolationMethod = "linear") -> Series`
Interpolate intermediate values.

### `interpolate_by(by: IntoExpr) -> Series`
Interpolate intermediate values with x-coordinate based on another column.

### `is_between(lower_bound: IntoExpr, upper_bound: IntoExpr, closed: ClosedInterval = "both") -> Series`
Get a boolean mask of the values that are between the given lower/upper bounds.

### `is_close(other: IntoExpr, *, abs_tol: float = 0.0, rel_tol: float = 1e-09, nans_equal: bool = False) -> Series`
Get a boolean mask of the values being close to the other values.

### `is_duplicated() -> Series`
Get mask of all duplicated values.

### `is_empty() -> bool`
Check if the Series is empty.

### `is_finite() -> Series`
Returns a boolean Series indicating which values are finite.

### `is_first_distinct() -> Series`
Return a boolean mask indicating the first occurrence of each distinct value.

### `is_in(other: Series | Collection[Any], *, nulls_equal: bool = False) -> Series`
Check if elements of this Series are in the other Series.

### `is_infinite() -> Series`
Returns a boolean Series indicating which values are infinite.

### `is_last_distinct() -> Series`
Return a boolean mask indicating the last occurrence of each distinct value.

### `is_nan() -> Series`
Returns a boolean Series indicating which values are NaN.

### `is_not_nan() -> Series`
Returns a boolean Series indicating which values are not NaN.

### `is_not_null() -> Series`
Returns a boolean Series indicating which values are not null.

### `is_null() -> Series`
Returns a boolean Series indicating which values are null.

### `is_sorted(*, descending: bool = False, nulls_last: bool = False) -> bool`
Check if the Series is sorted.

### `is_unique() -> Series`
Get mask of all unique values.

### `item(index: int | None = None) -> Any`
Return the Series as a scalar, or return the element at the given index.

### `kurtosis(*, fisher: bool = True, bias: bool = True) -> float | None`
Compute the kurtosis (Fisher or Pearson) of a dataset.

### `last(*, ignore_nulls: bool = False) -> PythonLiteral | None`
Get the last element of the Series.

### `le(other: Any) -> Series | Expr`
Method equivalent of operator expression `series <= other`.

### `len() -> int`
Return the number of elements in the Series.

### `limit(n: int = 10) -> Series`
Get the first `n` elements.

### `log(base: float | Series = math.e) -> Series`
Compute the logarithm to a given base.

### `log10() -> Series`
Compute the base 10 logarithm of the input array, element-wise.

### `log1p() -> Series`
Compute the natural logarithm of the input array plus one, element-wise.

### `lower_bound() -> Self`
Return the lower bound of this Series' dtype as a unit Series.

### `lt(other: Any) -> Series | Expr`
Method equivalent of operator expression `series < other`.

### `map_elements(function: Callable[[Any], Any], return_dtype: PolarsDataType | None = None, *, skip_nulls: bool = True) -> Self`
Map a custom/user-defined function (UDF) over elements in this Series.

### `max() -> PythonLiteral | None`
Get the maximum value in this Series.

### `max_by(by: IntoExpr) -> Expr`
Get the maximum value in this Series, ordered by an expression.

### `mean() -> PythonLiteral | None`
Reduce this Series to the mean value.

### `median() -> PythonLiteral | None`
Get the median of this Series.

### `min() -> PythonLiteral | None`
Get the minimal value in this Series.

### `min_by(by: IntoExpr) -> Expr`
Get the minimum value in this Series, ordered by an expression.

### `mode(*, maintain_order: bool = False) -> Series`
Compute the most occurring value(s).

### `mod(other: Any) -> Series | Expr`
Method equivalent of operator expression `series % other`.

### `nan_max() -> int | float | date | datetime | timedelta | str`
Get maximum value, but propagate/poison encountered NaN values.

### `nan_min() -> int | float | date | datetime | timedelta | str`
Get minimum value, but propagate/poison encountered NaN values.

### `n_chunks() -> int`
Get the number of chunks that this Series contains.

### `ne(other: Any) -> Series | Expr`
Method equivalent of operator expression `series != other`.

### `ne_missing(other: Any) -> Series | Expr`
Method equivalent of equality operator `series != other` where `None == None`.

### `new_from_index(index: int, length: int) -> Self`
Create a new Series filled with values from the given index.

### `not_() -> Series`
Negate a boolean Series.

### `null_count() -> int`
Count the null values in this Series.

### `n_unique() -> int`
Count the number of unique values in this Series.

### `pct_change(n: int | IntoExprColumn = 1) -> Series`
Computes percentage change between values.

### `peak_max() -> Self`
Get a boolean mask of the local maximum peaks.

### `peak_min() -> Self`
Get a boolean mask of the local minimum peaks.

### `pow(exponent: int | float | Series) -> Series`
Raise to the power of the given exponent.

### `product() -> int | float`
Reduce this Series to the product value.

### `qcut(quantiles: Sequence[float] | int, *, labels: Sequence[str] | None = None, left_closed: bool = False, allow_duplicates: bool = False, include_breaks: bool = False) -> Series`
Bin continuous values into discrete categories based on their quantiles.

### `quantile(quantile: float | list[float], interpolation: QuantileMethod = "nearest") -> float | None | list[float] | list[None]`
Get the quantile value of this Series.

### `rank(method: RankMethod = "average", *, descending: bool = False, seed: int | None = None) -> Series`
Assign ranks to data, dealing with ties appropriately.

### `rechunk(*, in_place: bool = False) -> Self`
Create a single chunk of memory for this Series.

### `reinterpret(*, signed: bool | None = None, dtype: type[int | float] | PolarsDataType | None = None) -> Series`
Reinterpret the underlying bits as a signed/unsigned integer or float.

### `rename(name: str) -> Series`
Rename this Series.

### `repeat_by(by: int | IntoExprColumn) -> Self`
Repeat the elements in this Series as specified in the given expression.

### `replace(old: IntoExpr | Sequence[Any] | Mapping[Any, Any], new: IntoExpr | Sequence[Any] | NoDefault = NO_DEFAULT, *, default: IntoExpr | NoDefault = NO_DEFAULT, return_dtype: PolarsDataType | None = None) -> Self`
Replace values by different values of the same data type.

### `replace_strict(old: IntoExpr | Sequence[Any] | Mapping[Any, Any], new: IntoExpr | Sequence[Any] | NoDefault = NO_DEFAULT, *, default: IntoExpr | NoDefault = NO_DEFAULT, return_dtype: PolarsDataType | None = None) -> Self`
Replace all values by different values.

### `reshape(dimensions: tuple[int, ...]) -> Series`
Reshape this Series to a flat Series or an Array Series.

### `reverse() -> Series`
Return Series in reverse order.

### `rle() -> Series`
Compress the Series data using run-length encoding.

### `rle_id() -> Series`
Get a distinct integer ID for each run of identical values.

### `rolling_kurtosis(window_size: int, *, fisher: bool = True, bias: bool = True, min_samples: int | None = None, center: bool = False) -> Series`
Compute a rolling kurtosis.

### `rolling_map(function: Callable[[Series], Any], window_size: int, weights: list[float] | None = None, *, min_samples: int | None = None, center: bool = False) -> Series`
Compute a custom rolling window function.

### `rolling_max(window_size: int, weights: list[float] | None = None, *, min_samples: int | None = None, center: bool = False) -> Series`
Apply a rolling max (moving max) over the values in this array.

### `rolling_max_by(by: IntoExpr, window_size: timedelta | str, *, min_samples: int = 1, closed: ClosedInterval = "right") -> Self`
Compute a rolling max based on another series.

### `rolling_mean(window_size: int, weights: list[float] | None = None, *, min_samples: int | None = None, center: bool = False) -> Series`
Apply a rolling mean (moving mean) over the values in this array.

### `rolling_mean_by(by: IntoExpr, window_size: timedelta | str, *, min_samples: int = 1, closed: ClosedInterval = "right") -> Self`
Compute a rolling mean based on another series.

### `rolling_median(window_size: int, weights: list[float] | None = None, *, min_samples: int | None = None, center: bool = False) -> Series`
Compute a rolling median.

### `rolling_median_by(by: IntoExpr, window_size: timedelta | str, *, min_samples: int = 1, closed: ClosedInterval = "right") -> Self`
Compute a rolling median based on another series.

### `rolling_min(window_size: int, weights: list[float] | None = None, *, min_samples: int | None = None, center: bool = False) -> Series`
Apply a rolling min (moving min) over the values in this array.

### `rolling_min_by(by: IntoExpr, window_size: timedelta | str, *, min_samples: int = 1, closed: ClosedInterval = "right") -> Self`
Compute a rolling min based on another series.

### `rolling_quantile(quantile: float, interpolation: QuantileMethod = "nearest", window_size: int = 2, weights: list[float] | None = None, *, min_samples: int | None = None, center: bool = False) -> Series`
Compute a rolling quantile.

### `rolling_quantile_by(by: IntoExpr, window_size: timedelta | str, *, quantile: float, interpolation: QuantileMethod = "nearest", min_samples: int = 1, closed: ClosedInterval = "right") -> Self`
Compute a rolling quantile based on another series.

### `rolling_rank(window_size: int, method: RankMethod = "average", *, seed: int | None = None, min_samples: int | None = None, center: bool = False) -> Series`
Compute a rolling rank.

### `rolling_rank_by(by: IntoExpr, window_size: timedelta | str, method: RankMethod = "average", *, seed: int | None = None, min_samples: int = 1, closed: ClosedInterval = "right") -> Series`
Compute a rolling rank based on another column.

### `rolling_skew(window_size: int, *, bias: bool = True, min_samples: int | None = None, center: bool = False) -> Series`
Compute a rolling skew.

### `rolling_std(window_size: int, weights: list[float] | None = None, *, min_samples: int | None = None, center: bool = False, ddof: int = 1) -> Series`
Compute a rolling std dev.

### `rolling_std_by(by: IntoExpr, window_size: timedelta | str, *, min_samples: int = 1, closed: ClosedInterval = "right", ddof: int = 1) -> Self`
Compute a rolling standard deviation based on another series.

### `rolling_sum(window_size: int, weights: list[float] | None = None, *, min_samples: int | None = None, center: bool = False) -> Series`
Apply a rolling sum (moving sum) over the values in this array.

### `rolling_sum_by(by: IntoExpr, window_size: timedelta | str, *, min_samples: int = 1, closed: ClosedInterval = "right") -> Self`
Compute a rolling sum based on another series.

### `rolling_var(window_size: int, weights: list[float] | None = None, *, min_samples: int | None = None, center: bool = False, ddof: int = 1) -> Series`
Compute a rolling variance.

### `rolling_var_by(by: IntoExpr, window_size: timedelta | str, *, min_samples: int = 1, closed: ClosedInterval = "right", ddof: int = 1) -> Self`
Compute a rolling variance based on another series.

### `round(decimals: int = 0, mode: RoundMode = "half_to_even") -> Series`
Round underlying floating point data by `decimals` digits.

### `round_sig_figs(digits: int) -> Series`
Round to a number of significant figures.

### `sample(n: int | None = None, *, fraction: float | None = None, with_replacement: bool = False, shuffle: bool = False, seed: int | None = None) -> Series`
Sample from this Series.

### `scatter(indices: Series | Iterable[int] | int | np.ndarray[Any, Any], values: Series | Iterable[PythonLiteral] | PythonLiteral | None) -> Series`
Set values at the index locations.

### `search_sorted(element: IntoExpr | np.ndarray[Any, Any] | None, side: SearchSortedSide = "any", *, descending: bool = False) -> int | Series`
Find indices where elements should be inserted to maintain order.

### `set(filter: Series, value: Any) -> Series`
Set masked values.

### `set_sorted(*, descending: bool = False) -> Self`
Flags the Series as 'sorted'.

### `shift(n: int = 1, *, fill_value: IntoExpr | None = None) -> Series`
Shift values by the given number of indices.

### `shrink_dtype() -> Series`
Shrink numeric columns to the minimal required datatype.

### `shrink_to_fit(*, in_place: bool = False) -> Series`
Shrink Series memory usage.

### `shuffle(seed: int | None = None) -> Series`
Shuffle the contents of this Series.

### `sign() -> Series`
Compute the element-wise sign function on numeric types.

### `sin() -> Series`
Compute the element-wise value for the sine.

### `sinh() -> Series`
Compute the element-wise value for the hyperbolic sine.

### `skew(*, bias: bool = True) -> float | None`
Compute the sample skewness of a data set.

### `slice(offset: int, length: int | None = None) -> Series`
Get a slice of this Series.

### `sort(*, descending: bool = False, nulls_last: bool = False, multithreaded: bool = True, in_place: bool = False) -> Self`
Sort this Series.

### `sql(query: str, *, table_name: str = "self") -> DataFrame`
Execute a SQL query against the Series.

### `sqrt() -> Series`
Compute the square root of the elements.

### `std(ddof: int = 1) -> float | timedelta | None`
Get the standard deviation of this Series.

### `sub(other: Any) -> Series | Expr`
Method equivalent of subtraction operator `series - other`.

### `sum() -> int | float | PyDecimal`
Reduce this Series to the sum value.

### `tail(n: int = 10) -> Series`
Get the last `n` elements.

### `tan() -> Series`
Compute the element-wise value for the tangent.

### `tanh() -> Series`
Compute the element-wise value for the hyperbolic tangent.

### `to_arrow(*, compat_level: CompatLevel | None = None) -> pa.Array`
Return the underlying Arrow array.

### `to_dummies(*, separator: str = "_", drop_first: bool = False, drop_nulls: bool = False) -> DataFrame`
Get dummy/indicator variables.

### `to_frame(name: str | None = None) -> DataFrame`
Cast this Series to a DataFrame.

### `to_init_repr(n: int = 1000) -> str`
Convert Series to instantiable string representation.

### `to_jax(device: jax.Device | str | None = None) -> jax.Array`
Convert this Series to a Jax Array.

### `to_list() -> list[Any]`
Convert this Series to a Python list.

### `to_numpy(*, writable: bool = False, allow_copy: bool = True, use_pyarrow: bool | None = None, zero_copy_only: bool | None = None) -> np.ndarray[Any, Any]`
Convert this Series to a NumPy ndarray.

### `to_pandas(*, use_pyarrow_extension_array: bool = False, **kwargs: Any) -> pd.Series[Any]`
Convert this Series to a pandas Series.

### `to_physical() -> Series`
Cast to physical representation of the logical dtype.

### `to_torch() -> torch.Tensor`
Convert this Series to a PyTorch Tensor.

### `top_k(k: int = 5) -> Series`
Return the `k` largest elements.

### `top_k_by(by: IntoExpr | Iterable[IntoExpr], k: int = 5, *, reverse: bool | Sequence[bool] = False) -> Series`
Return the `k` largest elements of the `by` column.

### `truncate(decimals: int = 0) -> Series`
Truncate numeric data toward zero to `decimals` number of decimal places.

### `unique(*, maintain_order: bool = False) -> Series`
Get unique elements in series.

### `unique_counts() -> Series`
Return a count of the unique values in the order of appearance.

### `upper_bound() -> Self`
Return the upper bound of this Series' dtype as a unit Series.

### `value_counts(*, sort: bool = False, parallel: bool = False, name: str | None = None, normalize: bool = False) -> DataFrame`
Count the occurrences of unique values.

### `var(ddof: int = 1) -> float | timedelta | None`
Get variance of this Series.

### `zip_with(mask: Series, other: Series) -> Self`
Take values from self or other based on the given mask.
