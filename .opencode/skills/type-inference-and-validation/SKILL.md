---
name: type-inference-and-validation
description: Implementation patterns and test conventions for Cell type inference and type validation in ExprCell/Expr*Operations methods
---

## When to use

Load this skill when working on type inference for Cell operations, type validation in ExprCell/Expr*Operations methods, or both. This covers adding inference rules to methods that currently return `DataTypes.Unknown()`, adding method-level type validation checks, writing type inference or type validation tests, or creating new `CellTypeRequirement` instances.

## Inference vs. validation

These two concerns have different correctness requirements:

- **Type inference** must match Polars exactly. Any mismatch between our inferred type and Polars' actual type is a behavioral regression (wrong reported type). When in doubt, return `DataTypes.Unknown()` — the fallback to Polars schema collection is always correct.
- **Type validation** can be stricter than Polars to catch semantic bugs. If we block a combination that Polars would accept (e.g., `Boolean + Boolean`), that's a usability improvement, not a correctness issue. If we miss a case, Polars will eventually raise an error anyway — we just lose the early, clear error message. Validation is about better error messages, not correctness.

## Inference principles

- **Conservative**: When the result type cannot be confidently determined, return `DataTypes.Unknown()` rather than guessing. A wrong non-`Unknown` type is a behavioral regression.
- **Prefer dynamic inference**: Use `infer_operation_type(operator, *input_types_or_literals)` from `src/portabellas/typing/_type_inference.py` to delegate to Polars' schema computation for cases involving type promotion or complex rules. Manual inference is acceptable where trivially correct (e.g., `self._type` for same-type operations, `Boolean()` for comparisons).
- **Unknown/Null skips validation**: When a Cell's type is `Unknown` or `Null`, both `check_type` and `_validate_operation_type` skip validation entirely — no false positives.

## Inference implementation patterns

Every `ExprCell` and `Expr*Operations` method must set the `type=` parameter when constructing the result `ExprCell`. There are eight patterns:

### 1. Hardcoded return type

Used when the output type is always the same regardless of input type. Most common in namespace methods and boolean/comparison operators.

```python
_BOOLEAN = DataTypes.Boolean()
_FLOAT64 = DataTypes.Float64()
_INT32 = DataTypes.Int32()

def sin(self) -> Cell:
    return _expr_cell(self._expression.sin(), type=_FLOAT64)

def __invert__(self) -> Cell:
    check_type(self, required=CellTypeRequirements.BOOLEAN)
    return ExprCell(self._expression.cast(pl.Boolean).__invert__(), type=_BOOLEAN)
```

Define module-level constants for frequently used types to avoid repeated construction.

### 2. Type-preserving

Used when the output type equals the input type. Common for identity-like numeric operations.

```python
def abs(self) -> Cell:
    check_type(self, required=CellTypeRequirements.NUMERIC)
    return _expr_cell(self._expression.__abs__(), type=self._type)
```

### 3. Polars cross-check via `infer_operation_type`

Used when the output type depends on type promotion rules or complex Polars logic. Primary tool for binary arithmetic operators.

```python
def __add__(self, other: ConvertibleToCell) -> Cell:
    other_type = _type_or_literal_of_other(other)
    result_type = infer_operation_type(pl.Expr.__add__, self._type, other_type)
    other_expr = _to_polars_expression(other)
    return ExprCell(self._expression.__add__(other_expr), type=result_type)
```

Rare in namespace methods — currently only `list.sum()` uses it:

```python
def sum(self) -> Cell:
    result_type = infer_operation_type(lambda a: a.list.sum(), self._type)
    return _expr_cell(self._expression.list.sum(), type=result_type)
```

### 4. Literal inference via `infer_type_from_literal`

Used by `Cell.constant` and `check_type` when a Python literal is passed. See `src/portabellas/typing/_type_inference.py` for the mapping. Note: `bool` is checked before `int` since `bool` is a subclass of `int`.

### 5. Structural extraction

Used when the output type is derived from the structure of the input type.

**List inner type** — `_inner_type_if_list` helper extracts `List(T).inner` → `T`, or `Unknown` if not a `List`:

```python
def _inner_type_if_list(type: DataType) -> DataType:
    if isinstance(type, DataTypes.List):
        return type.inner
    return DataTypes.Unknown()

def first(self) -> Cell:
    return _expr_cell(self._expression.list.first(), type=_inner_type_if_list(self._type))
```

