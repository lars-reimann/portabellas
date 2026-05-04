# Series Namespaces

## StringNameSpace (`series.str`)

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `concat` | `(delimiter: IntoExprColumn | str, *, ignore_nulls: bool = True) -> Series` | Concatenate all string values. |
| `contains` | `(pattern: str | Expr, *, literal: bool = False, strict: bool = True) -> Series` | Check if string contains a pattern. |
| `contains_any` | `(patterns: IntoExpr | Sequence[str], *, ascii_case_insensitive: bool = False, overlapping: bool = False) -> Series` | Check if string contains any of the given patterns. |
| `count_matches` | `(pattern: str | Expr, *, literal: bool = False) -> Series` | Count all occurrences of a pattern. |
| `decode` | `(encoding: str, *, strict: bool = True) -> Series` | Decode a string using the provided encoding. |
| `encode` | `(encoding: str) -> Series` | Encode a string using the provided encoding. |
| `ends_with` | `(suffix: str | Expr) -> Series` | Check if string ends with a suffix. |
| `extract` | `(pattern: IntoExprColumn | str, group_index: int = 1) -> Series` | Extract the first match of a regex pattern. |
| `extract_all` | `(pattern: str | Expr) -> Series` | Extract all matches of a regex pattern. |
| `extract_groups` | `(pattern: str) -> DataFrame` | Extract all capture groups as a DataFrame. |
| `extract_many` | `(patterns: IntoExpr | Sequence[str], *, ascii_case_insensitive: bool = False, overlapping: bool = False) -> Series` | Extract multiple matches. |
| `find` | `(literal: str | Expr, *, strict: bool = True) -> Series` | Return the index of the first occurrence. |
| `join` | `(delimiter: str | Expr, *, ignore_nulls: bool = True) -> Series` | Join list elements with a delimiter. |
| `json_decode` | `(dtype: PolarsDataType | None = None, *, infer_schema_length: int | None = None) -> Series` | Parse a JSON string. |
| `json_path_match` | `(json_path: str) -> Series` | Extract the first match from a JSON string. |
| `len_bytes` | `() -> Series` | Return the length in bytes. |
| `len_chars` | `() -> Series` | Return the length in characters. |
| `levenstein` | `(other: Series | str, *, parallel: bool = False) -> Series` | *(deprecated)* |
| `levenshtein` | `(other: Series | str, *, parallel: bool = False) -> Series` | Compute Levenshtein distance. |
| `pad_end` | `(length: int | Expr, fill_char: str | Expr = " ") -> Series` | Right-pad with a fill character. |
| `pad_start` | `(length: int | Expr, fill_char: str | Expr = " ") -> Series` | Left-pad with a fill character. |
| `replace` | `(pattern: str | Expr, value: str | Expr, *, literal: bool = False, n: int = 1) -> Series` | Replace first `n` occurrences. |
| `replace_all` | `(pattern: str | Expr, value: str | Expr, *, literal: bool = False) -> Series` | Replace all occurrences. |
| `reverse` | `() -> Series` | Reverse each string. |
| `slice` | `(offset: int | Expr, length: int | Expr | None = None) -> Series` | Create a substring. |
| `split` | `(by: IntoExpr | Sequence[str], *, inclusive: bool = False) -> Series` | Split into a list. |
| `split_exact` | `(by: IntoExpr | Sequence[str], n: int, *, inclusive: bool = False) -> Series` | Split into exactly `n+1` parts. |
| `splitn` | `(by: IntoExpr | Sequence[str], n: int) -> Series` | Split into at most `n` parts. |
| `starts_with` | `(prefix: str | Expr) -> Series` | Check if string starts with a prefix. |
| `strip_chars` | `(characters: str | Expr | None = None) -> Series` | Remove leading and trailing characters. |
| `strip_chars_end` | `(characters: str | Expr | None = None) -> Series` | Remove trailing characters. |
| `strip_chars_start` | `(characters: str | Expr | None = None) -> Series` | Remove leading characters. |
| `strip_prefix` | `(prefix: str | Expr) -> Series` | Remove a prefix. |
| `strip_suffix` | `(suffix: str | Expr) -> Series` | Remove a suffix. |
| `strptime` | `(dtype: PolarsTemporalType, format: str | None = None, *, strict: bool = True, exact: bool = True, cache: bool = True, utc: bool = False, ambiguous: Ambiguous | Series = "raise") -> Series` | Parse a string into a temporal type. |
| `to_date` | `(format: str | None = None, *, strict: bool = True, exact: bool = True, cache: bool = True, utc: bool = False, ambiguous: Ambiguous | Series = "raise") -> Series` | Convert to Date. |
| `to_datetime` | `(format: str | None = None, *, time_unit: TimeUnit | None = None, time_zone: str | None = None, strict: bool = True, exact: bool = True, cache: bool = True, utc: bool = False, ambiguous: Ambiguous | Series = "raise") -> Series` | Convert to Datetime. |
| `to_decimal` | `(infer_schema_length: int | None = 100, *, freeze: bool = False) -> Series` | Convert to Decimal. |
| `to_integer` | `(base: int | Expr | None = None, *, strict: bool = True) -> Series` | Convert to Integer. |
| `to_time` | `(format: str | None = None, *, strict: bool = True, exact: bool = True, cache: bool = True, ambiguous: Ambiguous | Series = "raise") -> Series` | Convert to Time. |
| `to_lowercase` | `() -> Series` | Convert to lowercase. |
| `to_uppercase` | `() -> Series` | Convert to uppercase. |
| `to_titlecase` | `() -> Series` | Convert to titlecase. |
| `url_decode` | `() -> Series` | Decode a URL-encoded string. |
| `url_encode` | `() -> Series` | URL-encode a string. |
| `zfill` | `(length: int | Expr) -> Series` | Zero-pad to a given length. |

