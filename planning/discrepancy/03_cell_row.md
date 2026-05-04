# Cell & Row vs Expr

## Polars has, Portabellas doesn't

### Expr methods not on Cell

| Polars (Expr) | Notes |
|---|---|
| `agg_groups()` | Group indices |
| `append(other, *, upcast)` | Append expressions |
| `cum_count/cum_max/cum_min/cum_prod/cum_sum` | Cumulative operations |
| `cumulative_eval(expr, *, min_samples)` | Custom cumulative eval |
| `degrees()` / `radians()` | Angle conversion |
| `diff(n, null_behavior)` | Discrete difference |
| `drop_nans()` / `drop_nulls()` | Drop NaN/null |
| `entropy(base, *, normalize)` | Entropy |
| `eq_missing(other)` / `ne_missing(other)` | Equality with null == null |
| `exclude(columns)` | Exclude columns from selection |
| `explode(*, empty_as_null, keep_nulls)` | Explode list |
| `extend_constant(value, n)` | Extend with constant |
| `fill_nan(value)` / `fill_null(value, strategy, limit)` | Fill missing |
| `filter(*predicates)` | Filter expression |
| `forward_fill(limit)` / `backward_fill(limit)` | Fill with adjacent |
| `get(index, *, null_on_oob)` | Get by index |
| `has_nulls()` | Check for nulls |
| `head(n)` / `tail(n)` / `limit(n)` | First/last n |
| `hist(bins, *, bin_count, ...)` | Histogram |
| `implode(*, maintain_order)` | Aggregate to list |
| `index_of(element)` | Index of first occurrence |
| `inspect(fmt)` | Debug inspect |
| `interpolate(method)` / `interpolate_by(by)` | Interpolation |
| `is_between(lower, upper, closed)` | Between bounds |
| `is_close(other, *, abs_tol, rel_tol, nans_equal)` | Approximate equality |
| `is_duplicated()` / `is_unique()` | Duplicate/unique mask |
| `is_finite()` / `is_infinite()` | Finite/infinite |
| `is_first_distinct()` / `is_last_distinct()` | First/last distinct |
| `is_in(other, *, nulls_equal)` | Membership |
| `is_nan()` / `is_not_nan()` / `is_null()` / `is_not_null()` | Null/NaN checks |
| `kurtosis(*, fisher, bias)` / `skew(*, bias)` | Shape statistics |
| `map_batches(function, *, ...)` | Custom batch function |
| `map_elements(function, *, skip_nulls, pass_name, strategy)` | Map UDF per element |
| `nan_max()` / `nan_min()` | Max/min with NaN propagation |
| `null_count()` | Count nulls |
| `n_unique()` | Count unique |
| `over(partition_by, *, order_by, ...)` | Window function |
| `pct_change(n)` | Percentage change |
| `peak_max()` / `peak_min()` | Local peaks |
| `pipe(function, *args, **kwargs)` | Pipeable |
| `qcut(quantiles, *, ...)` / `cut(breaks, *, ...)` | Binning |
| `quantile(quantile, interpolation)` | Quantile value |
| `rank(method, *, descending, seed)` | Rank |
| `rechunk()` | Contiguous memory |
| `register_plugin(*, lib, symbol, ...)` | Plugin registration |
| `reinterpret(*, signed, dtype)` | Reinterpret bits |
| `replace(old, new, *, default, return_dtype)` | Replace values |
| `replace_strict(old, new, *, ...)` | Strict replace |
| `repeat_by(by)` | Repeat elements |
| `reshape(dimensions)` | Reshape |
| `rle()` / `rle_id()` | Run-length encoding |
| `rolling(*, period, offset, closed)` | Rolling groups |
| `rolling_kurtosis/rolling_map/rolling_max/rolling_mean/rolling_median/rolling_min/rolling_quantile/rolling_rank/rolling_skew/rolling_std/rolling_sum/rolling_var` (plus `*_by` variants) | Rolling window functions |
| `search_sorted(element, side, *, descending)` | Binary search |
| `set_sorted(*, descending, nulls_last)` | Flag sorted |
| `shift(n, *, fill_value)` | Shift values |
| `shrink_dtype()` | Shrink to minimal dtype |
| `shuffle(seed)` | Random shuffle |
| `sample(n, *, fraction, with_replacement, shuffle, seed)` | Random sample |
| `sort(*, descending, nulls_last)` | Sort |
| `sort_by(by, *, descending, nulls_last, multithreaded, maintain_order)` | Sort by other |
| `to_physical()` | Physical dtype |
| `top_k(k)` / `bottom_k(k)` | Top/bottom k |
| `top_k_by(by, k, *, reverse)` / `bottom_k_by(by, k, *, reverse)` | Top/bottom by other |
| `truncate(decimals)` | Truncate |
| `unique(*, maintain_order)` | Unique values |
| `unique_counts()` | Unique value counts |
| `upper_bound()` / `lower_bound()` | Dtype bounds |
| `value_counts(*, sort, parallel, name, normalize)` | Value counts |
| `where(predicate)` | Filter (deprecated) |

