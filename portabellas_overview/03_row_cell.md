# Row & Cell

Sources:
- `src/portabellas/containers/_row/_row.py` (Row ABC)
- `src/portabellas/containers/_row/_expr_row.py` (ExprRow)
- `src/portabellas/containers/_cell/_cell.py` (Cell ABC)
- `src/portabellas/containers/_cell/_expr_cell.py` (ExprCell)

---

## Row (Abstract Base Class)

### Dunder Methods

`__contains__(self, key: object, /) -> bool` — Delegates to `has_column`.

`__getitem__(self, name: str) -> Cell` — Delegates to `get_cell`.

`__iter__(self) -> Iterator[str]` — Delegates to `column_names`.

`__len__(self) -> int` — Delegates to `column_count`.

### Properties

`column_count -> int` *(abstract)* — The number of columns.

`column_names -> list[str]` *(abstract)* — The names of the columns.

`schema -> Schema` *(abstract)* — The schema of the row, which is a mapping from column names to their types.

### Methods

`get_cell(self, name: str) -> Cell` *(abstract)* — Get the cell in the specified column.

`get_column_type(self, name: str) -> DataType` *(abstract)* — Get the type of a column.

`has_column(self, name: str) -> bool` *(abstract)* — Check if the row has a column with a specific name.

---

## ExprRow

### Constructor

`__init__(self, table: Table) -> None`

### Properties

`column_count -> int` — Delegates to `self._table.column_count`.

`column_names -> list[str]` — Delegates to `self._table.column_names`.

`schema -> Schema` — Delegates to `self._table.schema`.

### Methods

`get_cell(self, name: str) -> ExprCell`

`get_column_type(self, name: str) -> DataType`

`has_column(self, name: str) -> bool`

---

## Cell (Abstract Base Class)

### Static Methods

`constant(value: object, *, type: DataType | None = None) -> Cell` — Create a cell with a constant value.

`date(year: ConvertibleToIntCell, month: ConvertibleToIntCell, day: ConvertibleToIntCell) -> Cell[date | None]` — Create a cell with a date.

`datetime(year: ConvertibleToIntCell, month: ConvertibleToIntCell, day: ConvertibleToIntCell, hour: ConvertibleToIntCell, minute: ConvertibleToIntCell, second: ConvertibleToIntCell, *, microsecond: ConvertibleToIntCell = 0, time_zone: str | None = None) -> Cell[datetime | None]` — Create a cell with a datetime.

`duration(*, weeks: ConvertibleToIntCell = 0, days: ConvertibleToIntCell = 0, hours: ConvertibleToIntCell = 0, minutes: ConvertibleToIntCell = 0, seconds: ConvertibleToIntCell = 0, milliseconds: ConvertibleToIntCell = 0, microseconds: ConvertibleToIntCell = 0) -> Cell[timedelta | None]` — Create a cell with a duration.

`time(hour: ConvertibleToIntCell, minute: ConvertibleToIntCell, second: ConvertibleToIntCell, *, microsecond: ConvertibleToIntCell = 0) -> Cell[time | None]` — Create a cell with a time.

`first_not_none(cells: list[Cell[P]]) -> Cell[P | None]` — Return the first cell that is not None or None if all cells are None.

### Properties

`dt -> DatetimeOperations` *(abstract)* — Namespace for operations on datetime/date/time values.

`dur -> DurationOperations` *(abstract)* — Namespace for operations on durations.

`list -> ListOperations` *(abstract)* — Namespace for operations on lists.

`math -> MathOperations` *(abstract)* — Namespace for mathematical operations.

`str -> StringOperations` *(abstract)* — Namespace for operations on strings.

`struct -> StructOperations` *(abstract)* — Namespace for operations on structs.

### Boolean Operators (Dunder)

`__invert__(self) -> Cell[bool | None]` *(abstract)*

`__and__(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]` *(abstract)*

`__rand__(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]` *(abstract)*

`__or__(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]` *(abstract)*

`__ror__(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]` *(abstract)*

`__xor__(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]` *(abstract)*

`__rxor__(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]` *(abstract)*

### Comparison Operators (Dunder)

`__eq__(self, other: object) -> Cell[bool | None]` *(abstract)*

`__ne__(self, other: object) -> Cell[bool | None]` *(abstract)*

`__ge__(self, other: object) -> Cell[bool | None]` *(abstract)*

`__gt__(self, other: object) -> Cell[bool | None]` *(abstract)*

`__le__(self, other: object) -> Cell[bool | None]` *(abstract)*