---

## DateTimeNameSpace (`series.dt`)

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `add_business_days` | `(n: int | Expr | Series, *, week_mask: Sequence[bool] = (True, True, True, True, True), holidays: Sequence[date] | None = None, roll: Roll = "raise") -> Series` | Add `n` business days. |
| `base_utc_offset` | `() -> Series` | Get the base UTC offset. |
| `cast_time_unit` | `(tu: TimeUnit | None) -> Series` | Cast the time unit. |
| `cast_time_zone` | `(tz: str | None) -> Series` | Cast the time zone. |
| `century` | `() -> Series` | Get the century. |
| `combine` | `(time: time | Series, time_unit: TimeUnit = "us", *, ambiguous: Ambiguous | Series = "raise") -> Series` | Combine Date with Time to create Datetime. |
| `convert_time_zone` | `(time_zone: str) -> Series` | Convert to a different time zone. |
| `date` | `() -> Series` | Get the date component. |
| `day` | `() -> Series` | Get the day. |
| `dst_offset` | `() -> Series` | Get the DST offset. |
| `epoch` | `(time_unit: EpochTimeUnit = "us") -> Series` | Get the epoch value. |
| `hour` | `() -> Series` | Get the hour. |
| `iso_year` | `() -> Series` | Get the ISO year. |
| `is_leap_year` | `() -> Series` | Check if the year is a leap year. |
| `microsecond` | `() -> Series` | Get the microsecond. |
| `millisecond` | `() -> Series` | Get the millisecond. |
| `minute` | `() -> Series` | Get the minute. |
| `month` | `() -> Series` | Get the month. |
| `month_end` | `() -> Series` | Get the last day of the month. |
| `month_start` | `() -> Series` | Get the first day of the month. |
| `nanosecond` | `() -> Series` | Get the nanosecond. |
| `offset_by` | `(by: str | Series) -> Series` | Offset by a duration string. |
| `quarter` | `() -> Series` | Get the quarter (1-4). |
| `replace` | `(*, year: int | Series | None = None, month: int | Series | None = None, day: int | Series | None = None, hour: int | Series | None = None, minute: int | Series | None = None, second: int | Series | None = None, microsecond: int | Series | None = None, nanosecond: int | Series | None = None, ambiguous: Ambiguous | Series = "raise") -> Series` | Replace component(s). |
| `replace_time_zone` | `(time_zone: str | None, *, ambiguous: Ambiguous | Series = "raise") -> Series` | Replace the time zone without converting. |
| `second` | `() -> Series` | Get the second. |
| `strftime` | `(format: str) -> Series` | Format as a string. |
| `time` | `() -> Series` | Get the time component. |
| `time_zone` | `() -> Series` | Get the time zone string. |
| `timestamp` | `(time_unit: TimeUnit = "us") -> Series` | Get the timestamp. |
| `total_days` | `() -> Series` | Get total days (Duration only). |
| `total_hours` | `() -> Series` | Get total hours (Duration only). |
| `total_microseconds` | `() -> Series` | Get total microseconds (Duration only). |
| `total_milliseconds` | `() -> Series` | Get total milliseconds (Duration only). |
| `total_minutes` | `() -> Series` | Get total minutes (Duration only). |
| `total_nanoseconds` | `() -> Series` | Get total nanoseconds (Duration only). |
| `total_seconds` | `() -> Series` | Get total seconds (Duration only). |
| `truncate` | `(every: str | dt.timedelta | Series) -> Series` | Truncate to a given unit/interval. |
| `weekday` | `() -> Series` | Get the weekday (Monday=0, Sunday=6). |
| `week` | `() -> Series` | Get the ISO week number. |
| `year` | `() -> Series` | Get the year. |