**Struct field type** — looks up `self._type.fields[name]`, or `Unknown` if not a `Struct`:

```python
def get(self, name: str) -> Cell:
    if isinstance(self._type, DataTypes.Struct):
        check_struct_field_exists(name, self._type)
        result_type = self._type.fields[name]
    else:
        result_type = DataTypes.Unknown()
    return _expr_cell(self._expression.struct.field(name), type=result_type)
```

**Struct reconstruction** — `rename`/`prefix_names`/`suffix_names` rebuild the struct type with modified field names:

```python
def rename(self, old_name: str, new_name: str) -> Cell:
    result_type = (
        DataTypes.Struct({new_name if k == old_name else k: v for k, v in self._type.fields.items()})
        if isinstance(self._type, DataTypes.Struct)
        else self._type
    )
    return _expr_cell(self._expression.name.map_fields(...), type=result_type)
```

### 6. Conditional on parameter value

Used when the output type depends on a runtime parameter.

```python
def to_datetime(self, *, format: str = "iso") -> Cell:
    if format == "iso":
        type_ = _DATETIME_UTC
    elif format == "auto":
        type_ = _UNKNOWN
    else:
        polars_format = check_and_convert_datetime_format(format, ...)
        type_ = _DATETIME_UTC if _has_timezone_specifier(polars_format) else _DATETIME
    return _expr_cell(self._expression.str.to_datetime(format=polars_format, strict=False), type=type_)
```

### 7. User-specified

Used by `cast` and `constant(value, type=...)` where the user explicitly provides the `DataType`:

```python
def cast(self, type: DataType) -> Cell:
    return ExprCell(self._expression.cast(type._polars_data_type), type=type)
```

### 8. Conservative Unknown for multi-type aggregation

Used by `Cell.first_not_null` via `_infer_first_not_null_type`:

