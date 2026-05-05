# Cell Type Tracking & Early Type Validation

## Motivation

Currently, we only validate column names via the schema (e.g., `row["col"]` checks that `col` exists). We do not validate column types, so errors like `cell.list` on a string cell only surface at Polars evaluation time — far from where the mistake was made. By tracking types on `Cell` and validating namespace access, we can catch these errors early, consistent with the library's early-validation philosophy.

## Design Decisions

- **Validation point**: At the earliest possible point — namespace properties for namespace access, method body for method-level constraints. Errors point directly to the user's code.
- **Validation granularity**: Namespace-level first (e.g., `cell.list` requires `List` type). Method-level sub-constraints (e.g., `dt.year` only valid for `Date`/`Datetime`, not `Time`) and `ExprCell` method constraints (e.g., `__invert__` requires `Boolean`) are added incrementally.
- **Unknown type**: `DataTypes.Unknown` as a sentinel for "type not yet inferred". When a Cell's type is Unknown, validation is skipped entirely — no false positives.
- **Type visibility**: Private `_type` field only. Not part of the public API.
- **Incremental rollout**: All methods returning a `Cell` default to `DataTypes.Unknown()` initially. Type inference is added method-by-method over time.
- **Parameter naming**: `type` (not `_type`) — overwrites the BIF but makes call sites more readable.
- **Default value**: Module-level `_UNKNOWN = DataTypes.Unknown()` constant used as default for `ExprCell.__init__` and `_expr_cell` helpers. Satisfies B008 (function call in argument defaults) since `DataTypes.Unknown()` is immutable.
- **`ExprCell.__init__`**: Keyword-only `type` parameter with `_UNKNOWN` default.
- **`Expr*Operations.__init__`**: Positional required `type` parameter (always known from the creating cell).
- **Type inference testing**: `assert_cell_has_type(cell, expected_type)` helper that checks the `_type` field of a returned `Cell` directly — no mocking needed. Used with `cell_of_type` factory. Type inference tests go in existing per-method test files (not separate files).
- **Conservative inference**: When we cannot confidently determine the result type (e.g., `str.to_datetime` with a custom format string), return `Unknown` rather than guessing. `Unknown` is always safe — it skips validation and falls back to Polars schema collection. A wrong non-`Unknown` type is a behavioral regression once `Cell._type` is propagated to `Column.__type_cache`.
- **Prefer dynamic inference**: Use `infer_operation_type(operator, *input_types)` to delegate type inference to Polars' schema computation whenever feasible. This is minimal overhead (~3μs, cached), always matches Polars behavior, and requires no maintenance when Polars updates its type promotion rules. Manual inference rules are acceptable where they're trivially correct (e.g., `self._type` for same-type operations, fixed return types like `Boolean()` for comparisons), but any case involving type promotion or complex rules should use dynamic inference.
- **Correctness cross-check**: In debug builds, `Column.type` asserts that the cached type matches the Polars-inferred type on first access. This catches inference mistakes at test time with zero production overhead. See the "Correctness Assurance" section below.

---

## Done

1. `feat(typing): add DataTypes.Unknown`
2. `feat(containers): add _type field to ExprCell and Expr*Operations`
3. `feat(validation): add check_type validator`
4. `feat(containers): validate cell namespace types`
5. `test(containers): test type validation`
6. `feat(containers): validate boolean and unary numeric operators on ExprCell`
7. `test(containers): test boolean and unary numeric operator validation`
8. `feat(typing): add infer_type_from_literal`
9. `refactor(validation): merge check_type and check_type_if_cell with literal type inference`
10. `refactor(test): add cell_of_type/cell_of_unknown_type factories`
11. `refactor(test): add assert_cell_has_type helper`
12. `feat(containers): add type inference for trivial Cell operations`
13. `feat(containers): add type inference for trivial *Operations methods`
14. `feat(containers): add type inference for same-type input-dependent operations`
15. `feat(containers): add type inference for cast and Cell static methods`
16. `fix(containers): improve str.to_datetime type inference`
17. `test(typing): add type inference correctness tests`
18. `feat(typing): add dynamic type inference for binary arithmetic operators`

