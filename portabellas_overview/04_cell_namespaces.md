# Cell Namespaces

Sources:
- `src/portabellas/query/_string_operations/` — `StringOperations` (ABC), `ExprStringOperations`
- `src/portabellas/query/_datetime_operations/` — `DatetimeOperations` (ABC), `ExprDatetimeOperations`
- `src/portabellas/query/_duration_operations/` — `DurationOperations` (ABC), `ExprDurationOperations`
- `src/portabellas/query/_math_operations/` — `MathOperations` (ABC), `ExprMathOperations`
- `src/portabellas/query/_list_operations/` — `ListOperations` (ABC), `ExprListOperations`
- `src/portabellas/query/_struct_operations/` — `StructOperations` (ABC), `ExprStructOperations`

All `Expr*` classes have `__init__(self, expression: pl.Expr) -> None` (not shown below for brevity).

---

## StringOperations (ABC)

### Methods

`contains(self, substring: ConvertibleToStringCell) -> Cell[bool | None]` *(abstract)* — Check if the string contains the substring.

`ends_with(self, suffix: ConvertibleToStringCell) -> Cell[bool | None]` *(abstract)* — Check if the string ends with the suffix.

`index_of(self, substring: ConvertibleToStringCell) -> Cell[int | None]` *(abstract)* — Get the index of the first occurrence of the substring.

`length(self, *, optimize_for_ascii: bool = False) -> Cell[int | None]` *(abstract)* — Get the number of characters.

`pad_end(self, length: int, *, character: str = " ") -> Cell[str | None]` *(abstract)* — Pad the end of the string with the given character until it has the given length.

`pad_start(self, length: int, *, character: str = " ") -> Cell[str | None]` *(abstract)* — Pad the start of the string with the given character until it has the given length.

`remove_prefix(self, prefix: ConvertibleToStringCell) -> Cell[str | None]` *(abstract)* — Remove a prefix from the string.

`remove_suffix(self, suffix: ConvertibleToStringCell) -> Cell[str | None]` *(abstract)* — Remove a suffix from the string.

`repeat(self, count: ConvertibleToIntCell) -> Cell[str | None]` *(abstract)* — Repeat the string a number of times.

`replace_all(self, old: ConvertibleToStringCell, new: ConvertibleToStringCell) -> Cell[str | None]` *(abstract)* — Replace all occurrences of the old substring with the new substring.

`reverse(self) -> Cell[str | None]` *(abstract)* — Reverse the string.

`slice(self, *, start: ConvertibleToIntCell = 0, length: ConvertibleToIntCell = None) -> Cell[str | None]` *(abstract)* — Get a slice of the string.

`starts_with(self, prefix: ConvertibleToStringCell) -> Cell[bool | None]` *(abstract)* — Check if the string starts with the prefix.

`strip(self, *, characters: ConvertibleToStringCell = None) -> Cell[str | None]` *(abstract)* — Remove leading and trailing characters.

`strip_end(self, *, characters: ConvertibleToStringCell = None) -> Cell[str | None]` *(abstract)* — Remove trailing characters.

`strip_start(self, *, characters: ConvertibleToStringCell = None) -> Cell[str | None]` *(abstract)* — Remove leading characters.

`to_date(self, *, format: str | None = "iso") -> Cell[date | None]` *(abstract)* — Convert a string to a date.

`to_datetime(self, *, format: str | None = "iso") -> Cell[datetime | None]` *(abstract)* — Convert a string to a datetime.

`to_float(self) -> Cell[float | None]` *(abstract)* — Convert the string to a float.

`to_int(self, *, base: ConvertibleToIntCell = 10) -> Cell[int | None]` *(abstract)* — Convert the string to an integer.

`to_lowercase(self) -> Cell[str | None]` *(abstract)* — Convert the string to lowercase.

`to_time(self, *, format: str | None = "iso") -> Cell[time | None]` *(abstract)* — Convert a string to a time.

`to_uppercase(self) -> Cell[str | None]` *(abstract)* — Convert the string to uppercase.

## ExprStringOperations

Same methods as `StringOperations` (23 methods), returning `Cell` instead of `Cell[...]`. Signatures identical apart from return type.

