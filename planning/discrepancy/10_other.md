# Other Discrepancies

## Top-Level Functions: Polars has, Portabellas doesn't

### Aggregation functions

| Polars | Notes |
|---|---|
| `pl.all(*names)` / `pl.any(*names)` | Column selection |
| `pl.all_horizontal(*exprs)` / `pl.any_horizontal(*exprs)` | Horizontal boolean |
| `pl.approx_n_unique(*columns)` | Approximate unique count |
| `pl.count(*columns)` / `pl.sum(*columns)` / `pl.mean(*columns)` / `pl.median(*columns)` / `pl.min(*columns)` / `pl.max(*columns)` | Column-wise aggregation |
| `pl.n_unique(*columns)` / `pl.quantile(column, quantile)` | Aggregation |
| `pl.std(column, ddof)` / `pl.var(column, ddof)` | Aggregation |
| `pl.sum_horizontal(*exprs)` / `pl.mean_horizontal(*exprs)` / `pl.min_horizontal(*exprs)` / `pl.max_horizontal(*exprs)` | Horizontal aggregation |

### Column/expression constructors

| Polars | Notes |
|---|---|
| `pl.col(*names)` | Column reference |
| `pl.lit(value, *, dtype)` | Literal value |
| `pl.element()` | Element in eval context |
| `pl.field(name)` | Struct field reference |
| `pl.first(*columns)` / `pl.last(*columns)` | First/last value or column |
| `pl.len()` | Row count |
| `pl.nth(*indices)` | Column by index |
| `pl.exclude(columns)` | Exclude from selection |
| `pl.select(*exprs)` | Select in expression context |

### Arithmetic/math

| Polars | Notes |
|---|---|
| `pl.arange(start, end, step, *, dtype, eager)` | Integer range |
| `pl.int_range(start, end, step, *, dtype, eager)` | Integer range |
| `pl.int_ranges(start, end, step, *, dtype, eager)` | Integer ranges per row |
| `pl.linear_space(start, end, num, *, eager)` | Evenly spaced numbers |
| `pl.linear_spaces(start, end, num, *, eager)` | Evenly spaced numbers per row |
| `pl.ones(n)` / `pl.zeros(n)` | Filled series |
| `pl.repeat(value, n, *, dtype, eager)` | Repeat value |
| `pl.arctan2(y, x)` / `pl.arctan2d(y, x)` | Two-argument arctangent |

### String/list functions

| Polars | Notes |
|---|---|
| `pl.concat_str(exprs, separator, *, ignore_nulls)` | Horizontal string concat |
| `pl.format(template, *exprs)` | Format string template |
| `pl.escape_regex(str)` | Escape regex |
| `pl.concat_arr(*exprs)` | Concatenate arrays |
| `pl.concat_list(exprs)` | Concatenate lists |
| `pl.implode(*columns)` | Aggregate to list |

### Conditional/logical

| Polars | Notes |
|---|---|
| `pl.coalesce(*exprs)` | First non-null |
| `pl.when(condition)` | When-then-otherwise chain |

### Cumulative

| Polars | Notes |
|---|---|
| `pl.cum_count(*exprs, *, reverse)` | Cumulative count |
| `pl.cum_sum(*exprs, *, reverse)` / `pl.cum_sum_horizontal(*exprs)` | Cumulative sum |
| `pl.cum_fold(acc, function, exprs, *, include_init)` | Cumulative fold |
| `pl.cum_reduce(function, exprs)` | Cumulative reduce |
| `pl.fold(acc, function, exprs, *, include_init)` / `pl.reduce(function, exprs)` | Fold/reduce |

### Temporal constructors

| Polars | Notes |
|---|---|
| `pl.date(*, year, month, day)` | Date expression |
| `pl.datetime(*, year, month, day, hour, ...)` | Datetime expression |
| `pl.duration(*, weeks, days, hours, ...)` | Duration expression |
| `pl.time(*, hour, minute, second, ...)` | Time expression |
| `pl.date_range(start, end, interval, *, eager, closed)` | Date range |
| `pl.date_ranges(start, end, interval, *, eager, closed)` | Date ranges per row |
| `pl.datetime_range(start, end, interval, *, eager, closed, ...)` | Datetime range |
| `pl.datetime_ranges(start, end, interval, ...)` | Datetime ranges per row |
| `pl.time_range(start, end, interval, *, eager, closed)` | Time range |
| `pl.time_ranges(start, end, interval, ...)` | Time ranges per row |

### Sorting/ranking

| Polars | Notes |
|---|---|
| `pl.arg_sort_by(exprs, *, descending, nulls_last, ...)` | Sort indices |
| `pl.arg_where(condition)` | Indices where True |
| `pl.row_index(name, offset)` | Row index column |

### Business days

| Polars | Notes |
|---|---|
| `pl.business_day_count(start, end, *, week_mask, holidays)` | Business day count |

### Correlation/covariance

| Polars | Notes |
|---|---|
| `pl.corr(a, b, *, ddof, propagate_nans)` | Pearson correlation |
| `pl.cov(a, b, *, ddof)` | Covariance |
| `pl.rolling_corr(x, y, window_size, *, min_samples, ddof)` | Rolling correlation |
| `pl.rolling_cov(x, y, window_size, *, min_samples, ddof)` | Rolling covariance |

### Epoch/conversion