- If any cell is `Unknown` → return `Unknown` immediately.
- Skip `Null`-typed cells (they don't constrain the type).
- If all non-null cells have the same type → return that type.
- If non-null cells have different types → return `Unknown`.
- If all cells are `Null` → return `Null`.

## Validation implementation

### Pattern 1: Precondition check — `check_type`

Used when validity depends only on the input type(s), not on the result. Examples: namespace properties (`.dt`, `.str`, `.math`), boolean operators (`__invert__`, `__and__`).

```python
from portabellas._validation import check_type
from portabellas._validation._cell_type_requirements import CellTypeRequirements

@property
def str(self) -> StringOperations:
    check_type(self, required=CellTypeRequirements.STRING)
    return ExprStringOperations(self._expression, self._type)

def __invert__(self) -> Cell:
    check_type(self, required=CellTypeRequirements.BOOLEAN)
    return ExprCell(self._expression.cast(pl.Boolean).__invert__(), type=_BOOLEAN)
```

### Pattern 2: Postcondition check — `_validate_operation_type`

Used when validity depends on the combination of operand types and the result. Examples: arithmetic operators (`__add__`, `__mul__`) where the result type is inferred via `infer_operation_type`, and an `Unknown` result from known operands signals an invalid combination.

```python
def __add__(self, other: ConvertibleToCell) -> Cell:
    other_type = _type_or_literal_of_other(other)
    result_type = infer_operation_type(pl.Expr.__add__, self._type, other_type)
    _validate_operation_type("+", self._type, other_type, result_type)
    other_expr = _to_polars_expression(other)
    return ExprCell(self._expression.__add__(other_expr), type=result_type)
```

### `check_type` behavior

`check_type` and `_validate_operation_type` both **skip validation for `Unknown` and `Null` types** — no error is raised. This prevents false positives when the type hasn't been inferred yet (`Unknown`) or when the actual type is indeterminate (`Null` adapts to any type at runtime).

### `CellTypeRequirements`

Defined in `src/portabellas/_validation/_cell_type_requirements.py`. Two kinds:

- `InstanceOf(*types)` — checks `isinstance(dt, types)` and auto-generates a description like `"Boolean"` or `"Date, Datetime, or Time"`.
- `CellTypeRequirement(description, check)` — for predicate-based requirements (e.g., `is_numeric`, `is_list`, `is_struct`) where `InstanceOf` doesn't apply.

To add a new requirement, add it to `CellTypeRequirements`. Use `InstanceOf` when the check is against specific `DataType` subclasses; use `CellTypeRequirement` with a predicate for category-based checks.

### Validation entry point

All `check_type` calls live in `src/portabellas/containers/_cell/_expr_cell.py`. Operations in `query/` (e.g., `ExprStringOperations`, `ExprMathOperations`) receive pre-validated cells and do not call `check_type` themselves. This keeps validation at the entry point — the `ExprCell` method or property that users call.

## Inference test patterns

### Standard unary — 3-tuple

All type inference tests use a class with two methods sharing one parametrize:

```python
@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Int32(), lambda cell: cell.math.abs(), DataTypes.Int32(), id="int"),
        pytest.param(DataTypes.Float64(), lambda cell: cell.math.abs(), DataTypes.Float64(), id="float"),
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

### Binary Cell+Cell — 4-tuple

For binary operations with two Cell operands:

```python
@pytest.mark.parametrize(
    ("left_type", "right_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Int8(), DataTypes.Int8(), lambda cell, _: cell + _, DataTypes.Int8(), id="int8_plus_int8"),
        pytest.param(DataTypes.Int32(), DataTypes.Float64(), lambda cell, _: cell + _, DataTypes.Float64(), id="int32_plus_float64"),
    ],
)
class TestShouldInferType:
    def test_should_match_ground_truth(self, left_type: DataType, right_type: DataType, operation: Callable[[Cell, Cell], Cell], expected_type: DataType) -> None:
        result = operation(cell_of_type(left_type), cell_of_type(right_type))
        assert_cell_has_type(result, expected_type)

    def test_should_match_polars_type(self, left_type: DataType, right_type: DataType, operation: Callable[[Cell, Cell], Cell], expected_type: DataType) -> None:
        assert_cell_type_matches_polars((left_type, right_type), operation, expected_type)
```

### Binary with literal — separate `TestShouldInferTypeWithLiteral` class

The operation lambda bakes in the literal value, and `given_type` is a single `DataType`. Uses the same 3-tuple shape and two-test structure as unary, but the class is named `TestShouldInferTypeWithLiteral`.

### Extending the pattern

- **More Cell operands** (ternary, n-ary): Add type params before `operation` in the tuple. Pass the type tuple to `assert_cell_type_matches_polars`. Vary the class name (e.g., `TestShouldInferTypeWithCellBounds` for `math.clip`).
- **Static methods with Cell args** (e.g., `Cell.atan2`): Same shape as multi-operand, but the operation lambda calls the static method. Class name: `TestShouldInferTypeWithCellArgs`.
- **Static methods with no Cell args** (e.g., `Cell.date`): Use a dummy `given_type` with `lambda _: Cell.static_method(...)`.
- **`Cell.constant`**: Uses `TestShouldInferTypeFromValue` (infers from literal value) and `TestShouldUseExplicitTypeOverInferred` (explicit `type=` overrides inference). See `tests/portabellas/containers/_cell/test_constant.py`.

## Validation test patterns

### Namespace properties — three-test pattern

In the same test file as other tests for that namespace (e.g., `test_namespace_str.py`, `test_namespace_dt.py`):

```python
@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.String(), id="string"),
    ],
)
def test_should_not_raise_for_string_type(cell_type: DataType) -> None:
    _ = cell_of_type(cell_type).str


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.Int64(), id="int"),
        pytest.param(DataTypes.Boolean(), id="boolean"),
    ],
)
def test_should_raise_for_non_string_type(cell_type: DataType) -> None:
    with pytest.raises(ColumnTypeError, match="Expected String type"):
        _ = cell_of_type(cell_type).str


def test_should_skip_validation_for_unknown_type() -> None:
    _ = cell_of_unknown_type().str
```

- **Valid types** — access the property, no assertion needed (no error = pass).
- **Invalid types** — `pytest.raises(ColumnTypeError, match=...)` with the `required.description` embedded in the match string.
- **Unknown type** — single non-parametrized test, access the property, no assertion (skip = pass).

### Boolean binary operators — class-based covering both positions

```python
@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.String(), id="string"),
        pytest.param(DataTypes.Int64(), id="int"),
    ],
)
class TestShouldRaiseForNonBooleanType:
    def test_self(self, cell_type: DataType) -> None:
        with pytest.raises(ColumnTypeError, match="Expected Boolean type"):
            _ = cell_of_type(cell_type) ^ True

    def test_other_cell(self, cell_type: DataType) -> None:
        with pytest.raises(ColumnTypeError, match="Expected Boolean type"):
            _ = cell_of_type(DataTypes.Boolean()) ^ cell_of_type(cell_type)

    def test_self_inverted_order(self, cell_type: DataType) -> None:
        with pytest.raises(ColumnTypeError, match="Expected Boolean type"):
            _ = True ^ cell_of_type(cell_type)


