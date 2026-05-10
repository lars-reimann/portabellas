# Portabellas

[![PyPI](https://img.shields.io/pypi/v/portabellas)](https://pypi.org/project/portabellas)
[![Main](https://github.com/Safe-DS/portabellas/actions/workflows/main.yml/badge.svg)](https://github.com/lars-reimann/portabellas/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/lars-reimann/portabellas/graph/badge.svg?token=H7HQN8Z5L1)](https://codecov.io/gh/lars-reimann/portabellas)
[![Documentation Status](https://readthedocs.org/projects/portabellas/badge/?version=latest)](https://portabellas.larsreimann.com)

**Type-safe, ergonomic table operations, with the speed of Polars.**

## Installation

```bash
pip install portabellas
```

## Why Portabellas?

Portabellas is built on [Polars](https://github.com/pola-rs/polars), so you get the same query optimization and parallelization, with these improvements on top:

- **Early validation:** Catch type and name errors directly where they occur, with negligible runtime overhead.

  ```python
  # Portabellas
  from portabellas import Table

  data = Table({"name": ["Alice", "Bob"], "age": [25, 30]})
  data = data.add_computed_column("result", lambda row: row["age"].struct.get("name"))
  #                                                     ^^^^^^^^^^^^^^^^^
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

> **Fun fact:** "Portabellas" is an anagram of "Polars table". And, as for any proper Python package, it starts with P.

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
