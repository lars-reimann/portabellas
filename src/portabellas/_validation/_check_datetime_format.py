from __future__ import annotations

from typing import Literal

from portabellas._utils import get_similar_strings

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


def check_and_convert_datetime_format(
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
            converted_format += _check_and_convert_template_expression(expression, type_, replacements)
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


def _check_and_convert_template_expression(
    expression: str,
    type_: str,
    replacements: dict[str, str],
) -> str:
    if expression in replacements:
        return "%" + replacements[expression]

    similar = get_similar_strings(expression, replacements.keys())
    msg = f"Invalid specifier '{expression}' for type {type_}."
    if similar:
        msg += f" Did you mean one of {similar}?"
    raise ValueError(msg)