class TestShouldSkipValidationForUnknownType:
    def test_self(self) -> None:
        _ = cell_of_unknown_type() ^ True

    def test_other_cell(self) -> None:
        _ = cell_of_type(DataTypes.Boolean()) ^ cell_of_unknown_type()

    def test_other_literal_none(self) -> None:
        _ = cell_of_type(DataTypes.Boolean()) ^ None
```

- `test_self` — the left operand has the wrong type.
- `test_other_cell` — the right operand (a Cell) has the wrong type.
- `test_self_inverted_order` — reflected operator (`__rxor__`), the Cell is the right operand of a literal.
- `TestShouldSkipValidationForUnknownType` — covers `Unknown` self, `Unknown` other cell, and `None` literal (infers `Null` type, which also skips validation).

### Arithmetic operators (postcondition check) — invalid type combinations

For arithmetic operators using `_validate_operation_type`:

```python
@pytest.mark.parametrize(
    ("left_type", "right_type"),
    [
        pytest.param(DataTypes.Boolean(), DataTypes.Boolean(), id="bool_plus_bool"),
        pytest.param(DataTypes.String(), DataTypes.Int64(), id="string_plus_int"),
    ],
)
class TestShouldRaiseForInvalidOperandTypes:
    def test_cell_plus_cell(self, left_type: DataType, right_type: DataType) -> None:
        with pytest.raises(ColumnTypeError, match="Invalid operand types"):
            _ = cell_of_type(left_type) + cell_of_type(right_type)
```

Use a separate `TestShouldRaiseForInvalidOperandTypesWithLiteral` class for literal tests (2-tuple `(given_type, operation)` with the literal baked into the operation lambda) — same rationale as inference: different parametrize shape. Include a `TestShouldSkipValidationForUnknownType` class covering `Unknown` self, `Unknown` other, and `None` literal.

## Parametrize conventions

- **Use `pytest.param(..., id=...)`** — no separate `ids=[...]` list.
- **Inference tuples**: Always `(given_type, operation, expected_type)` for unary, `(left_type, right_type, operation, expected_type)` for binary, `(value_type, lower_type, upper_type, operation, expected_type)` for ternary. Even for fixed-return-type methods, repeat `given_type` in each tuple. No 2-tuples or non-parametrized single-case tests.
- **Validation match strings**: Use the `required.description` from `CellTypeRequirement` for `check_type`-based tests (e.g., `"Expected Boolean type"`, `"Expected Date, Datetime, or Time type"`). Use `"Invalid operand types"` for `_validate_operation_type`-based tests.
- **Invalid type parametrize**: Include enough types to cover distinct categories (numeric, string, boolean, temporal, duration, list, struct). Don't enumerate every possible `DataType` variant — a representative from each category is sufficient.

## Test helpers

- `assert_cell_has_type(cell, expected_type)` — checks `_type` field directly.
- `cell_of_type(dtype)` and `cell_of_unknown_type()` — create `ExprCell` instances. Both from `tests.helpers`.
- `assert_cell_type_matches_polars(given_types, operation, inferred_type)` — Polars cross-check. Accepts `DataType | tuple[DataType, ...]` (bare `DataType` for unary, tuple for binary/n-ary). Builds a 1-row Polars LazyFrame with the input dtype(s), applies the expression via `ExprCell(pl.col(name), type=dtype)`, collects the schema, and compares in the Polars type system (converts `inferred_type` to `_polars_data_type`). `pytest.skip()` when `inferred_type` is `Unknown`. Bypasses `Column.map` entirely.

## Scope

Type inference and validation tests are co-located with existing per-method test files across `containers/_cell/` (e.g., `test_namespace_str.py`, `test_namespace_dt.py`, `test_xor.py`) and `query/` operation directories (`query/_math_operations/`, `query/_datetime_operations/`, `query/_duration_operations/`, `query/_string_operations/`, `query/_list_operations/`, `query/_struct_operations/`).

Do not add `test_should_match_polars_type` to Column-level test files like `test_map.py`, `test_any.py`, `test_all.py`, `test_count_if.py`, `test_none.py`. These test that the mapper receives a cell with the correct type, not that inference matches Polars.
