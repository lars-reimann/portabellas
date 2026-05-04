# Expr Namespaces

## ExprStringNameSpace (`expr.str`)

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `concat` | `(delimiter: IntoExprColumn | str, *, ignore_nulls: bool = True) -> Expr` | Concatenate all string values in a list/column. |
| `contains` | `(pattern: str | Expr, *, literal: bool = False, strict: bool = True) -> Expr` | Check if string contains a pattern. |
| `contains_any` | `(patterns: IntoExpr | Sequence[str], *, ascii_case_insensitive: bool = False, overlapping: bool = False) -> Expr` | Check if string contains any of the given patterns. |
| `count_matches` | `(pattern: str | Expr, *, literal: bool = False) -> Expr` | Count all occurrences of a pattern. |
| `decode` | `(encoding: str, *, strict: bool = True) -> Expr` | Decode a string using the provided encoding. |
| `encode` | `(encoding: str) -> Expr` | Encode a string using the provided encoding. |
| `ends_with` | `(suffix: str | Expr) -> Expr` | Check if string ends with a suffix. |
| `extract` | `(pattern: IntoExprColumn | str, group_index: int = 1) -> Expr` | Extract the first match of a regex pattern. |
| `extract_all` | `(pattern: str | Expr) -> Expr` | Extract all matches of a regex pattern. |
| `extract_groups` | `(pattern: str) -> Expr` | Extract all capture groups of a regex pattern as a struct. |
| `extract_many` | `(patterns: IntoExpr | Sequence[str], *, ascii_case_insensitive: bool = False, overlapping: bool = False) -> Expr` | Extract multiple matches. |
| `find` | `(literal: str | Expr, *, strict: bool = True) -> Expr` | Return the index of the first occurrence of a literal. |
| `join` | `(delimiter: str | Expr, *, ignore_nulls: bool = True) -> Expr` | Join list elements with a delimiter. |
| `json_decode` | `(dtype: PolarsDataType | None = None, *, infer_schema_length: int | None = None) -> Expr` | Parse a JSON string into a Polars data type. |
| `json_extract` | `(dtype: PolarsDataType | None = None, *, infer_schema_length: int | None = None) -> Expr` | *(deprecated — use json_decode)* |
| `json_path_match` | `(json_path: str) -> Expr` | Extract the first match from a JSON string with a JSONPath expression. |
| `len_bytes` | `() -> Expr` | Return the length in bytes of each string. |
| `len_chars` | `() -> Expr` | Return the length in characters of each string. |
| `levenstein` | `(other: Expr | str, *, parallel: bool = False) -> Expr` | Compute the Levenshtein distance between two strings. |
| `levenshtein` | `(other: Expr | str, *, parallel: bool = False) -> Expr` | Compute the Levenshtein distance between two strings. |
| `pad_end` | `(length: int | Expr, fill_char: str | Expr = " ") -> Expr` | Right-pad the string with a fill character. |
| `pad_start` | `(length: int | Expr, fill_char: str | Expr = " ") -> Expr` | Left-pad the string with a fill character. |
| `replace` | `(pattern: str | Expr, value: str | Expr, *, literal: bool = False, n: int = 1) -> Expr` | Replace first `n` occurrences of a pattern. |
| `replace_all` | `(pattern: str | Expr, value: str | Expr, *, literal: bool = False) -> Expr` | Replace all occurrences of a pattern. |
| `reverse` | `() -> Expr` | Reverse each string. |
| `slice` | `(offset: int | Expr, length: int | Expr | None = None) -> Expr` | Create a substring. |
| `split` | `(by: IntoExpr | Sequence[str], *, inclusive: bool = False) -> Expr` | Split a string into a list. |
| `split_exact` | `(by: IntoExpr | Sequence[str], n: int, *, inclusive: bool = False) -> Expr` | Split a string into exactly `n+1` parts. |
| `splitn` | `(by: IntoExpr | Sequence[str], n: int) -> Expr` | Split a string into at most `n` parts. |
| `starts_with` | `(prefix: str | Expr) -> Expr` | Check if string starts with a prefix. |
| `strip_chars` | `(characters: str | Expr | None = None) -> Expr` | Remove leading and trailing characters. |
| `strip_chars_end` | `(characters: str | Expr | None = None) -> Expr` | Remove trailing characters. |
| `strip_chars_start` | `(characters: str | Expr | None = None) -> Expr` | Remove leading characters. |
| `strip_prefix` | `(prefix: str | Expr) -> Expr` | Remove a prefix. |
| `strip_suffix` | `(suffix: str | Expr) -> Expr` | Remove a suffix. |
| `strptime` | `(dtype: PolarsTemporalType, format: str | None = None, *, strict: bool = True, exact: bool = True, cache: bool = True, utc: bool = False, ambiguous: Ambiguous | Expr = "raise") -> Expr` | Parse a string into a Date/Datetime/Time type. |
| `to_date` | `(format: str | None = None, *, strict: bool = True, exact: bool = True, cache: bool = True, utc: bool = False, ambiguous: Ambiguous | Expr = "raise") -> Expr` | Convert to Date. |
| `to_datetime` | `(format: str | None = None, *, time_unit: TimeUnit | None = None, time_zone: str | None = None, strict: bool = True, exact: bool = True, cache: bool = True, utc: bool = False, ambiguous: Ambiguous | Expr = "raise") -> Expr` | Convert to Datetime. |
| `to_decimal` | `(infer_schema_length: int | None = 100, *, freeze: bool = False) -> Expr` | Convert to Decimal. |
| `to_integer` | `(base: int | Expr | None = None, *, strict: bool = True) -> Expr` | Convert to Integer. |
| `to_time` | `(format: str | None = None, *, strict: bool = True, exact: bool = True, cache: bool = True, ambiguous: Ambiguous | Expr = "raise") -> Expr` | Convert to Time. |
| `to_lowercase` | `() -> Expr` | Convert to lowercase. |
| `to_uppercase` | `() -> Expr` | Convert to uppercase. |
| `to_titlecase` | `() -> Expr` | Convert to titlecase. |
| `trim` | `() -> Expr` | *(deprecated — use strip_chars)* |
| `trim_end` | `() -> Expr` | *(deprecated — use strip_chars_end)* |
| `trim_start` | `() -> Expr` | *(deprecated — use strip_chars_start)* |
| `url_decode` | `() -> Expr` | Decode a URL-encoded string. |
| `url_encode` | `() -> Expr` | URL-encode a string. |
| `zfill` | `(length: int | Expr) -> Expr` | Zero-pad the string to a given length. |

