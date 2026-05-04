# Table

Source: `src/portabellas/containers/_table.py`

## Constructor

`__init__(self, data: Mapping[str, Sequence[object]]) -> None` — A two-dimensional collection of data.

## Class Attributes

`read: TableReader` — Create a new table by reading from various sources.

## Static Methods

`from_columns(columns: Column | list[Column]) -> Table` — Create a table from columns.

`from_dict(data: dict[str, list[object]]) -> Table` — Create a table from a dictionary that maps column names to column values.

## Properties

`column_count: int` — The number of columns.

`column_names: list[str]` — The names of the columns in the table.

`plot: TablePlotter` — Create interactive plots of this table.

`row_count: int` — The number of rows.

`schema: Schema` — The schema of the table.

`write: TableWriter` — Write this table to various targets.

## Dunder Methods

`__getitem__(self, name: str) -> Column` — Get the column with the specified name.

`__eq__(self, other: object) -> bool`

`__hash__(self) -> int`

`__repr__(self) -> str`

`__str__(self) -> str`

`__dataframe__(self, *, allow_copy: bool = True) -> DataFrame` — Return a dataframe object that conforms to the dataframe interchange protocol.

## Methods

### Column Operations

`add_columns(self, columns: Column | list[Column]) -> Table` — Add columns to the table and return the result as a new table.

`add_computed_column(self, name: str, mapper: Callable[[Row], Cell]) -> Table` — Add a computed column to the table and return the result as a new table.

`add_index_column(self, name: str, *, first_index: int = 0) -> Table` — Add an index column to the table and return the result as a new table.

`get_column(self, name: str) -> Column` — Get the column with the specified name.

`get_column_type(self, name: str) -> DataType` — Get the type of a column.

`has_column(self, name: str) -> bool` — Check if the table has a column with a specific name.

`remove_columns(self, selector: str | list[str], *, ignore_unknown_names: bool = False) -> Table` — Remove the specified columns from the table and return the result as a new table.

`remove_columns_with_missing_values(self, *, missing_value_ratio_threshold: float = 0) -> Table` — Remove columns with too many missing values and return the result as a new table.

`remove_non_numeric_columns(self) -> Table` — Remove non-numeric columns and return the result as a new table.

`rename_column(self, old_name: str, new_name: str) -> Table` — Rename a column and return the result as a new table.

`replace_column(self, old_name: str, new_columns: Column | list[Column] | Table) -> Table` — Replace a column with zero or more columns and return the result as a new table.

`select_columns(self, selector: str | list[str]) -> Table` — Select a subset of the columns and return the result as a new table.

`transform_columns(self, selector: str | list[str], mapper: Callable[[Cell], Cell] | Callable[[Cell, Row], Cell]) -> Table` — Transform columns with a custom function and return the result as a new table.

### Row Operations

`count_rows_if(self, predicate: Callable[[Row], Cell[bool | None]], *, ignore_unknown: bool = True) -> int | None` — Count how many rows in the table satisfy the predicate.

`filter_rows(self, predicate: Callable[[Row], Cell[bool | None]]) -> Table` — Keep only rows that satisfy a condition and return the result as a new table.

`filter_rows_by_column(self, name: str, predicate: Callable[[Cell], Cell[bool | None]]) -> Table` — Keep only rows that satisfy a condition on a specific column and return the result as a new table.

`remove_duplicate_rows(self) -> Table` — Remove duplicate rows and return the result as a new table.

`remove_rows(self, predicate: Callable[[Row], Cell[bool | None]]) -> Table` — Remove rows that satisfy a condition and return the result as a new table.

`remove_rows_by_column(self, name: str, predicate: Callable[[Cell], Cell[bool | None]]) -> Table` — Remove rows that satisfy a condition on a specific column and return the result as a new table.

`remove_rows_with_missing_values(self, *, selector: str | list[str] | None = None) -> Table` — Remove rows that contain missing values in the specified columns and return the result as a new table.

`remove_rows_with_outliers(self, *, selector: str | list[str] | None = None, z_score_threshold: float = 3) -> Table` — Remove rows that contain outliers in the specified columns and return the result as a new table.

`shuffle_rows(self, *, random_seed: int = 0) -> Table` — Shuffle the rows and return the result as a new table.

`slice_rows(self, *, start: int = 0, length: int | None = None) -> Table` — Slice the rows and return the result as a new table.

`sort_rows(self, key_selector: Callable[[Row], Cell], *, descending: bool = False) -> Table` — Sort the rows by a custom function and return the result as a new table.

`sort_rows_by_column(self, name: str, *, descending: bool = False) -> Table` — Sort the rows by a specific column and return the result as a new table.

`split_rows(self, percentage_in_first: float, *, shuffle: bool = True, random_seed: int = 0) -> tuple[Table, Table]` — Create two tables by splitting the rows of the current table.

### Table Operations

`add_tables_as_columns(self, others: Table | list[Table]) -> Table` — Add the columns of other tables and return the result as a new table.

`add_tables_as_rows(self, others: Table | list[Table]) -> Table` — Add the rows of other tables and return the result as a new table.

`join(self, right_table: Table, left_names: str | list[str], right_names: str | list[str], *, mode: Literal["inner", "left", "right", "full"] = "inner") -> Table` — Join the current table (left table) with another table (right table) and return the result as a new table.

### Statistics

`summarize_statistics(self) -> Table` — Return a table with important statistics about this table.

### Conversion

`to_columns(self) -> list[Column]` — Return the data of the table as a list of columns.

`to_dict(self) -> dict[str, list[object]]` — Return a dictionary that maps column names to column values.
