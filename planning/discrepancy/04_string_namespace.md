# String Namespace Discrepancies

## Polars has, Portabellas doesn't

| Polars (`expr.str` / `series.str`) | Notes |
|---|---|
| `concat(delimiter, *, ignore_nulls)` | Concatenate all values in a column |
| `contains_any(patterns, *, ascii_case_insensitive, overlapping)` | Contains any of multiple patterns |
| `count_matches(pattern, *, literal)` | Count regex matches |
| `decode(encoding, *, strict)` / `encode(encoding)` | Encoding conversion |
| `extract(pattern, group_index)` | Extract first regex match |
| `extract_all(pattern)` | Extract all regex matches |
| `extract_groups(pattern)` | Extract capture groups as struct |
| `extract_many(patterns, *, ascii_case_insensitive, overlapping)` | Extract multiple matches |
| `find(literal, *, strict)` | Index of first occurrence of literal |
| `json_decode(dtype, *, infer_schema_length)` | Parse JSON |
| `json_path_match(json_path)` | Extract with JSONPath |
| `len_bytes()` | Byte length |
| `levenshtein(other, *, parallel)` | Levenshtein distance |
| `replace(pattern, value, *, literal, n)` | Replace first n occurrences |
| `split(by, *, inclusive)` | Split into list |
| `split_exact(by, n, *, inclusive)` | Split into exactly n+1 parts |
| `splitn(by, n)` | Split into at most n parts |
| `strptime(dtype, format, *, strict, exact, cache, utc, ambiguous)` | Parse with format |
| `to_decimal(infer_schema_length, *, freeze)` | Convert to Decimal |
| `to_titlecase()` | Title case |
| `url_decode()` / `url_encode()` | URL encoding |
| `zfill(length)` | Zero-pad |
| `join(delimiter, *, ignore_nulls)` | Join list elements (list-to-string) |

---

## Portabellas has, Polars doesn't

| Portabellas (`cell.str`) | Notes |
|---|---|
| `index_of(substring)` | Index of first occurrence of substring (Polars: `str.find(literal)`) |
| `length(*, optimize_for_ascii)` | Character count (Polars: `str.len_chars()`) |
| `repeat(count)` | Repeat string (no direct Polars equivalent) |
| `to_float()` | Convert to float (Polars: no direct string-to-float, use `cast()` or `str.to_integer()` + cast) |

---

## Both have but with different APIs

| Feature | Portabellas | Polars | Difference |
|---|---|---|---|
| Contains | `cell.str.contains(substring)` | `expr.str.contains(pattern, *, literal, strict)` | Polars supports regex; Portabellas substring only |
| Ends with | `cell.str.ends_with(suffix)` | `expr.str.ends_with(suffix)` | Similar |
| Starts with | `cell.str.starts_with(prefix)` | `expr.str.starts_with(prefix)` | Similar |
| Pad end | `cell.str.pad_end(length, *, character)` | `expr.str.pad_end(length, fill_char)` | Different param name |
| Pad start | `cell.str.pad_start(length, *, character)` | `expr.str.pad_start(length, fill_char)` | Different param name |
| Remove prefix | `cell.str.remove_prefix(prefix)` | `expr.str.strip_prefix(prefix)` | Different name |
| Remove suffix | `cell.str.remove_suffix(suffix)` | `expr.str.strip_suffix(suffix)` | Different name |
| Replace all | `cell.str.replace_all(old, new)` | `expr.str.replace_all(pattern, value, *, literal)` | Polars supports regex |
| Reverse | `cell.str.reverse()` | `expr.str.reverse()` | Same |
| Slice | `cell.str.slice(*, start, length)` | `expr.str.slice(offset, length)` | Portabellas: keyword-only; Polars: positional |
| Strip | `cell.str.strip(*, characters)` | `expr.str.strip_chars(characters)` | Different name |
| Strip end | `cell.str.strip_end(*, characters)` | `expr.str.strip_chars_end(characters)` | Different name |
| Strip start | `cell.str.strip_start(*, characters)` | `expr.str.strip_chars_start(characters)` | Different name |
| To date | `cell.str.to_date(*, format)` | `expr.str.to_date(format, *, strict, exact, cache, utc, ambiguous)` | Polars has more options |
| To datetime | `cell.str.to_datetime(*, format)` | `expr.str.to_datetime(format, *, time_unit, time_zone, strict, exact, cache, utc, ambiguous)` | Polars has more options |
| To int | `cell.str.to_int(*, base)` | `expr.str.to_integer(base, *, strict)` | Different name |
| To lowercase | `cell.str.to_lowercase()` | `expr.str.to_lowercase()` | Same |
| To uppercase | `cell.str.to_uppercase()` | `expr.str.to_uppercase()` | Same |
| To time | `cell.str.to_time(*, format)` | `expr.str.to_time(format, *, strict, exact, cache, ambiguous)` | Polars has more options |
