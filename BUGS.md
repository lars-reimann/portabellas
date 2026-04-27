# Known Bugs in `feat/plotting`

## High

### scatter_plot & histogram_2d — independent `drop_nulls()` misaligns paired data

`src/portabellas/plotting/_table_plotter.py`:

- `scatter_plot` (line ~486): x and y data are filtered of nulls independently via `._series.drop_nulls()`. This destroys pairwise alignment. For data where `x=[1, null, 3]` and `y=[4, 5, null]`, the result is `x=[1, 3], y=[4, 5]`, which plots (1,4) and (3,5) — neither is a real row.
- Additionally, `color_name` data is not null-filtered at all, causing a potential length mismatch between `marker.color` and the x/y arrays.
- `histogram_2d` (line ~411-412): Same independent `drop_nulls()` issue for 2D histograms.

**Fix**: Drop rows where *either* the x or y column is null, preserving pairs. Use `table.drop_nulls(subset=[x_name, y_name])`.

---

## Medium

### correlation_heatmap — `fill_null(0)` biases correlation

`src/portabellas/plotting/_table_plotter.py:589`:
```python
corr_df = numerical_table._data_frame.fill_null(0).corr()
```

Replacing nulls with `0` before computing correlation silently produces incorrect coefficients for any dataset containing nulls. Polars' `.corr()` already excludes null pairs by default, so `fill_null(0)` is both unnecessary and harmful.

**Fix**: Remove `fill_null(0)`:
```python
corr_df = numerical_table._data_frame.corr()
```

### histogram_2d — missing numeric validation

`src/portabellas/plotting/_table_plotter.py:400-402` checks column existence and bin-count bounds, but never validates that `x_name` and `y_name` are numeric. The docstring claims a `ColumnTypeError` is raised for non-numeric columns.

**Fix**: Add `check_columns_are_numeric` for both x and y columns, or raise `ColumnTypeError` explicitly.

---

## Low

### `assert_plot_has_theme` not exported from test helpers

`tests/helpers/_plot_assertions.py` defines `assert_plot_has_theme`, but `tests/helpers/__init__.py` does not export it. It must be imported via the private module path — or it may be dead code if no test uses it.

**Fix**: Add the export to `tests/helpers/__init__.py` if tests depend on it; otherwise remove the function.