---

## TODO

### Type Inference (incremental — each method can be done independently)

#### Input-dependent methods (~20 methods)

These propagate or derive from the input type:

**Same-type as input (DONE):**

| Method | Rule |
|--------|------|
| `__abs__`, `__neg__`, `__pos__` | `self._type` |
| `math.abs`, `math.ceil`, `math.floor`, `math.sign` | `self._type` |
| `math.round_to_decimal_places`, `math.round_to_significant_figures` | `self._type` |
| `list.reverse`, `list.sort` | `self._type` |
| `struct.rename`, `struct.prefix_names`, `struct.suffix_names` | New `DataTypes.Struct` with renamed/prefixed/suffixed field names; `self._type` if not `Struct` |
| `dt.replace` | `self._type` |
| `dur.abs` | `self._type` |

**Inner type extraction (requires `self._type` is `DataTypes.List`):**

| Method | Rule |
|--------|------|
| `list.first`, `list.last`, `list.get` | `self._type.inner` |
| `list.max`, `list.min` | `self._type.inner` |
| `list.sum` | Dynamic inference via `infer_operation_type` — Polars promotes inner types (e.g., `Int8` → `Int64`, `UInt8` → `Int64`, `Bool` → `UInt32`), so `self._type.inner` is insufficient |

**Struct field type (requires `self._type` is `DataTypes.Struct`):**

| Method | Rule |
|--------|------|
| `struct.get(name)` | `self._type.fields[name]` |

#### Conditional methods (1 method) — DONE

| Method | Rule |
|--------|------|
| `cast(type)` | `type` parameter directly |

#### Cell static methods — DONE

| Method | Return Type |
|--------|------------|
| `Cell.date(...)` | `DataTypes.Date()` |
| `Cell.datetime(...)` | `DataTypes.Datetime(time_zone=...)` |
| `Cell.duration(...)` | `DataTypes.Duration(time_unit="us")` |
| `Cell.time(...)` | `DataTypes.Time()` |
| `Cell.first_not_null(...)` | Common type if all input cells have the same known type; `Unknown` if mixed types or any input is Unknown |

#### Binary arithmetic (~14 methods) — DONE

Instead of manually implementing Polars type promotion rules, delegate to Polars' schema computation. This guarantees correctness (always matches Polars) and zero maintenance (no promotion table to update when Polars changes).

**Approach:** `infer_operation_type(operator, *input_types_or_literals)` in `src/portabellas/typing/_type_inference.py` builds a tiny 1-row Polars DataFrame with the input dtypes, applies the operator expression, and reads the result dtype via `collect_schema()`. Results are cached in a module-level `_TYPE_CACHE` dict keyed by `(operator, input_types)` — only for all-DataType calls (literals bypass the cache).

**Variadic:** `infer_operation_type` accepts any number of `DataType | object` arguments, supporting unary, binary, and n-ary operations. For binary arithmetic, the call is always `infer_operation_type(operator, self._type, _type_or_literal_of_other(other))`.

**Literal handling:** When an operand is a Python literal (not a `Cell`), it's passed through to `pl.lit(value)` in the Polars computation. This ensures correct context-dependent literal adaptation (e.g., `Int8_cell + 3 → Int8`, `UInt64_cell + (-1) → Int64`). Literals bypass the cache since specific literal values are unlikely to repeat.

**Operand order:** For both forward and reverse operators, `self` always maps to `pl.col("a")` and `other` to `pl.col("b")` (or `pl.lit(value)` for literals). For `__rsub__`, `pl.Expr.__rsub__(self_expr, other_expr)` internally computes `other - self`, and `pl.Expr.__rsub__(pl.col("a"), pl.col("b"))` = `b - a` — same mapping.

**Early returns (no schema computation needed):**
- `Unknown` in any DataType operand → `Unknown`

**Error handling:** If Polars raises `InvalidOperationError` or `ComputeError` (invalid type combination like String + Int), return `Unknown`. Type validation (items 13/14) catches these with better error messages.

**Helper:** `_type_or_literal_of_other(other: object) -> DataType | object` in `_expr_cell.py` — returns `other._type` for Cell inputs, raw `other` for Python literals.