`__lt__(self, other: object) -> Cell[bool | None]` *(abstract)*

### Arithmetic Operators (Dunder)

`__abs__(self) -> Cell` *(abstract)*

`__ceil__(self) -> Cell` *(abstract)*

`__floor__(self) -> Cell` *(abstract)*

`__neg__(self) -> Cell` *(abstract)*

`__pos__(self) -> Cell` *(abstract)*

`__add__(self, other: ConvertibleToCell) -> Cell` *(abstract)*

`__radd__(self, other: ConvertibleToCell) -> Cell` *(abstract)*

`__floordiv__(self, other: ConvertibleToCell) -> Cell` *(abstract)*

`__rfloordiv__(self, other: ConvertibleToCell) -> Cell` *(abstract)*

`__mod__(self, other: ConvertibleToCell) -> Cell` *(abstract)*

`__rmod__(self, other: ConvertibleToCell) -> Cell` *(abstract)*

`__mul__(self, other: ConvertibleToCell) -> Cell` *(abstract)*

`__rmul__(self, other: ConvertibleToCell) -> Cell` *(abstract)*

`__pow__(self, other: ConvertibleToCell) -> Cell` *(abstract)*

`__rpow__(self, other: ConvertibleToCell) -> Cell` *(abstract)*

`__sub__(self, other: ConvertibleToCell) -> Cell` *(abstract)*

`__rsub__(self, other: ConvertibleToCell) -> Cell` *(abstract)*

`__truediv__(self, other: ConvertibleToCell) -> Cell` *(abstract)*

`__rtruediv__(self, other: ConvertibleToCell) -> Cell` *(abstract)*

### Other Dunder

`__hash__ = None` — Disables hashing since `__eq__` does not follow the standard contract.

`__repr__(self) -> str` *(abstract)*

`__str__(self) -> str` *(abstract)*

### Boolean Methods

`not_(self) -> Cell[bool | None]` — Negate a Boolean.

`and_(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]` — Perform a Boolean AND operation.

`or_(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]` — Perform a Boolean OR operation.

`xor(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]` — Perform a Boolean XOR operation.

### Arithmetic Methods

`neg(self) -> Cell` — Negate the value.

`add(self, other: ConvertibleToCell) -> Cell` — Add a value.

`div(self, other: ConvertibleToCell) -> Cell` — Divide by a value.

`mod(self, other: ConvertibleToCell) -> Cell` — Perform a modulo operation.

`mul(self, other: ConvertibleToCell) -> Cell` — Multiply by a value.

`pow(self, other: ConvertibleToCell) -> Cell` — Raise to a power.

`sub(self, other: ConvertibleToCell) -> Cell` — Subtract a value.

### Comparison Methods

`eq(self, other: object, *, propagate_missing_values: bool = True) -> Cell[bool | None]` *(abstract)* — Check if equal to a value.

`neq(self, other: object, *, propagate_missing_values: bool = True) -> Cell[bool | None]` *(abstract)* — Check if not equal to a value.

`ge(self, other: object) -> Cell[bool | None]` — Check if greater than or equal to a value.

`gt(self, other: object) -> Cell[bool | None]` — Check if greater than a value.

`le(self, other: object) -> Cell[bool | None]` — Check if less than or equal to a value.

`lt(self, other: object) -> Cell[bool | None]` — Check if less than a value.

### Type Conversion

`cast(self, type: DataType) -> Cell` *(abstract)* — Cast the cell to a different type.

---

## ExprCell

### Constructor

`__init__(self, expression: pl.Expr) -> None`

### Properties

`dt -> DatetimeOperations` — Returns `ExprDatetimeOperations`.

`dur -> DurationOperations` — Returns `ExprDurationOperations`.

`list -> ListOperations` — Returns `ExprListOperations`.

`math -> MathOperations` — Returns `ExprMathOperations`.

`str -> StringOperations` — Returns `ExprStringOperations`.

`struct -> StructOperations` — Returns `ExprStructOperations`.

### Methods

`eq(self, other: object, *, propagate_missing_values: bool = True) -> Cell[bool | None]`

`neq(self, other: object, *, propagate_missing_values: bool = True) -> Cell[bool | None]`

`cast(self, type: DataType) -> Cell`

### Dunder Methods

All operator dunders from `Cell` ABC are implemented (boolean, comparison, arithmetic). See the Cell ABC section above for full signatures.

`__hash__ = None`

`__repr__(self) -> str`

`__str__(self) -> str`
