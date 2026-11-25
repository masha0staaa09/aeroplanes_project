from typing import Any
from abc import ABC, abstractmethod
import json
from pathlib import Path
from src.aeroplane import Aeroplane


class BaseFileSaver(ABC):

    @abstractmethod
    def add(self, aeroplane: Aeroplane) -> None:
        pass

    @abstractmethod
    def get_all(self) -> list[Aeroplane]:
        pass

    @abstractmethod
    def delete(self, icao24: str) -> bool:
        pass


class JSONFileSaver(BaseFileSaver):

    def __init__(self, file_path: str = "data/aeroplanes.json"):
        self.file_path = Path(file_path)

    def _read_data(self) -> list[dict[str, Any]]:
        if not self.file_path.exists():
            return []

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

        except json.JSONDecodeError as error:
            raise ValueError("Ошибка чтения JSON-файла") from error

        if not isinstance(data, list):
            raise ValueError("Некорректная структура JSON-файла")

        return data

    def _write_data(self, data: list[dict[str, Any]]) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add(self, aeroplane: Aeroplane) -> None:
        data = self._read_data()

        data.append({
            "icao24": aeroplane.icao24,
            "callsign": aeroplane.callsign,
            "origin_country": aeroplane.origin_country,
            "altitude": aeroplane.altitude,
            "velocity": aeroplane.velocity
        })

        self._write_data(data)

    def get_all(self) -> list[Aeroplane]:
        data = self._read_data()

        return [
            Aeroplane(
                icao24=plane["icao24"],
                callsign=plane["callsign"],
                origin_country=plane["origin_country"],
                altitude=plane["altitude"],
                velocity=plane["velocity"]
            )
            for plane in data
        ]

    def delete(self, icao24: str) -> bool:
        data = self._read_data()

        filtered_data = [
            plane for plane in data
            if plane["icao24"] != icao24
        ]

        if len(data) == len(filtered_data):
            return False

        self._write_data(filtered_data)
        return True