**Architecture:** `infer_operation_type` is a 3-line entry point that dispatches to `_infer_operation_type_with_cache` (for all-DataType calls) or `_compute_operation_type_with_polars` (for calls with literals). The Polars computation is split into `_build_test_lazy_frame` (constructs schema + args + frame) and `_compute_operation_type_with_polars` (collects schema, handles errors).

**File:** `src/portabellas/typing/_type_inference.py` (renamed from `_infer_type_from_literal.py`) — houses `infer_type_from_literal`, `infer_operation_type`, and supporting private functions. No circular import: only depends on `_data_type.py` (same package) and `polars` (external).

**Performance:** Schema computation is ~3μs per call; cache converges in one test run (~50-100 entries); subsequent hits are pure dict lookups.

| Method | Inference |
|--------|-----------|
| `__add__`, `__radd__` | `infer_operation_type(pl.Expr.__add__/__radd__, self._type, other_type)` |
| `__sub__`, `__rsub__` | Same pattern with `pl.Expr.__sub__/__rsub__` |
| `__mul__`, `__rmul__` | Same pattern with `pl.Expr.__mul__/__rmul__` |
| `__truediv__`, `__rtruediv__` | Same pattern with `pl.Expr.__truediv__/__rtruediv__` |
| `__floordiv__`, `__rfloordiv__` | Same pattern with `pl.Expr.__floordiv__/__rfloordiv__` |
| `__mod__`, `__rmod__` | Same pattern with `pl.Expr.__mod__/__rmod__` |
| `__pow__`, `__rpow__` | Same pattern with `pl.Expr.__pow__/__rpow__` |

**Future consideration:** `infer_operation_type` is variadic and could replace the existing manual inference rules for unary operations (e.g., `infer_operation_type(pl.Expr.__neg__, Int8())` instead of hardcoded `self._type`). This would eliminate per-method inference code and make all inference dynamic + Polars-verified. Deferred — the existing manual rules work and have test coverage. The dynamic approach is proven for binary arithmetic first.

#### Comparison operators (~6 methods) — DONE (manual inference)

Comparison operators (`__eq__`, `__ne__`, `__lt__`, `__le__`, `__gt__`, `__ge__`) always return `Boolean`. This is trivially correct for all valid type combinations. Note: Polars does not raise errors for mismatched comparison types (e.g., `String < 3` returns `Boolean`), so `infer_operation_type` would not detect invalid comparisons — validation must be done separately if desired.

### Method-Level Type Validation (depends on type inference for inner-type propagation)

Namespace-level validation is intentionally coarse — e.g., `cell.dt` accepts `Date | Datetime | Time`. But many methods only make sense for a subset. This adds finer-grained checks inside `Expr*Operations` methods.

#### `dt.*` method-level sub-constraints

File: `src/portabellas/query/_datetime_operations/_expr_datetime_operations.py`

New requirements in `CellTypeRequirements`:

```python
DATE_OR_DATETIME = InstanceOf(DataTypes.Date, DataTypes.Datetime)
DATETIME_OR_TIME = InstanceOf(DataTypes.Datetime, DataTypes.Time)
DATETIME = InstanceOf(DataTypes.Datetime)
```

| Method(s) | Requirement | Rationale |
|-----------|-------------|-----------|
| `year`, `month`, `day`, `century`, `millennium`, `week`, `day_of_week`, `day_of_year`, `quarter`, `is_in_leap_year` | `DATE_OR_DATETIME` | Date components don't exist on `Time` |
| `hour`, `minute`, `second`, `millisecond`, `microsecond` | `DATETIME_OR_TIME` | Time components don't exist on `Date` |
| `date` | `DATETIME` | Extracting date only makes sense from `Datetime` |
| `time` | `DATETIME` | Extracting time only makes sense from `Datetime` |
| `to_string` | No additional check | All three types support `to_string` |
| `unix_timestamp` | No additional check | Works for `Date` and `Datetime` (Polars handles `Time` gracefully) |

#### `dt.to_string` format validation (optional/later)

