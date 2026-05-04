# When / Then Expressions

## When

Starting point for a conditional expression. Created via `pl.when(condition)`.

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `then` | `(value: Any) -> Then` | Attach a value to the condition. |

---

## Then

Intermediate result of a when-then expression.

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `otherwise` | `(value: Any) -> Expr` | Attach a default value. |
| `when` | `(condition: Expr) -> ChainedWhen` | Add another when condition. |

---

## ChainedWhen

A chained when condition within a when-then expression.

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `then` | `(value: Any) -> ChainedThen` | Attach a value to the chained condition. |

---

## ChainedThen

Intermediate result of a chained when-then expression.

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `otherwise` | `(value: Any) -> Expr` | Attach a default value. |
| `when` | `(condition: Expr) -> ChainedWhen` | Add another when condition. |

---

## Usage Pattern

```python
# Simple when-then-otherwise
pl.when(pl.col("x") > 0).then(1).otherwise(0)

# Chained when-then-otherwise
pl.when(pl.col("x") > 0).then(1).when(pl.col("x") < 0).then(-1).otherwise(0)
```
