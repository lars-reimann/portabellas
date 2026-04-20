# TODO — Functionality Not Yet Implemented

Sourced from `old_reference/`, tabular data preparation only. If something is not listed here, it's already done.

---

## 1. Plotters (`plotting/`)

- **Reference source**: `old_reference/src/safeds/data/tabular/plotting/_table_plotter.py`, `old_reference/src/safeds/data/tabular/plotting/_column_plotter.py`
- **Reference tests**: None (plotting had no separate test files in the old reference)

Stubs exist with `__init__` only. All plot methods missing.

### `TablePlotter`

- `box_plots(self, *, theme: Literal["dark", "light"] = "light") -> Image`
- `histograms(self, *, max_bin_count: int = 10, theme: Literal["dark", "light"] = "light") -> Image`
- `violin_plots(self, *, theme: Literal["dark", "light"] = "light") -> Image`
- `line_plot(self, x_name: str, y_names: list[str], *, show_confidence_interval: bool = True, theme: Literal["dark", "light"] = "light") -> Image`
- `histogram_2d(self, x_name: str, y_name: str, *, x_max_bin_count: int = 10, y_max_bin_count: int = 10, theme: Literal["dark", "light"] = "light") -> Image`
- `moving_average_plot(self, x_name: str, y_name: str, window_size: int, *, theme: Literal["dark", "light"] = "light") -> Image`
- `scatter_plot(self, x_name: str, y_names: list[str], *, theme: Literal["dark", "light"] = "light") -> Image`
- `correlation_heatmap(self, *, theme: Literal["dark", "light"] = "light") -> Image`
- Potentially create interactive plots (e.g. with plotly?), instead of static matplotlib plots

### `ColumnPlotter`

- `box_plot(self, *, theme: Literal["dark", "light"] = "light") -> Image`
- `histogram(self, *, max_bin_count: int = 10, theme: Literal["dark", "light"] = "light") -> Image`
- `lag_plot(self, lag: int, *, theme: Literal["dark", "light"] = "light") -> Image`
- `violin_plot(self, *, theme: Literal["dark", "light"] = "light") -> Image`
- Potentially create interactive plots (e.g. with plotly?), instead of static matplotlib plots

---

## 2. Additional `DataType` variants

- `Decimal(precision: int, scale: int) -> DataType`
- `Array(inner: DataType, width: int) -> DataType`
- `List(inner: DataType) -> DataType` (definitely!)
- `Struct(fields: list[tuple[str, DataType]]) -> DataType`  (definitely!)
- `Categorical() -> DataType`
- `Enum(categories: list[str]) -> DataType`
- `Object() -> DataType`
- `Unknown() -> DataType`

---

## 3. Integration rules

- `old_reference/` is in `.gitignore` — use `rm` (not `git rm`) to delete files from it.
- Only delete old_reference files for items that are **fully integrated** (e.g., don't delete Row source if Row still has missing methods).
- TODO.md lists only **missing** functionality — if something isn't listed, it's already done.

---

## 4. Other

- Review API design, src code, tests, docstrings
- Compare with Safe-DS library once more (src and tests)
- Add example notebooks and more documentation
- Move issues on GitHub to new repo
- Compare with polars to find gaps
- Develop plan for future extensions
