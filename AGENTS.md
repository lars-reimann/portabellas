# AGENTS.md

## Setup

- **Package manager**: uv (not pip/poetry). Use `uv sync --all-groups` to install all dependency groups (dev + docs). Use `uv run <cmd>` to execute.
- **Python**: 3.13–3.14 only (`>=3.13,<3.15`).

## Commands

```bash
uv run ruff check --fix    # lint (ALL rules, numpy docstring convention)
uv run ruff format         # format
uv run mypy src tests      # typecheck (strict)
uv run pytest              # run all tests (includes doctests)
uv run pytest tests/portabellas/containers/_column/test_init.py  # single test file
uv run pytest --cov=portabellas  # with coverage
```

Run lint → format → typecheck → test before committing:
```bash
uv run ruff check --fix && uv run ruff format && uv run mypy src tests && uv run pytest tests
```

Pre-commit hooks run ruff-check (with `--fix`), ruff-format, and mypy. Run via `uv run pre-commit run --all-files`.

## Architecture

- **Src layout**: `src/portabellas/` is the package. Public API: `Table`, `Column`, `Row`, `Cell` from `portabellas.containers`; `DataType`, `Schema` from `portabellas.typing`.
- **Polars LazyFrame internally**: Both `Table` and `Column` store `_lazy_frame` (LazyFrame) as the primary representation. `_data_frame`/`_series` are lazily cached properties — accessed via `._data_frame` / `._series`, which collect on first access and re-anchor the LazyFrame.
- **Cell ABC / ExprCell**: `Cell` is an abstract base class. `ExprCell` is the concrete subclass that wraps a Polars `Expr`. Users receive `ExprCell` instances via callbacks (e.g., `column.transform(lambda cell: ...)`).
- **Circular imports**: `Cell.constant()`, `Cell.date()`, `Cell.datetime()`, `Cell.duration()`, `Cell.time()`, `Cell.first_not_none()`, and `Column.transform()` must late-import `ExprCell` with `from ._expr_cell import ExprCell  # noqa: PLC0415` inside the method body. Namespace property implementations in ExprCell also use late imports with `# noqa: PLC0415`.
- **ExprCell is not re-exported**: Tests import it as `from portabellas.containers._cell._expr_cell import ExprCell`.
- **Type aliases** (defined in `_cell.py` with `type` keyword, not re-exported): `ConvertibleToCell`, `ConvertibleToBooleanCell`, `ConvertibleToIntCell`, `ConvertibleToStringCell`. No underscore prefix.
- Core submodules: `containers/`, `query/` (cell operation namespaces), `typing/`, `io/`, `plotting/`, `exceptions/`, `_validation/`, `_config/`, `_utils/`.

## Style & Linting

- **Line length**: 120 (not ruff default 88).
- **Ruff**: `select = ["ALL"]` (not the default), with various rules overridden in `pyproject.toml`.
- **Docstring convention**: numpy.
- **mypy**: strict, but `disallow_any_generics = false`, `disallow_untyped_decorators = false`, `no_warn_return_any = true`.
- Test files: `D103`, `FBT001`, `INP001`, `S101` additionally ignored.
- **Type aliases**: Use `type X = ...` (Python 3.12+ syntax), not `X: TypeAlias = ...`.
- **No comments** in code unless explicitly requested.

## Testing

- pytest runs **doctests** too (`--doctest-modules` is in addopts). Doctest examples must only use implemented methods/operators.
- **Snapshot testing** via syrupy (`--snapshot-warn-unused` in addopts). Update snapshots with `--snapshot-update`.
- Tests mirror `src/portabellas/` layout under `tests/portabellas/`.
- **Table assertions**: Use `assert_tables_are_equal` from `tests.helpers` (wraps `polars.testing.assert_frame_equal`).
- **Cell operation assertions**: Use `assert_cell_operation_works` from `tests.helpers`. It creates a `Column("a", [value])`, calls `.transform()`, and checks the result. Use the `type_if_none` keyword argument when the input value is `None` to give the column a known dtype.
- **Polars dtype quirk**: `pl.lit(3)` produces `i32`, not `i64`. Keep this in mind for doctest output and test expectations.

## Cell/ExprCell Implementation Gotchas

