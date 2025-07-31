from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from src.utils import fetch_vacancies, load_vacancies_from_file, save_to_json


def test_fetch_vacancies_success():
    with patch("src.utils.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "found": 100,
            "items": [
                {
                    "name": "Python Developer",
                    "employer": {"name": "Company"},
                    "salary": {"from": 100000, "to": 200000},
                }
            ],
        }

        # Вызываем функцию
        result = fetch_vacancies()

        # Проверяем результат
        assert "items" in result
        assert len(result["items"]) > 0


def test_save_to_json():
    data = {"test": "data"}
    with patch("builtins.open", new_callable=mock_open) as mock_file:
        save_to_json(data, "test_file")
        mock_file.assert_called_once_with(
            Path("data/test_file.json"), "w", encoding="utf-8"
        )
        mock_file().write.assert_called()


def test_load_vacancies_from_file_invalid_format():
    with patch("builtins.open", mock_open(read_data='{"invalid": "data"}')):
        result = load_vacancies_from_file("test.json")
        assert result == []


def test_load_vacancies_from_file_not_exists():
    with patch("pathlib.Path.exists", return_value=False):
        result = load_vacancies_from_file("non_existent.json")
        assert result == []


def test_load_vacancies_from_file_json_error():
    with patch("builtins.open", mock_open(read_data="invalid json")):
        result = load_vacancies_from_file("test.json")
        assert result == []


if __name__ == "__main__":
    pytest.main()