---

## DatetimeOperations (ABC)

### Methods

`century(self) -> Cell[int | None]` *(abstract)* — Extract the century from a datetime or date.

`date(self) -> Cell[python_date | None]` *(abstract)* — Extract the date from a datetime.

`day(self) -> Cell[int | None]` *(abstract)* — Extract the day from a datetime or date.

`day_of_week(self) -> Cell[int | None]` *(abstract)* — Extract the day of the week from a datetime or date as defined by ISO 8601.

`day_of_year(self) -> Cell[int | None]` *(abstract)* — Extract the day of the year from a datetime or date.

`hour(self) -> Cell[int | None]` *(abstract)* — Extract the hour from a datetime or time.

`microsecond(self) -> Cell[int | None]` *(abstract)* — Extract the microsecond from a datetime or time.

`millennium(self) -> Cell[int | None]` *(abstract)* — Extract the millennium from a datetime or date.

`millisecond(self) -> Cell[int | None]` *(abstract)* — Extract the millisecond from a datetime or time.

`minute(self) -> Cell[int | None]` *(abstract)* — Extract the minute from a datetime or time.

`month(self) -> Cell[int | None]` *(abstract)* — Extract the month from a datetime or date.

`quarter(self) -> Cell[int | None]` *(abstract)* — Extract the quarter from a datetime or date.

`second(self) -> Cell[int | None]` *(abstract)* — Extract the second from a datetime or time.

`time(self) -> Cell[python_time | None]` *(abstract)* — Extract the time from a datetime.

`week(self) -> Cell[int | None]` *(abstract)* — Extract the ISO 8601 week number from a datetime or date.

`year(self) -> Cell[int | None]` *(abstract)* — Extract the year from a datetime or date.

`is_in_leap_year(self) -> Cell[bool | None]` *(abstract)* — Check a datetime or date is in a leap year.

`replace(self, *, year: ConvertibleToIntCell = None, month: ConvertibleToIntCell = None, day: ConvertibleToIntCell = None, hour: ConvertibleToIntCell = None, minute: ConvertibleToIntCell = None, second: ConvertibleToIntCell = None, microsecond: ConvertibleToIntCell = None) -> Cell` *(abstract)* — Replace components of a datetime or date.

`to_string(self, *, format: str = "iso") -> Cell[str | None]` *(abstract)* — Convert a datetime, date, or time to a string.

`unix_timestamp(self, *, unit: Literal["s", "ms", "us"] = "s") -> Cell[int | None]` *(abstract)* — Get the Unix timestamp from a datetime.

## ExprDatetimeOperations

Same methods as `DatetimeOperations` (20 methods), returning `Cell` instead of `Cell[...]`. Signatures identical apart from return type.

---

## DurationOperations (ABC)

### Methods

`abs(self) -> Cell[timedelta | None]` *(abstract)* — Get the absolute value of the duration.

`full_weeks(self) -> Cell[int | None]` *(abstract)* — Get the number of full weeks in the duration.

`full_days(self) -> Cell[int | None]` *(abstract)* — Get the number of full days in the duration.

`full_hours(self) -> Cell[int | None]` *(abstract)* — Get the number of full hours in the duration.

`full_minutes(self) -> Cell[int | None]` *(abstract)* — Get the number of full minutes in the duration.

`full_seconds(self) -> Cell[int | None]` *(abstract)* — Get the number of full seconds in the duration.

`full_milliseconds(self) -> Cell[int | None]` *(abstract)* — Get the number of full milliseconds in the duration.

`full_microseconds(self) -> Cell[int | None]` *(abstract)* — Get the number of full microseconds in the duration.

`to_string(self, *, format: Literal["iso", "pretty"] = "iso") -> Cell[str | None]` *(abstract)* — Convert the duration to a string.

## ExprDurationOperations

Same methods as `DurationOperations` (9 methods), returning `Cell` instead of `Cell[...]`. Signatures identical apart from return type.

---

## MathOperations (ABC)

### Methods

`abs(self) -> Cell` *(abstract)* — Get the absolute value.

`acos(self) -> Cell` *(abstract)* — Get the inverse cosine.