Parse the chrono format string to check that specifiers are valid for the cell's type — e.g., `{Y}` is invalid for `Time`. This is complex enough to be its own increment and can be deferred.

#### `list.*` method-level sub-constraints

File: `src/portabellas/query/_list_operations/_expr_list_operations.py`

Depends on type inference propagating list inner types via `self._type.inner`. New requirements:

```python
NUMERIC_INNER = CellTypeRequirement("numeric inner", lambda t: t.is_list and t.inner.is_numeric)
STRING_INNER = CellTypeRequirement("string inner", lambda t: t.is_list and t.inner.is_string)
```

| Method | Requirement | Rationale |
|--------|-------------|-----------|
| `list.sum` | `NUMERIC_INNER` | Summing non-numeric inner types is a bug |
| `list.join` | `STRING_INNER` | Joining non-string inner types is a bug |

#### `struct.get(name)` field name validation

File: `src/portabellas/query/_struct_operations/_expr_struct_operations.py`

Depends on type inference propagating struct field types via `self._type.fields`. Validate that `name` exists in the struct's fields — this is name validation, not type validation, but fits naturally here since it uses the same `_type` infrastructure.

### Binary Arithmetic Type Validation (depends on type inference)

Binary arithmetic operators accept more than just numeric types in Polars. Valid combinations are operator-dependent and operand-dependent. Without validation, invalid combinations fail at Polars evaluation time with unhelpful error messages — far from where the mistake was made, due to lazy evaluation.

#### Research: Valid Polars combinations

**Addition (`+`):**

| Left type | Right type | Result | Valid? |
|-----------|-----------|--------|--------|
| Numeric | Numeric | Numeric (promoted) | Yes |
| String | String | String (concat) | Yes |
| Date | Duration | Date | Yes |
| Datetime | Duration | Datetime | Yes |
| Duration | Duration | Duration | Yes |
| Duration | Date | Date | Yes |
| Duration | Datetime | Datetime | Yes |
| Numeric | String | — | No (`InvalidOperationError`) |
| Boolean | Boolean | UInt32 | No (almost certainly a bug) |

**Subtraction (`-`):**

| Left type | Right type | Result | Valid? |
|-----------|-----------|--------|--------|
| Numeric | Numeric | Numeric (promoted) | Yes |
| Datetime | Datetime | Duration | Yes |
| Duration | Duration | Duration | Yes |
| Date | Duration | Date | Yes |
| Datetime | Duration | Datetime | Yes |
| Boolean | Boolean | — | No (`InvalidOperationError`) |

**Multiplication (`*`):**

| Left type | Right type | Result | Valid? |
|-----------|-----------|--------|--------|
| Numeric | Numeric | Numeric (promoted) | Yes |
| Duration | Int | Duration | Yes |
| Int | Duration | Duration | Yes |
| Boolean | Int | Int | Yes (but questionable) |

**True division (`/`):**

| Left type | Right type | Result | Valid? |
|-----------|-----------|--------|--------|
| Numeric | Numeric | Float64 | Yes |
| Duration | Int | Duration | Yes |

**Floor division (`//`):**

| Left type | Right type | Result | Valid? |
|-----------|-----------|--------|--------|
| Numeric | Numeric | Numeric (depends) | Yes |

**Modulo (`%`):**

| Left type | Right type | Result | Valid? |
|-----------|-----------|--------|--------|
| Numeric | Numeric | Same as left | Yes |

**Power (`**`):**

| Left type | Right type | Result | Valid? |
|-----------|-----------|--------|--------|
| Int | Int | Int | Yes |
| Numeric | Numeric | Float64 (mostly) | Yes |

#### Validation strategy

**Primary mechanism: dynamic validation via `infer_operation_type`.**

Since `infer_operation_type` returns `Unknown` when Polars raises `InvalidOperationError` or `ComputeError` for invalid type combinations, we can use it directly as a validation check:

```python
result_type = infer_operation_type(operator, self._type, other_type)
if isinstance(result_type, DataTypes.Unknown) and not isinstance(self._type, DataTypes.Unknown):
    raise ColumnTypeError(f"Invalid operand types for {operator.__name__}: {self._type} and {other_type}")
```

