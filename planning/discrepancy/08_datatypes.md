# DataType Discrepancies

## Polars has, Portabellas doesn't

| Polars Type | Notes |
|---|---|
| `Int128` / `UInt128` | 128-bit integers (Portabellas has `experimental_Int128`) |
| `Float16` | Half-precision float |
| `Categorical(ordering)` | Categorical with ordering strategy |
| `Enum(categories)` | Fixed-set enum type |
| `Decimal(precision, scale)` | Decimal with precision/scale |
| `Array(inner, width)` | Fixed-size array type |
| `Object` | Python object type |
| `Unknown` | Unknown type |
| `BaseExtension` / `Extension` | Extension type base classes |
| `Categories` | Categorical/enum categories helper |
| `DataTypeExpr` | Expression that resolves to DataType |
| `Field(name, dtype)` | Named field in struct (Portabellas uses `dict[str, DataType]` for struct fields) |
| `register_extension_type(dtype, *, namespace)` | Register custom extension type |
| `unregister_extension_type(name)` | Unregister extension type |
| `get_index_type(wo_integer)` | Get index data type |
| Type aliases: `PolarsDataType`, `PolarsTemporalType`, `PolarsIntegerType`, `PolarsNumericType`, `PolarsNestedType` | Type aliases |

---

## Portabellas has, Polars doesn't

| Portabellas (`DataType`) | Notes |
|---|---|
| Factory methods on `DataType` class (`DataType.Int8()`, `DataType.String()`, etc.) | Polars types are classes themselves (`pl.Int8`, `pl.String`), not factory methods |
| `DataType.is_float` / `is_int` / `is_numeric` / `is_signed_int` / `is_unsigned_int` / `is_temporal` / `is_list` / `is_struct` | Boolean properties for type introspection (Polars types have similar but scattered: `is_numeric()`, `is_integer()`, `is_float()`, `is_temporal()`, `is_nested()`) |
| `Schema` as `Mapping[str, DataType]` with `column_count`, `column_names`, `get_column_type`, `has_column`, `to_dict` | Polars `Schema` inherits from `OrderedDict` with `from_dict`, `from_names_and_dtypes`, `to_python`, `len`, `names`, `dtypes`, `equals` |

---

## Both have but with different APIs

| Feature | Portabellas | Polars | Difference |
|---|---|---|---|
| Int types | `DataType.Int8/Int16/Int32/Int64()` | `pl.Int8/Int16/Int32/Int64` | Factory methods vs classes |
| UInt types | `DataType.UInt8/UInt16/UInt32/UInt64()` | `pl.UInt8/UInt16/UInt32/UInt64` | Same |
| Float types | `DataType.Float32/Float64()` | `pl.Float32/Float64` | Same (Polars also has Float16) |
| String | `DataType.String()` | `pl.String` | Factory vs class |
| Boolean | `DataType.Boolean()` | `pl.Boolean` | Same |
| Binary | `DataType.Binary()` | `pl.Binary` | Same |
| Null | `DataType.Null()` | `pl.Null` | Same |
| Date | `DataType.Date()` | `pl.Date` | Same |
| Time | `DataType.Time()` | `pl.Time` | Same |
| Datetime | `DataType.Datetime(*, time_zone)` | `pl.Datetime(time_unit, time_zone)` | Polars has time_unit param |
| Duration | `DataType.Duration(time_unit)` | `pl.Duration(time_unit)` | Same |
| List | `DataType.List(inner)` | `pl.List(inner)` | Same |
| Struct | `DataType.Struct(fields: dict[str, DataType])` | `pl.Struct(fields: Sequence[Field \| DataType])` | Dict vs Sequence of Field |
| Schema constructor | `Schema(schema: Mapping[str, DataType])` | `Schema()` / `Schema(mapping)` | Polars Schema is OrderedDict-based |
