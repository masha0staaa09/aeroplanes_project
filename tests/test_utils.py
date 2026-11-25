import pytest
from src.aeroplane import Aeroplane
from src.utils import get_top_by_altitude, filter_by_country


def test_get_top_by_altitude():
    plane1 = Aeroplane("abc123", "CALL1", "Spain", 10000, 200)
    plane2 = Aeroplane("abc456", "CALL2", "France", 15000, 250)
    plane3 = Aeroplane("abc789", "CALL3", "Germany", 5000, 180)

    aeroplanes = [plane1, plane2, plane3]

    result = get_top_by_altitude(aeroplanes, 2)

    assert len(result) == 2
    assert result[0] == plane2
    assert result[1] == plane1


def test_filter_by_country():
    plane1 = Aeroplane("abc123", "CALL1", "Spain", 10000, 200)
    plane2 = Aeroplane("abc456", "CALL2", "France", 15000, 250)
    plane3 = Aeroplane("abc789", "CALL3", "Spain", 5000, 180)

    aeroplanes = [plane1, plane2, plane3]

    result = filter_by_country(aeroplanes, "Spain")

    assert len(result) == 2
    assert plane1 in result
    assert plane3 in result


def test_get_top_by_altitude_invalid_count():
    with pytest.raises(ValueError):
        get_top_by_altitude([], 0)
