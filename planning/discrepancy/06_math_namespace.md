# Math Namespace Discrepancies

## Polars has, Portabellas doesn't

| Polars (Expr methods) | Notes |
|---|---|
| `cot()` | Cotangent |
| `degrees()` | Radians to degrees |
| `radians()` | Degrees to radians |
| `log1p()` | log(1+x) |
| `clip(lower_bound, upper_bound)` | Clip values to bounds |
| `truncate(decimals)` | Truncate toward zero |
| `pow(exponent)` as method | Power (Portabellas has operator only) |
| `round(decimals, mode)` | Round with mode (half_to_even vs half_away_from_zero) |
| `nan_max()` / `nan_min()` | Max/min with NaN propagation |

---

## Portabellas has, Polars doesn't

| Portabellas (`cell.math`) | Notes |
|---|---|
| `degrees_to_radians()` | Named method (Polars: `expr.radians()`) |
| `radians_to_degrees()` | Named method (Polars: `expr.degrees()`) |
| `round_to_decimal_places(decimal_places)` | Named method (Polars: `expr.round(decimals)`) |
| `round_to_significant_figures(significant_figures)` | Named method (Polars: `expr.round_sig_figs(digits)`) |
| `ln()` | Natural log (Polars: `expr.log(base=e)` or `expr.log()`) |
| `log(base)` | Log with base (Polars: `expr.log(base)`) |
| `log10()` | Base-10 log (Polars: `expr.log10()`) |

---

## Both have but with different APIs

| Feature | Portabellas | Polars | Difference |
|---|---|---|---|
| Abs | `cell.math.abs()` | `expr.abs()` | Portabellas: namespace; Polars: direct |
| Acos/Acosh/Asin/Asinh/Atan/Atanh | `cell.math.acos/acosh/asin/asinh/atan/atanh()` | `expr.arccos/arccosh/arcsin/arcsinh/arctan/arctanh()` | Different names (short vs long) |
| Cbrt | `cell.math.cbrt()` | `expr.cbrt()` | Same |
| Ceil | `cell.math.ceil()` | `expr.ceil()` | Portabellas: namespace; Polars: direct |
| Cos/Cosh/Sin/Sinh/Tan/Tanh | `cell.math.cos/cosh/sin/sinh/tan/tanh()` | `expr.cos/cosh/sin/sinh/tan/tanh()` | Portabellas: namespace; Polars: direct |
| Exp | `cell.math.exp()` | `expr.exp()` | Same naming |
| Floor | `cell.math.floor()` | `expr.floor()` | Portabellas: namespace; Polars: direct |
| Sign | `cell.math.sign()` | `expr.sign()` | Same |
| Sqrt | `cell.math.sqrt()` | `expr.sqrt()` | Same |
