# AGENTS.md → Skills Rewrite Plan

## Goal

Split the monolithic `AGENTS.md` into:
1. A lean `AGENTS.md` (always-loaded essentials)
2. On-demand skill files in `.opencode/skills/<name>/SKILL.md`

## OpenCode Skills System

- Skills are auto-discovered from `.opencode/skills/<name>/SKILL.md`
- Each `SKILL.md` requires YAML frontmatter with `name` (lowercase, hyphen-separated, 1-64 chars) and `description` (1-1024 chars)
- Agents see available skills via the `skill` tool description and call `skill({ name: "..." })` to load the full content
- Skills load on-demand — only the name + description is in context until loaded

## Structure After Rewrite

### `AGENTS.md` (always-loaded)

Keep only the most frequently needed sections:

```markdown
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

## Development Workflow

- **Never commit directly to `main`**. Always develop on a separate feature branch.
- **Write failing tests first**, then implement just enough to pass (TDD).
- Cover all lines and edge cases with a **minimal** number of tests. Don't duplicate coverage.
- **Small, incremental commits** per logical change — not one giant commit per feature.

### Commit Conventions

- **Conventional commits** for all commit messages (required for semantic-release version bumps):
  - `feat:` new feature → minor version bump
  - `fix:` bug fix → patch version bump
  - `refactor:`, `test:`, `docs:`, `perf:`, `build:`, `ci:` for other changes (no version bump)
  - `feat!:` or `BREAKING CHANGE:` in footer → major version bump
- Scope is optional: `feat(containers): add Column.sort()`.
```

### Skills to Create (in `.opencode/skills/<name>/SKILL.md`)

#### 1. `architecture` — Internal Architecture

**Description**: Internal architecture: src layout, core submodules, Polars LazyFrame internals, IO design, Row/Cell ABCs, ExprRow/ExprCell, cell namespaces, exceptions, validation.

```markdown
---
name: architecture
description: Internal architecture: src layout, core submodules, Polars LazyFrame internals, IO design, Row/Cell ABCs, cell namespaces, exceptions, validation.
compatibility: opencode
---

## Architecture

- **Src layout**: `src/portabellas/` is the package. Public API: `Table`, `Column`, `Row`, `Cell` from `portabellas.containers`; `DataType`, `Schema` from `portabellas.typing`.
- **Core submodules**: `containers/`, `query/` (cell operation namespaces), `typing/`, `io/`, `plotting/`, `exceptions/`, `_validation/`, `_config/`, `_utils/`.
- **Polars LazyFrame internally**: Both `Table` and `Column` store `_lazy_frame` (LazyFrame) as the primary representation. `_data_frame`/`_series` are lazily cached properties — accessed via `._data_frame` / `._series`, which collect on first access and re-anchor the LazyFrame. `Table.schema` is similarly cached in `__schema_cache`.
- **IO**: `TableReader` (static methods: `csv_file`, `json_file`, `parquet_file`, `jsonl_file`) and `TableWriter` (instance methods on `self._table`). Factory/export methods (`from_columns`, `from_dict`, `to_columns`, `to_dict`) are on `Table` directly, not via `Table.read.*`/`table.write.*`.
- **Row ABC / ExprRow**: `Row` is an abstract base class. `ExprRow` is the concrete subclass that stores a `Table` reference and delegates all property/method calls to it. Users receive `ExprRow` instances via callbacks (e.g., `table.add_computed_column("c", lambda row: ...)`).
- **Cell ABC / ExprCell**: `Cell` is an abstract base class. `ExprCell` is the concrete subclass that wraps a Polars `Expr`. Users receive `ExprCell` instances via callbacks (e.g., `column.map(lambda cell: ...)`).
- **ExprRow/ExprCell are not re-exported**: Tests import them directly as `from portabellas.containers._row import ExprRow` and `from portabellas.containers._cell import ExprCell`.
- **Cell namespaces**: `cell.str` → `StringOperations`/`ExprStringOperations`, `cell.dt` → `DatetimeOperations`/`ExprDatetimeOperations`, `cell.dur` → `DurationOperations`/`ExprDurationOperations`, `cell.math` → `MathOperations`/`ExprMathOperations`. Each is an ABC in `_foo_operations.py` + concrete `ExprFooOperations` in `_expr_foo_operations.py`, both in `query/_foo_operations/`.
- **Exceptions**: All inherit from `PortabellasError`. Existing: `ColumnNotFoundError`, `DuplicateColumnError`, `FileExtensionError`, `IndexOutOfBoundsError`, `LazyComputationError`, `LengthMismatchError`, `OutOfBoundsError`. Add new ones as needed.
- **Validation**: `_validation/` contains `check_bounds`, `check_columns_dont_exist`, `check_columns_exist`, `check_indices`, `check_row_counts_are_equal`, `check_time_zone`, `normalize_and_check_file_path`. Add new ones as needed.
```

#### 2. `style` — Code Style & Linting

**Description**: Code style: Ruff select = ALL, line length 120, numpy docstrings, mypy strict settings, circular import handling, optional deps, no-comments rule.

