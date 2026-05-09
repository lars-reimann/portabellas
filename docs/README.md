# portabellas

**Type-safe, ergonomic table operations, with the speed of Polars.**

## Installation

```bash
pip install portabellas
```

## Why portabellas?

Portabellas is built on [Polars](https://github.com/pola-rs/polars), so you get the same query optimization and parallelization, with these improvements on top:

- **Early validation:** Catch type and name errors directly where they occur, with negligible runtime overhead.

  ```python
  # Portabellas
  from portabellas import Table

  data = Table({"name": ["Alice", "Bob"], "age": [25, 30]})
  data = data.add_computed_column("result", lambda row: row["age"].struct.get("name"))
  #                                              ^^^^^^^^^^^^^^^^^
  #
  # ColumnTypeError: Expected struct type, got i64
  ```

  ```python
  # Polars — same mistake, but error is deferred and misleading
  import polars as pl

  data = pl.LazyFrame({"name": ["Alice", "Bob"], "age": [25, 30]})
  data = data.with_columns(result=pl.col("age").struct.field("name"))  # No error
  data = data.collect()
  #      ^^^^^^^^^^^^^^
  #
  # StructFieldNotFoundError: name
  ```

- **No lazy/eager split:** No need to manually switch between lazy and eager mode. Lazy evaluation is active whenever possible. Operations that require eager mode handle it automatically.
- **Familiar abstractions:** Work with `Table`, `Column`, `Row`, and `Cell` — names that match how you think about data, not how the library stores it.

## For Developers

### Project Setup

1. [Install uv](https://pypi.org/project/uv/).
2. Run `uv sync` to generate a venv and install the dependencies.
3. Activate your venv by running `source .venv/bin/activate`.

### (Optional) Pre-Commit Hooks

We use pre-commit hooks for linting and formatting. Install the commit hooks locally via:

```bash
pre-commit install
```

The configuration can be adapted in `.pre-commit-config.yaml`.
