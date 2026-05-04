# Column

Source: `src/portabellas/containers/_column.py`

## Constructor

`__init__(self, name: str, data: Sequence[T_co], *, type: DataType | None = None) -> None` — A named, one-dimensional collection of homogeneous values.

## Dunder Methods

`__contains__(self, value: object) -> bool`

`__eq__(self, other: object) -> bool`

`__getitem__(self, index: int) -> T_co`

`__getitem__(self, index: slice) -> Column[T_co]`

`__getitem__(self, index: int | slice) -> T_co | Column[T_co]`

`__hash__(self) -> int`

`__iter__(self) -> Iterator[T_co]`

`__len__(self) -> int`

`__repr__(self) -> str`

`__str__(self) -> str`

## Properties

`name: str` — The name of the column.

`row_count: int` — The number of rows.

`plot: ColumnPlotter` — Create interactive plots of this column.

`type: DataType` — The type of the column.

## Methods

### Access

`get_value(self, index: int) -> T_co` — Return the column value at the specified index.

`distinct_values(self, *, ignore_missing_values: bool = True) -> Sequence[T_co | None]` — Return the distinct values in the column.

`rename(self, new_name: str) -> Column[T_co]` — Rename the column and return the result as a new column.

### Transformation

`map(self, mapper: Callable[[Cell[T_co]], Cell]) -> Column` — Transform the values in the column and return the result as a new column.

### Quantifiers

`all(self, predicate: Callable[[Cell[T_co]], Cell[bool | None]], *, ignore_unknown: bool = True) -> bool | None` — Check whether all values in the column satisfy the predicate.

`any(self, predicate: Callable[[Cell[T_co]], Cell[bool | None]], *, ignore_unknown: bool = True) -> bool | None` — Check whether any value in the column satisfies the predicate.

`count_if(self, predicate: Callable[[Cell[T_co]], Cell[bool | None]], *, ignore_unknown: bool = True) -> int | None` — Count how many values in the column satisfy the predicate.

`none(self, predicate: Callable[[Cell[T_co]], Cell[bool | None]], *, ignore_unknown: bool = True) -> bool | None` — Check whether no value in the column satisfies the predicate.

### Descriptive Statistics

`max(self) -> T_co | None` — Return the maximum value in the column.

`mean(self) -> float` — Return the mean of the values in the column.

`median(self) -> float` — Return the median of the values in the column.

`min(self) -> T_co | None` — Return the minimum value in the column.

`mode(self, *, ignore_missing_values: bool = True) -> Sequence[T_co | None]` — Return the mode of the values in the column.

`standard_deviation(self) -> float` — Return the standard deviation of the values in the column.

`variance(self) -> float` — Return the variance of the values in the column.

`correlation_with(self, other: Column) -> float` — Calculate the Pearson correlation between this column and another column.

### Missing Values & Distinct Counts

`distinct_value_count(self, *, ignore_missing_values: bool = True) -> int` — Return the number of distinct values in the column.

`missing_value_count(self) -> int` — Return the number of missing values in the column.

### Statistics Summary

`summarize_statistics(self) -> Table` — Return a table with important statistics about the column.

### Conversion

`to_list(self) -> list[T_co]` — Return the values of the column in a list.

`to_table(self) -> Table` — Create a table that contains only this column.
