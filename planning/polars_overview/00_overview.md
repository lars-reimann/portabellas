# Polars Public API Overview

This folder contains a comprehensive overview of the public API of the [Polars](https://pola.rs/) library,
extracted from the source code. Each file covers a major module or class.

## File Index

| File | Content |
|------|---------|
| [01_dataframe.md](01_dataframe.md) | `DataFrame` class — constructor, properties, methods |
| [02_lazyframe.md](02_lazyframe.md) | `LazyFrame` class — constructor, properties, methods |
| [03_series.md](03_series.md) | `Series` class — constructor, properties, methods |
| [04_expr.md](04_expr.md) | `Expr` class — constructor, properties, methods, operators |
| [05_datatypes.md](05_datatypes.md) | Data type classes (`Int8`, `String`, `Datetime`, `List`, `Struct`, etc.) and `DataTypeExpr` |
| [06_expr_namespaces.md](06_expr_namespaces.md) | Expr namespace accessors: `.str`, `.dt`, `.cat`, `.list`, `.struct`, `.bin`, `.arr`, `.meta`, `.name`, `.ext` |
| [07_series_namespaces.md](07_series_namespaces.md) | Series namespace accessors: `.str`, `.dt`, `.cat`, `.list`, `.struct`, `.bin`, `.arr` |
| [08_functions.md](08_functions.md) | Top-level functions: `col`, `lit`, `when`, `concat`, `sum`, `mean`, date ranges, etc. |
| [09_io.md](09_io.md) | IO functions: `read_csv`, `scan_parquet`, `write_*`, `sink_*`, credential providers |
| [10_groupby.md](10_groupby.md) | `GroupBy`, `LazyGroupBy`, `DynamicGroupBy`, `RollingGroupBy` |
| [11_when_then.md](11_when_then.md) | `When`, `Then`, `ChainedWhen`, `ChainedThen` (when-then-otherwise chain) |
| [12_schema_config_misc.md](12_schema_config_misc.md) | `Schema`, `Config`, `SQLContext`, `StringCache`, `Selectors`, `CompatLevel`, `QueryOptFlags`, `GPUEngine`, exceptions, meta, convert, catalog, api |

## Conventions

- Each entry lists the **full signature** (parameters with types and defaults, return type) and the **first sentence of the docstring**.
- Deprecated methods are marked with *(deprecated)*.
- Unstable methods are marked with *(unstable)*.
- Private methods (starting with `_`) are excluded, except for dunder methods that are part of the public API.
