from unittest.mock import Mock, patch
import pytest
import requests
from src.api import AeroplanesAPI


def test_get_country_coordinates():
    api = AeroplanesAPI()

    mock_response = Mock()
    mock_response.json.return_value = [
        {
            "boundingbox": [
                "35.0", "44.0", "-10.0", "5.0"
            ]
        }
    ]

    with patch("src.api.requests.get", return_value=mock_response):
        result = api.get_country_coordinates("Spain")

    assert result == [35.0, 44.0, -10.0, 5.0]


def test_country_not_found():
    api = AeroplanesAPI()

    mock_response = Mock()
    mock_response.json.return_value = []

    with patch("src.api.requests.get", return_value=mock_response):
        with pytest.raises(ValueError):
            api.get_country_coordinates("UnknownCountry")


def test_get_aeroplanes():
    api = AeroplanesAPI()

    mock_response = Mock()
    mock_response.json.return_value = {
        "states": [["abc123", "CALL1", "Spain"]]
    }

    with patch.object(
        api,
        "get_country_coordinates",
        return_value=[35.0, 44.0, -10.0, 5.0]
    ):
        with patch(
            "src.api.requests.get",
            return_value=mock_response
        ):
            result = api.get_aeroplanes("Spain")

    assert result == [["abc123", "CALL1", "Spain"]]


def test_get_country_coordinates_connection_error():
    api = AeroplanesAPI()

    with patch(
        "src.api.requests.get",
        side_effect=requests.ConnectionError
    ):
        with pytest.raises(ConnectionError):
            api.get_country_coordinates("Spain")


def test_get_aeroplanes_connection_error():
    api = AeroplanesAPI()

    with patch.object(
        api,
        "get_country_coordinates",
        return_value=[35.0, 44.0, -10.0, 5.0]
    ):
        with patch(
            "src.api.requests.get",
            side_effect=requests.ConnectionError
        ):
            with pytest.raises(ConnectionError):
                api.get_aeroplanes("Spain")
