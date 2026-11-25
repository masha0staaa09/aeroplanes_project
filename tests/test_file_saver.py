import pytest
from src.aeroplane import Aeroplane
from src.file_saver import JSONFileSaver


def test_add_and_get_all(tmp_path):
    file_path = tmp_path / "aeroplanes.json"
    storage = JSONFileSaver(file_path)

    plane = Aeroplane("abc123", "CALL1", "Spain", 10000, 200)

    storage.add(plane)
    result = storage.get_all()

    assert len(result) == 1
    assert result[0].icao24 == "abc123"
    assert result[0].origin_country == "Spain"


def test_delete_existing_plane(tmp_path):
    file_path = tmp_path / "aeroplanes.json"
    storage = JSONFileSaver(file_path)

    plane = Aeroplane("abc123", "CALL1", "Spain", 10000, 200)
    storage.add(plane)

    result = storage.delete("abc123")

    assert result is True
    assert storage.get_all() == []


def test_delete_missing_plane(tmp_path):
    file_path = tmp_path / "aeroplanes.json"
    storage = JSONFileSaver(file_path)

    result = storage.delete("unknown")

    assert result is False


def test_get_all_empty_storage(tmp_path):
    file_path = tmp_path / "aeroplanes.json"
    storage = JSONFileSaver(file_path)

    assert storage.get_all() == []


def test_read_invalid_json(tmp_path):
    file_path = tmp_path / "aeroplanes.json"
    file_path.write_text("{invalid json}", encoding="utf-8")

    storage = JSONFileSaver(file_path)

    with pytest.raises(ValueError, match="Ошибка чтения JSON-файла"):
        storage.get_all()


def test_read_json_with_wrong_structure(tmp_path):
    file_path = tmp_path / "aeroplanes.json"

    file_path.write_text(
        '{"plane": "abc123"}',
        encoding="utf-8"
    )

    storage = JSONFileSaver(file_path)

    with pytest.raises(
        ValueError,
        match="Некорректная структура JSON-файла"
    ):
        storage.get_all()
