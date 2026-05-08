from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal

import pytest

from portabellas.typing import DataTypes
from portabellas.typing._type_inference import infer_type_from_literal


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(True, DataTypes.Boolean(), id="bool_true"),
        pytest.param(False, DataTypes.Boolean(), id="bool_false"),
        pytest.param(42, DataTypes.Int32(), id="int"),
        pytest.param(3.14, DataTypes.Float64(), id="float"),
        pytest.param("hello", DataTypes.String(), id="str"),
        pytest.param(date(2024, 1, 1), DataTypes.Date(), id="date"),
        pytest.param(datetime(2024, 1, 1, 12, 0, tzinfo=UTC), DataTypes.Datetime(time_unit="us"), id="datetime"),
        pytest.param(time(12, 0), DataTypes.Time(), id="time"),
        pytest.param(timedelta(days=1), DataTypes.Duration(time_unit="us"), id="timedelta"),
        pytest.param(None, DataTypes.Null(), id="none"),
        pytest.param(Decimal("1.5"), DataTypes.Unknown(), id="decimal"),
        pytest.param(b"bytes", DataTypes.Binary(), id="bytes"),
        pytest.param(object(), DataTypes.Unknown(), id="arbitrary_object"),
    ],
)
def test_should_infer_type_from_literal(value: object, expected: DataTypes.Unknown | type[DataTypes]) -> None:
    assert infer_type_from_literal(value) == expected
