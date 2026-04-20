from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from portabellas._validation import check_bounds

from ._string_operations import StringOperations

if TYPE_CHECKING:
    import polars as pl

    from portabellas.containers import Cell
    from portabellas.containers._cell import ConvertibleToIntCell, ConvertibleToStringCell


class ExprStringOperations(StringOperations):
    def __init__(self, expression: pl.Expr) -> None:
        self._expression: pl.Expr = expression

    def contains(self, substring: ConvertibleToStringCell) -> Cell:
        substring_expr = _to_string_expression(substring)

        return _expr_cell(self._expression.str.contains(substring_expr, literal=True))

    def ends_with(self, suffix: ConvertibleToStringCell) -> Cell:
        suffix_expr = _to_polars_expression(suffix)

        return _expr_cell(self._expression.str.ends_with(suffix_expr))

    def index_of(self, substring: ConvertibleToStringCell) -> Cell:
        substring_expr = _to_string_expression(substring)

        return _expr_cell(self._expression.str.find(substring_expr, literal=True))

    def length(self, *, optimize_for_ascii: bool = False) -> Cell:
        if optimize_for_ascii:
            return _expr_cell(self._expression.str.len_bytes())

        return _expr_cell(self._expression.str.len_chars())

    def pad_end(self, length: int, *, character: str = " ") -> Cell:
        check_bounds("length", length, lower_bound=0, lower_bound_mode="closed")
        if len(character) != 1:
            msg = "Can only pad with a single character."
            raise ValueError(msg)

        return _expr_cell(self._expression.str.pad_end(length, character))

    def pad_start(self, length: int, *, character: str = " ") -> Cell:
        check_bounds("length", length, lower_bound=0, lower_bound_mode="closed")
        if len(character) != 1:
            msg = "Can only pad with a single character."
            raise ValueError(msg)

        return _expr_cell(self._expression.str.pad_start(length, character))

    def repeat(self, count: ConvertibleToIntCell) -> Cell:
        if isinstance(count, int):
            check_bounds("count", count, lower_bound=0, lower_bound_mode="closed")

        count_expr = _to_polars_expression(count)

        return _expr_cell(self._expression.repeat_by(count_expr).list.join("", ignore_nulls=False))

    def remove_prefix(self, prefix: ConvertibleToStringCell) -> Cell:
        prefix_expr = _to_string_expression(prefix)

        return _expr_cell(self._expression.str.strip_prefix(prefix_expr))

    def remove_suffix(self, suffix: ConvertibleToStringCell) -> Cell:
        suffix_expr = _to_string_expression(suffix)

        return _expr_cell(self._expression.str.strip_suffix(suffix_expr))

    def replace_all(self, old: ConvertibleToStringCell, new: ConvertibleToStringCell) -> Cell:
        old_expr = _to_string_expression(old)
        new_expr = _to_string_expression(new)

        return _expr_cell(self._expression.str.replace_all(old_expr, new_expr, literal=True))

    def reverse(self) -> Cell:
        return _expr_cell(self._expression.str.reverse())

    def slice(
        self,
        *,
        start: ConvertibleToIntCell = 0,
        length: ConvertibleToIntCell = None,
    ) -> Cell:
        if isinstance(length, int):
            check_bounds("length", length, lower_bound=0, lower_bound_mode="closed")

        start_expr = _to_polars_expression(start)
        length_expr = _to_polars_expression(length)

        return _expr_cell(self._expression.str.slice(start_expr, length_expr))

    def starts_with(self, prefix: ConvertibleToStringCell) -> Cell:
        prefix_expr = _to_polars_expression(prefix)

        return _expr_cell(self._expression.str.starts_with(prefix_expr))

    def strip(self, *, characters: ConvertibleToStringCell = None) -> Cell:
        characters_expr = _to_polars_expression(characters)

        return _expr_cell(self._expression.str.strip_chars(characters_expr))

    def strip_end(self, *, characters: ConvertibleToStringCell = None) -> Cell:
        characters_expr = _to_polars_expression(characters)

        return _expr_cell(self._expression.str.strip_chars_end(characters_expr))

    def strip_start(self, *, characters: ConvertibleToStringCell = None) -> Cell:
        characters_expr = _to_polars_expression(characters)

        return _expr_cell(self._expression.str.strip_chars_start(characters_expr))

    def to_date(self, *, format: str | None = "iso") -> Cell:  # noqa: A002
        if format == "iso":
            polars_format = "%F"
        elif format is not None:
            polars_format = _convert_and_check_datetime_format(format, type_="date", used_for_parsing=True)
        else:
            polars_format = None

        return _expr_cell(self._expression.str.to_date(format=polars_format, strict=False))

    def to_datetime(self, *, format: str | None = "iso") -> Cell:  # noqa: A002
        if format == "iso":
            polars_format = "%+"
        elif format is not None:
            polars_format = _convert_and_check_datetime_format(format, type_="datetime", used_for_parsing=True)
        else:
            polars_format = None

        return _expr_cell(self._expression.str.to_datetime(format=polars_format, strict=False))

    def to_float(self) -> Cell:
        import polars as pl

        return _expr_cell(self._expression.cast(pl.Float64, strict=False))

    def to_int(self, *, base: ConvertibleToIntCell = 10) -> Cell:
        base_expr = _to_polars_expression(base)

        return _expr_cell(self._expression.str.to_integer(base=base_expr, strict=False))

    def to_lowercase(self) -> Cell:
        return _expr_cell(self._expression.str.to_lowercase())

    def to_time(self, *, format: str | None = "iso") -> Cell:  # noqa: A002
        if format == "iso":
            polars_format = "%T%.f"
        elif format is not None:
            polars_format = _convert_and_check_datetime_format(format, type_="time", used_for_parsing=True)
        else:
            polars_format = None

        return _expr_cell(self._expression.str.to_time(format=polars_format, strict=False))

    def to_uppercase(self) -> Cell:
        return _expr_cell(self._expression.str.to_uppercase())


