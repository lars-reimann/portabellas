# TODO — Functionality Not Yet Implemented

Sourced from `old_reference/`, tabular data preparation only. If something is not listed here, it's already done.

---

## 1. Plotters (`plotting/`)

- **Reference source**: `old_reference/src/safeds/data/tabular/plotting/_table_plotter.py`, `old_reference/src/safeds/data/tabular/plotting/_column_plotter.py`
- **Reference tests**: `old_reference/tests/safeds/data/tabular/plotting/` (column_plotter/, table_plotter/)

Stubs exist with `__init__` only. All plot methods missing.

### Architecture

#### Plotting framework: Plotly or Altair (decide before implementing)

**Decision needed**: Choose between Plotly and Altair. Re-evaluate before implementation, particularly regarding performance.

##### Option A: Plotly

- Pros:
  - Full chart type coverage without workarounds (native violin, box, heatmap, etc.)
  - Rich interactivity out of the box (hover, zoom, pan)
  - Jupyter integration via `_repr_html_`
- Cons:
  - Heavier dependency, slower rendering for large datasets
  - Static export requires `kaleido` (optional dep, ~100MB binary)
  - kaleido can have cross-platform reliability issues

##### Option B: Altair

- Pros:
  - Declarative, based on Vega-Lite — very performant for large datasets
  - Deterministic SVG output (good for testing, no kaleido needed)
  - Static PNG export via `vl-convert-python` (pure Rust, no browser, small binary, cross-platform)
  - Jupyter integration via Vega-Lite renderer
  - Lighter dependency than Plotly
- Cons:
  - No native violin plots (must build from `transform_density` + `mark_area` — ~10 lines, but less polished)
  - Fewer chart types overall
  - Less interactive than Plotly (limited selection, no native zoom/pan in static render)
  - Combining multiple violins (e.g., `violin_plots` for a table) requires more manual work

#### Dependencies (if Plotly)

- `plotly` — **required** dependency (added to `dependencies` in `pyproject.toml`)
- `kaleido` — **optional** dependency under `portabellas[static-plots]` extra
  - Needed only for `.to_image()` on `Plot` objects
  - If not installed, `.to_image()` raises `ImportError` with install instructions
  - Tests gated with `pytest.importorskip("kaleido")`

#### Dependencies (if Altair)

- `altair` — **required** dependency
- `vl-convert-python` — **required** dependency (for PNG export, no browser needed, lightweight)

#### New classes

1. **`Plot`** (`plotting/_plot.py`)
   - Wraps a Plotly `Figure` or Altair `Chart`
   - `_repr_html_()` — rich display in Jupyter
   - `to_image() -> Image` — converts to static image (if Plotly: requires `kaleido`, raises `ImportError` with install instructions if missing; if Altair: uses `vl-convert-python`, always available)
   - `show() -> None` — opens in browser
   - Internal: `._figure` / `._chart` property returning the underlying object (for advanced users who want full customizability)

2. **`Image`** (`plotting/_image.py`)
   - Wraps `PIL.Image.Image` (Pillow)
   - `_repr_png_()` — rich display in Jupyter
   - `save(path: str | Path) -> None` — saves as PNG
   - Internal: `._pil_image` property returning the underlying Pillow image

#### New dependencies in `pyproject.toml` (if Plotly)

```toml
dependencies = [
    ...,
    "plotly>=6.0.0",
    "Pillow>=11.0.0",
]

[project.optional-dependencies]
static-plots = ["kaleido>=1.0.0"]
```

Pillow is a required dependency (needed for `Image` class). Plotly is a required dependency. Kaleido is optional.

#### New dependencies in `pyproject.toml` (if Altair)

```toml
dependencies = [
    ...,
    "altair>=5.5.0",
    "vl-convert-python>=1.7.0",
    "Pillow>=11.0.0",
]
```

All are required dependencies. No optional extras needed for static export.

#### Testing strategy

- **Primary**: Snapshot-test the figure/chart JSON (structure, not pixels). Extract the underlying dict and assert on key fields (data traces, layout, axis labels, etc.) or snapshot with syrupy.
- **Secondary**: Snapshot-test the rendered PNG via `plot.to_image()` → syrupy PNG snapshot. This verifies actual rendering. With Plotly, this is gated on kaleido and may be brittle across kaleido/OS versions. With Altair, PNG export is deterministic and always available, so this is more reliable.
- Doctest examples should use `to_image()` sparingly (only if kaleido is guaranteed for Plotly). Prefer testing figure structure.

### `TablePlotter`

