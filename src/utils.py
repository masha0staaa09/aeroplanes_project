from src.aeroplane import Aeroplane


def get_top_by_altitude(
    aeroplanes: list[Aeroplane],
    count: int
) -> list[Aeroplane]:

    if count <= 0:
        raise ValueError("Количество самолётов должно быть больше нуля")

    planes_with_altitude = [
        plane for plane in aeroplanes
        if plane.altitude is not None
    ]

    sorted_aeroplanes = sorted(
        planes_with_altitude,
        key=lambda plane: plane.altitude or 0,
        reverse=True
    )

    return sorted_aeroplanes[:count]


def filter_by_country(
    aeroplanes: list[Aeroplane],
    country: str
) -> list[Aeroplane]:

    return [
        plane for plane in aeroplanes
        if plane.origin_country.lower() == country.strip().lower()
    ]