def _expr_cell(expression: pl.Expr) -> Cell:
    from portabellas.containers._cell._expr_cell import ExprCell  # circular import

    return ExprCell(expression)


def _to_polars_expression(cell_proxy: object) -> pl.Expr:
    from portabellas.containers._cell._cell import _to_polars_expression as _base_to_polars_expression

    return _base_to_polars_expression(cell_proxy)


def _to_string_expression(value: ConvertibleToStringCell) -> pl.Expr:
    import polars as pl

    from portabellas.containers._cell import Cell

    if isinstance(value, Cell):
        return value._polars_expression

    if value is None:
        return pl.lit(value, dtype=pl.Utf8)

    return pl.lit(value)


_DATE_REPLACEMENTS: dict[str, str] = {
    "Y": "Y",
    "_Y": "_Y",
    "^Y": "-Y",
    "Y99": "y",
    "_Y99": "_y",
    "^Y99": "-y",
    "M": "m",
    "_M": "_m",
    "^M": "-m",
    "M-full": "B",
    "M-short": "b",
    "W": "V",
    "_W": "_V",
    "^W": "-V",
    "D": "d",
    "_D": "_d",
    "^D": "-d",
    "DOW": "u",
    "DOW-full": "A",
    "DOW-short": "a",
    "DOY": "j",
    "_DOY": "_j",
    "^DOY": "-j",
}

_TIME_REPLACEMENTS: dict[str, str] = {
    "h": "H",
    "_h": "_H",
    "^h": "-H",
    "h12": "I",
    "_h12": "_I",
    "^h12": "-I",
    "m": "M",
    "_m": "_M",
    "^m": "-M",
    "s": "S",
    "_s": "_S",
    "^s": "-S",
    ".f": ".f",
    "ms": "3f",
    "us": "6f",
    "ns": "9f",
    "AM/PM": "p",
    "am/pm": "P",
}

_DATETIME_REPLACEMENTS: dict[str, str] = {
    **_DATE_REPLACEMENTS,
    **_TIME_REPLACEMENTS,
    "z": "z",
    ":z": ":z",
    "u": "s",
}

_DATETIME_REPLACEMENTS_WHEN_PARSING: dict[str, str] = {
    **_DATETIME_REPLACEMENTS,
    "z": "#z",
    ":z": "#z",
}


def _convert_and_check_datetime_format(
    format_: str,
    *,
    type_: Literal["datetime", "date", "time"],
    used_for_parsing: bool,
) -> str:
    replacements = _get_replacements(type_, used_for_parsing=used_for_parsing)
    converted_format = ""
    index = 0

    while index < len(format_):
        char = format_[index]

        if char == "\\" and _char_at(format_, index + 1) == "\\":
            converted_format += "\\"
            index += 2
        elif char == "\\" and _char_at(format_, index + 1) == "{":
            converted_format += "{"
            index += 2
        elif char == "\n":
            converted_format += "%n"
            index += 1
        elif char == "\t":
            converted_format += "%t"
            index += 1
        elif char == "%":
            converted_format += "%%"
            index += 1
        elif char == "{":
            end_index = format_.find("}", index)
            if end_index == -1:
                msg = f"Unclosed specifier at index {index}."
                raise ValueError(msg)

            expression = format_[index + 1 : end_index]
            converted_format += _convert_and_check_template_expression(expression, type_, replacements)
            index = end_index + 1
        else:
            converted_format += char
            index += 1

    return converted_format


def _get_replacements(
    type_: Literal["datetime", "date", "time"],
    *,
    used_for_parsing: bool,
) -> dict[str, str]:
    if type_ == "datetime":
        return _DATETIME_REPLACEMENTS_WHEN_PARSING if used_for_parsing else _DATETIME_REPLACEMENTS
    if type_ == "date":
        return _DATE_REPLACEMENTS
    return _TIME_REPLACEMENTS


def _char_at(string: str, i: int) -> str | None:
    if i >= len(string):
        return None
    return string[i]


def _convert_and_check_template_expression(
    expression: str,
    type_: str,
    replacements: dict[str, str],
) -> str:
    if expression in replacements:
        return "%" + replacements[expression]

    from portabellas._utils import get_similar_strings

    similar = get_similar_strings(expression, replacements.keys())
    msg = f"Invalid specifier '{expression}' for type {type_}."
    if similar:
        msg += f" Did you mean one of {similar}?"
    raise ValueError(msg)
