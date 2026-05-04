# Data Types

## DataType Hierarchy

All data types inherit from `DataType`. The hierarchy includes several abstract base classes:

- `DataType` (base)
  - `NumericType` (abstract)
    - `IntegerType` (abstract)
    - `FloatType` (abstract, used internally)
  - `TemporalType` (abstract)
  - `NestedType` (abstract)

## Concrete Types

### Integer Types

| Type | Description |
|------|-------------|
| `Int8` | 8-bit signed integer |
| `Int16` | 16-bit signed integer |
| `Int32` | 32-bit signed integer |
| `Int64` | 64-bit signed integer |
| `Int128` | 128-bit signed integer |
| `UInt8` | 8-bit unsigned integer |
| `UInt16` | 16-bit unsigned integer |
| `UInt32` | 32-bit unsigned integer |
| `UInt64` | 64-bit unsigned integer |
| `UInt128` | 128-bit unsigned integer |

### Float Types

| Type | Description |
|------|-------------|
| `Float16` | 16-bit floating point (half precision) |
| `Float32` | 32-bit floating point (single precision) |
| `Float64` | 64-bit floating point (double precision) |

### Other Primitive Types

| Type | Description |
|------|-------------|
| `Boolean` | Boolean type |
| `String` | UTF-8 encoded string type |
| `Binary` | Binary byte array type |
| `Null` | Null type |
| `Unknown` | Unknown type |

### Temporal Types

| Type | Description |
|------|-------------|
| `Date` | Calendar date type (days since epoch) |
| `Time` | Time of day type |

### Decimal Type

#### `Decimal(precision: int | None = None, scale: int = 0)`

Decimal type with optional precision and scale parameters.

- `precision`: Number of significant digits (None = infinite precision)
- `scale`: Number of digits after the decimal point

### Parameterized Temporal Types

#### `Datetime(time_unit: TimeUnit | None = None, time_zone: str | None = None)`

Datetime type with optional time unit and time zone.

- `time_unit`: One of `"ms"`, `"us"`, `"ns"` (default: `"us"`)
- `time_zone`: Time zone string (e.g., `"America/New_York"`), or `None` for naive

#### `Duration(time_unit: TimeUnit | None = None)`

Duration type with optional time unit.

- `time_unit`: One of `"ms"`, `"us"`, `"ns"` (default: `"us"`)

### Categorical Types

#### `Categorical(ordering: CategoricalOrdering = "physical")`

Categorical type with optional ordering strategy.

- `ordering`: `"physical"` (default) or `"lexical"`

#### `Enum(categories: Sequence[str] | None = None)`

Enum type with a fixed set of string categories.

- `categories`: Sequence of allowed string values

### Nested Types

#### `List(inner: PolarsDataType | None = None)`

List type with an optional inner element type.

- `inner`: The data type of elements in the list

#### `Array(inner: PolarsDataType | None = None, width: int | None = None)`

Fixed-size array type with inner type and width.

- `inner`: The data type of elements in the array
- `width`: The fixed size of the array

#### `Struct(fields: Sequence[Field | PolarsDataType] | None = None)`

Struct type with named fields.

- `fields`: Sequence of `Field` objects or data types

#### `Field(name: str, dtype: PolarsDataType)`

Named field within a Struct.

- `name`: Field name
- `dtype`: Field data type

### Extension Types

#### `BaseExtension(name: str)`

Base class for extension types.

- `name`: The name of the extension type

#### `Extension(name: str, storage_type: PolarsDataType | None = None)`

Concrete extension type with optional storage type.

- `name`: The name of the extension type
- `storage_type`: The underlying storage data type

### Object Type

| Type | Description |
|------|-------------|
| `Object` | Python object type (cannot be serialized) |

### Categories Helper

#### `Categories(categories: Series | Sequence[str])`

Helper for constructing categorical/enum categories.

- `categories`: A Series or sequence of strings

## DataTypeExpr

### `DataTypeExpr`

An expression that resolves to a DataType at execution time. Used in contexts where the data type depends on the schema (e.g., `cast(pl.datatype_expr())`).

## Extension Type Functions

### `register_extension_type(dtype: type[DataType], *, namespace: str = "") -> None`

Register a custom extension type so Polars can (de)serialize it.

### `unregister_extension_type(name: str) -> None`

Unregister a previously registered extension type.

### `get_index_type(wo_integer: bool = False) -> PolarsDataType`

Get the index data type used by Polars.

## Type Aliases

| Alias | Type |
|-------|------|
| `PolarsDataType` | `DataType | type[DataType]` |
| `PolarsTemporalType` | `TemporalType | type[TemporalType]` |
| `PolarsIntegerType` | `IntegerType | type[IntegerType]` |
| `PolarsNumericType` | `NumericType | type[NumericType]` |
| `PolarsNestedType` | `NestedType | type[NestedType]` |