This eliminates the need for per-operator `CellTypeRequirement` constants (`NUMERIC_OR_STRING_OR_TEMPORAL`, `NUMERIC_OR_DURATION`, etc.) and cross-operand compatibility tables. Validation is always correct by definition — if Polars accepts the combination, so do we.

**Trade-off:** The error messages are less specific ("invalid operand types") compared to a manual approach ("addition requires numeric, string, or temporal operands"). This can be mitigated by providing a generic message that includes the operator and types, which is usually sufficient for debugging.

**Secondary mechanism (optional): single-operand requirements.**

For cases where only one operand is a `Cell` with a known type and the other is a literal, a simple `check_type` call with a broad requirement can catch obvious mistakes early (e.g., `"hello" + numeric_cell`). This is optional since `infer_operation_type` handles literals correctly — `pl.lit("hello") + Int32` would raise and return `Unknown`. But a single-operand check provides a clearer error message at lower cost.

### Type Propagation from ExprCell to Column

When a mapper callback returns an `ExprCell` with a known (non-`Unknown`) `_type`, that type can be used to seed the output Column's `__type_cache` directly — avoiding a Polars schema collection call.

**Implementation:**

Add an optional `type` keyword parameter to `Column._from_polars_lazy_frame`:

```python
def _from_polars_lazy_frame(name: str, data: pl.LazyFrame, *, type: DataType | None = None) -> Column:
    result = object.__new__(Column)
    result._name = name
    result.__series_cache = None
    result._lazy_frame = data.select(name)
    result.__type_cache = type
    return result
```

Then extract the result type from the `ExprCell` in `Column.map` and `Table.add_computed_column`/`add_computed_columns`:

```python
result_cell = mapper(ExprCell(pl.col(self.name), type=self.type))
expression = result_cell._polars_expression.alias(self.name)
result_lf = self._lazy_frame.with_columns(expression)

result_type = result_cell._type if not isinstance(result_cell._type, DataTypes.Unknown) else None
return self._from_polars_lazy_frame(self.name, result_lf, type=result_type)
```

**Scope:** Applies to `Column.map`, `Table.add_computed_column`, and `Table.add_computed_columns`.

**Fallback:** When `_type` is `Unknown` (type not yet inferred), `__type_cache` stays `None` and the existing Polars schema collection path is used — identical to current behavior.

**Correctness:** Our type inference rules mirror Polars exactly. As a safety net, add an assertion in debug/test builds that the cached type matches the Polars-inferred type on first access of `Column.type` when both are available.

### Conservative Inference for Ambiguous Cases

Once `Cell._type` is propagated to `Column.__type_cache`, any inaccuracy becomes a **behavioral regression** (wrong reported type) rather than just a validation miss. The rule is simple: **when in doubt, return `Unknown`**.

**Concrete case: `str.to_date` / `str.to_datetime` / `str.to_time`**

All three methods accept `format: str = "iso"` (not `str | None` — `"auto"` replaces the old `None` sentinel).

**`str.to_datetime`** — result timezone depends on the format string content or the data itself:

| `format` value | Inferred type | Rationale |
|-----------------|---------------|-----------|
| `"iso"` | `Datetime(time_unit="us", time_zone="UTC")` | Polars always produces UTC for ISO format |
| Custom format with `{z}` or `{:z}` | `Datetime(time_unit="us", time_zone="UTC")` | Polars converts to UTC when parsing with `%#z` (the Polars equivalent of `{z}`/`{:z}` for parsing), regardless of the offset values in the data |
| Custom format without `{z}`/`{:z}` | `Datetime(time_unit="us")` | No timezone offset in format → Polars produces a naive datetime (no timezone) |
| `"auto"` | `Unknown` | Polars infers timezone from the data itself; cannot determine statically |

**`str.to_date`** — always produces `Date`, regardless of format:

| `format` value | Inferred type | Rationale |
|-----------------|---------------|-----------|
| `"iso"` | `Date()` | Unambiguous |
| `"auto"` | `Date()` | Polars always produces `Date` for `str.to_date` |
| Custom format | `Date()` | Unambiguous |

