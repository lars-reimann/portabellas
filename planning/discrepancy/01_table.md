# Table vs DataFrame/LazyFrame

## Polars has, Portabellas doesn't

### Aggregation (column-wise)

| Polars (DataFrame/LazyFrame) | Notes |
|---|---|
| `count()` | Non-null count per column |
| `sum()` / `mean()` / `median()` | Column-wise aggregation |
| `min()` / `max()` | Column-wise aggregation |
| `std(ddof)` / `var(ddof)` | Column-wise aggregation |
| `product()` | Column-wise product |
| `quantile(quantile, interpolation)` | Column-wise quantile |
| `approx_n_unique()` | Approximate unique count |
| `null_count()` | Null count per column |
| `n_unique(subset)` | Unique row count |
| `corr(*, label)` | Pairwise Pearson correlation |

### Horizontal operations

| Polars | Notes |
|---|---|
| `sum_horizontal(*, ignore_nulls)` | Sum across columns |
| `mean_horizontal(*, ignore_nulls)` | Mean across columns |
| `min_horizontal()` | Min across columns |
| `max_horizontal()` | Max across columns |
| `fold(operation)` | Custom horizontal reduction |

### Row access & iteration

| Polars | Notes |
|---|---|
| `head(n)` / `tail(n)` | First/last n rows |
| `limit(n)` | Alias for head |
| `row(index, *, by_predicate, named)` | Get single row values |
| `rows(*, named)` | All rows as list of tuples |
| `rows_by_key(key, *, named, include_key, unique)` | Rows keyed by column |
| `iter_rows(*, named, buffer_size)` | Iterator over rows |
| `iter_columns()` | Iterator over columns |
| `iter_slices(n_rows)` | Non-copying iterator of slices |
| `item(row, column)` | Get scalar value |
| `gather_every(n, offset)` | Take every nth row |

### Missing value handling

| Polars | Notes |
|---|---|
| `fill_null(value, strategy, limit)` | Fill nulls with value or strategy |
| `fill_nan(value)` | Fill NaN values |
| `drop_nans(subset)` | Drop rows with NaN |
| `interpolate()` | Interpolate missing values |

### Sorting & ordering

| Polars | Notes |
|---|---|
| `reverse()` | Reverse row order |
| `set_sorted(column, *, descending)` | Flag column as sorted |
| `shift(n, *, fill_value)` | Shift values by n indices |
| `top_k(k, *, by, reverse)` | k largest rows |
| `bottom_k(k, *, by, reverse)` | k smallest rows |

### Reshaping

| Polars | Notes |
|---|---|
| `pivot(on, *, index, values, ...)` | Long to wide (pivot table) |
| `unpivot(on, *, index, variable_name, value_name)` | Wide to long (melt) |
| `explode(columns)` | Explode list columns |
| `transpose(*, include_header, header_name, column_names)` | Transpose |
| `unnest(columns)` | Decompose struct columns |
| `to_struct(name)` | Convert to struct Series |
| `unstack(*, step, how, columns, fill_values)` | Unstack without aggregation |

### Join variants

| Polars | Notes |
|---|---|
| `join_asof(other, *, left_on, right_on, on, by, strategy, tolerance, ...)` | Asof (nearest) join |
| `join_where(other, *predicates, suffix)` | Join on inequality predicates |
| `merge_sorted(other, key, *, maintain_order)` | Merge two sorted frames |
| `update(other, on, how, *, left_on, right_on, include_nulls)` | Update values from other |

### GroupBy

| Polars | Notes |
|---|---|
| `group_by(*by, maintain_order)` | Group by operation |
| `group_by_dynamic(index_column, *, every, period, offset, ...)` | Time-based grouping |
| `rolling(index_column, *, period, offset, closed, group_by)` | Rolling window grouping |

### Schema & type operations

