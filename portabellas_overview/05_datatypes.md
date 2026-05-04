# DataType & Schema

Sources:
- `src/portabellas/typing/_data_type.py` — `DataType` (ABC)
- `src/portabellas/typing/_polars_data_type.py` — `PolarsDataType` (internal)
- `src/portabellas/typing/_schema.py` — `Schema`

Public exports: `DataType`, `Schema` (from `portabellas.typing`)

---

## DataType

### Static Factory Methods

`Float32() -> DataType` — Create a `Float32` type (32-bit floating point number).

`Float64() -> DataType` — Create a `Float64` type (64-bit floating point number).

`Int8() -> DataType` — Create an `Int8` type (8-bit signed integer).

`Int16() -> DataType` — Create an `Int16` type (16-bit signed integer).

`Int32() -> DataType` — Create an `Int32` type (32-bit signed integer).

`Int64() -> DataType` — Create an `Int64` type (64-bit signed integer).

`experimental_Int128() -> DataType` — Create an `Int128` type (128-bit signed integer).

`UInt8() -> DataType` — Create a `UInt8` type (8-bit unsigned integer).

`UInt16() -> DataType` — Create a `UInt16` type (16-bit unsigned integer).

`UInt32() -> DataType` — Create a `UInt32` type (32-bit unsigned integer).

`UInt64() -> DataType` — Create a `UInt64` type (64-bit unsigned integer).

`Date() -> DataType` — Create a `Date` type, which represents a calendar date.

`Datetime(*, time_zone: str | None = None) -> DataType` — Create a `Datetime` type, which combines a calendar date and a time of day.

`Duration(time_unit: Literal["ms", "us", "ns"]) -> DataType` — Create a `Duration` type.

`Time() -> DataType` — Create a `Time` type, which represents a time of day.

`String() -> DataType` — Create a `String` type.

`List(inner: DataType) -> DataType` — Create a `List` type with the specified inner type.

`Struct(fields: dict[str, DataType]) -> DataType` — Create a `Struct` type, which represents a collection of named fields.

`Binary() -> DataType` — Create a `Binary` type.

`Boolean() -> DataType` — Create a `Boolean` type.

`Null() -> DataType` — Create a `Null` type.

### Dunder Methods

`__eq__(self, other: object) -> bool` *(abstract)*

`__hash__(self) -> int` *(abstract)*

`__repr__(self) -> str` *(abstract)*

`__str__(self) -> str` *(abstract)*

### Properties

`is_float -> bool` — Whether this is a floating point type.

`is_int -> bool` — Whether this is an integer type (signed or unsigned).

`is_numeric -> bool` — Whether this is a numeric type.

`is_signed_int -> bool` — Whether this is a signed integer type.

`is_temporal -> bool` — Whether this is a temporal type.

`is_unsigned_int -> bool` — Whether this is an unsigned integer type.

`is_list -> bool` — Whether this is a list type.

`is_struct -> bool` — Whether this is a struct type.

---

## PolarsDataType (Internal)

Not re-exported. Wraps a `pl.DataType` to implement the `DataType` ABC.

### Constructor

`__init__(self, dtype: pl.DataType) -> None`

### Properties

Same as `DataType` (`is_float`, `is_int`, `is_numeric`, `is_signed_int`, `is_temporal`, `is_unsigned_int`, `is_list`, `is_struct`).

---

## Schema

Inherits from `Mapping[str, DataType]`.

### Constructor

`__init__(self, schema: Mapping[str, DataType]) -> None`

### Dunder Methods

`__contains__(self, key: object, /) -> bool`

`__eq__(self, other: object) -> bool`

`__getitem__(self, key: str, /) -> DataType`

`__hash__(self) -> int`

`__iter__(self) -> Iterator[str]`

`__len__(self) -> int`

`__repr__(self) -> str`

`__str__(self) -> str`

### Properties

`column_count -> int` — The number of columns.

`column_names -> list[str]` — The names of the columns.

### Methods

`get_column_type(self, name: str) -> DataType` — Get the type of a column.

`has_column(self, name: str) -> bool` — Check if the schema has a column with a specific name.

`to_dict(self) -> dict[str, DataType]` — Return a dictionary that maps column names to column types.
