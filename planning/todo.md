# Portabellas Gap Analysis & Action Items

## 1. Most Important Missing Functionality

### Critical (core data-wrangling gaps that limit everyday use)

1. **GroupBy / aggregation framework** — No `group_by`, no aggregation after grouping. This is a top-5 DataFrame operation. Without it, users must drop to Polars for any grouped summary. (01, 10)

2. **When/Then (conditional expressions)** — No `when(...).then(...).otherwise(...)` equivalent. Conditional column creation is fundamental; currently impossible without workarounds. (10)

3. **Null/NaN handling on Column** — No `fill_null`, `fill_nan`, `drop_nulls`, `drop_nans`, `forward_fill`, `backward_fill`, `interpolate`, `is_null`, `is_not_null`, `is_nan`, `is_not_nan`. `null_count` now exists. Missing-value handling is essential for real-world data. (02)

4. **Null/NaN handling on Table** — Same gap at the Table level: no `fill_null`, `fill_nan`, `drop_nans`, `interpolate`, `null_count`. (01)

5. **Sorting & ordering on Column** — No `sort`, `reverse`, `shift`, `top_k`, `bottom_k`, `rank`, `arg_min`, `arg_max`. These are basic operations users expect on any column. (02)

6. **Sorting & ordering on Table** — No `reverse`, `shift`, `top_k`, `bottom_k`, `head`, `tail`, `gather_every`. Row-level access and ordering is very limited. (01)

7. **Value inspection & membership on Column** — No `is_in`, `is_between`, `is_unique`, `is_duplicated`, `is_first_distinct`, `is_last_distinct`, `is_close`, `search_sorted`. These are needed for filtering logic and data quality checks. (02)

8. **Cumulative & rolling operations** — No `cum_sum`, `cum_max`, `cum_min`, `cum_prod`, `diff`, `pct_change`, no rolling window functions at all. Critical for time-series and sequential analysis. (02, 03)

9. **Value replacement & binning** — No `replace`, `replace_strict`, `cut`, `qcut`, `clip`, `value_counts`, `unique_counts`, `rle`. Needed for data cleaning and discretization. (02, 03)

### Important (common operations that force fallback to Polars)

11. **Reshaping** — No `pivot`, `unpivot`, `explode`, `transpose`, `unnest`, `to_struct`. Reshaping is a core data manipulation category. (01)

12. **Join variants** — Only basic equi-join. No `join_asof`, `join_where`, `merge_sorted`, `update`. Asof join is critical for time-series alignment. (01)

13. **Horizontal operations on Table** — No `sum_horizontal`, `mean_horizontal`, `min_horizontal`, `max_horizontal`, `fold`. Can't compute row-wise aggregations. (01)

14. **Column-wise aggregation on Table** — No `sum`, `mean`, `median`, `min`, `max`, `std`, `var`, `product`, `quantile`, `count`, `null_count`, `n_unique`, `corr`. Currently must extract columns and aggregate individually. (01)

15. **String namespace gaps** — No `extract`, `extract_all`, `extract_groups`, `split`, `split_exact`, `splitn`, `count_matches`, `concat`, `zfill`, `to_titlecase`, `strptime`, `json_decode`, `json_path_match`, `replace` (first n). Many string processing workflows are blocked. (04)

16. **Datetime namespace gaps** — No `offset_by`, `truncate`, `cast_time_zone`, `convert_time_zone`, `replace_time_zone`, `timestamp`, `epoch`, `month_start`/`month_end`, `add_business_days`, `combine`. Timezone and date arithmetic are essential for temporal data. (05)

17. **List namespace gaps** — Only 8 of ~30 Polars list operations. Missing `eval`, `explode`, `gather`, `gather_every`, `slice`, `diff`, `shift`, `set_diff/intersection/union`, `n_unique`, `unique`, `concat`, `sample`, `head`/`tail`. (07)

18. **Math namespace gaps** — No `clip`, `truncate`, `cot`, `degrees`, `radians`, `pow` (as method), `nan_max`/`nan_min`, rounding mode option. `log1p` now exists. (06)

19. **Table inspect** — No `glimpse`, `equals`, `is_empty`, `is_duplicated`, `is_unique`, `shape`, `estimated_size`. `summarize_statistics` already covers `describe` functionality. (01)

20. **Column append/extend** — No `append`, `extend`, `extend_constant` on Column. Can't grow a column. (02)

21. **Table sampling** — No `sample_rows`. (01)

### Nice-to-have (advanced or niche features)

22. **Selectors** — No type-based column selection (Polars `cs.numeric()`, `cs.string()`, etc.). No general selector system. (10)

23. **I/O expansion** — Only CSV/JSON/JSONL/Parquet. No IPC, Avro, Excel, Delta, Iceberg, database, or cloud storage support. I/O options are minimal compared to Polars. (09)

24. **Lazy-specific features** — No `cache`, `explain`, `profile`, `sink_*`, `collect_schema`, `map_batches`, `with_context`. Power users lose lazy execution benefits. (01)

25. **SQL support** — No `SQLContext` or `table.sql()`. (10)

26. **Missing data types** — No `Categorical`, `Enum`, `Decimal`, `Array`. `ExperimentalFloat16` and `ExperimentalInt128` now exist; `UInt128` does not exist in Polars. (08)

27. **Missing Cell namespaces** — No `cell.cat`, `cell.bin`, `cell.arr`, `cell.meta`, `cell.name`. (03)

28. **Temporal constructors** — No `date_range`, `datetime_range`, `time_range` (ranges per row). (10)

29. **Other top-level functions** — No `pl.concat`, `pl.when`, `pl.arange`, `pl.int_range`, `pl.ones`/`pl.zeros`, `pl.repeat`, `pl.format`, `pl.concat_str`, `pl.struct`. (`pl.coalesce` is covered by `Cell.first_not_null`.) (10)

30. **Struct namespace gaps** — No `field` retrieval, no `with_fields`. Only `get`, `rename`, `prefix_names`, `suffix_names`, `to_json`. (07)

31. **Duration namespace** — Missing `total_nanoseconds`. Otherwise fairly complete. (05)

32. **Bitwise operations** — No bitwise methods on Column. (02)

33. **Serialization** — No `serialize`/`deserialize`. (01)

34. **Type casting convenience method** — No dedicated `cast` on Table or Column. Table casting is achievable via `transform_columns("col", lambda cell: cell.cast(...))`; Column casting via `map(lambda cell: cell.cast(...))`. A dedicated `cast` method would be more convenient but is not a true gap. (01, 02)
