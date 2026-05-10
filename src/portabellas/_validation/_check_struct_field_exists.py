"""The module name must differ from the function name, so it can be re-exported properly."""

from __future__ import annotations

from typing import TYPE_CHECKING

from portabellas._utils import get_similar_strings
from portabellas.exceptions import StructFieldNotFoundError

if TYPE_CHECKING:
    from portabellas.typing import DataTypes


def check_struct_field_exists(name: str, struct_type: DataTypes.Struct) -> None:
    """
    Check whether the specified field exists in a struct type, and raise an error if it does not.

    Parameters
    ----------
    name:
        The field name to check.
    struct_type:
        The struct type whose fields are checked.

    Raises
    ------
    StructFieldNotFoundError
        If the field name does not exist in the struct.
    """
    if name not in struct_type.fields:
        sorted_fields = _sort_fields_by_similarity(name, struct_type)
        msg = _build_error_message(name, sorted_fields)
        raise StructFieldNotFoundError(msg) from None


def _sort_fields_by_similarity(name: str, struct_type: DataTypes.Struct) -> list[str]:
    similar = get_similar_strings(name, struct_type.fields.keys())
    remaining = [field for field in struct_type.fields if field not in similar]
    return similar + remaining


def _build_error_message(name: str, sorted_fields: list[str]) -> str:
    result = f'Struct has no field "{name}". Available fields:\n'
    for field in sorted_fields:
        result += f'    - "{field}"\n'
    return result.rstrip("\n")
