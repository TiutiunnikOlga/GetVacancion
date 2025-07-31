import pytest
import requests
from unittest.mock import MagicMock, patch
from src.classes import HH


class TestHH(HH):
    def __init__(self, file_worker, page=0):  # Добавляем параметр page
        self.url = "https://api.hh.ru/vacancies"
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {
            "text": "",
            "page": page,
            "per_page": 100,
        }  # Используем page из параметров
        self.vacancies = []
        self.file_worker = file_worker

    def work(self):
        pass


@pytest.fixture
def hh_instance():
    return TestHH(file_worker=MagicMock(), page=0)  # Передаем page=0


@pytest.mark.parametrize("keyword, expected_count", [("python", 40), ("java", 40)])
def test_load_vacancies_success(hh_instance, keyword, expected_count):
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"items": [{"id": 1}, {"id": 2}]}
        mock_get.return_value = mock_response

        hh_instance.load_vacancies(keyword)

        # Исправленный вариант проверки
        mock_get.assert_called_with(
            "https://api.hh.ru/vacancies",
            headers={"User-Agent": "HH-User-Agent"},
            params={
                "text": keyword,
                "per_page": 100,
                "page": hh_instance.params[
                    "page"
                ],  # Проверяем значение page из инстанса
            },
        )
        assert len(hh_instance.vacancies) == expected_count


def test_load_vacancies_empty(hh_instance):
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        hh_instance.load_vacancies("nonexistent")
        assert len(hh_instance.vacancies) == 0


def test_load_vacancies_error(hh_instance):
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        try:
            hh_instance.load_vacancies("test")
        except requests.exceptions.RequestException:
            pass  # Ожидаем исключение
        assert len(hh_instance.vacancies) == 0


def test_work_method(hh_instance):
    result = hh_instance.work()
    assert result is None


if __name__ == "__main__":
    pytest.main()
