# TODO — Functionality Not Yet Implemented

Sourced from `old_reference/`, tabular data preparation only. If something is not listed here, it's already done.

---

## 1. Plotter enhancements (`plotting/`)

### What's already done

All v1 plot methods are implemented and tested. `PlotConfig` and `AxisConfig` dataclasses exist. The API has been migrated from `title`/`theme` keyword args to `config: PlotConfig | None = None`.

### Step 2: Wire up `log` from `AxisConfig`

`AxisConfig(log: bool = False)` exists in `plotting/_axis_config.py`. `apply_axis_config` helper exists in `_plotting_utils.py`. Now add `x_axis`/`y_axis` parameters to methods and call `apply_axis_config`.

**Which methods get which axis params:**

- **`x_axis` only**: `ColumnPlotter.histogram`
- **`y_axis` only**: `ColumnPlotter.box_plot`, `ColumnPlotter.violin_plot`, `TablePlotter.box_plots`, `TablePlotter.violin_plots`
- **Both `x_axis` and `y_axis`**: `TablePlotter.scatter_plot`, `TablePlotter.line_plot`, `TablePlotter.histogram_2d`
- **Neither**: `TablePlotter.histograms` (multiple subplots, axis config would be ambiguous), `TablePlotter.correlation_heatmap` (heatmap axes don't support log scale meaningfully)

**Implementation per method:**

1. Add `x_axis: AxisConfig | None = None` and/or `y_axis: AxisConfig | None = None` to the method signature
2. Add the parameter docstring entries
3. Import `AxisConfig` in `TYPE_CHECKING` block of `_column_plotter.py` and `_table_plotter.py`
4. Import `apply_axis_config` from `_plotting_utils` in both files
5. Call `apply_axis_config(fig, x_axis, y_axis)` after `apply_config(fig, effective_config)` in each method body

**Tests:**

- Add `test_axis_log.py` (or add to existing test files) — one test per method that passes `x_axis=AxisConfig(log=True)` or `y_axis=AxisConfig(log=True)` and asserts the axis type is "log" in the figure dict:
  ```python
  fig_dict = plot._figure.to_dict()
  assert fig_dict["layout"]["xaxis"]["type"] == "log"  # for x_axis
  assert fig_dict["layout"]["yaxis"]["type"] == "log"  # for y_axis
  ```
- Keep minimal: one parametrized test per plotter (ColumnPlotter, TablePlotter) is enough, testing all axis configs.

**Commit**: `feat(plotting): add log axis support via AxisConfig`

### Step 3: Add `color_name` to `scatter_plot`

Add a `color_name: str | None = None` parameter to `TablePlotter.scatter_plot`. When provided, uses a third column's values to color the markers via a continuous color scale.

**Implementation:**

1. Add `color_name: str | None = None` parameter to `scatter_plot` method signature (before `config`)
2. Add validation: if `color_name` is not None, call `check_columns_exist(self._table, [color_name])` and `check_columns_are_numeric(self._table, [color_name], operation="color scatter plot")`
3. When `color_name` is not None:
   - Get the color column data: `color_data = self._table.get_column(color_name)`
   - Set `marker_color=color_data._series.drop_nulls().to_list()` and `marker_colorscale="Viridis"` and `marker_colorbar={"title": color_name}` on the `go.Scatter` trace
   - Note: need to drop nulls from color data and align with x/y data. Simplest approach: use the raw series without drop_nulls for color (Plotly handles None in marker_color by not coloring those points)
4. Update the docstring

**Tests:**

- Test that `color_name` creates a scatter plot with marker color data
- Test that `color_name` with non-existent column raises `ColumnNotFoundError`
- Test that `color_name` with non-numeric column raises `ColumnTypeError`
- Test that `color_name=None` (default) works as before (no color mapping)

**Commit**: `feat(plotting): add color_name parameter to scatter_plot`

### Step 4: Add `scatter_matrix` to `TablePlotter`

A scatter plot matrix showing pairwise relationships for all numeric columns.

**Implementation:**

1. Add `scatter_matrix` method to `TablePlotter`:
   ```python
   def scatter_matrix(
       self,
       *,
       config: PlotConfig | None = None,
   ) -> Plot:
   ```
2. Get numeric columns via `self._table.remove_non_numeric_columns().to_columns()`
3. If no numeric columns, raise `ColumnTypeError` (same as `box_plots`/`violin_plots`)
4. Use `go.Splom` trace:
   ```python
   dimensions = [{"label": col.name, "values": col._series.drop_nulls().to_list()} for col in columns]
   fig = go.Figure(data=go.Splom(dimensions=dimensions))
   fig.update_layout(dragmode="select")
   ```
5. Apply config

**Docstring:**
```
Create a scatter plot matrix for all numerical columns.

Parameters
----------
config:
    The configuration of the plot. If None, sensible defaults are used.

Returns
-------
plot:
    The scatter plot matrix.

Raises
------
ColumnTypeError
    If the table contains only non-numerical columns.
```

**Tests:**

- Test that scatter_matrix creates a plot with a splom trace
- Test that scatter_matrix raises ColumnTypeError for table with only non-numeric columns
- Test that scatter_matrix works with a single numeric column (1x1 matrix)

**Commit**: `feat(plotting): add scatter_matrix to TablePlotter`

### Step 5: Add `ecdf_plot` to `ColumnPlotter`

An empirical cumulative distribution function plot.

**Implementation:**

1. Add `ecdf_plot` method to `ColumnPlotter`:
   ```python
   def ecdf_plot(
       self,
       *,
       x_axis: AxisConfig | None = None,
       y_axis: AxisConfig | None = None,
       config: PlotConfig | None = None,
   ) -> Plot:
   ```
2. Compute ECDF data:
   ```python
   data = self._column._series.drop_nulls().sort()
   n = len(data)
   x = data.to_list()
   y = [(i + 1) / n for i in range(n)]
   ```
3. Create figure:
   ```python
   fig = go.Figure()
   fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name=self._column.name))
   fig.update_layout(xaxis_title=self._column.name, yaxis_title="Cumulative Probability")
   ```
4. Apply config and axis config

**Docstring:**
```
Create an empirical cumulative distribution function plot.

Parameters
----------
x_axis:
    The configuration of the x-axis. If None, sensible defaults are used.
y_axis:
    The configuration of the y-axis. If None, sensible defaults are used.
config:
    The configuration of the plot. If None, sensible defaults are used.

Returns
-------
plot:
    The ECDF plot.
```

**Tests:**

- Test that ecdf_plot creates a scatter trace with "lines" mode
- Test that ecdf_plot with empty column still works (no crash)
- Test that ecdf_plot with log axis works

**Commit**: `feat(plotting): add ecdf_plot to ColumnPlotter`

### Future extensions (not now)

- `ColumnPlotter.lag_plot(lag: int, *, config, ...) -> Plot` — standard time series diagnostic
- `TablePlotter.moving_average_plot(x_name, y_name, window_size, *, config, ...) -> Plot` — or fold into `line_plot` with a `window_size` parameter
- `ColumnPlotter.strip_plot(*, config, ...) -> Plot` — jittered points, useful alongside box/violin
- More `AxisConfig` fields: `label: str | None`, `range: tuple[float, float] | None`, `tick_format: str | None`
- More `PlotConfig` fields: `legend: bool`, `font_size: int`

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

## 3. Other

- Review API design, src code, tests, docstrings
- Compare with Safe-DS library once more (src and tests)
- Add example notebooks and more documentation
- Move issues on GitHub to new repo
- Compare with polars to find gaps
- Develop plan for future extensions