| Polars | Notes |
|---|---|
| `cast(dtypes, *, strict)` | Cast column types |
| `match_to_schema(schema, *, missing_columns, ...)` | Match/evolve schema |
| `clear(n)` | Empty or null-filled copy |
| `clone()` | Explicit copy |

### Inspection & display

| Polars | Notes |
|---|---|
| `describe(percentiles, *, interpolation)` | Summary statistics |
| `glimpse(*, max_items_per_column, ...)` | Dense preview |
| `show(limit, *, ...)` | Show rows with formatting options |
| `equals(other, *, null_equal)` | Check equality |
| `estimated_size(unit)` | Memory estimation |
| `is_duplicated()` / `is_unique()` / `is_empty()` | Boolean checks |
| `flags` | Column flags property |
| `shape` | (rows, cols) tuple |
| `style` | Great Table styling |

### Conversion

| Polars | Notes |
|---|---|
| `to_arrow()` | Apache Arrow |
| `to_numpy()` | NumPy ndarray |
| `to_pandas()` | pandas DataFrame |
| `to_dummies()` | One-hot encoding |
| `to_dicts()` | List of dicts |
| `to_init_repr(n)` | Instantiable string repr |
| `to_jax()` / `to_torch()` | ML framework interop |

### Serialization

| Polars | Notes |
|---|---|
| `serialize(file, *, format)` | Serialize to file/string |
| `deserialize(source, *, format)` | Deserialize from file |

### Lazy-specific

| Polars (LazyFrame) | Notes |
|---|---|
| `collect(*, optimizations, engine, background)` | Materialize query |
| `collect_async(*, gevent, engine)` | Async collect |
| `collect_batches(*, chunk_size, maintain_order)` | Streaming batches |
| `collect_schema()` | Resolve schema without collecting |
| `cache()` | Cache intermediate result |
| `explain(*, format, optimized)` | Show query plan |
| `profile(*, show_plot, figsize)` | Profile query |
| `show_graph(*, optimized, show, output_path)` | Show query graph |
| `inspect(fmt)` | Inspect computation node |
| `sink_csv/sink_parquet/sink_ipc/sink_ndjson` | Streaming writes |
| `sink_delta/sink_iceberg` | Streaming writes to Delta/Iceberg |
| `map_batches(function, *, ...)` | Custom function on batches |
| `pipe_with_schema(function)` | Alter with resolved schema |
| `with_context(other)` | Add external context |

### SQL

| Polars | Notes |
|---|---|
| `sql(query, *, table_name)` | SQL query on frame |

### Misc

| Polars | Notes |
|---|---|
| `sample(n, *, fraction, with_replacement, shuffle, seed)` | Random sample |
| `pipe(function, *args, **kwargs)` | Pipeable functions |
| `partition_by(by, *, maintain_order, include_key, as_dict)` | Split into groups |
| `upsample(time_column, *, every, group_by)` | Upsample time series |
| `hash_rows(seed, seed_1, seed_2, seed_3)` | Hash rows |
| `rechunk()` | Contiguous memory allocation |
| `shrink_to_fit(*, in_place)` | Reduce memory |
| `drop_in_place(name)` | In-place column drop |
| `extend(other)` | In-place vertical extension |
| `hstack(columns, *, in_place)` | Horizontal stack (in-place option) |
| `vstack(other, *, in_place)` | Vertical stack (in-place option) |
| `n_chunks(strategy)` | Number of chunks |
| `select(*exprs)` | Select with expressions |
| `with_columns(*exprs)` | Add columns with expressions |
| `select_seq` / `with_columns_seq` | Sequential variants |
| `sql_expr(sql)` | Parse SQL expression |

---

## Portabellas has, Polars doesn't

| Portabellas (Table) | Notes |
|---|---|
| `add_computed_column(name, mapper)` | Add column via Row-callback (Polars uses `with_columns` + Expr) |
| `count_rows_if(predicate)` | Count rows satisfying predicate (Polars: `filter(predicate).height`) |
| `filter_rows_by_column(name, predicate)` | Filter by predicate on specific column (Polars: `filter(pl.col(name).fn())`) |

