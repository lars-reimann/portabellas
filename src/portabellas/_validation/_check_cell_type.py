from __future__ import annotations

from typing import TYPE_CHECKING

from portabellas.exceptions import ColumnTypeError

if TYPE_CHECKING:
    from collections.abc import Callable

    from portabellas.typing import DataType


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


def check_cell_type(cell_type: DataType, *, required: CellTypeRequirement) -> None:
    """
    Check whether a cell's type satisfies a requirement, and raise an error if it does not.

    Parameters
    ----------
    cell_type:
        The type of the cell to check.
    required:
        The requirement that the cell's type must satisfy.

    Raises
    ------
    ColumnTypeError
        If the cell's type does not satisfy the requirement.

    Notes
    -----
    If the cell's type is `DataTypes.Unknown`, validation is skipped entirely (no error is raised).
    This prevents false positives when the type has not yet been inferred.
    """
    from portabellas.typing import DataTypes  # circular import  # noqa: PLC0415

    if isinstance(cell_type, DataTypes.Unknown):
        return
    if not required(cell_type):
        msg = f"Expected {required.description} type, got {cell_type}"
        raise ColumnTypeError(msg)