---

## ExprDateTimeNameSpace (`expr.dt`)

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `add_business_days` | `(n: int | Expr, *, week_mask: Sequence[bool] = (True, True, True, True, True), holidays: Sequence[date] | None = None, roll: Roll = "raise") -> Expr` | Add `n` business days. |
| `base_utc_offset` | `() -> Expr` | Get the base UTC offset of the timezone. |
| `cast_time_unit` | `(tu: TimeUnit | None) -> Expr` | Cast the time unit. |
| `cast_time_zone` | `(tz: str | None) -> Expr` | Cast the time zone. |
| `century` | `() -> Expr` | Get the century. |
| `combine` | `(time: time | Expr, time_unit: TimeUnit = "us", *, ambiguous: Ambiguous | Expr = "raise") -> Expr` | Combine a Date with a Time to create a Datetime. |
| `convert_time_zone` | `(time_zone: str) -> Expr` | Convert to a different time zone. |
| `date` | `() -> Expr` | Get the date component. |
| `day` | `() -> Expr` | Get the day. |
| `dst_offset` | `() -> Expr` | Get the DST offset of the timezone. |
| `epoch` | `(time_unit: EpochTimeUnit = "us") -> Expr` | Get the epoch value. |
| `hour` | `() -> Expr` | Get the hour. |
| `iso_year` | `() -> Expr` | Get the ISO year. |
| `is_leap_year` | `() -> Expr` | Check if the year is a leap year. |
| `microsecond` | `() -> Expr` | Get the microsecond. |
| `millisecond` | `() -> Expr` | Get the millisecond. |
| `minute` | `() -> Expr` | Get the minute. |
| `month` | `() -> Expr` | Get the month. |
| `month_end` | `() -> Expr` | Get the last day of the month. |
| `month_start` | `() -> Expr` | Get the first day of the month. |
| `nanosecond` | `() -> Expr` | Get the nanosecond. |
| `offset_by` | `(by: str | Expr) -> Expr` | Offset by a duration string (e.g., `"1mo"`, `"2d"`). |
| `quarter` | `() -> Expr` | Get the quarter (1-4). |
| `replace` | `(*, year: int | Expr | None = None, month: int | Expr | None = None, day: int | Expr | None = None, hour: int | Expr | None = None, minute: int | Expr | None = None, second: int | Expr | None = None, microsecond: int | Expr | None = None, nanosecond: int | Expr | None = None, ambiguous: Ambiguous | Expr = "raise") -> Expr` | Replace component(s) of a datetime. |
| `replace_time_zone` | `(time_zone: str | None, *, ambiguous: Ambiguous | Expr = "raise") -> Expr` | Replace the time zone without converting. |
| `second` | `() -> Expr` | Get the second. |
| `strftime` | `(format: str) -> Expr` | Format as a string. |
| `time` | `() -> Expr` | Get the time component. |
| `time_zone` | `() -> Expr` | Get the time zone string. |
| `timestamp` | `(time_unit: TimeUnit = "us") -> Expr` | Get the timestamp. |
| `total_days` | `() -> Expr` | Get total days (Duration only). |
| `total_hours` | `() -> Expr` | Get total hours (Duration only). |
| `total_microseconds` | `() -> Expr` | Get total microseconds (Duration only). |
| `total_milliseconds` | `() -> Expr` | Get total milliseconds (Duration only). |
| `total_minutes` | `() -> Expr` | Get total minutes (Duration only). |
| `total_nanoseconds` | `() -> Expr` | Get total nanoseconds (Duration only). |
| `total_seconds` | `() -> Expr` | Get total seconds (Duration only). |
| `truncate` | `(every: str | dt.timedelta | Expr) -> Expr` | Truncate to a given unit/interval. |
| `weekday` | `() -> Expr` | Get the weekday (Monday=0, Sunday=6). |
| `week` | `() -> Expr` | Get the ISO week number. |
| `year` | `() -> Expr` | Get the year. |

