"""The module name must differ from the function name, so it can be re-exported properly."""

from __future__ import annotations

from typing import TYPE_CHECKING

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
        available = list(struct_type.fields.keys())
        msg = f'Struct has no field "{name}". Available fields: {available}'
        raise StructFieldNotFoundError(msg) from None
