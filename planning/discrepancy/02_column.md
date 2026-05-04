# Column vs Series

## Polars has, Portabellas doesn't

### Aggregation

| Polars (Series) | Notes |
|---|---|
| `sum()` | Sum of values |
| `product()` | Product of values |
| `std(ddof)` / `var(ddof)` | Standard deviation / variance |
| `quantile(quantile, interpolation)` | Quantile value |
| `approx_n_unique()` | Approximate unique count |
| `kurtosis(*, fisher, bias)` | Kurtosis |
| `skew(*, bias)` | Skewness |
| `entropy(base, *, normalize)` | Entropy |
| `nan_max()` / `nan_min()` | Max/min propagating NaN |

### Cumulative & Rolling

| Polars | Notes |
|---|---|
| `cum_count(*, reverse)` | Cumulative non-null count |
| `cum_max(*, reverse)` | Cumulative max |
| `cum_min(*, reverse)` | Cumulative min |
| `cum_prod(*, reverse)` | Cumulative product |
| `cum_sum(*, reverse)` | Cumulative sum |
| `cumulative_eval(expr, *, min_samples, parallel)` | Custom cumulative eval |
| `diff(n, null_behavior)` | First discrete difference |
| `pct_change(n)` | Percentage change |
| `ewm_mean(*, com, span, half_life, alpha, ...)` | Exponentially-weighted moving avg |
| `ewm_mean_by(by, *, half_life)` | Time-based EWM mean |
| `ewm_std(*)` / `ewm_var(*)` | EWM std/var |
| `rolling_*` (22 methods) | Rolling window stats (sum, mean, min, max, std, var, median, quantile, skew, kurtosis, rank, map) |
| `peak_max()` / `peak_min()` | Local maxima/minima |

### Filtering & searching

| Polars | Notes |
|---|---|
| `filter(predicate)` | Filter by boolean mask |
| `gather(indices)` | Take values by index |
| `gather_every(n, offset)` | Take every nth value |
| `search_sorted(element, side, *, descending)` | Binary search |
| `arg_max()` / `arg_min()` | Index of max/min value |
| `arg_sort(*, descending, nulls_last)` | Indices that would sort |
| `arg_true()` | Indices where True |
| `arg_unique()` | Index of first unique value |
| `index_of(element)` | Index of first occurrence |
| `is_between(lower, upper, closed)` | Between bounds check |
| `is_close(other, *, abs_tol, rel_tol, nans_equal)` | Approximate equality |
| `is_duplicated()` / `is_unique()` | Duplicate/unique mask |
| `is_finite()` / `is_infinite()` | Finite/infinite check |
| `is_first_distinct()` / `is_last_distinct()` | First/last occurrence mask |
| `is_in(other, *, nulls_equal)` | Membership check |
| `is_nan()` / `is_not_nan()` | NaN check |
| `is_null()` / `is_not_null()` | Null check |
| `is_sorted(*, descending, nulls_last)` | Check if sorted |
| `has_nulls()` / `has_validity()` | Null checks |
| `is_empty()` | Empty check |

### Missing values

| Polars | Notes |
|---|---|
| `fill_null(value, strategy, limit)` | Fill nulls |
| `fill_nan(value)` | Fill NaN |
| `forward_fill(limit)` / `backward_fill(limit)` | Fill with adjacent |
| `drop_nans()` / `drop_nulls()` | Drop NaN/null values |
| `interpolate(method)` / `interpolate_by(by)` | Interpolation |
| `null_count()` | Count nulls |

### Sorting & ordering

| Polars | Notes |
|---|---|
| `sort(*, descending, nulls_last, multithreaded, in_place)` | Sort |
| `reverse()` | Reverse order |
| `shift(n, *, fill_value)` | Shift values |
| `set_sorted(*, descending)` | Flag as sorted |
| `shuffle(seed)` | Random shuffle |
| `sample(n, *, fraction, with_replacement, shuffle, seed)` | Random sample |
| `rank(method, *, descending, seed)` | Rank values |
| `top_k(k)` / `bottom_k(k)` | Top/bottom k |
| `top_k_by(by, k, *, reverse)` / `bottom_k_by(by, k, *, reverse)` | Top/bottom by other column |

### Type operations

| Polars | Notes |
|---|---|
| `cast(dtype, *, strict, wrap_numerical)` | Cast type |
| `shrink_dtype()` | Shrink to minimal dtype |
| `reinterpret(*, signed, dtype)` | Reinterpret bits |
| `to_physical()` | Cast to physical representation |
| `reshape(dimensions)` | Reshape |

### String-like operations on Series level

| Polars | Notes |
|---|---|
| `cut(breaks, *, labels, left_closed, include_breaks)` | Bin continuous values |
| `qcut(quantiles, *, labels, left_closed, allow_duplicates, include_breaks)` | Quantile-based binning |
| `rle()` / `rle_id()` | Run-length encoding |
| `hist(bins, *, bin_count, include_category, include_breakpoint)` | Histogram |
| `value_counts(*, sort, parallel, name, normalize)` | Value counts |
| `unique_counts()` | Count of each unique value |
| `clip(lower_bound, upper_bound)` | Clip values |
| `replace(old, new, *, default, return_dtype)` | Replace values |
| `replace_strict(old, new, *, default, return_dtype)` | Strict replace |
| `repeat_by(by)` | Repeat elements |

