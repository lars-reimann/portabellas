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