---

## CatNameSpace (`series.cat`)

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_categories` | `() -> Series` | Get the categories. |
| `is_local` | `() -> bool` | Check if the categorical is local. |
| `set_ordering` | `(ordering: CategoricalOrdering) -> Series` | Set the ordering type. |
| `to_local` | `() -> Series` | Convert from global to local categorical. |
| `uses_lexical_ordering` | `() -> bool` | Check if the categorical uses lexical ordering. |

---

## ListNameSpace (`series.list`)

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `all` | `(*, ignore_nulls: bool = True) -> Series` | Check if all values are true. |
| `any` | `(*, ignore_nulls: bool = True) -> Series` | Check if any value is true. |
| `arg_max` | `() -> Series` | Get the index of the maximum value. |
| `arg_min` | `() -> Series` | Get the index of the minimum value. |
| `concat` | `(other: Series | list[Series]) -> Series` | Concatenate lists. |
| `contains` | `(item: IntoExpr | float | int | str | bool | None) -> Series` | Check if the list contains an item. |
| `count_matches` | `(element: IntoExpr | None = None) -> Series` | Count occurrences of an element. |
| `diff` | `(n: int = 1, null_behavior: NullBehavior = "ignore") -> Series` | Compute first discrete difference. |
| `drop_nulls` | `() -> Series` | Drop null values from each list. |
| `eval` | `(expr: Expr, *, parallel: bool = False) -> Series` | Run an expression on each element. |
| `explode` | `() -> Series` | Explode a list column. |
| `first` | `() -> Series` | Get the first element. |
| `gather` | `(indices: Series | list[int], *, null_on_oob: bool = False) -> Series` | Take elements by index. |
| `gather_every` | `(n: int, offset: int = 0) -> Series` | Take every nth element. |
| `get` | `(index: int | Series, *, null_on_oob: bool = False) -> Series` | Get element by index. |
| `head` | `(n: int = 5) -> Series` | Get the first n elements. |
| `index_of` | `(element: IntoExpr) -> Series` | Get index of first occurrence. |
| `join` | `(separator: str = ",", *, ignore_nulls: bool = True) -> Series` | Join elements with a separator. |
| `last` | `() -> Series` | Get the last element. |
| `len` | `() -> Series` | Get the length. |
| `max` | `() -> Series` | Get the max value. |
| `mean` | `() -> Series` | Get the mean value. |
| `min` | `() -> Series` | Get the min value. |
| `n_unique` | `() -> Series` | Count unique values. |
| `new_from_index` | `(index: int, n: int) -> Series` | Repeat list at index. |
| `reverse` | `() -> Series` | Reverse each list. |
| `sample` | `(n: int | None = None, *, fraction: float | None = None, with_replacement: bool = False, shuffle: bool = False, seed: int | None = None) -> Series` | Sample from each list. |
| `set_diff` | `(other: Series) -> Series` | Compute set difference. |
| `set_intersection` | `(other: Series) -> Series` | Compute set intersection. |
| `set_symmetric_difference` | `(other: Series) -> Series` | Compute set symmetric difference. |
| `set_union` | `(other: Series) -> Series` | Compute set union. |
| `shift` | `(periods: int = 1) -> Series` | Shift values. |
| `slice` | `(offset: int, length: int | None = None) -> Series` | Slice each list. |
| `sort` | `(*, descending: bool = False, nulls_last: bool = False) -> Series` | Sort each list. |
| `sum` | `() -> Series` | Sum values. |
| `tail` | `(n: int = 5) -> Series` | Get the last n elements. |
| `to_array` | `(width: int | PolarsDataType | None = None) -> Series` | Convert list to fixed-size array. |
| `unique` | `(*, maintain_order: bool = False) -> Series` | Get unique values. |

---

## StructNameSpace (`series.struct`)

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `field` | `(name: str | Sequence[str]) -> Series | DataFrame` | Retrieve one or more fields. |
| `json_encode` | `() -> Series` | Encode struct as a JSON string. |
| `rename_fields` | `(names: Sequence[str]) -> Series` | Rename fields. |
| `with_fields` | `(*exprs: IntoExpr) -> Series` | Add or replace fields. |

---

## BinaryNameSpace (`series.bin`)

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `base64_decode` | `(*, strict: bool = True) -> Series` | Decode a Base64-encoded binary. |
| `base64_encode` | `() -> Series` | Encode to Base64. |
| `contains` | `(literal: bytes) -> Series` | Check if binary contains a literal. |
| `ends_with` | `(suffix: bytes) -> Series` | Check if binary ends with a suffix. |
| `hex_decode` | `(*, strict: bool = True) -> Series` | Decode a hex-encoded binary. |
| `hex_encode` | `() -> Series` | Encode to hex. |
| `size` | `() -> Series` | Get the size in bytes. |
| `starts_with` | `(prefix: bytes) -> Series` | Check if binary starts with a prefix. |

---

## ArrayNameSpace (`series.arr`)

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `all` | `(*, ignore_nulls: bool = True) -> Series` | Check if all values are true. |
| `any` | `(*, ignore_nulls: bool = True) -> Series` | Check if any value is true. |
| `arg_max` | `() -> Series` | Get the index of the maximum value. |
| `arg_min` | `() -> Series` | Get the index of the minimum value. |
| `contains` | `(item: float | int | str | bool | None) -> Series` | Check if the array contains an item. |
| `count_matches` | `(element: float | int | str | bool | None = None) -> Series` | Count occurrences of an element. |
| `first` | `() -> Series` | Get the first element. |
| `get` | `(index: int, *, null_on_oob: bool = False) -> Series` | Get element by index. |
| `join` | `(separator: str = ",", *, ignore_nulls: bool = True) -> Series` | Join elements with a separator. |
| `last` | `() -> Series` | Get the last element. |
| `max` | `() -> Series` | Get the max value. |
| `mean` | `() -> Series` | Get the mean value. |
| `median` | `() -> Series` | Get the median value. |
| `min` | `() -> Series` | Get the min value. |
| `mode` | `(*, maintain_order: bool = False) -> Series` | Get the mode. |
| `n_unique` | `() -> Series` | Count unique values. |
| `reverse` | `() -> Series` | Reverse each array. |
| `shift` | `(periods: int = 1) -> Series` | Shift values. |
| `sort` | `(*, descending: bool = False, nulls_last: bool = False) -> Series` | Sort each array. |
| `std` | `(*, ddof: int = 1) -> Series` | Get the standard deviation. |
| `sum` | `() -> Series` | Sum values. |
| `to_list` | `() -> Series` | Convert to a list. |
| `unique` | `(*, maintain_order: bool = False) -> Series` | Get unique values. |
| `var` | `(*, ddof: int = 1) -> Series` | Get the variance. |