- `box_plots(self, *, theme: Literal["dark", "light"] = "light") -> Plot`
- `histograms(self, *, max_bin_count: int = 10, theme: Literal["dark", "light"] = "light") -> Plot`
- `violin_plots(self, *, theme: Literal["dark", "light"] = "light") -> Plot`
- `line_plot(self, x_name: str, y_names: list[str], *, show_confidence_interval: bool = True, theme: Literal["dark", "light"] = "light") -> Plot`
- `histogram_2d(self, x_name: str, y_name: str, *, x_max_bin_count: int = 10, y_max_bin_count: int = 10, theme: Literal["dark", "light"] = "light") -> Plot`
- `moving_average_plot(self, x_name: str, y_name: str, window_size: int, *, theme: Literal["dark", "light"] = "light") -> Plot`
- `scatter_plot(self, x_name: str, y_names: list[str], *, theme: Literal["dark", "light"] = "light") -> Plot`
- `correlation_heatmap(self, *, theme: Literal["dark", "light"] = "light") -> Plot`

### `ColumnPlotter`

- `box_plot(self, *, theme: Literal["dark", "light"] = "light") -> Plot`
- `histogram(self, *, max_bin_count: int = 10, theme: Literal["dark", "light"] = "light") -> Plot`
- `lag_plot(self, lag: int, *, theme: Literal["dark", "light"] = "light") -> Plot`
- `violin_plot(self, *, theme: Literal["dark", "light"] = "light") -> Plot`

### Implementation order

1. Decide between Plotly and Altair
2. Add deps to `pyproject.toml`
3. Create `Plot` class (`plotting/_plot.py`) + `Image` class (`plotting/_image.py`)
4. Update `plotting/__init__.py` to re-export `Plot` and `Image`
5. Implement `ColumnPlotter` methods (simpler, fewer chart types)
6. Implement `TablePlotter` methods
7. Add tests (figure JSON snapshots + optional PNG snapshots)
8. Update `Table.plot` and `Column.plot` docstrings with examples
9. Delete old_reference plotting files once fully integrated

---

## 2. Struct support

### `DataType.Struct`

```python
@staticmethod
def Struct(fields: dict[str, DataType]) -> DataType:
```

- Maps to `pl.Struct([pl.Field(name, dtype) for name, dtype in fields.items()])`
- No separate `DataType.Field` — use `dict[str, DataType]` instead
- Add `is_struct: bool` abstract property on `DataType` + implementation on `PolarsDataType`
- Skip `DataType.fields` introspection property for now

### `cell.struct` namespace — `StructOperations` ABC

**File:** `query/_struct_operations/_struct_operations.py`

| Method | Signature | Polars equivalent | Description |
|---|---|---|---|
| `field` | `(name: str) -> Cell` | `expr.struct.field(name)` | Access a struct field by name |
| `rename` | `(old_name: str, new_name: str) -> Cell` | `expr.name.map_fields(fn)` | Rename a single struct field |
| `to_json` | `() -> Cell[str \| None]` | `expr.struct.json_encode()` | Convert struct to JSON string |

- **`rename` implementation:** Uses `expr.name.map_fields(lambda name: new_name if name == old_name else name)`, which is a pure lazy Polars expression. No schema access or `map_batches` needed.
- **Excluded:** `unnest` (returns multiple columns; belongs as `Column.unnest()`), `with_fields` (multi-column operation; belongs at Table/Row level), `__getitem__` / index-based access (omit per "prefer named functions" convention).

### `ExprStructOperations`

**File:** `query/_struct_operations/_expr_struct_operations.py`

Standard pattern: stores `self._expression: pl.Expr`, each method wraps Polars expr result in `ExprCell`.

### Wire-up

- `Cell` ABC: add `struct` abstract property returning `StructOperations`
- `ExprCell`: add `struct` concrete property returning `ExprStructOperations(self._expression)`
- `query/__init__.py`: re-export `StructOperations`

### New files

```
src/portabellas/query/_struct_operations/
├── __init__.py
├── _struct_operations.py
└── _expr_struct_operations.py
```

### Tests

```
tests/portabellas/query/_struct_operations/
├── __init__.py
├── test_field.py
├── test_rename.py
└── test_to_json.py
```

---

## 3. Additional `DataType` variants

- `Decimal(precision: int, scale: int) -> DataType`
- `Array(inner: DataType, width: int) -> DataType`
- `List(inner: DataType) -> DataType` (definitely!)
- `Categorical() -> DataType`
- `Enum(categories: list[str]) -> DataType`
- `Object() -> DataType`
- `Unknown() -> DataType`

---

## 4. Integration rules

- `old_reference/` is in `.gitignore` — use `rm` (not `git rm`) to delete files from it.
- Only delete old_reference files for items that are **fully integrated** (e.g., don't delete Row source if Row still has missing methods).
- TODO.md lists only **missing** functionality — if something isn't listed, it's already done.

---

## 5. Other

- Review API design, src code, tests, docstrings
- Compare with Safe-DS library once more (src and tests)
- Add example notebooks and more documentation
- Move issues on GitHub to new repo
- Compare with polars to find gaps
- Develop plan for future extensions
