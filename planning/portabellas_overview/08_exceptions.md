# Exceptions

Source: `src/portabellas/exceptions/__init__.py`

All exceptions inherit from `PortabellasError`.

---

## Exception Hierarchy

`PortabellasError` — Base class for all exceptions defined by portabellas.

`ColumnNotFoundError(PortabellasError, KeyError)` — Raised when a column is not found.

`ColumnTypeError(PortabellasError, TypeError)` — Raised when a column does not have the expected type.

`DuplicateColumnError(PortabellasError, ValueError)` — Raised when a column name already exists.

`FileExtensionError(PortabellasError, ValueError)` — Raised when a path has the wrong file extension.

`IndexOutOfBoundsError(PortabellasError, IndexError)` — Raised when trying to access an invalid index.

`LazyComputationError(PortabellasError, RuntimeError)` — Raised when a lazy computation fails.

`LengthMismatchError(PortabellasError, ValueError)` — Raised when objects have different lengths.

`MissingValuesColumnError(PortabellasError, ValueError)` — Raised when trying to do an operation on a column containing missing values.

`OutOfBoundsError(PortabellasError, ValueError)` — Raised when a value is outside its expected range.

`SchemaError(PortabellasError, ValueError)` — Raised when a schema does not match the expected schema.