### Expr namespaces not on Cell

| Polars | Notes |
|---|---|
| `expr.cat` | Categorical operations |
| `expr.bin` | Binary operations |
| `expr.arr` | Fixed-size array operations |
| `expr.meta` | Expression introspection |
| `expr.name` | Expression name manipulation |
| `expr.ext` | Extension type operations |

### Row: Polars has no equivalent

Polars has no `Row` object. Rows are accessed via `df.row(index)` or `df.iter_rows()`, which return Python tuples/dicts, not lazy Row objects.

---

## Portabellas has, Polars doesn't

| Portabellas | Notes |
|---|---|
| `Cell.constant(value, *, type)` | Create constant Cell (Polars: `pl.lit(value)`) |
| `Cell.date(year, month, day)` | Create date Cell (Polars: `pl.date(year, month, day)`) |
| `Cell.datetime(year, month, day, hour, minute, second, *, microsecond, time_zone)` | Create datetime Cell (Polars: `pl.datetime(...)`) |
| `Cell.duration(*, weeks, days, hours, ...)` | Create duration Cell (Polars: `pl.duration(...)`) |
| `Cell.time(hour, minute, second, *, microsecond)` | Create time Cell (Polars: `pl.time(...)`) |
| `Cell.first_not_none(cells)` | Coalesce (Polars: `pl.coalesce(*exprs)`) |
| `Row` ABC / `ExprRow` | Lazy row object for callbacks; no Polars equivalent |
| `cell.eq(other, *, propagate_missing_values)` | Eq with null propagation control (Polars: `eq` vs `eq_missing`) |
| `cell.neq(other, *, propagate_missing_values)` | Neq with null propagation control |
| `cell.not_()` / `cell.and_()` / `cell.or_()` / `cell.xor()` | Named boolean methods (Polars: operators or `not_()`, `and_()`, `or_()`) |
| `cell.neg()` / `cell.add()` / `cell.div()` / `cell.mod()` / `cell.mul()` / `cell.pow()` / `cell.sub()` | Named arithmetic methods (Polars: operators or `add/sub/mul/mod/pow`) |
| `cell.eq/neq/ge/gt/le/lt` | Named comparison methods (Polars: `eq/ne/ge/gt/le/lt`) |

---

## Both have but with different APIs

| Feature | Portabellas (Cell) | Polars (Expr) | Difference |
|---|---|---|---|
| Cast | `cell.cast(type)` | `expr.cast(dtype, *, strict, wrap_numerical)` | Polars has strict/wrap_numerical |
| Abs | `cell.math.abs()` / `__abs__` | `expr.abs()` | Portabellas: namespace; Polars: direct |
| Ceil/Floor | `cell.math.ceil()` / `cell.math.floor()` / `__ceil__` / `__floor__` | `expr.ceil()` / `expr.floor()` | Portabellas: namespace; Polars: direct |
| Neg | `cell.neg()` / `__neg__` | `expr.neg()` / `__neg__` | Similar |
| Trig | `cell.math.sin/cos/tan/asin/acos/atan/...` | `expr.sin/cos/tan/arcsin/arccos/arctan/...` | Different names (asin vs arcsin) |
| Exp/Log | `cell.math.exp/ln/log/log10` | `expr.exp/log/log10/log1p` | Portabellas missing log1p |
| Sqrt/Cbrt | `cell.math.sqrt/cbrt` | `expr.sqrt/cbrt` | Same |
| Sign | `cell.math.sign()` | `expr.sign()` | Same |
| Round | `cell.math.round_to_decimal_places(n)` / `round_to_significant_figures(n)` | `expr.round(decimals, mode)` / `round_sig_figs(digits)` | Different names |
| String ops | `cell.str.contains/ends_with/starts_with/...` | `expr.str.contains/ends_with/starts_with/...` | Via namespace in both |
| Datetime ops | `cell.dt.year/month/day/...` | `expr.dt.year/month/day/...` | Via namespace in both |