| Polars | Notes |
|---|---|
| `pl.from_epoch(column, time_unit)` | Convert from epoch |
| `pl.dtype_of(*columns)` | Get dtype |
| `pl.self_dtype()` | Current expression dtype |

### Grouping/merging

| Polars | Notes |
|---|---|
| `pl.groups(column)` | Group indices |
| `pl.merge_sorted(l_df, r_df, key)` | Merge sorted frames |

### Collection

| Polars | Notes |
|---|---|
| `pl.collect_all(*lfys, ...)` | Collect multiple LazyFrames in parallel |
| `pl.collect_all_async(lfys, ...)` | Collect multiple async |
| `pl.defer(function, *args, schema, **kwargs)` | Deferred function call |

### Concat

| Polars | Notes |
|---|---|
| `pl.concat(items, *, rechunk, how, parallel)` | Combine DataFrames/Series |

### Struct

| Polars | Notes |
|---|---|
| `pl.struct(*exprs, *, eager, schema)` | Create struct |
| `pl.struct_with_fields(expr, *fields)` | Add/replace fields |

### SQL

| Polars | Notes |
|---|---|
| `pl.sql_expr(sql)` | Parse SQL to Expr |

### Misc

| Polars | Notes |
|---|---|
| `pl.align_frames(*frames, on, select, descending)` | Align frames on common key |
| `pl.explain_all(*lfys)` | Explain multiple query plans |
| `pl.map_batches(function, return_dtype, *, agg_list)` | Custom batch function |
| `pl.map_groups(function, return_dtype, *, returns_scalar)` | Custom group function |
| `pl.set_random_seed(seed)` | Set random seed |
| `pl.union(*exprs)` | Set union of list columns |

---

## GroupBy: Polars has, Portabellas doesn't

| Polars | Notes |
|---|---|
| `GroupBy` (eager) | agg, all, first, head, iter, last, len, map_groups, max, mean, median, min, n_groups, quantile, size, std, sum, tail, var |
| `LazyGroupBy` | Same methods, returns LazyFrame |
| `DynamicGroupBy` | Time-based grouping |
| `RollingGroupBy` | Rolling window grouping |

---

## When/Then: Polars has, Portabellas doesn't

| Polars | Notes |
|---|---|
| `pl.when(condition).then(value).otherwise(value)` | Conditional expressions |
| Chained: `pl.when(c1).then(v1).when(c2).then(v2).otherwise(v3)` | Multi-condition |

---

## SQL: Polars has, Portabellas doesn't

| Polars | Notes |
|---|---|
| `SQLContext` | Register tables, execute SQL queries |
| `DataFrame.sql(query)` / `LazyFrame.sql(query)` | SQL on frame |

---

## Selectors: Polars has, Portabellas doesn't

| Polars | Notes |
|---|---|
| `cs.all()` / `cs.boolean()` / `cs.string()` / `cs.numeric()` / `cs.integer()` / `cs.float()` / `cs.temporal()` / `cs.date()` / `cs.datetime()` / `cs.duration()` / `cs.categorical()` / `cs.binary()` / `cs.struct()` / `cs.time()` / `cs.decimal()` / `cs.signed_integer()` / `cs.unsigned_integer()` | Type-based column selection |
| `cs.by_name(*names)` / `cs.by_dtype(*dtypes)` / `cs.contains(substring)` / `cs.matches(pattern)` / `cs.starts_with(*prefixes)` / `cs.ends_with(*suffixes)` / `cs.first()` / `cs.last()` | Name/pattern-based selection |
| Set operations: `|`, `&`, `~` | Union, intersection, complement on selectors |

---

## Config: Polars has, Portabellas doesn't

| Polars | Notes |
|---|---|
| `pl.Config` class | Many display/formatting options |
| `load_from_env()` / `save_to_env()` | Environment variable config |
| `QueryOptFlags` | Query optimization control |
| `GPUEngine` | GPU acceleration config |
| `CompatLevel` | Serialization compatibility |
| `StringCache` | Global categorical string cache |

---

## Portabellas has, Polars doesn't

| Portabellas | Notes |
|---|---|
| `TablePlotter` / `ColumnPlotter` | Built-in plotting (Polars: `plot` property exists but delegates to external library) |
| Custom exceptions (`MissingValuesColumnError`, `ColumnTypeError`, `LazyComputationError`, `SchemaError`, `LengthMismatchError`, `FileExtensionError`, `IndexOutOfBoundsError`, `OutOfBoundsError`) | Domain-specific exceptions wrapping Polars errors |
| `Cell.constant/date/datetime/duration/time/first_not_none` | Cell factory methods (Polars: `pl.lit()`, `pl.date()`, etc.) |
| Validation functions (`check_bounds`, `check_column_has_no_missing_values`, `check_column_is_numeric`, `check_columns_are_numeric`, `check_columns_dont_exist`, `check_columns_exist`, `check_and_convert_datetime_format`, `check_indices`, `check_row_counts_are_equal`, `check_schema`, `check_time_zone`, `normalize_and_check_file_path`) | Internal validation helpers |
| `get_polars_config()` | Pre-configured Polars display settings |
| `compute_duplicates(values, *, forbidden_values)` | Find duplicates in a list |
| `safely_collect_lazy_frame(frame)` / `safely_collect_lazy_frame_schema(frame)` | Safe collection with custom errors |
| `get_similar_strings(given_string, valid_strings)` | Fuzzy string matching for error messages |
