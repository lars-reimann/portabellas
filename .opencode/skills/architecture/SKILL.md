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
