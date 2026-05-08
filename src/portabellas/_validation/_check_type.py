from __future__ import annotations

from typing import TYPE_CHECKING

from portabellas.exceptions import ColumnTypeError
from portabellas.typing import DataType, DataTypes
from portabellas.typing._infer_type_from_literal import infer_type_from_literal

if TYPE_CHECKING:
    from collections.abc import Callable


class CellTypeRequirement:
    def __init__(self, description: str, check: Callable[[DataType], bool]) -> None:
        self.description = description
        self.check = check

    def __call__(self, cell_type: DataType) -> bool:
        return self.check(cell_type)


class InstanceOf(CellTypeRequirement):
    def __init__(self, *types: type) -> None:
        self._types = types
        if len(types) == 1:
            description = types[0].__name__
        elif len(types) == 2:
            description = f"{types[0].__name__} or {types[1].__name__}"
        else:
            description = ", ".join(t.__name__ for t in types[:-1]) + ", or " + types[-1].__name__
        super().__init__(description, lambda dt: isinstance(dt, types))


def check_type(value: object, required: CellTypeRequirement) -> None:
    """
    Check whether a value's type satisfies a requirement, and raise an error if it does not.

    Parameters
    ----------
    value:
        The value to check. Can be a `DataType`, a `Cell`, or a Python literal.
    required:
        The requirement that the type must satisfy.

    Raises
    ------
    ColumnTypeError
        If the type does not satisfy the requirement.

    Notes
    -----
    If the type is `DataTypes.Unknown` or `DataTypes.Null`, validation is skipped entirely
    (no error is raised). This prevents false positives when the type has not yet been
    inferred (Unknown) or when the actual type is indeterminate (Null adapts to any type
    at runtime).
    """
    from portabellas.containers import Cell  # circular import  # noqa: PLC0415

    if isinstance(value, DataType):
        data_type = value
    elif isinstance(value, Cell):
        data_type = value._type
    else:
        data_type = infer_type_from_literal(value)

    if isinstance(data_type, (DataTypes.Unknown, DataTypes.Null)):
        return  # Null adapts to any type at runtime, so validation cannot be precise
    elif not required(data_type):
        msg = f"Expected {required.description} type, got {data_type}"
        raise ColumnTypeError(msg)
