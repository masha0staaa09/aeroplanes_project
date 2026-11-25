class Aeroplane:

    def __init__(
        self,
        icao24: str,
        callsign: str | None,
        origin_country: str,
        altitude: float | None,
        velocity: float | None
    ):
        if not isinstance(icao24, str) or not icao24.strip():
            raise ValueError("Некорректный идентификатор самолёта")

        if not isinstance(origin_country, str) or not origin_country.strip():
            raise ValueError("Некорректная страна регистрации")

        if altitude is not None and (
                not isinstance(altitude, (int, float))
                or isinstance(altitude, bool)
        ):
            raise TypeError("Высота должна быть числом")

        if velocity is not None and (
                not isinstance(velocity, (int, float))
                or isinstance(velocity, bool)
        ):
            raise TypeError("Скорость должна быть числом")

        if velocity is not None and velocity < 0:
            raise ValueError("Скорость не может быть отрицательной")
        self.icao24 = icao24
        self.callsign = callsign
        self.origin_country = origin_country
        self.altitude = altitude
        self.velocity = velocity

    def compare_speed(self, other):
        if self.velocity is None or other.velocity is None:
            raise ValueError("Невозможно сравнить скорость")

        return self.velocity - other.velocity

    def compare_altitude(self, other):
        if self.altitude is None or other.altitude is None:
            raise ValueError("Невозможно сравнить высоту")

        return self.altitude - other.altitude

    def __lt__(self, other):
        if not isinstance(other, Aeroplane):
            return NotImplemented

        return self.compare_speed(other) < 0

    def __gt__(self, other):
        if not isinstance(other, Aeroplane):
            return NotImplemented

        return self.compare_speed(other) > 0

    def __eq__(self, other):
        if not isinstance(other, Aeroplane):
            return NotImplemented

        return (
                self.icao24 == other.icao24
        )

    @classmethod
    def cast_to_object_list(
            cls,
            data: list
    ) -> list["Aeroplane"]:
        aeroplanes = []

        for plane in data:
            aeroplane = cls(
                icao24=plane[0],
                callsign=plane[1],
                origin_country=plane[2],
                altitude=plane[7],
                velocity=plane[9]
            )

            aeroplanes.append(aeroplane)

        return aeroplanes
