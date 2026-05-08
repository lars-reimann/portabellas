---
name: type-inference-testing
description: Class-based test pattern and Polars cross-check conventions for Cell type inference and type validation
---

## When to use

Load this skill when working on type inference for Cell operations or type validation in ExprCell/Expr*Operations methods. This covers adding inference rules to methods that currently return `DataTypes.Unknown()`, adding method-level type validation checks, or writing type inference tests.

## Class-based test pattern

All type inference tests use a class with two methods sharing one parametrize:

```python
@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Boolean(), lambda cell: ~cell, DataTypes.Boolean(), id="__invert__"),
        pytest.param(DataTypes.Boolean(), lambda cell: cell.not_(), DataTypes.Boolean(), id="not_"),
    ],
)
class TestShouldInferType:
    def test_should_match_ground_truth(self, given_type, operation, expected_type):
        result = operation(cell_of_type(given_type))
        assert_cell_has_type(result, expected_type)

    def test_should_match_polars_type(self, given_type, operation, expected_type):
        assert_cell_type_matches_polars(given_type, operation, expected_type)
```

- `test_should_match_ground_truth`: Checks the inferred `_type` against the expected `DataType`.
- `test_should_match_polars_type`: Computes the Polars output type directly from the expression (bypasses `Column.map`), converts `expected_type` to its Polars equivalent via `_polars_data_type`, and compares. Skips when `expected_type` is `Unknown`.

## Parametrize conventions

- **3-tuple**: Always `(given_type, operation, expected_type)`, even for fixed-return-type methods (repeat `given_type` in each tuple). No 2-tuples or non-parametrized single-case tests.
- **Use `pytest.param(..., id=...)`** — no separate `ids=[...]` list.

## Binary operations with Cell+Cell operands

For binary operations with two Cell operands (e.g., `__add__`, `__mul__`), use a 4-tuple parametrize and pass both cells to the operation:

```python
@pytest.mark.parametrize(
    ("left_type", "right_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Int8(), DataTypes.Int8(), lambda cell, _: cell + _, DataTypes.Int8(), id="int8_plus_int8"),
        pytest.param(DataTypes.Int32(), DataTypes.Float64(), lambda cell, _: cell + _, DataTypes.Float64(), id="int32_plus_float64"),
    ],
)
class TestShouldInferType:
    def test_should_match_ground_truth(self, left_type, right_type, operation, expected_type):
        result = operation(cell_of_type(left_type), cell_of_type(right_type))
        assert_cell_has_type(result, expected_type)

    def test_should_match_polars_type(self, left_type, right_type, operation, expected_type):
        assert_cell_type_matches_polars((left_type, right_type), lambda a, b: operation(a, b), expected_type)
```

## Binary operations with literal operands

Use a separate `TestShouldInferTypeWithLiteral` class in the same test file. The operation lambda bakes in the literal value, and `given_type` is a single `DataType`:

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

This is separate from `TestShouldInferType` because the parametrize shape differs: 3-tuple vs 4-tuple.

## Cell static methods

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

## Test helpers

- `assert_cell_has_type(cell, expected_type)` — checks `_type` field directly.
- `cell_of_type(dtype)` and `cell_of_unknown_type()` — create `ExprCell` instances for type inference tests.
- `assert_cell_type_matches_polars(given_types, operation, inferred_type)` — Polars cross-check. Accepts `DataType | tuple[DataType, ...]` (bare `DataType` for unary, tuple for binary/n-ary). Builds a 1-row Polars LazyFrame with the input dtype(s), applies the expression via `_polars_expression`, collects the schema, and compares in the Polars type system (converts `inferred_type` to `_polars_data_type`). Uses `ExprCell(pl.col("a"), type=given_type)` inline — the `"a"` column name contract between ExprCell and DataFrame schema is explicit. `pytest.skip()` when `inferred_type` is `Unknown`. Bypasses `Column.map` entirely — future-proof once `Column.map` propagates `Cell._type` to `Column.__type_cache`.

## Scope

Type inference tests are co-located with existing per-method test files across `containers/_cell/`, `query/_math_operations/`, `query/_datetime_operations/`, `query/_duration_operations/`, `query/_string_operations/`, `query/_list_operations/`, `query/_struct_operations/`.

## Column-level tests

Do not add `test_should_match_polars_type` to Column-level test files like `test_map.py`, `test_any.py`, `test_all.py`, `test_count_if.py`, `test_none.py`. These test that the mapper receives a cell with the correct type, not that inference matches Polars.

## Inference principles

- **Conservative**: When the result type cannot be confidently determined, return `DataTypes.Unknown()` rather than guessing. A wrong non-`Unknown` type is a behavioral regression.
- **Prefer dynamic inference**: Use `infer_operation_type(operator, *input_types)` from `src/portabellas/typing/_type_inference.py` to delegate to Polars' schema computation for cases involving type promotion or complex rules. Manual inference is acceptable where trivially correct (e.g., `self._type` for same-type operations, `Boolean()` for comparisons).
- **Unknown skips validation**: When a Cell's type is `Unknown`, `check_type` skips validation entirely — no false positives.

## Inference vs. validation

These two concerns have different correctness requirements:

- **Type inference** must match Polars exactly. Once `Cell._type` is propagated to `Column.__type_cache` via `Column.map`, any mismatch between our inferred type and Polars' actual type is a behavioral regression (wrong reported type). When in doubt, return `DataTypes.Unknown()` — the fallback to Polars schema collection is always correct.
- **Type validation** can be stricter than Polars to catch semantic bugs. If we block a combination that Polars would accept (e.g., `Boolean + Boolean`), that's a usability improvement, not a correctness issue. If we miss a case, Polars will eventually raise an error anyway — we just lose the early, clear error message. Validation is about better error messages, not correctness.