---

## ExprCatNameSpace (`expr.cat`)

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_categories` | `() -> Expr` | Get the categories of a categorical column. |
| `is_local` | `() -> Expr` | Check if the categorical is local. |
| `set_ordering` | `(ordering: CategoricalOrdering) -> Expr` | Set the ordering type. |
| `to_local` | `() -> Expr` | Convert from global to local categorical. |
| `uses_lexical_ordering` | `() -> Expr` | Check if the categorical uses lexical ordering. |

---

## ExprListNameSpace (`expr.list`)

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `all` | `(*, ignore_nulls: bool = True) -> Expr` | Check if all values in the list are true. |
| `any` | `(*, ignore_nulls: bool = True) -> Expr` | Check if any value in the list is true. |
| `arg_max` | `() -> Expr` | Get the index of the maximum value. |
| `arg_min` | `() -> Expr` | Get the index of the minimum value. |
| `concat` | `(other: IntoExpr | Sequence[IntoExpr]) -> Expr` | Concatenate lists. |
| `contains` | `(item: IntoExpr) -> Expr` | Check if the list contains an item. |
| `count_matches` | `(element: IntoExpr | None = None) -> Expr` | Count occurrences of an element. |
| `diff` | `(n: int = 1, null_behavior: NullBehavior = "ignore") -> Expr` | Compute first discrete difference. |
| `drop_nulls` | `() -> Expr` | Drop null values from each list. |
| `eval` | `(expr: Expr, *, parallel: bool = False) -> Expr` | Run an expression on each element of the list. |
| `explode` | `() -> Expr` | Explode a list column. |
| `first` | `() -> Expr` | Get the first element of each list. |
| `gather` | `(indices: IntoExpr | Sequence[int | Expr] | Expr, *, null_on_oob: bool = False) -> Expr` | Take elements by index. |
| `gather_every` | `(n: int, offset: int = 0) -> Expr` | Take every nth element. |
| `get` | `(index: int | Expr, *, null_on_oob: bool = False) -> Expr` | Get element by index. |
| `head` | `(n: int | Expr = 5) -> Expr` | Get the first n elements. |
| `index_of` | `(element: IntoExpr) -> Expr` | Get index of first occurrence. |
| `join` | `(separator: IntoExprColumn | str = ",", *, ignore_nulls: bool = True) -> Expr` | Join list elements with a separator. |
| `last` | `() -> Expr` | Get the last element. |
| `len` | `() -> Expr` | Get the length of each list. |
| `max` | `() -> Expr` | Get the max value. |
| `mean` | `() -> Expr` | Get the mean value. |
| `min` | `() -> Expr` | Get the min value. |
| `n_unique` | `() -> Expr` | Count unique values. |
| `new_from_index` | `(index: int, n: int) -> Expr` | Repeat list at index `n` times. |
| `reverse` | `() -> Expr` | Reverse each list. |
| `sample` | `(n: int | IntoExprColumn | None = None, *, fraction: float | IntoExprColumn | None = None, with_replacement: bool = False, shuffle: bool = False, seed: int | None = None) -> Expr` | Sample from each list. |
| `set_operation` | `(other: IntoExpr, function: Callable[[Any, Any], Any]) -> Expr` | Compute a set operation. |
| `shift` | `(periods: int = 1) -> Expr` | Shift values. |
| `slice` | `(offset: int | Expr, length: int | Expr | None = None) -> Expr` | Slice each list. |
| `sort` | `(*, descending: bool = False, nulls_last: bool = False) -> Expr` | Sort each list. |
| `sum` | `() -> Expr` | Sum values. |
| `tail` | `(n: int | Expr = 5) -> Expr` | Get the last n elements. |
| `to_array` | `(width: int | PolarsDataType | None = None) -> Expr` | Convert list to fixed-size array. |
| `unique` | `(*, maintain_order: bool = False) -> Expr` | Get unique values. |
| `union` | `(other: IntoExpr) -> Expr` | Compute set union. |
| `set_diff` | `(other: IntoExpr) -> Expr` | Compute set difference. |
| `set_intersection` | `(other: IntoExpr) -> Expr` | Compute set intersection. |
| `set_symmetric_difference` | `(other: IntoExpr) -> Expr` | Compute set symmetric difference. |

---

## ExprStructNameSpace (`expr.struct`)

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `field` | `(name: str | Sequence[str]) -> Expr` | Retrieve one or more fields from a struct. |
| `json_encode` | `() -> Expr` | Encode struct as a JSON string. |
| `rename_fields` | `(names: Sequence[str]) -> Expr` | Rename fields of a struct. |
| `with_fields` | `(*exprs: IntoExpr) -> Expr` | Add or replace fields in a struct. |

---

## ExprBinaryNameSpace (`expr.bin`)

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `base64_decode` | `(*, strict: bool = True) -> Expr` | Decode a Base64-encoded binary. |
| `base64_encode` | `() -> Expr` | Encode to Base64. |
| `contains` | `(literal: bytes | Expr) -> Expr` | Check if binary contains a literal. |
| `ends_with` | `(suffix: bytes | Expr) -> Expr` | Check if binary ends with a suffix. |
| `hex_decode` | `(*, strict: bool = True) -> Expr` | Decode a hex-encoded binary. |
| `hex_encode` | `() -> Expr` | Encode to hex. |
| `size` | `() -> Expr` | Get the size in bytes. |
| `starts_with` | `(prefix: bytes | Expr) -> Expr` | Check if binary starts with a prefix. |

---

## ExprArrayNameSpace (`expr.arr`)

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `all` | `(*, ignore_nulls: bool = True) -> Expr` | Check if all values are true. |
| `any` | `(*, ignore_nulls: bool = True) -> Expr` | Check if any value is true. |
| `arg_max` | `() -> Expr` | Get the index of the maximum value. |
| `arg_min` | `() -> Expr` | Get the index of the minimum value. |
| `contains` | `(item: IntoExpr) -> Expr` | Check if the array contains an item. |
| `count_matches` | `(element: IntoExpr | None = None) -> Expr` | Count occurrences of an element. |
| `first` | `() -> Expr` | Get the first element. |
| `get` | `(index: int | Expr, *, null_on_oob: bool = False) -> Expr` | Get element by index. |
| `join` | `(separator: IntoExprColumn | str = ",", *, ignore_nulls: bool = True) -> Expr` | Join elements with a separator. |
| `last` | `() -> Expr` | Get the last element. |
| `max` | `() -> Expr` | Get the max value. |
| `mean` | `() -> Expr` | Get the mean value. |
| `median` | `() -> Expr` | Get the median value. |
| `min` | `() -> Expr` | Get the min value. |
| `mode` | `(*, maintain_order: bool = False) -> Expr` | Get the mode. |
| `n_unique` | `() -> Expr` | Count unique values. |
| `reverse` | `() -> Expr` | Reverse each array. |
| `shift` | `(periods: int = 1) -> Expr` | Shift values. |
| `sort` | `(*, descending: bool = False, nulls_last: bool = False) -> Expr` | Sort each array. |
| `std` | `(*, ddof: int = 1) -> Expr` | Get the standard deviation. |
| `sum` | `() -> Expr` | Sum values. |
| `to_list` | `() -> Expr` | Convert to a list. |
| `unique` | `(*, maintain_order: bool = False) -> Expr` | Get unique values. |
| `var` | `(*, ddof: int = 1) -> Expr` | Get the variance. |

---

## ExprMetaNameSpace (`expr.meta`)

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `eq` | `(other: Expr) -> bool` | Check if two expressions are equal. |
| `has_multiple_outputs` | `() -> bool` | Check if expression produces multiple outputs. |
| `is_column` | `() -> bool` | Check if expression is a simple column. |
| `is_column_selection` | `(*, exclude: Sequence[str] = ()) -> bool` | Check if expression selects columns. |
| `is_literal` | `() -> bool` | Check if expression is a literal. |
| `output_name` | `() -> str` | Get the output column name. |
| `pop` | `() -> list[Expr]` | Pop the latest expression. |
| `root_names` | `() -> list[str]` | Get the root column names. |
| `selector_over` | `() -> frozenset[str] | None` | Get the columns this expression is a selector over. |
| `tree_format` | `(*, return_as_string: bool = False) -> str | None` | Format the expression as a tree. |
| `undo_aliases` | `() -> Expr` | Undo all aliases. |
| `update_columns` | `(columns: Callable[[str], str] | Mapping[str, str]) -> Expr` | Update column names. |
| `vertical` | `(*names: str) -> Expr` | Combine expressions vertically. |

---

## ExprNameNameSpace (`expr.name`)

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `camel_to_snake` | `() -> Expr` | Transform name from CamelCase to snake_case. |
| `keep` | `() -> Expr` | Keep the original name. |
| `map` | `(function: Callable[[str], str]) -> Expr` | Map a function over the expression name. |
| `prefix` | `(prefix: str) -> Expr` | Add a prefix to the expression name. |
| `suffix` | `(suffix: str) -> Expr` | Add a suffix to the expression name. |
| `to_lowercase` | `() -> Expr` | Convert name to lowercase. |
| `to_uppercase` | `() -> Expr` | Convert name to uppercase. |

---

## ExprExtensionNameSpace (`expr.ext`)

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `register` | `(function_name: str, *, lib: str, symbol: str, args: list[IntoExpr] | None = None, kwargs: dict[Any, Any] | None = None, is_elementwise: bool = False, input_wildcard_expansion: bool = False, returns_scalar: bool = False, cast_to_supertypes: bool = False, pass_name_to_apply: bool = False, changes_length: bool = False) -> Expr` | Register a plugin function on this expression's extension namespace. |
