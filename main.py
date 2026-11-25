from src.api import AeroplanesAPI
from src.aeroplane import Aeroplane
from src.file_saver import JSONFileSaver
from src.utils import get_top_by_altitude, filter_by_country


api = AeroplanesAPI()
storage = JSONFileSaver()

while True:
    country = input("Введите страну для поиска самолётов: ")

    try:
        raw_aeroplanes = api.get_aeroplanes(country)
        aeroplanes = Aeroplane.cast_to_object_list(raw_aeroplanes)

        for plane in aeroplanes:
            storage.add(plane)

        break

    except ValueError:

        print("Такую страну не удалось найти. Попробуйте ещё раз.")

    except ConnectionError as error:

        print(f"Не удалось подключиться к серверу: {error}")
print(f"Найдено самолётов: {len(aeroplanes)}")

while True:
    print("\nВыберите действие:")
    print("1 — Показать самолёты с наибольшей высотой")
    print("2 — Найти самолёты по стране регистрации")
    print("0 — Выход")

    choice = input("Ваш выбор: ")

    if choice == "1":
        while True:
            try:
                count = int(input("Сколько самолётов показать? "))

                if count <= 0:
                    print("Введите положительное число.")
                    continue

                break

            except ValueError:
                print("Нужно ввести целое число. Попробуйте ещё раз.")

        top_aeroplanes = get_top_by_altitude(aeroplanes, count)

        for plane in top_aeroplanes:
            print(
                f"Самолёт: {plane.icao24}, "
                f"Страна: {plane.origin_country}, "
                f"Высота: {plane.altitude} м"
            )
    elif choice == "2":

        while True:

            registration_country = input(

                "Введите страну регистрации самолёта: "

            )

            filtered_aeroplanes = filter_by_country(

                aeroplanes,

                registration_country

            )

            if filtered_aeroplanes:
                break

            print(

                "Самолётов с такой страной регистрации не найдено. "

                "Попробуйте ещё раз."

            )

        print(f"Найдено самолётов: {len(filtered_aeroplanes)}")

        for plane in filtered_aeroplanes:
            print(

                f"Самолёт: {plane.icao24}, "

                f"Высота: {plane.altitude} м, "

                f"Скорость: {plane.velocity} м/с"

            )

    elif choice == "0":

        print("Программа завершена.")

        break
    else:
        print("Неверный выбор. Выберите 1, 2 или 0.")
