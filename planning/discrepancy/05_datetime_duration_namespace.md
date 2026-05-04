# Datetime & Duration Namespace Discrepancies

## Datetime: Polars has, Portabellas doesn't

| Polars (`expr.dt` / `series.dt`) | Notes |
|---|---|
| `add_business_days(n, *, week_mask, holidays, roll)` | Add business days |
| `base_utc_offset()` | Base UTC offset of timezone |
| `cast_time_unit(tu)` | Cast time unit |
| `cast_time_zone(tz)` | Cast time zone |
| `combine(time, time_unit, *, ambiguous)` | Combine Date + Time to Datetime |
| `convert_time_zone(time_zone)` | Convert timezone |
| `dst_offset()` | DST offset |
| `epoch(time_unit)` | Get epoch value |
| `iso_year()` | ISO year (distinct from `year`) |
| `microsecond()` | Microsecond component |
| `millisecond()` | Millisecond component |
| `nanosecond()` | Nanosecond component |
| `month_end()` / `month_start()` | First/last day of month |
| `nanosecond()` | Nanosecond component |
| `offset_by(by)` | Offset by duration string |
| `replace_time_zone(time_zone, *, ambiguous)` | Replace timezone without converting |
| `strftime(format)` | Format as string (Portabellas: `to_string(format)`) |
| `time_zone()` | Get timezone string |
| `timestamp(time_unit)` | Get timestamp |
| `truncate(every)` | Truncate to interval |
| `weekday()` | Weekday (Mon=0) (Portabellas: `day_of_week`) |
| `week()` | ISO week number (Portabellas: `week()`) |

---

## Datetime: Portabellas has, Polars doesn't

| Portabellas (`cell.dt`) | Notes |
|---|---|
| `century()` | Century (Polars has it too) |
| `day_of_year()` | Day of year (Polars: no direct method; use `expr.dt.ordinal_day()` or compute) |
| `millennium()` | Millennium (no Polars equivalent) |
| `to_string(*, format)` | Convert to string (Polars: `strftime(format)`) |
| `unix_timestamp(*, unit)` | Unix timestamp (Polars: `epoch(time_unit)`) |

---

## Both have but with different APIs

| Feature | Portabellas | Polars | Difference |
|---|---|---|---|
| Century | `cell.dt.century()` | `expr.dt.century()` | Same |
| Date | `cell.dt.date()` | `expr.dt.date()` | Same |
| Day | `cell.dt.day()` | `expr.dt.day()` | Same |
| Day of week | `cell.dt.day_of_week()` | `expr.dt.weekday()` | Different name (ISO vs Polars naming) |
| Hour | `cell.dt.hour()` | `expr.dt.hour()` | Same |
| Is leap year | `cell.dt.is_in_leap_year()` | `expr.dt.is_leap_year()` | Same |
| Minute | `cell.dt.minute()` | `expr.dt.minute()` | Same |
| Month | `cell.dt.month()` | `expr.dt.month()` | Same |
| Quarter | `cell.dt.quarter()` | `expr.dt.quarter()` | Same |
| Second | `cell.dt.second()` | `expr.dt.second()` | Same |
| Time | `cell.dt.time()` | `expr.dt.time()` | Same |
| Week | `cell.dt.week()` | `expr.dt.week()` | Same |
| Year | `cell.dt.year()` | `expr.dt.year()` | Same |
| Replace | `cell.dt.replace(*, year, month, day, hour, minute, second, microsecond)` | `expr.dt.replace(*, year, month, day, hour, minute, second, microsecond, nanosecond, ambiguous)` | Polars has nanosecond + ambiguous |

---

## Duration: Polars has, Portabellas doesn't

| Polars (via `expr.dt` / `series.dt`) | Notes |
|---|---|
| `total_days()` | Total days |
| `total_hours()` | Total hours |
| `total_minutes()` | Total minutes |
| `total_seconds()` | Total seconds |
| `total_milliseconds()` | Total milliseconds |
| `total_microseconds()` | Total microseconds |
| `total_nanoseconds()` | Total nanoseconds |

---

## Duration: Portabellas has, Polars doesn't

| Portabellas (`cell.dur`) | Notes |
|---|---|
| `abs()` | Absolute value of duration (Polars: `expr.abs()` on duration column) |
| `full_weeks()` | Full weeks (Polars: `total_days() // 7`) |
| `full_days()` | Full days (Polars: `total_days()`) |
| `full_hours()` | Full hours (Polars: `total_hours()`) |
| `full_minutes()` | Full minutes (Polars: `total_minutes()`) |
| `full_seconds()` | Full seconds (Polars: `total_seconds()`) |
| `full_milliseconds()` | Full milliseconds (Polars: `total_milliseconds()`) |
| `full_microseconds()` | Full microseconds (Polars: `total_microseconds()`) |
| `to_string(*, format)` | Format duration (Polars: no direct method) |

---

## Both have but with different APIs

| Feature | Portabellas | Polars | Difference |
|---|---|---|---|
| Total days | `cell.dur.full_days()` | `expr.dt.total_days()` | Different name; Portabellas rounds down (full), Polars returns total |
| Total hours | `cell.dur.full_hours()` | `expr.dt.total_hours()` | Same naming difference |
| Total minutes | `cell.dur.full_minutes()` | `expr.dt.total_minutes()` | Same naming difference |
| Total seconds | `cell.dur.full_seconds()` | `expr.dt.total_seconds()` | Same naming difference |
| Total milliseconds | `cell.dur.full_milliseconds()` | `expr.dt.total_milliseconds()` | Same naming difference |
| Total microseconds | `cell.dur.full_microseconds()` | `expr.dt.total_microseconds()` | Same naming difference |
| Duration as string | `cell.dur.to_string(*, format)` | No direct equivalent | Portabellas has "iso" and "pretty" formats |