`acosh(self) -> Cell` *(abstract)* — Get the inverse hyperbolic cosine.

`asin(self) -> Cell` *(abstract)* — Get the inverse sine.

`asinh(self) -> Cell` *(abstract)* — Get the inverse hyperbolic sine.

`atan(self) -> Cell` *(abstract)* — Get the inverse tangent.

`atanh(self) -> Cell` *(abstract)* — Get the inverse hyperbolic tangent.

`cbrt(self) -> Cell` *(abstract)* — Get the cube root.

`ceil(self) -> Cell` *(abstract)* — Round up to the nearest integer.

`cos(self) -> Cell` *(abstract)* — Get the cosine.

`cosh(self) -> Cell` *(abstract)* — Get the hyperbolic cosine.

`degrees_to_radians(self) -> Cell` *(abstract)* — Convert degrees to radians.

`exp(self) -> Cell` *(abstract)* — Get the exponential.

`floor(self) -> Cell` *(abstract)* — Round down to the nearest integer.

`ln(self) -> Cell` *(abstract)* — Get the natural logarithm.

`log(self, base: float) -> Cell` *(abstract)* — Get the logarithm to the specified base.

`log10(self) -> Cell` *(abstract)* — Get the common logarithm (base 10).

`radians_to_degrees(self) -> Cell` *(abstract)* — Convert radians to degrees.

`round_to_decimal_places(self, decimal_places: int) -> Cell` *(abstract)* — Round to the specified number of decimal places.

`round_to_significant_figures(self, significant_figures: int) -> Cell` *(abstract)* — Round to the specified number of significant figures.

`sign(self) -> Cell` *(abstract)* — Get the sign (-1 if negative, 0 for zero, and 1 if positive).

`sin(self) -> Cell` *(abstract)* — Get the sine.

`sinh(self) -> Cell` *(abstract)* — Get the hyperbolic sine.

`sqrt(self) -> Cell` *(abstract)* — Get the square root.

`tan(self) -> Cell` *(abstract)* — Get the tangent.

`tanh(self) -> Cell` *(abstract)* — Get the hyperbolic tangent.

## ExprMathOperations

Same methods as `MathOperations` (26 methods). Signatures identical.

---

## ListOperations (ABC)

### Methods

`contains(self, item: ConvertibleToCell) -> Cell[bool | None]` *(abstract)* — Check if the list contains the given item.

`first(self) -> Cell` *(abstract)* — Get the first value of the list.

`get(self, index: ConvertibleToIntCell) -> Cell` *(abstract)* — Get the value at the specified index in the list.

`join(self, separator: ConvertibleToStringCell) -> Cell[str | None]` *(abstract)* — Join all elements in the list into a string, separated by the given separator.

`last(self) -> Cell` *(abstract)* — Get the last value of the list.

`length(self) -> Cell[int | None]` *(abstract)* — Get the number of elements in the list.

`max(self) -> Cell` *(abstract)* — Get the maximum value in the list.

`min(self) -> Cell` *(abstract)* — Get the minimum value in the list.

`reverse(self) -> Cell` *(abstract)* — Reverse the list.

`sort(self, *, descending: bool = False) -> Cell` *(abstract)* — Sort the list.

`sum(self) -> Cell` *(abstract)* — Sum all values in the list.

## ExprListOperations

Same methods as `ListOperations` (11 methods), returning `Cell` instead of `Cell[...]`. Signatures identical apart from return type.

---

## StructOperations (ABC)

### Methods

`get(self, name: str) -> Cell` *(abstract)* — Get the value of a struct field by name.

`rename(self, old_name: str, new_name: str) -> Cell` *(abstract)* — Rename a field of the struct.

`prefix_names(self, prefix: str) -> Cell` *(abstract)* — Add a prefix to all field names of the struct.

`suffix_names(self, suffix: str) -> Cell` *(abstract)* — Add a suffix to all field names of the struct.

`to_json(self) -> Cell[str | None]` *(abstract)* — Convert the struct to a JSON string.

## ExprStructOperations

Same methods as `StructOperations` (5 methods), returning `Cell` instead of `Cell[str | None]`. Signatures identical apart from return type.