**`str.to_time`** — always produces `Time`, regardless of format:

| `format` value | Inferred type | Rationale |
|-----------------|---------------|-----------|
| `"iso"` | `Time()` | Unambiguous |
| `"auto"` | `Time()` | Polars always produces `Time` for `str.to_time` |
| Custom format | `Time()` | Unambiguous |

Verified: Polars always produces `datetime[μs, UTC]` when `%#z` is in the parse format, even with varying offsets like `+0200` and `-0500`. Without `%#z`, the result is `datetime[μs]` (no timezone).

**General principle:** Any method where we cannot perfectly match Polars behavior should return `Unknown`. The fallback path (Polars schema collection) is always correct.

### Correctness Assurance

Two complementary strategies to ensure inferred types match Polars, especially across version upgrades:

#### Runtime cross-check assertion (defense in depth)

In `Column._from_polars_lazy_frame` and `Column._from_polars_series`, when a `type` parameter is provided, assert it matches the Polars-inferred type — but only when running under pytest, to avoid any production overhead:

```python
@classmethod
def _from_polars_lazy_frame(cls, name: str, data: pl.LazyFrame, *, type: DataType | None = None) -> Column:
    result = object.__new__(Column)
    result._name = name
    result.__series_cache = None
    result._lazy_frame = data.select(name)
    result.__type_cache = type

    # Cross-check cached type against Polars to catch inference regressions
    if "PYTEST_CURRENT_TEST" in os.environ and type is not None:
        schema = safely_collect_lazy_frame_schema(result._lazy_frame)
        polars_type = _from_polars_data_type(schema.dtypes()[0])
        assert type == polars_type, f"Type mismatch: cached={type}, actual={polars_type}"

    return result
```

And similarly in `_from_polars_series`, using the series dtype directly.

**Why in the factory methods, not in `Column.type`:** The check runs once at construction time rather than on every property access. It catches mismatches immediately when the Column is created, closer to the source. The factory methods are called infrequently and are clearly "construction" code, so the `PYTEST_CURRENT_TEST` guard is more natural here.

pytest sets `PYTEST_CURRENT_TEST` per-test during execution, so this check only fires inside test functions — zero overhead in production, no extra env var or `__debug__` flag needed.

#### Dedicated type inference correctness tests

Rather than a separate test module, correctness tests are co-located with the existing type inference tests in each per-method test file. The existing ground-truth test and the new Polars-comparison test share the same parametrize list via a class-based pattern.

**Helper:** `assert_cell_type_matches_polars(given_types, operation, inferred_type)` in `tests/helpers/_assertions.py`:

```python
def assert_cell_type_matches_polars(
    given_types: DataType | tuple[DataType, ...],
    operation: Callable[..., Cell],
    inferred_type: DataType,
) -> None:
    if isinstance(inferred_type, DataTypes.Unknown):
        pytest.skip("Cannot compare Unknown type to Polars")

    if isinstance(given_types, DataType):
        given_types = (given_types,)

    column_names = list("abcdefghijklmnopqrstuvwxyz"[: len(given_types)])
    schema = {name: dtype._polars_data_type for name, dtype in zip(column_names, given_types, strict=True)}
    cells = [ExprCell(pl.col(name), type=dtype) for name, dtype in zip(column_names, given_types, strict=True)]

    polars_dtype = (
        pl.DataFrame({name: [None] for name in schema}, schema=schema)
        .lazy()
        .select(result=operation(*cells)._polars_expression)
        .collect_schema()["result"]
    )

    assert polars_dtype == inferred_type._polars_data_type, (
        f"Inferred {inferred_type} ({inferred_type._polars_data_type}), Polars produced {polars_dtype}"
    )
```

Accepts `DataType | tuple[DataType, ...]` — bare `DataType` for unary operations, tuple for binary/n-ary.

**Key design choices:**