```markdown
---
name: style
description: Code style: Ruff select = ALL, line length 120, numpy docstrings, mypy strict, circular import handling, optional deps, no-comments rule.
compatibility: opencode
---

## Style & Linting

- **Ruff**: `select = ["ALL"]` (not the default), with various rules overridden in `pyproject.toml`.
- **Line length**: 120 (not ruff default 88).
- **Docstring convention**: numpy.
- **mypy**: strict, but `disallow_any_generics = false`, `disallow_untyped_decorators = false`, `no_warn_return_any = true`.
- **Circular imports**: Late-import inside the method body with a `# circular import  # noqa: PLC0415` comment. Only use late imports for genuinely circular dependencies — verify before adding. Non-circular imports should be at the top of the file.
- **Optional dependencies**: Guard optional dependency imports at the top of the file with `try/except ImportError`, raising an `ImportError` with install instructions. Use `importlib.util.find_spec` to check availability without importing.
- **No comments** in code unless explicitly requested or to explain gotchas (e.g., the `# circular import` comment). No emojis.
```

#### 3. `api-design` — API Design Conventions

**Description**: API design conventions: immutability, lazy Row/Cell, no axis/kwargs, keyword-only params, methods over functions, exception wrapping, callback naming.

```markdown
---
name: api-design
description: API design conventions: immutability, lazy Row/Cell, no axis/kwargs, keyword-only params, methods over functions, exception wrapping, callback naming.
compatibility: opencode
---

## API Design

- **Immutability**: All container methods return new objects; never mutate in-place.
- **Lazy Row/Cell**: `Row` and `Cell` objects build Polars expressions internally. They must not materialize actual Python values — doing so causes 100–1000x slowdowns.
- **No `axis` parameter**: Use explicit names like `remove_columns` / `remove_rows`.
- **No `**kwargs`**: Explicitly list all allowed parameters.
- **Optional parameters are keyword-only**: Use `*` separator to enforce this.
- **No parameter dependencies**: If a parameter's meaning depends on another parameter value, split into separate functions.
- **Prefer methods to global functions**: Enables chaining and code-completion.
- **Prefer named functions to operators**: Operators don't appear in code-completion and can be ambiguous. (Cell operator overloading for numeric `==`, `<`, `+` is an exception.)
- **No uncommon abbreviations**: Use full words; common DS abbreviations (CSV, min, max) are fine.
- **Check preconditions early**: Validate at function start, before expensive work. `_validation/` contains commonly needed checks.
- **Wrap underlying exceptions**: Catch/wrap Polars exceptions with custom exceptions in `exceptions/`, inheriting from `PortabellasError`.
- **Callback parameter naming**: `mapper` for value-mapping callbacks (returns `Cell`), `predicate` for filtering/quantifier callbacks (returns `Cell[bool | None]`), `key_selector` for sort key extraction.
- **Row/Cell not directly instantiable**: Only received via callbacks (e.g., `table.remove_rows(lambda row: ...)`).
```

#### 4. `testing` — Testing Conventions & Helpers

**Description**: Testing conventions: layout, __init__.py requirement, one file per method, parametrize style, public API, doctests, snapshot testing, test helpers.

```markdown
---
name: testing
description: Testing conventions: layout, __init__.py, one file per method, parametrize style, public API, doctests, snapshot testing, test helpers.
compatibility: opencode
---

## Testing

- Tests mirror `src/portabellas/` layout under `tests/portabellas/`.
- **Every test subdirectory needs an `__init__.py`** (can be empty). Otherwise, file names of tests would need to be globally unique.
- **One test file per method/feature**, named `test_<method>.py` (e.g., `test_init.py`, `test_name.py`).
- Use `@pytest.mark.parametrize` with `pytest.param(..., id=...)` — do **not** use a separate `ids=[...]` list.
- **Use public API in tests** — no `table._data_frame`, use `table["col"]` etc.
- pytest runs **doctests** too (`--doctest-modules` is in addopts). Doctest examples must only use implemented functionality.
- **Snapshot testing** via syrupy. Update snapshots with `--snapshot-update`.

### Test Helpers

- **Table assertions**: Use `assert_tables_are_equal` from `tests.helpers` (wraps `polars.testing.assert_frame_equal`).
- **Row operation assertions**: Use `assert_row_operation_works` from `tests.helpers`. It calls `table.add_computed_column()` with the given mapper and checks the resulting column values.
- **Cell operation assertions**: Use `assert_cell_operation_works` from `tests.helpers`. It creates a `Column("a", [value])`, calls `.map()`, and checks the result. Use the `type_if_none` keyword argument when the input value is `None` to give the column a known dtype.
- **Resource path helper**: `resolve_resource_path` from `tests.helpers` resolves paths to `tests/resources/` fixture files.
```

#### 5. `docs` — Documentation Conventions

**Description**: Documentation conventions: mkdocs with mkdocstrings, auto-generated reference pages (do not edit by hand).

```markdown
---
name: docs
description: Documentation conventions: mkdocs with mkdocstrings, auto-generated reference pages (do not edit by hand).
compatibility: opencode
---

## Docs

- mkdocs with mkdocstrings. Reference pages are **auto-generated**. Do not edit files in `docs/reference/portabellas/` by hand.
```

## Implementation Steps

1. Create directory `.opencode/skills/` (root of project, alongside `AGENTS.md`)
2. Create subdirectories with `SKILL.md` files:
   - `.opencode/skills/architecture/SKILL.md`
   - `.opencode/skills/style/SKILL.md`
   - `.opencode/skills/api-design/SKILL.md`
   - `.opencode/skills/testing/SKILL.md`
   - `.opencode/skills/docs/SKILL.md`
3. Update `AGENTS.md` to keep only Setup, Commands, Development Workflow (including Commit Conventions)
4. Verify skill files are valid (valid YAML frontmatter, `name` matches directory name, `description` is 1-1024 chars)
