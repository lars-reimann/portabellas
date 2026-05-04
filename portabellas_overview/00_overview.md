# Portabellas Public API Overview

This folder contains a comprehensive overview of the public API of the [Portabellas](https://github.com/lars-reimann/portabellas) library,
extracted from the source code. Each file covers a major module or class.

## File Index

| File | Content |
|------|---------|
| [01_table.md](01_table.md) | `Table` class — constructor, properties, methods, factory methods |
| [02_column.md](02_column.md) | `Column` class — constructor, properties, methods |
| [03_row_cell.md](03_row_cell.md) | `Row` (ABC), `ExprRow`, `Cell` (ABC), `ExprCell` — properties, methods, operators |
| [04_cell_namespaces.md](04_cell_namespaces.md) | Cell namespace ABCs and their Expr implementations: `.str`, `.dt`, `.dur`, `.math`, `.list`, `.struct` |
| [05_datatypes.md](05_datatypes.md) | `DataType` class (factory methods, properties), `PolarsDataType`, `Schema` |
| [06_io.md](06_io.md) | `TableReader` (static read methods), `TableWriter` (instance write methods) |
| [07_plotting.md](07_plotting.md) | `TablePlotter`, `ColumnPlotter` |
| [08_exceptions.md](08_exceptions.md) | All exception classes inheriting from `PortabellasError` |
| [09_validation_config_utils.md](09_validation_config_utils.md) | Validation functions, Config, utility functions |

## Conventions

- Each entry lists the **full signature** (parameters with types and defaults, return type) and the **first sentence of the docstring**.
- Abstract methods are marked with *(abstract)*.
- Deprecated methods are marked with *(deprecated)*.
- Private methods (starting with `_`) are excluded, except for dunder methods that are part of the public API.