### Math on Series

| Polars | Notes |
|---|---|
| `abs()` / `sign()` | Absolute value / sign |
| `ceil()` / `floor()` / `round(decimals, mode)` / `round_sig_figs(digits)` | Rounding |
| `truncate(decimals)` | Truncate |
| `sqrt()` / `cbrt()` | Square/cube root |
| `exp()` | Exponential |
| `log(base)` / `log10()` / `log1p()` | Logarithms |
| `sin/cos/tan/sinh/cosh/tanh/arcsin/arccos/arctan/arcsinh/arccosh/arctanh/cot()` | Trig |
| `pow(exponent)` | Power |
| `dot(other)` | Dot product |
| `lower_bound()` / `upper_bound()` | Dtype bounds |

### Bitwise operations

| Polars | Notes |
|---|---|
| `bitwise_and()` / `bitwise_or()` / `bitwise_xor()` | Bitwise aggregation |
| `bitwise_count_ones()` / `bitwise_count_zeros()` | Count set/unset bits |
| `bitwise_leading_ones()` / `bitwise_leading_zeros()` | Leading set/unset bits |
| `bitwise_trailing_ones()` / `bitwise_trailing_zeros()` | Trailing set/unset bits |

### Chunk & memory operations

| Polars | Notes |
|---|---|
| `chunk_lengths()` | Length of each chunk |
| `get_chunks()` | Get chunks as list |
| `n_chunks()` | Number of chunks |
| `rechunk(*, in_place)` | Contiguous allocation |
| `estimated_size(unit)` | Memory estimation |
| `shrink_to_fit(*, in_place)` | Reduce memory |

### Append & extend

| Polars | Notes |
|---|---|
| `append(other)` | Append Series |
| `extend(other)` | Extend memory |
| `extend_constant(value, n)` | Extend with constant |

### Conversion

| Polars | Notes |
|---|---|
| `to_arrow()` / `to_numpy()` / `to_pandas()` | Convert to other formats |
| `to_dummies()` | One-hot encoding |
| `to_frame(name)` | Convert to DataFrame |
| `to_init_repr(n)` | Instantiable string |
| `to_jax()` / `to_torch()` | ML framework interop |
| `to_list()` | To Python list |
| `to_physical()` | Physical dtype |
| `item(index)` | Get scalar |

### Misc

| Polars | Notes |
|---|---|
| `describe(percentiles, interpolation)` | Summary statistics |
| `equals(other, *, check_dtypes, check_names, null_equal)` | Equality check |
| `scatter(indices, values)` | Set values at indices |
| `set(filter, value)` | Set masked values |
| `zip_with(mask, other)` | Conditional select |
| `sql(query, *, table_name)` | SQL query |
| `new_from_index(index, length)` | Repeat value at index |
| `not_()` | Negate boolean |
| `mode(*, maintain_order)` | Most frequent value(s) |
| `map_elements(function, return_dtype, *, skip_nulls)` | Map UDF |
| `min_by(by)` / `max_by(by)` | Min/max by other column |
| `eq(other)` / `ne(other)` / `lt(other)` / `le(other)` / `gt(other)` / `ge(other)` | Named comparison methods |
| `eq_missing(other)` / `ne_missing(other)` | Equality with null == null |

---

## Portabellas has, Polars doesn't

| Portabellas (Column) | Notes |
|---|---|
| `map(mapper)` | Transform via Cell-callback (Polars has `map_elements` but it's eager row-by-row) |
| `all(predicate, *, ignore_unknown)` | Universal quantifier with Cell-callback |
| `any(predicate, *, ignore_unknown)` | Existential quantifier with Cell-callback |
| `none(predicate, *, ignore_unknown)` | No-value quantifier with Cell-callback |
| `count_if(predicate, *, ignore_unknown)` | Count satisfying Cell-predicate |
| `correlation_with(other)` | Pearson correlation with another Column |
| `summarize_statistics()` | Summary statistics table (Polars: `describe()`) |
| `to_table()` | Convert single column to Table |
| `distinct_values(*, ignore_missing_values)` | Get distinct values (Polars: `unique()`) |
| `missing_value_count()` | Count missing values (Polars: `null_count()`) |
| `distinct_value_count(*, ignore_missing_values)` | Count distinct values (Polars: `n_unique()`) |
| `rename(new_name)` | Rename column (Polars: `alias(name)`) |

---

## Both have but with different APIs

| Feature | Portabellas | Polars | Difference |
|---|---|---|---|
| Row count | `column.row_count` | `series.len()` / `len(series)` | Property vs method |
| Type | `column.type` | `series.dtype` | Property name |
| Name | `column.name` | `series.name` | Same |
| Get value | `column.get_value(index)` | `series[index]` / `series.item(index)` | Method vs indexing |
| Max/Min/Mean/Median | `column.max()` / `.min()` / `.mean()` / `.median()` | `series.max()` / `.min()` / `.mean()` / `.median()` | Similar; Polars returns None on empty, Portabellas too |
| Mode | `column.mode(*, ignore_missing_values)` | `series.mode(*, maintain_order)` | Different parameter |
| Standard deviation | `column.standard_deviation()` | `series.std(ddof)` | Name and ddof param |
| Variance | `column.variance()` | `series.var(ddof)` | Name and ddof param |
