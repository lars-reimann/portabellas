# List & Struct Namespace Discrepancies

## List: Polars has, Portabellas doesn't

| Polars (`expr.list` / `series.list`) | Notes |
|---|---|
| `all(*, ignore_nulls)` / `any(*, ignore_nulls)` | Check all/any true in list |
| `arg_max()` / `arg_min()` | Index of max/min |
| `concat(other)` | Concatenate lists |
| `count_matches(element)` | Count occurrences |
| `diff(n, null_behavior)` | Discrete difference |
| `drop_nulls()` | Drop nulls from lists |
| `eval(expr, *, parallel)` | Run expression on each element |
| `explode()` | Explode list column |
| `gather(indices, *, null_on_oob)` | Take by index |
| `gather_every(n, offset)` | Take every nth element |
| `get(index, *, null_on_oob)` | Get by index |
| `head(n)` / `tail(n)` | First/last n elements |
| `index_of(element)` | Index of first occurrence |
| `mean()` | Mean of list values |
| `n_unique()` | Count unique in list |
| `new_from_index(index, n)` | Repeat list at index |
| `sample(n, *, fraction, with_replacement, shuffle, seed)` | Sample from list |
| `set_operation(other, function)` | Generic set operation |
| `set_diff(other)` / `set_intersection(other)` / `set_union(other)` / `set_symmetric_difference(other)` | Set operations |
| `shift(periods)` | Shift list elements |
| `slice(offset, length)` | Slice list |
| `unique(*, maintain_order)` | Unique elements in list |
| `to_array(width)` | Convert to fixed-size array |

---

## List: Portabellas has, Polars doesn't

| Portabellas (`cell.list`) | Notes |
|---|---|
| `first()` | First element (Polars: `list.first()` on Expr, but not on Series) |
| `last()` | Last element (Polars: `list.last()` on Expr, but not on Series) |

---

## Both have but with different APIs

| Feature | Portabellas | Polars | Difference |
|---|---|---|---|
| Contains | `cell.list.contains(item)` | `expr.list.contains(item)` | Similar |
| Get | `cell.list.get(index)` | `expr.list.get(index, *, null_on_oob)` | Polars has null_on_oob |
| Join | `cell.list.join(separator)` | `expr.list.join(separator, *, ignore_nulls)` | Polars has ignore_nulls |
| Length | `cell.list.length()` | `expr.list.len()` | Different name |
| Max/Min | `cell.list.max()` / `cell.list.min()` | `expr.list.max()` / `expr.list.min()` | Same |
| Reverse | `cell.list.reverse()` | `expr.list.reverse()` | Same |
| Sort | `cell.list.sort(*, descending)` | `expr.list.sort(*, descending, nulls_last)` | Polars has nulls_last |
| Sum | `cell.list.sum()` | `expr.list.sum()` | Same |

---

## Struct: Polars has, Portabellas doesn't

| Polars (`expr.struct` / `series.struct`) | Notes |
|---|---|
| `field(name)` | Retrieve field(s) by name (can return multiple) |
| `with_fields(*exprs)` | Add/replace fields |

---

## Struct: Portabellas has, Polars doesn't

| Portabellas (`cell.struct`) | Notes |
|---|---|
| `rename(old_name, new_name)` | Rename a single field (Polars: `rename_fields(names)` for all fields at once) |
| `prefix_names(prefix)` | Add prefix to all field names (no direct Polars equivalent) |
| `suffix_names(suffix)` | Add suffix to all field names (no direct Polars equivalent) |

---

## Both have but with different APIs

| Feature | Portabellas | Polars | Difference |
|---|---|---|---|
| Get field | `cell.struct.get(name)` | `expr.struct.field(name)` | Different name (get vs field) |
| Rename fields | `cell.struct.rename(old_name, new_name)` | `expr.struct.rename_fields(names)` | Portabellas: single field; Polars: all fields at once |
| JSON encode | `cell.struct.to_json()` | `expr.struct.json_encode()` | Different name |

---

## Polars namespaces with no Portabellas equivalent

| Polars Namespace | Notes |
|---|---|
| `expr.cat` / `series.cat` | Categorical operations (get_categories, set_ordering, to_local, uses_lexical_ordering, is_local) |
| `expr.bin` / `series.bin` | Binary operations (base64_encode/decode, hex_encode/decode, contains, starts_with, ends_with, size) |
| `expr.arr` / `series.arr` | Fixed-size array operations (all, any, arg_max, arg_min, contains, count_matches, first, get, join, last, max, mean, median, min, mode, n_unique, reverse, shift, sort, std, sum, to_list, unique, var) |
| `expr.meta` | Expression introspection (eq, has_multiple_outputs, is_column, is_column_selection, is_literal, output_name, pop, root_names, tree_format, undo_aliases, update_columns, vertical) |
| `expr.name` | Expression name manipulation (camel_to_snake, keep, map, prefix, suffix, to_lowercase, to_uppercase) |
| `expr.ext` | Extension type plugin registration |