| `remove_rows_by_column(name, predicate)` | Remove rows by predicate on specific column |

| `shuffle_rows(*, random_seed)` | Shuffle rows deterministically (Polars: `sample(shuffle=True, seed=)`) |
| `split_rows(percentage_in_first, *, shuffle, random_seed)` | Train/test split |
| `summarize_statistics()` | Summary statistics (Polars: `describe()`) |
| `transform_columns(selector, mapper)` | Transform columns via Cell-callback (Polars: `with_columns(pl.col(name).map(...))`) |
| `from_columns(columns)` | Factory from Column objects (Polars: `DataFrame(list_of_series)`) |
| `from_dict(data)` | Factory from dict (Polars: `pl.from_dict()` or constructor) |

---

## Both have but with different APIs

| Feature | Portabellas | Polars | Difference |
|---|---|---|---|
| Row count | `table.row_count` | `df.height` | Property name |
| Column count | `table.column_count` | `df.width` | Property name |
| Column names | `table.column_names` | `df.columns` | Property name |
| Add columns | `table.add_columns(columns)` | `df.with_columns(*exprs)` or `df.hstack(columns)` | Portabellas takes Column objects; Polars takes Expr or Series |
| Remove columns | `table.remove_columns(selector, *, ignore_unknown_names)` | `df.drop(*columns, strict)` | Different parameter names |
| Rename column | `table.rename_column(old_name, new_name)` | `df.rename(mapping)` | Portabellas: single column; Polars: mapping for multiple |
| Select columns | `table.select_columns(selector)` | `df.select(*exprs)` | Portabellas: string/list; Polars: expressions |
| Filter rows | `table.filter_rows(predicate)` | `df.filter(*predicates)` | Portabellas: Row-callback; Polars: Expr predicates |
| Remove rows | `table.remove_rows(predicate)` | `df.remove(*predicates)` | Portabellas: Row-callback; Polars: Expr predicates |
| Remove duplicates | `table.remove_duplicate_rows()` | `df.unique(subset, *, keep, maintain_order)` | Polars has more options (subset, keep strategy) |
| Drop nulls | `table.remove_rows_with_missing_values(*, selector)` | `df.drop_nulls(subset)` | Similar functionality, different param name |
| Slice | `table.slice_rows(*, start, length)` | `df.slice(offset, length)` | Portabellas: keyword-only; Polars: positional |
| Sort | `table.sort_rows(key_selector, *, descending)` | `df.sort(by, *, descending, nulls_last, multithreaded, maintain_order)` | Portabellas: Row-callback; Polars: column name/Expr + more options |
| Join | `table.join(right_table, left_names, right_names, *, mode)` | `df.join(other, on, how, *, left_on, right_on, suffix, validate, ...)` | Polars has many more options (suffix, validate, coalesce, etc.) |
| Get column | `table.get_column(name)` | `df.get_column(name, *, default)` | Polars has default fallback |
| Column type | `table.get_column_type(name)` | No direct method (use `df.schema[name]`) | Different access pattern |
| Has column | `table.has_column(name)` | `name in df.columns` | Portabellas: method; Polars: `in` operator |
| Add index | `table.add_index_column(name, *, first_index)` | `df.with_row_index(name, offset)` | Different parameter name (first_index vs offset) |
| Stack vertically | `table.add_tables_as_rows(others)` | `df.vstack(other)` | Portabellas accepts list; Polars single frame |
| Stack horizontally | `table.add_tables_as_columns(others)` | `df.hstack(columns)` | Portabellas accepts Table objects; Polars accepts Series/DataFrame |
| To dict | `table.to_dict()` | `df.to_dict(as_series=False)` | Polars defaults to Series; Portabellas returns lists |