- **Direct Polars computation** — bypasses `Column.map` entirely. Builds a minimal Polars LazyFrame, applies the expression via `_polars_expression`, and collects the schema. This is future-proof: once `Column.map` propagates `Cell._type` to `Column.__type_cache`, the helper still gets the ground truth from Polars rather than the cached inferred type.
- **Explicit column name** — uses `ExprCell(pl.col("a"), type=given_type)` inline rather than `cell_of_type(given_type)`, making the `"a"` column name contract between ExprCell and DataFrame schema explicit.
- **Compares in Polars type system** — converts `inferred_type` to its Polars equivalent via `_polars_data_type` and compares against the Polars-computed dtype. This avoids relying on `_from_polars_data_type` (which could have its own bugs) and uses Polars as the authoritative ground truth.
- **Null column with explicit type** — `pl.DataFrame({"a": [None]}, schema={"a": given_type._polars_data_type})` works because Polars determines output types from the expression plan and input schema, not from actual data values. Verified for all type categories including `List`, `Struct`, `Datetime` with timezone, and `Duration`.
- **Unknown handling** — `pytest.skip()` when `inferred_type` is `Unknown`, since there's no meaningful Polars comparison.

**Test pattern:** All type inference tests use a class with two methods sharing one parametrize:

```python
@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [...],
)
class TestShouldInferType:
    def test_should_match_ground_truth(self, given_type, operation, expected_type):
        result = operation(cell_of_type(given_type))
        assert_cell_has_type(result, expected_type)

    def test_should_match_polars_type(self, given_type, operation, expected_type):
        assert_cell_type_matches_polars(given_type, operation, expected_type)
```

**Normalization:** All parametrize lists use the 3-tuple `(given_type, operation, expected_type)`, even for fixed-return-type methods (the `given_type` is simply repeated in each tuple). Previous 2-tuple `(operation, expected_type)` and non-parametrized single-case tests are converted.

**Cell static methods** (`Cell.date`, `Cell.datetime`, `Cell.time`, `Cell.duration`, `Cell.constant`, `Cell.first_not_null`): Use `lambda _: Cell.date(...)` etc. as the `operation`, with a dummy `given_type` (e.g., `DataTypes.Int64()`).

**Column-level tests** (`test_map`, `test_any`, `test_all`, `test_count_if`, `test_none`): Skipped — these test that the mapper receives a cell with the correct type, not that inference matches Polars.

**Scope:** ~110 test files across `containers/_cell/`, `query/_math_operations/`, `query/_datetime_operations/`, `query/_duration_operations/`, `query/_string_operations/`, `query/_list_operations/`, `query/_struct_operations/`.

**Recommendation:** Do both the runtime cross-check and the dedicated tests. The runtime assertion catches mismatches anywhere in the test suite with zero extra test code. The dedicated tests provide clear, focused coverage. Together, they make Polars upgrade breakage very visible.

### Schema Propagation for Table

Same pattern as Column type propagation — derive the output schema from known inputs without a Polars schema collection call. Many Table operations can compute the new schema mechanically:

| Method | Schema derivation |
|--------|------------------|
| `rename_column` | Same schema, update column name |
| `rename_columns` | Same schema, update column names |
| `remove_columns` | Remove entries from schema |
| `select_columns` | Subset of schema |
| `reorder_columns` | Same schema, reorder |
| `add_column` / `add_columns` | Union of schemas |
| `add_computed_column` / `add_computed_columns` | Add entries (type from `Cell._type` or Unknown) |
| `replace_column` | Replace entry in schema |
| `add_index_column` | Add Int64 column |

**Implementation:** Add an optional `schema` keyword to `Table._from_polars_lazy_frame` and populate `__schema_cache`. Methods that can derive the schema do so; others fall back to Polars collection.

**Separate from Column type propagation:** Column propagation exploits `Cell._type` from callbacks. Table schema propagation exploits the known schema from Table operations. They share the same caching mechanism but have different sources of truth. Implement as a follow-up after Column type propagation works and is validated.

