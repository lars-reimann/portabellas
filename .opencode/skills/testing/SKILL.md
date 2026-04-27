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