- **`Cell.__hash__` must be `None`**: `__eq__` returns `Cell[bool | None]` (not `bool`), so `__hash__ = None` with `# type: ignore[assignment]` on the ABC. `ExprCell` needs `# noqa: PLW1641` on the class.
- **Don't reassign to `other` in ExprCell**: Use `other_expr = _to_polars_expression(other)` instead of `other = _to_polars_expression(other)` — reassigning to the parameter name confuses mypy's type narrowing.
- **`__eq__`/`__ne__` in tests**: Inverted-order comparisons (e.g., `3 == cell`) need `# type: ignore[arg-type,return-value]`; other dunders don't have this mypy issue.
- **`eq()`/`neq()` with `propagate_missing_values=False`**: Use Polars `.eq_missing()`/`.ne_missing()` which treats `None` as a regular value.
- **`pl.duration` with null inputs**: Null-typed expressions cause "expected integer or float dtype, (got null)". Cast null expressions to `Int32` via a `_to_int_expression` helper.
- **`pl.time`/`pl.datetime` silently accept microseconds > 999999**: Wrap in `pl.when(pl_microsecond <= 999_999).then(...).otherwise(None)` to convert invalid values to null.

## API Design

- **Immutability**: All container methods return new objects; never mutate in-place.
- **Lazy Row/Cell**: `Row` and `Cell` objects build Polars expressions internally. They must not materialize actual Python values — doing so causes 100–1000x slowdowns.
- **No `axis` parameter**: Use explicit names like `remove_columns` / `remove_rows`.
- **No `**kwargs`**: Explicitly list all allowed parameters.
- **Optional parameters are keyword-only**: Use `*` separator to enforce this.
- **No parameter dependencies**: If a parameter's meaning depends on another's value, split into separate functions.
- **Prefer methods to global functions**: Enables chaining and code-completion.
- **Prefer named functions to operators**: Operators don't appear in code-completion and can be ambiguous. (Cell operator overloading for numeric `==`, `<`, `+` is an exception.)
- **No uncommon abbreviations**: Use full words; common DS abbreviations (CSV, min, max) are fine.
- **Check preconditions early**: Validate at function start, before expensive work.
- **Wrap underlying exceptions**: Catch/wrap Polars exceptions with custom exceptions in `exceptions/`, inheriting from `PortabellasError`.
- **Cell namespaces**: `cell.str` for string ops, `cell.dt` for datetime ops, `cell.dur` for duration ops, `cell.math` for math ops.
- **Row/Cell not directly instantiable**: Only received via callbacks (e.g., `table.remove_rows(lambda row: ...)`).

## Docs

- mkdocs with mkdocstrings. Reference pages are **auto-generated** by `docs/reference/generate_reference_pages.py` (triggered by `gen-files` plugin). Do not edit files in `docs/reference/portabellas/` by hand.

## Branches & Commits

- **Never commit directly to `main`**. Always develop on a separate feature branch.
- **Small, incremental commits** per logical change — not one giant commit per feature.
- **Conventional commits** for all commit messages (required for semantic-release version bumps):
  - `feat:` new feature → minor version bump
  - `fix:` bug fix → patch version bump
  - `refactor:`, `test:`, `docs:`, `ci:`, `build:` for other changes (no version bump)
  - `feat!:` or `BREAKING CHANGE:` in footer → major version bump
- Scope is optional: `feat(containers): add Column.sort()`.

## Development Workflow (TDD)

- **Write failing tests first**, then implement just enough to pass.
- Use `@pytest.mark.parametrize` with `pytest.param(..., id=...)` instead of many separate test methods. Do **not** use a separate `ids=[...]` list; put the `id` close to the values:
   ```python
   @pytest.mark.parametrize(
       ("column", "expected"),
       [
           pytest.param(Column("col1", []), [], id="empty"),
           pytest.param(Column("col1", [1]), [1], id="non-empty"),
       ],
   )
   def test_should_store_the_data(column: Column, expected: list[Any]) -> None:
       assert list(column) == expected
   ```
- One test file per method/feature, named `test_<method>.py` (e.g., `test_init.py`, `test_name.py`, `test_row_count.py`).
- Cover all lines and edge cases with a **minimal** number of tests. Don't duplicate coverage.
