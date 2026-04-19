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
uv run pre-commit run --all-files  # run all pre-commit hooks
```

Run lint → format → typecheck → test before committing:
```bash
uv run ruff check --fix && uv run ruff format && uv run mypy src tests && uv run pytest tests
```

## Architecture

- **Src layout**: `src/portabellas/` is the package. Public API: `Table`, `Column`, `Row`, `Cell` from `portabellas.containers`; `DataType`, `Schema` from `portabellas.typing`.
- **Polars LazyFrame internally**: Both `Table` and `Column` store `_lazy_frame` (LazyFrame) as the primary representation. `_data_frame`/`_series` are lazily cached properties — accessed via `._data_frame` / `._series`, which collect on first access and re-anchor the LazyFrame. `Table.schema` is similarly cached in `__schema_cache`.
- **Cell ABC / ExprCell**: `Cell` is an abstract base class. `ExprCell` is the concrete subclass that wraps a Polars `Expr`. Users receive `ExprCell` instances via callbacks (e.g., `column.map(lambda cell: ...)`).
- **Row ABC / ExprRow**: `Row` is an abstract base class. `ExprRow` is the concrete subclass that stores a `Table` reference and delegates all property/method calls to it. Users receive `ExprRow` instances via callbacks (e.g., `table.add_computed_column("c", lambda row: ...)`).
- **Circular imports**: Methods that create `ExprCell`/`ExprRow` instances must late-import with `# noqa: PLC0415` inside the method body. Affected: `Cell.constant()`, `Cell.date()`, `Cell.datetime()`, `Cell.duration()`, `Cell.time()`, `Cell.first_not_none()`, `Column.map()`, `Table.get_column()`, `Table.add_computed_column()`, `ExprRow.get_cell()`. Also `Table.schema` late-imports `Schema`, and validation functions late-import `Table`.
- **ExprCell/ExprRow are not re-exported**: Tests import them directly as `from portabellas.containers._cell._expr_cell import ExprCell` and `from portabellas.containers._row._expr_row import ExprRow`.
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
- **Cell operation assertions**: Use `assert_cell_operation_works` from `tests.helpers`. It creates a `Column("a", [value])`, calls `.map()`, and checks the result. Use the `type_if_none` keyword argument when the input value is `None` to give the column a known dtype.
- **Row operation assertions**: Use `assert_row_operation_works` from `tests.helpers`. It calls `table.add_computed_column()` with the given mapper and checks the resulting column values.
- **Polars dtype quirk**: `pl.lit(3)` produces `i32`, not `i64`. Keep this in mind for doctest output and test expectations.
- **One test file per method/feature**, named `test_<method>.py` (e.g., `test_init.py`, `test_name.py`).
- Use `@pytest.mark.parametrize` with `pytest.param(..., id=...)` — do **not** use a separate `ids=[...]` list.

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
- **Callback parameter naming**: `mapper` for value-mapping callbacks (returns `Cell`), `predicate` for filtering/quantifier callbacks (returns `Cell[bool | None]`), `key_selector` for sort key extraction.
- **Row/Cell not directly instantiable**: Only received via callbacks (e.g., `table.remove_rows(lambda row: ...)`).
- **Validation functions accept `Table | Schema`**: `check_columns_exist` and `check_columns_dont_exist` convert `Table` to its schema internally via late import. Callers pass `self` (the Table) directly, not `self.schema`.

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
- **Release**: Triggered manually via `release.yml` workflow. Uses semantic-release with `conventionalcommits` preset. Publishes to PyPI via trusted publishing.

## Development Workflow (TDD)

- **Write failing tests first**, then implement just enough to pass.
- Cover all lines and edge cases with a **minimal** number of tests. Don't duplicate coverage.
