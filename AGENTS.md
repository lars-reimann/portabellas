# AGENTS.md

## Setup

- **Package manager**: uv (not pip/poetry). Use `uv sync` to install, `uv run <cmd>` to execute.
- **Python**: 3.12–3.13 only (`>=3.12,<3.14`).

## Commands

```bash
uv run ruff check --fix # lint (ruff lint, ALL rules selected, numpy docstring convention)
uv run ruff format # format
uv run mypy src # typecheck (strict mode)
uv run pytest # run tests
uv run pytest tests/portabellas/containers/_column/test_init.py # single test file
uv run pytest --cov=portabellas # with coverage
```

Pre-commit hooks run ruff-check (with `--fix`), ruff-format, and mypy.

## Architecture

- **Src layout**: `src/portabellas/` is the package. Public API exports `Column` and `Table` from `containers/`.
- Core submodules: `containers/` (Table, Column, Row, Cell), `query/` (cell operation namespaces backing cell.str, cell.dt, etc.), `typing/` (DataType, Schema), `io/` (read/write), `plotting/`, `_validation/`, `_config/`, `_utils/`.
- `Table` and `Column` wrap Polars DataFrames/Series via private `_data_frame`/`_series` attributes.

## Style & Linting

- **Line length**: 120 (not ruff default 88).
- **Ruff**: `select = ["ALL"]` with specific ignores (see `pyproject.toml`). Key ones:
  - `D100`/`D104` ignored (no module/package docstrings required)
  - `SLF001` ignored (private attribute access is acceptable)
  - `PLR09` ignored (no complexity limits)
  - `ANN401` ignored (`Any` types allowed)
- **Docstring convention**: numpy.
- **mypy**: strict, but `disallow_any_generics = false`, `disallow_untyped_decorators = false`, `no_warn_return_any = true`.
- Test files: `D103`, `FBT001`, `INP001`, `S101` additionally ignored.

## Testing

- pytest runs **doctests** too (`--doctest-modules` is in addopts).
- **Snapshot testing** via syrupy (`--snapshot-warn-unused` in addopts). Update snapshots with `--snapshot-update`.
- Tests mirror `src/portabellas/` layout under `tests/portabellas/`.
- Use `assert_tables_are_equal` from `tests.helpers` (wraps `polars.testing.assert_frame_equal`) instead of manual assertions.

## Docs

- mkdocs with mkdocstrings. Reference pages are **auto-generated** by `docs/reference/generate_reference_pages.py` (triggered by `gen-files` plugin). Do not edit files in `docs/reference/portabellas/` by hand.

## API Design

- **Immutability**: All container methods return new objects; never mutate in-place.
- **Lazy Row/Cell**: `Row` and `Cell` objects build Polars expressions internally (via `ExprRow`/`ExprCell` subclasses). They must not materialize actual Python values — doing so causes 100–1000x slowdowns.
- **No `axis` parameter**: Use explicit names like `remove_columns` / `remove_rows` instead of a single method with an `axis` kwarg.
- **No `**kwargs`**: Explicitly list all allowed parameters.
- **Optional parameters are keyword-only**: Use `*` separator to enforce this.
- **No parameter dependencies**: If a parameter's meaning depends on another parameter's value, split into separate functions.
- **Prefer methods to global functions**: Enables chaining and code-completion.
- **Prefer named functions to operators**: Operators don't appear in code-completion and can be ambiguous. (Cell operator overloading for numeric `==`, `<`, `+` is an exception.)
- **No uncommon abbreviations**: Use full words; common DS abbreviations (CSV, min, max) are fine.
- **Check preconditions early**: Validate at function start, before expensive work.
- **Wrap underlying exceptions**: Catch/wrap Polars exceptions with custom exceptions in `exceptions/`, inheriting from `PortabellasError`.
- **Cell namespaces**: `cell.str` for string ops, `cell.dt` for datetime ops.
- **Row/Cell not directly instantiable**: Only received via callbacks (e.g., `table.remove_rows(lambda row: ...)`).

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
- Use `@pytest.mark.parametrize` with descriptive `id`s instead of many separate test methods — easier to extend later:
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
- Run `uv run ruff check --fix && uv run ruff format && uv run mypy src && uv run pytest tests` before committing.
