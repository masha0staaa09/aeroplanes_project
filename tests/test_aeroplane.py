import pytest
from src.aeroplane import Aeroplane


def test_create_aeroplane():
    plane = Aeroplane("abc123", "CALL1", "Spain", 10000, 200)

    assert plane.icao24 == "abc123"
    assert plane.callsign == "CALL1"
    assert plane.origin_country == "Spain"
    assert plane.altitude == 10000
    assert plane.velocity == 200


def test_invalid_icao24():
    with pytest.raises(ValueError):
        Aeroplane("", "CALL1", "Spain", 10000, 200)


def test_invalid_country():
    with pytest.raises(ValueError):
        Aeroplane("abc123", "CALL1", "", 10000, 200)


def test_invalid_altitude():
    with pytest.raises(TypeError):
        Aeroplane("abc123", "CALL1", "Spain", "high", 200)


def test_invalid_velocity():
    with pytest.raises(TypeError):
        Aeroplane("abc123", "CALL1", "Spain", 10000, "fast")


def test_negative_velocity():
    with pytest.raises(ValueError):
        Aeroplane("abc123", "CALL1", "Spain", 10000, -200)


def test_compare_speed():
    plane1 = Aeroplane("abc123", "CALL1", "Spain", 10000, 200)
    plane2 = Aeroplane("abc456", "CALL2", "France", 15000, 300)

    assert plane1.compare_speed(plane2) == -100


def test_compare_altitude():
    plane1 = Aeroplane("abc123", "CALL1", "Spain", 10000, 200)
    plane2 = Aeroplane("abc456", "CALL2", "France", 15000, 300)

    assert plane1.compare_altitude(plane2) == -5000


def test_equal_aeroplanes():
    plane1 = Aeroplane("abc123", "CALL1", "Spain", 10000, 200)
    plane2 = Aeroplane("abc123", "CALL2", "France", 15000, 300)

    assert plane1 == plane2


def test_less_than():
    plane1 = Aeroplane("abc123", "CALL1", "Spain", 10000, 200)
    plane2 = Aeroplane("abc456", "CALL2", "France", 15000, 300)

    assert plane1 < plane2


def test_greater_than():
    plane1 = Aeroplane("abc123", "CALL1", "Spain", 10000, 300)
    plane2 = Aeroplane("abc456", "CALL2", "France", 15000, 200)

    assert plane1 > plane2
