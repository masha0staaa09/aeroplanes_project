from abc import ABC, abstractmethod
import requests


class BaseAPI(ABC):

    @abstractmethod
    def get_country_coordinates(self, country: str) -> list[float]:
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str) -> list[list]:
        pass


class AeroplanesAPI(BaseAPI):

    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
    OPENSKY_URL = "https://opensky-network.org/api/states/all"

    def get_country_coordinates(self, country: str) -> list[float]:
        params = {
            "country": country,
            "format": "jsonv2",
            "featureType": "country"
        }

        headers = {
            "User-Agent": "AeroplanesCoursework/1.0"
        }

        try:
            response = requests.get(
                self.NOMINATIM_URL,
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

        except requests.RequestException as error:
            raise ConnectionError(
                f"Ошибка при обращении к Nominatim: {error}"
            ) from error

        if (
                not isinstance(data, list)
                or not data
                or not isinstance(data[0], dict)
                or "boundingbox" not in data[0]
        ):
            raise ValueError(f"Страна {country} не найдена")

        boundingbox = data[0]["boundingbox"]

        if not isinstance(boundingbox, list) or len(boundingbox) != 4:
            raise ValueError("Некорректные координаты страны")

        try:
            return [float(value) for value in boundingbox]
        except (TypeError, ValueError) as error:
            raise ValueError("Ошибка координат") from error

    def get_aeroplanes(self, country: str) -> list[list]:
        coordinates = self.get_country_coordinates(country)

        params = {
            "lamin": coordinates[0],
            "lamax": coordinates[1],
            "lomin": coordinates[2],
            "lomax": coordinates[3]
        }

        try:
            response = requests.get(
                self.OPENSKY_URL,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

        except requests.RequestException as error:
            raise ConnectionError(
                f"Ошибка при обращении к OpenSky: {error}"
            ) from error

        if not isinstance(data, dict):
            raise ValueError("Некорректный ответ OpenSky")

        states = data.get("states")

        if states is None:
            return []

        if not isinstance(states, list):
            raise ValueError("Некорректный список самолётов OpenSky")

        return states