**Safety:** Table schema propagation is simpler and safer than Column type propagation because the schema is derived from **known** inputs (the input Table's schema + the operation), not from inference about Polars behavior. The only uncertain part is `add_computed_column` where the new column's type comes from `Cell._type` — this has the same correctness guarantees as the Column-level propagation.

### Suggested Commit Order

1. ~~`feat(containers): add type inference for input-dependent operations`~~ ✓
2. ~~`feat(containers): add type inference for cast and Cell static methods`~~ ✓
3. ~~`refactor(typing): rename _infer_type_from_literal.py → _type_inference.py, add infer_operation_type with Polars-based dynamic inference and cache`~~ ✓
4. `feat(containers): propagate ExprCell type to Column via _from_polars_lazy_frame with debug cross-check`
5. ~~`test(typing): add type inference correctness tests`~~ ✓
6. ~~`fix(containers): improve str.to_datetime type inference`~~ ✓
7. `feat(containers): propagate Table schema for mechanical operations` (rename, remove, select, reorder, etc.)
9. `feat(query): add dt.* method-level type validation`
10. `feat(query): add list.* method-level type validation` (requires inner-type propagation)
11. `feat(query): add struct.get field name validation` (requires field-type propagation)
12. `feat(query): add dt.to_string format validation` (optional, complex)
13. `feat(containers): validate binary arithmetic operand types via infer_operation_type`
14. ~~`feat(containers): validate binary arithmetic operand compatibility`~~ (merged into 13 — `infer_operation_type` returns `Unknown` for invalid combinations, replacing the manual cross-operand compatibility tables)

### Type Inference Testing Strategy

All type inference tests use a class-based pattern with two methods sharing one parametrize. The parametrize is always a 3-tuple `(given_type, operation, expected_type)`, even for fixed-return-type methods.

#### Class-based test pattern

```python
@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Boolean(), lambda cell: ~cell, DataTypes.Boolean(), id="__invert__"),
        pytest.param(DataTypes.Boolean(), lambda cell: cell.not_(), DataTypes.Boolean(), id="not_"),
    ],
)
class TestShouldInferType:
    def test_should_match_ground_truth(self, given_type: DataType, operation: Callable[[Cell], Cell], expected_type: DataType) -> None:
        result = operation(cell_of_type(given_type))
        assert_cell_has_type(result, expected_type)

    def test_should_match_polars_type(self, given_type: DataType, operation: Callable[[Cell], Cell], expected_type: DataType) -> None:
        assert_cell_type_matches_polars(given_type, operation, expected_type)
```

- `test_should_match_ground_truth`: Checks the inferred `_type` against the expected `DataType`.
- `test_should_match_polars_type`: Computes the Polars output type directly from the expression (bypasses `Column.map`), converts `expected_type` to its Polars equivalent via `_polars_data_type`, and compares. Skips when `expected_type` is `Unknown`.

#### Binary operations with literal operands

For binary arithmetic operators, add a separate `TestShouldInferTypeWithLiteral` class in the same test file. The operation lambda bakes in the literal value, and `given_type` is a single `DataType` (unary-like signature):

```python
@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Int8(), lambda cell: cell + 3, DataTypes.Int8(), id="int8_plus_int"),
        pytest.param(DataTypes.Int32(), lambda cell: cell + 3.14, DataTypes.Float64(), id="int32_plus_float"),
    ],
)
class TestShouldInferTypeWithLiteral:
    def test_should_match_ground_truth(self, given_type, operation, expected_type):
        result = operation(cell_of_type(given_type))
        assert_cell_has_type(result, expected_type)

    def test_should_match_polars_type(self, given_type, operation, expected_type):
        assert_cell_type_matches_polars(given_type, operation, expected_type)
```

This is separate from `TestShouldInferType` (Cell+Cell) because the parametrize signature differs: `(given_type, operation, expected_type)` vs `(left_type, right_type, operation, expected_type)`.

#### Cell static methods

Use `lambda _: Cell.static_method(...)` as the operation with a dummy `given_type`:

```python
@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Int64(), lambda _: Cell.date(1, 2, 3), DataTypes.Date(), id="date"),
        pytest.param(DataTypes.Int64(), lambda _: Cell.datetime(1, 2, 3, 0, 0, 0, time_zone="UTC"), DataTypes.Datetime(time_zone="UTC"), id="datetime_utc"),
    ],
)
class TestShouldInferType:
    ...
```
